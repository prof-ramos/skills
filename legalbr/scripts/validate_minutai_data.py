#!/usr/bin/env python3
"""Validate an external MinutaIA data checkout without importing raw files."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def pair_inventory(directory: Path, extension: str) -> tuple[set[str], set[str]]:
    return (
        {path.stem for path in directory.glob("*.json")},
        {path.stem for path in directory.glob(f"*.{extension}")},
    )


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in {".json", ".txt"}):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def validate_pairs(directory: Path, label: str, problems: list[str]) -> dict:
    json_files, txt_files = pair_inventory(directory, "txt")
    for stem in sorted(json_files - txt_files):
        problems.append(f"{label}: .txt ausente para {stem}")
    for stem in sorted(txt_files - json_files):
        problems.append(f"{label}: .json ausente para {stem}")
    invalid_json = 0
    empty_text = 0
    for path in sorted(directory.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or not value.get("id"):
                problems.append(f"{label}: metadata sem objeto/id em {path.name}")
        except (OSError, json.JSONDecodeError) as exc:
            invalid_json += 1
            problems.append(f"{label}: JSON inválido em {path.name}: {exc}")
    for path in sorted(directory.glob("*.txt")):
        if not path.read_text(encoding="utf-8").strip():
            empty_text += 1
            problems.append(f"{label}: texto vazio em {path.name}")
    return {"json": len(json_files), "txt": len(txt_files), "pairs": len(json_files & txt_files), "invalid_json": invalid_json, "empty_text": empty_text}


def validate(root: Path) -> dict:
    """Coleta estatísticas e problemas estruturais do checkout.

    Não compara com o manifesto: essa etapa é responsabilidade de
    ``compare_manifest``, para que um refresh legítimo não seja confundido
    com um erro estrutural.
    """
    problems: list[str] = []
    legislation = root / "legislacao"
    jurisprudence = root / "jurisprudencia"
    digest_path = legislation / "boletim_30dias.json"
    digest_days = digest_items = 0
    if not digest_path.exists():
        problems.append(f"legislacao: arquivo ausente {digest_path}")
    else:
        try:
            digest = json.loads(digest_path.read_text(encoding="utf-8"))
            digest_days = len(digest.get("dias", []))
            digest_items = sum(len(day.get("itens", [])) for day in digest.get("dias", []))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"legislacao: boletim inválido: {exc}")
    legislation_stats = validate_pairs(legislation / "textos", "legislacao", problems)
    courts = {}
    for court_dir in sorted(p for p in jurisprudence.iterdir() if p.is_dir()) if jurisprudence.exists() else []:
        courts[court_dir.name] = validate_pairs(court_dir, court_dir.name, problems)
    juris_records = sum(item["pairs"] for item in courts.values())
    report = {
        "root": str(root),
        "problems": problems,
        "legislacao": {"digest_days": digest_days, "digest_items": digest_items, "textos": legislation_stats},
        "jurisprudencia": {
            "court_directories": len(courts),
            "courts_with_data": sum(1 for item in courts.values() if item["pairs"]),
            "empty_courts": [court for court, item in courts.items() if not item["pairs"]],
            "records": juris_records,
            "courts": courts,
        },
        "tree_sha256": tree_hash(root) if root.exists() else None,
    }
    report["problems"] = problems
    return report


def compare_manifest(report: dict, manifest: dict) -> list[str]:
    """Compara o relatório com o baseline registrado no manifesto."""
    problems: list[str] = []
    expected = manifest.get("datasets", {})
    legislation = report["legislacao"]
    jurisprudence = report["jurisprudencia"]
    if legislation["digest_items"] != expected.get("legislacao", {}).get("digest_items", legislation["digest_items"]):
        problems.append("legislacao: quantidade de itens diverge do manifesto")
    if legislation["textos"]["pairs"] != expected.get("legislacao", {}).get("json_txt_pairs", legislation["textos"]["pairs"]):
        problems.append("legislacao: quantidade de pares diverge do manifesto")
    if jurisprudence["records"] != expected.get("jurisprudencia", {}).get("records", jurisprudence["records"]):
        problems.append("jurisprudencia: quantidade de registros diverge do manifesto")
    if jurisprudence["empty_courts"] != expected.get("jurisprudencia", {}).get("empty_courts", jurisprudence["empty_courts"]):
        problems.append("jurisprudencia: tribunais vazios divergem do manifesto")
    recorded_hash = manifest.get("data_tree_sha256")
    if recorded_hash and report["tree_sha256"] != recorded_hash:
        problems.append("arvore de dados diverge do hash registrado no manifesto")
    return problems


def update_manifest(path: Path, report: dict) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema_version": 1}
    legislation = report["legislacao"]
    jurisprudence = report["jurisprudencia"]
    manifest.setdefault("datasets", {})
    manifest["datasets"]["legislacao"] = {
        **manifest["datasets"].get("legislacao", {}),
        "digest_items": legislation["digest_items"],
        "full_text_records": legislation["textos"]["pairs"],
        "json_txt_pairs": legislation["textos"]["pairs"],
    }
    manifest["datasets"]["jurisprudencia"] = {
        **manifest["datasets"].get("jurisprudencia", {}),
        "records": jurisprudence["records"],
        "json_txt_pairs": jurisprudence["records"],
        "court_directories_present": jurisprudence["court_directories"],
        "courts_with_data": jurisprudence["courts_with_data"],
        "empty_courts": jurisprudence["empty_courts"],
    }
    manifest["last_verified_at"] = datetime.now(timezone.utc).date().isoformat()
    manifest["data_tree_sha256"] = report["tree_sha256"]
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-manifest", action="store_true", help="atualiza contagens e hash no manifesto")
    args = parser.parse_args()
    if args.write_manifest and not args.manifest:
        parser.error("--write-manifest exige --manifest")
    report = validate(args.data_root.resolve())
    structural_problems = list(report["problems"])

    manifest = None
    if args.manifest and args.manifest.exists():
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    if structural_problems:
        # Checkout inválido nunca reescreve o baseline confiável do manifesto.
        report["problems"] = structural_problems
    else:
        if args.write_manifest:
            update_manifest(args.manifest, report)
            manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report["problems"] = compare_manifest(report, manifest) if manifest else []

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"jurisprudencia: {report['jurisprudencia']['records']} registros")
        print(f"legislacao: {report['legislacao']['digest_items']} itens no boletim, {report['legislacao']['textos']['pairs']} textos")
        print(f"tree_sha256: {report['tree_sha256']}")
        for problem in report["problems"]:
            print(f"ERRO: {problem}", file=sys.stderr)
    return 1 if report["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
