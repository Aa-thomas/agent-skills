from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_skills", ROOT / "tools" / "validate_skills.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateSkillsTests(unittest.TestCase):
    def test_repository_skills_are_valid(self) -> None:
        errors = [
            error
            for path in sorted((ROOT / "skills").iterdir())
            if path.is_dir()
            for error in VALIDATOR.validate_skill(path)
        ]
        self.assertEqual(errors, [])

    def test_reports_broken_relative_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "example-skill"
            (skill / "agents").mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: example-skill\ndescription: Example.\n---\n\n"
                "[Missing](references/nope.md)\n",
                encoding="utf-8",
            )
            (skill / "agents" / "openai.yaml").write_text(
                'interface:\n  default_prompt: "Use $example-skill now."\n',
                encoding="utf-8",
            )
            self.assertIn(
                "missing linked file", "\n".join(VALIDATOR.validate_skill(skill))
            )

    def test_reports_name_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "example-skill"
            (skill / "agents").mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: wrong-name\ndescription: Example.\n---\n",
                encoding="utf-8",
            )
            (skill / "agents" / "openai.yaml").write_text(
                'interface:\n  default_prompt: "Use $example-skill now."\n',
                encoding="utf-8",
            )
            self.assertIn(
                "name must match", "\n".join(VALIDATOR.validate_skill(skill))
            )


if __name__ == "__main__":
    unittest.main()
