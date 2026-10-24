# AgentMD

The rules every agent follows (`AGENTS.md`, `CLAUDE.md`) and the installer that puts them, together with all skills in this repo, on any Linux machine.

## Table of Contents

- [Workflow and skills](#workflow-and-skills)
- [Install](#install)
- [Gitea setup (once)](#gitea-setup-once)
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
| 2 | Write code from the approved plan on a branch from `dev` | `embed_executing_plans` (uses `embed_programming`) |
| 2 | Create the Gitea repo, push, open the pull request, answer the review, confirm the merge | `embed_programming_discussion` |
| 3 | Capture what the session learned | `embed_summary` |
| 3 | Document what was just done | `embed_document` |
| any | Make text a person reads sound human, facts unchanged (called by the skills above, or on request) | `embed_writing` |

Also installed: `embed_create_coding_template` (project skeleton; `embed_programming_discussion` then creates its Gitea repo with `main` and `dev`), `handoff`, `half-clone` (session continuity).

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
- At the end the installer warns (and changes nothing) if `tea` is missing or there is no `Agent` login. See the next section.

## Gitea setup (once)

Code review runs in a local Gitea at `http://localhost:3000`. The agent works there as its own Gitea user, `Agent`, and never with your token. You own the repos, review and merge.

1. Install `tea`, the Gitea CLI (https://gitea.com/gitea/tea). Tested with `tea` 0.16 and Gitea 28.2.
2. As a Gitea admin, create the user `Agent`: Site Administration → User Accounts → Create User Account. Log in as `Agent` once to set its password.
3. As `Agent`: Settings → Applications → Generate token, with these scopes: repository read/write, user read, issue read/write.
4. Add the token as the `tea` login named `Agent`:

   ```bash
   tea login add --name Agent --url http://localhost:3000 --token <Agent's token>
   tea login list          # the Agent row must show USER Agent
   ```

5. New repos: `Agent` creates the repo and pushes `main` and `dev`, then transfers it to you. Accept the transfer in Gitea and keep `Agent` as a **Write** collaborator (Repo → Settings → Collaborators). For an existing repo of yours, add `Agent` as a Write collaborator the same way.

The agent sets two things per repo, only in that repo's `.git/config`: the commit identity `Agent`, and a credential helper that asks `tea` for the `Agent` token on push. Your global git config is not touched.

When you review: comment on lines, then submit with the green **Review** button (Comment, Approve or Request changes). A review you only started stays a draft that `Agent` can't see.

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
