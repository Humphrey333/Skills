# Skills

A library of Claude Code skills for embedded Linux engineering. The skills plan a new bring-up, scaffold the project, write the code from the plan, find bugs from a description, write the documents, and keep knowledge between sessions. Home: https://github.com/Humphrey333/Skills

## Table of Contents

- [About the Project](#about-the-project)
- [Project Status](#project-status)
- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
  - [Getting the Source](#getting-the-source)
  - [Installation](#installation)
  - [Usage](#usage)
- [Shared Knowledge Layer](#shared-knowledge-layer)
- [Release Process](#release-process)
- [How to Get Help](#how-to-get-help)
- [Further Reading](#further-reading)
- [Authors](#authors)
- [License](#license)

## About the Project

These skills are prompt and workflow documents. There is nothing to build or test. Each is a `SKILL.md` that tells Claude Code how to work through one kind of embedded-engineering task.

The `embed_*` skills run in three steps. Each step needs your approval before the next one starts.

1. Plan, debug, document or learn: `embed_planning-embedded-topics` for a new topic, `embed_debug` for a bug (it ends in a plan for the fix), `embed_document` for `README.md` and `BUILD.md`, `embed_learning` for a learning path, book companion and exams. After a plan is agreed, `embed_create_coding_template` can create the project skeleton.
2. Write the code from the approved plan, one task per approval: `embed_executing_plans`, which uses `embed_programming`.
3. Capture what was learned with `embed_summary`, then document what was done with `embed_document`.

`embed_writing` is called by every skill whose output a person reads. It removes the signs of AI writing, cuts padding and deletes any sentence no source supports, and it never changes a command, number or feature status.

`handoff` and `half-clone` sit outside the chain and carry a session over to a new one. Four skills never self-trigger: `/embed_summary`, `/embed_document`, `/handoff`, `/half-clone`.

**[Back to top](#table-of-contents)**

## Project Status

| Skill | Status |
|---|---|
| `embed_planning-embedded-topics` | working |
| `embed_executing_plans` | working |
| `embed_debug` | working |
| `embed_document` | TODO: verify |
| `embed_create_coding_template` | TODO: verify |
| `embed_programming` | TODO: verify |
| `embed_summary` | TODO: verify |
| `embed_learning` | TODO: verify |
| `embed_writing` | TODO: verify (tested on 3 sample drafts only) |
| `handoff` | TODO: verify |
| `half-clone` | TODO: verify |
| `AgentMD/install.sh` | TODO: verify (`bash AgentMD/tests/test_install.sh` passes) |

**[Back to top](#table-of-contents)**

## Getting Started

### Dependencies

- Claude Code, with a `~/.claude/skills/` directory.
- bash on Linux, to run `AgentMD/install.sh`.

### Getting the Source

```bash
git clone https://github.com/Humphrey333/Skills.git
cd Skills
```

### Installation

One script installs every skill plus the shared rules (`AGENTS.md`, `CLAUDE.md`) for Claude Code, Codex, Gemini CLI and Antigravity. It copies by default; `--link` symlinks to the clone.

```bash
bash AgentMD/install.sh                    # all agents
bash AgentMD/install.sh --agents claude    # only some
```

Run it from a terminal. When a target file differs, the script asks whether to overwrite it; with no terminal it skips that file. An overwritten file is moved to `~/.agentmd-backup/<date-time>/`. Restart the agent session afterwards. Paths, the workflow table and the details are in [`AgentMD/README.md`](AgentMD/README.md). A single skill can still be copied by hand: `cp -r <skill-name> ~/.claude/skills/`.

### Usage

| Skill | Use it when | Trigger | Not for |
|---|---|---|---|
| `embed_planning-embedded-topics` | Starting a new bring-up, subsystem, board support or feature | auto | an existing bug → `embed_debug` |
| `embed_create_coding_template` | A plan is agreed and you want the CMake skeleton on disk, or to refine `.clang-format`/`.clang-tidy` | auto | planning → `embed_planning-embedded-topics`; kernel modules, Yocto recipes, vendor patch projects |
| `embed_debug` | A bug, crash, oops, hang or misconfiguration in embedded Linux code; you want to know where and why it breaks, explained point by point in plain words (no code), ending in a report | auto | new bring-up/feature → `embed_planning-embedded-topics`; learning → `embed_learning`; saving knowledge → `embed_summary`; code Claude can run and test directly |
| `embed_executing_plans` | A plan from `embed_planning-embedded-topics` is approved and must be implemented, one task per approval (uses `embed_programming`) | auto | planning → `embed_planning-embedded-topics`; bugs → `embed_debug` |
| `embed_programming` | Writing or changing code: extensible structure for new code, smallest complete change for existing code | auto | planning, debugging, docs → their `embed_*` skill |
| `embed_document` | You want `README.md` / `BUILD.md` to match Plans, code and build files | `/embed_document` | session knowledge → `embed_summary`; skeleton → `embed_create_coding_template` |
| `embed_summary` | End of a session or milestone; capture what was learned | `/embed_summary` | plans → `embed_planning-embedded-topics`; bugs → `embed_debug` |
| `embed_learning` | You want to learn a topic (7-day path + books), study a book you supply, or take/grade an exam | auto | implementing a topic → `embed_planning-embedded-topics`; bugs → `embed_debug` |
| `embed_writing` | A skill is about to show or write text a person reads, or you want a draft to read less like AI | called by the other skills, or on request | code → `embed_programming`; what a document contains → the skill that owns it |
| `handoff` | End of a session; write `HANDOFF.md` for a fresh session | `/handoff` | continuing mid-dialogue → `half-clone` |
| `half-clone` | A long conversation; write `HALF-CLONE.md` of the recent half | `/half-clone` | end-of-session summary → `handoff` |

**[Back to top](#table-of-contents)**

## Shared Knowledge Layer

`~/.claude/Knowledge/` is the cross-project memory that ties the chain together. `embed_summary` writes one `<topic-slug>.md` per topic plus a one-line entry in `INDEX.md`. Every other `embed_*` skill reads `INDEX.md` first (Step 0) and opens the matching topic files. If a knowledge entry conflicts with what you say now, your current statement wins and the conflict is flagged for `/embed_summary`.

**[Back to top](#table-of-contents)**

## Release Process

TODO: release cycle and how to find the latest release (no tags or release branches exist yet).

### Versioning

TODO: versioning scheme.

## How to Get Help

TODO: contact or issue tracker.

## Further Reading

- [`CLAUDE.md`](CLAUDE.md) — conventions for writing or editing a skill
- [`AgentMD/README.md`](AgentMD/README.md) — rules for all agents, the installer and where files go
- [`AgentMD/AGENTS.md`](AgentMD/AGENTS.md) — the rules and the workflow table
- Each skill's `SKILL.md`, e.g. [`embed_debug/SKILL.md`](embed_debug/SKILL.md)
- [`embed_document/references/readme-structure.md`](embed_document/references/readme-structure.md)

## Authors

[Humphrey333](https://github.com/Humphrey333)

## License

MIT — see [LICENSE](LICENSE).

**[Back to top](#table-of-contents)**
