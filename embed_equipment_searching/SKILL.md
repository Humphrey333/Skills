---
name: embed_equipment_searching
description: "Use when an embedded topic is choosing hardware (sensor, camera module, lens, IMU, SoM, radio, converter or any other part) against a requirement, when a hardware-selection project has Requirements/, Vendors/, Research/, Export/ or Feedback/ folders, or when the developer brings a new Requirements/Improvement_N.md or a Feedback/ review report for such a project. Called from embed_planning-embedded-topics. Not for: bring-up or drivers (use embed_planning-embedded-topics), bugs (use embed_debug)."
---

# Equipment Searching

## Overview

Find and compare hardware for a stated requirement, and keep the results in a fixed folder layout and a fixed file format so every hardware project looks the same. This skill sets where files go, how candidates are compared, and how links are checked. The rules from AGENTS.md still apply: ask, never assume; never download platform documents; show every change as a diff and wait for a yes; prose goes through `embed_writing`.

## Project layout

| Folder | Holds | Written by |
|---|---|---|
| `Requirements/` | `Requirements.md` (brief), `Improvement_N.md` (each one is a change request) | Developer only |
| `Vendors/` | PDFs the developer supplies (current part, datasheets) | Developer only |
| `Plans/` | `Plan_<slug>_<YYYY-MM-DD>.md` | Agent, after a yes (`embed_planning-embedded-topics`) |
| `Research/` | `ResearchPlan_*`, `Findings_*`, `Documents_to_collect_*`, side analyses | Agent |
| `Research/scripts/` | Calculation scripts (`<name>.py`) that the docs cite | Agent |
| `Export/` | Exactly two files: `<Topic>_selection_<date>.md` and `<Topic>_vendors_<date>.md` | Agent, after a yes |
| `Feedback/` | Review reports from other people or tools | Reviewer |

The formats of the two Export files and of `Documents_to_collect` are in `references/file-formats.md`. Read it before writing any of them. A folder that does not exist yet is created when its first file is approved. A file that a later decision makes outdated keeps its content and gets a first line: `> Superseded <date>: <reason>. See <file>.`

## Search method

1. **Step 0.** Read `~/.agents/Knowledge/INDEX.md`. A knowledge file from another hardware topic does not carry over. Ask before reusing any of its facts (host, carrier, interface).
2. **Read the inputs.** Read `Requirements/` (the brief, then every `Improvement_N.md` in order; a later one overrides an earlier one) and the PDFs in `Vendors/`. List each open fact as a question.
3. **Derive the deciding numbers.** Turn the requirement into numbers with a formula. Mark each input as supplied or judgement. Compute with a script, never by hand: save it as `Research/scripts/<name>.py`, run it with `python3 -I`, and cite that path in the docs. Camera example: GSD = pixel pitch x distance / focal length, pixels per defect, depth of field, maximum exposure.
4. **Search.** Use vendor product pages, distributor pages and papers. Never download a datasheet, TRM or app note. Add each needed document to `Research/Documents_to_collect_<date>.md` with its exact name or search words.
5. **Classify.** Each candidate is a Module (ready to connect to the host, driver available) or a Raw part (needs our own PCB, converter or driver). Modules are listed first. Raw parts stay listed.
6. **Score.** Define factors F1 to Fn from the requirement. Mark each candidate ✓, ✗ or ?. A spec without a supplied datasheet is unverified.
7. **Pair.** When parts must fit together (lens and sensor, module and carrier, converter and host), build a pairing table by script. Show the fit check (for example image circle ≥ sensor diagonal).

## Links

- A model name links to that model's own page. A series page, a family flyer or a news page goes in Sources, not on the model name. A model with no own page stays unlinked; say so in the report.
- Check every new or changed link: `curl -sL -A "<browser UA>" -w '%{http_code} %{url_effective}'` and read the page title. For a PDF, use a HEAD request only (`curl -sIL`); never download it.
- 200 with the right model in the title: keep. Write the final URL after redirects.
- 200 with a generic title (series, lineup, home page): not the model page. It may go in Sources.
- 404, or 200 with "Not Found" in the title: dead. Search for the real page.
- 403, timeout, bot wall ("Just a moment"), or 200 with an empty title (a page built by JavaScript): unverified. Write it as plain text, list it, and ask the developer to open it in a browser.
- A URL typed from memory or built from a vendor's URL pattern is a guess. It goes in only after the check above passes.
- A number taken from a search summary, not from the page itself, is marked "via search summary".

## Change loop (each Improvement_N or Feedback report)

1. Read it fully. Split it into numbered items.
2. Ask about anything unclear (which viewer, which table, which file).
3. An item that needs new research goes through a plan. A mechanical item (links, a column, a correction) goes straight to a diff.
4. Show the diff line by line. Wait for a yes. Apply only what was approved.
5. Verify: compare against a copy taken before the edit (only the approved lines changed), re-run the scripts, check the links.
6. Report what changed, then what was not checked. Mention related places the change did not touch (other files with the same old link, a Sources line).

An existing file that does not match `references/file-formats.md` is reported, not reformatted, unless the developer asks.

## Common mistakes

| Mistake | Instead |
|---|---|
| Linking a model name to a guessed URL that returns 404 | Check status and title before reporting |
| Treating 403 as "page exists" | 403 is unverified; ask the developer |
| Linking a series page because the model page was not found | Leave the name unlinked |
| Writing a third file in `Export/` | Extra material goes in `Research/` |
| Editing files in `Requirements/` or `Vendors/` | They belong to the developer |
| Computing GSD, weights or fits by hand | Script in `Research/scripts/`, then compare the table to the output |
| Fixing one file and leaving the same dead link in another | Grep the project for it and report each place |
| Using facts from another topic's knowledge file | Ask first |
| Reformatting an old file while doing an unrelated Improvement | Report the mismatch; change only what was asked |
