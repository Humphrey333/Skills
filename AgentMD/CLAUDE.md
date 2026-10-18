# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Claude Code specifics

- Skills load through the Skill tool. Invoke the matching `embed_*` skill before acting, including before clarifying questions.
- Shared knowledge lives in `~/.agents/Knowledge/`. `embed_planning-embedded-topics` reads `INDEX.md` first (its Step 0); `embed_summary` writes it.
- `embed_summary`, `embed_document`, `handoff` and `half-clone` are manual-only. Propose them, never self-trigger.
