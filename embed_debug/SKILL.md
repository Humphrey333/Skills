---
name: embed_debug
description: Use when a developer reports a bug, crash, kernel panic/oops, hang, or misconfiguration (e.g. a misbehaving camera sensor) in embedded Linux code or configuration (drivers, bootloader, device-tree/sensor settings, userspace daemons) and wants to know where and why it breaks, especially when the report is incomplete or platform documentation is needed. Not for: a new bring-up or feature (use embed_planning-embedded-topics), learning a topic (use embed_learning), or saving session knowledge (use embed_summary).
---

# Embedded Debugging

## Overview

Find the exact place, or places, in the code that cause the symptom the developer reported. Explain each one so a person gets it on the first read: short, plain words, still precise. Then talk through how to fix each one, also in plain words. Finish with a report. Claude reads and reasons only. It does not run or reproduce the failure, because target hardware is usually not available.

**Violating the letter of these rules is violating the spirit of them.**

## When to Use

- Bug reports, crashes, kernel oops/panics, hangs, misbehaving peripherals (e.g. a camera sensor module like Sony IMX586 producing bad frames), or misconfiguration in embedded Linux code or configuration (kernel drivers, bootloader, device-tree/sensor settings, userspace daemons).
- Not for: a new bring-up, subsystem or feature (use `embed_planning-embedded-topics`); learning a topic (use `embed_learning`); saving session knowledge (use `embed_summary`); bugs in code Claude can directly execute/test (e.g. a hosted app with a runnable test suite), where normal debugging applies.

## Hard Rules

These hold in every stage, including when the developer is in a hurry.

1. **No code, no fix.** Write no patch, diff, code snippet, printk/debug line, changed value, repro program or script, and edit no source file. You may point at `file:line` and quote up to 2 *existing* lines that are wrong. The only file this skill writes is the report (Stage 4). If the developer asks for code or a patch, say that this skill stops at the agreed solution in words, and that the report is the input for doing the fix afterwards.
2. **Ask, never assume.** If a fact the analysis depends on was not stated or supplied, ask, and wait for the answer. This covers requirements, hardware details, a register value, timing, an expected behavior, and a document. A guess from the code is a *suggested answer* inside the question, never a conclusion. "I'll assume X unless told otherwise" is still an assumption.
3. **Never fetch or download a document yourself** (datasheet, TRM, errata, app note). Name the exact document, or give search segments, then stop and wait for the developer to supply it (Stage 2).
4. **One point per message, in the template.** Each point and each solution uses the fixed template below, in short plain words. Then wait for the developer before moving on.
5. **Stay on the reported symptom.** Suspicious code that does not explain the reported symptom goes on the *also noticed* list. It gets no explanation until every reported point has been covered and the developer asks for the list.

| Rationalization | Reality |
|---|---|
| "A one-line diff is clearer than words" | Say what to change and where in words. Code is out of scope for this skill. |
| "The developer asked for the patch / is in a hurry" | Give the cause and the solution in words, one point at a time. Hurry is when a wrong guess costs most. |
| "It's only a debug print / test script, not a fix" | Still code. Describe what to check and what result to look for. |
| "Raising the timeout to N is a safe guess" | N is invented. Name the document the real value comes from and wait. |
| "I can work out the rate/clock myself" | A number nobody supplied is an assumption. Ask, or name the document. |
| "Listing every bug at once saves time" | The developer can't check five points at once. One point, then wait. |
| "Those cleanup bugs are real, I should mention them" | Put them on the *also noticed* list and offer it at the end. |

