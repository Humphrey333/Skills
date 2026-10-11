---
name: embed_document
description: Use when the developer invokes /embed_document to create or update a project's README.md and BUILD.md so they match the project's Plans, code and build files (what was added or fixed, how to get dependencies, how to build and run). Manual only. Not for capturing session knowledge (use embed_summary), generating a new project skeleton (use embed_create_coding_template), locating a bug (use embed_debug), or carrying a session over to a new one (use handoff).
---

# Embedded Project Documentation

## Overview

Keep a project's `README.md` and `BUILD.md` true. The documents are written from evidence — the project's `Plans/`, its code and build files, and `git log` — not from memory of the conversation and not from guesses. Core principle: **every statement in the docs traces to a source; what no source confirms becomes a question or a `TODO:` marker, never prose.** Nothing is written to disk until the developer has seen the diff and said yes.

Style: CLI-focused with a table of contents (from the awesome-readme list) — install and usage first, `Getting Started` is the bulk of the README. Section-by-section rules are in `references/readme-structure.md`.

## When to Use

- The developer invokes `/embed_document` — to create `README.md` / `BUILD.md` in a project that lacks them, or to bring existing ones up to date after features or fixes landed.
- Manual only: never trigger this skill on your own, and never suggest running it in the middle of other work except as a one-line pointer at the end.
- Not for: capturing decisions and trade-offs from a session (use `embed_summary`), creating the project skeleton and first-draft docs (use `embed_create_coding_template`), finding a bug (use `embed_debug`), or session continuity (use `handoff` / `half-clone`). Other documents (CHANGELOG, ARCHITECTURE.md, `docs/design.md`) are out of scope.

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.claude/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.claude/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Step 1 — Gate: Root and Mode

Ask for anything not already stated, one specific question each:

- **Project root** — the directory whose `README.md` / `BUILD.md` are to be written. Offer the current directory as a suggested answer; don't treat it as confirmed.
- **Mode** — README, BUILD, or both.
- **Install target** (BUILD mode) — which distro / package manager the install commands should target, or "Yocto only". Offer what the project suggests (e.g. an `apt` list in a CI file) as a suggested answer.

**Hard rule — ask, never assume.** A stated assumption ("I'll assume Ubuntu") does not satisfy this; an inference from the codebase is a *suggested answer* inside the question. **Never fetch or download documentation yourself** (datasheet, TRM, app note, vendor guide): name the exact document and wait for the developer to supply it.

| Rationalization | Reality |
|---|---|
| "The license is obviously MIT, the template says so" | A template's text is not this project's license. `TODO:` or ask. |
| "The package name is the same on Ubuntu, so I'll write `apt install`" | The target distro is the developer's call. Ask. |
| "The plan says it works, so I'll document it as working" | Plans state intent. Status comes from code and `git log`, or is a `TODO:`. |
| "A short README without Getting Started is fine" | Getting Started is the bulk of this style. Fill it from evidence or mark `TODO:`. |
| "Writing it directly saves a round trip" | The developer approves diffs; a wrong overwrite costs more than one question. |

## Step 2 — Gather Evidence

Read, in this order, and record each fact together with where it came from:

1. `Plans/*.md` in the project — goal, chosen direction, what was built, verification criteria, open questions.
2. Build and code — `CMakeLists.txt` (`find_package`, `pkg_check_modules`, options, install rules), `subprojects/` / `external/`, scripts under `tools/`, Yocto `DEPENDS`/recipes if present, the entry points that define Usage.
3. `git log` — fixes and features, to confirm "what we have added / fixed". Commit messages are hints; the code decides.
4. The existing `README.md` / `BUILD.md`, if any — to preserve hand-written content that is still true.
5. Knowledge files loaded in Step 0 — as hints only.

Facts that no source confirms: ask the developer, or leave a `TODO:` marker. Unknowables such as license, authors, CI badge URL and project home URL default to `TODO:` markers.

## Step 3 — README Mode

Create `README.md` if absent; otherwise compare it with the evidence and change only what is stale, missing or wrong — keep hand-written wording that is still true.

Fixed section order: table of contents, About the Project, Project Status, Getting Started (Dependencies, Getting the Source, Building, Running Tests, Installation, Usage), Release Process (with Versioning), How to Get Help, Further Reading, Authors, License. Rules per section, and the CLI-focused style notes, are in `references/readme-structure.md` — read it before writing.

- Put working, copy-pasteable commands in Getting Started; every command comes from the project's own scripts or build files.
- `Project Status` states what builds, what is not implemented and what is in progress, each traced to code, a plan step or `git log`.
- Dependencies are summarised in the README and point to `BUILD.md` for the full list.

## Step 4 — BUILD Mode

Find the dependencies the project actually uses (see Step 2, item 2) and write `BUILD.md` with:

- a dependency table — name, what needs it, how it is found (e.g. `find_package(GTest QUIET)`), whether it is required or optional, and the install command for the target confirmed in Step 1;
- how to use each dependency in this project: the CMake option or variable that selects it, the `subprojects/` entry if it is vendored, behaviour when it is absent;
- host build, test and install steps from the project's own CMake/scripts;
- cross-build / Yocto steps **only** when the plan or build files show they exist — otherwise omit the section.

Do not run installs or builds on the developer's machine as part of this skill unless asked. A command you could not verify from a source is marked `TODO: verify`.

## Step 5 — Propose, Then Wait

Show a diff (or the full new file) per document, with each non-obvious statement's source in one short line beneath it. Ask exactly once per file set: *"Write these changes?"* Corrections → revise and show again. Only an explicit yes counts; write nothing before it, and write only the approved changes.

## Step 6 — Report

After writing: the files changed, remaining `TODO:` markers, and any statement you could not source. Write nothing outside `README.md` / `BUILD.md` — no plan edits, no knowledge files (suggest `/embed_summary` if durable decisions came up).

## Common Mistakes

- Self-triggering, or starting without the developer invoking `/embed_document`.
- Skipping Step 0 and re-asking what `~/.claude/Knowledge/` already records.
- Writing documentation from memory of the conversation instead of from Plans, code, build files and `git log`.
- Stating a fact (license, authors, status, a command, a dependency version) that no source confirmed instead of asking or leaving a `TODO:`.
- Assuming the project root, mode or target distro instead of asking; stating the assumption as a caveat instead of getting an answer.
- Fetching or downloading a datasheet, TRM or other platform document instead of naming it and waiting.
- Documenting something as working because a plan says it is planned.
- Overwriting hand-written README content that is still true, or rewriting sections that are already correct.
- Writing any file before showing the diff and getting an explicit yes.
- Extending scope to CHANGELOG, ARCHITECTURE.md or `docs/design.md`.
- Adding a cross-build or Yocto section the plan and build files don't support.
- Copying template placeholder text ("Phillip Johnston", example URLs, "Embedded Artistry LLC") into a real project's README.
