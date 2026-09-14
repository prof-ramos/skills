#!/usr/bin/env python3
"""Unit tests for scripts/validate_skills_sh.py.

Zero-external-dependency tests using Python standard library unittest.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

# Ensure scripts directory is importable
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_skills_sh import (
    parse_frontmatter,
    discover_physical_skills,
    validate_schema_and_parity,
)


class TestFrontmatterParser(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_frontmatter(self):
        f = self.temp_path / "SKILL.md"
        f.write_text(
            "---\nname: test-skill\ndescription: A test skill description\n---\n# Body\n",
            encoding="utf-8",
        )
        data, err = parse_frontmatter(f)
        self.assertIsNone(err)
        self.assertEqual(data.get("name"), "test-skill")
        self.assertEqual(data.get("description"), "A test skill description")

    def test_quoted_frontmatter(self):
        f = self.temp_path / "SKILL.md"
        f.write_text(
            '---\nname: "quoted-skill"\ndescription: \'single quoted\'\n---\n',
            encoding="utf-8",
        )
        data, err = parse_frontmatter(f)
        self.assertIsNone(err)
        self.assertEqual(data.get("name"), "quoted-skill")
        self.assertEqual(data.get("description"), "single quoted")

    def test_block_scalar_description(self):
        f = self.temp_path / "SKILL.md"
        f.write_text(
            "---\nname: block-skill\ndescription: >\n  Line one\n  Line two\n---\n",
            encoding="utf-8",
        )
        data, err = parse_frontmatter(f)
        self.assertIsNone(err)
        self.assertEqual(data.get("name"), "block-skill")
        self.assertEqual(data.get("description"), "Line one Line two")

    def test_missing_opening_marker(self):
        f = self.temp_path / "SKILL.md"
        f.write_text("name: broken\n---\n", encoding="utf-8")
        data, err = parse_frontmatter(f)
        self.assertIsNotNone(err)
        self.assertIn("Missing opening", err)

    def test_missing_closing_marker(self):
        f = self.temp_path / "SKILL.md"
        f.write_text("---\nname: broken\n", encoding="utf-8")
        data, err = parse_frontmatter(f)
        self.assertIsNotNone(err)
        self.assertIn("Missing closing", err)


class TestSchemaValidation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        skill_dir = self.temp_path / "skills" / "demo-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: Demo skill\n---\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_config(self, obj: dict) -> Path:
        cfg = self.temp_path / "skills.sh.json"
        cfg.write_text(json.dumps(obj, indent=2), encoding="utf-8")
        return cfg

    def test_minimal_valid_config(self):
        cfg = self._write_config({
            "$schema": "https://skills.sh/schemas/skills.sh.schema.json",
            "groupings": [
                {
                    "title": "General",
                    "skills": ["demo-skill"]
                }
            ]
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertTrue(res["valid"])
        self.assertEqual(res["groupingsCount"], 1)
        self.assertEqual(res["maxSkillsPerGroup"], 1)
        self.assertEqual(res["emptyTitles"], 0)
        self.assertEqual(res["duplicates"], 0)
        self.assertEqual(res["slugParity"], 1.0)
        self.assertEqual(len(res["errors"]), 0)

    def test_missing_groupings(self):
        cfg = self._write_config({
            "$schema": "https://skills.sh/schemas/skills.sh.schema.json"
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertTrue(any("Missing required root property 'groupings'" in e for e in res["errors"]))

    def test_unexpected_root_property(self):
        cfg = self._write_config({
            "groupings": [{"title": "General", "skills": ["demo-skill"]}],
            "unknownProperty": 123
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertTrue(any("unexpected property 'unknownProperty'" in e for e in res["errors"]))

    def test_invalid_not_grouped(self):
        cfg = self._write_config({
            "notGrouped": "middle",
            "groupings": [{"title": "General", "skills": ["demo-skill"]}]
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertTrue(any("'notGrouped' must be one of" in e for e in res["errors"]))

    def test_groupings_empty_array(self):
        cfg = self._write_config({"groupings": []})
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertTrue(any("at least 1 item" in e for e in res["errors"]))

    def test_groupings_exceeds_max_items(self):
        groups = [{"title": f"Group {i}", "skills": ["demo-skill"]} for i in range(51)]
        cfg = self._write_config({"groupings": groups})
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertTrue(any("exceeds maximum limit of 50 items" in e for e in res["errors"]))

    def test_grouping_missing_title(self):
        cfg = self._write_config({
            "groupings": [{"skills": ["demo-skill"]}]
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertEqual(res["emptyTitles"], 1)

    def test_grouping_empty_title(self):
        cfg = self._write_config({
            "groupings": [{"title": "   ", "skills": ["demo-skill"]}]
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertEqual(res["emptyTitles"], 1)

    def test_grouping_missing_skills(self):
        cfg = self._write_config({
            "groupings": [{"title": "Empty Group"}]
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertTrue(any("missing required property 'skills'" in e for e in res["errors"]))

    def test_duplicate_within_group(self):
        cfg = self._write_config({
            "groupings": [{"title": "General", "skills": ["demo-skill", "demo-skill"]}]
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertEqual(res["duplicates"], 1)
        self.assertTrue(any("duplicate skill 'demo-skill' declared within group" in e for e in res["errors"]))

    def test_duplicate_across_groups(self):
        cfg = self._write_config({
            "groupings": [
                {"title": "Group A", "skills": ["demo-skill"]},
                {"title": "Group B", "skills": ["demo-skill"]}
            ]
        })
        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertEqual(res["duplicates"], 1)
        self.assertTrue(any("declared across multiple groups" in e for e in res["errors"]))


class TestPhysicalParityAndStrict(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        s1 = self.temp_path / "skills" / "alpha"
        s1.mkdir(parents=True)
        (s1 / "SKILL.md").write_text("---\nname: alpha\ndescription: Alpha\n---\n", encoding="utf-8")

        s2 = self.temp_path / "skills" / "beta_dir"
        s2.mkdir(parents=True)
        (s2 / "SKILL.md").write_text("---\nname: beta-slug\ndescription: Beta\n---\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_declared_missing_from_physical(self):
        cfg = self.temp_path / "skills.sh.json"
        cfg.write_text(json.dumps({
            "groupings": [{"title": "General", "skills": ["non-existent-skill"]}]
        }), encoding="utf-8")

        res = validate_schema_and_parity(cfg, self.temp_path)
        self.assertFalse(res["valid"])
        self.assertEqual(res["missingPhysicalCount"], 1)
        self.assertEqual(res["slugParity"], 0.0)

    def test_directory_mismatch_normal_mode(self):
        cfg = self.temp_path / "skills.sh.json"
        cfg.write_text(json.dumps({
            "groupings": [{"title": "General", "skills": ["alpha", "beta-slug"]}]
        }), encoding="utf-8")

        res = validate_schema_and_parity(cfg, self.temp_path, strict=False)
        self.assertTrue(res["valid"])
        self.assertEqual(res["directoryMismatchCount"], 1)
        self.assertEqual(len(res["warnings"]), 1)
        self.assertEqual(len(res["errors"]), 0)

    def test_directory_mismatch_strict_mode(self):
        cfg = self.temp_path / "skills.sh.json"
        cfg.write_text(json.dumps({
            "groupings": [{"title": "General", "skills": ["alpha", "beta-slug"]}]
        }), encoding="utf-8")

        res = validate_schema_and_parity(cfg, self.temp_path, strict=True)
        self.assertFalse(res["valid"])
        self.assertEqual(res["directoryMismatchCount"], 1)
        self.assertEqual(len(res["warnings"]), 0)
        self.assertEqual(len(res["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
