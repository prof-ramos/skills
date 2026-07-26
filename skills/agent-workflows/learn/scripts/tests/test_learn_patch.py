#!/usr/bin/env python3
"""Regression test for the patch-application seam (scripts/_learn_patch.py).

Plain unittest, no external dependency, runnable standalone:
    python3 skills/agent-workflows/learn/scripts/tests/test_learn_patch.py

Wired into `make check` as `check-learn-patch` (see repo Makefile), following
the same convention as `check-khaos-smoke`: a real behavioral smoke check for
one specific module, not just syntax.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _learn_patch import apply_patch_to_target  # noqa: E402


DIFF_ADD_LINE = """\
--- AGENTS.md
+++ AGENTS.md
@@ -1,2 +1,3 @@
 # AGENTS.md

+- Nova regra.
"""


class ApplyPatchToTargetTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.project_root = Path(self._tmp.name)
        self.target = self.project_root / "AGENTS.md"
        self.target.write_text("# AGENTS.md\n\n", encoding="utf-8")

    def test_apply_then_reverse_round_trips_to_original_bytes(self) -> None:
        original = self.target.read_text(encoding="utf-8")

        forward = apply_patch_to_target(self.target, DIFF_ADD_LINE)
        self.assertTrue(forward.success, msg=forward.stderr)
        self.assertIn("Nova regra.", self.target.read_text(encoding="utf-8"))
        self.assertTrue(forward.reverse_diff.strip())

        backward = apply_patch_to_target(self.target, forward.reverse_diff)
        self.assertTrue(backward.success, msg=backward.stderr)
        self.assertEqual(self.target.read_text(encoding="utf-8"), original)

    def test_creates_missing_target_and_parent_directories(self) -> None:
        nested_target = self.project_root / "sub" / "AGENTS.md"
        diff = (
            "--- /dev/null\n"
            "+++ AGENTS.md\n"
            "@@ -0,0 +1,1 @@\n"
            "+# Novo arquivo\n"
        )

        result = apply_patch_to_target(nested_target, diff)

        self.assertTrue(result.success, msg=result.stderr)
        self.assertEqual(nested_target.read_text(encoding="utf-8"), "# Novo arquivo\n")

    def test_conflicting_diff_returns_failure_without_raising(self) -> None:
        # Context ("linha que nao existe") never matches the real file content.
        bad_diff = (
            "--- AGENTS.md\n"
            "+++ AGENTS.md\n"
            "@@ -1,2 +1,3 @@\n"
            " linha que nao existe\n"
            " outra linha que nao existe\n"
            "+- Nunca deveria ser aplicado.\n"
        )

        result = apply_patch_to_target(self.target, bad_diff)

        self.assertFalse(result.success)
        self.assertNotIn("Nunca deveria ser aplicado.", self.target.read_text(encoding="utf-8"))

    def test_no_leftover_orig_backup_file(self) -> None:
        apply_patch_to_target(self.target, DIFF_ADD_LINE)

        self.assertFalse((self.target.parent / "AGENTS.md.orig").exists())


if __name__ == "__main__":
    unittest.main()
