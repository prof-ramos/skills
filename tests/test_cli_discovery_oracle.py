#!/usr/bin/env python3
"""
Empirical verification oracle for CLI discovery, directory hierarchy,
and frontmatter integrity across the skills repository.
"""

import os
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RENAMED_SKILLS = [
    ("social-carousel", "social-carousel/SKILL.md"),
    ("gerador-de-simulados", "gerador-de-simulados/SKILL.md"),
    (
        "uniao-homoafetiva-stf-tema-1072",
        "legalbr/materia/familia-sucessoes/uniao-homoafetiva-stf-tema-1072/SKILL.md",
    ),
    (
        "execucao-individual-sentenca-coletiva-lacp-cdc",
        "legalbr/materia/processo-civil/execucao-individual-sentenca-coletiva-lacp-cdc/SKILL.md",
    ),
    (
        "intervencao-anomala-uniao-tema-1101-fundo",
        "legalbr/materia/processo-civil/intervencao-anomala-uniao-tema-1101-fundo/SKILL.md",
    ),
    (
        "recurso-extraordinario-rg-tema-69-cf-102",
        "legalbr/materia/processo-civil/recurso-extraordinario-rg-tema-69-cf-102/SKILL.md",
    ),
    (
        "execucao-pena-transito-adc-43-44-54",
        "legalbr/materia/processo-penal/execucao-pena-transito-adc-43-44-54/SKILL.md",
    ),
    (
        "insanidade-incidente-cpp-149-suspensao",
        "legalbr/materia/processo-penal/insanidade-incidente-cpp-149-suspensao/SKILL.md",
    ),
    (
        "principios-acusatorio-cpp-3a-tema-1303",
        "legalbr/materia/processo-penal/principios-acusatorio-cpp-3a-tema-1303/SKILL.md",
    ),
    (
        "icms-st-base-pis-cofins-tema-1125-stj",
        "legalbr/materia/tributario/icms-st-base-pis-cofins-tema-1125-stj/SKILL.md",
    ),
    (
        "ir-juros-mora-pessoa-fisica-tema-808",
        "legalbr/materia/tributario/ir-juros-mora-pessoa-fisica-tema-808/SKILL.md",
    ),
]


