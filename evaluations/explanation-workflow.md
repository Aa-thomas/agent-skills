# Explanation workflow cases

These cases define release behavior for `explain-code`.

| Case | Expected behavior |
| --- | --- |
| Focused function question | Explain one concrete input through decisions, effects, result, and failure path without producing a large artifact. |
| Pull request walkthrough | Identify base and head, explain the full behavior change, map plausible next changes, compare consequential alternatives, and check a strong claim against source evidence. |
| Migration slice | Distinguish current and target owners, intentional behavior changes, caller routing, and remaining cutover work. |
| Unavailable source or revision | Name the unavailable evidence and stop before presenting inferred behavior as source-inspected. |
| Hypothetical next requirement | Mark proposed locations as proposed and distinguish required edits from boundaries that only need checking. |
| Existing tests but no observed run | Cite the protection the tests appear to provide and state that execution was not observed. |
| PR-readiness request | Select `validate-pr`; do not substitute an explanation for a readiness verdict. |
