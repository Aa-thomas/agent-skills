#!/usr/bin/env python3
"""Print the current compact Codex weekly-usage footer from the local cache."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


def local_label(value: str, timezone_name: str) -> str:
    moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    local = moment.astimezone(ZoneInfo(timezone_name))
    hour = local.strftime("%I").lstrip("0") or "0"
    return (
        f"{local.strftime('%b')} {local.day} {hour}:{local.strftime('%M')} "
        f"{local.strftime('%p')} {local.tzname()}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-file", default="~/.codex/usage-advisor/weekly.json")
    parser.add_argument("--max-age", type=float, default=900)
    parser.add_argument("--timezone", default="America/Toronto")
    args = parser.parse_args()

    try:
        payload = json.loads(Path(args.cache_file).expanduser().read_text(encoding="utf-8"))
        cached_at = datetime.fromisoformat(payload["cached_at"].replace("Z", "+00:00"))
        age = max(0, (datetime.now(tz=timezone.utc) - cached_at).total_seconds())
        if age > args.max_age:
            raise ValueError("stale cache")
        weekly = payload["weekly"]
        print(
            f"Usage — weekly: {weekly['remaining_percent']}% remaining · "
            f"updated: {local_label(payload['cached_at'], args.timezone)} · "
            f"resets: {local_label(weekly['resets_at'], args.timezone)}"
        )
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError, OSError):
        print("Usage — weekly: unavailable · updated: stale cache · resets: unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
