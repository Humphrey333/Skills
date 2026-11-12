"""argus_isp: build or edit a Jetson Argus camera_overrides.isp.

Subcommands
  inspect-qcom XML_DIR            list Chromatix regions, CCMs, gamma fits, black level
  build-qcom   XML_DIR -o OUT      port LSC + CCM + gamma + black level into a .isp
  set-ccm      ISP -o OUT          replace only colorCorrection.srgbMatrix
  set-gamma    ISP -o OUT          replace only tc.* (Gamma.Value in every preset)
  check        ISP [--ref ISP]     structure and colour invariants, diff vs a reference

Run `python3 argus_isp.py <cmd> -h` for options.
"""
import argparse
import sys

import numpy as np

from . import bezier, color, qcom, qcom480
from .isp_file import IspFile, black_lines, ccm_lines, lsc_lines, tc_gamma_lines

np.set_printoptions(precision=4, suppress=True)


def _pick_ccm(xml_dir, region):
    """First CCM whose CCT range equals `region` (Spectra 480: first = bright lux, no LED)."""
    lo, hi = (float(v) for v in region.split("-"))
    src = qcom480.cc13(xml_dir) if qcom480.is_480(xml_dir) else qcom.cc14(xml_dir)
    for c in src:
        if tuple(c["cct"]) == (lo, hi):
            return c["ccm"]
    sys.exit(f"no CCM region {region}; run inspect-qcom")


def _lsc_tables(xml_dir, gain, ccts):
    """One normalised table set per Argus ctrlPoint CCT.

    Spectra 780 (lsc42) has one table: reused for every ctrlPoint.
    Spectra 480 (lsc34) has tables per CCT band and gain band: for each Argus
    CCT take the band containing it (else the nearest band centre) at `gain`.
    """
    if not qcom480.is_480(xml_dir):
        reg = qcom.lsc42(xml_dir)[0]
        return [(reg, "lsc42 single table")] * len(ccts)
    glo, ghi = (float(v) for v in gain.split("-"))
    cand = [d for d in qcom480.lsc34(xml_dir)
            if d["trig"].get("gain") == (glo, ghi) and d["trig"].get("led_idx", 0) == 0]
    if not cand:
        sys.exit(f"lsc34 has no gain band {gain}; run inspect-qcom")
    out = []
    for cct in ccts:
        best = min(cand, key=lambda d: 0 if d["trig"]["cct"][0] <= cct <= d["trig"]["cct"][1]
                   else abs(sum(d["trig"]["cct"]) / 2 - cct))
        out.append((best, f"lsc34 gain {gain} cct {best['trig']['cct']}"))
    return out


def _ccm(args):
    """Resolve the CCM options shared by build-qcom and set-ccm."""
    if args.matrix:
        return np.array(args.matrix, float).reshape(3, 3)
    m = None
    if args.qcom:
        m = color.qcom_to_argus(_pick_ccm(args.qcom, args.ccm_region))
    if args.ccm_mode == "transpose":
        return m
    if args.ccm_mode == "identity":
        return color.blend_identity(m, args.k)
    if args.ccm_mode == "grey":
        base = IspFile.read(args.ccm_base).matrix()
        if base is None:
            sys.exit(f"{args.ccm_base} has no colorCorrection.srgbMatrix")
        return color.grey_preserving(base, m, args.k)
    if args.ccm_mode == "none":
        return None
    if args.ccm_mode == "copy":
        return IspFile.read(args.ccm_base).matrix()
    sys.exit(f"unknown --ccm-mode {args.ccm_mode}")


