# Ticket-writing workflow cases

These cases define release behavior for `to-tickets`.

| Case | Expected behavior |
| --- | --- |
| Approved plan with configured tracker | Inspect relevant code, propose grounded vertical slices, reuse approval, and publish only to the configured destination. |
| No configured destination | Draft the breakdown in the response and identify the missing destination without assuming `/setup-matt-pocock-skills` exists. |
| Named reuse candidate cannot be inspected | Mark it unverified and avoid making its path or contract an implementation requirement. |
| Required product decision unresolved | Keep affected tickets blocked or proposed and name the decision needed. |
| Approved breakdown rewritten without material scope or edge changes | Preserve approval rather than repeating the quiz. |
| Wide mechanical migration | Use expand–migrate–contract batches when vertical slices cannot independently stay green. |
| Publication times out | Read back the tracker before retrying; do not create duplicates from an uncertain response. |
| Existing matching tickets | Reconcile the approved plan with existing identifiers instead of publishing duplicates. |
