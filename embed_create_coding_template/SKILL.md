---
name: embed_create_coding_template
description: Use when a plan for a new embedded C/C++ userspace project has been agreed with embed_planning-embedded-topics and the developer wants the CMake project skeleton created on disk (src, include, test, tools, docs, lint configs, build/BUILD docs) before coding starts, or wants an existing project's .clang-format/.clang-tidy refined. Not for planning (see embed_planning-embedded-topics), existing bugs (see embed_debug), or kernel modules, Yocto recipes and vendor-source patch projects.
---

# Create Coding Template

## Overview

After a plan is agreed, create the project skeleton so the next coding skill (or the developer) starts from a tree that already configures, builds and passes one test. The skeleton is **real files** in `templates/project/` next to this document, copied into a new project folder and specialised by placeholder substitution plus the agreed plan. The project is built standalone first and later goes into a Yocto build, so nothing in it may need the network at configure time.

Core rule: **the template is the definition; the plan only fills it in.** Do not redesign the layout per project.

## When to Use

- A `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md` exists with a chosen direction and a step-by-step plan, and the developer asks for the project/skeleton/template to be created.
- The developer asks to improve the `.clang-format` / `.clang-tidy` of an existing project (see "Refining lint configs").
- Not for: a topic that has no agreed plan yet (use `embed_planning-embedded-topics`), writing the plan's feature code (use `embed_executing_plans`; this skill only creates the skeleton), an existing bug (use `embed_debug`), or out-of-tree kernel modules, Yocto recipes, or patch-on-vendor-source projects — those are outside this template.

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.claude/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.claude/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Step 1 — Require the Agreed Plan

Locate `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md` for this topic. If there is none, or it has no chosen direction and plan steps, **stop** and tell the developer to finish `/embed_planning-embedded-topics` first. Do not scaffold from a verbal description.

From the plan, extract (these become *suggested answers* in Step 2, not confirmed ones):

- project name — from the topic slug
- the modules the plan names → `src/<module>.cpp` + `include/<slug>/<module>.hpp`
- the verification criteria → one `test/` case each
- the dependencies → rows in `BUILD.md`
- the goal paragraph → `README.md` and `docs/design.md`

## Step 2 — Interview Gate (ask, never assume)

Ask for every item below that the plan or knowledge files do not state explicitly. Offer your plan-derived inference as the suggested answer inside the question; a stated assumption is still unconfirmed.

| Item | Notes |
|---|---|
| Project name | gives `@PROJECT_NAME@`; derive `@PROJECT_SLUG@` (lower_snake) and `@PROJECT_UPPER@` |
| Artefact kind | `executable`, `static` library or `shared` library |
| Target architecture | host-only, or cross: architecture, compiler prefix, absolute sysroot path |
| C++ standard | default suggestion 17 |
| License + copyright holder | MIT, Apache-2.0 or proprietary |
| CI system | GitHub Actions, GitLab CI, or none (then `tools/ci-local.sh` is the stand-in) |
| Dependencies | any the plan does not name |

State the context to the developer: the project is built **standalone first, then included in Yocto**. Do not accept a sysroot or compiler path you cannot see on disk without the developer confirming it. Never download a dependency or document yourself.

| Rationalization | Reality |
|---|---|
| "Host-only is obviously fine for now" | Architecture is the developer's call; ask. |
| "The plan's slug is a fine project name" | Offer it as the suggestion, wait for confirmation. |
| "MIT is the safe default license" | License is a legal decision; ask. |

## Step 3 — Propose, Then Wait

Print: the target path `<root of the repo holding Plans/>/<project-name>/`, the full proposed tree, and the placeholder → value table. **Write nothing until the developer confirms or edits it.**

If the target folder already exists, stop and ask for a different name — this skill never merges into or overwrites an existing tree.

## Step 4 — Create

The template lives in this skill's installed directory: `~/.claude/skills/embed_create_coding_template/templates/`. Copy from there, not from a repo checkout, and **state the exact path you copied from** in the final report so a stale install is visible.

1. `cp -r templates/project <target>`
2. Resolve variants:
   - library artefact → delete `src/main.cpp`
   - host-only → delete `cmake/` and the "Cross build" section of `BUILD.md`
   - cross → rename `cmake/cross-toolchain.cmake.in` to `cmake/<arch>-cross.cmake`
3. Rename paths containing placeholders, deepest first (`src/@PROJECT_SLUG@.cpp`, `include/@PROJECT_SLUG@/`).
4. Substitute placeholders in every file with `sed`. Use a delimiter that cannot appear in the values (e.g. `|` for paths) and escape `&` and `\` in values.
5. Copy `templates/licenses/<choice>.txt` to `<target>/LICENSE` (substituting `@YEAR@`, `@COPYRIGHT_HOLDER@`). **Apache-2.0**: the template holds only the standard notice — tell the developer to place the full license text themselves; never fetch it.
6. CI: copy `templates/ci/github-actions.yml` → `.github/workflows/ci.yml`, or `templates/ci/gitlab-ci.yml` → `.gitlab-ci.yml`, or neither.
7. `chmod +x tools/*.sh`.

## Step 5 — Specialise From the Plan

Add only what the plan states: module stubs, one test per verification criterion, dependency rows with install commands in `BUILD.md`, the goal paragraph in `README.md` and `docs/design.md`. Replace the `TODO:` markers the plan answers; leave the others and list them in the report. Comments explain the non-obvious reason, never restate the code. Do not invent behavior the plan does not specify — if a stub needs a decision the plan lacks, ask.

Pass the prose of `README.md`, `BUILD.md` and `docs/design.md` through `embed_writing` before Step 6. Commands and placeholder values stay unchanged.

## Step 6 — Verify, Then Report

Run, in the new project, and report the **actual output**:

1. `grep -rn '@[A-Z_]*@' .` — must be empty (also check file and directory names with `find . -name '*@*'`).
2. `cmake -S . -B build && cmake --build build -j`
3. `ctest --test-dir build --output-on-failure` when GTest is present. When it is absent, confirm the configure output shows `GTest not found or BUILD_TESTING=OFF - tests disabled` and the build still succeeded — that is the Yocto-relevant path.

Cross builds are **not** run here (the sysroot may not be populated); say so. Then report: the tree, the template path used, build/test output, remaining `TODO:` markers, and the next commands from `BUILD.md`. Write nothing outside the new project folder — no plan-doc edits, no knowledge files (suggest `/embed_summary` if durable decisions came up).

## Refining Lint Configs

When invoked on an existing project, read its `.clang-format` / `.clang-tidy`, diff them against the template versions, and propose specific changes with a reason each. Wait for approval, then write only the approved changes. Never replace the developer's config wholesale with the template.

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question.
- Scaffolding without an agreed plan, or from a verbal description.
- Assuming architecture, artefact kind, C++ standard, or license instead of asking.
- Writing files before the developer confirms the proposed tree.
- Scaffolding into an existing folder instead of stopping and asking for a new name.
- Copying from the repo checkout (or not saying which path) so a stale installed skill produces an old scaffold unnoticed.
- Leaving `@PLACEHOLDER@` text in file contents or file names.
- Claiming the skeleton builds without running configure + build, or hiding that the GTest-present path was not exercised.
- Adding `FetchContent`, `ExternalProject`, or any configure-time download — it breaks the Yocto build.
- Fetching a license text, dependency, or platform document yourself.
- Replacing an existing `.clang-format` / `.clang-tidy` without proposing a diff.
- Inventing module behavior, dependencies, or test expectations the plan does not state.
- Writing outside the new project folder.
