---
name: embed_summary
description: Use when the developer invokes /embed_summary to capture what was learned in the current embedded-engineering session (constraints, pros/cons and trade-offs, decisions, key documents, corrections, preferences, open questions) into a per-topic knowledge file that future conversations can refer to.
---

# Embedded Session Summary

## Overview

"Review the tape" after a working session: pull out the durable knowledge — insights, constraints that drove the design, pros/cons that were weighed, corrections to Claude's default approach, new preferences — and store it where the next conversation will find it. Output goes to the shared knowledge folder `~/.claude/Knowledge/<topic-slug>.md`, with a one-line entry in `~/.claude/Knowledge/INDEX.md`. Every `embed_*` skill reads `INDEX.md` as its first step, so the next session picks it up regardless of which project it runs in.

Core question: **"What did we learn in this session that's worth knowing next time?"**

## When to Use

- The developer invokes `/embed_summary` — at the end of a session, after a milestone, or before context gets long/compacted.
- Manual only: do not run this on your own initiative.
- Not for: writing a plan (use `embed_planning-embedded-topics`), locating a bug (use `embed_debug`), or recording details that only matter to the current conversation.

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Read `~/.claude/Knowledge/INDEX.md` and every topic file it lists that relates to this session. You need them to pick the right topic slug (Step 1) and to dedupe (Step 3). If `INDEX.md` doesn't exist yet, say so — it will be created in Step 5.

## Step 1 — Identify the Topic

- Suggest a topic slug — an existing one from `INDEX.md` if the session continues that topic, otherwise a new one (from the matching `Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md` if one exists) — and ask the developer to confirm it. Same hard rule as the planning skill: **ask, never assume.**
- Slugs are global across projects, so make them specific (part number, board, subsystem — e.g. `imx586-mipi-csi-bringup`, not `camera`).
- If the session covered several unrelated topics, ask whether to split them into separate knowledge files.

## Step 2 — Harvest the Session

Go back through the whole conversation and collect items under these categories:

| Category | What to capture |
|---|---|
| **Constraints** | Hardware, timing, memory, power, real-time/context rules (e.g. "no dynamic allocation in ISR context"), toolchain/kernel version limits — and *why* each applies. |
| **Options & trade-offs** | Each approach considered, with its pros, cons, and trade-offs. |
| **Decisions** | What was chosen, why, and which alternatives were rejected (and why). |
| **Key documents** | Datasheet / TRM / errata / app note by exact name + revision + section/page; important file paths, functions, commits, register names. |
| **Corrections** | Places where the developer corrected Claude's default approach — especially anything corrected more than once. |
| **Preferences** | How the developer wants work done (style, workflow, tools, output format). |
| **Open questions / next steps** | Unresolved points, pending experiments, what to do next session. |

Rules:
- Record only what was **explicitly stated or confirmed** in the session. An inference or unconfirmed assumption goes under *Open questions*, never as a fact.
- Distill, don't transcribe: one short, self-contained line per item that makes sense without the original conversation.
- Keep concrete values exact (register addresses, pins, timings, versions) — copy them as given, never round or paraphrase.

## Step 3 — Dedupe Against Existing Knowledge

- Compare the harvest with the existing `~/.claude/Knowledge/<topic-slug>.md`.
- Skip items already recorded; if an item refines an older one, propose updating the old entry instead of adding a duplicate.
- If a new item **contradicts** an existing entry, flag it explicitly and ask which one is correct.

## Step 4 — Propose, Then Wait

Pass the wording of the proposed entries through `embed_writing` before showing them. Facts, part numbers and document names stay unchanged.

Show the developer the proposed entries grouped by category, marked as **new / update / contradiction**. Do not write anything until they explicitly confirm or edit the list.

Also point out items that may belong somewhere else as well — suggestions only, never auto-written:
- A preference valid for all projects → global `CLAUDE.md`
- A repeated correction to a workflow → the relevant skill (`embed_debug`, `embed_planning-embedded-topics`, …)
- An architecture-level decision → an ADR or the project `README.md`

## Step 5 — Write

1. Create or update `~/.claude/Knowledge/<topic-slug>.md` using the template below; add a new dated `## Session YYYY-MM-DD` block and apply any confirmed updates to older entries.
2. Add or refresh the topic's line in `~/.claude/Knowledge/INDEX.md` (create the file with a `# Embedded Knowledge Index` heading if missing). Keep it to one line per topic, with keywords other skills can match on:
   `- [<Topic title>](<topic-slug>.md) — <part numbers / board / subsystem>; <one-line hook>`
3. Report the files written and the number of items added/updated.

### File Template

```markdown
# <Topic title>

Project: <absolute path of the project this topic belongs to>
Related plan: <project>/Plans/Plan_<topic-slug>_<YYYY-MM-DD>.md (if any)

## Session YYYY-MM-DD

### Constraints
- <constraint> — why: <reason>

### Options & Trade-offs
- <option>: pros — …; cons — …; trade-off — …

### Decisions
- <decision> — why: <reason>; rejected: <alternative> (<why>)

### Key Documents
- <Document name, rev, section/page> — <what it's used for>

### Corrections
- <what Claude did by default> → <what to do instead>

### Preferences
- <preference>

### Open Questions / Next Steps
- <question or task>
```

Omit a category heading if it has no items for that session.

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question.
- Writing to files before the developer confirms the proposed list.
- Recording an assumption or inference as a confirmed fact.
- Duplicating entries that already exist instead of updating them; silently overwriting a contradicting entry.
- Dumping the conversation transcript instead of distilled, self-contained lines.
- Vague document references ("the datasheet") without exact name, revision, and section/page.
- Forgetting the `INDEX.md` entry (or writing vague keywords in it), so other `embed_*` skills never find the file.
- Writing to a project-local `Knowledge/` folder instead of the shared `~/.claude/Knowledge/`.
- Running the skill without being invoked.
