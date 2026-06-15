# Plan 001: Substituir referências a `args` global em `activate_khaos()` pelos parâmetros da função

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat cee3861..HEAD -- ollama-godmode/godmode-kit/activate.py`
> Se o arquivo mudou desde cee3861, compare os trechos de "Current state"
> contra o código atual antes de prosseguir. Se divergir, STOP.

## Status

- **Priority**: P1
- **Effort**: S (minutos)
- **Risk**: LOW
- **Depends on**: none
- **Category**: bug
- **Planned at**: commit `cee3861`, 2026-06-15

## Why this matters

A função `activate_khaos()` recebe todos os parâmetros que precisa (provider, model, api_key, strategy, etc.), mas dentro do corpo ela ignora dois deles e lê diretamente da variável global `args` — que só existe no bloco `if __name__ == "__main__"`.

Isso significa que se alguém chamar `activate_khaos()` programaticamente (de outro módulo, de um teste, de um `start.sh`), as flags `--list-models` e `--prefill` são lidas de `args`, que não existe, causando `AttributeError: 'NoneType' object has no attribute 'list_models'`.

Duas referências problemáticas:
- Linha 365: `if args.list_models:` — deveria ser o parâmetro `model` ou uma flag `list_models` passada como parâmetro
- Linha 391: `prefill = load_prefill(args.prefill)` — deveria usar o parâmetro `prefill` (que a função recebe mas se chama `strategy` — confuso, mas o caminho do prefill nunca chega)

## Current state

Arquivo: `ollama-godmode/godmode-kit/activate.py`

**Problema 1 — linha 365:**
```python
    # List models
    if args.list_models:
        return list_models(provider)
```

Aqui `args.list_models` referencia a variável global `args`. A função `activate_khaos` não recebe `list_models` como parâmetro. O único jeito de listar modelos é via `--list-models` na CLI.

**Problema 2 — linha 391:**
```python
    prefill = load_prefill(args.prefill)
```

Aqui `args.prefill` referencia a global. A função `activate_khaos` não recebe `prefill` como parâmetro. O parâmetro que sobra é `strategy` (string), não o caminho do prefill.

**Assinatura atual da função (linha 340):**
```python
def activate_khaos(provider, model, api_key, base_url, strategy,
                   dry_run, interactive, honcho_key, honcho_workspace):
```

**Chamada no `if __name__` (linhas 655-657):**
```python
    activate_khaos(args.provider, args.model, args.api_key, args.base_url,
                   args.strategy, args.dry_run, args.interactive,
                   args.honcho_api_key, args.honcho_workspace)
```

Nota: `args.list_models` e `args.prefill` não são passados — estão sendo ignorados na chamada.

**Convenção do repositório:** Módulo único de ~600 linhas, Python padrão, sem type hints. Funções têm docstrings. Args do CLI são definidos via argparse no bloco `if __name__`.

## Scope

**In scope** (os únicos arquivos que você deve modificar):
- `ollama-godmode/godmode-kit/activate.py`

**Out of scope** (NÃO toque, mesmo que pareçam relacionados):
- Qualquer outro arquivo no repositório
- `templates/prefill.json`
- `.khos.env`
- `.khos_state.json`

## Git workflow

- Branch: `fix/activate-khaos-args`
- Um único commit com mensagem: `fix: replace args globals with function parameters in activate_khaos()`
- Não faça push ou abra PR a menos que instruído.

## Steps

### Step 1: Adicionar parâmetros `list_models` e `prefill_path` à assinatura da função

No arquivo `activate.py`, localize a assinatura de `activate_khaos()` (linha ~340) e adicione dois parâmetros:

**Antes:**
```python
def activate_khaos(provider, model, api_key, base_url, strategy,
                   dry_run, interactive, honcho_key, honcho_workspace):
```

**Depois:**
```python
def activate_khaos(provider, model, api_key, base_url, strategy,
                   dry_run, interactive, honcho_key, honcho_workspace,
                   list_models=False, prefill_path=None):
```

**Verifique**: `python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"` → imprime `OK`

### Step 2: Substituir `args.list_models` pelo parâmetro `list_models`

