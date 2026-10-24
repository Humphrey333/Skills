---
name: embed_programming
description: "Use when writing or modifying code in an embedded project (new module, bug fix, refactor, dependency choice), especially while executing an approved plan with embed_executing_plans. Not for: planning a topic (use embed_planning-embedded-topics), locating a bug without changing code (use embed_debug), or docs (use embed_document)."
---

# Embedded Programming

## Overview

Write the least code that fully solves the task. New code gets a structure that is easy to extend and easy to manage. Existing code gets the smallest complete change. Reply in a way a busy developer understands in one read.

## When to Use

- Any code change: new file or module, bug fix, refactor, adding a dependency.
- Loaded by `embed_executing_plans` before its first todo.
- Not for: planning (use `embed_planning-embedded-topics`), reading code to find a bug (use `embed_debug`), writing docs (use `embed_document`).

## Before you write

Read the task and the code it touches. List every place the change must reach: callers, tests, fixtures, config, exports. Check what it could break: data it would destroy or expose, callers that stop working. That is the scope. Extra features are not.

If a fact is missing (a value, a pin, a timing, a behavior), ask. Never fill it in. Prefer reading documents online, without asking, and cite the URL; only a document that can't be read online goes into `Docs/REQUIRED_DOCS.md`, and the developer downloads it by hand.

## Function header comments

Every function you write or change gets a header comment with three parts, so a reviewer understands it from the Gitea pull request alone:

1. **Purpose**: one short line on what the function is for.
2. **In / out**: each parameter, the return value and any error or side effect (a register written, memory owned or released).
3. **How it works**: a few lines on the method: the order of steps, the protocol or register sequence, why it is done this way.

C and C++ use Doxygen:

```c
/**
 * @brief  Read the sensor chip ID over I2C.
 * @param  client  I2C client of the sensor; must be powered and out of reset.
 * @param  id      out: the 16-bit chip ID.
 * @return 0 on success, a negative errno on a bus error.
 *
 * How it works: reads the two ID registers high byte first, because the
 * sensor latches the low byte on the high-byte read.
 */
```

Linux kernel code uses kernel-doc (`/** name() - purpose`, `@arg:` lines, `Return:`) with the same three parts. Python uses a docstring, and other languages their own doc-comment form. When changing a function that has no header, add one. When its behavior changes, update the header in the same commit.

Inside the body, comment only the why the code cannot show: a register meaning, a timing constraint, why an order matters.

## Writing new code

For C or C++ code, read `references/cpp-embedded.md` first and follow it (ownership, constants, error checks, interrupt and real-time paths). The project's own style wins on a conflict; mention it.

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

**Never cut:** validation at trust boundaries, error handling that prevents data loss, security, the calibration real hardware needs, anything the developer asked for.

## Reply

End with one or two lines: what you skipped or did not check, and any risk the developer must know.

## Common Mistakes

- Writing C or C++ without reading `references/cpp-embedded.md`: raw `new`/`delete`, `#define` constants, blocking or allocating in an interrupt path.
- A new or changed function without its header comment (purpose, in / out, how it works), or a header left stale after the behavior changed.
- Adding an option, wrapper, abstraction or dependency nobody asked for.
- Writing new code with no structure, or old code with a rewrite, instead of the rule for its case.
- Changing, reformatting or deleting code the task does not name.
- Fixing a bug in one caller without grepping the others.
- Dropping validation or error handling when moving code.
- Guessing a register value, pin or timing, downloading a datasheet, or using an online fact without its URL.
- Body comments that restate the code instead of explaining the non-obvious why.
- New non-trivial logic with no test or self-check.
- A reply that hides what was skipped or what is risky.

---

Derived from `ponytail` by DietrichGebert (MIT License). Rewritten for the `embed_*` chain: no levels or slash commands, and a structure-first rule for new code.
