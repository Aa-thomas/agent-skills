# Agent Skills

Six reusable skills for careful delivery, model routing, and usage awareness:

- `trunk-based-delivery` — deliver a small change through a short-lived branch.
- `draft-commit` — draft or create a truthful Conventional Commit.
- `draft-pr` — draft an evidence-backed pull request title and body.
- `validate-pr` — assess whether a branch or pull request is ready.
- `usage-advisor` — track, explain, and forecast Codex usage.
- `model-router` — choose models and reasoning effort by cost and risk.

## Install

Copy the skill folders you want into your agent's skills directory. For Codex,
that is usually `$CODEX_HOME/skills` (commonly `~/.codex/skills`).

```sh
cp -R skills/trunk-based-delivery "$CODEX_HOME/skills/"
cp -R skills/draft-commit "$CODEX_HOME/skills/"
cp -R skills/draft-pr "$CODEX_HOME/skills/"
cp -R skills/validate-pr "$CODEX_HOME/skills/"
cp -R skills/usage-advisor "$CODEX_HOME/skills/"
cp -R skills/model-router "$CODEX_HOME/skills/"
```

Restart or refresh your agent after installation so it discovers the skills.

## Contents

Each directory contains a `SKILL.md` instruction file and an
`agents/openai.yaml` interface definition.
