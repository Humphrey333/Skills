---
name: embed_programming_discussion
description: "Use when code from embed_programming must be discussed with the developer in the local Gitea (http://localhost:3000): a new project from embed_create_coding_template needs its Gitea repo, embed_executing_plans finished a plan's todos and the branch must be pushed and opened as a pull request into dev, or the developer says that pull request was reviewed (comments, request changes) or merged. Not for: writing or changing code (use embed_programming), running a plan's todos (use embed_executing_plans), creating the project skeleton (use embed_create_coding_template), or projects without a Gitea repo."
---

# Programming Discussion

## Overview

The code review is a discussion in the developer's local Gitea at `http://localhost:3000`. You are the Gitea user `Agent`; the developer is the reviewer and the repo owner. You create the repo, push the work branch, open a pull request into `dev`, read the developer's review, fix what it asks, reply in one short line, and confirm the merge. The developer merges and releases (`dev` → `main`). You never merge and never use the developer's token.

**Defaults** (developer's choice, 2026-10-31; don't ask for them): the developer's Gitea user is `Humphrey333` (reviewer, maintainer, final owner of every repo); Agent's commit email is `someAddress@gmail.com`; the remote is always HTTP, `http://localhost:3000/<owner>/<repo>.git`, never SSH.

**Violating the letter of these rules is violating the spirit of them.**

## When to Use

- `embed_create_coding_template` finished Step 6 and loads this skill for a new repo (Step 2 below).
- `embed_executing_plans` finished the last todo of a plan on `feature/<plan-slug>` or `fix/<plan-slug>` and loads this skill to open the pull request (Step 3).
- The developer says the pull request was reviewed (Step 4) or merged (Step 5).
- Not for: writing or changing code (use `embed_programming`), running a plan's todos (use `embed_executing_plans`), creating the skeleton (use `embed_create_coding_template`), or a project that has no Gitea repo (stop and tell the developer).

## Hard Rules

