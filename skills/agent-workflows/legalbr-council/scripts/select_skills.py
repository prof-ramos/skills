#!/usr/bin/env python3
"""Local bounded LegalBR retrieval. No legal verification, network or query logging.

Python 3.10+, standard library. Reads YAML's scalar/list subset used by the
catalogue; unsupported search fields are rejected rather than misinterpreted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

FIELDS = {'id', 'name', 'title', 'materia', 'triggers', 'description', 'version', 'category'}
STOP = set('para como sobre pelo pela pelos pelas uma umas uns que com dos das por entre esse essa este esta quero preciso redigir elaborar analisar direito juridico juridica servidor servidores'.split())


def normalize(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(text)).lower() if not unicodedata.combining(c))


def tokens(text):
    return {t for t in re.findall(r'[a-z0-9]+', normalize(text)) if len(t) >= 3 and t not in STOP}


def scalar(value):
    value = value.strip()
    if value in ('null', '~', ''):
        return ''
    if value.startswith('"'):
        # Catalogue double-quoted scalar values use JSON-compatible escapes.
        return str(json.loads(value))
    if value.startswith("'"):
        if not value.endswith("'"):
            raise ValueError('unterminated scalar')
        return value[1:-1].replace("''", "'")
    if value.startswith(('[', '{', '&', '*', '!')):
        raise ValueError('unsupported scalar syntax')
    return value.split(' #', 1)[0].strip()


def metadata(path):
    """Read only frontmatter; never load unselected bodies into model context."""
    lines = []
    with path.open(encoding='utf-8') as stream:
        if stream.readline().strip() != '---':
            raise ValueError('missing frontmatter')
        for line in stream:
            if line.strip() == '---':
                break
            lines.append(line.rstrip('\n'))
            if sum(map(len, lines)) > 65536:
                raise ValueError('frontmatter too large')
        else:
            raise ValueError('unterminated frontmatter')
    result = {}
    i = 0
    while i < len(lines):
        match = re.match(r'^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$', lines[i])
        i += 1
        if not match or match[1] not in FIELDS:
            continue
        key, value = match.groups()
        if key in result:
            raise ValueError('duplicate search field')
        block = []
        while i < len(lines) and (lines[i].startswith(' ') or not lines[i].strip()):
            block.append(lines[i].strip())
            i += 1
        if key == 'triggers' and not value:
            if any(item and not item.startswith('- ') for item in block):
                raise ValueError('unsupported triggers')
            result[key] = ' '.join(scalar(item[2:]) for item in block if item)
        elif value in ('|', '|-', '>', '>-'):
            result[key] = ' '.join(block)
        else:
            result[key] = scalar(value)
    if not result.get('name'):
        raise ValueError('missing name')
    return result


def corpus(root):
    root = root.resolve()
    if not (root / 'forma').is_dir() or not (root / 'materia').is_dir():
        raise ValueError('catalogue requires forma/ and materia/ directories')
    records, skipped = {}, []
    for category in ('forma', 'materia'):
        for path in sorted((root / category).rglob('SKILL.md')):
            rel = path.relative_to(root).as_posix()
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                skipped.append(rel)
                continue
            try:
                records[rel] = metadata(path)
            except (ValueError, OSError, UnicodeError):
                skipped.append(rel)
    return records, skipped


def index_status(root, records):
    """TSV is advisory: check file coverage and every indexed search field.

    Missing triggers/description in the TSV are always read from frontmatter.
    No timestamps or trusted status flags stand in for actual metadata parity.
    """
    path = root / 'indice.tsv'
    if not path.exists():
        return 'absent: local metadata scan'
    try:
        with path.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream, delimiter='\t'))
        indexed = {}
        for row in rows:
            rel = row.get('path', '')
            if rel == 'SKILL.md':
                continue
            if rel in indexed:
                return 'stale: local metadata scan'
            indexed[rel] = row
        if indexed.keys() != records.keys():
            return 'stale: local metadata scan'
        for rel, meta in records.items():
            for key in ('name', 'title', 'materia', 'version', 'category'):
                if indexed[rel].get(key, '-') != (meta.get(key) or '-'):
                    return 'stale: local metadata scan'
        return 'current: TSV checked against local metadata'
    except (OSError, UnicodeError, csv.Error):
        return 'invalid: local metadata scan'


def select(root, query, *, area=None, form=None, limit=6, include_content=False):
    root = Path(root).resolve()
    if not 1 <= limit <= 12:
        raise ValueError('limit must be between 1 and 12')
    query_tokens = tokens(query)
    if not query_tokens:
        raise ValueError('query must contain substantive search terms')
    records, skipped = corpus(root)
    if area and not any(p.startswith(f'materia/{area}/') for p in records):
        raise ValueError('unknown area')
    form_path = f'forma/{form}/SKILL.md' if form else None
    if form_path and form_path not in records:
        raise ValueError('unknown form')
    ranked = []
    for rel, meta in records.items():
        if form_path and rel.startswith('forma/') and rel != form_path:
            continue
        if area and rel.startswith('materia/') and not rel.startswith(f'materia/{area}/'):
            continue
        high = tokens(' '.join(meta.get(k, '') for k in ('name', 'title', 'triggers')))
        low = tokens(' '.join(meta.get(k, '') for k in ('description', 'materia')))
        matched = query_tokens & (high | low)
        score = 4 * len(query_tokens & high) + len(query_tokens & low)
        if score:
            ranked.append((score, rel, 'metadata', sorted(matched)))
    # Fallback is disk-only; content reaches output solely for selected files.
    if not ranked:
        for rel in records:
            if form_path and rel.startswith('forma/') and rel != form_path:
                continue
            if area and rel.startswith('materia/') and not rel.startswith(f'materia/{area}/'):
                continue
            body = (root / rel).read_text(encoding='utf-8').split('---', 2)[-1]
            matched = query_tokens & tokens(body)
            if matched:
                ranked.append((len(matched), rel, 'body fallback', sorted(matched)))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    chosen = ranked[:limit]
    if form_path:
        # Explicit form reserves one slot even when query words describe only merit.
        chosen = [item for item in ranked if item[1] != form_path][:limit - 1]
        chosen.append(next((item for item in ranked if item[1] == form_path), (0, form_path, 'explicit form', [])))
    results = []
    for score, rel, basis, matched in chosen:
        content = (root / rel).read_text(encoding='utf-8')
        meta = metadata(root / rel)
        if meta != records[rel]:
            raise ValueError('catalogue changed during retrieval; retry')
        item = {'path': 'legalbr/' + rel, 'name': meta['name'], 'id': meta.get('id') or None,
                'version': meta.get('version') or None, 'sha256': hashlib.sha256(content.encode()).hexdigest(),
                'score': score, 'matched_terms': matched, 'basis': basis,
                'legal_verification': 'not performed'}
        if include_content:
            item['content'] = content
        results.append(item)
    return {'index': index_status(root, records), 'scanned_headers': len(records),
            'skipped_paths': skipped, 'selected': results, 'limit': limit,
            'warning': 'Lexical shortlist; review relevance and opposing theses. Catalogue is not an official legal source.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True, help='path to legalbr/')
    parser.add_argument('--query', help='generic legal terms only; omit to read stdin')
    parser.add_argument('--area', help='optional exact materia directory; omitted searches all areas')
    parser.add_argument('--form', help='optional exact forma slug; reserves one result slot')
    parser.add_argument('--limit', type=int, default=6)
    parser.add_argument('--include-content', action='store_true', help='output full selected files only')
    args = parser.parse_args(argv)
    try:
        result = select(args.catalog, args.query if args.query is not None else sys.stdin.read(),
                        area=args.area, form=args.form, limit=args.limit, include_content=args.include_content)
    except (ValueError, OSError, UnicodeError):
        parser.exit(2, 'Retrieval failed: check catalogue, scalar metadata, substantive query, area, form and limit.\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
