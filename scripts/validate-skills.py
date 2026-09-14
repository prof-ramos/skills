#!/usr/bin/env python3
"""Validate tracked Agent Skill frontmatter used by this repository."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


import json

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
ALLOWED_DIRECTORY_NAME_MISMATCHES: set[str] = set()


def validate_skills_sh_json(root: Path) -> list[str]:
    cfg_path = root / "skills.sh.json"
    if not cfg_path.exists():
        return ["skills.sh.json: missing root configuration file"]

    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"skills.sh.json: invalid JSON - {exc}"]

    errors = []
    if "$schema" not in data:
        errors.append("skills.sh.json: missing '$schema' field")
    if "groupings" not in data or not isinstance(data["groupings"], list):
        errors.append("skills.sh.json: missing or invalid 'groupings' array")
    else:
        for idx, group in enumerate(data["groupings"]):
            if "title" not in group:
                errors.append(f"skills.sh.json: grouping[{idx}] missing 'title'")
            if "skills" not in group or not isinstance(group["skills"], list):
                errors.append(f"skills.sh.json: grouping[{idx}] missing 'skills' list")

    return errors


def tracked_skill_files() -> list[Path]:
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", "ls-files", "-z", "*SKILL.md"],
        check=True,
        capture_output=True,
    )
    files = [
        Path(f.decode("utf-8"))
        for f in result.stdout.split(b"\0")
        if f.strip()
    ]
    return [
        path
        for path in files
        if "docs/reference/official-skills/" not in path.as_posix()
    ]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: missing opening frontmatter marker"]

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return {}, [f"{path}: missing closing frontmatter marker"]

    data: dict[str, str] = {}
    fm = lines[1:end]
    i = 0
    while i < len(fm):
        line = fm[i]
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            i += 1
            continue
        key, raw = match.groups()
        raw = raw.strip()
        if raw in {"|", ">", "|-", ">-"}:
            block: list[str] = []
            i += 1
            while i < len(fm) and (fm[i].startswith(" ") or not fm[i].strip()):
                block.append(fm[i].strip())
                i += 1
            data[key] = " ".join(part for part in block if part).strip()
            continue
        data[key] = raw.strip("\"'")
        i += 1
    return data, []


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    root = Path(__file__).resolve().parents[1]
    failures.extend(validate_skills_sh_json(root))

    files = tracked_skill_files()

    for path in files:
        data, errors = parse_frontmatter(path)
        failures.extend(errors)
        if errors:
            continue

        name = data.get("name", "")
        description = data.get("description", "")
        if not name:
            failures.append(f"{path}: missing required 'name'")
        elif not NAME_RE.match(name):
            failures.append(f"{path}: name must be lowercase kebab-case, got {name!r}")

        if not description:
            failures.append(f"{path}: missing required 'description'")
        elif len(description) > 1024:
            failures.append(f"{path}: description exceeds 1024 characters ({len(description)})")

        normalized_dir = path.parent.name.replace("_", "-").lower()
        path_key = path.as_posix()
        if (
            name
            and normalized_dir not in {name, "skills"}
            and path_key not in ALLOWED_DIRECTORY_NAME_MISMATCHES
            and not path_key.endswith(".claude/skills/run-edital-verticalizado/SKILL.md")
        ):
            warnings.append(f"{path}: directory name {path.parent.name!r} differs from skill name {name!r}")

    for warning in warnings:
        print(f"WARN: {warning}")

    if failures:
        print("Skill validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"Skill frontmatter & skills.sh.json OK ({len(files)} files, {len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
