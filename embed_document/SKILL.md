---
name: embed_document
description: "Use when the developer invokes /embed_document to create or update a project's README.md and BUILD.md so they match the project's Plans, code and build files (what was added or fixed, how to get dependencies, how to build and run). Manual only. Not for capturing session knowledge (use embed_summary), generating a new project skeleton (use embed_create_coding_template), locating a bug (use embed_debug), or carrying a session over to a new one (use handoff)."
---

# Embedded Project Documentation

## Overview

Keep a project's `README.md` and `BUILD.md` true. The documents are written from evidence — the project's `Plans/`, its code and build files, and `git log` — not from memory of the conversation and not from guesses. Core principle: **every statement in the docs traces to a source; what no source confirms becomes a question or a `TODO:` marker, never prose.** A plan never confirms that a function works, so the skill only looks at functions that have been planned and asks the developer whether each one is working. Nothing is written to disk until the developer has seen the diff and said yes.

Style: CLI-focused with a table of contents (from the awesome-readme list) — install and usage first, `Getting Started` is the bulk of the README. Section-by-section rules are in `references/readme-structure.md`.

## When to Use

- The developer invokes `/embed_document` — to create `README.md` / `BUILD.md` in a project that lacks them, or to bring existing ones up to date after features or fixes landed.
- Manual only: never trigger this skill on your own, and never suggest running it in the middle of other work except as a one-line pointer at the end.
- Not for: capturing decisions and trade-offs from a session (use `embed_summary`), creating the project skeleton and first-draft docs (use `embed_create_coding_template`), finding a bug (use `embed_debug`), writing the code (use `embed_executing_plans`), or session continuity (use `handoff` / `half-clone`). Other documents (CHANGELOG, ARCHITECTURE.md, `docs/design.md`) are out of scope.

## Step 1 — Gate: Unknowns

Fixed by the invocation, not asked:

- **Project root** — the directory the developer invoked the skill from. Its `README.md` / `BUILD.md` are the targets.
- **Mode** — both `README.md` and `BUILD.md`, unless the developer names only one.

Ask for anything else you don't know, one specific question each:

- **Install target** (BUILD mode) — which distro / package manager the install commands should target, when the project doesn't settle it. Offer what the project suggests (e.g. an `apt` list in a CI file) as a suggested answer.
- Any other fact the evidence in Step 2 can't confirm.

**Hard rule — ask, never assume.** A stated assumption ("I'll assume Ubuntu") does not satisfy this; an inference from the codebase is a *suggested answer* inside the question. Platform documents (datasheet, TRM, app note) are rarely needed for a README or BUILD.md — don't ask for them by default; if one is truly needed, read it online first (cite the URL); only if it can't be read online, list it in `Docs/REQUIRED_DOCS.md` for the developer to download by hand. **Never download documentation yourself.**

| Rationalization | Reality |
|---|---|
| "The license is obviously MIT, the template says so" | A template's text is not this project's license. `TODO:` or ask. |
| "The package name is the same on Ubuntu, so I'll write `apt install`" | The target distro is the developer's call. Ask. |
| "The plan says it works, so I'll document it as working" | A plan never confirms that anything works. Ask the developer, feature by feature. |
| "The code and `git log` show it, so I'll mark it working" | They are a suggested answer inside the question, not the developer's confirmation. Ask. |
| "This function isn't in a plan but I can see it in the code" | Only planned functions are checked and documented. Leave it out. |
| "A short README without Getting Started is fine" | Getting Started is the bulk of this style. Fill it from evidence or mark `TODO:`. |
| "Writing it directly saves a round trip" | The developer approves diffs; a wrong overwrite costs more than one question. |

## Step 2 — Gather Evidence

Read, in this order, and record each fact together with where it came from:

1. `Plans/*.md` in the project — goal, chosen direction, the planned functions/features, verification criteria, open questions. This is the **only** source of the feature list.
2. Build and code — `CMakeLists.txt` (`find_package`, `pkg_check_modules`, options, install rules), `subprojects/` / `external/`, scripts under `tools/`, the entry points that define Usage.
3. `git log` — hints for the suggested answer when asking about a planned feature's status; never a source of features on its own.
4. The existing `README.md` / `BUILD.md`, if any — to preserve hand-written content that is still true.