def cmd_inspect(a):
    if qcom480.is_480(a.xml):
        return _inspect_480(a)
    for d in qcom.lsc42(a.xml):
        print("lsc42 region", d["path"][-2:], "gr centre", d["gr"][6, 8],
              "corner/centre R,GR,B", [round(float(d[c].max() / d[c][6, 8]), 3) for c in ("r", "gr", "b")])
    for c in qcom.cc14(a.xml):
        print("cc14 CCT", c["cct"], "rows\n", c["ccm"])
    for g in qcom.gamma15(a.xml):
        print("gamma15 lux", g["lux"], "log fit", round(color.gamma_power_fit(g["g"]), 3),
              "linear fit", round(color.gamma_power_fit_linear(g["g"]), 3))
    off = qcom.bls12_offset(a.xml)
    print("bls12 offset", off, "-> Argus", color.black_level(off, a.offset_bits, a.sensor_bits))


def _inspect_480(a):
    print("layout: Spectra 480 (lsc34 / cc13 / gamma15 table / linearization34)")
    for d in qcom480.lsc34(a.xml):
        t, s = d["trig"], d["gr"][6, 8]
        print("lsc34 gain", t.get("gain"), "cct", t.get("cct"), "led", t.get("led_idx"),
              "corner/centre R,GR,B", [round(float(d[c].max() / d[c][6, 8]), 2) for c in ("r", "gr", "b")])
    for c in qcom480.cc13(a.xml):
        print("cc13 led", c["trig"].get("led_idx"), "lux", c["trig"].get("lux_idx"), "cct", c["cct"], "rows", c["ccm"].round(4).tolist())
    for g in qcom480.gamma15(a.xml)[::3]:
        print("gamma15 led", g["trig"].get("led_idx"), "lux", g["lux"], "log fit", round(color.gamma_power_fit(g["g"]), 3),
              "linear fit", round(color.gamma_power_fit_linear(g["g"]), 3))
    off, bits = qcom480.black_14bit(a.xml)
    print("black", off, f"@{bits}-bit -> Argus", color.black_level(off, bits, a.sensor_bits))


