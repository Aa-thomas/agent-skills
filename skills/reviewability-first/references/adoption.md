# Adopt rules that the repository can enforce

## Inspect, then adapt

1. Establish the requested outcome: audit, policy setup, a refactor, or applying
   existing rules. Make changes already authorized by that outcome; do not start
   an application rewrite as a side effect of setting up a policy.
2. Read applicable instructions, manifests, entry points, CI configuration,
   existing architecture decisions, and a representative change path. Locate
   real check commands and their included and excluded files.
3. Map responsibilities with existing paths: owner, accepted state, public
   operations, permitted dependencies, and forbidden cross-boundary access.
   Explain conflicting meanings using separate contexts and explicit contracts.
4. Identify the smallest useful enforcement gap. Reuse a working linter, type
   checker, or test runner. Add a tool only when a concrete rule needs it and the
   maintenance cost is justified. Do not install every tool in the language guide.
5. Adapt the policy template into the existing engineering guide, or a short
   `docs/engineering.md` if none exists. Resolve every placeholder; mark a needed
   decision as proposed rather than inventing facts. Remove irrelevant sections.

Keep the policy specific: an actual path, dependency direction, owner, invariant,
or executable check is more useful than another page of generic advice. Do not
copy this entire skill into AGENTS.md. Preserve existing instructions and add a
small hook once the project policy exists, for example:

```md
## Maintainability

For code changes, apply $reviewability-first and follow docs/engineering.md.
Read the affected feature's ownership rules before editing. Run the checks
listed there. Do not weaken check scope, baselines, or exceptions to pass a change.
```

Adapt the path and invocation syntax to the agent in use. The checked-in policy
should still be understandable by a human or an agent without skill support.

## Turn selected rules into real checks

| Rule | Suitable evidence or enforcement |
| --- | --- |
| Allowed dependency direction and no cycles | Import or dependency graph checker |
| Types at public interfaces | Configured type checker with inspected source coverage |
| Excessive branching or nesting | Linter/analyzer with a measured baseline |
| Domain invariant and rejection semantics | Focused behavioral tests |
| API compatibility across runtimes | Shared wire fixtures and contract tests |
| Human comprehension and useful abstraction | Review of a representative operation |

For each enforced rule record its command, configuration, covered paths,
baseline or exceptions, and the CI job that runs it. A successful command over
an empty or irrelevant file set proves nothing. Include new source directories
and check CI path filters, not just the tool's configuration.

When adding or materially changing enforcement, prove one representative failure
is caught: use a disposable fixture or isolated edit, observe the expected
nonzero result, remove the violation, and verify the clean result. Never commit
the deliberate violation. Check configuration syntax alone is insufficient.

Use the same commands locally and in CI where feasible. Report separately if a
job exists but is not a required merge check. Follow the task's authority for
remote repository settings; configuring CI is not permission to change protection.

## Introduce a baseline without hiding debt

An existing violation need not force a repository rewrite. Measure current code
with the selected analyzer, preserve its result, and block new violations or
worsening existing ones when that policy is adopted. Compare new and changed
symbols to the baseline; carry an existing violation through a rename or move.

Use a tool's supported baseline or narrow per-rule exceptions where possible.
Do not build a custom general-purpose analyzer for a few existing violations.
If the tool cannot compare per-symbol changes, state that limitation and choose
a simpler enforceable policy, such as strict checks on a named new package plus
review of legacy changes. Do not claim a ratchet that the tooling cannot enforce.

Each exception needs a rule, exact scope, measured value where applicable,
reason, responsible owner, and expiry or removal condition. An exception for a
legacy function must not exempt new functions throughout its module. Baseline
updates and exceptions must be visible in the change review, not regenerated
automatically as a way to make CI pass.

## Confirm adoption

Report the policy path, short instruction hook, enforcement added, measured
baseline, commands and observed results, and remaining manual review duties.
Installation, writing the policy, and activating enforcement are distinct steps.
Do not report enforcement complete when it is only documented or configured.
