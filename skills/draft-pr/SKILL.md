---
name: draft-pr
description: Draft an evidence-backed pull request title and structured body from the full Git branch diff against its target branch. Use when the user asks to write, prepare, improve, or review PR content before publishing.
---

# Draft a Pull Request

Draft a reviewable PR from the entire branch change. Do not publish or update a PR unless the user separately asks.

## Establish the change set

1. Resolve the target branch from the user, an existing PR, the tracked remote default, or repository conventions, in that order. State the selected target when it is not explicit.
2. Inspect `git status --short`, the current branch, and commits since the merge base. Stop if the current branch is the selected target: an ordinary trunk-based PR needs a short-lived feature branch.
3. Inspect `git diff --stat <target>...HEAD` and the full `git diff --find-renames <target>...HEAD`.
4. Include every committed branch change, not merely the latest commit. Treat unstaged and untracked files as outside the PR diff and disclose relevant ones as warnings.
5. Detect unrelated change groups. Recommend concrete split boundaries when the branch does not describe one reviewable product or architectural change.

Use the branch diff as the source of truth for change claims. Use issues, design documents, commit messages, or user-provided context only when available and consistent with the diff.
For branch creation, merge authorization, and post-merge verification, use
`$trunk-based-delivery`.

## Gather verification evidence

Discover repository-prescribed test, lint, type-check, and build commands from its checked-in guidance. Run safe, proportionate checks when drafting a publishable PR unless the user requests a text-only draft. Record the exact command and outcome.

Treat a verification claim as supported only when:

- the command ran during the current work and its result was observed; or
- the user supplied specific evidence and the body labels it as user-supplied.

Do not convert the presence of test files into a claim that tests passed. Mark checks that did not run as unchecked and explain why in `Evidence` or `Risks`.

## Write the title

Use `<type>(<scope>): <imperative summary>` with one of:

`feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `build`, `ci`, or `perf`.

Choose the primary responsibility as the scope, keep the title at most 72 characters, and omit a trailing period. The title must summarize the full PR rather than one commit.

## Write the body

Use exactly these sections:

```markdown
## Problem

What limitation, failure, or requirement motivated this change?

## Change

What changed?

## Design decisions

Why was this implementation chosen?
Which responsibilities remain outside this PR?

## Verification

- [ ] Tests added or updated
- [ ] Full test suite passes
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Manual behavior verified

## Evidence

Commands, observed results, traces, screenshots, or benchmarks.

## Risks

What could regress?
What assumptions does the change depend on?

## Follow-up work

What was intentionally left outside this PR?
```

Replace prompts with concise, concrete prose. Check a box only when evidence supports that exact statement. Use `None identified` rather than inventing risks or follow-up work. If the problem or a design rationale is not established by available artifacts, say so plainly or request the missing context; do not manufacture it.

Return the proposed title in a text block followed by the complete Markdown body. Add warnings after the draft only when they materially affect publishing or review.
