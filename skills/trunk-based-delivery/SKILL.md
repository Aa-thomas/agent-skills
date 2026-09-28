---
name: trunk-based-delivery
description: Carry one coherent repository change through a short-lived branch, commit, pull request, validation, and authorized merge. Use when the user asks to start, ship, or take a change through multiple delivery stages. Do not use for a commit-message-only, PR-draft-only, or read-only PR-readiness request.
---

# Trunk-Based Delivery

Keep trunk releasable while moving one coherent change through the stages the user
requested. Resume from the repository's actual state; do not restart completed
stages or ask again for authorization already given in the session.

## Establish the delivery state

Inspect the worktree, current branch, remotes, remote default branch, commits, and
any existing PR. Treat the remote default as trunk without assuming its name.
Identify which stages are complete, current, and still requested.

Preserve unrelated and dirty work. Do not discard changes, stage unrelated files,
rewrite shared history, switch away from uncommitted work, or delete branches
without explicit authorization.

For new work, refresh remote trunk and create a descriptive short-lived branch
before editing. Keep one reviewable change per branch. If work already exists on
a suitable branch, continue there rather than creating a duplicate.

## Move through the requested stages

1. Implement and verify the bounded change using repository guidance.
2. Use `$draft-commit` for one coherent staged diff when a commit is requested.
3. Push and use `$draft-pr` when PR publication is requested. The PR must describe
   the complete branch diff.
4. Use `$validate-pr` before a requested merge. Refresh live mergeability,
   required checks, and PR content.
5. Merge only when the current session authorizes the merge and the host reports
   it is allowed. Follow the configured merge method; if none is established and
   the choice would change history, obtain the user's choice.

Do not treat a commit, push, PR, or passing local check as authorization for the
next consequential stage. Equally, do not interrupt already authorized work with
repeated confirmation requests.

## Handle interruptions and failures

On a conflict, rejected push, failing check, unavailable host, or uncertain
mergeability, preserve the work and report the exact failed stage. Retry only
when the failure is transient and the retry cannot duplicate an external effect;
otherwise re-read the remote state before proceeding.

Direct-to-trunk and emergency requests are explicit exceptions. Preserve the same
scope and evidence standards and record which normal boundary was bypassed.

## Finish with evidence

Report the furthest completed stage, branch, commits, PR URL when present, exact
checks and outcomes, and anything still required. After merge, verify the merged
PR and resulting trunk commit. Do not delete the branch unless that action was
authorized.
