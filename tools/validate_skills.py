#!/usr/bin/env python3
"""Validate portable structure and local references for every published skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def scalar(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return [f"{skill_file}: invalid or missing YAML frontmatter"]

    frontmatter = match.group("body")
    name = scalar(frontmatter, "name")
    description = scalar(frontmatter, "description")
    if name != skill_dir.name:
        errors.append(f"{skill_file}: name must match directory {skill_dir.name!r}")
    if not name or not NAME.fullmatch(name):
        errors.append(f"{skill_file}: invalid skill name")
    if not description or len(description) > 1024:
        errors.append(f"{skill_file}: description must contain 1-1024 characters")

    metadata = skill_dir / "agents" / "openai.yaml"
    if not metadata.is_file():
        errors.append(f"{metadata}: missing interface metadata")
    else:
        metadata_text = metadata.read_text(encoding="utf-8")
        if f"${skill_dir.name}" not in metadata_text:
            errors.append(f"{metadata}: default prompt must mention ${skill_dir.name}")

    for source in skill_dir.rglob("*.md"):
        source_text = source.read_text(encoding="utf-8")
        for target in LINK.findall(source_text):
            clean = target.split("#", 1)[0]
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (source.parent / clean).resolve()
            if not resolved.exists():
                errors.append(f"{source}: missing linked file {target!r}")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skills = root / "skills"
    if not skills.is_dir():
        print(f"error: {skills} does not exist", file=sys.stderr)
        return 2

    errors = [
        error
        for path in sorted(skills.iterdir())
        if path.is_dir()
        for error in validate_skill(path)
    ]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {sum(path.is_dir() for path in skills.iterdir())} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
