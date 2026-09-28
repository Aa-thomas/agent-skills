# Agent Skills

Reusable skills for maintainable code, careful delivery, model routing, and usage awareness:

- `clear-code` — adapt maintainability rules, practical DDD boundaries,
  complexity review, and enforcement to a repository.
- `event-modeling` — create and review visual Event Models with concrete data,
  ownership, and command/view scenarios; usable independently for planning.
- `explain-code` — understand a change through its behavior, change-impact map,
  important alternatives, and an explanation checked against the evidence.
- `trunk-based-delivery` — deliver a small change through a short-lived branch.
- `draft-commit` — draft or create a truthful Conventional Commit.
- `draft-pr` — draft an evidence-backed pull request title and body.
- `validate-pr` — assess whether a branch or pull request is ready.
- `usage-advisor` — track, explain, and forecast Codex usage.
- `model-router` — choose models and reasoning effort by cost and risk.

- `to-tickets` — turn approved plans into vertical slices with explicit outcomes,
  reuse, invariants, failure verification, dependencies, and open decisions;
  adapted from Matt Pocock.

## Install

Copy the complete skill folders you want into your agent's skills directory.
For current Codex, use `~/.agents/skills` for personal skills, or `.agents/skills`
inside the target repository for a checked-in project skill. See the
[official skills guidance](https://learn.chatgpt.com/docs/customization/overview#skills).

Install `clear-code` with its `event-modeling` companion. Clear Code requires the
companion for business-workflow modeling; Event Modeling can also be installed
and used on its own. Installing one folder does not install the other.

For example, from this repository, install both for personal use:

```sh
mkdir -p "$HOME/.agents/skills"
# Review existing copies before replacing them.
for skill_name in clear-code event-modeling; do
  test -e "$HOME/.agents/skills/$skill_name" ||
    cp -R "skills/$skill_name" "$HOME/.agents/skills/"
done
```

For a repository such as Evoke, copy both skill folders into its `.agents/skills/`
directory, including their `agents`, `references`, and `assets` folders. Keep the
folders as siblings so their links resolve. Review existing copies before
replacing them. Record the source commit and update the pair together so later
changes can be reviewed.

Then invoke it in the target repository:

> Use $clear-code to adopt maintainability rules for this repository.
> Map the existing domain boundaries, add a short AGENTS.md hook and project
> policy, and implement the smallest useful checks. Preserve working behavior.

Or invoke the modeling workflow directly:

> Use $event-modeling to model this feature before implementation.

Both skills support Python, TypeScript, and Svelte migrations and adapt to other
stacks. Installation makes the guidance available; adopting a project policy and
configuring checks are separate work. Installation does not automatically rewrite
code or enforce every recommendation.

## Contents

Use Explain Code for a focused Markdown explanation or a substantial HTML
walkthrough, with optional questions and small demonstrations:

> Use $explain-code to explain this PR and where a future requirement would fit.

It reads the project's own rules and does not require the other skills to be
installed. Copy its complete folder using the same installation convention above.

Each directory contains a `SKILL.md` instruction file and an
`agents/openai.yaml` interface definition. Some skills also include references or
templates that should be copied with the skill.
