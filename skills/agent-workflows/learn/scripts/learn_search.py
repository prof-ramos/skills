#!/usr/bin/env python3
"""Search for existing knowledge before proposing a new learning (RF-04).

Scans, in this order, and returns scored candidate matches as JSON:

  1. AGENTS.md hierarchy: subdirectory AGENTS.md files under the project,
     the project root AGENTS.md, and the global ~/.codex/AGENTS.md.
  2. Skill descriptions: .agents/skills/**/SKILL.md under the project and
     under $HOME/.agents/skills/**/SKILL.md.
  3. .agents/learn/index.json -- including learnings with status "ignored"
     or "archived", so a previously-rejected idea is surfaced instead of
     silently re-proposed.

This script only *finds candidates*; deciding duplicate vs. conflict vs.
genuinely new is the agent's job (see references/conflict-and-dedup.md).

Usage:
    python3 learn_search.py --project-root /path/to/project --query "retry logic flaky test"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _learn_common import learn_dir, load_index

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
WORD_RE = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> set[str]:
    return {tok.lower() for tok in WORD_RE.findall(text)}


def score(query_tokens: set[str], text: str) -> int:
    return len(query_tokens & tokenize(text))


def find_agents_md_files(project_root: Path) -> list[Path]:
    found = []
    for path in project_root.rglob("AGENTS.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        found.append(path)
    global_agents = Path.home() / ".codex" / "AGENTS.md"
    if global_agents.exists():
        found.append(global_agents)
    return found


def find_skill_md_files(project_root: Path) -> list[Path]:
    found = []
    for base in (project_root / ".agents" / "skills", Path.home() / ".agents" / "skills"):
        if base.exists():
            found.extend(base.rglob("SKILL.md"))
    return found


def parse_skill_description(text: str) -> str:
    match = re.search(r"^description:\s*(.*)$", text, re.MULTILINE)
    return match.group(1).strip().strip("\"'") if match else ""


def search(project_root: Path, query: str) -> list[dict]:
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results: list[dict] = []

    for path in find_agents_md_files(project_root):
        text = path.read_text(encoding="utf-8", errors="replace")
        for para in text.split("\n\n"):
            s = score(query_tokens, para)
            if s > 0:
                results.append(
                    {
                        "source": "agents_md",
                        "path": str(path),
                        "score": s,
                        "snippet": para.strip()[:300],
                    }
                )

    for path in find_skill_md_files(project_root):
        text = path.read_text(encoding="utf-8", errors="replace")
        description = parse_skill_description(text)
        s = score(query_tokens, description)
        if s > 0:
            results.append(
                {
                    "source": "skill_description",
                    "path": str(path),
                    "score": s,
                    "snippet": description[:300],
                }
            )

    index = load_index(project_root)
    for entry in index.get("learnings", []):
        haystack = " ".join(
            [
                entry.get("title", ""),
                entry.get("category", ""),
                " ".join(entry.get("tags", [])),
            ]
        )
        s = score(query_tokens, haystack)
        if s > 0:
            results.append(
                {
                    "source": "learn_index",
                    "path": f"{learn_dir(project_root)}/learnings/{entry.get('id')}.md",
                    "score": s,
                    "snippet": f"[{entry.get('status')}] {entry.get('title')}",
                    "id": entry.get("id"),
                    "status": entry.get("status"),
                }
            )

    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Root of the target project")
    parser.add_argument("--query", required=True, help="Keywords describing the candidate learning")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"error: project root {project_root} is not a directory", file=sys.stderr)
        return 1

    results = search(project_root, args.query)[: args.limit]
    print(json.dumps({"query": args.query, "matches": results}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