def cmd_build(a):
    out = IspFile.read(a.base) if a.base else IspFile([])
    notes = [f"VARIANT {a.variant}", "", f"Built by argus_isp build-qcom from {a.xml}", ""]
    # lens shading
    ccts = ((2856, 1), (4000, 2), (6500, 1))
    ctrls, errs, srcs = [], [], []
    for reg, src in _lsc_tables(a.xml, a.lsc_gain, [c for c, _ in ccts]):
        scale = reg["gr"][reg["gr"].shape[0] // 2, reg["gr"].shape[1] // 2]
        ctrl = {}
        for ch in ("r", "gr", "gb", "b"):
            src_ch = "gr" if a.lsc_colour == "luma" else ch
            c, mx, rms = bezier.fit(reg[src_ch] / scale)
            ctrl[ch.upper()] = c
            errs.append((mx, rms))
        ctrls.append(ctrl)
        srcs.append(src)
    mx, rms = max(e[0] for e in errs), max(e[1] for e in errs)
    vmax = max(float(c[ch].max()) for c in ctrls for ch in c)
    out.replace_group("lensShading.", lsc_lines(ctrls, a.width, a.height, ccts))
    out.replace_group("ap15Function.lensShading",
                      [f"ap15Function.lensShading = {'FALSE' if a.lsc_off else 'TRUE'};"])
    notes.append(f"lens shading  10x10 Bezier per ctrlPoint, centre Gr = 1, fit max {mx:.1%} rms {rms:.1%}, max ctrl {vmax:.2f}")
    if a.lsc_colour == "luma":
        notes.append("                LUMA ONLY: Gr fit written to R/GR/GB/B (vendor colour shading dropped)")
    if a.lsc_off:
        notes.append("                ap15Function.lensShading = FALSE: LSC keys kept but not applied")
    for (cct, _), src in zip(ccts, srcs):
        notes.append(f"                ctrlPoint cct {cct} <- {src}")
    # CCM
    m = _ccm(a)
    if m is None:
        out.replace_group("colorCorrection.srgbMatrix", [])
        notes.append("CCM           none: no colorCorrection key, Argus default matrix")
    else:
        out.replace_group("colorCorrection.srgbMatrix", ccm_lines(m), anchor_after="ap15Function")
        notes.append(f"CCM           mode {a.ccm_mode}, k {a.k}, region {a.ccm_region}, base {a.ccm_base}, col sums {m.sum(0).round(4)}")
    # tone
    if a.gamma == "auto":
        g = (qcom480.gamma15(a.xml) if qcom480.is_480(a.xml) else qcom.gamma15(a.xml))[0]["g"]
        gamma = round(color.gamma_power_fit(g), 2)
    else:
        gamma = float(a.gamma)
    out.replace_group("tc.", tc_gamma_lines(gamma), anchor_after="colorCorrection.srgbMatrix")
    notes.append(f"tone          tc.v2 Gamma.Value {gamma:.2f} in all presets")
    # black level
    if qcom480.is_480(a.xml):
        off, bits = qcom480.black_14bit(a.xml)
    else:
        off, bits = qcom.bls12_offset(a.xml), a.offset_bits
    ival, fval = color.black_level(off, bits, a.sensor_bits)
    out.replace_group("opticalBlack.", black_lines(ival, fval))
    notes.append(f"black level   opticalBlack {ival} / {fval:.8f}")
    notes += ["", "NOT PORTED (Argus defaults): AWB, NR, sharpening, AE, LTM/GTM.",
              "UNVERIFIED: CCM channel order, LSC row orientation, LSC scaling to other modes."]
    out.set_header(notes + (a.note or []))
    out.write(a.out)
    print(f"wrote {a.out}")


def cmd_set_ccm(a):
    f = IspFile.read(a.isp)
    m = _ccm(a)
    f.replace_group("colorCorrection.srgbMatrix", ccm_lines(m), anchor_after="ap15Function")
    f.write(a.out)
    print(f"wrote {a.out}\n{m}\ncol sums {m.sum(0).round(4)}")


def cmd_set_gamma(a):
    f = IspFile.read(a.isp)
    f.replace_group("tc.", tc_gamma_lines(a.gamma), anchor_after="colorCorrection.srgbMatrix")
    f.write(a.out)
    print(f"wrote {a.out}")


def cmd_check(a):
    f = IspFile.read(a.isp)
    ok = True
    m = f.matrix()
    if m is not None:
        print("CCM\n", m, "\ncol sums", m.sum(0).round(4), "diag", np.diag(m).round(4))
    n = int(f.get("lensShading.ctrlPointsCount") or 0)
    for p in range(n):
        cnt = sum(1 for ln in f.lines if (f.key_of(ln) or "").startswith(f"lensShading.ctrlPoints[{p}].controlPoint"))
        vals = [float(f.get(k)) for k in (f.key_of(ln) for ln in f.lines)
                if k and k.startswith(f"lensShading.ctrlPoints[{p}].controlPoint")]
        print(f"LSC ctrlPoint {p}: {cnt} values (want 400), range {min(vals):.3f}..{max(vals):.3f}")
        ok &= cnt == 400
    print("ap15Function.lensShading =", f.get("ap15Function.lensShading"),
          "| Gamma.Value =", f.get("tc.v2.user.presets[0].Gamma.Value"),
          "| opticalBlack =", f.get("opticalBlack.manualBiasR"))
    if a.ref:
        r = IspFile.read(a.ref)
        fk = {f.key_of(ln): f.get(f.key_of(ln)) for ln in f.lines if f.key_of(ln)}
        rk = {r.key_of(ln): r.get(r.key_of(ln)) for ln in r.lines if r.key_of(ln)}
        diff = [k for k in fk.keys() | rk.keys() if not _same(fk.get(k), rk.get(k), a.tol)]
        exp = tuple(a.expect or ())
        unexpected = [k for k in diff if not (exp and k.startswith(exp))]
        print(f"keys differing from {a.ref} (tol {a.tol}): {len(diff)}, "
              f"expected by --expect {list(exp)}: {len(diff) - len(unexpected)}, unexpected: {len(unexpected)}")
        for k in sorted(diff)[:40]:
            print(f"  {'ok ' if k not in unexpected else 'BAD'} {k}: {rk.get(k)} -> {fk.get(k)}")
        if exp and len(diff) == len(unexpected):
            print("  no key under --expect changed: the edit did nothing")
            ok = False
        ok &= not unexpected
    print("CHECK", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def _same(x, y, tol):
    if x == y:
        return True
    if x is None or y is None:
        return False
    try:
        xs = [float(v) for v in x.strip("{} ").split(",")]
        ys = [float(v) for v in y.strip("{} ").split(",")]
        return len(xs) == len(ys) and all(abs(p - q) <= tol for p, q in zip(xs, ys))
    except ValueError:
        return x.upper() == y.upper()


def _ccm_opts(p):
    p.add_argument("--qcom", help="Chromatix XML dir for the CCM source")
    p.add_argument("--ccm-region", default="5500-7000", help="cc14 CCT region, e.g. 5500-7000")
    p.add_argument("--ccm-mode", default="grey", choices=["transpose", "identity", "grey", "copy", "none"],
                   help="transpose = vendor CCM as is; identity = I+k(M-I); "
                        "grey = (I+k(M-I)) @ base CCM (keeps base white balance); copy = base CCM; "
                        "none = remove the CCM keys (Argus default)")
    p.add_argument("--ccm-base", help=".isp whose CCM is known good on the board (grey/copy modes)")
    p.add_argument("-k", type=float, default=0.15, help="vendor saturation share")
    p.add_argument("--matrix", type=float, nargs=9, help="explicit Argus matrix, 9 values row by row")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="argus_isp", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("inspect-qcom")
    p.add_argument("xml")
    p.add_argument("--offset-bits", type=int, default=18, help="BLS offset bit depth (Spectra 780: 18)")
    p.add_argument("--sensor-bits", type=int, default=10)
    p.set_defaults(fn=cmd_inspect)

    p = sp.add_parser("build-qcom")
    p.add_argument("xml")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--base", help="existing .isp to edit; its other keys are kept")
    p.add_argument("--variant", required=True, help="variant name for the header")
    p.add_argument("--note", action="append", help="extra header line (repeatable)")
    p.add_argument("--width", type=int, default=4000)
    p.add_argument("--height", type=int, default=3000)
    p.add_argument("--lsc-gain", default="1-4", help="Spectra 480 lsc34 gain band, e.g. 1-4")
    p.add_argument("--lsc-colour", default="table", choices=["table", "luma"],
                   help="table = vendor per-channel shading; luma = Gr shading on all channels (no colour shading)")
    p.add_argument("--lsc-off", action="store_true", help="write ap15Function.lensShading = FALSE")
    p.add_argument("--gamma", default="auto", help="'auto' = log-space fit of gamma15 region 0, or a value")
    p.add_argument("--offset-bits", type=int, default=18)
    p.add_argument("--sensor-bits", type=int, default=10)
    _ccm_opts(p)
    p.set_defaults(fn=cmd_build, qcom=None)

    p = sp.add_parser("set-ccm")
    p.add_argument("isp")
    p.add_argument("-o", "--out", required=True)
    _ccm_opts(p)
    p.set_defaults(fn=cmd_set_ccm)

    p = sp.add_parser("set-gamma")
    p.add_argument("isp")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--gamma", type=float, required=True)
    p.set_defaults(fn=cmd_set_gamma)

    p = sp.add_parser("check")
    p.add_argument("isp")
    p.add_argument("--ref")
    p.add_argument("--tol", type=float, default=0.0)
    p.add_argument("--expect", action="append",
                   help="key prefix allowed to differ from --ref (repeatable), e.g. colorCorrection.srgbMatrix")
    p.set_defaults(fn=cmd_check)

    a = ap.parse_args(argv)
    if a.cmd == "build-qcom" and a.qcom is None:
        a.qcom = a.xml
    a.fn(a)


if __name__ == "__main__":
    main()
