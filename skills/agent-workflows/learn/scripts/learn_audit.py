#!/usr/bin/env python3
"""Report obsolescence, duplication, and dependency-graph health for learnings.

Answers the "future evaluation" questions from the spec: is this rule still
used, is this skill obsolete, is there a duplicate, what was never reused.
Read-only -- never modifies index.json or any learning file.

Usage:
    python3 learn_audit.py --project-root /path/to/project [--stale-days 180]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from _learn_common import load_index


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def find_never_used(learnings: list[dict]) -> list[str]:
    return [e["id"] for e in learnings if e.get("status") == "applied" and not e.get("last_used")]


def find_stale(learnings: list[dict], stale_days: int, now: datetime) -> list[dict]:
    stale = []
    for e in learnings:
        if e.get("status") != "applied":
            continue
        reference = parse_iso(e.get("last_validated")) or parse_iso(e.get("applied_at"))
        if reference is None or (now - reference).days > stale_days:
            stale.append({"id": e["id"], "last_validated": e.get("last_validated"), "applied_at": e.get("applied_at")})
    return stale


def find_duplicate_candidates(learnings: list[dict]) -> list[list[str]]:
    groups: dict[tuple[str, str, str], list[str]] = {}
    for e in learnings:
        key = (normalize_title(e.get("title", "")), e.get("category", ""), e.get("scope", ""))
        groups.setdefault(key, []).append(e["id"])
    return [ids for ids in groups.values() if len(ids) > 1]


def find_dependency_issues(learnings: list[dict]) -> dict:
    ids = {e["id"] for e in learnings}
    missing_refs = []
    for e in learnings:
        for ref in (e.get("depends_on") or []):
            if ref not in ids:
                missing_refs.append({"id": e["id"], "missing_dependency": ref})
        superseded_by = e.get("superseded_by")
        if superseded_by and superseded_by not in ids:
            missing_refs.append({"id": e["id"], "missing_superseded_by": superseded_by})

    graph = {e["id"]: (e.get("depends_on") or []) for e in learnings}
    cycles = []
    for start in graph:
        visited: list[str] = []
        node = start
        for _ in range(len(graph) + 1):
            deps = graph.get(node, [])
            if not deps:
                break
            node = deps[0]
            if node in visited:
                cycles.append(visited + [node])
                break
            visited.append(node)
            if node == start:
                cycles.append(visited)
                break

    return {"missing_references": missing_refs, "cycles": cycles}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Root of the target project")
    parser.add_argument("--stale-days", type=int, default=180)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"error: project root {project_root} is not a directory", file=sys.stderr)
        return 1

    index = load_index(project_root)
    learnings = index.get("learnings", [])
    now = datetime.now(timezone.utc)

    report = {
        "total_learnings": len(learnings),
        "never_used": find_never_used(learnings),
        "stale": find_stale(learnings, args.stale_days, now),
        "duplicate_candidates": find_duplicate_candidates(learnings),
        "dependency_issues": find_dependency_issues(learnings),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
