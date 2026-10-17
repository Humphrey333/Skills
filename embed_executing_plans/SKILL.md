---
name: embed_executing_plans
description: Use when an embedded-engineering plan (Plans/Plan_<slug>_<date>.md from embed_planning-embedded-topics) has been approved and its tasks must now be implemented, or the developer says "execute the plan" or "start coding the plan". Not for: planning a new topic (use embed_planning-embedded-topics), locating a bug (use embed_debug), or writing docs (use embed_document).
---

# Executing Plans

## Overview

Run an approved plan one task at a time, in this session. After each task, show the result and its verification, then wait for the developer's explicit yes before the next task. The plan already did the thinking: follow it exactly, and ask when it is wrong or silent.

**Violating the letter of these rules is violating the spirit of them.**

## When to Use

- A plan exists at `Plans/Plan_<slug>_<date>.md` with a `## Tasks` list, and the developer approved it.
- Not for: a plan that is not approved or has no `## Tasks` (go back to `embed_planning-embedded-topics`); a bug with no plan yet (use `embed_debug`); docs only (use `embed_document`).

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.claude/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.claude/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Hard Rules

1. **One task, then stop.** After a task, show what changed and the verification output, then wait for an explicit yes. Silence, "ok whatever" or your own judgment is not a yes.
2. **Follow the plan.** Do not add, skip, reorder or reshape tasks. If a task is wrong, impossible or silent on a needed detail, stop and ask. Do not rule on it yourself.
3. **Ask, never assume.** A register value, pin, timing, path or behavior the plan and the developer did not give is asked for. A stated assumption is still an assumption.
4. **Never fetch or download a document** (datasheet, TRM, errata, app note). Name the exact document, or give search segments, and wait for the developer to supply it.
5. **Code follows `embed_programming`.** Load it before the first task.
6. **Evidence before claims.** A task is done only when its `verify` step ran in this session and you read the output. Hardware checks that cannot run here are handed to the developer with the expected result, and the task stays open until they report.

| Rationalization | Reality |
|---|---|
| "The next task is small, I'll just do it too" | One task per approval. The gate is the product. |
| "The plan is wrong here, I'll do the right thing" | Stop and ask. A silent deviation is an unapproved change. |
| "It should pass, the change was trivial" | "Should" is not evidence. Run the verify step and read it. |
| "I'll fill in this value, it is the usual one" | A value nobody supplied is an assumption. Ask, or name the document. |
| "Asking again slows things down" | A wrong task built on a guess costs the whole task again. |

Red flags — stop: starting task N+1 without a yes for N; editing a file no task names; writing "assuming…"; a verify step you did not run.

## The Task Loop

1. **Setup (once).** Read the plan and its `## Tasks`. Tick state lives in the plan: a task marked `- [x]` is done, so resume at the first `- [ ]`. Tell the developer which task you are starting. Load `embed_programming`.
2. **Do the task.** Make exactly the change the task describes, in the files it names. When the check can run on the host, write it first and watch it fail, then make it pass.
3. **Verify.** Run the task's `verify` step. Show the command and the real output.
4. **Report and wait.** Use this shape, then ask *"Approve task N and go to task N+1?"*:

   ```
   Task N of M — <name>
   - Changed: files and a one-line summary each
   - Verified: command → result (or: hand-off check for the developer + expected result)
   - Deviations: none / the question you need answered
   ```

   Pass the report's wording through `embed_writing`. Commands and their real output stay unchanged.

5. **On an explicit yes,** tick the task `- [x]` in the plan file and take the next one. A correction means fix the task and show it again.

## Finish

After the last task is approved:

1. Read the whole diff once against the plan. Report anything the plan did not ask for, and anything a task left undone.
2. Propose Step 3, and wait. Do not run them yourself: `/embed_summary` captures what was learned, `/embed_document` updates README.md and BUILD.md.

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question.
- Skipping Step 0, so facts already recorded in `~/.claude/Knowledge/` get asked again.
- Starting the next task without an explicit yes, or batching several tasks into one report.
- Deviating from the plan (adding, skipping, reordering, reshaping a task) instead of stopping to ask.
- Assuming a missing value or fetching a platform document instead of asking.
- Claiming a task done without running its verify step, or without reading the output.
- Marking a hardware-only check as passed instead of handing it to the developer.
- Writing code without loading `embed_programming`.
- Running `/embed_summary` or `/embed_document` yourself instead of proposing them.
- Forgetting to tick `- [x]` in the plan, so a resumed session redoes finished tasks.

---

Derived from `executing-plans` in obra/superpowers (MIT License). Rewritten for the `embed_*` chain: per-task approval gate, no subagents, worktrees or ledger scripts.
