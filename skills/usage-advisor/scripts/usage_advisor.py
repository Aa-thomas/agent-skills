#!/usr/bin/env python3
"""Estimate text usage, project Codex credits, or query Codex account telemetry."""

from __future__ import annotations

import argparse
import json
import os
import selectors
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
RATES_PATH = ROOT / "references" / "rates.json"


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def estimated_tokens(text: str) -> int:
    if not text:
        return 0
    utf8_bytes = len(text.encode("utf-8"))
    words = len(text.split())
    # English prose is often near four bytes per token; code and punctuation
    # tokenize more densely. Blend byte- and word-based estimates.
    return max(1, round((utf8_bytes / 4.0) * 0.7 + (words / 0.75) * 0.3))


def load_rates() -> dict:
    return json.loads(RATES_PATH.read_text(encoding="utf-8"))


def command_count(args: argparse.Namespace) -> int:
    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    if text is None:
        text = sys.stdin.read()
    emit(
        {
            "classification": "estimated",
            "estimated_tokens": estimated_tokens(text),
            "visible_utf8_bytes": len(text.encode("utf-8")),
            "limitations": [
                "Tokenizer-independent heuristic; not an authoritative model count.",
                "Excludes hidden instructions, reasoning, tools, retries, and prior context."
            ],
        }
    )
    return 0


def credits(rate: dict, input_tokens: float, output_tokens: float, cached_fraction: float) -> float:
    cached = input_tokens * cached_fraction
    uncached = input_tokens - cached
    return (
        uncached * rate["input"]
        + cached * rate["cached_input"]
        + output_tokens * rate["output"]
    ) / 1_000_000


def command_project(args: argparse.Namespace) -> int:
    table = load_rates()
    model = args.model.lower()
    if model not in table["models"]:
        emit({"error": f"No fallback rate for {args.model}", "known_models": sorted(table["models"])})
        return 2
    if not 0 <= args.cached_fraction <= 1:
        emit({"error": "--cached-fraction must be between 0 and 1"})
        return 2
    if min(args.input_min, args.input_max, args.output_min, args.output_max) < 0:
        emit({"error": "Token ranges cannot be negative"})
        return 2
    if args.input_min > args.input_max or args.output_min > args.output_max:
        emit({"error": "Minimum token values cannot exceed maximum values"})
        return 2
    rate = table["models"][model]
    low = credits(rate, args.input_min, args.output_min, args.cached_fraction)
    high = credits(rate, args.input_max, args.output_max, args.cached_fraction)
    emit(
        {
            "classification": "calculated_from_estimated_token_ranges",
            "model": model,
            "tokens": {
                "input": [args.input_min, args.input_max],
                "output": [args.output_min, args.output_max],
                "assumed_cached_input_fraction": args.cached_fraction,
            },
            "projected_credits": [round(low, 3), round(high, 3)],
            "rates_as_of": table["as_of"],
            "rate_source": table["source"],
            "limitations": table["notes"],
        }
    )
    return 0


def rpc_send(proc: subprocess.Popen[str], payload: dict) -> None:
    assert proc.stdin is not None
    proc.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
    proc.stdin.flush()


def read_stderr_nonblocking(proc: subprocess.Popen[str], limit: int = 2000) -> str:
    """Read currently available stderr without waiting for the child to exit."""
    if proc.stderr is None:
        return ""
    descriptor = proc.stderr.fileno()
    was_blocking = os.get_blocking(descriptor)
    try:
        os.set_blocking(descriptor, False)
        return os.read(descriptor, limit).decode(errors="replace")
    except (OSError, ValueError):
        return ""
    finally:
        try:
            os.set_blocking(descriptor, was_blocking)
        except OSError:
            pass


def iso_timestamp(value: object) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def summarize_rate_limits(result: object) -> object:
    if not isinstance(result, dict):
        return result
    buckets = result.get("rateLimitsByLimitId")
    if not isinstance(buckets, dict):
        single = result.get("rateLimits")
        buckets = {single.get("limitId", "default"): single} if isinstance(single, dict) else {}
    summary = []
    for limit_id, bucket in buckets.items():
        if not isinstance(bucket, dict):
            continue
        primary = bucket.get("primary") if isinstance(bucket.get("primary"), dict) else {}
        used = primary.get("usedPercent")
        credits_data = bucket.get("credits") if isinstance(bucket.get("credits"), dict) else {}
        summary.append(
            {
                "limit_id": limit_id,
                "limit_name": bucket.get("limitName"),
                "plan_type": bucket.get("planType"),
                "used_percent": used,
                "remaining_percent": round(100 - used, 3) if isinstance(used, (int, float)) else None,
                "window_duration_minutes": primary.get("windowDurationMins"),
                "resets_at": iso_timestamp(primary.get("resetsAt")),
                "rate_limit_reached_type": bucket.get("rateLimitReachedType"),
                "credit_balance": credits_data.get("balance"),
                "has_credits": credits_data.get("hasCredits"),
                "unlimited_credits": credits_data.get("unlimited"),
            }
        )
    reset_credits = result.get("rateLimitResetCredits")
    return {
        "buckets": summary,
        "available_reset_credits": reset_credits.get("availableCount") if isinstance(reset_credits, dict) else None,
    }


