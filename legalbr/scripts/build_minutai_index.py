#!/usr/bin/env python3
"""Build an optional SQLite FTS5 index from an external MinutaIA dataset."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def add_document(connection: sqlite3.Connection, kind: str, source_id: str, tribunal: str, title: str, text: str, metadata: dict) -> None:
    cursor = connection.execute(
        "INSERT INTO documents(kind, source_id, tribunal, title, text, metadata_json) VALUES (?, ?, ?, ?, ?, ?)",
        (kind, source_id, tribunal, title, text, json.dumps(metadata, ensure_ascii=False)),
    )
    connection.execute(
        "INSERT INTO documents_fts(rowid, kind, source_id, tribunal, title, text) VALUES (?, ?, ?, ?, ?, ?)",
        (cursor.lastrowid, kind, source_id, tribunal, title, text),
    )


def build(data_root: Path, output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(output)
    try:
        connection.executescript(
            """
            PRAGMA journal_mode = WAL;
            DROP TABLE IF EXISTS documents_fts;
            DROP TABLE IF EXISTS documents;
            DROP TABLE IF EXISTS index_meta;
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY,
                kind TEXT NOT NULL,
                source_id TEXT NOT NULL UNIQUE,
                tribunal TEXT NOT NULL,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            );
            CREATE VIRTUAL TABLE documents_fts USING fts5(
                kind UNINDEXED, source_id UNINDEXED, tribunal UNINDEXED, title, text,
                tokenize = 'unicode61'
            );
            CREATE TABLE index_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            """
        )
        count = 0
        juris_root = data_root / "jurisprudencia"
        for json_path in sorted(juris_root.glob("*/*.json")):
            text_path = json_path.with_suffix(".txt")
            if not text_path.exists():
                continue
            metadata = json.loads(json_path.read_text(encoding="utf-8"))
            text = text_path.read_text(encoding="utf-8").strip()
            court = json_path.parent.name
            source_id = f"{court}/{metadata.get('id', json_path.stem)}"
            add_document(connection, "jurisprudencia", source_id, court, text.splitlines()[0] if text else source_id, text, metadata)
            count += 1
        legislation_root = data_root / "legislacao" / "textos"
        for json_path in sorted(legislation_root.glob("*.json")):
            text_path = json_path.with_suffix(".txt")
            if not text_path.exists():
                continue
            metadata = json.loads(json_path.read_text(encoding="utf-8"))
            text = text_path.read_text(encoding="utf-8").strip()
            source_id = f"legislacao/{metadata.get('id', json_path.stem)}"
            add_document(connection, "legislacao", source_id, "federal", metadata.get("ementa") or metadata.get("numero") or source_id, text, metadata)
            count += 1
        connection.execute("INSERT INTO index_meta VALUES (?, ?)", ("document_count", str(count)))
        connection.execute("INSERT INTO index_meta VALUES (?, ?)", ("data_root", str(data_root)))
        connection.commit()
        return count
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.output.exists() and not args.overwrite:
        parser.error(f"arquivo já existe; use --overwrite: {args.output}")
    count = build(args.data_root.resolve(), args.output.resolve())
    print(f"índice criado: {count} documentos em {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
