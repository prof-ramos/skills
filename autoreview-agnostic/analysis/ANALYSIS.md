# Análise do skill `autoreview` original (OpenClaw)

Fonte inspecionada: `openclaw/openclaw` @ commit `f0be8e7b6ee8618f5a8155e59274db489c7dc582`,
caminho `.agents/skills/autoreview/`.

## 1. Árvore de arquivos do skill original

```
.agents/skills/autoreview/
├── SKILL.md                      (14.747 bytes — contrato, escopo, modos, engines)
└── scripts/
    ├── autoreview                (52.630 bytes — helper Python de orquestração)
    ├── test-review-harness       (367 bytes — wrapper shell fino)
    ├── test-review-harness.ps1   (1.022 bytes — wrapper PowerShell para Windows)
    └── test-review-harness.py    (7.079 bytes — harness de smoke test)
```

## 2. Propósito

`autoreview` é um **skill de closeout** (verificação final antes de commit/ship).
Não é roteamento de aprovação (`auto_review` do Guardian); é revisão de código
estruturada sobre um bundle de mudança, executada por um engine de LLM externo,
com saída validada contra um schema JSON.

## 3. Entradas esperadas

- **Alvo da revisão** selecionado por `--mode`:
  - `local` / `uncommitted` — worktree suja (unstaged + staged + untracked).
  - `branch --base <ref>` — diff da branch vs base (default `origin/main`, ou
    `baseRefName` do PR via `gh pr view`).
  - `commit --commit <ref>` — um commit já landado (default `HEAD`).
  - `auto` (default) — escolhe `local` se houver patch sujo; senão base do PR; senão
    `origin/main`.
- Contexto extra opcional: `--prompt`, `--prompt-file`, `--dataset` (evidências).
- `--engine` codex (default) | claude | droid | copilot.
- Painéis: `--reviewers codex,claude` ou `--panel`; `--model`, `--thinking` por engine.

## 4. Saídas geradas

Objeto JSON único validado contra `SCHEMA`:

```json
{
  "findings": [
    {
      "title": "...",
      "body": "...",
      "priority": "P0|P1|P2|P3",
      "confidence": 0.0..1.0,
      "category": "bug|security|regression|test_gap|maintainability",
      "code_location": { "file_path": "...", "line": 1 }
    }
  ],
  "overall_correctness": "patch is correct | patch is incorrect",
  "overall_explanation": "...",
  "overall_confidence": 0.0..1.0
}
```

Saída humana em stdout (ou `--output`); JSON validado em `--json-output`. Heartbeats
em stderr (`review still running: <engine> elapsed=... pid=...`). Exit 0 = clean
(sem findings aceitos); exit nonzero = findings presentes.

## 5. Comandos/ferramentas invocadas

- `git` (diff, status, show, rev-parse, merge-base, ls-files) — resolvido só de
  entradas absolutas de `PATH`, nunca do checkout revisado.
- `gh pr view` — para resolver a base real do PR.
- Engines: `codex exec` (sandbox read-only, `--output-schema`), `claude`
  (`--output-format stream-json|json --json-schema`, `--allowedTools`),
  `droid exec`, `copilot` (`--output-format json`). Cada um com seu binário
  configurável via `--*-bin` ou env (`CODEX_BIN`, `CLAUDE_BIN`, etc.).
- `gitcrawl doctor` — reparo de cache portátil em erros de proveniência.

## 6. Instruções de sistema/prompt (contrato do SKILL.md)

Princípios centrais preservados:
- Saída **advisory** — nunca aplicar cegamente.
- **Verificar cada finding** lendo o caminho real de código e arquivos adjacentes;
  ler docs/source/types de dependências quando o finding depender de comportamento
  externo.
- **Rejeitar** edge cases irrealistas, riscos especulativos, rewrites amplos, fixes
  que supercomplicam o codebase.
- Preferir **menor fix no boundary de ownership correto**; sem refactor a menos que
  melhore claramente a classe do bug.
- Inspecionar **instâncias irmãs** do mesmo bug class no escopo do PR antes de fixar.
- **Scope Governor**: freeze de baseline antes da primeira revisão; classificação
  in-scope blocker / follow-up / stop-and-escalate; parar após 2 ciclos sem
  convergência; exceções críticas explícitas (data loss, crash, install break,
  security exposure).
- **Release branches**: freeze discipline; só release blockers/exact backports.
- Nunca trocar/sobrescrever o engine/modelo solicitado; retentar o mesmo se bater
  capacidade.
- Paciência: até 30 min por bundle; heartbeats são progresso saudável, não hang.
- Não invocar `codex review` built-in, reviewers aninhados ou painéis de dentro da
  revisão (um bundle, um engine, um resultado estruturado, para).
- Não push só para revisar; push só quando o usuário pediu ship/PR update.
- **Final Report**: comando usado, testes/proof executados, findings aceitos/rejeitados
  e por quê, resultado clean da última execução.

## 7. Dependências

- Python 3 (helper). `git`, `gh` (opcionais para auto-detecção). Pelo menos um engine
  CLI instalado (`codex` recomendado como default). `gitcrawl` para proveniência.

