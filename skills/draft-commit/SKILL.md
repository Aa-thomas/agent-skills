---
name: draft-commit
description: Draft a truthful Conventional Commit message from the currently staged Git diff, and create the commit when requested. Use when the user says "commit", "commit this", or "commit my staged changes", asks for a commit message, wants to describe staged changes, or needs a standardized commit title and body.
---

# Draft a Commit

Produce a commit message for one coherent staged change. Create the commit only when the user's request explicitly includes the commit action, including concise requests such as `commit`, `commit this`, or `commit my staged changes`.

## Inspect the staged change

1. Run `git status --short`.
2. Resolve the current branch and the remote default branch. If they are the
   same, do not commit unless the user explicitly requested a direct-to-trunk
   exception; otherwise ask to create a short-lived branch first.
3. Run `git diff --staged --stat` and `git diff --staged --find-renames`.
4. Inspect relevant staged binary, mode, rename, or submodule changes that the textual diff does not explain.
5. If nothing is staged, stop and say that no commit message can be grounded in a staged diff.
6. If the staged files contain unrelated changes, identify the proposed boundaries and recommend splitting them before drafting a final message.

Treat the staged diff as the source of truth. Use repository history only to learn established scope vocabulary and formatting. Never describe unstaged or untracked changes.
For the complete branch, PR, and merge lifecycle, use `$trunk-based-delivery`.

## Construct the message

Use this form:

```text
<type>(<scope>): <imperative summary>

<optional explanation grounded in the staged diff>

<optional issue or breaking-change footer>
```

Choose exactly one type:

- `feat`: add user-visible capability
- `fix`: correct faulty behavior
- `refactor`: restructure without intentionally changing behavior
- `test`: add or revise tests without a product-code change
- `docs`: change documentation only
- `chore`: perform maintenance outside the other types
- `build`: change build tooling or dependencies
- `ci`: change continuous-integration behavior
- `perf`: improve performance

Choose a specific, stable scope from the primary affected responsibility, such as `model-call`, `validation`, `agent-loop`, or `curriculum`. Prefer an established repository scope when one exists. Do not use a filename as the scope when a domain or component name is clearer.

Write an imperative summary that completes “This commit will …”. Keep the header at most 72 characters, prefer lower case after the colon, and omit a trailing period. Wrap body text near 72 characters.

Add `BREAKING CHANGE: <description>` only when the staged diff clearly introduces an incompatible public behavior or interface. Add issue footers only when an issue identifier is present in the staged artifacts or supplied by the user.

## Protect accuracy

- Describe only behavior and intent demonstrated by the staged diff.
- Do not invent motivation, test results, compatibility claims, issue links, or follow-up work.
- Do not claim a behavior is unchanged unless the diff supports that conclusion.
- Prefer omitting a body over filling it with generic restatement.
- If the correct type or primary change is genuinely ambiguous, state the ambiguity and provide at most two labeled candidates.

When the user asks only for a draft, return the proposed commit message in a fenced text block. When the user asks to commit, run `git commit` with the complete message, then report the created commit hash and exact message. Follow either result only with concise warnings that affect trustworthiness or coherence.
