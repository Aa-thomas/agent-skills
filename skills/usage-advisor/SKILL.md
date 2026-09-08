---
name: usage-advisor
description: Track, explain, and forecast Codex token and credit usage. Use when the user asks about available usage, rate-limit windows, credits, context consumption, per-message or per-turn token counts, or projected cost for a large request or plan.
---

# Usage Advisor

Classify every number as measured, calculated, or estimated.

## Ordinary turns

Run `scripts/footer.py` immediately before every user-visible assistant message, including progress updates and the final answer, and use its exact one-line output. It reads the shared local cache and is the cross-session source of truth. A timer refreshes that cache every five minutes; the footer command does not call account telemetry.

Append one compact footer when global guidance requests it. Do not include per-message token counts when the global guidance requests the simplified footer:

```text
Usage — weekly: 96% remaining · updated: Aug 28 9:32 AM EDT · resets: Aug 28 9:37 AM EDT
```

Never substitute a remembered value, an earlier footer, or an instruction snapshot for the helper output.

## Large-task projection

Forecast billable input and output across all expected model calls. State the cached-input assumption, credit range, confidence, and main uncertainty. Prefer current official rates; use `references/rates.json` only as a dated fallback.

## Manual diagnostics

```bash
python3 scripts/usage_advisor.py cached-weekly
python3 scripts/footer.py
python3 scripts/usage_advisor.py telemetry --weekly-only \
  --cache-file ~/.codex/usage-advisor/weekly.json \
  --agents-file ~/.codex/AGENTS.md
```

Do not equate context-window occupancy, goal budgets, lifetime tokens, or raw visible-message length with account quota.