1. **Always the Agent account.** Every `tea` command takes `--login Agent`, and that login must be the Gitea user `Agent`. Pushes go through the repo-local credential helper pinned to `Agent`; commits carry the repo-local identity `Agent`. Never type, ask for or store a token or password.
2. **Never merge, never touch `dev` or `main`.** Push only the work branch. The developer merges in Gitea and does `dev` → `main` releases.
3. **Stop on a failed login, push or transfer.** Ask the developer to fix it; don't work around it with another login, remote or credential.
4. **Every review comment gets an answer.** A requested change is fixed and pushed, then answered with one short line naming the commit. A comment you disagree with, or one that is unclear, is asked about; don't decide it yourself.
5. **Record the discussion** in the plan under `## Review results`, so the next round and the next session see it.
6. **No `embed_writing` pass** (developer's choice, 2026-10-24). Keep the pull request description to the project's template and replies to one short line.

| Rationalization | Reality |
|---|---|
| "The Agent login is missing, I'll use the developer's login for now" | Stop and ask. Everything in Gitea goes through `Agent`. |
| "They approved it, I'll merge to save them a click" | The developer merges. Never merge. |
| "The push failed, I'll try another remote or credential" | Stop and ask. Credentials are the developer's. |
| "Both review lists are empty, so there's nothing to do" | The review may be an unsubmitted `PENDING` draft that `Agent` can't see. Ask the developer to submit it. |
| "The PR is approved, so the line comments don't matter" | A comment asking for a change is fixed and answered, approved or not. |
| "This comment is wrong, I'll skip it" | Ask about it. Don't decide it yourself. |
| "A longer reply explains it better" | One short line: `Changed in <sha7>: <what>`. The commit holds the detail. |

Red flags (stop): any `tea` command without `--login Agent`; a push to `dev` or `main`; `tea pulls merge`; a token in a command line or file; a review comment left without a reply.

## Step 1 — Agent check (every time)

Run in the project folder:

1. `tea login list`: a login named `Agent` on `http://localhost:3000` whose USER is `Agent`. If `tea` is missing, ask the developer to install it (https://gitea.com/gitea/tea). If the login is missing or shows another user, ask the developer to add it themselves (`! tea login add --name Agent --url http://localhost:3000 --token <Agent's token>`), see `AgentMD/README.md` "Gitea setup (once)". Wait.
2. Repo-local commit identity: `git config --local user.name` is `Agent` and `user.email` is `someAddress@gmail.com`. If not, set both with `git config --local`, without asking.
3. The remote is always HTTP (once `origin` exists, `git remote get-url origin` starts with `http://localhost:3000/`; if it is SSH or anything else, stop and ask). The repo-local credential helper is pinned to `Agent`:

   ```bash
   git config --local --replace-all credential.http://localhost:3000.helper ''
   git config --local --add credential.http://localhost:3000.helper '!f() { test "$1" = get && tea login helper get --login Agent; }; f'
   ```

   Check with `git config --local --get-all credential.http://localhost:3000.helper`. The first, empty line drops the global helpers, so a push can never use the developer's token.

## Step 2 — New repo (called by `embed_create_coding_template`)

The project folder has passed the template's Step 6 and has no `.git` yet.

1. If the folder sits inside another git repo, ask before `git init` (it becomes a nested repo). Then `git init -b main`, run Step 1 items 2 and 3, `git add -A`, `git commit -m "<project-name>: initial skeleton"`, and `git branch dev`.
2. `tea repos create --login Agent --name <project-slug> --private` (no `--init`: the history comes from the local repo). If the name exists, stop and ask.
3. `git remote add origin http://localhost:3000/Agent/<project-slug>.git` and `git push -u origin main dev`.
4. **Transfer to the developer:** `tea api --login Agent -X POST 'repos/Agent/<project-slug>/transfer' -f new_owner=Humphrey333`. Ask the developer to accept the transfer in Gitea and to keep `Agent` as a **Write** collaborator (add it back if Gitea dropped it). Wait, then check: `tea api --login Agent 'repos/Humphrey333/<project-slug>'` shows the new owner and `"push": true`.
5. `git remote set-url origin http://localhost:3000/Humphrey333/<project-slug>.git`, `git fetch origin`.
6. Report the repo URL, the pushed branches, and that `docs/pull_request_template.md` is the pull request body. After this, nothing commits to `main`.

## Step 3 — Open the pull request (called by `embed_executing_plans`)

The work branch holds one commit per todo and every check has run.

1. Run Step 1.
2. **Description.** Fill the project's `docs/pull_request_template.md` with the plan (or `Debug_*.md`) the work comes from, each check with its real result, board checks handed to the developer with the expected result, and anything the plan did not ask for or a todo left undone (from `embed_executing_plans`' diff read). Tick a box only with evidence from this session; an unticked box gets one line saying why. Write it to a temporary file outside the repo.
3. `git push -u origin <branch>`, then:

   ```bash
   tea pulls create --login Agent --base dev --head <branch> --title "<plan title>" --description-file <description file>
   ```

4. Give the developer the pull request URL and say: comment on lines, submit the review with the green **Review** button (Comment, Approve or Request changes), merge in Gitea when satisfied, then tell me. Wait.

## Step 4 — Read the review

When the developer says the review is done:

1. Run Step 1, then read it:
   - line comments: `tea pulls review-comments --login Agent <index>` (id, path, line, body);
   - review state: `tea api --login Agent 'repos/<owner>/<repo>/pulls/<index>/reviews'` (`APPROVED`, `REQUEST_CHANGES` or `COMMENT`);
   - conversation comments: `tea api --login Agent 'repos/<owner>/<repo>/issues/<index>/comments'`.

   A review the developer started but did not submit is a `PENDING` draft that only they can see. If they say they reviewed but every list is empty, ask them to submit it (Files changed → green **Review** button) and wait.
2. Record it in the plan under `## Review results` → `### Round N (<date>, head <sha7>)`: the review state and each comment as `path L<n>: <comment>` or `general: <comment>`, wording as given.
3. For each comment that asks for a change: fix it on the same branch following `embed_programming`, run the checks the fix touches, commit (`<plan-slug> review N: <summary>`), push, and reply:

   ```bash
   tea pulls reply --login Agent <index> <comment id> "Changed in <sha7>: <what>" </dev/null
   ```

   Without `</dev/null`, `tea` can wait on input and hang. A comment that only asks a question gets a one-line answer and no commit.
4. Tell the developer the new head is pushed, and wait for the next review.

## Step 5 — After the merge

When the developer says the pull request is merged:

1. Check: `tea api --login Agent 'repos/<owner>/<repo>/pulls/<index>'` shows `"merged": true` and base `dev`. If not, say so and ask.
2. `git switch dev && git pull`, then `git branch -d <branch>`. Leave the remote branch to the developer.
3. Record `Merged into dev (<date>)` under `## Review results`.
4. Hand back to `embed_executing_plans`, which proposes `/embed_summary` and `/embed_document`.

`tea` commands follow its CLI reference (https://gitea.com/gitea/tea/src/branch/main/docs/CLI.md) and were tested with `tea` 0.16 against Gitea 28.2. If one fails because the installed `tea` differs, read `tea <command> -h`, adapt, and tell the developer which command you used.

## Common Mistakes

- Running a `tea` command without `--login Agent`, or with a login whose USER is not `Agent`.
- Pushing without the repo-local credential helper pinned to `Agent`, or committing without the repo-local `Agent` identity.
- Typing, asking for or storing a token or password.
- Asking for the remote type, the developer's username or Agent's email instead of using the defaults.
- Using an SSH or https remote instead of `http://localhost:3000/...`.
- Merging the pull request, pushing to `dev` or `main`, or deleting the remote branch.
- Working around a failed login, push or transfer instead of stopping and asking.
- Creating the repo public or with `--init`, or leaving it under the `Agent` account instead of transferring it to the developer and checking `"push": true`.
- Treating empty review lists as "no comments" instead of asking the developer to submit a `PENDING` draft.
- Leaving a review comment without a fix or a reply, writing a long reply, or deciding a disputed comment yourself.
- Running `tea pulls reply` without `</dev/null`, so it hangs.
- Not recording the review or the merge under `## Review results`.
- A pull request description that skips the project's template sections or ticks a box without evidence.
- Passing the description or replies through `embed_writing` (this skill doesn't load it).
