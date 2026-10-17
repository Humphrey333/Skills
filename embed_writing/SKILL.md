---
name: embed_writing
description: Use when an embed_* skill is about to show or write text that a person will read (explanations, reports, plans, README.md, BUILD.md, learning material, handoff notes), or the developer asks to make a draft read less like AI. Not for: code (use embed_programming), deciding what a document contains (use the skill that owns it), or trimming a transcript (use half-clone).
---

# Embedded Writing

## Overview

Make text that a person reads sound like a person wrote it, without changing a single fact. Core principle: **edit the wording, never the content.** The skill removes the signs of AI writing, cuts padding, and deletes any sentence no source supports. It adds nothing.

The calling skill owns what the document says and its approval gate. This skill only cleans the draft before the developer sees it.

## When to Use

- Another `embed_*` skill (or `handoff`) has a draft and is about to show it or write it to a file.
- The developer pastes a draft and asks to make it read less like AI.
- Not for: code or code comments (use `embed_programming`), choosing what a document must contain (use `embed_document`, `embed_planning-embedded-topics` and the others), or a trimmed transcript (use `half-clone`).

## Step 0 — Load Shared Knowledge (mandatory, do this first)

Before anything else, read `~/.claude/Knowledge/INDEX.md` (one line per topic, maintained by `embed_summary`).

- Open every topic file in `~/.claude/Knowledge/` whose entry matches the current request (part number, subsystem, board, feature) and apply what it records: constraints, prior decisions and trade-offs, key documents, corrections, preferences, open questions.
- Tell the developer in one line which knowledge files you loaded, or that none matched — they can point you to one you missed.
- Knowledge entries are previously confirmed facts, but if one conflicts with what the developer says now, the developer's current statement wins — flag the conflict so it can be corrected with `/embed_summary`.
- If `INDEX.md` doesn't exist or nothing matches, say so and continue.

## Step 1 — Mark what is protected

Before editing, mark these. They pass through unchanged, character for character:

- commands, code blocks, file names, paths, URLs, numbers, units, register and pin values
- quoted text and cited sources
- `TODO:` markers and their wording
- the status of every feature, exactly as the developer gave it
- the calling skill's structure: its headings, its fixed message template, and any question it puts to the developer

Everything else is prose and may be edited. Headings and questions are never added or removed here, only reworded to sentence case.

## Step 2 — Pass 1: content

Read `references/ai-signs.md` first. Then, for each sentence of prose:

1. Find the source of the sentence in the calling skill's evidence. A sentence with no source is **deleted**, or replaced by `TODO: <what is missing>` when the heading needs a fact. Never keep it because it sounds plausible.
2. A sentence that repeats an earlier one is deleted. An intro is not restated under the first heading.
3. A heading with no sourced fact under it stays in place with `TODO: <what is missing>`, and is listed in the return line as "empty: <heading>". The calling skill and the developer decide whether to drop it. Do not fill it, and do not delete it yourself.
4. Greetings, closing recaps and offers ("Hope this helps", "Let me know") are deleted.

This pass can shorten the text a lot. That is correct.

## Step 3 — Pass 2: words and sentences

Using the lists in `references/ai-signs.md`:

- Replace each flagged word with the plain one. A flagged word that is the exact technical term stays.
- Rewrite each flagged shape (negative parallelism, groups of three, trailing "-ing" clauses, question then answer, mirror sentences, vague attribution) as one direct statement of the fact.
- Use no em dashes.
- Subject first, plain verb ("is", "has", "reads", "returns"), one idea per sentence. Short sentences are good. Do not force variety.
- Use the same name for the same thing throughout. Do not swap in synonyms for variety.
- Explain a term the reader may not know in the sentence where it first appears, in a few words. Do not explain terms every embedded developer knows.

## Step 4 — Pass 3: format

- Headings in sentence case, levels in order, no emoji.
- Bold only a term at its definition or a warning. Prefer a sentence or a table to `**Label:** text` bullets.
- A command goes in its own fenced block with the expected result under it when the calling skill supplied one. Do not invent output.
- Plain ASCII quotes in anything copy-pasteable.

## Step 5 — Check and return

Before returning, confirm all of these:

- [ ] Every protected item from Step 1 is unchanged. Compare them, do not assume.
- [ ] No sentence remains without a source.
- [ ] No leftover: chatbot line, placeholder, tool marker.
- [ ] No Tier 1 word from `references/ai-signs.md` remains.
- [ ] No em dash. No negative parallelism. No group of three used as filler.
- [ ] Nothing repeats an earlier sentence.
- [ ] Each term means one thing and has one name.

Return the clean text. Then add one line **for the developer, outside the document**: `embed_writing removed: <the signs found, in a few words>`, plus any empty heading from Step 2. If nothing was found, say "no signs found". The calling skill's own approve-then-write gate still applies.

If a fix would need a fact you do not have, leave `TODO:` and tell the calling skill. Do not ask the developer new questions yourself unless the calling skill has no gate.

## Rationalizations

| Rationalization | Reality |
|---|---|
| "A benefit line makes the About section feel complete" | No source, no sentence. Use `TODO:` or leave the heading empty and say so. |
| "The section needs a closing sentence" | A paragraph may just stop. Delete the recap. |
| "This word is only Tier 2, so it can stay" | Replace it unless it is the exact technical term. |
| "The sentence is true, it just needs a source later" | Unsourced now means deleted now. |
| "Reading smoothly matters more than keeping the exact status wording" | Feature status and numbers pass through unchanged. |
| "I'll fix the facts while I'm here" | This skill edits wording only. Report the problem to the calling skill. |
| "This heading is empty, so I'll remove it" | Headings belong to the calling skill. Keep it with `TODO:` and report it. |
| "That closing question is just padding" | A question the calling skill's template requires is structure. Keep it. |
| "A little variety in word choice reads more human" | One name per thing. Synonyms confuse a reader following steps. |

## Common Mistakes

- Skipping Step 0 and re-asking what `~/.claude/Knowledge/` already records.
- Changing a command, path, number, quote, `TODO:` marker or feature status while editing wording.
- Keeping an unsourced benefit, audience or "easy to use" line because it reads well.
- Filling an empty heading instead of marking it `TODO:` and reporting it, or deleting the heading.
- Removing a question or a template part that the calling skill requires.
- Leaving a restated intro, a recap paragraph, a greeting or a closing offer.
- Swapping one cliche for another instead of stating the fact.
- Using em dashes, Title Case headings, bold-label bullets or emoji.
- Replacing the exact technical term with a plainer word that changes the meaning.
- Putting the "removed:" line inside the document instead of telling the developer.
- Writing a file itself or skipping the calling skill's approval gate.
- Adding facts, examples or expected output that the calling skill did not supply.

---

Derived from `humanize-writing` by Luis Guzman (MIT License) and the Wikipedia page "Signs of AI writing". Rewritten for the `embed_*` chain: technical text only, one fixed plain voice, no LinkedIn rules, and a sourcing rule that deletes unsupported sentences.
