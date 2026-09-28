---
name: half-clone
description: Use when the current conversation has grown long and you want a fresh session to continue mid-dialogue instead of from a cold summary — extracts and cleans the most recent half of the conversation into HALF-CLONE.md. Not for end-of-session summaries (see handoff).
---

# Half-Clone

## Overview

`/half-clone` trims a long conversation down to its most recent half so a new session can pick up the actual dialogue — not just the outcome. Unlike `handoff` (a curated Goal/Done/Worked/Didn't/Next summary), half-clone preserves the flow of recent exchanges, cleaned of bulky tool output, so continuation feels like resuming mid-conversation rather than starting from a report.

## When to Use

- The conversation is long enough that continuing risks losing recent nuance to compaction, and a full summary (`handoff`) would lose too much of the actual back-and-forth.
- Not for: end-of-session handoff to a differently-scoped follow-up task — use `handoff` for that.

## How to Build HALF-CLONE.md

1. **Count turns.** A turn = one user message plus the assistant's response to it (including any tool use in between). Count total turns in the visible conversation.
2. **Take the most recent half.** Identify the turn index at the midpoint; keep everything from there to the end. If the count is odd, round toward keeping *more* recent context.
3. **Clean, don't gut.** For each kept turn:
   - Keep user messages and assistant prose verbatim.
   - Replace large tool-output blocks (full file dumps, skill-file contents, long search/grep results, subagent transcripts) with a one-line reference to what happened and its outcome (e.g. "[Read SKILL.md, ~200 lines, confirmed no existing hard rule]") — not a summary of the dialogue itself, just the bulky payload.
   - **Hard rule:** if a tool-output block contains a decision, fact, or data that later turns depend on, keep that specific content (or an accurate inline note of it) — never delete something load-bearing just because it's large. When unsure whether it's load-bearing, keep it.
4. **Preserve order and continuity.** Output reads top-to-bottom as a trimmed transcript, not a reordered digest. Don't merge or paraphrase separate exchanges into one.
5. **Write/overwrite `HALF-CLONE.md`** at the repo root with the cleaned turns, prefixed by one line noting how many total turns existed and how many were kept.

## After Writing

Tell the developer the file's path and that a new session can be pointed at `HALF-CLONE.md` to continue the conversation from where it left off.

## Common Mistakes

- Copying tool-output blocks verbatim — defeats the purpose; the file ends up nearly as large as the original context.
- Deleting a tool-output block that contained a decision or fact later turns rely on.
- Cutting mid-exchange instead of at a clean turn boundary.
- Miscounting turns by treating each tool call as its own turn instead of grouping by user message.
- Reordering or paraphrasing dialogue into a summary — that's what `handoff` is for.
