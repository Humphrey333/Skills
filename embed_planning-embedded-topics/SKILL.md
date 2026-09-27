---
name: embed_planning-embedded-topics
description: Use when starting a new embedded-engineering topic (new peripheral bring-up, subsystem, board support, or feature) that needs research and a plan before implementation — not for an existing bug (see embedded-debugging instead).
---

# Planning Embedded Topics

## Overview

A new embedded topic goes through three stages, in strict order: research (facts and trade-offs only, no code), planning (pick a direction, then build a step-by-step plan), and output (the actual pseudocode/reference code and setup docs). Each stage's saved doc lives at `Plans/YYYY-MM-DD-<topic-slug>.md`, kept updated as stages complete.

## When to Use

- Starting a new peripheral bring-up, subsystem, board support effort, or feature in embedded Linux/firmware work.
- Not for: an existing bug or misconfiguration (use `embedded-debugging`), or a trivial one-line change.

## Stage 1 — Research (facts and trade-offs only — no code)

- Gather and summarize what's known about the topic/problem domain: relevant existing code in the project, prior art, platform/hardware constraints.
- **Hard rule:** if information is missing, or a platform/component document is needed (datasheet, TRM, errata), stop and ask the developer — do not guess. Same no-fetch rule as `embedded-debugging` Stage 2: never download a document yourself; name the exact document (or search segments if unsure) and wait for the developer to supply it.
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

- Generating pseudocode or code during Stage 1 or Stage 2 — reference code only belongs in Stage 3.
- Skipping the pros/cons/trade-offs comparison in Stage 1 because one option "obviously" wins.
- Picking the direction for the developer instead of asking in Stage 2 Step 1.
- Writing plan steps without concrete, actionable instructions for whoever implements them.
- Machine-sounding comments that restate the code instead of explaining the non-obvious reasoning behind it.
- Inventing a code pattern instead of grounding Stage 3 output in verified sample code/reference flow.
- Guessing at missing information or fetching a platform document yourself instead of asking (Stage 1 hard rule).
