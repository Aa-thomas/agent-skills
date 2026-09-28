# Cost and usage workflow cases

These cases define release behavior for `model-router` and `usage-advisor`.

| Case | Expected behavior |
| --- | --- |
| Ordinary bounded task | Do not add routing overhead or a route report. |
| Large implementation with supported tiers | Choose the lowest reliable tier, project ranges, and state confidence and the main uncertainty. |
| Preferred model or delegation unavailable | Map to available capability or continue locally; do not stall the task or invent availability. |
| No current credit rate | Report token ranges and say the credit rate is unavailable. |
| Fresh valid weekly cache | Print measured percentage, measurement time, and reset time in one footer line. |
| Stale, missing, malformed, unreadable, or timezone-invalid cache | Print the exact unavailable footer without reusing an older percentage. |
| Telemetry lacks the general Codex weekly bucket | Preserve the old cache and return `weekly_cache_updated: false` with a reason. |
| Non-user hook event | Produce no injected context. |
