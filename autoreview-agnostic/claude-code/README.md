# autoreview — versão Claude Code

Port idiomático do skill `autoreview` do OpenClaw para **Claude Code**. Preserva a
intenção funcional (revisão de closeout estruturada, advisory, read-only, com
verificação de cada finding e disciplina de escopo) e adapta o mecanismo para os
construtos nativos do Claude Code: **subagent** (`.claude/agents/`), **slash
command** (`.claude/commands/`) e **skill** (`.claude/skills/`).

## Árvore de arquivos

```
claude-code/.claude/
├── agents/
│   └── autoreview.md                          # subagent read-only (frontmatter name/description/tools/model)
├── commands/
│   └── autoreview.md                          # slash command /autoreview (delega ao subagent)
└── skills/
    └── autoreview/
        ├── SKILL.md                           # playbook + scope governor + modos
        ├── references/
        │   ├── schema.json                    # contrato de saída JSON
        │   └── rubric.md                       # o que reportar / rejeitar
        └── scripts/
            └── diff-bundle.sh                 # seleção read-only do bundle de mudança
```

## Como instalar

1. Copie a pasta `.claude/` para a raiz do seu projeto (ou mescle nos diretórios
   `.claude/agents/`, `.claude/commands/`, `.claude/skills/` já existentes).
2. Garanta permissão de execução ao helper:
   `chmod +x .claude/skills/autoreview/scripts/diff-bundle.sh`.
3. (Opcional) Para instalação **global** (todos os projetos), copie para
   `~/.claude/agents/`, `~/.claude/commands/`, `~/.claude/skills/`.
4. (Opcional) ajuste o campo `model` em `.claude/agents/autoreview.md` para outro
   tier (default `sonnet`; use `opus` para revisões mais profundas).

## Como usar

```text
/autoreview                    # auto: dirty local → base do PR → origin/main
/autoreview local              # worktree suja (unstaged + staged + untracked)
/autoreview branch origin/main # diff da branch vs base
/autoreview commit HEAD        # um commit já landado
```

Ou invoque o subagent diretamente pela Task tool com `subagent_type: autoreview`,
passando o modo e o ref.

O subagent é read-only: ele gera o bundle, aplica o rubric e o schema, e retorna
exatamente um objeto JSON seguido de um breve resumo humano.

### Exemplo de invocação

```text
> /autoreview branch origin/main
```

O subagent:

1. Executa `bash .claude/skills/autoreview/scripts/diff-bundle.sh --mode branch --base origin/main`.
2. Lê o bundle, o rubric e o schema.
3. Verifica cada candidate finding contra o código real (com `Read`/`Grep`/`Glob`)
   e arquivos adjacentes.
4. Emite exatamente um objeto JSON e depois um resumo humano.

### Saída esperada (JSON)

```json
{
  "findings": [
    {
      "title": "Off-by-one in pagination loop",
      "body": "activate.py:512 iterates while page < total_pages but total_pages is 1-based; the last page is skipped when total_pages == 1. Confirmed by reading the caller fetch_page(page).",
      "priority": "P1",
      "confidence": 0.9,
      "category": "bug",
      "code_location": { "file_path": "ollama-godmode/godmode-kit/activate.py", "line": 512, "end_line": 514, "function": "paginate" },
      "suggested_fix": "Change `page < total_pages` to `page <= total_pages` in the pagination boundary."
    }
  ],
  "overall_correctness": "patch is incorrect",
  "overall_explanation": "P1 off-by-one bug in pagination introduced by the diff; no other accepted findings.",
  "overall_confidence": 0.9
}
```

## Como validar

