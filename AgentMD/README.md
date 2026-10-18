# AgentMD

The rules every agent follows (`AGENTS.md`, `CLAUDE.md`) and the installer that puts them, together with all skills in this repo, on any Linux machine.

## Table of Contents

- [Workflow and skills](#workflow-and-skills)
- [Install](#install)
- [Where files go](#where-files-go)
- [Changing a skill later](#changing-a-skill-later)
- [Reference clones](#reference-clones)

## Workflow and skills

Each step needs the developer's explicit approval before the next. To swap a skill, change its name here, in `AGENTS.md`, and in the routing lines of its siblings.

| Step | Task | Skill |
|---|---|---|
| 1 | Plan a new topic (bring-up, subsystem, board, feature) | `embed_planning-embedded-topics` |
| 1 | Find where and why a bug breaks, then plan its fix (if the board test fails, back to `embed_debug` with the tried list) | `embed_debug` → `embed_planning-embedded-topics` |
| 1 | Write or update README.md / BUILD.md | `embed_document` |
| 1 | Teach a topic, learning path, exam | `embed_learning` |
| 2 | Write code from the approved plan, each change shown for a yes before it is written | `embed_executing_plans` (uses `embed_programming`) |
| 3 | Capture what the session learned | `embed_summary` |
| 3 | Document what was just done | `embed_document` |
| any | Make text a person reads sound human, facts unchanged (called by the skills above, or on request) | `embed_writing` |

Also installed: `embed_create_coding_template` (project skeleton), `handoff`, `half-clone` (session continuity).

`embed_executing_plans` is forked from superpowers `executing-plans`, and `embed_programming` from ponytail. `embed_writing` is forked from humanize-writing plus the Wikipedia list of AI-writing signs. The attribution is at the end of each `SKILL.md`. `embed_writing` is loaded by every skill whose output a person reads (see its `SKILL.md`).

## Install

```bash
git clone <your Skills repo URL> Skills
cd Skills/AgentMD
bash install.sh                     # all agents, copy mode
bash install.sh --link              # symlink to this clone instead of copying
bash install.sh --agents claude,codex
```

- Agents: `claude`, `codex`, `gemini`, `antigravity` (default: all).
- If a target already exists and differs, the script lists every such item first, then asks once: overwrite all or skip all. With no terminal it skips all. An overwritten file or skill is replaced with no backup, so copy anything you want to keep first.
- Developer-only files (`Requi*`, `Plans*`) are never copied into the installed skills.
- Restart your agent sessions afterwards.

## Where files go

| Agent | Rules | Skills |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` + `~/.claude/AGENTS.md` | `~/.claude/skills/` |
| Codex | `~/.codex/AGENTS.md` | `~/.agents/skills/` |
| Gemini CLI | `~/.gemini/GEMINI.md` | `~/.agents/skills/` |
| Antigravity | `~/.gemini/GEMINI.md` | `~/.gemini/config/skills/` |

The installer also creates `~/.agents/Knowledge/INDEX.md` and `~/.agents/Learning/INDEX.md` once, for every agent, and never overwrites them. Gemini CLI and Antigravity share one `GEMINI.md`. The paths come from each agent's documentation and are one table at the top of `install.sh`. If an agent moves them, edit that table.

## Changing a skill later

Edit the skill in this repo, run `bash install.sh` again (in `--link` mode nothing needs re-running). The skill rules for editing are in `../CLAUDE.md`.

Test the installer (uses a temporary HOME, never your real one): `bash tests/test_install.sh`.

## Reference clones

`andrej-karpathy-skills/`, `ponytail/`, `superpowers/` and `humanize-writing-skill/` in this folder are upstream clones kept as reading material. They are git-ignored and never installed.
