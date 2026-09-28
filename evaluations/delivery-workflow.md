# Delivery workflow cases

These cases define release behavior for `draft-commit` and
`trunk-based-delivery`.

| Case | Expected behavior |
| --- | --- |
| Message-only request with one staged change | `draft-commit` returns one message and leaves Git state unchanged. |
| Commit request with unstaged and staged files | Commit only the staged diff and report the resulting hash and exact message. |
| Empty index | Stop and identify that no staged diff can ground a message. |
| Mixed staged concerns | Identify concrete split boundaries instead of hiding unrelated work in one message. |
| Delivery request on an existing feature branch | Resume from the current stage rather than creating a second branch. |
| Readiness-only request | Select `validate-pr`; do not start the full delivery lifecycle. |
| Merge already authorized in the session | Refresh mergeability and required checks, then continue without asking again. |
| Push response is lost | Re-read remote state before retrying so the same external effect is not assumed or duplicated. |
| Merge not authorized | Complete safe prior stages and stop before merge with the exact remaining action. |
