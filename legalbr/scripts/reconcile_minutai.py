#!/usr/bin/env python3
"""Reconcile the canonical legalbr corpus with a MinutaIA checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


FIELD_RE = re.compile(r"^(id|name|category|path|sourcePath|legacySourcePath):\s*(.*?)\s*$")


def header(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"frontmatter ausente: {path}")
    result: dict[str, str] = {}
    delimiters = [i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"]
    if not delimiters:
        raise ValueError(f"frontmatter sem fechamento: {path}")
    for line in lines[1 : delimiters[0]]:
        match = FIELD_RE.match(line)
        if match:
            result[match.group(1)] = match.group(2).strip("\"'")
    for required in ("id", "name", "category"):
        if required not in result:
            raise ValueError(f"campo {required} ausente: {path}")
    return result


def body_hash(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    delimiters = [i for i, line in enumerate(lines) if line.strip() == "---"]
    body = "\n".join(lines[delimiters[1] + 1 :]) + "\n"
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def collect(root: Path, minutai: bool) -> tuple[dict[str, dict[str, str]], list[str]]:
    base = root / "skills" if minutai else root
    paths = list((base / "forma").rglob("*.md")) + list((base / "materia").rglob("*.md"))
    if not minutai:
        paths = list((base / "forma").rglob("SKILL.md")) + list((base / "materia").rglob("SKILL.md"))
    records: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for path in sorted(paths):
        data = header(path)
        item = {
            "id": data["id"],
            "name": data["name"],
            "category": data["category"],
            "path": path.relative_to(root).as_posix(),
            "path_slug": path.stem if minutai else path.parent.name,
            "body_sha256": body_hash(path),
        }
        if item["id"] in records:
            duplicates.append(item["id"])
        records[item["id"]] = item
    return records, duplicates


def build_report(minutai_root: Path, legalbr_root: Path) -> dict:
    minutai, minutai_duplicates = collect(minutai_root, minutai=True)
    legalbr, legalbr_duplicates = collect(legalbr_root, minutai=False)
    common = sorted(set(minutai) & set(legalbr))
    renames = [
        {
            "id": item_id,
            "minutai_name": minutai[item_id]["name"],
            "legalbr_name": legalbr[item_id]["name"],
            "minutai_path": minutai[item_id]["path"],
            "legalbr_path": legalbr[item_id]["path"],
        }
        for item_id in common
        if minutai[item_id]["name"] != legalbr[item_id]["name"]
    ]
    path_renames = [
        {
            "id": item_id,
            "minutai_path_slug": minutai[item_id]["path_slug"],
            "legalbr_path_slug": legalbr[item_id]["path_slug"],
            "minutai_path": minutai[item_id]["path"],
            "legalbr_path": legalbr[item_id]["path"],
        }
        for item_id in common
        if minutai[item_id]["path_slug"] != legalbr[item_id]["path_slug"]
    ]
    body_differences = [
        item_id for item_id in common if minutai[item_id]["body_sha256"] != legalbr[item_id]["body_sha256"]
    ]
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "minutai": len(minutai),
            "legalbr": len(legalbr),
            "same_uuid": len(common),
            "same_name": len(common) - len(renames),
            "renamed": len(renames),
            "path_renamed": len(path_renames),
            "missing_in_minutai": len(set(legalbr) - set(minutai)),
            "missing_in_legalbr": len(set(minutai) - set(legalbr)),
            "body_differences": len(body_differences),
        },
        "renames": renames,
        "path_renames": path_renames,
        "missing_in_minutai": [legalbr[item_id] for item_id in sorted(set(legalbr) - set(minutai))],
        "missing_in_legalbr": [minutai[item_id] for item_id in sorted(set(minutai) - set(legalbr))],
        "body_differences": body_differences,
        "duplicate_ids": {"minutai": sorted(set(minutai_duplicates)), "legalbr": sorted(set(legalbr_duplicates))},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minutai-root", type=Path, required=True)
    parser.add_argument("--legalbr-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true", help="falha em UUIDs duplicados ou divergência de corpo")
    args = parser.parse_args()
    report = build_report(args.minutai_root.resolve(), args.legalbr_root.resolve())
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")
    if args.strict and (report["body_differences"] or any(report["duplicate_ids"].values())):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
