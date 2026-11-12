# Qualcomm Chromatix (Spectra 680/780) -> Argus

Project layout: `<proj>/Scenario.Default/XML/{IFE,BPS,IPE,SFE,AON,EVA,SW_CONTROL,STATS,MISC}/*.xml`,
one file per block. Each file has a trigger tree (lens position, drc_gain, aec_exp_sensitivity_ratio,
led_idx, lux_idx, cct or gain) ending in `<region>` elements. `qcom._regions()` walks it.

**Tuned or template?** A block is tuned if it has more than one `<region>` or a later edit date than
the template batch (in the IMX586 project: after 10-06 11:46; STATS files dated 09-15 were defaults).
Ask the developer before porting a block that looks like a template default.

| Chromatix block | Argus keys | Ported by script | How |
|---|---|---|---|
| `IFE/lsc42_ife_v2.xml` (17x13 mesh per r/gr/gb/b, rows = 13) | `lensShading.*` | yes | divide by centre Gr, least-squares 10x10 Bezier fit; one table -> same net on all 3 ctrlPoints |
| `IPE/cc14_ipe_v2.xml` (`c_tab` 9 values, rows = output R,G,B, rows sum 1; one region per CCT) | `colorCorrection.srgbMatrix` | yes | transpose, then blend (see argus_keys.md) |
| `IFE/cc13` | - | no | identity in the IMX586 tune |
| `IPE/gamma15_ipe_v2.xml` (257 pts, 0..1023, region per lux idx) | `tc.v2 Gamma.Value` | yes | power fit. Log-space fit x>=0.01 gave 2.05; linear fit 2.29 on the same curve: report both |
| `IFE/bls12_ife_v2.xml` `offset` (18-bit on Spectra 780) | `opticalBlack.*` | yes | 16384/2^18 = 0.0625 -> 64 @10-bit |
| `STATS/*AWB*`, `refPt*`, `MWBGain*` | `awb.v4` | no | no known mapping from R/G,B/G ref points to the Argus grey-line U space |
| `IPE/anr14`, `hnr11`, `tf22`, `IFE/bpcabf41` | `noiseReduction.*` | no | gain-indexed regions; units differ |
| `IPE/asf35` | `sharpness.*` | no | |
| `IPE/ltm20`, `gtm13` | - | no | Argus has no matching block in the Char-lite set |
| `STATS/aecx*` | `ae.*` | no | |

Also unverified: whether `c_tab` is R,G,B or G,B,R order (a red/blue swap on a ColorChecker shows it),
and whether the 4000x3000 LSC net is valid for the 8000x6000 mode.

## Spectra 480 layout (SM8250 / SDM865), reader `qcom480.py`

Detected when `IFE/lsc34_ife.xml` and `IPE/cc13_ipe.xml` exist. Regions are `<blockNN_rgn_data>`;
triggers are named (`cct_trigger`, `aec_trigger` lux_idx/gain, `led_idx_trigger`).

| Block | Argus | Notes (IMX412 / sm8250_gremsy_imx577) |
|---|---|---|
| `IFE/lsc34_ife.xml` per CCT x gain | `lensShading` 3 ctrlPoints | `--lsc-gain 1-4` picks the gain band; Argus 2856/4000/6500 take the 2700-3100 / 3800-4200 / 5800-9000 bands. Corner gain ~5x at gain 1-4 (Argus clamp unknown). |
| `IPE/cc13_ipe.xml` per CCT x lux | `srgbMatrix` | First region of a CCT = bright lux (270-300), no LED. |
| `IPE/gamma15_ipe.xml` `<table>` 257 pts, 10-bit | `Gamma.Value` | Log fit 1.82, linear 2.14. |
| `IFE/linearization34_ife.xml` first `r_lut_p` knee, 14-bit | `opticalBlack` | `bls12` disabled (offset 0). 1024/16384 -> 64 @10-bit. |
| file dates | - | All identical (extracted zip): the date rule for tuned blocks does not apply. Use region counts. |
