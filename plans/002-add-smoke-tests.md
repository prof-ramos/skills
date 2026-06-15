# Plan 002: Adicionar smoke tests com pytest para o KHAOS Activation Kernel

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat cee3861..HEAD -- ollama-godmode/godmode-kit/`
> Se qualquer arquivo mudou desde cee3861, STOP e reporte.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: plan 001 (a função precisa ter parâmetros limpos para ser testável)
- **Category**: tests
- **Planned at**: commit `cee3861`, 2026-06-15

## Why this matters

O KHAOS Activation Kernel tem zero testes automatizados. Nenhum smoke test, nenhum teste unitário, nenhum CI. Toda mudança (planos 001, 003, 004) só pode ser verificada manualmente, e não há como saber se algo quebrou sem rodar o `activate.py` de verdade (o que consome API calls).

Um smoke test mínimo cobre: dry-run sem erros, validação de provider/estratégias, modo interativo. Planos 003 e 004 dependem desta verificação.

## Current state

Arquivo: `ollama-godmode/godmode-kit/activate.py` (~600 linhas, função `activate_khaos()` como god function)

Nenhum diretório `tests/` existe. Nenhum `pyproject.toml` ou `pytest.ini`. Dependências só mencionadas no README.

Estrutura do kit:
```
godmode-kit/
├── activate.py
├── SOUL.md
├── .khos.env (gitignorado)
├── khos.env.example
├── .khos_state.json
├── .gitignore
├── README.md
└── templates/
    └── prefill.json
```

## Commands you will need

| Purpose   | Command                              | Expected on success |
|-----------|--------------------------------------|---------------------|
| Install   | `pip install pytest`                 | exit 0              |
| Tests     | `python3 -m pytest tests/ -v`        | all pass            |

## Scope

**In scope:**
- `ollama-godmode/godmode-kit/pyproject.toml` (criar)
- `ollama-godmode/godmode-kit/tests/test_smoke.py` (criar)

**Out of scope** (NÃO toque):
- `activate.py` (plano 001 cuida dos bugs)
- `templates/prefill.json`, `.khos.env`, `.khos_state.json`, `README.md`

## Git workflow

- Branch: `add/khaos-smoke-tests`
- Um commit: `test: add smoke tests for KHAOS activation kernel`
- Não faça push nem PR a menos que instruído.

## Steps

### Step 1: Criar `pyproject.toml` na raiz do godmode-kit

Crie `ollama-godmode/godmode-kit/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.backends._legacy:_Backend"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.setuptools.packages.find]
where = ["."]
include = ["activate*"]
```

**Verifique**: `test -f ollama-godmode/godmode-kit/pyproject.toml` → exit 0

### Step 2: Criar diretório `tests/`

```bash
mkdir -p /Users/gabrielramos/projetos/skills/ollama-godmode/godmode-kit/tests
```

**Verifique**: `test -d ollama-godmode/godmode-kit/tests` → exit 0

### Step 3: Criar `tests/__init__.py`

Arquivo vazio em `ollama-godmode/godmode-kit/tests/__init__.py`.

**Verifique**: `test -f ollama-godmode/godmode-kit/tests/__init__.py` → exit 0

### Step 4: Criar `tests/test_smoke.py`

Crie `ollama-godmode/godmode-kit/tests/test_smoke.py`:

```python
"""Smoke tests for KHAOS GodMode Activation Kernel.

All tests run via dry_run=True — no real provider is contacted.
"""

import sys
import os
from pathlib import Path

_KIT_DIR = Path(__file__).resolve().parent.parent
if str(_KIT_DIR) not in sys.path:
    sys.path.insert(0, str(_KIT_DIR))

import pytest
from activate import activate_khaos, DEFAULT_PROVIDERS, TEMPLATES


class TestCLIProviderDefaults:
    def test_known_providers(self):
        assert "ollama-cloud" in DEFAULT_PROVIDERS
        assert "openai" in DEFAULT_PROVIDERS
        assert "anthropic" in DEFAULT_PROVIDERS
        assert "ollama-local" in DEFAULT_PROVIDERS
        assert "openrouter" in DEFAULT_PROVIDERS
        assert "xai" in DEFAULT_PROVIDERS

    def test_ollama_cloud_defaults(self):
        p = DEFAULT_PROVIDERS["ollama-cloud"]
        assert p["default_model"] == "gemma4:31b"
        assert p["base_url"] == "https://ollama.com/v1"
        assert p["api_key_env"] == "OLLAMA_API_KEY"

    def test_openai_defaults(self):
        p = DEFAULT_PROVIDERS["openai"]
        assert p["default_model"] == "gpt-4o"
        assert p["base_url"] == "https://api.openai.com/v1"

    def test_ollama_local_no_key_env(self):
        p = DEFAULT_PROVIDERS["ollama-local"]
        assert p["api_key_env"] is None


