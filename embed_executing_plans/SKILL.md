---
name: embed_executing_plans
description: "Use when an embedded-engineering plan (Plans/Plan_<slug>_<date>.md from embed_planning-embedded-topics) has been approved and its tasks must now be implemented, or the developer says \"execute the plan\" or \"start coding the plan\". Not for: planning a new topic (use embed_planning-embedded-topics), locating a bug (use embed_debug), or writing docs (use embed_document)."
---

# Executing Plans

## Overview

Run an approved plan task by task, in this session. Every code or document change is shown to the developer and needs an explicit yes before it is written. Everything else runs without stopping. The plan already did the thinking: follow it exactly, and ask when it is wrong or silent.

**Violating the letter of these rules is violating the spirit of them.**

## When to Use

- A plan exists at `Plans/Plan_<slug>_<date>.md` with a `## Tasks` list, and the developer approved it.
- Not for: a plan that is not approved or has no `## Tasks` (go back to `embed_planning-embedded-topics`); a bug with no plan yet (use `embed_debug`); docs only (use `embed_document`).

## Hard Rules

1. **Gate the changes, not the tasks.** An explicit yes is needed for exactly these, and nothing else:
   1. changing existing code, shown as a line-by-line diff per file;
   2. adding new code, shown one function block (function, class or struct) per message;
   3. settling a bug point or choosing a solution;
   4. moving to the next workflow step;
   5. changing a document, shown as a diff.

   Show the change before writing it. Silence, "ok whatever" or your own judgment is not a yes. Reading, searching, host builds and tests, ticking the plan and a task's verify step run without stopping. A failed verify stops and reports.
2. **Follow the plan.** Do not add, skip, reorder or reshape tasks. If a task is wrong, impossible or silent on a needed detail, stop and ask. Do not rule on it yourself.
3. **Ask, never assume.** A register value, pin, timing, path or behavior the plan and the developer did not give is asked for. A stated assumption is still an assumption.
4. **Never fetch or download a document** (datasheet, TRM, errata, app note). Name the exact document, or give search segments, and wait for the developer to supply it.
5. **Code follows `embed_programming`.** Load it before the first task.
6. **Evidence before claims.** A task is done only when its `verify` step ran in this session and you read the output. Hardware checks that cannot run here are handed to the developer with the expected result, and the task stays open until they report.

| Rationalization | Reality |
|---|---|
| "This change is small, I'll write it and show it after" | Show it first. A yes after the fact is not approval. |
| "I'll show the whole new file at once" | Modified code: a line-by-line diff. New code: one function block per message. |
| "I'll ask before running the tests too" | Host builds, tests and verify steps run without stopping. Only the five gates wait. |
| "The plan is wrong here, I'll do the right thing" | Stop and ask. A silent deviation is an unapproved change. |
| "It should pass, the change was trivial" | "Should" is not evidence. Run the verify step and read it. |
| "I'll fill in this value, it is the usual one" | A value nobody supplied is an assumption. Ask, or name the document. |
| "Asking again slows things down" | A wrong task built on a guess costs the whole task again. |

Red flags — stop: writing code or a doc before its yes; editing a file no task names; writing "assuming…"; a verify step you did not run.

## The Task Loop

1. **Setup (once).** Read the plan and its `## Tasks`. Tick state lives in the plan: a task marked `- [x]` is done, so resume at the first `- [ ]`. Tell the developer which task you are starting. Load `embed_programming`.
2. **Do the task.** Prepare exactly the change the task describes, in the files it names. Show it in the gate's form (Hard Rule 1) and write it only after the yes for that diff or block. When the check can run on the host, write it first and watch it fail, then make it pass.
3. **Verify.** Run the task's `verify` step. Show the command and the real output.
4. **Report.** Use this shape, then go on to the next task. Stop only when the next task needs a gate, verify failed, or a hardware check is with the developer:

   ```
   Task N of M — <name>
   - Changed: files and a one-line summary each
   - Verified: command → result (or: hand-off check for the developer + expected result)
   - Deviations: none / the question you need answered
   ```

   Pass the report's wording through `embed_writing`. Commands and their real output stay unchanged.

5. **Tick** the task `- [x]` in the plan file once its verify passed (or the developer reported the hardware check). A correction means fix the task and show it again.

## Board results (bug-fix plans)

When the plan came from a `Debug_*.md` report (it has a `## Board results` section), each task's board check goes to the developer. Record every report there: solution, tested or not, worked or not, what the developer saw. When every solution is tested:

- One worked: go to Finish.
- None worked: show every point and solution tried, with its result, and propose going back to `embed_debug` with that list (its re-entry case). Do not look for new causes yourself.

## Finish

After the last task is ticked:

1. Read the whole diff once against the plan. Report anything the plan did not ask for, and anything a task left undone.
2. Propose Step 3 (optional), and wait. Do not run them yourself: `/embed_summary` captures what was learned, `/embed_document` updates README.md and BUILD.md.

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question, or remove or change a fact, reason, hedge or warning.
- Writing a code or document change before the developer's yes, or showing a whole file instead of a line-by-line diff or one function block at a time.
- Stopping for a yes on reading, searching, a host build, a test or a verify step.
- Deviating from the plan (adding, skipping, reordering, reshaping a task) instead of stopping to ask.
- Assuming a missing value or fetching a platform document instead of asking.
- Claiming a task done without running its verify step, or without reading the output.
- Marking a hardware-only check as passed instead of handing it to the developer.
- Not recording board results, or hunting for a new cause yourself when no solution worked instead of proposing `embed_debug` re-entry.
- Writing code without loading `embed_programming`.
- Running `/embed_summary` or `/embed_document` yourself instead of proposing them.
- Forgetting to tick `- [x]` in the plan, so a resumed session redoes finished tasks.

---

Derived from `executing-plans` in obra/superpowers (MIT License). Rewritten for the `embed_*` chain: per-change approval gate, no subagents, worktrees or ledger scripts.
