# AGENTS.md

Rules for every coding agent working with this developer on embedded Linux. Short on purpose: follow them literally.

## Rules

1. **Ask, never assume.** If a fact was not stated or supplied (requirement, register, pin, timing, path, scope), ask and wait. A stated assumption is still an assumption. An inference from the code is a suggested answer inside a question.
2. **Read online, never download.** Prefer reading online: search for and read documents without asking, and cite the URL of every fact you take from one. Never download a file (datasheet, TRM, errata, app note, book, archive); downloads are done by the developer by hand. Only a document that can't be read online goes into `Docs/REQUIRED_DOCS.md` in the project folder, one row per document: Document, Revision, Why needed, Search terms, Status (`needed`, then `supplied: Docs/<file>` or `not found (developer)`); then wait for the developer to supply it in `Docs/`.
3. **Think before coding.** Several readings of the request: list them, do not pick silently. A simpler way exists: say so. Unclear: stop and name what is unclear.
4. **New code: build for extension and management.** Choose the structure that is easy to extend and manage, and accept the extra effort. Put no speculative features in it.
5. **Changing code: smallest complete change.** Reuse what exists, match its style, touch only what the task names. Every changed line traces to the request. Mention unrelated dead code, do not delete it. Remove only what your change made unused.
6. **Goal-driven.** Turn the task into a check you can run, then loop until it passes. "Fix the bug" means reproduce it, then make the check pass. Never claim done without running the check and reading the output.
7. **Review in Gitea.** New projects live in the local Gitea (`http://localhost:3000`) with `main` for releases and `dev` for work. Each feature or fix goes on its own branch from `dev`, one commit per plan todo, with no diffs in the CLI and no yes between todos; then `embed_programming_discussion` pushes it and opens a pull request into `dev`. The developer comments, requests changes or merges in Gitea; you fix what the review asks, push, and reply in one short line. In Gitea you are always the user `Agent`: every `tea` command takes `--login Agent`, pushes go through a repo-local credential helper pinned to that login, and commits carry the repo-local identity `Agent`. Never use, type or store the developer's token. Never merge and never touch `main`. Setup: `AgentMD/README.md`, "Gitea setup (once)". The developer's explicit yes is needed only for: the plan; a bug point or a chosen solution; moving to the next workflow step; a document change from `embed_document`. Silence is not a yes.
8. **Be short.** Answer in plain words a busy person gets in one read. End with what you skipped or did not check. Text a person will read (reports, plans, docs, lessons) goes through `embed_writing` before you show it.

## Workflow

| Step | Task | Skill |
|---|---|---|
| 1 | Plan a new topic (bring-up, subsystem, board, feature) | `embed_planning-embedded-topics` |
| 1 | Find where and why a bug breaks, then plan its fix | `embed_debug` → `embed_planning-embedded-topics` |
| 1 | Write or update README.md / BUILD.md | `embed_document` |
| 1 | Teach a topic, build a learning path, exam | `embed_learning` |
| 2 | Write code from the approved plan on a branch from `dev` | `embed_executing_plans` (uses `embed_programming`) |
| 2 | Create the Gitea repo, push, open the pull request, answer the review, confirm the merge | `embed_programming_discussion` |
| 3 | Capture what the session learned | `embed_summary` |
| 3 | Document what was just done | `embed_document` |
| any | Make text a person reads sound human, facts unchanged (called by the skills above, or on request) | `embed_writing` |

- Bug loop: `embed_debug` report → `embed_planning-embedded-topics` (one todo per agreed solution) → `embed_executing_plans` → the developer tests on the board → if nothing worked, back to `embed_debug` with the tried list. `embed_summary` is optional at the end.
- Step 1 ends with a saved plan or report. Step 2 starts only from an approved plan. Step 3 starts only after the developer merged the pull request.
- `embed_summary` and `embed_document` are manual: propose them, let the developer run them.
- Where a skill below conflicts with a skill from a plugin (for example brainstorming, writing-plans, systematic-debugging), the `embed_*` skill wins.
- A new skill whose output a person reads must load `embed_writing`. Ask the developer when adding one.
- An agent without a skill tool: open `skills/<name>/SKILL.md` and follow it as plain instructions.

---

Rules 3, 5 and 6 are adapted from the Karpathy-inspired guidelines (andrej-karpathy-skills, MIT).
