#!/usr/bin/env python3
"""Run bash syntax checks for tracked shell scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def tracked_shell_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.sh"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    failures: list[str] = []
    files = tracked_shell_files()
    for path in files:
        result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            failures.append(f"{path}: {detail}")

    if failures:
        print("Shell syntax check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"Shell syntax OK ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
