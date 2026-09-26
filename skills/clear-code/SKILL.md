---
name: clear-code
description: Establish and apply maintainability rules for agent-written code. Use when the user asks for agent coding rules, a complexity budget, a maintainability audit, practical DDD boundaries, or a reviewable refactor or migration; also use when repository instructions explicitly adopt this skill. Adapt shared principles to the repository's language, domain, and existing tools. Do not initiate a repository-wide audit or rewrite for an ordinary small fix.
---

# Clear Code

Write code that humans can understand and agents can safely maintain.

Make a change understandable without its original ticket. A maintainer should
be able to find its purpose, inputs, state owner, rules, effects, failure behavior,
and verification without reconstructing hidden conventions.

## Choose the scope

- **Adopt:** establish repository rules and the smallest useful checks. Read
  [adoption and enforcement](references/adoption.md), then adapt the
  [policy template](assets/engineering-policy.md) into existing project docs.
- **Apply:** follow an adopted policy while implementing or reviewing the
  requested change. Read only the affected feature's rules and dependencies.
- **Audit or plan:** inspect and report evidence; do not edit application code
  or install tools when the request is read-only.

Read applicable repository instructions first. Preserve their delivery,
authorization, and design requirements. Installing this skill makes guidance
available; it does not adopt a policy, configure CI, or guarantee agent compliance.
Keep domain decisions in the target repository, not in this reusable skill.

## Establish ownership before changing code

Trace one representative operation from entry point to state change and effects.
Identify the existing implementation, its public interface, callers, rule owner,
and tests. Distinguish observed structure from proposed structure. Read more only
where a dependency or unresolved risk requires it.

Use domain-driven design (DDD) where it clarifies responsibility:

- **Shared language:** use the project's business terms in code. Clarify a term
  when different meanings would change a rule; keep an existing glossary current.
- **Bounded contexts:** name areas where a model and its rules have a consistent
  meaning. Record which area owns each decision and how others obtain its result.
  A context is a responsibility boundary, not necessarily a service or folder.
- **Explicit translation:** the same real-world thing can have different models
  in different contexts. Translate at their interface instead of making every
  context depend on a universal entity with all possible fields.
- **Invariants:** place rules that must stay true near their enforcing operation.
  Tests should demonstrate the allowed transition and meaningful rejection cases.
- **Selective patterns:** use a value object when it prevents invalid values;
  use an aggregate when related changes must preserve a rule atomically. Do not
  prescribe a repository class per entity, a framework, or microservices.

For example, order capture owns what was ordered; fulfillment owns shipment
progress. An order update should use their contract, not mutate shipment internals.
A small application can implement both responsibilities in ordinary modules.

## Make the implementation easy to follow

Follow established language, framework, and local project conventions. Explain
the concrete problem before introducing a competing pattern. A transferable
principle need not have an identical implementation in Python and TypeScript.

1. Group code by feature or domain responsibility where that improves locality.
   Keep related UI, state, API calls, and tests discoverable together; retain a
   useful existing structure instead of moving files for stylistic uniformity.
2. Name operations for their effect: `resolve_note_conflict`, not `process_data`.
   Show inputs, outputs, errors, and side effects at the public boundary.
3. Keep business decisions independent of HTTP, storage, UI, and provider details
   where practical. Pass validated values or narrow dependencies explicitly;
   add a forwarding layer only when it protects a named boundary or present need.
4. Judge an abstraction by what callers no longer need to understand. A single
   consumer can justify a module that hides a difficult or change-prone decision
   behind a simpler interface, or protects a real boundary. Demonstrated reuse
   is useful evidence; speculative future capabilities are insufficient. Prefer
   a cohesive operation over a chain of tiny helpers.
5. Allow inexpensive local duplication when it aids understanding. Give accepted
   business decisions one authoritative owner; do not duplicate them casually
   across a browser, backend, worker, or second language.
6. Distinguish authoritative state, drafts, queued work, and derived views. Name
   who can change each and through which operation. Make hidden writes, retries,
   partial failure, and conflict handling visible where relevant to the feature.
7. Validate untrusted input at runtime. Static types do not validate network,
   persistence, or model output. Prefer one canonical boundary contract and
   generated types where generation removes genuine drift.

When fields depend on one another, model the valid variants explicitly instead
of combining independent booleans and optional fields. For example, a completed
run requires a result and a failed run requires an error. Check that all variants
are handled using the language's types and relevant behavioral tests.

## Judge complexity with evidence

Do not turn maintainability into one score. Inspect these independent signals:

| Signal | Question to answer |
| --- | --- |
| Control flow | How many branches, nesting levels, and failure paths must a reader track? |
| Locality | How many files and forwarding calls are needed to explain one operation? |
| Coupling | Which contexts or private internals must change together? Are imports cyclic? |
| State | How many independently writable copies or hidden transitions exist? |
| Change cost | Which high-change areas repeatedly break or require wide edits? |

If no policy exists, propose these **review triggers**, then calibrate them on
representative code: cyclomatic complexity above 10, nesting above 3 levels,
functions above 80 nonblank noncomment lines, or modules above 400 such lines.
These are starting heuristics, not research-backed universal limits. Define how
the chosen analyzer counts each metric. Assess Svelte markup, fixtures, generated
code, and handwritten logic separately; do not silently exclude meaningful logic.

A trigger calls for inspection, not automatic rejection or splitting. Enforce
numeric limits only after the repository adopts an explicit rule and baseline.
Never lower a score by hiding logic behind forwarding helpers, compressing lines,
moving it into unchecked files, or broadening suppressions. A low score does not
prove understandable code.

Before adding a dependency, layer, service, state store, or generic mechanism,
state the present need, the complexity it removes or necessarily introduces,
and the simpler option considered. A net increase may be justified by a real
requirement; speculative flexibility is not a sufficient justification.

For a consequential, nonobvious decision, retain the rationale, rejected
alternative, and accepted limitations near the code or in an existing decision
record. Keep it brief; routine edits do not need a separate design document.

## Apply checks and handle migrations

Use the repository's existing tools first. Read the
[Python and TypeScript guidance](references/python-typescript.md) only for those
languages or a migration involving them. Other stacks use the same ownership
principles with their own native tools.

Keep structural refactors and behavior changes in separately reviewable steps.
Establish passing checks for affected observable behavior before restructuring,
and keep them passing through small changes. If coverage is missing, add focused
characterization tests where the risk warrants them. Identify known defects
explicitly; changing that behavior is a separate step, not a hidden cleanup.

For a migration, select a small working slice, preserve its observable contract,
and identify cutover and rollback before adding a second implementation. If both
must coexist, document the current authority, shared contract cases, and retirement
condition. Language conversion is not permission to redesign product rules.

Run required repository checks and focused checks for affected behavior. Test
invariants, public boundaries, and meaningful failure cases rather than helper
structure. Treat edits to check scope, baselines, or suppressions as policy changes
that need explicit review; do not weaken a gate to make the current change pass.

For design rationale or deciding whether stronger verification is warranted,
read [principles and their limits](references/design-principles.md). Apply them
in proportion to the change; they are not additional mandatory tooling.

## Finish concisely

Report what changed or was found, the owning boundary, checks actually run and
their outcomes, and any material exception or unresolved decision. For an audit,
prioritize a few findings with file/symbol evidence and a concrete next action;
label sampled coverage and do not claim a full audit from a few large files.

Separate installed guidance, adopted policy, configured checks, observed passing
checks, and required remote merge checks. None implies the next automatically.
