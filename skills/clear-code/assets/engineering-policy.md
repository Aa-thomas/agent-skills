# Engineering policy for {{project}}

<!-- Adapt into the project's existing guide when possible. Resolve placeholders,
     keep only relevant sections, and distinguish proposed rules from adopted ones. -->

## Purpose

Code must make its purpose, inputs, state changes, side effects, failure behavior,
and verification understandable without its original ticket. Prefer explicit,
local code. An abstraction must serve a present need or protect a real boundary.

## Language and ownership

Domain definitions: {{existing glossary or a few terms whose meaning matters}}.
An owner below is the module/context responsible for the rule, not a new service.

| Context and actual path | Authoritative decisions/state | Public operations | Allowed dependencies |
| --- | --- | --- | --- |
| {{context / path}} | {{rules and state it owns}} | {{interface symbols or endpoints}} | {{contexts / packages}} |

Forbidden dependencies or private access: {{specific imports or calls}}.
Cross-context translation: {{where different models meet, or not applicable}}.
Consequential decisions and accepted limitations: {{existing record or brief rationale; omit for routine choices}}.

## Invariants and effects

| Rule that must remain true | Enforcing operation | Allowed side effects | Behavioral evidence |
| --- | --- | --- | --- |
| {{domain rule}} | {{path / symbol}} | {{writes / external actions}} | {{test path / case}} |

Draft/accepted/derived state ownership: {{only the distinctions this project uses}}.
Retries, conflicts, and failure semantics: {{relevant operations and policy}}.

## Event Modeling

Authoritative models and editable sources: {{existing feature specifications / model paths}}.
Rendering and review: {{existing diagram tool / export process; no new tool required}}.
Method reference: {{link to the event-modeling skill or maintained project reference}}.

Before implementing a new or changed business workflow, use `$event-modeling`
to create or update its actual visual Event Model. Keep the full method and
examples in that skill; use the model's command/view scenarios to guide
implementation and review. Install it alongside `$clear-code` for agent use.

Associate each scenario with one command or read model. Cover meaningful
rejection and failure cases; identify relevant retry, concurrency, and partial
completion behavior. Link implementation slices and tests to these scenarios.
Record unknown product decisions explicitly and preserve existing review gates.
Update the model and all affected explanations with the implementation. Reuse
existing models for changes that preserve behavior; do not require new diagrams
for unrelated mechanical edits. Modeling does not require event sourcing.

## Checks and complexity budget

| Rule | Command / configuration | Covered paths | Enforcement |
| --- | --- | --- | --- |
| {{rule}} | {{verified command and config}} | {{actual includes / exclusions}} | {{review trigger, local, CI job, required merge check, or proposed}} |

Review triggers and metric definitions: {{calibrated limits; do not assume universal numbers}}.
Existing baseline: {{measured artifact and comparison procedure, or none}}.
Exceptions: {{rule, exact scope, value, reason, owner, removal condition; or none}}.
Human review: explain an operation through its actual call path; examine hidden
state, cross-boundary changes, and abstractions even when numeric checks pass.
Do not weaken scope, limits, or baselines to make a feature pass its checks.

## Comments and documentation

Document public contracts and non-obvious reasoning without narrating syntax.
Trace code and contract changes through callers, tests, other implementations,
event models, and shared documentation. Update or remove inaccurate comments and
docstrings anywhere affected by the change, including obsolete TODOs and workaround notes.
Maintain generated documentation at its source. Resolve code/comment conflicts
against the intended contract; do not hide a regression by changing the prose.

## Migration boundary, when applicable

Current authority: {{runtime / operation}}. Target: {{runtime / operation}}.
Compatibility contract and evidence: {{schema and behavior cases}}.
Cutover, rollback, and old-code retirement: {{explicit conditions}}.

## Change evidence

Describe the changed behavior and owning boundary. Give checks actually run and
their outcomes. Identify material exceptions, missing verification, and remaining
decisions. Link the affected model and scenarios when applicable. Keep the
explanation proportional to the change.
