---
name: draft-pr
description: Draft or improve a pull request title and body from the complete branch diff and available evidence. Use when the user asks for PR copy, a PR description, or review-ready change notes. This skill drafts text; it does not publish, update, validate, or merge the PR.
---

# Draft a Pull Request

Explain the concrete problem and resulting behavior so a reviewer can assess the
whole branch without reconstructing the conversation. Return draft text only
unless the user separately asks to publish or update it.

## Establish the change

Resolve the target branch from the user, existing PR metadata, tracked remote
default, then repository convention. Inspect the current branch, worktree state,
commits since the merge base, and the complete three-dot diff including renames,
binary changes, modes, and submodules where relevant.

Treat committed branch content as PR scope. Mention relevant unstaged or untracked
work as a warning rather than describing it as part of the PR. If there is no
branch diff, the target cannot be resolved, or unrelated changes prevent one
truthful explanation, stop with the specific problem and next action.

Use issues, specifications, commit messages, and user context only when they are
available and agree with the diff. Never invent motivation or design rationale.

## Gather evidence

Follow checked-in repository guidance for required tests, linting, type checks,
builds, and manual checks. Run safe, proportionate checks for a publishable draft
unless the user asks for text only. Record each command, observed result, and the
code state it covers.

A verification claim is supported only when it was observed during the current
work or the user supplied specific evidence that is clearly labeled. The presence
of tests is not a passing result. Distinguish a product failure from an unavailable
tool or environment. Do not turn an unavailable check into a pass.

## Write for this repository

Use the repository's required PR template when one exists. Otherwise scale the
body to the change:

- Start with the concrete problem or requirement and the resulting behavior.
- Explain material implementation or design decisions that a reviewer needs.
- Report checks with exact commands and observed outcomes.
- Include risks, limitations, or follow-up work only when they are real.

A small, self-explanatory change may need one or two short paragraphs plus its
validation. A complex change may need sections such as `Problem`, `Change`,
`Design decisions`, `Verification`, `Evidence`, `Risks`, and `Follow-up work`.
Do not add empty sections or generic checklists merely to fill a template.

Write the title as `<type>(<scope>): <imperative summary>` when that matches the
repository convention. Otherwise follow the repository's format. Summarize the
full branch, keep the title concise, and do not add an issue identifier that was
not supplied by an authoritative source.

## Return the draft

Return the proposed title in a fenced text block, followed by the complete body
in a Markdown code fence. After the draft, add only warnings that materially
affect publication or review. Do not publish or update a PR as part of this skill.

For lifecycle work such as creating a branch, publishing, merging, or verifying
the post-merge result, use `$trunk-based-delivery` when that larger workflow was
requested.
