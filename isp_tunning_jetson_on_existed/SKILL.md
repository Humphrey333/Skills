---
name: isp_tunning_jetson_on_existed
description: Use when a Jetson (Argus, JetPack) camera needs a camera_overrides.isp built or changed - porting a tune from another platform (Qualcomm Chromatix XML, a vendor tuning blob, another sensor's .isp), starting from a Jetson tune already good on the board, or fixing a green or magenta cast, brightness or vignetting after a port.
---

# Jetson ISP tuning (Argus camera_overrides.isp)

## Overview
A vendor tune was made for the vendor's AWB and pipeline. Argus runs its own default AWB, so a vendor colour matrix that is right on its own platform leaves a colour cast on the Jetson. **Keep what is proven on the board, and add vendor data only in a way that cannot move it.** One block changes per variant. The board decides.

## Why ported colour turns green
- `colorCorrection.srgbMatrix` is stored transposed. **Its column sums are the grey response.**
- A known-good matrix with column sums of, for example, 1.18 / 1.00 / 1.02 is not "un-normalised". Those sums are what compensate the Argus AWB on that sensor.
- A vendor matrix whose columns sum to 1 throws that compensation away, and the image goes green. "Normalising" it, or blending it toward identity, still keeps column sums of 1, so it stays green.
- The fix:
  - Formula: `M = (I + k(V - I)) @ G`, with `G` the known-good matrix and `V` the vendor matrix transposed.
  - `I + k(V - I)` has unit column sums, so `M` keeps the grey response of `G` and adds only vendor saturation.
  - In the CLI this is `set-ccm --ccm-mode grey`. k = 0.15 was confirmed on IMX586.

## Ask before you choose
The developer's yes is needed for:
- which CCM option (`copy`, `grey` with k, `identity`, `transpose`);
- which blocks to port;
- whether a block that looks like a template default should be ported.

Ask even when they say "just give me the file". Pass your recommendation as the first option of the question. A file built on a silent choice is a guess the developer must test on the board.

## Steps
1. Read `~/.agents/Knowledge/INDEX.md` and the matching topic file. For IMX586 it is `imx586-sm8550-chromatix-to-jetson-argus-isp-port.md`.
2. Reverse the existing tune with REA. Do all of these, in order, for every tune from another platform. Plain XML is no exception.
   1. **REQUIRED SUB-SKILL:** invoke `rea:reverse-engineer-anything` with the Skill tool, naming the targets: the tune archive (`.zip`), the project folder, and any `.so`/`.bin`.
   2. Run `bash scripts/rea_check.sh`. Then run ToolSearch `open_binary inspect_artifact` to see whether REA tools are loaded in this session.
   3. **If the tools are loaded:**
      - Run `open_binary` on the archive, then `inspect_artifact` with `detail: "summary"` to get the member inventory and SHA-256 hashes.
      - Use native analysis for any binary tuning file.
      - Put the Evidence IDs in the report and the `.isp` header.
   4. **If they are not loaded:**
      - Tell the developer every FAIL and INFO line from `rea_check.sh`, with its fix. Do not run the fixes: they download packages or change configuration.
      - Write "REA not run: <blockers>" in the report and the `.isp` header, then continue.
   5. Parse the tables with `scripts/argus_isp/`. REA has no Chromatix table parser. `qcom.py` reads Spectra 680/780 and `qcom480.py` reads Spectra 480 (SM8250); a new format gets a new reader module next to them.
3. Inspect with `python3 scripts/argus_isp.py inspect-qcom <XML_DIR>`, then ask (see above).
4. Build or edit with `python3 scripts/argus_isp.py {build-qcom|set-ccm|set-gamma} ...` (run with `-h` for options). Always write a new file, and keep the last good variant. Use `--note` so the header lists the variant name, what was ported, what was not, and what is unverified.
5. Check with `python3 scripts/argus_isp.py check <new.isp> --ref <previous.isp> --expect <key prefix>`. Give one `--expect` per block you meant to change, for example `--expect colorCorrection.srgbMatrix` or `--expect tc.`. It prints `CHECK PASS` only if the ctrlPoints are complete, an expected key changed, and no other key changed. After editing the scripts, also run `bash scripts/selftest.sh <Reverse_ISP_Tune repo> <scratch dir>`.
6. Hand over for the board test: install path, restart, and what to compare. Never claim a colour result before the developer reports from the board. Pass the report through `embed_writing`.

Brightness only: change `Gamma.Value` with `set-gamma`, one variant per direction, because the direction is unconfirmed.

## Reference
- `reference/argus_keys.md`: key shapes, install path, IMX586 board results per variant, symptom table, `--ccm-mode` table.
- `reference/qcom_chromatix.md`: Chromatix block to Argus mapping, how to tell tuned from template, what cannot be ported and why.
- `reference/rea.md`: why REA tools can be missing although the plugin is installed, and how the developer fixes it.

## Common mistakes
- Skipping REA because the tune files are plain XML, or saying "REA is not connected" without the `rea_check.sh` lines that show why.
- Treating the known-good matrix's column sums as an error to normalise away.
- Blaming lens shading or gamma for a green cast before checking the CCM grey response.
- Copying a vendor value by key name. Units, bit depth and pipeline stage differ.
- Porting AWB, NR, sharpening or AE without a known mapping. Leave them at the Argus defaults and say so in the header.
- Reporting a gamma "fit" without saying the method. On IMX586 a log fit gives 2.05 and a linear fit 2.29.
