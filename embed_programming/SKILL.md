---
name: embed_programming
description: Use when writing or modifying code in an embedded project (new module, bug fix, refactor, dependency choice), especially while executing an approved plan with embed_executing_plans. Not for: planning a topic (use embed_planning-embedded-topics), locating a bug without changing code (use embed_debug), or docs (use embed_document).
---

# Embedded Programming

## Overview

Write the least code that fully solves the task. New code gets a structure that is easy to extend and easy to manage. Existing code gets the smallest complete change. Reply in a way a busy developer understands in one read.

## When to Use

- Any code change: new file or module, bug fix, refactor, adding a dependency.
- Loaded by `embed_executing_plans` before its first task.
- Not for: planning (use `embed_planning-embedded-topics`), reading code to find a bug (use `embed_debug`), writing docs (use `embed_document`).

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.claude/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.claude/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Before you write

Read the task and the code it touches. List every place the change must reach: callers, tests, fixtures, config, exports. Check what it could break: data it would destroy or expose, callers that stop working. That is the scope. Extra features are not.

If a fact is missing (a value, a pin, a timing, a behavior), ask. Never fill it in. Never fetch a platform document; name it and wait for the developer.

## Writing new code

Pick the structure that is easy to extend and manage, and accept the extra effort it takes: clear module boundaries, one job per file, names that say the job, config in one place. Then write only what the task needs inside that structure. Structure is not speculation: no unused options, hooks or "for later" code.

## Modifying existing code

Take the first option that fully works:

1. Does it need to exist? Skip features nobody asked for, and name them in one line.
2. Already in this codebase (helper, pattern)? Use it the way the surrounding code does.
3. Standard library or a platform feature? Use it, unless the project has its own.
4. An installed dependency? Use it. Never add one for a few lines.
5. Otherwise the minimum code that works.

- Be lazy about the solution, never about the change: finish every caller, test and fixture it breaks.
- Match the existing style, even if you would do it differently. Do not touch adjacent code. Mention unrelated dead code, do not delete it.
- Bug fix: grep every caller of the function you touch, then fix the root cause once, in the shared code.
- Code you move or merge keeps its error handling and validation.
- Remove only what your change made unused.
- New non-trivial logic (a branch, a loop, a parser, a protocol step) leaves one small test or assert-based self-check.
- A shortcut with a known limit gets one comment: `shortcut: <the limit>, <when to upgrade>`.
- Comment only the why the code cannot show: a register meaning, a timing constraint, why an order matters.

**Never cut:** validation at trust boundaries, error handling that prevents data loss, security, the calibration real hardware needs, anything the developer asked for.

## Reply

End with one or two lines: what you skipped or did not check, and any risk the developer must know.

## Common Mistakes

- Skipping Step 0.
- Adding an option, wrapper, abstraction or dependency nobody asked for.
- Writing new code with no structure, or old code with a rewrite, instead of the rule for its case.
- Changing, reformatting or deleting code the task does not name.
- Fixing a bug in one caller without grepping the others.
- Dropping validation or error handling when moving code.
- Guessing a register value, pin or timing, or fetching a datasheet instead of asking.
- Comments that restate the code instead of explaining the non-obvious why.
- New non-trivial logic with no test or self-check.
- A reply that hides what was skipped or what is risky.

---

Derived from `ponytail` by DietrichGebert (MIT License). Rewritten for the `embed_*` chain: no levels or slash commands, and a structure-first rule for new code.
