---
name: event-modeling
description: Create, update, or review actual Event Models using Adam Dymitruk's method. Use when the user asks to model a business workflow, create an event timeline, connect screens with commands and read models, or when project instructions require Event Modeling before implementation. Produces editable visual models, concrete data contracts, and command/view scenarios. A modeling request does not authorize application implementation.
---

# Event Modeling

Describe what happens over time, who owns each change, and where information
comes from and goes. This skill can be used independently for feature planning,
specification review, or migration design.

## Establish the scope

Read the applicable project instructions and existing feature specifications,
models, domain terms, and approved wireframes. Use existing artifacts as the
starting point. Distinguish observed behavior, proposed changes, and unanswered
questions. Keep one authoritative model with the feature specification.

For review-only requests, report gaps without rewriting artifacts. A request to
model a workflow does not authorize implementing it, publishing tickets, changing
architecture, or bypassing the project's design and approval requirements.

## Apply the method

Read and follow the [Event Modeling method](references/event-modeling.md). Its
seven steps, four patterns where applicable, and information-completeness review
are required. The reference includes concrete contracts, command/view scenarios,
and an [editable visual example](assets/event-model-example.svg).

Produce an editable visual timeline with concrete data, ownership lanes, screens
or system actors, commands, events, and read models. Include external translation
and automation wherever the workflow uses them. A summary table or generic
flowchart alone does not satisfy this requirement. Keep the work proportional by
modeling the affected journey and relevant alternatives while retaining the
method. Behavior-preserving changes can reuse their existing model.

Resolve consequential unknowns with the domain owner; do not invent product rules
or guarantees to complete the picture. Report which decisions remain open and
which parts of the model depend on them. Model semantics work across languages
and storage designs without requiring event sourcing or new infrastructure.

## Review and hand off

Trace modeled fields from their sources to their destinations. Check that each
scenario names one command or read model and that meaningful rejection, failure,
and concurrency cases agree with the proposed contract. Render and inspect the
visual artifact; syntax or rendering success alone cannot prove the model correct.

Deliver the model and editable source, data contracts, scenario IDs, ownership,
and unresolved decisions. When implementation is in scope, connect scenarios to
real code and test locations and report checks actually run. For a migration,
identify the current authority and shared behavior cases before cutover. Update
models and affected explanations alongside behavior changes; reuse the same
model rather than creating a competing implementation document.