def parse_frontmatter(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    frontmatter_text = parts[1]
    name_match = re.search(r"^name:\s*(?:[\"']?)([^\"'\n\r]+)(?:[\"']?)$", frontmatter_text, re.MULTILINE)
    desc_match = re.search(r"^description:\s*([|\"'].*|.+)$", frontmatter_text, re.MULTILINE)
    return {
        "name": name_match.group(1).strip() if name_match else None,
        "description": desc_match.group(1).strip() if desc_match else None,
        "raw": frontmatter_text,
    }


def run_cli_add_list(args):
    cmd = ["npx", "skills", "add"] + args
    res = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    return res


def extract_skills_from_cli_output(output: str):
    found_count_match = re.search(r"Found\s+(\d+)\s+skills", output)
    found_count = int(found_count_match.group(1)) if found_count_match else None
    
    skill_names = set()
    for line in output.splitlines():
        match = re.match(r"^│\s{4}([a-z0-9\-_]+)\s*$", line)
        if match:
            skill_names.add(match.group(1).strip())
    return found_count, skill_names


class TestCliDiscoveryAndDirectoryHierarchy(unittest.TestCase):

    def test_01_all_11_directories_exist_and_match_frontmatter(self):
        """Verify that all 11 renamed directories exist, have SKILL.md, and frontmatter matches directory name."""
        for expected_name, rel_path in RENAMED_SKILLS:
            full_path = REPO_ROOT / rel_path
            self.assertTrue(full_path.is_file(), f"File does not exist: {rel_path}")
            
            dir_name = full_path.parent.name
            self.assertEqual(dir_name, expected_name, f"Directory name {dir_name} != expected {expected_name}")
            
            fm = parse_frontmatter(full_path)
            self.assertIsNotNone(fm, f"Failed to parse frontmatter in {rel_path}")
            self.assertEqual(fm["name"], expected_name, f"Frontmatter name {fm['name']} != expected {expected_name}")
            self.assertTrue(fm["description"], f"Missing description in {rel_path}")

    def test_02_cli_root_default_discovery(self):
        """Verify npx skills add . --list runs without error and discovers 24 skills."""
        res = run_cli_add_list([".", "--list"])
        self.assertEqual(res.returncode, 0, f"CLI exited with {res.returncode}: {res.stderr}")
        found_count, discovered = extract_skills_from_cli_output(res.stdout)
        self.assertEqual(found_count, 24, f"Expected 24 skills, found {found_count}")
        self.assertIn("social-carousel", discovered)
        self.assertIn("gerador-de-simulados", discovered)

    def test_03_cli_legalbr_discovery(self):
        """Verify npx skills add ./legalbr --list discovers all 2149 legalbr skills."""
        res = run_cli_add_list(["./legalbr", "--list"])
        self.assertEqual(res.returncode, 0, f"CLI exited with {res.returncode}: {res.stderr}")
        found_count, discovered = extract_skills_from_cli_output(res.stdout)
        self.assertEqual(found_count, 2149, f"Expected 2149 skills, found {found_count}")
        # Verify the 9 legalbr renamed skills are in discovered set
        for expected_name, rel_path in RENAMED_SKILLS[2:]:
            self.assertIn(expected_name, discovered, f"Skill {expected_name} missing from ./legalbr discovery")

    def test_04_cli_root_full_depth_discovery(self):
        """Verify npx skills add . --list --full-depth discovers all 2178 skills."""
        res = run_cli_add_list([".", "--list", "--full-depth"])
        self.assertEqual(res.returncode, 0, f"CLI exited with {res.returncode}: {res.stderr}")
        found_count, discovered = extract_skills_from_cli_output(res.stdout)
        self.assertEqual(found_count, 2178, f"Expected 2178 skills, found {found_count}")

    def test_05_collision_freedom_across_all_physical_skills(self):
        """Verify that skill names have zero unintended collisions."""
        all_skills = {}
        for root, dirs, files in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "dist", "build")]
            if "SKILL.md" in files:
                skill_file = Path(root) / "SKILL.md"
                rel_path = skill_file.relative_to(REPO_ROOT).as_posix()
                if "template" in rel_path:
                    continue
                fm = parse_frontmatter(skill_file)
                if fm and fm["name"]:
                    name = fm["name"]
                    if name not in all_skills:
                        all_skills[name] = []
                    all_skills[name].append(rel_path)

        unintended_collisions = {k: v for k, v in all_skills.items() if len(v) > 1 and k != "autoreview"}
        self.assertEqual(unintended_collisions, {}, f"Found unexpected name collisions: {unintended_collisions}")

    def test_06_path_modality_robustness(self):
        """Adversarially test CLI discovery with trailing slashes, absolute paths, and subpaths."""
        # 1. Trailing slash on legalbr
        res1 = run_cli_add_list(["./legalbr/", "--list"])
        self.assertEqual(res1.returncode, 0)
        found1, _ = extract_skills_from_cli_output(res1.stdout)
        self.assertEqual(found1, 2149)

        # 2. Absolute path to repository root
        res2 = run_cli_add_list([str(REPO_ROOT), "--list"])
        self.assertEqual(res2.returncode, 0)
        found2, _ = extract_skills_from_cli_output(res2.stdout)
        self.assertEqual(found2, 24)

        # 3. Subcategory deep discovery without full-depth
        res3 = run_cli_add_list(["./legalbr/materia/tributario", "--list"])
        self.assertEqual(res3.returncode, 0)
        found3, disc3 = extract_skills_from_cli_output(res3.stdout)
        self.assertGreater(found3, 10)
        self.assertIn("icms-st-base-pis-cofins-tema-1125-stj", disc3)
        self.assertIn("ir-juros-mora-pessoa-fisica-tema-808", disc3)

    def test_07_negative_flag_constraints(self):
        """Adversarially verify invalid flag combinations exit cleanly with non-zero error."""
        res = run_cli_add_list([".", "--list", "--json"])
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("The --json flag cannot be combined with --list.", res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main()
