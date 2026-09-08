---
name: trunk-based-delivery
description: Deliver a small, coherent repository change through a trunk-based workflow. Use when Codex starts a change, creates a branch, opens a PR, asks whether a PR is ready, merges or ships a PR, or is asked to commit directly to trunk.
---

# Trunk-Based Delivery

Keep trunk continuously releasable. Work in one short-lived branch for one
coherent change, validate it, and merge it promptly. Treat the repository's
checked-in policy and the user's explicit request as higher priority.

## Establish the workflow

1. Inspect `git status --short`, the current branch, remotes, and the remote
   default branch. Call that default branch **trunk**; do not assume its name.
2. Preserve a dirty worktree. Do not switch branches, stage unrelated files,
   discard changes, or delete a branch without explicit authorization.
3. For ordinary change work, fetch trunk and create a descriptive branch from
   its current remote tip before editing. Use one of `feat/`, `fix/`, `docs/`,
   `refactor/`, `test/`, or `chore/` when it fits the change.
4. Keep the branch to one reviewable vertical slice. Split unrelated changes
   before committing or opening a PR.

## Commit and open a PR

1. Use `$draft-commit` for the staged diff. Do not commit directly to trunk
   unless the user expressly requests that exception.
2. Push the branch and use `$draft-pr` against trunk. Make the PR describe the
   complete branch diff, not only the last commit.
3. Run repository-prescribed checks plus focused checks appropriate to the
   change. Record exact commands and observed outcomes; leave unchecked items
   visibly unchecked.

## Validate and merge

1. Use `$validate-pr` before merge. Require a coherent diff, a clean merge,
   all required remote checks, and no known local test failure.
2. Do not merge merely because a PR exists. Merge only after the user
   explicitly authorizes it and GitHub (or the repository host) reports it is
   mergeable.
3. Follow the repository's configured merge method. If none is evident, ask
   the user whether to use merge, squash, or rebase; do not guess.
4. Do not delete the feature branch unless the user expressly asks.

## Verify the outcome

1. Confirm the PR is merged and record the resulting trunk commit.
2. Fetch trunk without modifying unrelated local work.
3. Report the PR URL, merged commit, checks run, and any intentionally deferred
   validation or live acceptance.

## Explicit exceptions

When the user explicitly requests a direct-to-trunk or emergency change,
preserve the same evidence standard: inspect scope, run proportionate checks,
and report that the normal PR boundary was intentionally bypassed. Do not turn
an implied urgency into an exception.