Red flags: stop and rewrite the message if it contains any of these:
- a ```` ``` ```` block with new code
- `diff`/`+`/`-` lines
- "assuming…", "probably around…", "roughly N"
- a value you chose yourself
- more than one point
- an unrelated bug before the *also noticed* stage

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.claude/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.claude/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Stage 1 — Understand (ask before pointing at anything)

1. **Scan the code.** Get the overall structure first, then the code path behind the symptom: error string, function, probe path, IRQ/register, device-tree node/property, sensor mode/register table.
2. **Run the info gate** against the developer's report. Items already covered by loaded knowledge are not asked again.
   - **Context**: what the system/component is supposed to do
   - **Code/file references**: relevant files, functions, or subsystem
   - **Exact error output**: verbatim (oops/panic trace, log lines, error codes), not paraphrased
   - **Symptoms**: *known* (observed) kept apart from *suspected* (guessed)
   - **What's been tried**: causes or fixes already ruled out
   - **Verification**: how a point can be checked (a log line, a register read, a test)
   - **Focus**: anything the developer wants looked at or left out
3. **Mental-model check.** Ask what the code is *supposed* to do at the failure point. The gap between that and what it does is often the bug.
4. **Ask for everything missing in one message**: facts, files, documents. You may offer a suggested answer from the code inside each question. Do not present any point until the answers are in. If the developer explicitly says to go on without an item, note the gap and continue.

## Stage 2 — Point by Point

1. List the candidate points that explain the **reported** symptom, most likely first. Anything that doesn't explain it goes on the *also noticed* list (Hard Rule 5).
2. Present **one point per message** in this template, then wait:

   ```
   Point N of M — <short name>
   - Where: `path/file.c:123` in `function()`
   - What goes wrong: 1–3 short sentences in everyday words. Use a technical
     term only when needed, and explain it in a few words.
   - Why this gives your symptom: tie it to the exact error/log the developer gave.
   - How sure: confirmed / likely / possible, and what that rests on.
   - How to check: one thing the developer can run or look at, and which
     result means yes or no (see references/techniques.md).
   ```

   Then ask: *"Does this match what you see? Shall I go to the next point?"*

3. The developer agrees, rejects or asks for a check. Record the outcome (confirmed / rejected and why / open) and only then present the next point.
4. **Documentation stop.** If a point can't be settled from the code alone, name the document and wait (Hard Rule 3). This happens with configuration (register settings, DT properties, init/mode-switch sequences, timing) and with vendor BSP/downstream code (NVIDIA L4T, TI Processor SDK, NXP BSP).
   - If you can name the exact document (e.g. "Sony IMX586 Product Datasheet Rev X", "NVIDIA Jetson AGX Xavier TRM v1.3"), give its exact title, and a link if a search finds one.
   - Otherwise give search segments: part number, vendor, document type, suspected revision.
   - Mark the point *open* and do not guess register values or timing from memory. Resume when the developer confirms the document is available.
5. **When every point is covered**, give one line per point with its outcome. Then ask whether to go through the *also noticed* list. If yes, use the same loop and template.
6. **Nothing found?** Ask specific narrowing questions tied to what you've already ruled out, not a repeat of Stage 1. For example:
   - "Does this reproduce with `<subsystem/config>` disabled?"
   - "What's the value of `<variable/register>` at the point of failure?"
   - "All boards/revisions, or just one?"

Example. The developer reported `chip id mismatch: got 0x0000` at probe, on the new board revision only.

Bad (jargon, a fix, and several points in one message):
> `reset-gpios` is `GPIO_ACTIVE_HIGH` but `gpiod_set_value(reset, 0)` deasserts logically, so the line stays physically asserted and the I2C read returns 0; change the DT flag to `GPIO_ACTIVE_LOW`. Also `of_node_put` is missing and the regulator delay is short.

Good:
> **Point 1 of 2 — the camera is kept in reset**
> - Where: `board-revb.dts:212`, the `reset-gpios` line of the camera node
> - What goes wrong: the board file says the reset pin is "on when high". The new board wires it the other way round. So when the driver lets go of reset, the pin actually ends up holding the camera in reset.
> - Why this gives your symptom: a camera held in reset doesn't answer, so the ID read comes back as all zeros, which is the `0x0000` in your log.
> - How sure: likely. It rests on the board-rev diff; the schematic isn't checked yet.
> - How to check: measure the reset pin while the driver probes. If it stays low the whole time, this is it.

## Stage 3 — Solutions (in words only)

Once every point has an outcome, recommend a solution for each confirmed point. If one change fixes several points, give one solution for that group. Use this template:

```
Solution for Point N (or Points N, M) — <short name>
- Change: what to change and where, in plain words (no code)
- Why it fixes it: link back to the point
- Watch out for: side effects or risks
- How to verify: what the developer should see afterwards
```

The developer discusses how to apply each solution. Update it until they agree. Values that need a document follow Hard Rule 3. Hard Rule 1 still holds: no code or patch, even when the developer asks.

## Stage 4 — Report

1. **Recap**, with nothing new added. Cover:
   - **Symptom**, as reported
   - **Facts and documents provided**
   - **Points**, in the template, each with its outcome: confirmed / rejected and why / open
   - **Agreed solutions**, in the template
   - **Also noticed**
   - **Open questions**
2. Propose the name `Debug_<bug-slug>_<YYYY-MM-DD>.md`, written in the **directory the skill was invoked from** (the current working directory, not `Plans/`). Ask once: *"Do you agree with this report and its name?"*
3. Write it **only on an explicit yes**. A correction or a "no" means fix it, show it again and ask again. Silence or "whatever" is not a yes. Tell the developer the path once written.

## Common Mistakes

- Skipping Step 0, so facts, documents or ruled-out causes already recorded in `~/.claude/Knowledge/` get asked for again.
- Pointing at a cause before the Stage 1 questions are answered.
- Assuming, or stating an assumption as a caveat, instead of asking.
- Writing any code: a patch, a diff, a debug print, a test script, or a changed value. Also editing a source file. This holds even when the developer is in a hurry or asks for it.
- Inventing a number (timeout, clock, rate) instead of naming the document it comes from.
- Fetching or downloading a document yourself.
- Putting more than one point in a message, or moving on before the developer has answered.
- Leaving out a template field, or explaining in jargon without plain words.
- Mixing suspicious code that doesn't explain the reported symptom into the points instead of the *also noticed* list.
- Giving solutions before every point has an outcome.
- Writing the report without an explicit yes, under another name, or outside the invocation directory.
- Asking generic follow-ups ("more info?") instead of specific narrowing questions.
- Trying to run or reproduce the bug yourself, instead of giving the developer a check to run.
