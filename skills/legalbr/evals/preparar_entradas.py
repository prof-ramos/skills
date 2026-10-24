#!/usr/bin/env python3
"""Exporta contexto e entradas cegas. Não executa modelo nem pontua respostas."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CONTEXT_PATHS = (
    'legalbr/SKILL.md',
    'legalbr/references/verificacao.md',
    'skills/legalbr/SKILL.md',
    'skills/legalbr/references/fluxos-operacionais.md',
    'legalbr/materia/contratos/nda-acordo-confidencialidade/SKILL.md',
    'legalbr/materia/digital-dados/cookies-consentimento-anpd-guia/SKILL.md',
)


def prepare(ref, output):
    sha = subprocess.check_output(['git', 'rev-parse', '--verify', ref + '^{commit}'], cwd=ROOT, text=True).strip()
    def read(path):
        return subprocess.check_output(['git', 'show', sha + ':' + path], cwd=ROOT)
    files = {path: read(path) for path in CONTEXT_PATHS}
    rubric = read('skills/legalbr/evals/cenarios.json')
    cases = json.loads(rubric)['casos']
    output.mkdir(parents=True, exist_ok=False)
    context = '\n\n'.join('## FILE: ' + path + '\n' + content.decode() for path, content in files.items())
    (output / 'context.md').write_text(context, encoding='utf-8')
    for name, subset in [('nda', cases[:5]), ('cookies', cases[5:])]:
        (output / (name + '-inputs.json')).write_text(json.dumps([
            {'id': case['id'], 'entrada': case['entrada']} for case in subset
        ], ensure_ascii=False, indent=2), encoding='utf-8')
    manifest = {'commit': sha, 'sha256': {path: hashlib.sha256(content).hexdigest() for path, content in files.items()}}
    manifest['rubrica_sha256'] = hashlib.sha256(rubric).hexdigest()
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref', required=True, help='Commit/ref Git com a skill e rubricas')
    parser.add_argument('--output', required=True, type=Path, help='Novo diretório; não sobrescreve')
    args = parser.parse_args()
    prepare(args.ref, args.output)