## 8. Premissas operacionais

- Repos git. Engine CLI instalado e no `PATH`. Worktree local limpa vs suja define o
  modo. `gh` autenticado para base de PR. Pathos fixos do `steipete/agent-scripts`
  referenciados literalmente no SKILL original.

## 9. Pontos do OpenClaw que NÃO podem ser copiados literalmente

- **Helper Python de 52 KB** (`scripts/autoreview`) — acopla-se a engines CLI
  específicas (Codex `--output-schema`, Claude `--json-schema`, droid, copilot),
  `gitcrawl`, pathos do `steipete/agent-scripts` (`/Users/steipete/Projects/...`,
  `~/.codex/skills/agent-scripts/`), sandboxes Codex, PowerShell shells. Portar isto
  literalmente quebra idiomacidade e amarra a instalações externas.
- **`agent-scripts` global paths** — hard-coded a uma máquina específica.
- **Engine default = Codex** — decisão de ecossistema OpenClaw; nas portas, o engine
  é o **próprio agente nativo** da ferramenta (OpenCode/Claude Code), não um CLI
  externo separado.
- **Categorias limitadas** (`bug, security, regression, test_gap, maintainability`) —
  o pedido explicita também `style` e `documentation`; estenderemos o schema.
- **`gitcrawl` provenance** — específico do ecossistema OpenClaw; não portar.

## 10. Partes reutilizáveis entre OpenClaw, OpenCode e Claude Code

- **Contrato de revisão** (advisory, verify-every-finding, reject-speculative,
  smallest-fix-at-boundary) — texto, portável.
- **Scope Governor / freeze discipline** — texto, portável.
- **Schema JSON estruturado** — porta literal (estendido com `style`,
  `documentation`, `suggested_fix`, `end_line`, `function`).
- **Rubric de categorias e rejeição** — portável.
- **Seleção de target** (`local` / `branch --base` / `commit`) — portável como
  script shell read-only (`shared/diff-bundle.sh`).
- **Final Report** — formato, portável.

## Decisões técnicas (síntese)

1. **Não portar o helper Python.** O motor de revisão, em cada ferramenta, é o
   agente nativo com tools de leitura. O script `diff-bundle.sh` cobre só a seleção
   de target (read-only, sem chamar engines externos).
2. **Schema compartilhado** em `shared/schema.json`, idêntico entre OpenCode e
   Claude Code, estendido conforme o pedido (categorias + `suggested_fix`).
3. **Rubric compartilhada** em `shared/rubric.md` — fonte única de verdade do que
   reportar/rejeitar, preservando a intenção do contrato OpenClaw.
4. **OpenCode**: subagent `autoreview` (mode `subagent`, `edit: deny`, bash
   read-only git) em `opencode/agent/autoreview.md` + config mínima em `opencode.json`
   + command `/autoreview` em `opencode/command/autoreview.md` que roda com aquele
   agente + skill `opencode/skills/autoreview/SKILL.md` com o playbook.
5. **Claude Code**: subagent `.claude/agents/autoreview.md` (tools read-only:
   `Read, Grep, Glob, Bash(git:*, gh pr view:*, gh pr diff:*)`, `WebFetch`,
   `WebSearch`) + slash command `.claude/commands/autoreview.md` + skill
   `.claude/skills/autoreview/SKILL.md` com o playbook completo.
6. **Segurança**: revisor é estritamente read-only (edit/write/commit/push
   proibidos); nunca expor/substituir secrets; nunca commit/push automático; nunca
   dados externos sem instrução explícita; findings de segurança só quando há risco
   concreto e acionável.

## Documentação consultada (Context7)

| Biblioteca | ID Context7 | Uso |
|---|---|---|
| OpenCode | `/anomalyco/opencode` | `opencode.json`, agentes (`mode`, `permission`), commands (`agent`, `model`, `$ARGUMENTS`), skills paths, AGENTS.md |
| OpenCode (site) | `/websites/opencode_ai` | formato `.md` de command/AGENTS.md, `$1`/`$2`, lazy loading de refs |
| Claude Code | `/anthropics/claude-code` | plugins: skills (`SKILL.md` frontmatter `name`/`description`, `scripts/`/`references/`), agents (`.claude/agents/`, `tools`, `model`), commands (`.claude/commands/`, `allowed-tools`, `argument-hint`, `$ARGUMENTS`, `Bash(git:*)`) |
| OpenClaw | `/openclaw/openclaw` | confirmação da estrutura `.agents/skills/` e do conteúdo do `SKILL.md` |

> Observação de incerteza: a doc do Context7 sobre OpenCode mostra agentes
> definíveis tanto em `opencode.json` (`agent` key) quanto em
> `.opencode/agent/<name>.md`; optamos pelo arquivo `.md` (mais idiomático para
> prompts longos) e mantemos uma entrada mínima em `opencode.json` para o command
> `/autoreview`. O Claude Code não documenta um mecanismo "invocar subagent a
> partir de command" direto — o command instrui o agente principal a delegar via
> ferramenta de agentes, e o subagent pode também ser invocado diretamente.