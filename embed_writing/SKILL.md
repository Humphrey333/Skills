---
name: embed_writing
description: Use when an embed_* skill is about to show or write text that a person will read (explanations, reports, plans, README.md, BUILD.md, learning material, handoff notes), or the developer asks to make a draft read less like AI. Not for: code (use embed_programming), deciding what a document contains (use the skill that owns it), or trimming a transcript (use half-clone).
---

# Embedded Writing

## Overview

Make text that a person reads sound like a person wrote it, without changing a single fact. Core principle: **reword, never remove.** The skill replaces AI-sounding words and sentence shapes with plain ones that mean the same thing. The output carries every fact, claim, reason, step, hedge, warning and list item of the input, in the same order. It adds nothing and deletes nothing.

The calling skill owns what the document says and its approval gate. This skill only rewords the draft before the developer sees it.

## When to Use

- Another `embed_*` skill (or `handoff`) has a draft and is about to show it or write it to a file.
- The developer pastes a draft and asks to make it read less like AI.
- Not for: code or code comments (use `embed_programming`), choosing what a document must contain (use `embed_document`, `embed_planning-embedded-topics` and the others), or a trimmed transcript (use `half-clone`).

## Step 1 — Mark what is protected

Before editing, mark these. They pass through unchanged, character for character:

- commands, code blocks, file names, paths, URLs, numbers, units, register and pin values
- quoted text and cited sources
- `TODO:` markers and their wording
- the status of every feature, exactly as the developer gave it
- the calling skill's structure: its headings, its fixed message template (labels, field names, separators such as `—` and bold), and any question it puts to the developer

These keep their meaning and may only be reworded, never removed:

- negations and contrasts ("does not release reset", "active low instead of active high")
- hedges and confidence levels ("likely", "possible", "not checked yet")
- warnings, risks and side effects
- cause-and-effect reasoning ("so", "because", "which is why")
- pass and fail criteria of a check, and expected results
- every item of a list

Everything else is wording and may be rewritten.

## Step 2 — Pass 1: leftovers

Read `references/ai-signs.md` first. Then strip only what carries no information:

1. Chatbot lines: greetings, "Hope this helps", "Let me know if…", "Here's a detailed overview…".
2. Tool markers (`oaicite`, `contentReference`, `[cite: 1]`, `utm_source=`).

An offer or a next step that the calling skill requires (for example "Shall I go to the next point?") is structure. Keep it.

Do not delete anything else. A sentence that looks unsourced, repeated or padded stays, reworded if it has AI signs, and goes on the `flagged:` list (Step 5). The calling skill and the developer decide what to cut.

## Step 3 — Pass 2: words and sentences

Using the lists in `references/ai-signs.md`, rewrite each sign so the sentence means the same thing:

- Replace each flagged word with the plain one. A flagged word that is the exact technical term stays.
- Rewrite each flagged shape (negative parallelism, groups of three, trailing "-ing" clauses, question then answer, mirror sentences) as a direct statement that keeps every fact in it. A real contrast, negation or hedge stays as a contrast, negation or hedge.
- Use no em dashes in prose. Text in the calling skill's fixed template keeps its own.
- Subject first, plain verb ("is", "has", "reads", "returns"), one idea per sentence. Splitting a long sentence is fine; dropping part of it is not.
- Use the same name for the same thing throughout. Do not swap in synonyms for variety.
- Explain a term the reader may not know in the sentence where it first appears, in a few words. Do not explain terms every embedded developer knows.

## Step 4 — Pass 3: format

- Headings in sentence case, levels in order, no emoji. The calling skill's fixed headings stay as given.
- In prose, bold only a term at its definition or a warning. Prefer a sentence or a table to `**Label:** text` bullets. The calling skill's template keeps its own bold and labels.
- A command goes in its own fenced block with the expected result under it when the calling skill supplied one. Do not invent output.
- Plain ASCII quotes in anything copy-pasteable.

## Step 5 — Check and return

Before returning, confirm all of these:

- [ ] Every protected item from Step 1 is unchanged. Compare them, do not assume.
- [ ] **Meaning check.** List each fact, claim, reason, step, hedge, warning and list item of the input. Each one is in the output with the same meaning. If one is missing or changed, put it back.
- [ ] Nothing was removed except Step 2 leftovers.
- [ ] No leftover: chatbot line, placeholder, tool marker.
- [ ] No Tier 1 word from `references/ai-signs.md` remains, unless it is the exact technical term.
- [ ] No em dash in prose. No negative parallelism used as filler.
- [ ] Each term means one thing and has one name.

Return the clean text. Then add one line **for the developer, outside the document**:

`embed_writing changed: <signs reworded, in a few words>; stripped: <leftovers, or none>; flagged: <sentence, why>`

Flag a sentence that seems unsourced, repeated or padded, with the reason in a few words. If nothing was found, say "no signs found". The calling skill's own approve-then-write gate still applies.

If a sign can't be fixed without changing the meaning, keep the original wording and flag it. Do not ask the developer new questions yourself unless the calling skill has no gate.

## Rationalizations

| Rationalization | Reality |
|---|---|
| "This sentence is padding, I'll cut it" | Reword it and flag it. The caller and the developer decide what to cut. |
| "This sentence has no source, so it goes" | Keep it and flag it. Reasoning and explanation are content, not padding. |
| "The paragraph repeats itself, I'll drop the recap" | A recap may be the report's required summary. Keep it and flag it. |
| "The hedge sounds weak, I'll state it plainly" | "Likely" and "not checked yet" are facts about certainty. Keep them. |
| "'Does not' is negation filler" | A real negation is often the bug itself. Rewrite only when it says nothing. |
| "Three items is a filler group, I'll keep two" | Every list item stays. Reword the group, not its size. |
| "Reading smoothly matters more than keeping the exact status wording" | Feature status and numbers pass through unchanged. |
| "I'll fix the facts while I'm here" | This skill edits wording only. Report the problem to the calling skill. |
| "That closing question is just padding" | A question the calling skill's template requires is structure. Keep it. |
| "A little variety in word choice reads more human" | One name per thing. Synonyms confuse a reader following steps. |

## Common Mistakes

- Deleting a sentence, clause or list item that carries a fact, a reason, a hedge, a warning or a pass criterion, instead of rewording it and flagging it.
- Turning a real negation, contrast or confidence level into a plain positive statement that means something else.
- Changing a command, path, number, quote, `TODO:` marker or feature status while editing wording.
- Skipping the meaning check in Step 5.
- Removing a question or a template part that the calling skill requires, or rewriting its fixed headings, separators or bold.
- Leaving a greeting, a closing offer or a tool marker that the calling skill does not require.
- Swapping one cliche for another instead of stating the fact.
- Using em dashes in prose, Title Case headings, bold-label bullets or emoji.
- Replacing the exact technical term with a plainer word that changes the meaning.
- Putting the `changed:` line inside the document instead of telling the developer.
- Writing a file itself or skipping the calling skill's approval gate.
- Adding facts, examples or expected output that the calling skill did not supply.

---

Derived from `humanize-writing` by Luis Guzman (MIT License) and the Wikipedia page "Signs of AI writing". Rewritten for the `embed_*` chain: technical text only, one fixed plain voice, no LinkedIn rules, and a meaning-preserving rule: reword, never remove.
