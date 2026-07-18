"""Tests for export_bundle drift check."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_export_check_clean():
    r = subprocess.run(
        [sys.executable, "-m", "godmode_agnostic", "export", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**dict(**__import__("os").environ), "PYTHONPATH": str(ROOT)},
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_hall_of_fame_ids():
    from godmode_agnostic.core import load_bundle

    b = load_bundle()
    ids = {c["id"] for c in b["HALL_OF_FAME"]}
    assert ids == {
        "grok-420",
        "gemini-reset",
        "gpt-classic",
        "claude-inversion",
        "hermes-fast",
    }


def test_export_deterministic():
    from godmode_agnostic.export import build_bundle, dumps_bundle

    a = dumps_bundle(build_bundle())
    b = dumps_bundle(build_bundle())
    assert a == b
