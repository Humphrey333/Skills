"""Readers for the older Chromatix layout (Spectra 480, SM8250 / SDM865).

Differences from the Spectra 680/780 layout read by qcom.py:
- regions are `<blockNN_rgn_data>`, not `<region>`;
- triggers are named children (`cct_trigger`, `aec_trigger` with lux_idx_*/gain_*,
  `led_idx_trigger`, `drc_gain_trigger`, `hdr_aec_trigger`);
- block versions: IFE/lsc34 (per CCT and gain), IPE/cc13 (per CCT and lux),
  IPE/gamma15 (`table`, 257 pts, 10-bit), IFE/linearization34 (black level as the
  first knee of a 14-bit LUT; IFE/bls12 is disabled in the IMX577/IMX412 project).

Every reader returns a list of dicts with a `trig` dict so the caller picks.
"""
import os
import xml.etree.ElementTree as ET

import numpy as np


def _nums(el):
    return np.array([float(v) for v in el.text.split()])


def _trig(t):
    """Trigger element -> dict of named ranges."""
    def num(s):
        try:
            return float(s)
        except (TypeError, ValueError):
            return (s or "").strip()      # e.g. anr10 pass trigger "PASS_FULL"
    if len(t) == 0:
        return {t.tag.replace("_trigger", ""): num(t.text)}
    kids = {c.tag: num(c.text) for c in t}
    name = t.tag.replace("_trigger", "")
    out = {}
    if "start" in kids:
        out[name] = (kids["start"], kids["end"])
    for k in ("lux_idx", "gain", "exp_time", "aec_sensitivity", "exp_gain"):
        if f"{k}_start" in kids:
            out[k] = (kids[f"{k}_start"], kids[f"{k}_end"])
    return out


def regions(path):
    """Yield (trig dict, rgn element) for every *_rgn_data in a block file."""
    root = ET.parse(path).getroot()

    def walk(node, trig):
        t = [c for c in node if c.tag.endswith("_trigger")]
        if t:
            trig = {**trig, **_trig(t[0])}
        for c in node:
            if c.tag.endswith("_rgn_data"):
                yield trig, c
            elif not c.tag.endswith("_trigger"):
                yield from walk(c, trig)

    core = next(el for el in root if el.tag.endswith("_core"))
    yield from walk(core, {})


def is_480(xml_dir):
    return os.path.exists(os.path.join(xml_dir, "IFE/lsc34_ife.xml")) and \
        os.path.exists(os.path.join(xml_dir, "IPE/cc13_ipe.xml"))


def lsc34(xml_dir, rows=13, cols=17):
    out = []
    for t, r in regions(os.path.join(xml_dir, "IFE/lsc34_ife.xml")):
        d = {"trig": t}
        for ch in ("r", "gr", "gb", "b"):
            d[ch] = _nums(r.find(f"{ch}_gain_tab/{ch}_gain")).reshape(rows, cols)
        out.append(d)
    return out


def cc13(xml_dir):
    """IPE/cc13 CCMs, rows = output R,G,B (rows sum to 1)."""
    return [{"trig": t, "cct": t.get("cct"), "ccm": _nums(r.find("c_tab/c")).reshape(3, 3)}
            for t, r in regions(os.path.join(xml_dir, "IPE/cc13_ipe.xml"))]


def gamma15(xml_dir, full_scale=1023.0):
    """IPE/gamma15 curves. One `table` per channel; the first of each region is used."""
    return [{"trig": t, "lux": t.get("lux_idx"), "g": _nums(r.find("table")) / full_scale}
            for t, r in regions(os.path.join(xml_dir, "IPE/gamma15_ipe.xml"))]


def black_14bit(xml_dir):
    """Black level from IFE/linearization34: first knee of r_lut_p (14-bit domain).

    Returns (value, bits). IFE/bls12 offset is used instead when it is non-zero.
    """
    for t, r in regions(os.path.join(xml_dir, "IFE/bls12_ife.xml")):
        off = float(r.find("offset").text)
        if off:
            return off, 14
        break
    for t, r in regions(os.path.join(xml_dir, "IFE/linearization34_ife.xml")):
        return float(r.find("r_lut_p_tab/r_lut_p").text.split()[0]), 14
