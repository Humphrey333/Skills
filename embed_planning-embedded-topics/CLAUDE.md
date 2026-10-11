# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this directory is

A single Claude Code skill — `SKILL.md` is the whole artifact (no `references/`, no templates, nothing to build or test). It is the entry point of the `embed_*` workflow chain: planning for a *new* embedded topic (bring-up, subsystem, board support, feature) before any implementation. Repo-wide conventions, skill roster, and the shared-knowledge layer are documented in `../CLAUDE.md`; this file only covers what is specific to this skill.

## Editing `SKILL.md`

- **Install after editing:** the running skill is the copy in `~/.claude/skills/`, not this file. `cp -r ../embed_planning-embedded-topics ~/.claude/skills/`, then restart the session. Check with `diff -r . ~/.claude/skills/embed_planning-embedded-topics`.
- **Step 0 is shared.** The "Load Shared Knowledge" block is verbatim in every `embed_*` skill. Change it here only together with `embed_debug`, `embed_summary`, `embed_create_coding_template` (and any new chain skill).
- **Stage boundaries are the product.** Research → Planning → Output is strictly ordered, and code is forbidden before Stage 3. Don't add wording that lets pseudocode leak into Stage 1/2.
- **Stage 1 has two coupled mechanisms:** the "ask, never assume" hard rule and its Rationalization/Reality table + red-flags list. A change to one usually needs a matching change to the other and to the last two bullets of `Common Mistakes`.
- **`Common Mistakes` mirrors the body.** Every hard rule or skippable step above it has a bullet below; keep them in sync.
- **Negative routing lives in two places:** the frontmatter `description` and `When to Use`. Both point existing bugs to `embed_debug`.

## Output location quirk

The topic doc (`Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md`, written only after the Stage 2 Step 3 approval gate) is written into the **developer's target project repo**, not into this skills repo. Stage 3 artifacts (code, README, build/run instructions) are project deliverables and are deliberately *not* part of that doc. After a plan is agreed, hand-off to project scaffolding goes to `embed_create_coding_template`.
