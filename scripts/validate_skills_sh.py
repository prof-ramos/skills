#!/usr/bin/env python3
"""Deterministic validator for skills.sh.json schema and repository parity.

Conforms strictly to https://skills.sh/schemas/skills.sh.schema.json and ensures
100% parity with physical SKILL.md files in the repository.
Zero external dependencies (standard library only).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Schema definition constants
ALLOWED_ROOT_PROPERTIES = {"$schema", "schema", "notGrouped", "groupings"}
ALLOWED_GROUP_PROPERTIES = {"title", "description", "skills"}
ALLOWED_NOT_GROUPED = {"top", "bottom"}

# Directories excluded from physical skill discovery
DEFAULT_IGNORE_DIRS = {
    ".git",
    ".agents",
    "node_modules",
    ".verboo",
    ".venv",
    "venv",
    "__pycache__",
    ".gemini",
}

# Explicitly exempt non-skill template files
EXEMPT_SKILL_PATHS = {
    "docs/reference/official-skills/template/SKILL.md",
}


def parse_frontmatter(path: Path) -> Tuple[Dict[str, str], Optional[str]]:
    """Parse YAML frontmatter from a SKILL.md file without external dependencies.

    Returns:
        (data_dict, error_message)
    """
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:
        return {}, f"Could not read file {path}: {exc}"

    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, f"Missing opening '---' frontmatter marker in {path}"

    end_idx = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return {}, f"Missing closing '---' frontmatter marker in {path}"

    fm_lines = lines[1:end_idx]
    data: Dict[str, str] = {}
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            i += 1
            continue

        key, raw_val = match.groups()
        raw_val = raw_val.strip()

        # Handle YAML multiline block scalars: |, >, |-, >-
        if raw_val in {"|", ">", "|-", ">-"}:
            block: List[str] = []
            i += 1
            while i < len(fm_lines) and (fm_lines[i].startswith(" ") or not fm_lines[i].strip()):
                block.append(fm_lines[i].strip())
                i += 1
            data[key] = " ".join(part for part in block if part).strip()
            continue

        # Handle quoted or unquoted scalars
        data[key] = raw_val.strip("\"'")
        i += 1

    return data, None


def discover_physical_skills(
    repo_root: Path,
    ignore_dirs: Optional[Set[str]] = None,
) -> Tuple[Dict[str, List[Dict[str, Any]]], List[str]]:
    """Recursively discover all physical SKILL.md files in repository.

    Returns:
        (skills_by_name, discovery_errors)
        where skills_by_name maps slug -> list of metadata dicts.
    """
    if ignore_dirs is None:
        ignore_dirs = DEFAULT_IGNORE_DIRS

    skills_by_name: Dict[str, List[Dict[str, Any]]] = {}
    errors: List[str] = []

    for root_dir, dirs, files in os.walk(repo_root):
        # Prune ignored directories in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for fname in files:
            if fname == "SKILL.md":
                full_path = Path(root_dir) / fname
                try:
                    rel_path = full_path.relative_to(repo_root).as_posix()
                except ValueError:
                    rel_path = full_path.as_posix()

                if rel_path in EXEMPT_SKILL_PATHS:
                    continue

                fm_data, fm_err = parse_frontmatter(full_path)
                if fm_err:
                    errors.append(fm_err)
                    continue

                name = fm_data.get("name")
                if not name:
                    errors.append(f"Physical skill missing 'name' in frontmatter: {rel_path}")
                    continue

                leaf_dir = full_path.parent.name
                skill_info = {
                    "full_path": full_path,
                    "rel_path": rel_path,
                    "leaf_dir": leaf_dir,
                    "fm_name": name,
                    "frontmatter": fm_data,
                }
                skills_by_name.setdefault(name, []).append(skill_info)

    return skills_by_name, errors


def validate_schema_and_parity(
    config_path: Path,
    repo_root: Path,
    strict: bool = False,
) -> Dict[str, Any]:
    """Execute complete schema and repository parity validation."""
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Verify existence and load skills.sh.json
    if not config_path.is_file():
        return {
            "valid": False,
            "groupingsCount": 0,
            "maxSkillsPerGroup": 0,
            "emptyTitles": 0,
            "duplicates": 0,
            "slugParity": 0.0,
            "totalDeclaredSkills": 0,
            "totalPhysicalSkills": 0,
            "missingPhysicalCount": 0,
            "directoryMismatchCount": 0,
            "errors": [f"Config file not found: {config_path}"],
            "warnings": [],
        }

    try:
        raw_text = config_path.read_text(encoding="utf-8")
        data = json.loads(raw_text)
    except Exception as exc:
        return {
            "valid": False,
            "groupingsCount": 0,
            "maxSkillsPerGroup": 0,
            "emptyTitles": 0,
            "duplicates": 0,
            "slugParity": 0.0,
            "totalDeclaredSkills": 0,
            "totalPhysicalSkills": 0,
            "missingPhysicalCount": 0,
            "directoryMismatchCount": 0,
            "errors": [f"Invalid JSON in {config_path}: {exc}"],
            "warnings": [],
        }

    if not isinstance(data, dict):
        return {
            "valid": False,
            "groupingsCount": 0,
            "maxSkillsPerGroup": 0,
            "emptyTitles": 0,
            "duplicates": 0,
            "slugParity": 0.0,
            "totalDeclaredSkills": 0,
            "totalPhysicalSkills": 0,
            "missingPhysicalCount": 0,
            "directoryMismatchCount": 0,
            "errors": ["Root of skills.sh.json must be a JSON object"],
            "warnings": [],
        }

    # 2. Root additionalProperties check
    for key in data.keys():
        if key not in ALLOWED_ROOT_PROPERTIES:
            errors.append(
                f"Root object contains unexpected property '{key}' "
                f"(allowed: {sorted(ALLOWED_ROOT_PROPERTIES)})"
            )

    # 3. notGrouped enum check
    if "notGrouped" in data:
        not_grouped = data["notGrouped"]
        if not isinstance(not_grouped, str) or not_grouped not in ALLOWED_NOT_GROUPED:
            errors.append(
                f"'notGrouped' must be one of {sorted(ALLOWED_NOT_GROUPED)}, got {not_grouped!r}"
            )

    # 4. groupings array bounds check (1 to 50)
    if "groupings" not in data:
        errors.append("Missing required root property 'groupings'")
        groupings = []
    elif not isinstance(data["groupings"], list):
        errors.append("'groupings' must be an array")
        groupings = []
    else:
        groupings = data["groupings"]
        if len(groupings) < 1:
            errors.append(f"'groupings' must contain at least 1 item, got {len(groupings)}")
        elif len(groupings) > 50:
            errors.append(f"'groupings' exceeds maximum limit of 50 items, got {len(groupings)}")

    groupings_count = len(groupings)
    max_skills_in_group = 0
    empty_titles_count = 0
    duplicate_count = 0

    all_declared_slugs: Dict[str, Set[int]] = {}  # slug -> set of group indices

    for idx, group in enumerate(groupings):
        if not isinstance(group, dict):
            errors.append(f"groupings[{idx}]: item must be a JSON object")
            continue

        # Group additionalProperties check
        for gkey in group.keys():
            if gkey not in ALLOWED_GROUP_PROPERTIES:
                errors.append(
                    f"groupings[{idx}]: unexpected property '{gkey}' "
                    f"(allowed: {sorted(ALLOWED_GROUP_PROPERTIES)})"
                )

        # Required 'title' check
        if "title" not in group:
            errors.append(f"groupings[{idx}]: missing required property 'title'")
            empty_titles_count += 1
            title = ""
        else:
            title = group["title"]
            if not isinstance(title, str):
                errors.append(f"groupings[{idx}]: 'title' must be a string")
                empty_titles_count += 1
            elif not title.strip():
                errors.append(f"groupings[{idx}]: 'title' cannot be empty or blank")
                empty_titles_count += 1
            elif len(title) > 120:
                errors.append(f"groupings[{idx}]: 'title' exceeds 120 characters ({len(title)} chars)")

        # Optional 'description' check
        if "description" in group:
            desc = group["description"]
            if not isinstance(desc, str):
                errors.append(f"groupings[{idx}] ('{title}'): 'description' must be a string")
            elif len(desc) > 500:
                errors.append(
                    f"groupings[{idx}] ('{title}'): 'description' exceeds 500 characters "
                    f"({len(desc)} chars)"
                )

        # Required 'skills' check (1 to 500)
        if "skills" not in group:
            errors.append(f"groupings[{idx}] ('{title}'): missing required property 'skills'")
            skills_list = []
        elif not isinstance(group["skills"], list):
            errors.append(f"groupings[{idx}] ('{title}'): 'skills' must be an array")
            skills_list = []
        else:
            skills_list = group["skills"]
            if len(skills_list) < 1:
                errors.append(f"groupings[{idx}] ('{title}'): 'skills' array must contain at least 1 item")
            elif len(skills_list) > 500:
                errors.append(
                    f"groupings[{idx}] ('{title}'): 'skills' array exceeds maximum limit of 500 items "
                    f"({len(skills_list)} items)"
                )

        if len(skills_list) > max_skills_in_group:
            max_skills_in_group = len(skills_list)

        group_slugs_seen: Set[str] = set()
        for sidx, slug in enumerate(skills_list):
            if not isinstance(slug, str):
                errors.append(f"groupings[{idx}] ('{title}').skills[{sidx}]: skill must be a string")
                continue
            if not (1 <= len(slug) <= 120):
                errors.append(
                    f"groupings[{idx}] ('{title}').skills[{sidx}]: skill slug length must be "
                    f"1-120 chars: '{slug}'"
                )

            # Duplicate within same group
            if slug in group_slugs_seen:
                errors.append(f"groupings[{idx}] ('{title}'): duplicate skill '{slug}' declared within group")
                duplicate_count += 1
            else:
                group_slugs_seen.add(slug)

            all_declared_slugs.setdefault(slug, set()).add(idx)

    # Duplicate across groups
    for slug, group_indices in all_declared_slugs.items():
        if len(group_indices) > 1:
            sorted_indices = sorted(group_indices)
            group_titles = [f"groupings[{i}] ('{groupings[i].get('title', '')}')" for i in sorted_indices]
            errors.append(f"Duplicate skill '{slug}' declared across multiple groups: {', '.join(group_titles)}")
            duplicate_count += (len(group_indices) - 1)

    total_declared_skills = len(all_declared_slugs)

    # 5. Physical Repository Parity Cross-Check
    physical_skills, discovery_errors = discover_physical_skills(repo_root)
    errors.extend(discovery_errors)

    total_physical_skills = sum(len(items) for items in physical_skills.values())

    missing_physical_slugs: List[str] = []
    directory_mismatches: List[Dict[str, str]] = []

    matched_declared_count = 0
    for slug in all_declared_slugs.keys():
        if slug not in physical_skills:
            missing_physical_slugs.append(slug)
            errors.append(f"Declared skill '{slug}' not found in any physical SKILL.md frontmatter")
        else:
            matched_declared_count += 1
            for p_info in physical_skills[slug]:
                leaf_dir = p_info["leaf_dir"]
                if leaf_dir != slug:
                    mismatch_entry = {
                        "slug": slug,
                        "leaf_dir": leaf_dir,
                        "rel_path": p_info["rel_path"],
                    }
                    directory_mismatches.append(mismatch_entry)
                    msg = (
                        f"Directory name mismatch: skill '{slug}' is located in folder "
                        f"'{leaf_dir}' ({p_info['rel_path']})"
                    )
                    if strict:
                        errors.append(msg)
                    else:
                        warnings.append(msg)

    slug_parity = (
        round(matched_declared_count / total_declared_skills, 4)
        if total_declared_skills > 0
        else 0.0
    )

    is_valid = (len(errors) == 0)

    return {
        "valid": is_valid,
        "groupingsCount": groupings_count,
        "maxSkillsPerGroup": max_skills_in_group,
        "emptyTitles": empty_titles_count,
        "duplicates": duplicate_count,
        "slugParity": slug_parity,
        "totalDeclaredSkills": total_declared_skills,
        "totalPhysicalSkills": total_physical_skills,
        "missingPhysicalCount": len(missing_physical_slugs),
        "directoryMismatchCount": len(directory_mismatches),
        "errors": errors,
        "warnings": warnings,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic validator for skills.sh.json schema and repository parity."
    )
    parser.add_argument(
        "--config",
        "--skills-file",
        type=Path,
        default=None,
        dest="config",
        help="Path to skills.sh.json (default: <repo-root>/skills.sh.json)",
    )
    parser.add_argument(
        "--repo-root",
        "--root",
        type=Path,
        default=None,
        dest="repo_root",
        help="Repository root directory (default: parent of scripts/ or current dir)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce strict validation (treat warnings as errors, including directory name mismatches)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output validation results as structured JSON to stdout",
    )

    args = parser.parse_args(argv)

    if args.repo_root:
        repo_root = args.repo_root.resolve()
    else:
        current_dir = Path.cwd().resolve()
        if (current_dir / "skills.sh.json").is_file():
            repo_root = current_dir
        else:
            repo_root = Path(__file__).resolve().parents[1]

    config_path = (args.config or (repo_root / "skills.sh.json")).resolve()

    res = validate_schema_and_parity(config_path, repo_root, strict=args.strict)

    if args.json_output:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        status_label = "PASSED" if res["valid"] else "FAILED"
        print(f"=== skills.sh Validation {status_label} ===")
        print(f"Config: {config_path}")
        print(f"Repository Root: {repo_root}")
        print(f"Strict Mode: {args.strict}")
        print(f"Groupings Count: {res['groupingsCount']} (schema limit: 1-50)")
        print(f"Max Skills / Group: {res['maxSkillsPerGroup']} (schema limit: 1-500)")
        print(f"Empty Titles: {res['emptyTitles']}")
        print(f"Duplicate Slugs: {res['duplicates']}")
        print(f"Declared Skills: {res['totalDeclaredSkills']}")
        print(f"Physical Skills: {res['totalPhysicalSkills']}")
        print(f"Slug Parity: {res['slugParity'] * 100:.1f}%")
        print(f"Directory Mismatches: {res['directoryMismatchCount']}")

        if res["warnings"]:
            print(f"\nWarnings ({len(res['warnings'])}):")
            for w in res["warnings"]:
                print(f"  [WARN] {w}")

        if res["errors"]:
            print(f"\nErrors ({len(res['errors'])}):", file=sys.stderr)
            for err in res["errors"]:
                print(f"  [ERROR] {err}", file=sys.stderr)

    return 0 if res["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
