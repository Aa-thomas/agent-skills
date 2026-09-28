# PR workflow pilot cases

These cases record the behavior expected from `draft-pr` and `validate-pr`.
They are release checks, not examples that every output must copy verbatim.

## Drafting cases

| Case | Input | Expected behavior |
| --- | --- | --- |
| Tiny documentation change | One committed wording correction with a passing link check | Use the repository template when required; otherwise return a brief problem/change statement and observed verification without empty sections. |
| Multi-commit behavior change | Several commits contributing to one feature | Explain the complete three-dot diff, not only the latest commit. Include material design decisions and exact verification. |
| Dirty worktree | A coherent committed branch plus unrelated unstaged files | Keep the draft scoped to committed work and warn about relevant local files. |
| Unsupported test claim | A commit message says tests pass but no current result exists | Leave the claim unsupported or unchecked and identify the missing evidence. |
| Repository template | A checked-in PR template conflicts with the generic section set | Follow the repository template while keeping claims grounded in the diff. |

## Validation cases

| Case | Expected behavior |
| --- | --- |
| Accurate small PR with current required checks | Return `ready`, empty blocking and missing-evidence arrays, and a truthful suggested title. |
| Claimed passing test without a current or supplied result | Return `needs_changes`; list the result under `missing_evidence` and explain any unsafe publication consequence under `blocking_findings`. |
| Required check fails because of the change | Return `needs_changes` with a concrete blocking finding. |
| Check cannot run because its service is unavailable | Keep the result under `missing_evidence`; do not describe it as a product failure or pass. |
| Incoherent branch with unrelated features | Return `needs_changes`, identify reviewable split boundaries, and use `suggested_title: null` when no truthful combined title exists. |

## Selection boundaries

- “Write a commit message for my staged files” selects `draft-commit`, not either
  PR skill.
- “Write my PR description” selects `draft-pr` and does not publish it.
- “Is this PR ready?” selects `validate-pr` and remains read-only.
- “Take this completed change through a validated PR” selects
  `trunk-based-delivery`, which may call both skills at the appropriate stages.
