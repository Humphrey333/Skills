# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

`embed_debug` is a Claude Code skill (Markdown only — nothing to build or test). It finds the places in embedded Linux code and configuration that cause a symptom the developer reported, explains each one in short plain words, talks through solutions in words, and writes a report. It never writes code or applies a fix. The git repo root is the parent `Skills/` directory. `../CLAUDE.md` holds the conventions every skill follows (frontmatter, section layout, Step 0 block, hard rules, install-by-copy); read it before editing here.

## Files

- `SKILL.md` — Hard Rules (+ rationalization table, red flags) → Step 0 (shared knowledge) → Stage 1 understand + info gate → Stage 2 point by point → Stage 3 solutions in words → Stage 4 report → Common Mistakes.
- `references/techniques.md` — the checks behind a point's **How to check** field (elimination checklist, `git bisect`, standalone program under ASan/UBSan/Valgrind, `creduce`). These are run by the developer; Claude explains them and writes no code or scripts.
- Design record: `../Plans/Plan_embed-debug-plain-explain_2026-10-13.md` (git-ignored).

## Rules specific to this skill (developer decisions, 2026-10-13)

- **No code, no fix.** No patch, diff, snippet, debug print, test script or invented value; no source edits. Quoting at most 2 *existing* wrong lines is allowed. The report is the only file the skill writes.
- **One point per message**, in the fixed Point template (Where / What goes wrong / Why this gives your symptom / How sure / How to check), then wait for the developer. Solutions use the Solution template (Change / Why it fixes it / Watch out for / How to verify). A template binds the plain-language shape better than prose rules — keep fields, don't loosen them.
- **Reported symptom only.** Unrelated suspicious code goes on the *also noticed* list, offered only after every reported point has an outcome.
- **Report**: `Debug_<bug-slug>_<YYYY-MM-DD>.md` in the invocation directory (not `Plans/`), written only after a recap and an explicit yes.
- Ask-never-assume and the no-fetch rule are hard rules here too; Stage 2's documentation stop marks the point *open* rather than guessing.
- The good/bad example in Stage 2 must not match the test scenario used to verify the skill, or the test only measures copying.
- **This file's Step 0 is the reference copy.** Sibling skills verify their Step 0 by diffing against `embed_debug/SKILL.md`. Change Step 0 in every `embed_*` skill in the same edit.
- Keep `Common Mistakes` and the rationalization table in sync with the Hard Rules.

## Activating

`cp -r embed_debug ~/.claude/skills/` (copy, not symlink), then restart the session. Verify with `diff -r embed_debug ~/.claude/skills/embed_debug`.
