---
name: embed_executing_plans
description: "Use when an embedded-engineering plan (Plans/Plan_<slug>_<date>.md from embed_planning-embedded-topics) has been approved and its todos must now be implemented, or the developer says \"execute the plan\" or \"start coding the plan\". Not for: planning a new topic (use embed_planning-embedded-topics), locating a bug (use embed_debug), writing docs (use embed_document), or a pull request that was reviewed or merged (use embed_programming_discussion)."
---

# Executing Plans

## Overview

Run the approved plan's `## Todo` list on a new branch from `dev`, one commit per todo, without asking between todos and without printing diffs in the CLI. The code follows `embed_programming`. When the last todo is done, load `embed_programming_discussion`: it pushes the branch, opens the pull request into `dev` in the developer's local Gitea, and handles the review and the merge. The plan already did the thinking: follow it exactly, and ask when it is wrong or silent.

**Violating the letter of these rules is violating the spirit of them.**

## When to Use

- A plan exists at `Plans/Plan_<slug>_<date>.md` with a `## Todo` list, the developer approved it, and the project has a Gitea repo (made by `embed_create_coding_template` with `embed_programming_discussion`).
- Not for: a plan that is not approved (go back to `embed_planning-embedded-topics`); a bug with no plan yet (use `embed_debug`); docs only (use `embed_document`); a pull request that was reviewed or merged (use `embed_programming_discussion`).

## Hard Rules

