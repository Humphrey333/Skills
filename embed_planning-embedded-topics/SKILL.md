---
name: embed_planning-embedded-topics
description: "Use when starting a new embedded-engineering topic (new peripheral bring-up, subsystem, board support, or feature) that needs research and a plan before implementation, or when embed_debug has confirmed a cause and the fix needs a plan. Not for: an existing bug that is not yet located (use embed_debug), or running an already approved plan (use embed_executing_plans)."
---

# Planning Embedded Topics

## Overview

A new embedded topic goes through three stages, in strict order: research (facts and trade-offs only, no code), planning (pick a direction, then write a short plan: summary, recap of the decisions, todo list), and hand-off (the approved plan goes to `embed_executing_plans`). This skill never writes code. The plan is closed out with a clean recap and an explicit final approval, then stored as `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md` in the current directory before the hand-off.

## When to Use

- Starting a new peripheral bring-up, subsystem, board support effort, or feature in embedded Linux/firmware work.
- Planning the fix for a cause that `embed_debug` confirmed (its report is the input).
- Not for: an existing bug or misconfiguration that is not yet located (use `embed_debug`), running an approved plan (use `embed_executing_plans`), or a trivial one-line change.

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.agents/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.agents/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Bug-fix mode (input is a `Debug_*.md` report)

When the developer brings an `embed_debug` report, the report replaces the broad research of Stage 1:

1. Read the report. Its confirmed points and agreed solutions are the starting facts. Do not re-research the bug.
2. For each solution, find any document the fix needs: read it online first (cite the URL); only if it can't be read online, add it to `Docs/REQUIRED_DOCS.md` and wait for the developer to download and supply it.
3. Agree the fix for each solution with the developer. When a solution has several ways to apply it, give the trade-offs and let the developer choose (Stage 2 Step 1).
4. Write one todo per solution. The todo gives the smallest fix in words, following `embed_programming` (reuse what exists, fix the root cause, reach every caller), and ends with its check: `developer builds and runs on the board: <expected result from the report>`.
5. Add an empty `## Board results` section at the end of the plan; `embed_executing_plans` fills it.

Then continue with Stage 2 Step 3 (recap, approval, save) and Stage 3.

## Stage 1 — Research (facts and trade-offs only — no code)

> **We are not coding yet. Ask questions about anything you're uncertain about.**

- Gather and summarize what's known about the topic/problem domain, starting from the knowledge loaded in Step 0: relevant existing code in the project, prior art, platform/hardware constraints. Open questions recorded in knowledge files are still open — ask them, don't treat them as answered.
- **Hard rule — ask, never assume:** if any point relevant to the topic isn't explicitly stated by the developer — requirements, constraints, hardware details, desired behavior, scope, edge cases, a platform/component document (datasheet, TRM, errata) — stop and ask. Do not guess, infer a "reasonable default," or fill the gap yourself, even temporarily. Documents: prefer reading online; search and read them without asking, and cite the URL of every fact you use. Never download one; downloads are the developer's, by hand. Only a document that can't be read online goes into `Docs/REQUIRED_DOCS.md` in the project folder, one row per document: Document, Revision, Why needed, Search terms, Status (`needed`, then `supplied: Docs/<file>` or `not found (developer)`); then wait for the developer to supply it.
  - Stating an assumption out loud ("I'll assume X unless told otherwise") does not satisfy this rule — it is still an assumption. Ask the question and wait for an explicit answer instead of proceeding on a caveat.
  - An inference drawn from the existing codebase is a *suggested answer*, not a confirmed one — surface it as part of the question, don't substitute it for asking.

  | Rationalization | Reality |
  |---|---|
  | "This detail is minor/obvious" | If the developer didn't say it, it isn't confirmed. Ask. |
  | "I'll state my assumption and keep going" | A stated assumption is still unconfirmed — get an explicit answer before using it. |
  | "Asking slows things down" | An acted-on wrong assumption costs far more than one question. |
  | "I can infer this from the code" | Inference isn't the developer's confirmation — offer it as your suggested answer within the question. |
  | "It's just research, not code yet" | Research is exactly where an unconfirmed assumption gets baked into the plan, then the code. |
  | "They skipped that question, so it can't matter" | Unanswered is not "not needed". Ask again until they answer or say they can't. |
  | "The document they sent is close enough" | A wrong part, revision or a document without the needed fact does not answer the question. Say what is wrong and ask again. |

  Red flags — stop and ask instead of continuing: writing "assuming…"/"presumably…" anywhere in the doc; filling in a register value, pin, timing, protocol detail, or behavior that wasn't stated or supplied; picking a default for anything the developer left open.
- **Re-ask until answered.** Check every reply against the questions you asked. A question left unanswered, an answer that doesn't settle it, or a supplied document that is the wrong part or revision or doesn't hold the needed fact is asked again in the next message, saying what is still missing. Skip it only when the developer says they can't find it or have no information; then record it under the plan's open questions, and a document as `not found (developer)` in `Docs/REQUIRED_DOCS.md`. Never drop a question silently, and don't move to Stage 2 while one is still open.
- For every viable approach/aspect, write out explicit **pros, cons, and trade-offs**. This comparison is the most important output of this stage — don't skip or shortcut it even when one option looks obviously best.
- Note any experiments that would help down-select between close options (e.g. a quick spike, a benchmark, a hardware-in-loop check).
- **Do not generate pseudocode or implementation code here or anywhere in this skill** — code belongs to `embed_executing_plans` (with `embed_programming`).