Localize a linha:
```python
    if args.list_models:
        return list_models(provider)
```

Substitua por:
```python
    if list_models:
        return list_models(provider)
```

**Verifique**: `grep -n 'args\.list_models' ollama-godmode/godmode-kit/activate.py` → nenhuma ocorrência

### Step 3: Substituir `args.prefill` pelo parâmetro `prefill_path`

Localize a linha:
```python
    prefill = load_prefill(args.prefill)
```

Substitua por:
```python
    prefill = load_prefill(prefill_path)
```

**Verifique**: `grep -n 'args\.prefill' ollama-godmode/godmode-kit/activate.py` → nenhuma ocorrência

### Step 4: Atualizar a chamada no `if __name__`

Localize a chamada da função (linhas ~655-657):

**Antes:**
```python
    activate_khaos(args.provider, args.model, args.api_key, args.base_url,
                   args.strategy, args.dry_run, args.interactive,
                   args.honcho_api_key, args.honcho_workspace)
```

**Depois:**
```python
    activate_khaos(args.provider, args.model, args.api_key, args.base_url,
                   args.strategy, args.dry_run, args.interactive,
                   args.honcho_api_key, args.honcho_workspace,
                   list_models=args.list_models, prefill_path=args.prefill)
```

**Verifique**: `grep -n 'args\.list_models\|args\.prefill' ollama-godmode/godmode-kit/activate.py` → deve mostrar apenas esta linha (a chamada), nenhuma dentro do corpo da função

### Step 5: Verificar que `args.list_models` e `args.prefill` não são usados em nenhum outro lugar

**Verifique**: `grep -c 'args\.list_models\|args\.prefill' ollama-godmode/godmode-kit/activate.py` → deve retornar `1` (apenas a chamada na linha atualizada)

### Step 6: Verificar que o código ainda compila e o dry-run funciona

**Verifique**: 
```bash
cd /Users/gabrielramos/projetos/skills
python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"
```
→ imprime `OK`

**Verifique (dry-run sem .khos.env):**
```bash
cd /Users/gabrielramos/projetos/skills/ollama-godmode/godmode-kit
KHAOS_HONCHO_KEY="" python3 activate.py --dry-run --provider ollama-cloud --model gemma4:31b 2>&1 | tail -10
```
→ Mostra "Dry run complete. No API call made." (pode mostrar aviso de Honcho demo mode — isso é esperado)

## Test plan

Este plano não adiciona testes novos (o teste automatizado de regressão será o plano 002). A verificação é:
- Compilação Python OK
- `--dry-run` funciona sem crash
- A funcionalidade `--list-models` e `--prefill` continuam funcionando pela CLI (teste manual com `--dry-run`)

## Done criteria

Todos devem valer:

- [ ] `grep -n 'args\.list_models' ollama-godmode/godmode-kit/activate.py` retorna 0 ocorrências no *corpo da função* (apenas na chamada no `__main__`)
- [ ] `grep -n 'args\.prefill' ollama-godmode/godmode-kit/activate.py` retorna 0 ocorrências no *corpo da função* (apenas na chamada no `__main__`)
- [ ] `python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"` → `OK`
- [ ] `KHAOS_HONCHO_KEY="" python3 ollama-godmode/godmode-kit/activate.py --dry-run 2>&1 | grep -q "Dry run complete"` → exit 0
- [ ] `plans/README.md` status row atualizado para "DONE"

## STOP conditions

Pare e reporte se:

- O código em `activate.py` não corresponde aos trechos em "Current state" (o repo divergiu).
- A compilação Python falha após qualquer passo.
- `grep` após o passo 3 ainda encontra `args.prefill` ou `args.list_models` *dentro do corpo da função* (fora do `if __name__`).
- Você precisar modificar arquivos fora do escopo para fazer o plano funcionar.

## Maintenance notes

- Se no futuro mais flags forem adicionadas ao argparse, a chamada em `if __name__` deve sempre passar explicitamente `flag_name=args.flag_name` para garantir que a função não precise depender de globais.
- Quando o `activate_khaos()` for refatorado para extrair partes (plano 004), essa assinatura limpa vai facilitar a separação.