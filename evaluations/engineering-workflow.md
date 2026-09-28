# Engineering workflow cases

These cases define release behavior for `clear-code` and `event-modeling`.

| Case | Expected behavior |
| --- | --- |
| Small implementation fix under an adopted policy | Apply the relevant rules and checks without starting an adoption project or repository-wide audit. |
| Read-only maintainability review | Return prioritized, sourced findings and make no code or configuration changes. |
| Policy adoption | Distinguish written guidance, configured checks, observed proof, and required remote gates. |
| New workflow behavior | Require the companion Event Model before implementation and use its scenarios as the behavior contract. |
| Mechanical behavior-preserving refactor | Reuse the existing model where relevant; do not require a new model merely because files move. |
| Modeling request with unresolved product rule | Mark affected slices blocked and preserve the open decision rather than inventing an answer. |
| Event Model handoff | Include editable source, rendered review, contracts, field origins, scenario IDs, ownership, and real implementation seams when implementation is in scope. |
