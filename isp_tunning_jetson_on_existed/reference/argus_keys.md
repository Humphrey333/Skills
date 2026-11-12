# Argus camera_overrides.isp: keys this skill writes

NVIDIA does not publish these keys (partner-only). Names and value shapes come from the
NVIDIA Char-lite IMX477 file (`IMX477/camera_overrides.isp` in the Reverse_ISP_Tune repo) and these forum threads:
- https://forums.developer.nvidia.com/t/camera-isp-tuning-mechanism/62332
- https://forums.developer.nvidia.com/t/color-control-matrix-and-tone-curves-in-camera-override-isp/120405
- https://forums.developer.nvidia.com/t/jetpack-7-2-isp-overrides-no-longer-working/372703 (overrides stop working on JetPack 7.2)

Install path on the Jetson: `/data/nvcam/settings/camera_overrides.isp`, then restart `nvargus-daemon`.
A key the file leaves out falls back to the Argus default.

| Key group | Shape | Notes |
|---|---|---|
| `ap15Function.lensShading` | `TRUE`/`FALSE` | Must be TRUE for `lensShading.*` to apply. |
| `colorCorrection.srgbMatrix[0..2]` | `{a, b, c};` | **Transposed**: columns sum to 1 (Char-lite). Vendor row-form CCM -> transpose. Column sums = grey response. |
| `tc.Enable`, `tc.Version=v2`, `tc.v2.user.presets[0..8].Gamma.Value`, `.UserCurve.Enable`, `.CurveControl.Enable`, `.Brightness.Enable`, `tc.v2.user.UseIndices`, `FlashUseIndices` | float / bool / 9 ints | Semantics are undocumented. Whether a higher Gamma.Value means brighter is not confirmed. |
| `lensShading.correction_type.enableLSC/enableWPC`, `module_cal_enable`, `ctrlPointsCount`, `imageWidth/Height`, `left/center/top/middlePatchFactor` | | The patch factors set the Bezier patch widths (0.25/0.5/0.25). |
| `lensShading.ctrlPoints[n].cct`, `.light_family`, `.controlPoint{R,GR,GB,B}[i][j]` | 10x10 per channel | Gains, 1.0 = no gain. Taken as i = row (top to bottom), j = column: **unverified**. |
| `opticalBlack.manualBias{R,GR,GB,B}` | int @ sensor bits | 64 @ 10-bit for IMX586. |
| `opticalBlack.float.manualBias*` | int / (2^bits - 1) | 0.06256109 = 64/1023. |

Not handled by the scripts (use the Char-lite file as a shape reference): `awb.v4` (grey-line U space),
`noiseReduction.v6`, `sharpness`, `ae.*`, `falloff_srfc`, `mwbCCTTint`, `flicker`.

## Known board results (IMX586, Orin NX, JetPack 6.2)

| Variant | CCM | Result |
|---|---|---|
| 18 (`IMX586/`) | {1,0,-0.2},{0.14,1,0.22},{0.04,0,1}, LSC off | Correct colour |
| 20 | Qualcomm 5500-7000K transposed | Brighter, **green** |
| 21 | I + 0.3(Q - I) | Still green |
| 24 (`IMX586_Jetson/`) | (I + 0.15(Q - I)) @ variant-18 CCM | **Good** (confirmed 2026-11-11) |

## Known board results (IMX412, same family, Orin NX)

| Variant | CCM | Result |
|---|---|---|
| 02 (`IMX412_Jetson/`) | I + 0.3(Q - I), IMX412 cc13 5500-7000K | **Green** (2026-11-12) |
| 02b | none (Argus default) | **Green** (2026-11-12) |
| 03 | (I + 0.15(Q - I)) @ IMX586 variant-18 CCM, vendor colour LSC | Colour OK, but **bluish soft disc at centre** (2026-11-12) |
| 04a (`camera_overrides_lsc_luma.isp`) | as 03, LSC `--lsc-colour luma` (Gr shading on all channels) | **Good** (2026-11-12) |
| 04b (`camera_overrides_lsc_off.isp`) | as 03, LSC off | not reported |

Lesson: a vendor colour-shading table that relies on vendor runtime correction (Qualcomm lsc40 ALSC, tintless20) can leave a coloured centre disc under Argus. Port the luma shading only (`--lsc-colour luma`) unless the colour shading is measured on the Jetson.

The Argus default CCM is green on both IMX586 and IMX412, so a matrix with unit column sums is not a safe starting point.

Lesson: the Argus default AWB is not the Qualcomm AWB, so a vendor CCM tuned for the vendor AWB
amplifies the leftover cast. Keep the grey response of a CCM known good on Argus, and add vendor
saturation only through a factor whose columns sum to 1 (`--ccm-mode grey`).

## Symptom table

| Symptom on board | First move |
|---|---|
| Green or magenta cast after a CCM port | `set-ccm --ccm-mode grey` on a known-good CCM; lower `-k`. |
| Red and blue swapped | Vendor CCM channel order (R,G,B vs G,B,R) is wrong; ask, then reorder. |
| Top/bottom brightness step | LSC row order flipped (unverified convention). |
| Brightness only, colour fine | `set-gamma`, one variant per direction (e.g. 2.30 and 1.85). |
| Coloured (e.g. bluish) soft disc at the centre | Vendor colour-shading table does not match the Jetson raw (vendor ALSC/tintless not ported). A/B with `build-qcom --lsc-colour luma` and `--lsc-off`. |
| LSC wrong in another sensor mode | Net built for 4000x3000; ask whether the mode scales. |

## CLI --ccm-mode

| Mode | Matrix | Use |
|---|---|---|
| `grey` (default) | (I + k(V - I)) @ base | Keeps base white balance, adds vendor saturation. |
| `identity` | I + k(V - I) | Loses base grey response; green on IMX586. |
| `transpose` | V | Raw vendor CCM; green on IMX586. |
| `copy` | base | Exact copy of a known-good CCM. |
| `--matrix a b c d e f g h i` | given | Explicit values, row by row. |
