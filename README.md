# Agent Skills

Reusable skills for maintainable code, careful delivery, model routing, and usage awareness:

- `clear-code` — adapt maintainability rules, practical DDD boundaries,
  complexity review, and enforcement to a repository.
- `explain-code` — understand a change through its behavior, change-impact map,
  important alternatives, and an explanation checked against the evidence.
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

For example, from this repository, install Clear Code for personal use:

```sh
mkdir -p "$HOME/.agents/skills"
# Review existing copies before replacing them.
test -e "$HOME/.agents/skills/clear-code" ||
  cp -R skills/clear-code "$HOME/.agents/skills/"
```

For project-local installation, copy the complete `clear-code` folder into the
repository's `.agents/skills/` directory. Record the source commit when vendoring
it. For personal automatic use, add a short hook to your global `AGENTS.md` to
apply Clear Code before coding. Each repository keeps its own engineering policy;
the global hook does not copy Evoke's domain rules into another project.

Clear Code uses [em](https://github.com/milehimikey/em) for Event Modeling. The
former custom `event-modeling` skill has been retired. When upgrading, update
Clear Code and remove only that old custom skill after checking for local changes;
do not delete an unrelated or upstream skill with the same name.

Install em as a development tool when adopting modeling in a repository. For
example, `npm install --save-dev --save-exact --include=dev @milehimikey/em@1.13.0` pins the
version verified for this adoption. Other stacks can use a small tooling package
or a documented pinned CLI installation. Record the version, model directory,
setup, validation, and render commands in the project's engineering policy.
Future projects inherit the shared guidance, not an automatic installation or
CI setup. Existing working models are migrated only when their workflow changes.

Then invoke it in the target repository:

> Use $clear-code to adopt maintainability rules for this repository.
> Map the existing domain boundaries, add a short AGENTS.md hook and project
> policy, and implement the smallest useful checks. Preserve working behavior.

Or invoke the modeling workflow directly:

> Use em to model this feature, following this repository's engineering policy.

The guidance supports Python, TypeScript, and Svelte migrations and adapts to
other stacks. em is development tooling, not an application runtime dependency.
Its basic model/render/validate workflow needs no upstream Claude skill bundle
or MCP server. Installation makes tools available; adopting a project policy and
configuring checks are separate work. It does not rewrite application code.

## Contents

Use Explain Code for a focused Markdown explanation or a substantial HTML
walkthrough, with optional questions and small demonstrations:

> Use $explain-code to explain this PR and where a future requirement would fit.

It reads the project's own rules and does not require the other skills to be
installed. Copy its complete folder using the same installation convention above.

Each directory contains a `SKILL.md` instruction file and an
`agents/openai.yaml` interface definition. Some skills also include references or
templates that should be copied with the skill.