**Feature status.** List every function/feature the plans mention. A plan never confirms that a function works, so ask the developer for the status of each — working, partly working, not working, or not started — batched into as few questions as possible, one option per feature. Put what code or `git log` suggests inside the question as a suggested answer. Only planned functions are checked: do not inventory the code for functions no plan lists. Other facts no source confirms: ask the developer, or leave a `TODO:` marker. Unknowables such as license, authors, CI badge URL and project home URL default to `TODO:` markers.

## Step 3 — README Mode

Create `README.md` if absent; otherwise compare it with the evidence and change only what is stale, missing or wrong — keep hand-written wording that is still true.

Fixed section order: table of contents, About the Project, Project Status, Getting Started (Dependencies, Getting the Source, Building, Running Tests, Installation, Usage), Release Process (with Versioning), How to Get Help, Further Reading, Authors, License. `references/readme-structure.md` is the structural template — rules per section, the CLI-focused style notes and a heading skeleton. Read it before writing. The skeleton gives structure only; all content is written from the evidence.

- Pass the README's prose through `embed_writing` before Step 5. Commands, versions and feature statuses stay unchanged.
- Put working, copy-pasteable commands in Getting Started; every command comes from the project's own scripts or build files.
- `Project Status` states what builds, what is not implemented and what is in progress, each from the developer's per-feature status answers (Step 2) — a plan todo alone, or code alone, is not enough.
- Dependencies are summarised in the README and point to `BUILD.md` for the full list.

## Step 4 — BUILD Mode

Find the dependencies the project actually uses (see Step 2, item 2) and write `BUILD.md` with:

- a dependency table — name, what needs it, how it is found (e.g. `find_package(GTest QUIET)`), whether it is required or optional, and the install command for the target confirmed in Step 1;
- how to use each dependency in this project: the CMake option or variable that selects it, the `subprojects/` entry if it is vendored, behaviour when it is absent;
- host build, test and install steps from the project's own CMake/scripts.

Pass the prose of `BUILD.md` through `embed_writing` before Step 5. Commands and dependency names stay unchanged.

`BUILD.md` covers the host build only — no cross-build or Yocto section, even when the plan or build files mention one.

Do not run installs or builds on the developer's machine as part of this skill unless asked. A command you could not verify from a source is marked `TODO: verify`.

## Step 5 — Propose, Then Wait

Show the `embed_writing` result as a diff (or the full new file) per document, with each non-obvious statement's source in one short line beneath it. Ask exactly once per file set: *"Write these changes?"* Corrections → revise and show again. Only an explicit yes counts; write nothing before it, and write only the approved changes.

## Step 6 — Report

After writing: the files changed, remaining `TODO:` markers, and any statement you could not source. Write nothing outside `README.md` / `BUILD.md` (and `Docs/REQUIRED_DOCS.md`) — no plan edits, no knowledge files (suggest `/embed_summary` if durable decisions came up).

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question, or remove or change a fact, reason, hedge or warning.
- Self-triggering, or starting without the developer invoking `/embed_document`.
- Writing documentation from memory of the conversation instead of from Plans, code and build files, with feature status from the developer.
- Stating a fact (license, authors, status, a command, a dependency version) that no source confirmed instead of asking or leaving a `TODO:`.
- Asking for the project root or mode (they are the invocation directory and both files), or assuming the target distro or any other unknown instead of asking; stating the assumption as a caveat instead of getting an answer.
- Downloading a datasheet, TRM or other platform document, or asking for one when the README/BUILD.md doesn't need it — if one is truly needed, read it online or list it in `Docs/REQUIRED_DOCS.md`.
- Documenting a function as working because a plan lists it, or because code/`git log` suggests it, instead of asking the developer for each planned feature's status.
- Documenting or checking functions that no plan lists.
- Overwriting hand-written README content that is still true, or rewriting sections that are already correct.
- Writing any file before showing the diff and getting an explicit yes.
- Extending scope to CHANGELOG, ARCHITECTURE.md or `docs/design.md`.
- Writing a cross-build or Yocto section in `BUILD.md` — it is host build only.
- Copying example text ("Phillip Johnston", example URLs, "Embedded Artistry LLC") from any template into a real project's README — `references/readme-structure.md` gives structure only.
