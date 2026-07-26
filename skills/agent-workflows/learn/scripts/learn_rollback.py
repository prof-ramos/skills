#!/usr/bin/env python3
"""Revert ONE applied learning via its stored reverse diff (never the whole file).

Refuses to run if another *applied* learning declares this id in its
depends_on -- pass --force only after the user has confirmed they understand
the impact (see references/rollback-and-migration.md#impacto-de-dependencias).

This script is a thin adapter around _learn_patch.apply_patch_to_target(): it
resolves the previously-captured reverse diff, hands it to the shared
patch-mechanics module, and translates the result into index.json/history
updates.

Usage:
    python3 learn_rollback.py --project-root /path/to/project --id LP-000123 [--force]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _learn_common import (
    append_history,
    find_learning,
    learning_path,
    load_index,
    parse_learning_entry,
    resolve_target,
    save_index,
    snapshot_path,
)
from _learn_patch import apply_patch_to_target


def dependents_of(index: dict, learning_id: str) -> list[str]:
    return [
        e["id"]
        for e in index.get("learnings", [])
        if e.get("status") == "applied" and learning_id in (e.get("depends_on") or [])
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Root of the target project")
    parser.add_argument("--id", required=True, help="Learning id, e.g. LP-000123")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Proceed even if other applied learnings depend on this one",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    index = load_index(project_root)
    entry = find_learning(index, args.id)
    if entry is None:
        print(f"error: {args.id} not found in index.json", file=sys.stderr)
        return 1
    if entry.get("status") != "applied":
        print(f"error: {args.id} has status {entry.get('status')!r}, expected 'applied'", file=sys.stderr)
        return 1

    dependents = dependents_of(index, args.id)
    if dependents and not args.force:
        print(
            json.dumps(
                {
                    "id": args.id,
                    "result": "blocked",
                    "reason": "other applied learnings depend on this one",
                    "dependents": dependents,
                },
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    snap_path = snapshot_path(project_root, args.id)
    if not snap_path.is_file():
        print(f"error: no snapshot at {snap_path}; refusing to fall back to a whole-file restore", file=sys.stderr)
        return 1
    reverse_diff = snap_path.read_text(encoding="utf-8")
    if not reverse_diff.strip():
        print(f"error: snapshot for {args.id} is empty; nothing to revert", file=sys.stderr)
        return 1

    entry_path = learning_path(project_root, args.id)
    frontmatter, _ = parse_learning_entry(entry_path.read_text(encoding="utf-8"))
    target_file = frontmatter.get("target_file")
    if not target_file:
        print(f"error: {entry_path} has no 'target_file' in frontmatter", file=sys.stderr)
        return 1
    target_path = resolve_target(project_root, target_file)

    result = apply_patch_to_target(target_path, reverse_diff)
    if not result.success:
        append_history(
            project_root,
            {"id": args.id, "action": "rollback", "target_file": target_file, "result": "failed"},
        )
        print(
            json.dumps(
                {"id": args.id, "result": "failed", "stdout": result.stdout, "stderr": result.stderr},
                indent=2,
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    entry["status"] = "rolled_back"
    save_index(project_root, index)
    append_history(
        project_root,
        {"id": args.id, "action": "rollback", "target_file": target_file, "result": "success"},
    )

    print(json.dumps({"id": args.id, "result": "success", "target_file": target_file}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
