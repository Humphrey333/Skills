# AGENTS.md

Rules for every coding agent working with this developer on embedded Linux. Short on purpose: follow them literally.

## Rules

1. **Ask, never assume.** If a fact was not stated or supplied (requirement, register, pin, timing, path, scope), ask and wait. A stated assumption is still an assumption. An inference from the code is a suggested answer inside a question.
2. **Never fetch or download platform documentation** (datasheet, TRM, errata, app note). Name the exact document, or give search segments, and wait for the developer to supply it.
3. **Think before coding.** Several readings of the request: list them, do not pick silently. A simpler way exists: say so. Unclear: stop and name what is unclear.
4. **New code: build for extension and management.** Choose the structure that is easy to extend and manage, and accept the extra effort. Put no speculative features in it.
5. **Changing code: smallest complete change.** Reuse what exists, match its style, touch only what the task names. Every changed line traces to the request. Mention unrelated dead code, do not delete it. Remove only what your change made unused.
6. **Goal-driven.** Turn the task into a check you can run, then loop until it passes. "Fix the bug" means reproduce it, then make the check pass. Never claim done without running the check and reading the output.
7. **One step at a time.** Each workflow step and each plan task needs the developer's explicit yes before the next. Silence is not a yes.
8. **Be short.** Answer in plain words a busy person gets in one read. End with what you skipped or did not check. Text a person will read (reports, plans, docs, lessons) goes through `embed_writing` before you show it.

## Workflow

| Step | Task | Skill |
|---|---|---|
| 1 | Plan a new topic (bring-up, subsystem, board, feature) | `embed_planning-embedded-topics` |
| 1 | Find where and why a bug breaks, then plan its fix | `embed_debug` → `embed_planning-embedded-topics` |
| 1 | Write or update README.md / BUILD.md | `embed_document` |
| 1 | Teach a topic, build a learning path, exam | `embed_learning` |
| 2 | Write code from the approved plan, one task per approval | `embed_executing_plans` (uses `embed_programming`) |
| 3 | Capture what the session learned | `embed_summary` |
| 3 | Document what was just done | `embed_document` |
| any | Make text a person reads sound human and sourced (called by the skills above, or on request) | `embed_writing` |

- Step 1 ends with a saved plan or report. Step 2 starts only from an approved plan. Step 3 starts only after Step 2 is approved.
- `embed_summary` and `embed_document` are manual: propose them, let the developer run them.
- Where a skill below conflicts with a skill from a plugin (for example brainstorming, writing-plans, systematic-debugging), the `embed_*` skill wins.
- A new skill whose output a person reads must load `embed_writing`. Ask the developer when adding one.
- An agent without a skill tool: open `skills/<name>/SKILL.md` and follow it as plain instructions.

---

Rules 3, 5 and 6 are adapted from the Karpathy-inspired guidelines (andrej-karpathy-skills, MIT).
