#!/usr/bin/env python3
"""Parse tracked Python files without writing bytecode."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


def tracked_python_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    failures: list[str] = []
    for path in tracked_python_files():
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path}:{exc.lineno}:{exc.offset}: {exc.msg}")

    if failures:
        print("Python syntax check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"Python syntax OK ({len(tracked_python_files())} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
