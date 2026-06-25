# autoreview-agnostic

Porte idiomático do skill **`autoreview`** do [OpenClaw](https://github.com/openclaw/openclaw/tree/main/.agents/skills/autoreview)
para **OpenCode** e **Claude Code**. Preserva a intenção funcional do original
(revisão de closeout estruturada, *advisory*, read-only, com verificação de cada
finding e disciplina de escopo) e adapta estrutura, comandos, arquivos e convenções
para cada ferramenta — sem portar literalmente o helper Python de 52 KB específico
do ecossistema OpenClaw/steipete.

## Conteúdo

| Caminho | Descrição |
|---|---|
| `analysis/ANALYSIS.md` | Análise técnica do skill original + decisões + docs consultadas |
| `analysis/MATRIX.md` | Matriz comparativa OpenClaw × OpenCode × Claude Code |
| `opencode/` | Versão idiomática para OpenCode (subagent + command + skill) |
| `claude-code/` | Versão idiomática para Claude Code (subagent + slash command + skill) |
| `shared/` | Arquivos compartilhados entre as duas versões (schema, rubric, helper) |
| `README.md` | Este índice |

> **Sync note:** `shared/` is the single source of truth. After editing any shared file
> (schema.json, rubric.md, diff-bundle.sh), copy it to both platform copies:
> `opencode/skills/autoreview/` and `claude-code/.claude/skills/autoreview/`. There is
> no automated sync — changes must be propagated manually to keep the three copies
> identical. A future `Makefile` or CI check could automate this.

## Árvore final

```
autoreview-agnostic/
├── README.md
├── analysis/
│   ├── ANALYSIS.md
│   └── MATRIX.md
├── shared/                              # base única de verdade, copiada para cada versão
│   ├── schema.json                      # contrato de saída JSON (findings + verdict)
│   ├── rubric.md                        # o que reportar / rejeitar / scope governor
│   └── diff-bundle.sh                    # seleção read-only do bundle (local|branch|commit)
├── opencode/
│   ├── README.md
│   ├── opencode.json                    # command /autoreview (agent: autoreview) + skills.paths + instructions
│   ├── AGENTS.md
│   ├── agent/
│   │   └── autoreview.md                # subagent standalone (frontmatter mode/permission + prompt)
│   ├── command/
│   │   └── autoreview.md                # slash command /autoreview
│   └── skills/autoreview/
│       ├── SKILL.md
│       ├── references/{schema.json, rubric.md}
│       └── scripts/diff-bundle.sh
└── claude-code/
    ├── README.md
    └── .claude/
        ├── agents/autoreview.md         # subagent read-only (frontmatter name/tools/model + prompt)
        ├── commands/autoreview.md        # slash command /autoreview (delega ao subagent)
        └── skills/autoreview/
            ├── SKILL.md
            ├── references/{schema.json, rubric.md}
            └── scripts/diff-bundle.sh
```

## Resumo do `autoreview` original

Skill de **closeout** do OpenClaw: revisão de código estruturada sobre um bundle de
mudança, executada por um engine CLI externo (`codex` default, `claude`, `droid`,
`copilot`), com saída validada contra um schema JSON. Contrato: advisory; verificar
cada finding; rejeitar especulativo/amplo/irrealista; menor fix no boundary correto;
Scope Governor (freeze de baseline, classificação in-scope/follow-up/stop-and-
escalate, parada após 2 ciclos sem convergência); freeze discipline em release
branches; nunca trocar engine/modelo; nunca revisores aninhados/painéis; não push
só para revisar. Saída: `{findings[], overall_correctness, overall_explanation,
overall_confidence}` com findings `{title, body, priority(P0-P3), confidence,
category, code_location}`. Helper Python de 52 KB orquestra bundle + engines +
validação; usa `gitcrawl` para proveniência.

## Decisões técnicas (síntese)

1. **Não portar o helper Python.** O motor de revisão, em cada ferramenta, é o
   **agente nativo** com tools de leitura. `diff-bundle.sh` cobre só seleção de
   target (read-only, sem engines externos).
2. **Schema compartilhado** (`shared/schema.json`), estendido do original com
   `style` + `documentation` (categorias pedidas), `suggested_fix`, `end_line`,
   `function`.
3. **Rubric compartilhada** (`shared/rubric.md`) — fonte única do que
   reportar/rejeitar, preservando o contrato OpenClaw.
4. **OpenCode**: subagent standalone em `.opencode/agent/autoreview.md`
   (`mode: subagent`, `edit: deny`, bash read-only) + command `/autoreview` +
   skill. (Incerteza registrada sobre campos do frontmatter de agente-arquivo;
   fallback documentado via `opencode.json`.)
5. **Claude Code**: subagent `.claude/agents/autoreview.md` (tools read-only,
   `Bash` restrito por instrução a git/gh read-only + helper) + slash command
   `/autoreview` (delega via Task tool) + skill.
6. **Segurança**: revisor estritamente read-only; nunca expor/substituir secrets;
   nunca commit/push automático; nunca dados externos além de lookups visíveis;
   findings de segurança só com risco concreto e acionável.

## Como instalar

**OpenCode**: copie `opencode/` para a raiz do projeto (mescle `opencode.json`),
`chmod +x .opencode/skills/autoreview/scripts/diff-bundle.sh`.

**Claude Code**: copie `claude-code/.claude/` para a raiz do projeto (ou para
`~/.claude/` para uso global), `chmod +x .claude/skills/autoreview/scripts/diff-bundle.sh`.

Detalhes em `opencode/README.md` e `claude-code/README.md`.

## Como usar

**OpenCode**: `/autoreview [local|branch <base>|commit <ref>|auto]`
**Claude Code**: `/autoreview [local|branch <base>|commit <ref>|auto]` (delega ao
subagent `autoreview`) ou Task tool com `subagent_type: autoreview`.

Saída: um objeto JSON único (schema em `references/schema.json`) + resumo humano.

## Como validar

```bash
# frontmatters + JSON
uv run --with pyyaml python3 - <<'PY'
import yaml, json
for p in ["claude-code/.claude/agents/autoreview.md","claude-code/.claude/commands/autoreview.md","claude-code/.claude/skills/autoreview/SKILL.md","opencode/command/autoreview.md","opencode/agent/autoreview.md","opencode/skills/autoreview/SKILL.md"]:
    yaml.safe_load(open(p).read().split('---')[1]); print("FM OK", p)
for p in ["opencode/opencode.json","shared/schema.json"]:
    json.load(open(p)); print("JSON OK", p)
PY
# helper
bash -n shared/diff-bundle.sh && bash shared/diff-bundle.sh --mode commit --commit HEAD | head
# dentro de cada ferramenta, no projeto alvo:
#   OpenCode:     /autoreview commit HEAD
#   Claude Code:  /autoreview commit HEAD
```

## Limitações

- **Sem enforcement de schema no runtime** das ferramentas: a saída estruturada é
  garantida por prompt + schema em `references/`. Se vier texto extra, descarte e
  reexecute.
- **Engine = agente nativo** (não CLI externo como no OpenClaw); "painéis
  multi-reviewer" exigem múltiplos agentes configurados manualmente.
- **Proveniência de regressão** sem `gitcrawl`: usa blame/commit do git.
- **`diff-bundle.sh` não faz `git fetch`**: se a base do PR não estiver resolvida
  localmente, falha fechado (exit 3) com instruções. Também falha com exit 1 se
  executado fora de um repositório git.
- **Incerteza OpenCode** sobre campos de frontmatter de agente-arquivo (fallback
  documentado via `opencode.json`; se `mode: subagent` não for reconhecido no
  frontmatter do `.md`, defina o agente em `opencode.json` com
  `prompt: "{file:./.opencode/agent/autoreview.md}"`).
- **Claude Code**: `Bash` é restrito por instrução no prompt do subagent (não por
  enforcement de harness); para enforcement mais forte, veja o exemplo de hook
  `PreToolUse` em `claude-code/README.md`.

## Checklist final de conformidade

- [x] Resumo do `autoreview` original (`analysis/ANALYSIS.md`)
- [x] Fontes/documentação consultadas no Context7 (`analysis/ANALYSIS.md`)
- [x] Matriz comparativa OpenClaw × OpenCode × Claude Code (`analysis/MATRIX.md`)
- [x] Árvore final dos arquivos propostos (acima)
- [x] Conteúdo completo dos arquivos criados (em `opencode/` e `claude-code/`)
- [x] Instruções de instalação e uso (`opencode/README.md`, `claude-code/README.md`)
- [x] Comandos de validação (seção *Como validar* aqui e nos READMEs)
- [x] Limitações e decisões técnicas (`analysis/ANALYSIS.md` + seção *Limitações*)
- [x] Foco em bugs reais, regressões, segurança, manutenção, estilo, testes,
  documentação, sugestões acionáveis (rubric + schema com 7 categorias)
- [x] **Segurança**: revisor read-only; nunca expor/substituir secrets; nunca
  commit/push automático; nunca dados externos sem instrução; nunca editar fora do
  escopo; nunca mascarar falhas de validação; nunca sugerir correções inseguras
- [x] Fatos (docs Context7) separados de inferências técnicas (incertezas marcadas)
- [x] Validação executada: frontmatters YAML válidos, JSONs válidos, helper
  `bash -n` ok, smoke `--mode commit` ok, args inválidos fail-closed

## Segurança

- Revisor **estritamente read-only** em ambas as versões (OpenCode `edit: deny` +
  allowlist bash; Claude Code `tools` read-only + prompt que proíbe mutação).
- Nunca edita, escreve, commita ou faz push.
- Nunca substitui/expõe/transmite secrets; se encontrar um, reporta como finding
  `security` **sem reproduzir o valor**.
- Nunca envia dados a serviços externos além de lookups read-only visíveis ao
  usuário.
- Nunca modifica arquivos fora do projeto revisado.
- Separa fatos (código/docs lidos) de inferências.
- Nunca mascara falhas de validação ou sugere correções inseguras.