# Bounded demonstrations

Use an interactive demonstration only when changing an input helps the reader
understand a consequential rule. Prefer a small existing fixture, a trace of a
real execution, or a static worked example when that is enough.

## Keep the evidence honest

Label each demonstration as one of:

- **Actual execution:** a named function or harness executed against the stated
  source revision and inputs, with an observed result.
- **Source prediction:** an expected result reasoned from inspected code but not
  executed in this artifact.
- **Illustrative simulation:** a simplified teaching model, not the application.

Reuse a real pure function or existing fixture when practical. Do not create a
second rule engine just to make an explainer interactive. If a standalone HTML
file cannot safely run the real code, use a trace or clearly labeled simulation
and show what was omitted. Do not label an example with made-up domain data as a
real application outcome.

A fake store cannot prove atomicity, conflict handling, or durable idempotency.
Two views displaying the same answer cannot establish runtime parity. Identify
the real-store or integration evidence separately, including missing evidence.

## Bound execution and state

Use isolated, disposable local state. Do not call production services, spend
provider credits, alter learner records, or enable effects merely to explain
code. Follow existing task authorization and repository requirements for any
real execution. Keep secrets and private source out of published artifacts.

Give controls descriptive names, explain the input and visible result, and
provide a reset. Expose the facts that cause the outcome rather than decorating
the page with unrelated motion or dashboard controls. Keep answer state local
to the page unless persistence was explicitly requested.

## Check the useful paths

Check a representative accepted and rejected outcome, repeat/reset behavior,
keyboard operation, and a narrow viewport. Check that source-like text renders
as text without losing whitespace or executing markup. Report precisely which
paths were exercised. Do not add a new framework or broad test suite for a small
teaching artifact, or turn its questions into proof of learner competence.