def summarize_account_usage(result: object, include_daily: bool) -> object:
    if not isinstance(result, dict):
        return result
    output = {"summary": result.get("summary")}
    buckets = result.get("dailyUsageBuckets")
    if include_daily:
        output["daily_usage_buckets"] = buckets
    elif isinstance(buckets, list) and buckets:
        output["latest_daily_bucket"] = buckets[-1]
    return output


def select_general_weekly(rate_limits: object) -> dict | None:
    if not isinstance(rate_limits, dict):
        return None
    for bucket in rate_limits.get("buckets", []):
        if (
            isinstance(bucket, dict)
            and bucket.get("limit_id") == "codex"
            and bucket.get("window_duration_minutes") == 10080
        ):
            return bucket
    return None


def write_weekly_cache(path: str, weekly: dict) -> None:
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "classification": "measured_account_telemetry",
        "cached_at": datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        "weekly": weekly,
    }
    temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, target)


USAGE_BLOCK_START = "<!-- usage-advisor:start -->"
USAGE_BLOCK_END = "<!-- usage-advisor:end -->"


def local_label(value: str, timezone_name: str = "America/Toronto") -> str:
    moment = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(ZoneInfo(timezone_name))
    hour = moment.strftime("%I").lstrip("0") or "0"
    return f"{moment.strftime('%b')} {moment.day} {hour}:{moment.strftime('%M')} {moment.strftime('%p')} {moment.tzname()}"


def update_agents_usage(path: str, weekly: dict) -> None:
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    measured_at = datetime.now(tz=timezone.utc).astimezone(ZoneInfo("America/Toronto"))
    measured_hour = measured_at.strftime("%I").lstrip("0") or "0"
    measured_label = (
        f"{measured_at.strftime('%b')} {measured_at.day} "
        f"{measured_hour}:{measured_at.strftime('%M')} {measured_at.strftime('%p')} {measured_at.tzname()}"
    )
    block = "\n".join(
        [
            USAGE_BLOCK_START,
            (
                f"- `WEEKLY_USAGE`: {weekly['remaining_percent']}% remaining (measured {measured_label}); "
                f"resets {local_label(weekly['resets_at'])}."
            ),
            USAGE_BLOCK_END,
        ]
    )
    try:
        original = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        original = "# Personal usage awareness\n"
    start = original.find(USAGE_BLOCK_START)
    end = original.find(USAGE_BLOCK_END)
    if start >= 0 and end >= start:
        end += len(USAGE_BLOCK_END)
        updated = original[:start] + block + original[end:]
    else:
        updated = original.rstrip() + "\n\n" + block + "\n"
    temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    temporary.write_text(updated, encoding="utf-8")
    if target.exists():
        temporary.chmod(target.stat().st_mode & 0o777)
    else:
        temporary.chmod(0o600)
    os.replace(temporary, target)


def command_cached_weekly(args: argparse.Namespace) -> int:
    path = Path(args.cache_file).expanduser()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cached_at = datetime.fromisoformat(payload["cached_at"].replace("Z", "+00:00"))
        age = max(0, (datetime.now(tz=timezone.utc) - cached_at).total_seconds())
        payload["cache_age_seconds"] = round(age)
        payload["stale"] = age > args.max_age
        payload["cache_file"] = str(path)
        emit(payload)
        return 0
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError) as exc:
        emit({"available": False, "classification": "unavailable", "cache_file": str(path), "error": str(exc)})
        return 1