## Stage 2 — Planning (two steps, in order)

### Step 1 — Choose Direction

Present the researched approaches with their trade-offs and ask the developer which direction/technology/method to pursue. Do not pick for them. Wait for an explicit choice before moving on.

### Step 2 — Write the Plan

The questions were asked carefully in Stage 1, so the plan stays short. Once a direction is chosen, write it in three parts, in this order:

1. **Summary**: what the plan is for and what it changes, in a few lines.
2. **Recap**: a short table of what was discussed and decided (constraints, chosen direction and the main trade-off, answers the developer gave, documents with their URL or `Docs/` path).
3. **`## Todo`**: a numbered checklist, `- [ ] N. <what to change, in which files/APIs/registers, and why>`. A todo that involves programming carries enough concrete detail to code it without asking. Each todo ends with its check (test, host build, expected log or register state, or a board check for the developer).

No step-by-step section besides the todo list. `embed_executing_plans` runs the todos in order on a branch from `dev`, one commit per todo, without asking between them.

The README and build/run instructions are not todos here. They are written afterwards with `embed_document`.

### Step 3 — Final Review and Approval (gate before Stage 3)

Once the plan is settled, do not move on silently:

1. **Show the plan cleanly and briefly** as a standalone document the developer can read without the discussion: the summary, the recap (topic/goal, confirmed constraints, chosen direction with the one-line reason and the main trade-off accepted), the `## Todo` list with each todo's check, and any still-open questions. No new content — only what was already agreed. Pass the recap's prose through `embed_writing` before showing it.
2. **Propose the file name** `Plan_<topic-slug>_<YYYY-MM-DD>.md` (slug = what the plan is for, e.g. `Plan_imx586-mipi-csi-bringup_2026-10-10.md`) and ask exactly once: *"Do you agree with this plan, and with saving it under this name?"*
3. **Wait for an explicit yes.** Corrections or "no" → fix the plan, re-show the recap, and ask again. Silence, "looks fine, whatever", or your own judgment that it's agreed does not count.
4. **On yes:** write the recap to `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md` in the current directory (create `Plans/` if missing), tell the developer the path, then continue to Stage 3. Do not start Stage 3 before the file is written.

## Stage 3 — Hand-off

The skill ends here. It writes no code, README or build instructions.

- Tell the developer the plan is ready to run with `embed_executing_plans`. It works on a branch from `dev` in the project's Gitea repo, commits each todo without asking, and uses `embed_programming` for the code. Then `embed_programming_discussion` pushes it as the `Agent` user and opens a pull request into `dev`. The developer reviews and merges it in Gitea.
- If the plan is for a new C/C++ userspace project, mention that `embed_create_coding_template` creates the skeleton, and `embed_programming_discussion` its Gitea repo, first (as the plan's first todo, if the developer wants it). A project with no Gitea repo can't use `embed_executing_plans`.
- Wait for the developer to start the next skill. Do not start it yourself.

## Save the Topic Doc

The stored doc is `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md` in the current directory, written once at the Stage 2 Step 3 approval gate (not before, not left unsaved after). Content: summary, recap of the discussion (with the Stage 1 trade-offs and the chosen direction), and `## Todo` (Stage 2). `embed_executing_plans` later ticks the todos and adds `## Review results` (and `## Board results` for a bug fix). If the plan changes later, update the same file and re-confirm with the developer.

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question, or remove or change a fact, reason, hedge or warning.
- Skipping Step 0 — re-researching or re-asking what's already recorded in `~/.agents/Knowledge/`, or re-proposing an option a prior session already rejected.
- Generating pseudocode or code at any stage — this skill plans only; code belongs to `embed_executing_plans`.
- Skipping the pros/cons/trade-offs comparison in Stage 1 because one option "obviously" wins.
- Picking the direction for the developer instead of asking in Stage 2 Step 1.
- Moving from Stage 2 to Stage 3 without the clean recap, the single final "do you agree?" question, and an explicit yes.
- Treating the developer's lack of objection as approval, or saving the plan file before they confirm it (and its name).
- Saving the plan under any name other than `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md`, or outside the current directory's `Plans/`.
- Writing todos without concrete, actionable instructions for whoever implements them, or without a check, so `embed_executing_plans` can't run and commit them one by one.
- Writing a long step-by-step section instead of the summary, recap and `## Todo` list.
- Writing the README or build instructions here, or starting `embed_executing_plans` without the developer asking.
- In bug-fix mode: re-researching the bug instead of starting from the report, or writing a fix todo whose check is not a board check by the developer.
- Guessing at missing information instead of asking, downloading a document yourself, listing one in `Docs/REQUIRED_DOCS.md` before trying to read it online, or using an online fact without its URL (Stage 1 hard rule).
- Dropping a question the developer didn't answer, or accepting a wrong or incomplete document, instead of asking again until they answer or say they can't find it.
- Filling any undeclared point — a detail, default, or inference — with an assumption instead of stopping to ask, or stating the assumption as a caveat instead of getting explicit confirmation.
