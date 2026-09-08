---
name: model-router
description: Choose the lowest-cost reliable model, reasoning effort, context strategy, and subagent route for Codex work. Use before large plans or implementations, before spawning subagents, when work is ambiguous, high-risk, cross-system, or changing phase, and whenever the user asks which model to use or how to minimize token or credit usage. Do not invoke for an ordinary bounded task unless model or cost guidance is requested.
---

# Model Router

Minimize total task cost while preserving the required result. Optimize the whole workflow, including retries, repeated context, tools, and subagents; do not optimize only the first model call.

## Route the task

Choose the lowest tier that can reliably satisfy the task:

| Route | Use for | Default effort |
|---|---|---|
| Luna | Bounded questions, extraction, summarization, known configuration changes, mechanical edits, and cheap focused subagents | low; medium when synthesis is needed |
| Terra | Normal coding, debugging, research synthesis, UI implementation, multi-file work from an accepted plan, and long interactive learning sessions | medium; high for interacting failures |
| Sol | Architecture, authority or evidence design, high-risk migration, unresolved cross-system failures, and final adversarial review | high |

Treat Terra medium as the default for this user's typical work. Do not select Sol merely because a task is long. Use `xhigh`, `ultra`, or `max` only for one bounded quality-critical decision or review with explicit success criteria; never use them as an extended implementation default.

If these model names are unavailable, map Luna to the cheapest capable tier, Terra to the balanced production tier, and Sol to the frontier tier.

## Apply the decision gates

1. Use Luna when the outcome is bounded, reversible, and objectively verifiable.
2. Use Terra for implementation with a reasonably clear desired outcome.
3. Try Terra high first for a difficult bug with interacting systems.
4. Use Sol when the task establishes architecture, security, irreversible behavior, authority boundaries, or evidence validity.
5. Downgrade implementation to Terra after Sol produces an accepted decision or plan.
6. Escalate an unresolved evidence packet to Sol after two substantively different validation failures, not after a transient tool or environment failure.

Do not spawn another model solely to answer a short task already in progress; delegation overhead can exceed the savings. When a large task is running on a stronger root model, keep root work to routing, architecture, or review and delegate bounded implementation only when that produces a net saving.

## Control context and subagents

- Use subagents only for independent work that benefits from parallelism or a cheaper execution tier.
- Default to at most two concurrent subagents; use three only when the work has three genuinely independent streams.
- Prefer Luna for mechanical collection or transformation and Terra for implementation or repository analysis. Reserve Sol subagents for independent high-risk review.
- Pass `fork_turns="none"` or the smallest useful recent-turn window plus a compact task packet. Never pass full history unless the subtask materially depends on the conversation itself.
- Include only the goal, constraints, exact files or evidence, expected output, validation, and stopping condition in a task packet.
- At a phase boundary, write or update a durable handoff artifact and recommend a fresh thread instead of carrying a long exploratory history into implementation or verification.

## Report only when useful

Before a large or usage-sensitive task, emit one compact line:

```text
Route — Terra medium · projected 20k–40k input / 3k–6k output · ~2–4 credits · confidence: medium · uncertainty: repository breadth
```

Do not add a routing line to ordinary bounded tasks. Classify projections as measured, calculated, or estimated. When exact rates or account usage matter, follow the `usage-advisor` skill; otherwise avoid telemetry calls made only to choose a route.

## Estimate comparative cost

Calculate credits as:

```text
uncached_input_millions × input_rate
+ cached_input_millions × cached_rate
+ output_millions × output_rate
```

Include expected retries and delegated calls. Prefer representative validation over assuming the strongest model or effort is always best.
