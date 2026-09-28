---
name: draft-commit
description: Draft a truthful commit message from the currently staged Git diff, or create that commit when the user asks to commit. Use for staged-change commit messages and commit actions. Do not use for unstaged work, whole-branch PR descriptions, or the broader delivery lifecycle.
---

# Draft a Commit

Describe one coherent staged change. Treat the staged diff as the complete source
of truth for the message.

## Resolve the requested action

Draft only when the user asks for a message, wording, or description. Create the
commit when the user asks to commit, including concise requests such as “commit”
or “commit this.” Do not repeat a confirmation already supplied in the current
session.

Inspect `git status --short`, the current branch, and the remote default branch.
Then inspect `git diff --staged --stat` and the full staged diff including
renames, modes, binaries, and submodules where relevant.

Stop with a specific next action when:

- nothing is staged;
- the staged files contain unrelated changes that need separate commits; or
- the current branch is trunk and no direct-to-trunk exception is authorized.

Never describe unstaged or untracked work as committed. Use history only to learn
the repository's established message style and scope vocabulary.

## Write the message

Follow a checked-in commit convention when one exists. Otherwise use:

```text
<type>(<scope>): <imperative summary>

<optional explanation grounded in the staged diff>

<optional issue or breaking-change footer>
```

Choose a type that reflects the staged behavior: `feat`, `fix`, `refactor`,
`test`, `docs`, `chore`, `build`, `ci`, or `perf`. Choose the primary
domain or component as scope. Keep the summary concise, imperative, and free of a
trailing period.

Include a body only when it helps explain behavior, a material design choice, or
an important limitation. Add `BREAKING CHANGE:` only when the staged diff proves
an incompatible public change. Add issue references only from inspected artifacts
or user context. Never invent motivation, verification, compatibility, or future
work.

## Return or create

For a draft, return only the complete message in one fenced text block, followed
by a material coherence warning if needed.

For an authorized commit, create it with the complete message. If Git rejects the
operation, report the exact failure and leave staged work intact. On success,
return the commit hash and exact message. Do not push, open a PR, or change branch
state as part of this skill.

Use `$trunk-based-delivery` only when the user requested the broader branch,
publication, validation, or merge workflow.