1. **Work on a branch from `dev`.** All work happens on `feature/<plan-slug>` (new feature) or `fix/<plan-slug>` (bug-fix plan, from a `Debug_*.md` report), made from an up-to-date `dev`. Never commit to `dev` or `main`. Pushing, the pull request and the review belong to `embed_programming_discussion`.
2. **Run to the end without asking.** Do not stop between todos for a yes. Print no diffs in the CLI: one status line per todo is the whole report. Gitea is where the developer sees the change.
3. **Stop only for these:** a fact the plan and the developer did not give (ask, and ask again until it is answered or the developer says they can't find it); a todo that is wrong or impossible (ask, never rule on it yourself); a check that still fails after one root-cause fix; a hardware check that only the developer can run.
4. **Follow the plan.** Do not add, skip, reorder or reshape todos.
5. **Ask, never assume.** A register value, pin, timing, path or behavior nobody gave or cited is asked for. A stated assumption is still an assumption.
6. **Read online, never download.** Prefer reading documents online, without asking, and cite the URL. Only a document that can't be read online goes into `Docs/REQUIRED_DOCS.md`; then wait for the developer to download and supply it.
7. **Code follows `embed_programming`**, including its function-header comment on every function written or changed. Load it before the first todo.
8. **Evidence before claims.** A todo is done only when its check ran in this session and you read the output.

| Rationalization | Reality |
|---|---|
| "I'll show this diff in the chat so they can follow" | No diffs in the CLI. Gitea shows them. One status line per todo. |
| "I'll ask before the next todo to be safe" | Todos run without asking. Stop only for the reasons in Hard Rule 3. |
| "It's a tiny fix, I'll commit it on dev" | Every change goes on its own branch and through a pull request. |
| "I'll push and open the PR myself, it's quicker" | Load `embed_programming_discussion`; it holds the Agent account rules. |
| "The plan is wrong here, I'll do the right thing" | Stop and ask. A silent deviation is an unreviewed decision. |
| "It should pass, the change was trivial" | "Should" is not evidence. Run the check and read it. |
| "I'll fill in this value, it is the usual one" | A value nobody supplied or cited is an assumption. Ask, read it online, or list the document. |

Red flags (stop): a diff printed in the chat; a commit on `dev` or `main`; a `tea` command run from this skill; writing "assuming…"; a check you did not run.

## Step 1 — Setup

1. Read the plan and its `## Todo`. Load `embed_programming`.
2. **Gitea.** `git remote -v` must show a remote on `localhost:3000`. If there is none, stop: this flow is for projects made by `embed_create_coding_template`; tell the developer and wait. Load `embed_programming_discussion` and run its Step 1 (Agent check), so commits carry the `Agent` identity from the first todo.
3. **Clean tree.** If the working tree has uncommitted changes, stop and ask the developer what to do with them.
4. **Branch.** `git switch dev && git pull`, then `git switch -c <feature|fix>/<plan-slug>`, or switch to it if it exists (resuming).
5. **Local-only folders.** Add `Docs/` to `.git/info/exclude` if it is not there, so vendor documents are never committed.
6. **Resume.** Todos ticked `- [x]` in the plan are done. `git log dev..HEAD --format=%s` shows the `<plan-slug> todo N:` commits. Start at the first unticked todo. If the plan has `## Review results`, read it first.
7. Tell the developer in one line: the branch and the todo you start at.

## Step 2 — Run the todos

For each todo, in order:

1. Make exactly the change the todo describes, following `embed_programming`. When the check can run on the host, write it first and watch it fail, then make it pass.
2. Run the todo's check and read the output.
3. Commit only the files of this todo: `git commit -m "<plan-slug> todo N: <summary>"`, with a body line for anything a reviewer must know.
4. Tick the todo `- [x]` in the plan file.
5. Print one status line: `todo N/M <name>: done, check <command> → <result>`. No diff.

A hardware or board check that can't run here is not a blocker for the next todo. Record it for the pull request description and hand it to the developer with the expected result.

## Step 3 — Hand over to the discussion

After the last todo:

1. Read the whole branch diff (`git diff dev...HEAD`) once against the plan. Note anything the plan did not ask for and anything a todo left undone.
2. Load `embed_programming_discussion` and run its Step 3 (open the pull request), passing the plan, every check with its real result, the board checks handed to the developer, and the notes from item 1. Its Steps 4 and 5 handle the review rounds and the merge.
3. After it confirms the merge, propose Step 3 of the workflow, and wait. Do not run it yourself:
   - `/embed_summary` captures what was learned;
   - `/embed_document` updates README.md and BUILD.md.

## Board results (bug-fix plans)

When the plan came from a `Debug_*.md` report (it has a `## Board results` section), each todo's board check goes to the developer. Record every report there: solution, tested or not, worked or not, what the developer saw. When every solution is tested:

- One worked: continue with the review.
- None worked: show every point and solution tried, with its result. Propose going back to `embed_debug` with that list (its re-entry case). Do not look for new causes yourself.

## Common Mistakes

- Showing prose to the developer, or writing it to a file, without passing it through `embed_writing` first, or letting that pass change a command, number, heading or required question, or remove or change a fact, reason, hedge or warning.
- Printing diffs in the CLI, or stopping between todos for a yes instead of running to the end.
- Branching from a stale `dev`, committing on `dev` or `main`, mixing two todos in one commit, or committing `Docs/`.
- Running on a project with no Gitea remote instead of stopping, or branching over uncommitted changes without asking.
- Skipping `embed_programming_discussion`'s Agent check before the first commit, or pushing, opening the pull request or reading the review here instead of through that skill.
- Deviating from the plan (adding, skipping, reordering, reshaping a todo) instead of stopping to ask.
- Assuming a missing value, downloading a document, or using an online fact without its URL.
- Claiming a todo done without running its check, or marking a hardware-only check as passed instead of handing it to the developer.
- Forgetting to tick `- [x]` in the plan, so a resumed session redoes finished todos.
- Not recording board results, or hunting for a new cause yourself when no solution worked instead of proposing `embed_debug` re-entry.
- Writing code without loading `embed_programming`, or without the function-header comments.
- Running `/embed_summary` or `/embed_document` yourself instead of proposing them.

---

Derived from `executing-plans` in obra/superpowers (MIT License). Rewritten for the `embed_*` chain: a branch per plan and a Gitea pull request (through `embed_programming_discussion`) instead of per-task approval, no subagents, worktrees or ledger scripts.
