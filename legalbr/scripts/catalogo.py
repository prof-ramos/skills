#!/usr/bin/env python3
"""Validar metadados e manter índice local; não verificar conteúdo jurídico.

Requer Python 3.10+ e PyYAML. Executar --write após edição e --check no CI.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    sys.exit("Dependência ausente: PyYAML. Use um ambiente que já a forneça ou instale-a no ambiente de validação.")

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("path", "name", "category", "materia", "title", "version", "status", "verifiedAt", "reviewedAt", "reviewScope")
OFFICIAL = ("gov.br", "jus.br", "leg.br")


class UniqueLoader(yaml.SafeLoader):
    """Recusar chaves duplicadas em vez de aceitar o último valor."""


def unique_mapping(loader, node, deep=False):
    pairs = loader.construct_pairs(node, deep=deep)
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"chave YAML duplicada: {key}")
        result[key] = value
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def iso_date(value):
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        raise ValueError("usar data ISO sem horário")
    parsed = value if isinstance(value, dt.date) else dt.date.fromisoformat(str(value))
    if parsed > dt.datetime.now(dt.timezone.utc).date():
        raise ValueError("data de revisão no futuro")
    return parsed.isoformat()


def catalog():
    rows, errors, names = [], [], set()
    for path in sorted(ROOT.rglob("SKILL.md")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            parts = path.read_text(encoding="utf-8").split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                raise ValueError("frontmatter ausente")
            data = yaml.load(parts[1], Loader=UniqueLoader)
            if not isinstance(data, dict):
                raise ValueError("frontmatter não é mapa")
            name = data.get("name")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
                raise ValueError("name inválido")
            if name != path.parent.name or name in names:
                raise ValueError("name duplicado ou diferente da pasta")
            names.add(name)
            desc = data.get("description")
            if not isinstance(desc, str) or not 1 <= len(desc) <= 300:
                raise ValueError("description deve ter 1–300 caracteres")
            if not parts[2].strip():
                raise ValueError("corpo vazio")
            if rel == "SKILL.md":
                rows.append({"path": rel, "name": name, "category": "hub", "title": "LegalBR", "status": "protocolo"})
                continue
            if data.get("sourcePath") != "legalbr/" + rel:
                raise ValueError("sourcePath não corresponde ao arquivo real")
            if not isinstance(data.get("version"), int) or isinstance(data["version"], bool) or data["version"] < 1:
                raise ValueError("version deve ser inteiro positivo")
            if data.get("status") not in {"vigente", "alterada", "superada", "a conferir"}:
                raise ValueError("status inválido")
            for required in ("verifiedAt", "sources"):
                if required not in data:
                    raise ValueError(f"campo ausente: {required}")
            verified = iso_date(data.get("verifiedAt"))
            reviewed = iso_date(data.get("reviewedAt"))
            sources = data.get("sources")
            if not isinstance(sources, list):
                raise ValueError("sources deve ser lista")
            for source in sources:
                url = urlparse(source)
                host = url.hostname or ""
                if url.scheme != "https" or not any(host == suffix or host.endswith("." + suffix) for suffix in OFFICIAL):
                    raise ValueError("fonte de revisão não é URL HTTPS oficial")
            if verified and not sources:
                raise ValueError("verifiedAt exige sources")
            if data["status"] == "vigente" and not verified:
                raise ValueError("vigente exige revisão integral")
            if reviewed and (not data.get("reviewScope") or not sources):
                raise ValueError("revisão parcial exige escopo e fontes")
            row = {field: data.get(field, "") for field in FIELDS}
            row.update(path=rel, verifiedAt=verified or "", reviewedAt=reviewed or "")
            rows.append(row)
        except (ValueError, TypeError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
    return rows, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="gravar indice.tsv")
    mode.add_argument("--check", action="store_true", help="conferir índice sem alterar arquivos")
    args = parser.parse_args()
    rows, errors = catalog()
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row.get(key) if row.get(key) not in (None, "") else "-" for key in FIELDS})
    index = ROOT / "indice.tsv"
    if not errors and args.write:
        index.write_text(stream.getvalue(), encoding="utf-8")
    elif not errors and (not index.exists() or index.read_text(encoding="utf-8") != stream.getvalue()):
        errors.append("indice.tsv ausente ou desatualizado; executar --write")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(json.dumps({"skills": len(rows), "formas": sum(r["path"].startswith("forma/") for r in rows), "materias": sum(r["path"].startswith("materia/") for r in rows), "verified": sum(bool(r.get("verifiedAt")) for r in rows), "partial": sum(bool(r.get("reviewedAt")) for r in rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
