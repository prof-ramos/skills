#!/usr/bin/env python3
"""Allocate the next LP-XXXXXX learning id for a project.

Usage:
    python3 learn_id.py --project-root /path/to/project

Prints the new id (e.g. "LP-000123") to stdout. Safe to call once per
candidate that is actually going into a proposal -- see
references/id-and-versioning.md for the id format and why gaps are fine.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _learn_common import next_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Root of the target project")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"error: project root {project_root} is not a directory", file=sys.stderr)
        return 1

    print(next_id(project_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
