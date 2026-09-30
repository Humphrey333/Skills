---
name: embed_planning-embedded-topics
description: Use when starting a new embedded-engineering topic (new peripheral bring-up, subsystem, board support, or feature) that needs research and a plan before implementation — not for an existing bug (see embed_debug instead).
---

# Planning Embedded Topics

## Overview

A new embedded topic goes through three stages, in strict order: research (facts and trade-offs only, no code), planning (pick a direction, then build a step-by-step plan), and output (the actual pseudocode/reference code and setup docs). Each stage's saved doc lives at `Plans/YYYY-MM-DD-<topic-slug>.md`, kept updated as stages complete.

## When to Use

- Starting a new peripheral bring-up, subsystem, board support effort, or feature in embedded Linux/firmware work.
- Not for: an existing bug or misconfiguration (use `embed_debug`), or a trivial one-line change.

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.claude/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.claude/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Stage 1 — Research (facts and trade-offs only — no code)

> **We are not coding yet. Ask questions about anything you're uncertain about.**

- Gather and summarize what's known about the topic/problem domain, starting from the knowledge loaded in Step 0: relevant existing code in the project, prior art, platform/hardware constraints. Open questions recorded in knowledge files are still open — ask them, don't treat them as answered.
- **Hard rule — ask, never assume:** if any point relevant to the topic isn't explicitly stated by the developer — requirements, constraints, hardware details, desired behavior, scope, edge cases, a platform/component document (datasheet, TRM, errata) — stop and ask. Do not guess, infer a "reasonable default," or fill the gap yourself, even temporarily. Same no-fetch rule as `embed_debug` Stage 2 for documents: never download one yourself; name the exact document (or search segments if unsure) and wait for the developer to supply it.
  - Stating an assumption out loud ("I'll assume X unless told otherwise") does not satisfy this rule — it is still an assumption. Ask the question and wait for an explicit answer instead of proceeding on a caveat.
  - An inference drawn from the existing codebase is a *suggested answer*, not a confirmed one — surface it as part of the question, don't substitute it for asking.

  | Rationalization | Reality |
  |---|---|
  | "This detail is minor/obvious" | If the developer didn't say it, it isn't confirmed. Ask. |
  | "I'll state my assumption and keep going" | A stated assumption is still unconfirmed — get an explicit answer before using it. |
  | "Asking slows things down" | An acted-on wrong assumption costs far more than one question. |
  | "I can infer this from the code" | Inference isn't the developer's confirmation — offer it as your suggested answer within the question. |
  | "It's just research, not code yet" | Research is exactly where an unconfirmed assumption gets baked into the plan, then the code. |

  Red flags — stop and ask instead of continuing: writing "assuming…"/"presumably…" anywhere in the doc; filling in a register value, pin, timing, protocol detail, or behavior that wasn't stated or supplied; picking a default for anything the developer left open.
- For every viable approach/aspect, write out explicit **pros, cons, and trade-offs**. This comparison is the most important output of this stage — don't skip or shortcut it even when one option looks obviously best.
- Note any experiments that would help down-select between close options (e.g. a quick spike, a benchmark, a hardware-in-loop check).
- **Do not generate pseudocode or implementation code here** — that belongs only to Stage 3.

## Stage 2 — Planning (two steps, in order)

### Step 1 — Choose Direction

Present the researched approaches with their trade-offs and ask the developer which direction/technology/method to pursue. Do not pick for them. Wait for an explicit choice before moving on.

### Step 2 — Build the Step-by-Step Plan

Once a direction is chosen, write the implementation/porting plan as ordered steps. Every step that involves programming must carry concrete instructions (what to change, which files/APIs/registers, why). Include verification criteria alongside the plan (tests, hardware-in-loop checks, expected log/register state, how to confirm each step worked).

## Stage 3 — Output

Only now generate implementation artifacts, following the Stage 2 plan:

- **Pseudocode/reference code** that follows the flow of verified sample code already in the project or supplied by the developer — ground it in precedent, don't invent an unfamiliar pattern.
- **Comments** must read like a human explaining the non-obvious part of a block to another developer (register meaning, protocol step, timing constraint, why this order matters) — not restating what the code already shows.
- **Deliverables:**
  - A brief `README` explaining what the feature/topic is and how it works
  - Dependency install instructions
  - Instructions to build/run the result

## Save the Topic Doc

Write/update `Plans/YYYY-MM-DD-<topic-slug>.md` as stages complete: research summary + trade-offs (Stage 1), chosen direction + step-by-step plan + verification criteria (Stage 2). Stage 3's code/README/instructions are project deliverables, not part of this doc.

## Common Mistakes

- Skipping Step 0 — re-researching or re-asking what's already recorded in `~/.claude/Knowledge/`, or re-proposing an option a prior session already rejected.
- Generating pseudocode or code during Stage 1 or Stage 2 — reference code only belongs in Stage 3.
- Skipping the pros/cons/trade-offs comparison in Stage 1 because one option "obviously" wins.
- Picking the direction for the developer instead of asking in Stage 2 Step 1.
- Writing plan steps without concrete, actionable instructions for whoever implements them.
- Machine-sounding comments that restate the code instead of explaining the non-obvious reasoning behind it.
- Inventing a code pattern instead of grounding Stage 3 output in verified sample code/reference flow.
- Guessing at missing information or fetching a platform document yourself instead of asking (Stage 1 hard rule).
- Filling any undeclared point — a detail, default, or inference — with an assumption instead of stopping to ask, or stating the assumption as a caveat instead of getting explicit confirmation.
