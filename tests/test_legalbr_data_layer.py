#!/usr/bin/env python3
"""Unit tests for the legalbr optional data integration layer.

Covers corpus reconciliation, dataset validation (including Codex review
fixes: tree hash comparison, refuse-to-rewrite on structural failure,
revalidate after --write-manifest) and SQLite index overwrite.
"""

from __future__ import annotations

import io
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

LEGALBR_SCRIPTS = Path(__file__).resolve().parents[1] / "legalbr" / "scripts"
sys.path.insert(0, str(LEGALBR_SCRIPTS))

import build_data_index  # noqa: E402
import reconcile_corpus  # noqa: E402
import validate_data  # noqa: E402


SKILL_TEMPLATE = """\
---
id: {skill_id}
name: {name}
category: {category}
---
# {name}

corpo {body}
"""


def write_skill(path: Path, skill_id: str, name: str, category: str = "materia", body: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        SKILL_TEMPLATE.format(skill_id=skill_id, name=name, category=category, body=body),
        encoding="utf-8",
    )


def write_pair(directory: Path, stem: str, record_id: str, text: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{stem}.json").write_text(
        json.dumps({"id": record_id}, ensure_ascii=False),
        encoding="utf-8",
    )
    (directory / f"{stem}.txt").write_text(text, encoding="utf-8")


def write_digest(root: Path, items: list[str]) -> None:
    path = root / "legislacao" / "boletim_30dias.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"dias": [{"itens": [{"id": item} for item in items]}]}, ensure_ascii=False),
        encoding="utf-8",
    )


def fixture_data_root(root: Path, *, digest_items: list[str] | None = None, juris_text: str = "ementa stj") -> None:
    write_digest(root, digest_items or ["item-1"])
    write_pair(root / "legislacao" / "textos", "lei-1", "lei-1", "texto da lei")
    write_pair(root / "jurisprudencia" / "stj", "123", "123", juris_text)
    (root / "jurisprudencia" / "tream").mkdir(parents=True, exist_ok=True)


class TestReconcileCorpus(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_uuid_match_with_name_and_path_slug_differences(self) -> None:
        external = self.temp_path / "external"
        canonical = self.temp_path / "legalbr"
        write_skill(
            external / "skills" / "materia" / "controle-estadual.md",
            "uuid-1",
            "controle-estadual",
        )
        write_skill(
            canonical / "materia" / "controle" / "SKILL.md",
            "uuid-1",
            "controle",
        )
        report = reconcile_corpus.build_report(external, canonical)
        self.assertEqual(report["counts"]["external"], 1)
        self.assertEqual(report["counts"]["legalbr"], 1)
        self.assertEqual(report["counts"]["same_uuid"], 1)
        self.assertEqual(report["counts"]["renamed"], 1)
        self.assertEqual(report["counts"]["path_renamed"], 1)
        self.assertEqual(report["renames"][0]["external_name"], "controle-estadual")
        self.assertEqual(report["renames"][0]["legalbr_name"], "controle")
        self.assertNotIn("minutai", json.dumps(report))


class TestValidateData(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.data_root = self.temp_path / "data"
        fixture_data_root(self.data_root)
        self.report = validate_data.validate(self.data_root)
        self.manifest_path = self.temp_path / "manifest.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _baseline_manifest(self) -> dict:
        return {
            "schema_version": 1,
            "datasets": {
                "legislacao": {
                    "digest_items": 1,
                    "full_text_records": 1,
                    "json_txt_pairs": 1,
                },
                "jurisprudencia": {
                    "records": 1,
                    "json_txt_pairs": 1,
                    "empty_courts": ["tream"],
                },
            },
            "data_tree_sha256": self.report["tree_sha256"],
        }

    def test_compare_manifest_detects_tree_hash_mismatch(self) -> None:
        manifest = self._baseline_manifest()
        self.assertEqual(validate_data.compare_manifest(self.report, manifest), [])
        (self.data_root / "jurisprudencia" / "stj" / "123.txt").write_text(
            "ementa alterada sem mudar contagens",
            encoding="utf-8",
        )
        changed = validate_data.validate(self.data_root)
        problems = validate_data.compare_manifest(changed, manifest)
        self.assertIn("arvore de dados diverge do hash registrado no manifesto", problems)

    def test_write_manifest_skipped_on_structural_failure(self) -> None:
        manifest = self._baseline_manifest()
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        original = self.manifest_path.read_text(encoding="utf-8")
        (self.data_root / "legislacao" / "textos" / "lei-1.txt").unlink()
        argv = [
            "validate_data.py",
            "--data-root",
            str(self.data_root),
            "--manifest",
            str(self.manifest_path),
            "--write-manifest",
            "--json",
        ]
        old_argv = sys.argv
        sys.argv = argv
        try:
            with redirect_stdout(io.StringIO()):
                exit_code = validate_data.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(exit_code, 1)
        self.assertEqual(self.manifest_path.read_text(encoding="utf-8"), original)

    def test_write_manifest_revalidates_against_updated_baseline(self) -> None:
        manifest = self._baseline_manifest()
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        write_digest(self.data_root, ["item-1", "item-2"])
        argv = [
            "validate_data.py",
            "--data-root",
            str(self.data_root),
            "--manifest",
            str(self.manifest_path),
            "--write-manifest",
            "--json",
        ]
        old_argv = sys.argv
        sys.argv = argv
        try:
            with redirect_stdout(io.StringIO()):
                exit_code = validate_data.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(exit_code, 0)
        updated = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(updated["datasets"]["legislacao"]["digest_items"], 2)


class TestBuildDataIndex(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.data_root = self.temp_path / "data"
        fixture_data_root(self.data_root)
        self.output = self.temp_path / "index.sqlite3"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_overwrite_drops_index_meta(self) -> None:
        first = build_data_index.build(self.data_root, self.output)
        self.assertEqual(first, 2)
        second = build_data_index.build(self.data_root, self.output)
        self.assertEqual(second, 2)
        connection = sqlite3.connect(self.output)
        try:
            count = connection.execute(
                "SELECT value FROM index_meta WHERE key = 'document_count'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(count, "2")


if __name__ == "__main__":
    unittest.main()
