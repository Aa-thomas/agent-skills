#!/usr/bin/env python3
"""Inject fresh weekly-usage data into a Codex UserPromptSubmit turn."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


def compact_age(seconds: float) -> str:
    if seconds < 60:
        return f"{round(seconds)}s"
    if seconds < 3600:
        return f"{round(seconds / 60)}m"
    return f"{round(seconds / 3600, 1)}h"


def reset_label(value: str, timezone_name: str) -> str:
    reset = datetime.fromisoformat(value.replace("Z", "+00:00"))
    local = reset.astimezone(ZoneInfo(timezone_name))
    hour = local.strftime("%I").lstrip("0") or "0"
    return f"{local.strftime('%b')} {local.day} {hour}:{local.strftime('%M')} {local.strftime('%p')} {local.tzname()}"


def measured_label(value: str, timezone_name: str) -> str:
    measured = datetime.fromisoformat(value.replace("Z", "+00:00"))
    local = measured.astimezone(ZoneInfo(timezone_name))
    hour = local.strftime("%I").lstrip("0") or "0"
    return f"{local.strftime('%b')} {local.day} {hour}:{local.strftime('%M')} {local.strftime('%p')} {local.tzname()}"


def hook_output(context: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-file", default="~/.codex/usage-advisor/weekly.json")
    parser.add_argument("--max-age", type=float, default=900)
    parser.add_argument("--timezone", default="America/Toronto")
    args = parser.parse_args()

    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        event = {}
    if event.get("hook_event_name") not in (None, "UserPromptSubmit"):
        return 0

    path = Path(args.cache_file).expanduser()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        weekly = payload["weekly"]
        cached_at = datetime.fromisoformat(payload["cached_at"].replace("Z", "+00:00"))
        age_seconds = max(0, (datetime.now(tz=timezone.utc) - cached_at).total_seconds())
        if age_seconds > args.max_age:
            context = (
                f"USAGE_DATA unavailable reason=stale_cache cache_age={compact_age(age_seconds)}. "
                "Do not present a weekly remaining percentage as measured."
            )
        else:
            context = (
                f"USAGE_DATA weekly_remaining={weekly['remaining_percent']}% classification=measured "
                f"measured_at=\"{measured_label(payload['cached_at'], args.timezone)}\" "
                f"reset=\"{reset_label(weekly['resets_at'], args.timezone)}\" "
                f"cache_age={compact_age(age_seconds)} stale=false. "
                "Use this data in the required Usage footer; do not call telemetry tools."
            )
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError, OSError) as exc:
        context = f"USAGE_DATA unavailable reason={type(exc).__name__}. Do not call telemetry tools."

    print(json.dumps(hook_output(context), separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
