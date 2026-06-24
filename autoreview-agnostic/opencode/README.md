# autoreview — versão OpenCode

Port idiomático do skill `autoreview` do OpenClaw para **OpenCode**. Preserva a
intenção funcional (revisão de closeout estruturada, advisory, read-only, com
verificação de cada finding e disciplina de escopo) e adapta o mecanismo para os
construtos nativos do OpenCode: **subagent**, **command** e **skill**.

## Árvore de arquivos

```
opencode/
├── opencode.json                              # config: agent autoreview + command /autoreview
├── AGENTS.md                                  # instruções de projeto (anexar ao seu AGENTS.md)
├── agent/
│   └── autoreview.md                          # prompt do subagent autoreview
├── command/
│   └── autoreview.md                          # slash command /autoreview
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

1. Copie a pasta `opencode/` para a raiz do seu projeto (ou mescle os arquivos nos
   diretórios `.opencode/` já existentes — OpenCode procura agentes em
   `.opencode/agent/`, comandos em `.opencode/command/` e skills em
   `.opencode/skills/`). O agente `autoreview` é definido como **subagent
   standalone** em `.opencode/agent/autoreview.md` (com frontmatter `mode:
   subagent`, `permission.edit: deny` e allowlist de bash read-only).
2. Se você já tem um `opencode.json`, **mescle** as chaves `command.autoreview`,
   `skills.paths` e `instructions` em vez de sobrescrever.
3. Garanta permissão de execução ao helper:
   `chmod +x .opencode/skills/autoreview/scripts/diff-bundle.sh`.
4. (Opcional) ajuste o campo `model` em `.opencode/agent/autoreview.md` para o
   modelo da sua conta; o default é `anthropic/claude-sonnet-4-6`.

> Nota de incerteza: a documentação OpenCode confirma o caminho
> `.opencode/agent/<name>.md` e o padrão *frontmatter + body* para arquivos de
> agente, mas não enumera explicitamente os campos do frontmatter de agente
> (apenas os equivalentes em `opencode.json`). Adotamos os mesmos campos usados em
> `opencode.json` (`description`, `mode`, `model`, `permission`); se a sua versão do
> OpenCode exigir nomes diferentes, defina o agente pela chave `agent.autoreview`
> em `opencode.json` (campos confirmados) e aponte `prompt:
> "{file:./.opencode/agent/autoreview.md}"`.

> Para um diretório de configuração alternativo, defina
> `OPENCODE_CONFIG_DIR=/path/to/config` (documentação OpenCode).

## Como usar

```text
/autoreview                    # auto: dirty local → base do PR → origin/main
/autoreview local              # worktree suja (unstaged + staged + untracked)
/autoreview branch origin/main # diff da branch vs base
/autoreview commit HEAD        # um commit já landado
```

O command roda no subagent `autoreview` (read-only). A saída é um objeto JSON
único conforme `references/schema.json`, seguido de um breve resumo humano.

### Exemplo de invocação

```text
> /autoreview branch origin/main
```

O subagent:

1. Executa `bash .opencode/skills/autoreview/scripts/diff-bundle.sh --mode branch --base origin/main`.
2. Lê o bundle, o rubric e o schema.
3. Verifica cada candidate finding contra o código real e arquivos adjacentes.
4. Emite exatamente um objeto JSON e depois um resumo humano.

### Saída esperada (JSON)

```json
{
  "findings": [
    {
      "title": "Off-by-one no loop de paginação",
      "body": "activate.py:512 itera até page < total_pages mas total_pages é 1-based; a última página é pulada quando total_pages == 1. Confirmado lendo o caller fetch_page(page).",
      "priority": "P1",
      "confidence": 0.9,
      "category": "bug",
      "code_location": { "file_path": "ollama-godmode/godmode-kit/activate.py", "line": 512, "end_line": 514, "function": "paginate" },
      "suggested_fix": "Trocar `page < total_pages` por `page <= total_pages` no boundary de paginação."
    }
  ],
  "overall_correctness": "patch is incorrect",
  "overall_explanation": "Bug P1 de off-by-one na paginação introduzido pelo diff; sem outros findings aceitos.",
  "overall_confidence": 0.9
}
```

## Como validar

```bash
# 1. Sintaxe do helper
bash -n .opencode/skills/autoreview/scripts/diff-bundle.sh

# 2. JSON válido
python3 -c "import json,sys; json.load(open('.opencode/skills/autoreview/references/schema.json'))" && echo "schema ok"

# 3. opencode.json válido
python3 -c "import json; json.load(open('opencode.json'))" && echo "config ok"

# 4. Gerar bundle de teste (read-only, no seu repo)
bash .opencode/skills/autoreview/scripts/diff-bundle.sh --mode commit --commit HEAD | head

# 5. Smoke de revisão (requer OpenCode instalado)
opencode run --agent autoreview "review HEAD" 2>&1 | tail -20
```

## Limitações

- **Sem validação de schema nativa no nível do agente**: a saída estruturada é
  garantida por instrução de prompt + schema em `references/`, não por enforcement
  do runtime do OpenCode. Se o agente emitir texto extra, descarte e reexecute.
- **Engine = agente nativo**: ao contrário do OpenClaw (que chama `codex`/`claude`
  externos), aqui o próprio agente OpenCode é o revisor. Não há múltiplos engines
  CLI; "painéis multi-reviewer" exigiriam múltiplos agentes configurados manualmente.
- **Proveniência de regressão**: sem `gitcrawl`; usa blame/commit do git (`SHA, data,
  autor`) quando não houver PR rastreável.
- **Sem enforcement de read-only além das permissões**: a segurança vem de
  `permission.edit: deny` e da allowlist de bash. Revise a allowlist se adicionar
  novos comandos.
- **Comando `diff-bundle.sh`** não busca `git fetch` automaticamente; se a base do
  PR não estiver resolvida localmente, ele falha fechado (exit 3) com instruções.

## Segurança

- Revisor é **estritamente read-only** (`edit: deny`; bash restrito a git/gh
  read-only + o helper).
- Nunca edita, escreve, commita ou faz push.
- Nunca substitui/expõe/transmite secrets. Se encontrar um, reporta como finding
  `security` **sem reproduzir o valor**.
- Nunca envia dados a serviços externos além de lookups read-only de docs visíveis ao
  usuário.
- Nunca modifica arquivos fora do projeto revisado.
- Separa sempre fatos (de código/docs lidos) de inferências.
- Nunca mascara falhas de validação ou sugere correções inseguras.