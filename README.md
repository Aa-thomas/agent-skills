# Agent Skills

Reusable skills for maintainable code, careful delivery, model routing, and usage awareness:

- `clear-code` — adapt maintainability rules, Event Modeling, practical DDD boundaries,
  complexity review, and enforcement to a repository.
- `trunk-based-delivery` — deliver a small change through a short-lived branch.
- `draft-commit` — draft or create a truthful Conventional Commit.
- `draft-pr` — draft an evidence-backed pull request title and body.
- `validate-pr` — assess whether a branch or pull request is ready.
- `usage-advisor` — track, explain, and forecast Codex usage.
- `model-router` — choose models and reasoning effort by cost and risk.

## Install

Copy the complete skill folders you want into your agent's skills directory.
For current Codex, use `~/.agents/skills` for personal skills, or `.agents/skills`
inside the target repository for a checked-in project skill. See the
[official skills guidance](https://learn.chatgpt.com/docs/customization/overview#skills).

For example, from this repository, install the new skill for personal use:

```sh
mkdir -p "$HOME/.agents/skills"
# If this skill already exists, review its differences before replacing it.
test -e "$HOME/.agents/skills/clear-code" ||
  cp -R skills/clear-code "$HOME/.agents/skills/"
```

For a repository such as Evoke, copy `skills/clear-code/` into that
repository as `.agents/skills/clear-code/`, including its `agents`,
`references`, and `assets` folders. Review an existing copy before replacing it.
Record the source commit when copying so later updates can be reviewed.

Then invoke it in the target repository:

> Use $clear-code to adopt maintainability rules for this repository.
> Map the existing domain boundaries, add a short AGENTS.md hook and project
> policy, and implement the smallest useful checks. Preserve working behavior.

The skill supports Python, TypeScript, and Svelte migrations and adapts to other
stacks. Installation makes the guidance available; adopting a project policy and
configuring checks are separate work. It does not automatically rewrite code or
enforce every recommendation.

## Contents

Each directory contains a `SKILL.md` instruction file and an
`agents/openai.yaml` interface definition. Some skills also include references or
templates that should be copied with the skill.
