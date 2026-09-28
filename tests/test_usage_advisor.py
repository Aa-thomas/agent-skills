from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "usage-advisor"
SPEC = importlib.util.spec_from_file_location(
    "usage_advisor", SKILL / "scripts" / "usage_advisor.py"
)
assert SPEC and SPEC.loader
USAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(USAGE)


def cache_payload(age: timedelta = timedelta()) -> dict:
    measured = datetime.now(tz=timezone.utc) - age
    return {
        "classification": "measured_account_telemetry",
        "cached_at": measured.isoformat().replace("+00:00", "Z"),
        "weekly": {
            "remaining_percent": 42,
            "resets_at": (measured + timedelta(days=2)).isoformat().replace(
                "+00:00", "Z"
            ),
        },
    }


class UsageAdvisorTests(unittest.TestCase):
    def run_script(
        self, script: str, *arguments: str, stdin: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SKILL / "scripts" / script), *arguments],
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_footer_uses_fresh_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "weekly.json"
            cache.write_text(json.dumps(cache_payload()), encoding="utf-8")
            result = self.run_script(
                "footer.py",
                "--cache-file",
                str(cache),
                "--timezone",
                "UTC",
            )
            self.assertEqual(result.returncode, 0)
            self.assertRegex(result.stdout, r"^Usage — weekly: 42% remaining · ")
            self.assertEqual(len(result.stdout.splitlines()), 1)

    def test_footer_suppresses_stale_and_malformed_cache(self) -> None:
        expected = (
            "Usage — weekly: unavailable · updated: stale cache · "
            "resets: unavailable\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "weekly.json"
            cache.write_text(
                json.dumps(cache_payload(timedelta(hours=1))), encoding="utf-8"
            )
            stale = self.run_script("footer.py", "--cache-file", str(cache))
            self.assertEqual(stale.stdout, expected)
            cache.write_text("{", encoding="utf-8")
            malformed = self.run_script("footer.py", "--cache-file", str(cache))
            self.assertEqual(malformed.stdout, expected)

    def test_cached_weekly_marks_stale_data_without_discarding_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "weekly.json"
            cache.write_text(
                json.dumps(cache_payload(timedelta(hours=1))), encoding="utf-8"
            )
            result = self.run_script(
                "usage_advisor.py",
                "cached-weekly",
                "--cache-file",
                str(cache),
                "--max-age",
                "900",
            )
            self.assertEqual(result.returncode, 0)
            self.assertTrue(json.loads(result.stdout)["stale"])

    def test_cache_write_is_atomic_private_and_selective(self) -> None:
        matching = {
            "buckets": [
                {
                    "limit_id": "codex",
                    "window_duration_minutes": 10080,
                    "remaining_percent": 42,
                }
            ]
        }
        other = {
            "buckets": [
                {
                    "limit_id": "other",
                    "window_duration_minutes": 10080,
                }
            ]
        }
        self.assertEqual(USAGE.select_general_weekly(matching)["remaining_percent"], 42)
        self.assertIsNone(USAGE.select_general_weekly(other))
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "weekly.json"
            USAGE.write_weekly_cache(str(cache), matching["buckets"][0])
            self.assertEqual(os.stat(cache).st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(cache.read_text())["weekly"]["remaining_percent"], 42)

    def test_hook_ignores_non_user_events(self) -> None:
        result = self.run_script(
            "inject_weekly.py",
            stdin=json.dumps({"hook_event_name": "PostToolUse"}),
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