def command_telemetry(args: argparse.Namespace) -> int:
    # Account reads do not need the caller's persistent thread database. Use an
    # isolated writable state directory so this command works in read-only and
    # workspace-write sandboxes without requesting access to ~/.codex.
    state_dir = tempfile.mkdtemp(prefix="usage-advisor-state-")
    isolated_home = Path(state_dir) / "codex-home"
    work_dir = Path(state_dir) / "work"
    isolated_home.mkdir(mode=0o700)
    work_dir.mkdir(mode=0o700)
    (work_dir / ".codex").mkdir(mode=0o700)
    source_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    source_auth = source_home / "auth.json"
    if source_auth.is_file():
        shutil.copy2(source_auth, isolated_home / "auth.json")
    child_env = os.environ.copy()
    child_env["CODEX_HOME"] = str(isolated_home)
    command = [
        args.codex_binary,
        "app-server",
        "--stdio",
        "-c",
        f'sqlite_home="{state_dir}"',
    ]
    try:
        proc = subprocess.Popen(
            command,
            cwd=work_dir,
            env=child_env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
    except (FileNotFoundError, OSError) as exc:
        shutil.rmtree(state_dir, ignore_errors=True)
        emit({"available": False, "classification": "unavailable", "error": str(exc)})
        return 1

    responses: dict[int, dict] = {}
    deadline = time.monotonic() + args.timeout
    try:
        rpc_send(
            proc,
            {
                "method": "initialize",
                "id": 1,
                "params": {
                    "clientInfo": {"name": "usage_advisor", "title": "Usage Advisor", "version": "0.1.0"},
                    "capabilities": {},
                },
            },
        )
        assert proc.stdout is not None
        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ)

        initialized = False
        expected_ids = {1, 2} if args.weekly_only else {1, 2, 3}
        while time.monotonic() < deadline and not expected_ids.issubset(responses):
            events = selector.select(max(0, min(0.25, deadline - time.monotonic())))
            if not events:
                if proc.poll() is not None:
                    break
                continue
            line = proc.stdout.readline()
            if not line:
                break
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(message.get("id"), int):
                responses[message["id"]] = message
            if 1 in responses and not initialized:
                if "error" in responses[1]:
                    break
                rpc_send(proc, {"method": "initialized", "params": {}})
                rpc_send(proc, {"method": "account/rateLimits/read", "id": 2, "params": {}})
                if not args.weekly_only:
                    rpc_send(proc, {"method": "account/usage/read", "id": 3, "params": {}})
                initialized = True

        rate_result = responses.get(2, {}).get("result")
        usage_result = responses.get(3, {}).get("result")
        summarized_limits = summarize_rate_limits(rate_result)
        if args.weekly_only and isinstance(summarized_limits, dict):
            summarized_limits = {
                "buckets": [
                    bucket
                    for bucket in summarized_limits.get("buckets", [])
                    if bucket.get("window_duration_minutes") == 10080
                ],
                "available_reset_credits": summarized_limits.get("available_reset_credits"),
            }
        available = rate_result is not None if args.weekly_only else (rate_result is not None or usage_result is not None)
        output = {
            "available": available,
            "classification": "measured_account_telemetry" if available else "unavailable",
            "rate_limits": rate_result if args.raw else summarized_limits,
            "account_usage": usage_result if args.raw else summarize_account_usage(usage_result, args.daily),
            "errors": [responses[i]["error"] for i in sorted(responses) if "error" in responses[i]],
        }
        if not output["available"]:
            stderr = read_stderr_nonblocking(proc)
            output["error"] = stderr.strip() or "Codex app-server did not return telemetry before timeout."
        elif args.cache_file:
            weekly = select_general_weekly(summarized_limits)
            if weekly is not None:
                write_weekly_cache(args.cache_file, weekly)
                output["cache_file"] = str(Path(args.cache_file).expanduser())
                if args.agents_file:
                    update_agents_usage(args.agents_file, weekly)
                    output["agents_file"] = str(Path(args.agents_file).expanduser())
        emit(output)
        return 0 if output["available"] else 1
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                proc.kill()
                try:
                    proc.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    pass
        shutil.rmtree(state_dir, ignore_errors=True)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)

    count = sub.add_parser("count", help="Estimate tokens in visible text")
    source = count.add_mutually_exclusive_group()
    source.add_argument("--text")
    source.add_argument("--file")
    count.set_defaults(func=command_count)

    project = sub.add_parser("project", help="Calculate a credit range from projected tokens")
    project.add_argument("--model", required=True)
    project.add_argument("--input-min", type=int, required=True)
    project.add_argument("--input-max", type=int, required=True)
    project.add_argument("--output-min", type=int, required=True)
    project.add_argument("--output-max", type=int, required=True)
    project.add_argument("--cached-fraction", type=float, default=0.0)
    project.set_defaults(func=command_project)

    telemetry = sub.add_parser("telemetry", help="Read authenticated Codex account telemetry")
    telemetry.add_argument("--codex-binary", default=os.environ.get("CODEX_BINARY", "codex"))
    telemetry.add_argument("--timeout", type=float, default=8.0)
    telemetry.add_argument("--daily", action="store_true", help="Include all daily usage buckets")
    telemetry.add_argument("--raw", action="store_true", help="Return the full app-server responses")
    telemetry.add_argument("--weekly-only", action="store_true", help="Fetch only weekly rate-limit buckets")
    telemetry.add_argument("--cache-file", help="Write the measured general weekly bucket to this cache file")
    telemetry.add_argument("--agents-file", help="Refresh a marked WEEKLY_USAGE block in this AGENTS.md")
    telemetry.set_defaults(func=command_telemetry)

    cached = sub.add_parser("cached-weekly", help="Read the most recently refreshed weekly-usage cache")
    cached.add_argument("--cache-file", default="~/.codex/usage-advisor/weekly.json")
    cached.add_argument("--max-age", type=float, default=900)
    cached.set_defaults(func=command_cached_weekly)
    return result


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
