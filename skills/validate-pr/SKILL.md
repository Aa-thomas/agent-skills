---
name: validate-pr
description: Perform a read-only readiness assessment of a Git branch or pull request using its full diff, publication content, and verification evidence. Use when the user asks whether a PR is ready or requests PR validation. Do not use for drafting PR copy or carrying a change through delivery.
---

# Validate a Pull Request

Decide whether the PR is truthful, coherent, and supported by enough current
evidence to publish or merge as represented. This skill is read-only: do not edit
files, rewrite commits, change PR content, publish, or merge.

## Resolve the candidate

Resolve the target branch from the user, existing PR metadata, tracked remote
default, then repository convention. Inspect the current branch, worktree state,
commit history since the merge base, and complete three-dot diff including
renames and relevant binary, mode, ignored, untracked, and submodule state.

Read the live PR title and body when they exist; otherwise assess the supplied
draft. If neither exists, record missing publication content. Never validate only
the latest commit when the branch contains more work.

## Assess the evidence

Check that:

- the branch contains one coherent, reviewable change and differs from its target;
- the title and body accurately describe the full diff and follow repository rules;
- claimed motivation, behavior, compatibility, risk, and follow-up are supported;
- required checks have exact, current outcomes for the code being assessed;
- relevant files are not accidentally omitted from the branch;
- breaking behavior is identified; and
- mergeability and required remote checks are established when merge readiness is
  being claimed.

Run safe, proportionate, read-only checks required by the repository unless the
user requests inspection only. Treat generated caches or build outputs as effects;
do not run a check when its effects exceed the request's authority. Separate a
change failure from an environment or infrastructure limitation.

Missing evidence stays missing. A prior result may be reused only when it applies
to the same code and environment and remains current for the decision. Refresh
live host state before a merge-readiness conclusion.

## Classify the result

Use a blocking finding when the PR should not be published or merged as
represented, including a failing required check, materially false claim,
incoherent scope, undeclared breaking change, likely accidental omission, or no
meaningful diff. Use a warning for non-blocking uncertainty or improvement.

List an item under `missing_evidence` when a required fact or result was not
established. If that absence also makes publication or merge unsafe, state the
consequence under `blocking_findings`; do not duplicate the same sentence.

Set `status` to `ready` only when both `blocking_findings` and
`missing_evidence` are empty. Otherwise use `needs_changes`.

## Return YAML

Return only one fenced YAML document with exactly these top-level fields:

```yaml
status: ready | needs_changes
blocking_findings:
  - ...
warnings:
  - ...
suggested_title: ...
missing_evidence:
  - ...
```

Use `[]` for an empty collection. Every entry must name the evidence and next
action. Always suggest a truthful title when the diff is coherent enough; use
`null` only when no defensible title can be derived.

When the user requests full delivery or merge, return this assessment first and
leave subsequent lifecycle actions to `$trunk-based-delivery` under the user's
existing authorization.
