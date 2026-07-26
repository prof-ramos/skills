#!/usr/bin/env python3
"""Apply ONE approved learning to its target file (RF-07).

Only call this after the user has given explicit approval for this specific
id (see SKILL.md's "Gate de aprovacao"). This script does not itself check
who approved what -- that check is the agent's responsibility, before it
ever runs this command.

Diff convention (see references/rollback-and-migration.md): the ```diff```
block in the learning entry must use the *bare filename* of target_file in
its `---`/`+++` headers (e.g. `--- AGENTS.md` / `+++ AGENTS.md`, or
`--- /dev/null` / `+++ SKILL.md` when creating a new file). scripts/_learn_patch.py
runs `patch` with cwd set to target_file's parent directory, so the same diff
format works regardless of scope (project root, subdirectory, or the global
~/.codex/AGENTS.md).

This script is a thin adapter around _learn_patch.apply_patch_to_target(): it
resolves the learning's forward diff, hands it to the shared patch-mechanics
module, and translates the result into index.json/history updates.

Usage:
    python3 learn_apply.py --project-root /path/to/project --id LP-000123
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _learn_common import (
    append_history,
    extract_diff_block,
    find_learning,
    learning_path,
    load_index,
    parse_learning_entry,
    resolve_target,
    save_index,
    snapshot_path,
)
from _learn_patch import apply_patch_to_target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Root of the target project")
    parser.add_argument("--id", required=True, help="Learning id, e.g. LP-000123")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    entry_path = learning_path(project_root, args.id)
    if not entry_path.is_file():
        print(f"error: no learning entry at {entry_path}", file=sys.stderr)
        return 1

    frontmatter, body = parse_learning_entry(entry_path.read_text(encoding="utf-8"))
    target_file = frontmatter.get("target_file")
    if not target_file:
        print(f"error: {entry_path} has no 'target_file' in frontmatter", file=sys.stderr)
        return 1

    try:
        diff_text = extract_diff_block(body)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    target_path = resolve_target(project_root, target_file)
    result = apply_patch_to_target(target_path, diff_text)

    if not result.success:
        append_history(
            project_root,
            {"id": args.id, "action": "apply", "target_file": target_file, "result": "failed"},
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

    snapshot_path(project_root, args.id).write_text(result.reverse_diff, encoding="utf-8")

    index = load_index(project_root)
    entry = find_learning(index, args.id)
    if entry is None:
        print(f"error: {args.id} not found in index.json (was it registered?)", file=sys.stderr)
        return 1
    entry["status"] = "applied"
    save_index(project_root, index)

    append_history(
        project_root,
        {"id": args.id, "action": "apply", "target_file": target_file, "result": "success"},
    )

    print(
        json.dumps(
            {"id": args.id, "result": "success", "target_file": target_file, "diff_applied": diff_text},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
