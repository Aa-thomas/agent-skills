# Ticket formats and publication rules

Use these formats after the breakdown and destination are authorized. Adapt
tracker-native fields without dropping any required content area.

## Local files

Write one file per ticket under
`.scratch/<feature-slug>/issues/<NN>-<slug>.md`, with blockers first in numeric
order. Do not combine all tickets into one document.

```markdown
# <NN>: <Ticket title>

**Status:** ready-for-agent | blocked | proposed

## Expected behavior

The end-to-end outcome.

## Acceptance criteria

- [ ] Observable criterion

## Existing components and modules to reuse

- Verified owner and responsibility, dependency-delivered work, new work, or
  explicitly unverified candidate.

## Interfaces and invariants

- Material contract or rule.

## Failure cases and verification

- Failure → expected rejection or recovery → verification seam.

## Blocked by

- Ticket references and external gates, or “None”.

## Unresolved decisions

- Decision → blocking or non-blocking → required owner or evidence, or “None
  known” when supported.
```

## Issue trackers

Create one issue per ticket in dependency order.

```markdown
## Parent

Source issue or plan reference when applicable.

## Expected behavior

The end-to-end outcome.

## Acceptance criteria

- [ ] Observable criterion

## Existing components and modules to reuse

- Verified owner and responsibility, dependency-delivered work, new work, or
  explicitly unverified candidate.

## Interfaces and invariants

- Material contract or rule.

## Failure cases and verification

- Failure → expected rejection or recovery → verification seam.

## Blocked by

- Issue references and external gates, or “None”.

## Unresolved decisions

- Decision → blocking or non-blocking → required owner or evidence, or “None
  known” when supported.
```

Use the platform's native blocking or sub-issue relationship when it exists.
Otherwise keep exact issue identifiers in `Blocked by`. Never infer that creating
an issue closes, supersedes, or changes its parent.
