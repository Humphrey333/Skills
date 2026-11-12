"""Read, edit and write an Argus camera_overrides.isp as ordered lines.

Edits replace whole key groups (all lines whose key starts with a prefix) at
the position of the first old line, so the rest of the file stays byte-equal.
Line formats copy the files that worked on the Jetson.
"""
import re

import numpy as np

KEY = re.compile(r"^\s*([A-Za-z_][\w.\[\]]*)\s*=")


class IspFile:
    def __init__(self, lines=None):
        self.lines = list(lines or [])

    @classmethod
    def read(cls, path):
        with open(path) as f:
            return cls(f.read().split("\n"))

    def write(self, path):
        with open(path, "w") as f:
            f.write("\n".join(self.lines))

    # ---- queries -------------------------------------------------------
    def key_of(self, line):
        m = KEY.match(line)
        return m.group(1) if m else None

    def get(self, key):
        for ln in self.lines:
            if self.key_of(ln) == key:
                return ln.split("=", 1)[1].strip().rstrip(";").strip()
        return None

    def matrix(self, prefix="colorCorrection.srgbMatrix"):
        rows = [ln for ln in self.lines if (self.key_of(ln) or "").startswith(prefix)]
        if not rows:
            return None
        return np.array([[float(v) for v in re.search(r"\{(.*)\}", r).group(1).split(",")]
                         for r in rows])

    # ---- edits ---------------------------------------------------------
    def replace_group(self, prefix, new_lines, anchor_after=None):
        """Drop every line whose key starts with `prefix`, put `new_lines` there.

        If no such line exists, insert after the last line whose key starts
        with `anchor_after`, else append at the end.
        """
        idx = [i for i, ln in enumerate(self.lines) if (self.key_of(ln) or "").startswith(prefix)]
        if idx:
            at = idx[0]
            self.lines = [ln for i, ln in enumerate(self.lines) if i not in set(idx)]
        else:
            at = len(self.lines)
            if anchor_after:
                hits = [i for i, ln in enumerate(self.lines)
                        if (self.key_of(ln) or "").startswith(anchor_after)]
                if hits:
                    at = hits[-1] + 1
        self.lines[at:at] = list(new_lines)

    def set_header(self, comment_lines):
        """Replace the leading '#' comment block (or add one)."""
        n = 0
        while n < len(self.lines) and self.lines[n].startswith("#"):
            n += 1
        self.lines[0:n] = ["#" + "=" * 74] + ["# " + c if c else "#" for c in comment_lines] + ["#" + "=" * 74]


# ---- line builders (exact formats of the working IMX586 file) -----------
def ccm_lines(m):
    return [f"colorCorrection.srgbMatrix[{r}]\t = {{{m[r, 0]:.8f}, {m[r, 1]:.8f}, {m[r, 2]:.8f}}};"
            for r in range(3)]


def tc_gamma_lines(gamma, presets=9):
    out = ["tc.Enable=true;", "tc.Version=v2;"]
    for p in range(presets):
        out += [f"tc.v2.user.presets[{p}].Gamma.Value={gamma:.4f};",
                f"tc.v2.user.presets[{p}].UserCurve.Enable=FALSE;",
                f"tc.v2.user.presets[{p}].CurveControl.Enable=FALSE;",
                f"tc.v2.user.presets[{p}].Brightness.Enable=FALSE;"]
    z = ", ".join(["0"] * presets)
    out += [f"tc.v2.user.UseIndices={{ {z} }};", f"tc.v2.user.FlashUseIndices= {{ {z} }};"]
    return out


def lsc_lines(ctrls, width, height, ccts=((2856, 1), (4000, 2), (6500, 1)),
              first=0.25, center=0.5):
    """ctrls: list (one per ctrlPoint) of dict {R, GR, GB, B: 10x10}."""
    out = ["lensShading.correction_type.enableLSC\t = TRUE; ",
           "lensShading.correction_type.enableWPC\t = FALSE; ",
           "lensShading.module_cal_enable\t = 0; ",
           f"lensShading.ctrlPointsCount\t = {len(ccts)}; ",
           f"lensShading.imageWidth\t = {width}; ",
           f"lensShading.imageHeight\t = {height}; ",
           f"lensShading.leftPatchFactor\t = {first:.5f}; ",
           f"lensShading.centerPatchFactor\t = {center:.5f}; ",
           f"lensShading.topPatchFactor\t = {first:.5f}; ",
           f"lensShading.middlePatchFactor\t = {center:.5f}; "]
    for n, (cct, fam) in enumerate(ccts):
        c = ctrls[n] if len(ctrls) > 1 else ctrls[0]
        out += [f"lensShading.ctrlPoints[{n}].cct\t = {cct}; ",
                f"lensShading.ctrlPoints[{n}].light_family\t = {fam}; "]
        for ch in ("R", "GR", "GB", "B"):
            for i in range(10):
                for j in range(10):
                    out.append(f"lensShading.ctrlPoints[{n}].controlPoint{ch}[{i}][{j}]\t = {c[ch][i, j]:.12f}; ")
    return out


def black_lines(ival, fval):
    out = [f"opticalBlack.manualBias{c}\t = {ival};" for c in ("R", "GR", "GB", "B")]
    out += [f"opticalBlack.float.manualBias{c}\t = {fval:.8f};" for c in ("R", "GR", "GB", "B")]
    return out