class TestStrategyTemplates:
    def test_all_strategies_present(self):
        required = {"refusal_inversion", "og_godmode", "direct_godmode", "pliny_love"}
        assert required.issubset(set(TEMPLATES.keys()))

    def test_strategies_non_empty(self):
        for name, prompt in TEMPLATES.items():
            assert len(prompt) > 50, f"Strategy '{name}' is too short ({len(prompt)} chars)"


class TestDryRun:
    @pytest.fixture(autouse=True)
    def _ensure_api_key(self):
        if not os.getenv("OLLAMA_API_KEY"):
            os.environ["OLLAMA_API_KEY"] = "test-dummy-key"
        yield

    def test_dry_run_ollama_cloud(self, capsys):
        result = activate_khaos(
            provider="ollama-cloud",
            model="gemma4:31b",
            api_key=None,
            base_url=None,
            strategy="refusal_inversion",
            dry_run=True,
            interactive=False,
            honcho_key=None,
            honcho_workspace=None,
        )
        assert result is None

    def test_dry_run_output_contains_message(self, capsys):
        activate_khaos(
            provider="ollama-cloud",
            model="gemma4:31b",
            api_key=None,
            base_url=None,
            strategy="refusal_inversion",
            dry_run=True,
            interactive=False,
            honcho_key=None,
            honcho_workspace=None,
        )
        captured = capsys.readouterr()
        assert "Dry run complete" in captured.out

    def test_dry_run_openai(self, capsys):
        activate_khaos(
            provider="openai",
            model="gpt-4o",
            api_key="sk-test-fake",
            base_url=None,
            strategy="og_godmode",
            dry_run=True,
            interactive=False,
            honcho_key=None,
            honcho_workspace=None,
        )
        captured = capsys.readouterr()
        assert "Dry run complete" in captured.out

    def test_dry_run_honcho_demo(self, capsys):
        activate_khaos(
            provider="ollama-cloud",
            model="gemma4:31b",
            api_key=None,
            base_url=None,
            strategy="refusal_inversion",
            dry_run=True,
            interactive=False,
            honcho_key="",
            honcho_workspace="khaos",
        )
        captured = capsys.readouterr()
        assert "Dry run complete" in captured.out
```

**Verifique**: `python3 -c "compile(open('ollama-godmode/godmode-kit/tests/test_smoke.py').read(), 'test_smoke.py', 'exec'); print('OK')"` → `OK`

### Step 5: Rodar os testes

```bash
cd /Users/gabrielramos/projetos/skills/ollama-godmode/godmode-kit
python3 -m pytest tests/ -v
```

**Esperado**: Todos os testes passam. Se algum falhar, ajuste o teste (pode ser parâmetro faltando se o plano 001 ainda não foi aplicado).

### Step 6: Verificar gitignore

```bash
cd /Users/gabrielramos/projetos/skills
git check-ignore ollama-godmode/godmode-kit/pyproject.toml
```
→ Sem output (não ignorado).

## Done criteria

- [ ] `test -f ollama-godmode/godmode-kit/pyproject.toml` → exit 0
- [ ] `test -f ollama-godmode/godmode-kit/tests/test_smoke.py` → exit 0
- [ ] `python3 -m pytest ollama-godmode/godmode-kit/tests/ -v` → pelo menos 8 testes passam
- [ ] `git check-ignore ollama-godmode/godmode-kit/pyproject.toml` → sem output
- [ ] `plans/README.md` status row atualizado para "DONE"

## STOP conditions

- `activate.py` mudou desde cee3861 (drift check falhou).
- `python3 -m pytest` não está disponível após `pip install pytest`.
- Algum teste requer modificar `activate.py` ou arquivos fora do escopo.
- O dry-run test cria conexão real com a API.

## Maintenance notes

- Quando `activate_khaos()` ganhar novos parâmetros (plano 004), atualizar os testes dry-run.
- Quando KHAOS migrar para repo próprio (`prof-ramos/Khaos`), mover `pyproject.toml` e `tests/` para a raiz.