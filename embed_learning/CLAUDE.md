# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

`embed_learning` is a Claude Code skill (Markdown only — nothing to build or test) that makes Claude act as a professor who teaches the developer a topic. It has three functions: F1 a 7-day learning path with books, F2 a book companion, F3 HTML exams plus grading. The git repo root is the parent `Skills/` directory; `../CLAUDE.md` holds the conventions every skill follows. Read it before editing here.

## Files

- `SKILL.md` — Step 0 (shared knowledge, verbatim from `embed_debug`) → Step 1 gate (function, slug, resume from `Progress.md`, level, online permission) → F1 / F2 / F3 → Common Mistakes.
- `references/exam-format.md` — exam HTML page rules, export block, key file, grading output, `Progress.md` layout. Changing a filename or the export format means changing it here **and** in `SKILL.md` F3.
- `Requirements.md` — the developer's source requirements (git-ignored via `Requi*`). Don't edit. Design record: `../Plans/Plan_embed-learning-skill_2026-10-11.md`.

## Rules specific to this skill

- **Scoped exception to the repo's no-fetch rule:** web search or link fetch is allowed only after a per-request yes, given to an exact query and purpose. Downloading books, PDFs or datasheets stays forbidden. Don't widen this exception, and don't copy it into other skills.
- Book flow (developer, 2026-10-11): first ask for the local Markdown ebook folder (recorded as `ebooks:` on the topic's `INDEX.md` line), then name candidates from expertise, then search online through the per-request gate, and recommend only books not already in the local folder, in any format (PDF, HTML, docs). The search confirms books and their free sources; it never replaces expertise, and nothing is downloaded.
- Books: at most **5 per level** — the developer overrode the "at most 3" in `Requirements.md` on 2026-10-11 (design record `../Plans/Plan_embed-learning-book-selection_2026-10-11.md`). Free books get a `free` tag and rank first when about as good; days cite the best chapters from any listed books, and lessons combine and summarise across the supplied books, with each point cited to its own source. Official docs may stand in when no good book exists; one source may appear at two levels (counts once); only the book's name is needed, not the edition.
- Supplied books: ask for Markdown, not PDF. The developer converts the books (decision of 2026-10-11, after the UML books were checked; see `~/Documents/Markdown_Embedded_Ebook/UML_Design_Ebook/Verification_2026-10-11.md`). Before using a Markdown file, check its quality. Cite printed pages, not `.md` lines; get diagrams from the PDF page that a `[FIG p.N]` marker points to.
- The learner profile is hardcoded in `SKILL.md` on purpose; the developer accepted that it becomes public.
- Auto-triggers (unlike `embed_summary` / `embed_document`), so the description's `Not for:` routing to `embed_planning-embedded-topics`, `embed_debug` and `embed_summary` must stay.
- Day gate: a path day is passed only at 100% on its exam. Retakes are unlimited and always use new questions. Never soften this; it came from the developer.
- The exam page carries no answers. Answers and source locations live only in the `_key.md`.
- Output goes to the topic folder the developer confirmed (registered in `~/.claude/Learning/INDEX.md`). `Path_*.md`, `Book_*.md` and `Progress.md` are written only after a yes; an exam request (or a failed day needing a retake) is itself the go-ahead for exam files.
- Keep Step 0 identical to the sibling skills. To verify, compare from `## Step 0` to the next `## ` heading against `../embed_debug/SKILL.md`.

## Activating

`cp -r embed_learning ~/.claude/skills/` (copy, not symlink), then restart the session. Verify with `diff -r embed_learning ~/.claude/skills/embed_learning`.