```bash
# 1. Sintaxe do helper
bash -n .claude/skills/autoreview/scripts/diff-bundle.sh

# 2. JSON válido
python3 -c "import json; json.load(open('.claude/skills/autoreview/references/schema.json'))" && echo "schema ok"

# 3. Frontmatter YAML válido nos markdowns (requer PyYAML ou yq)
python3 -c "import yaml,sys; list(yaml.safe_load_all(open('.claude/agents/autoreview.md').read().split('---')[1])); print('agent frontmatter ok')"
python3 -c "import yaml; yaml.safe_load(open('.claude/commands/autoreview.md').read().split('---')[1]); print('command frontmatter ok')"
python3 -c "import yaml; yaml.safe_load(open('.claude/skills/autoreview/SKILL.md').read().split('---')[1]); print('skill frontmatter ok')"

# 4. Gerar bundle de teste (read-only, no seu repo)
bash .claude/skills/autoreview/scripts/diff-bundle.sh --mode commit --commit HEAD | head

# 5. Smoke de revisão (dentro do Claude Code, no projeto alvo)
/autoreview commit HEAD
```

## Limitações

- **Sem enforcement de schema no nível do runtime**: a saída estruturada é garantida
  por instrução de prompt + schema em `references/`. Se o subagent emitir texto extra,
  descarte e reexecute. (O `tools` field restringe ferramentas, mas não valida JSON.)
- **Engine = subagent nativo**: ao contrário do OpenClaw (que chama `codex`/`claude`
  externos via CLI), aqui o próprio subagent Claude Code é o revisor. Não há CLI
  engines externos; "painéis multi-reviewer" exigiriam múltiplos subagents
  configurados manualmente.
- **Command não "invoca subagent" como sintaxe dedicada**: o `/autoreview` instrui o
  agente principal a delegar via Task tool (`subagent_type: autoreview`). Você também
  pode chamar o subagent diretamente pela Task tool.
- **Proveniência de regressão**: sem `gitcrawl`; usa blame/commit do git (`SHA, data,
  autor`) quando não houver PR rastreável.
- **`Bash` restrito por instrução**: o `tools` field lista `Bash`, mas o prompt do
  subagent proíbe comandos de mutação. Para enforcement mais forte, combine com
  hooks `PreToolUse` em `settings.json` — exemplo:

  ```json
  {
    "hooks": {
      "PreToolUse": [
        {
          "matcher": "Bash",
          "hooks": [
            {
              "type": "command",
              "command": "bash -c 'cmd=$(cat | jq -r \".tool_input.command\"); echo \"$cmd\" | grep -qE \"^(git (diff|show|log|status|rev-parse|merge-base|ls-files)( |$)|gh (pr view|pr diff)( |$)|bash .claude/skills/autoreview/scripts/diff-bundle.sh( |$))\" || { echo \"Bash command not allowed by autoreview read-only policy: $cmd\" >&2; exit 1; }'"
            }
          ]
        }
      ]
    }
  }
  ```

  Isso bloqueia qualquer Bash command que não seja read-only git/gh ou o helper.
  Command hooks recebem o input como JSON em stdin; o campo do comando Bash está em
  `.tool_input.command`. (Hook não incluído por padrão — revise e ajuste para o
  seu ambiente.)
- **`diff-bundle.sh`** não faz `git fetch` automático; se a base do PR não estiver
  resolvida localmente, falha fechado (exit 3) com instruções.

## Segurança

- Subagent é **estritamente read-only**: `tools: [Read, Grep, Glob, Bash, WebFetch,
  WebSearch]` e o prompt proíbe `Edit`/`Write`/`NotebookEdit` e qualquer bash de
  mutação (`git add/commit/push/reset/...`, `rm`, `mv`, installs).
- Nunca edita, escreve, commita ou faz push.
- Nunca substitui/expõe/transmite secrets. Se encontrar um, reporta como finding
  `security` **sem reproduzir o valor**.
- Nunca envia dados a serviços externos além de lookups read-only de docs
  (`WebFetch`/`WebSearch`) visíveis ao usuário.
- Nunca modifica arquivos fora do projeto revisado.
- Separa sempre fatos (de código/docs lidos) de inferências.
- Nunca mascara falhas de validação ou sugere correções inseguras.