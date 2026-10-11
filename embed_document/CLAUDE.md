# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

`embed_document` is a Claude Code skill (Markdown only — nothing to build or test) that creates or updates a project's `README.md` and `BUILD.md`. The git repo root is the parent `Skills/` directory; `../CLAUDE.md` holds the conventions every skill follows (frontmatter, section layout, Step 0 block, hard rules, install-by-copy). Read it before editing here.

## Files

- `SKILL.md` — the skill: Step 0 (shared knowledge, verbatim from `embed_debug`) → gate (root = invocation dir, mode = both; install target and unknowns asked) → evidence → README mode → BUILD mode → propose-then-wait → report.
- `references/readme-structure.md` — section-by-section README rules and the CLI-focused + TOC style notes. Changing the section order means changing it here **and** in `SKILL.md` Step 3.
- `Requirements` — developer-supplied source requirements (note: the filename has a trailing space). Don't edit; the design record is `../Plans/Plan_embed-document-readme-build_2026-10-11.md`.
- `README.md` — the Embedded Artistry README template copy used as the structural reference; not documentation of this skill.

## Rules specific to this skill

- Manual only — the `description` must never read as an auto-trigger, and `When to Use` keeps the "Not for" routing to `embed_summary`, `embed_create_coding_template`, `embed_debug`, `handoff`.
- `BUILD.md` is host build only — no cross-build/Yocto section. Project root is the invocation directory and mode defaults to both files; unknowns are asked, never assumed.
- Feature list comes from `Plans/` only, and each planned feature's working/not-working status is asked of the developer — plans never confirm it, code/`git log` are only a suggested answer.
- Scope is `README.md` and `BUILD.md` only; CHANGELOG / ARCHITECTURE.md / `docs/design.md` were deliberately excluded.
- Every statement written into a project doc must trace to a source; unknowns are `TODO:` markers. Nothing is written before the developer approves the diff.
- Keep Step 0 identical to the sibling skills (verify: diff the block against `../embed_debug/SKILL.md`), and keep `Common Mistakes` in sync with the hard rules.

## Activating

`cp -r embed_document ~/.claude/skills/` (copy, not symlink), then restart the session. Verify with `diff -r embed_document ~/.claude/skills/embed_document`.
