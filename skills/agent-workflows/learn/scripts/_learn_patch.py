"""The patch-application seam shared by learn_apply.py and learn_rollback.py.

Deliberately knows nothing about the learn system's own domain concepts (ids,
index.json, scope) -- it only knows how to apply a unified diff to a file and
report what happened, including the diff that would undo it. Both scripts are
thin adapters around apply_patch_to_target(): one chooses to apply a
learning's forward diff, the other chooses to apply a previously-captured
reverse diff. The direction never has to appear in this module's interface.

Requires the `patch` command-line utility (standard on macOS/Linux).
"""

from __future__ import annotations

import difflib
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PatchResult:
    success: bool
    reverse_diff: str = ""
    stdout: str = ""
    stderr: str = ""


def apply_patch_to_target(target_path: Path, diff_text: str) -> PatchResult:
    """Apply diff_text to target_path, in place, via `patch`.

    Diff headers (`---`/`+++`) must use target_path's bare filename (see
    references/rollback-and-migration.md) -- this function runs `patch` with
    cwd set to target_path's parent so that convention works for any scope.

    Never raises for an ordinary patch failure (conflict, stale context):
    that comes back as PatchResult(success=False, stdout=..., stderr=...) so
    callers can log/report it without a try/except. Only genuinely
    exceptional I/O errors (e.g. permission denied creating a directory)
    propagate as exceptions.
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    original_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""

    result = subprocess.run(
        ["patch", "--batch", "-p0"],
        input=diff_text,
        cwd=str(target_path.parent),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return PatchResult(success=False, stdout=result.stdout, stderr=result.stderr)

    # Clean up any backup patch may have left; the caller's own snapshot
    # mechanism (or this function's reverse_diff) supersedes it.
    orig_backup = target_path.with_name(target_path.name + ".orig")
    if orig_backup.exists():
        orig_backup.unlink()

    new_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
    reverse_diff = "".join(
        difflib.unified_diff(
            new_text.splitlines(keepends=True),
            original_text.splitlines(keepends=True),
            fromfile=target_path.name,
            tofile=target_path.name,
        )
    )
    return PatchResult(success=True, reverse_diff=reverse_diff, stdout=result.stdout, stderr=result.stderr)
