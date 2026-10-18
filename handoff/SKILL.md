---
name: handoff
description: "Use when ending a work session and you want to capture context for a fresh session to continue from — creates/overwrites HANDOFF.md summarizing the goal, what's been done, what worked, what didn't, and next steps. Not for trimming a long conversation down to its recent half (see half-clone)."
---

# Handoff

## Overview

`/handoff` writes a concise, honest summary of the session to `HANDOFF.md` so a fresh session with no memory of this conversation can resume the work correctly — used instead of relying on the harness's own context compaction. Manual trigger only.

## When to Use

- The developer explicitly types `/handoff`.
- Not for: preserving the actual recent dialogue for a new session to continue mid-conversation — use `half-clone` for that.

## Hard Rule — Ask, Don't Invent

If you're unsure what actually happened, what genuinely worked or failed, or what the real next step is, stop and ask the developer rather than writing a plausible-sounding but fabricated account. A handoff doc with invented history is worse than no handoff doc — it sends the next session confidently in the wrong direction.

## What to Write

Overwrite `HANDOFF.md` at the repo root (create it if absent) with exactly these five sections:

### Goal
What the session (or the broader task, if this is one of several sessions) is trying to accomplish — in the developer's own terms where possible.

### Done So Far
Concrete work actually completed: files created/edited, commands run, decisions made. If this is a git repo, cross-check against `git status`/`git diff` so nothing completed is missed and nothing uncommitted or reverted is described as done.

### What Worked
Approaches, designs, or decisions that held up and are worth repeating without re-deriving them.

### What Didn't Work
Dead ends, rejected approaches, reverted changes — and *why* they were rejected, so the next session doesn't retry them blind.

### Next Steps
Concrete, ordered, actionable steps — not "continue working on X." Each step should be specific enough that a new session could start executing it immediately.

Pass the prose of the five sections through `embed_writing` before writing the file. Commands, paths and git output stay unchanged.

## After Writing

Tell the developer the file's path and that a new session can be pointed at `HANDOFF.md` (e.g. "read HANDOFF.md and continue") to resume.

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question, or remove or change a fact, reason, hedge or warning.
- Vague/generic sections that could describe any project.
- Omitting failed approaches (survivorship bias) — the next session needs to know what *not* to retry.
- Next steps phrased as goals ("finish the feature") instead of concrete actions.
- Describing uncommitted or reverted work as "done."
- Filling a gap with a plausible guess instead of asking the developer (Hard Rule).
