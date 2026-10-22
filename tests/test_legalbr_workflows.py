"""Structural regressions only; behavioral scenarios require agent evaluation."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / 'skills/legalbr/SKILL.md'
FLOW = ROOT / 'skills/legalbr/references/fluxos-operacionais.md'
NDA = ROOT / 'legalbr/materia/contratos/nda-acordo-confidencialidade/SKILL.md'
COOKIES = ROOT / 'legalbr/materia/digital-dados/cookies-consentimento-anpd-guia/SKILL.md'
PROVENANCE = ROOT / 'legalbr/PROVENIENCIA-FLUXOS.md'

class LegalBRWorkflowTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        for path in (HUB, FLOW, NDA, COOKIES, PROVENANCE, *(p.parent/'references/PROVENIENCIA.md' for p in (HUB, NDA, COOKIES))):
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((path.parent / target.split('#')[0]).exists(), (path, target))

    def test_required_guardrails_and_fields(self):
        checks = {
            FLOW: ('desconhecido', 'não aplicável', 'Faixa aceitável', 'Redline', 'Fallback', 'Aprovador', 'Não assine', 'não instruções'),
            NDA: ('Pendente de informação', 'critérios', 'não significa', 'a designar', 'Não assine', 'não limites legais'),
            COOKIES: ('desconhecido', 'Inventário observado', 'server-side', 'revogar', 'Reteste', 'Não publique', 'baseados em consentimento'),
        }
        for path, terms in checks.items():
            content = path.read_text().casefold()
            for term in terms:
                self.assertIn(term.casefold(), content, (path, term))

    def test_canonical_ids_unchanged(self):
        self.assertIn('id: "c5988b17-14e8-4158-a8d3-11bf1578638c"', NDA.read_text())
        self.assertIn('id: "fb5a1a4b-3813-4928-96a0-7961ebcadac4"', COOKIES.read_text())

    def test_license_and_provenance(self):
        for skill in (HUB, NDA, COOKIES):
            self.assertIn('Version 2.0, January 2004', (skill.parent/'references/Apache-2.0.txt').read_text())
        self.assertIn('33d3dea41a341b341d4f5da2e8801ae0c89be2b8', PROVENANCE.read_text())

    def test_behavioral_scenarios_are_explicit(self):
        data = json.loads((ROOT/'skills/legalbr/evals/cenarios.json').read_text())
        cases = data['casos']
        self.assertEqual(len(cases), len({case['id'] for case in cases}))
        for case in cases:
            self.assertTrue(case['entrada'])
            self.assertGreaterEqual(len(case['deve']), 2)
        self.assertTrue({'nda-sem-texto', 'nda-baixo-risco', 'cookies-so-captura', 'compliance-evidencia-ausente'}.issubset({case['id'] for case in cases}))

if __name__ == '__main__':
    unittest.main()
