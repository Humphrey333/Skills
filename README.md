# Skills

A library of Claude Code skills for embedded Linux engineering — planning a new bring-up, scaffolding the project, debugging from a description, keeping docs true, and carrying knowledge between sessions. Home: https://github.com/Humphrey333/Skills

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

These skills are prompt/workflow documents, not software: there is nothing to build or test. Each is a `SKILL.md` that tells Claude Code how to work through one kind of embedded-engineering task.

The `embed_*` skills form a chain:

plan (`embed_planning-embedded-topics`) → skeleton (`embed_create_coding_template`) → debug (`embed_debug`) → keep docs true (`embed_document`) → capture knowledge (`embed_summary`)

`handoff` and `half-clone` sit outside the chain and carry a session over to a new one. Four skills never self-trigger: `/embed_summary`, `/embed_document`, `/handoff`, `/half-clone`.

**[Back to top](#table-of-contents)**

## Project Status

| Skill | Status |
|---|---|
| `embed_planning-embedded-topics` | working |
| `embed_document` | working |
| `embed_create_coding_template` | TODO: verify |
| `embed_debug` | TODO: verify |
| `embed_summary` | TODO: verify |
| `handoff` | TODO: verify |
| `half-clone` | TODO: verify |

**[Back to top](#table-of-contents)**

## Getting Started

### Dependencies

- Claude Code, with a `~/.claude/skills/` directory.

### Getting the Source

```bash
git clone https://github.com/Humphrey333/Skills.git
cd Skills
```

### Installation

Skills are **copied**, not symlinked. Editing a file in the repo does not change the skill Claude Code is running.

```bash
cp -r <skill-name> ~/.claude/skills/                  # install or update
diff -r <skill-name> ~/.claude/skills/<skill-name>    # verify the installed copy matches
```

Restart the Claude Code session afterwards. `handoff` and `half-clone` are not installed by default; copy them the same way if you want them.

### Usage

| Skill | Use it when | Trigger | Not for |
|---|---|---|---|
| `embed_planning-embedded-topics` | Starting a new bring-up, subsystem, board support or feature | auto | an existing bug → `embed_debug` |
| `embed_create_coding_template` | A plan is agreed and you want the CMake skeleton on disk, or to refine `.clang-format`/`.clang-tidy` | auto | planning → `embed_planning-embedded-topics`; kernel modules, Yocto recipes, vendor patch projects |
| `embed_debug` | A bug, crash, oops, hang or misconfiguration in embedded Linux code | auto | greenfield design; code Claude can run and test directly |
| `embed_document` | You want `README.md` / `BUILD.md` to match Plans, code and build files | `/embed_document` | session knowledge → `embed_summary`; skeleton → `embed_create_coding_template` |
| `embed_summary` | End of a session or milestone; capture what was learned | `/embed_summary` | plans → `embed_planning-embedded-topics`; bugs → `embed_debug` |
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
- Each skill's `SKILL.md`, e.g. [`embed_debug/SKILL.md`](embed_debug/SKILL.md)
- [`embed_document/references/readme-structure.md`](embed_document/references/readme-structure.md)

## Authors

TODO: maintainers with links.

## License

MIT — see [LICENSE](LICENSE).

**[Back to top](#table-of-contents)**
