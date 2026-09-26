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

## Invariants and effects

| Rule that must remain true | Enforcing operation | Allowed side effects | Behavioral evidence |
| --- | --- | --- | --- |
| {{domain rule}} | {{path / symbol}} | {{writes / external actions}} | {{test path / case}} |

Draft/accepted/derived state ownership: {{only the distinctions this project uses}}.
Retries, conflicts, and failure semantics: {{relevant operations and policy}}.

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

## Migration boundary, when applicable

Current authority: {{runtime / operation}}. Target: {{runtime / operation}}.
Compatibility contract and evidence: {{schema and behavior cases}}.
Cutover, rollback, and old-code retirement: {{explicit conditions}}.

## Change evidence

Describe the changed behavior and owning boundary. Give checks actually run and
their outcomes. Identify material exceptions, missing verification, and remaining
decisions. Keep the explanation proportional to the change.
