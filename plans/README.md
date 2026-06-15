# Implementation Plans — KHAOS GodMode Activation Kernel

Gerado pelo "improve" skill em 2026-06-15 para o repositório `prof-ramos/skills`, subdiretório `ollama-godmode/godmode-kit/`.

## Estratégia geral

1. **Corrigir bugs** (plans 001, 003) — sem testes, sem segurança para refatorar
2. **Adicionar testes** (plan 002) — verificação automatizada para tudo que vem depois
3. **Refatorar** (plan 004) — só depois de ter testes e parâmetros limpos

## Execution order & status

| Plan | Title | Priority | Effort | Depends on | Status |
|------|-------|----------|--------|------------|--------|
| 001 | Substituir `args` globais por parâmetros | P1 | S | — | TODO |
| 002 | Adicionar smoke tests (pytest) | P1 | S | 001 | TODO |
| 003 | Limitar query loop (sliding window) | P1 | S | 001 | TODO |
| 004 | Extrair query loop para `run_query_loop()` | P2 | M | 001, 002, 003 | TODO |

## Dependency notes

- **Plan 002** (testes) depende de **001** (parâmetros limpos) porque os testes dry-run chamam `activate_khaos()` com argumentos nomeados. Sem o fix, o código referencia `args` global que não existe em contexto de teste.
- **Plan 003** (sliding window) depende de **001** para garantir que a assinatura da função está estável antes de modificar o query loop.
- **Plan 004** (extração) depende de **001, 002, 003**: precisa de parâmetros limpos (001), testes para verificar regressão (002), e a sliding window já aplicada (003) para que a extração capture o query loop no estado final correto.

## Recomendação de execução

```
Plano 001 → commit → git push
Plano 002 → commit → git push
Plano 003 → commit → git push
Plano 004 → commit → git push
```

Cada plano é autocontido. Não pule ordens — o plano 004 depende estruturalmente das mudanças de 001, 002 e 003.

## Aviso de migração futura

Estes planos operam dentro de `ollama-godmode/godmode-kit/` no repo `prof-ramos/skills`. O destino final do KHAOS é o repo `prof-ramos/Khaos`. Quando a migração acontecer, mover:
- `activate.py` → `Khaos/activate.py` (ou `Khaos/khaos.py`)
- `tests/` → `Khaos/tests/`
- `pyproject.toml` → `Khaos/pyproject.toml`

Os scripts dentro de `ollama-godmode/` (auto_jailbreak.py, godmode_race.py, parseltongue.py) **ficam** em `skills/` como biblioteca de técnicas de jailbreak — não migram.

## Findings considered and rejected

- **Keardcoded model list** (ARCH-02): baixa prioridade — não justifica plano agora. Será resolvido naturalmente na migração para `Khaos`.
- **Sem pyproject.toml original** (DX-01): resolvido pelo plano 002 (cria o pyproject.toml como parte dos testes).
- **interactive_mode() duplica lógica** (DX-02): plano separado se houver tempo depois dos 4 principais.
- **.khos_state.json sem gitignore** (SEC-01): risco baixo (arquivo local, gitignorado pelo `.gitignore` do kit). Adicionar entradas no `.gitignore` como parte dos planos não vale o desvio.