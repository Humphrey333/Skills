---
name: embedded-debugging
description: Use when a user reports a bug, crash, kernel panic/oops, hang, or misconfiguration (e.g. a misbehaving camera sensor) in embedded Linux code or configuration (drivers, bootloader, device-tree/sensor settings, userspace daemons), especially when the report is incomplete or platform documentation is needed to locate the cause.
---

# Embedded Debugging

## Overview

Locate embedded Linux bugs — in code logic or in configuration (sensor/peripheral register settings, device-tree properties, init/mode-switch sequences) — by reading and reasoning from the user's description, not by running or reproducing the failure directly (target hardware/serial console usually isn't available). Core principle: get precise facts first, search the code, pull in platform documentation when the source alone doesn't explain it, then narrow with hypotheses; only ask more questions when all of that stalls.

## When to Use

- Bug reports, crashes, kernel oops/panics, hangs, misbehaving peripherals (e.g. a camera sensor module like Sony IMX586 producing bad frames), or misconfiguration in embedded Linux code or configuration (kernel drivers, bootloader, device-tree/sensor settings, userspace daemons).
- Not for: greenfield feature design, or bugs in code Claude can directly execute/test (e.g. a hosted app with a runnable test suite) — normal debugging applies there instead.

## Stage 0 — Info Gate (mandatory, do this first)

Before searching any code, confirm the report includes:

- **Context** — what the system/component is supposed to do
- **Code/file references** — relevant files, functions, or subsystem
- **Exact error output** — verbatim (oops/panic trace, log lines, error codes), not paraphrased
- **Symptoms** — clearly separate what's *known* (observed) from what's *suspected* (guessed)
- **What's been tried** — already-ruled-out causes or fixes
- **Verification** — any way to check a hypothesis or a fix (a test, a log line, a register read)
- **Desired output** — a solution, a checklist, or an explanation?

If anything is missing or vague, ask for it specifically before proceeding — don't guess or start searching on an incomplete report. If the user explicitly says to proceed without an item, note the gap and continue anyway.

## Stage 1 — Search the Code

Using the gathered facts:

1. **Mental-model check** — ask the user to state what the code is *supposed* to do at the failure point, and compare that against what it actually does. The mismatch is often the bug itself.
2. **Targeted search** — grep/read the referenced files and the failure's code path (error string, function name, IRQ/register, driver probe path, device-tree node/property, sensor mode/register table), guided by the exact error output.
3. If found: report the file/line and the mechanism, then suggest a fix or a way to verify it.

## Stage 2 — Get Platform/Component Documentation (when code alone isn't enough)

Trigger this when the bug looks like a **configuration** issue (sensor/peripheral register settings, device-tree properties, init/mode-switch sequences — e.g. a camera sensor module like Sony IMX586) or the code lives in a vendor BSP/downstream fork (NVIDIA Linux for Tegra, TI Processor SDK, NXP BSP, etc.) where generic kernel/driver knowledge doesn't explain the failure.

**Hard rule: never fetch or download a document yourself.** Acquiring external documents is the developer's call, not something to do automatically — treat this as a security boundary.

1. If you can identify the exact document (e.g. "Sony IMX586 Product Datasheet Rev X", "NVIDIA Jetson AGX Xavier TRM v1.3"), search for it if you have search tools available, and give the developer the exact title — and a link if you found one — so *they* download it. Do not fetch the document's contents yourself.
2. If you can't pin down the exact document, give descriptive **search segments** instead — part number, vendor, document type (datasheet / TRM / application note / errata sheet), suspected version/revision — so the developer (or a colleague) can search for it manually.
3. Stop and wait: don't guess at register values or timing from memory once you've flagged that a doc is needed. Resume analysis once the developer confirms the document is available (pasted, attached, or placed in the repo).

## Stage 3 — If Still Not Found, Narrow Down

Pick whichever fits — don't run all of them:

| Approach | Use when |
|---|---|
| Elimination checklist | Several plausible causes; need to rule out one at a time |
| Suggestions/tips | Stuck, want fresh angles to try |
| `git bisect` | Regression — worked before, broke after some change |
| Simplify to a standalone program | Bug is in portable/userspace logic; can run on the dev machine under sanitizers (ASan/UBSan) instead of only on target |
| `creduce` | Have a failing C repro, but it's too large to reason about |

See `references/techniques.md` for how to apply each.

**If code search and narrowing still don't pin it down**, ask the developer specific, narrowing questions — not a repeat of Stage 0, but targeted questions that close the remaining gap, e.g.:

- "Does this reproduce with `<subsystem/config>` disabled?"
- "What's the value of `<variable/register>` at the point of failure?"
- "Does it happen on all boards/revisions, or just one?"

## Common Mistakes

- Skipping the info gate and searching on a vague report — wastes cycles on the wrong code path.
- Treating "what's been tried" as optional — re-suggesting already-ruled-out fixes wastes the developer's time.
- Trying to execute or reproduce the bug directly — usually not possible on embedded targets; reason about the code and give guidance instead.
- Fetching or downloading platform documentation yourself instead of naming it (or search segments for it) and letting the developer obtain it.
- Guessing at register values, timing, or vendor-specific behavior from memory instead of flagging that a platform doc is needed.
- Asking generic follow-ups ("can you give more info?") instead of specific narrowing questions tied to what's been found so far.
