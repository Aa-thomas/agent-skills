---
name: validate-pr
description: Perform a read-only, evidence-based readiness assessment of a Git branch or pull request. Use when the user asks whether a PR is ready, wants PR validation, or needs blocking findings, warnings, a corrected title, and missing verification evidence.
---

# Validate a Pull Request

Assess whether a branch or PR is trustworthy and reviewable. Report findings without silently editing files, rewriting commits, changing PR content, or publishing anything.

## Resolve and inspect the PR

1. Resolve the target branch from the user, existing PR metadata, tracked remote default, or repository conventions, in that order.
2. Inspect the current branch, `git status --short`, and the commit history since the merge base.
3. Inspect the complete `git diff --stat <target>...HEAD` and `git diff --find-renames <target>...HEAD`.
4. Inspect the PR title and body when they exist. If they do not exist, evaluate any supplied draft and otherwise list them as missing publication content.
5. Inspect relevant untracked, unstaged, ignored, binary, rename, mode, and submodule state so important omissions are visible.

Never validate only the latest commit when the PR contains more than one commit.

## Verify coherence and claims

Check:

- The branch contains one coherent, reviewable change.
- The branch differs from the selected trunk and is cleanly mergeable into it.
- The title uses `<type>(<scope>): <imperative summary>`, an allowed type, a meaningful scope, no trailing period, and at most 72 characters.
- The title and body describe the full branch diff accurately.
- Problem, design, risk, compatibility, and follow-up claims have artifact or user-supplied support.
- Verification claims correspond to exact commands and observed outcomes.
- Relevant tests, linting, type checking, builds, and manual checks have evidence appropriate to the change.
- No relevant tracked or untracked file appears accidentally omitted.
- Commit history is understandable and does not conceal unrelated work.
- Breaking changes are explicitly identified.

When the user asks to merge, report validation evidence first. Leave the merge
to `$trunk-based-delivery` after explicit user authorization; validation alone
never grants merge authority.

Discover checked-in repository guidance for required checks. Run safe, proportionate checks unless the user requests inspection only. A check that was not run is missing evidence, never an assumed pass. Distinguish failures caused by the change from infrastructure or environment limitations.

## Classify findings

Use a blocking finding when the PR should not be published or merged as represented, including:

- failing required checks;
- materially false or unsupported claims;
- missing essential title or body content;
- unrelated changes that prevent coherent review;
- an undeclared breaking change;
- likely accidental file omissions; or
- no meaningful branch diff.

Use a warning for non-blocking uncertainty, cleanup, or scope concerns. Do not block solely for an optional preference.

Set `status` to `ready` only when `blocking_findings` and `missing_evidence` are both empty. Otherwise set it to `needs_changes`.

## Return YAML

Return only one fenced YAML document using this shape:

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

Use empty arrays (`[]`) when a collection has no entries. Make each finding specific, actionable, and grounded in inspected evidence. Provide a corrected `suggested_title` even when the existing title is valid; use `null` only when the diff is too incoherent or absent to summarize truthfully.
