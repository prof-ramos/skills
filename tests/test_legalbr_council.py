"""Exercise real local retrieval. These tests do not validate legal conclusions."""
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/agent-workflows/legalbr-council/scripts/select_skills.py'
spec = importlib.util.spec_from_file_location('council_select', SCRIPT)
selector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selector)


class RetrievalTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'legalbr'
        (self.root / 'forma').mkdir(parents=True)
        (self.root / 'materia').mkdir()
        self.write('materia/administrativo/remocao', 'Remoção por saúde', ['junta médica', 'transferência'], 'corpo quasarxyz')
        self.write('materia/civil/remocao', 'Remoção contratual', ['transferência'], 'outro conteúdo')
        self.write('forma/recurso', 'Recurso administrativo', ['recurso'], 'minuta de recurso')

    def write(self, path, title, triggers, body):
        target = self.root / path / 'SKILL.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        category = path.split('/')[0]
        area = path.split('/')[1] if category == 'materia' else None
        name = path.split('/')[-1]
        text = f'---\nid: "id-{path}"\nname: "{name}"\ntitle: "{title}"\ncategory: "{category}"\nmateria: {json.dumps(area)}\nversion: 2\ntriggers:\n'
        text += ''.join(f'  - {json.dumps(t, ensure_ascii=False)}\n' for t in triggers)
        text += f'description: "{title}"\n---\n{body}\n'
        target.write_text(text)
        return target

    def index(self):
        rows, _ = selector.corpus(self.root)
        stream = io.StringIO()
        writer = csv.DictWriter(stream, ['path','name','title','materia','category','version'], delimiter='\t')
        writer.writeheader()
        for path, meta in rows.items():
            writer.writerow({'path': path, **{k:meta.get(k) or '-' for k in writer.fieldnames if k != 'path'}})
        (self.root / 'indice.tsv').write_text(stream.getvalue())

    def test_area_disambiguation_and_explicit_form(self):
        result = selector.select(self.root, 'remoção saúde', area='administrativo', form='recurso', limit=2)
        self.assertEqual([r['path'] for r in result['selected']], ['legalbr/materia/administrativo/remocao/SKILL.md','legalbr/forma/recurso/SKILL.md'])
        self.assertTrue(result['index'].startswith('absent'))

    def test_index_current_stale_missing_and_malformed_produce_same_selection(self):
        expected = selector.select(self.root, 'remoção')['selected']
        self.index()
        self.assertTrue(selector.select(self.root, 'remoção')['index'].startswith('current'))
        # Mutation of metadata with same file set invalidates existing index.
        self.write('materia/administrativo/remocao', 'Remoção alterada', ['junta médica'], 'corpo')
        stale = selector.select(self.root, 'remoção')
        self.assertTrue(stale['index'].startswith('stale'))
        (self.root / 'indice.tsv').unlink()
        absent = selector.select(self.root, 'remoção')
        self.assertEqual(stale['selected'], absent['selected'])
        (self.root / 'indice.tsv').write_text('wrong\tcolumns\nnot-a-path\tunknown\n')
        self.assertEqual(selector.select(self.root, 'remoção')['selected'], absent['selected'])
        self.assertEqual(len(expected), len(absent['selected']))

    def test_index_missing_added_and_duplicate_entries_are_stale(self):
        self.index()
        p = self.root / 'indice.tsv'
        original = p.read_text()
        for value in (original.splitlines()[0]+'\n', original+original.splitlines()[1]+'\n'):
            p.write_text(value)
            self.assertTrue(selector.select(self.root, 'remoção')['index'].startswith('stale'))
        p.write_text(original)
        self.write('materia/administrativo/novo', 'Remoção adicional', [], 'texto')
        self.assertTrue(selector.select(self.root, 'remoção')['index'].startswith('stale'))

    def test_provenance_matches_actual_text_and_version(self):
        row = selector.select(self.root, 'saúde', limit=1, include_content=True)['selected'][0]
        data = (self.root.parent / row['path']).read_bytes()
        self.assertEqual(row['sha256'], hashlib.sha256(data).hexdigest())
        self.assertEqual(row['content'].encode(), data)
        self.assertEqual(row['version'], '2')
        self.assertEqual(row['id'], 'id-materia/administrativo/remocao')
        self.assertEqual(row['legal_verification'], 'not performed')

    def test_body_fallback_and_no_result_do_not_invent_skill(self):
        row = selector.select(self.root, 'quasarxyz')['selected'][0]
        self.assertEqual(row['basis'], 'body fallback')
        self.assertNotIn('content', row)
        self.assertEqual(selector.select(self.root, 'nonexistentuniquetoken')['selected'], [])

    def test_empty_query_unknown_form_area_and_limit_rejected(self):
        for args in ({'query':'para uma'}, {'query':'saude','area':'missing'}, {'query':'saude','form':'missing'}, {'query':'saude','limit':0}, {'query':'saude','limit':13}):
            with self.subTest(args=args), self.assertRaises(ValueError):
                selector.select(self.root, **args)

    def test_limit_bounds_and_determinism(self):
        first = selector.select(self.root, 'remoção', limit=1)
        self.assertEqual(len(first['selected']),1)
        self.assertEqual(first, selector.select(self.root, 'remoção', limit=1))
        only_form = selector.select(self.root, 'saúde', limit=1, form='recurso')['selected']
        self.assertEqual([r['name'] for r in only_form], ['recurso'])

    def test_unsupported_metadata_reported_and_external_symlink_not_read(self):
        malformed = self.write('materia/civil/invalid', 'Objeto', [], 'text')
        malformed.write_text(malformed.read_text().replace('title: "Objeto"','title: {nested: value}'))
        external = Path(self.temp.name) / 'private.md'
        external.write_text('PRIVATE SENTINEL DO NOT READ')
        link = self.root / 'materia/civil/link/SKILL.md'
        link.parent.mkdir()
        link.symlink_to(external)
        result = selector.select(self.root, 'remoção')
        self.assertEqual(len(result['skipped_paths']),2)
        self.assertNotIn('PRIVATE SENTINEL',json.dumps(result))

    def test_cli_does_not_echo_input_or_create_artifacts(self):
        before = set(self.root.rglob('*'))
        query = 'remoção PRIVATE_SENTINEL_12345'
        run = subprocess.run([sys.executable,str(SCRIPT),'--catalog',str(self.root),'--limit','1'],input=query,text=True,capture_output=True,check=True)
        self.assertNotIn('PRIVATE_SENTINEL',run.stdout+run.stderr)
        self.assertEqual(len(json.loads(run.stdout)['selected']),1)
        self.assertEqual(before,set(self.root.rglob('*')))
        bad = subprocess.run([sys.executable,str(SCRIPT),'--catalog',str(self.root),'--area','PRIVATE_SENTINEL_12345','--query','saúde'],text=True,capture_output=True)
        self.assertEqual(bad.returncode,2)
        self.assertNotIn('PRIVATE_SENTINEL',bad.stdout+bad.stderr)


class ActualCatalogueTest(unittest.TestCase):
    def test_real_administrative_request_retrieves_matter_and_form(self):
        result = selector.select(ROOT/'legalbr','remoção por motivo de saúde junta médica oficial',area='administrativo',form='recurso-administrativo-geral',limit=3,include_content=True)
        self.assertEqual(result['scanned_headers'],2155)
        self.assertEqual(result['skipped_paths'],[])
        self.assertTrue(result['index'].startswith('current'))
        names = [r['name'] for r in result['selected']]
        self.assertEqual(names[0],'remocao-redistribuicao-servidor')
        self.assertIn('recurso-administrativo-geral',names)
        self.assertEqual(len(names),3)
        for row in result['selected']:
            self.assertEqual(row['content'],(ROOT/row['path']).read_text())


if __name__ == '__main__':
    unittest.main()
