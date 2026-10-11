# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

This repo is a library of Claude Code **skills** (prompt/workflow documents), not software. There is nothing to build, lint, or test — no package manifest, no test suite, no CI. The artifacts are Markdown files; "correctness" means a skill triggers on the right requests, routes to the right sibling skill, and keeps its hard rules intact.

Tracked skills live in `<skill-name>/SKILL.md`, optionally with `references/*.md` for detail that would bloat the main flow (see `embed_debug/references/techniques.md`).

`andrej-karpathy-skills/` is a separate upstream clone, listed in `.gitignore` — reference material only. Don't edit or commit it.

## Activating a skill

Skills are **copied**, not symlinked, into `~/.claude/skills/`. Editing a file here does not change the skill Claude Code is running:

```bash
cp -r <skill-name> ~/.claude/skills/            # install or update
diff -r <skill-name> ~/.claude/skills/<skill-name>   # verify installed copy matches the repo
```

Currently installed: `embed_debug`, `embed_planning-embedded-topics`, `embed_summary`, `embed_create_coding_template`, `embed_document`. `handoff` and `half-clone` exist in the repo but are not installed. The installed `embed_create_coding_template` and `embed_document` also carry developer-supplied `Requirements*` files (git-ignored via `Requi*` in `.gitignore`), so `diff -r` will show those as "Only in" the installed side — expected, not drift. After copying, the session must be restarted for Claude Code to pick up the change.

## Skill roster and division of labor

The `embed_*` skills are a workflow chain for embedded Linux engineering (NVIDIA Jetson/L4T, Yocto, camera sensor bring-up — see the sibling project dirs under `/home/vito/Learning/Claude/`):

- `embed_planning-embedded-topics` — new topic (bring-up, subsystem, board support, feature): Research (facts + trade-offs, **no code**) → Planning (developer picks direction, then step-by-step plan) → Output (reference code, README, build/run instructions). After a clean recap and explicit final approval, saves `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md` **in the target project repo**, not here.
- `embed_debug` — existing bug/crash/misconfiguration: info gate → code search → platform docs → narrowing techniques → targeted questions. Reasons from descriptions; does not run or reproduce on target hardware.
- `embed_summary` — manual `/embed_summary` only: harvests durable session knowledge into `~/.claude/Knowledge/<topic-slug>.md` + a one-line `INDEX.md` entry.
- `embed_create_coding_template` — runs after a plan is agreed in `embed_planning-embedded-topics`; copies `templates/project/` into `<plan repo root>/<project-name>/`, substitutes `@PLACEHOLDER@`s, specialises from the plan, then host-builds it. Design record: `Plans/2026-10-10-embed-create-coding-template.md` (lives in the project repo the skill was designed in, not in this repo). Unlike the other skills it ships real files (`templates/`: CMake, lint configs, CI, shell scripts) — editing a template means re-copying the whole skill dir. `grep -rn '@[A-Z_]*@'` on a generated project must stay empty, so a new placeholder must be added to `templates/README.md` too.
- `embed_document` — manual `/embed_document` only: creates or updates a project's `README.md` and `BUILD.md` from evidence (its `Plans/`, code/build files, `git log`), CLI-focused + TOC style (awesome-readme). Runs in the invocation directory; BUILD.md is host build only; only functions listed in Plans are documented, with each one's working status asked of the developer. Shows a diff and waits for yes before writing; unknowns are asked or become `TODO:` markers. Section rules live in `references/readme-structure.md`. Design record: `Plans/Plan_embed-document-readme-build_2026-10-11.md` (also not in this repo). Has its own `embed_document/CLAUDE.md` with skill-specific rules — read it before editing there. Complements `embed_create_coding_template` (first-draft docs) — this one keeps them true afterwards.
- `handoff` / `half-clone` — session continuity pair, both manual. `handoff` writes a curated `HANDOFF.md` (Goal / Done So Far / What Worked / What Didn't Work / Next Steps); `half-clone` writes `HALF-CLONE.md`, a trimmed transcript of the recent half of a conversation with bulky tool output collapsed. Each skill's `When to Use` explicitly points at the other for the wrong case.

Each skill's `description` and `When to Use` must carry that negative routing ("Not for: X — use Y instead"); it is what keeps the skills from stealing each other's triggers.

## The shared-knowledge layer

`~/.claude/Knowledge/` is the cross-project memory that ties the chain together: `embed_summary` writes it, every other `embed_*` skill reads it as **Step 0 — Load Shared Knowledge** before doing anything else. Slugs are global across projects, so they must be specific (`imx586-mipi-csi-bringup`, not `camera`).

The Step 0 block is reproduced verbatim in every `embed_*` skill. **When editing it, apply the identical change to all of them** — that includes any new skill added to the chain. Its semantics: read `INDEX.md`, open every matching topic file, tell the developer in one line what loaded (or that nothing matched), and when a knowledge entry conflicts with what the developer says now, the developer wins and the conflict gets flagged for `/embed_summary`.

## Conventions for writing or editing a skill

Structure every `SKILL.md` the way the existing ones are structured — deviation makes the set harder to maintain:

1. YAML frontmatter with `name` (matching the directory name exactly) and a `description` that starts "Use when …", names concrete triggers, and ends with the negative routing case.
2. `# Title` → `## Overview` (core principle in a few lines) → `## When to Use` (positive bullets + a `Not for:` bullet) → `## Step 0` / numbered Stages or Steps → `## Common Mistakes`.
3. `## Common Mistakes` is a mirror of the rules above it — every hard rule and skipped-step failure in the body gets a corresponding bullet. Keep them in sync when adding a rule.
4. Harden a rule that Claude will be tempted to rationalize past with a `| Rationalization | Reality |` table (see `embed_planning-embedded-topics` Stage 1).

Recurring hard rules — preserve these when editing, and carry them into new skills:

- **Never fetch or download platform documentation** (datasheet, TRM, errata, app note). Name the exact document, or give search segments if unsure, and wait for the developer to supply it. This is treated as a security boundary, not a convenience.
- **Ask, never assume.** A stated assumption ("I'll assume X unless told otherwise") does not satisfy this; an inference from the codebase is a *suggested answer* inside a question, never a confirmed one.
- **Propose, then wait.** Anything that writes to the developer's knowledge files or picks a direction requires explicit confirmation first.
- **Manual-only skills must not self-trigger** (`embed_summary`, `handoff`, `half-clone`).
- Prose is addressed to Claude-as-executor and refers to the user as "the developer."

## Scope notes

The git repo root is this `Skills/` directory. Two CLAUDE.md files above and beside it also load: `../CLAUDE.md` (parent library overview, outside any repo) and `../Digital_Zoom/CLAUDE.md` (a real embedded project, where the `embed_*` skills actually get used).
