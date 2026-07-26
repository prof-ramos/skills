# Compatibilidade com a especificação oficial do Codex

Esta skill usa exclusivamente mecanismos documentados publicamente para Codex CLI Skills. Fonte
primária consultada: `developers.openai.com/codex/skills` (redireciona para
`learn.chatgpt.com/docs/build-skills.md`), acessada em 2026-07-26. Sem invenção de campos ou
comportamento além do documentado.

## Frontmatter de `SKILL.md`

| Campo exigido pela spec | Uso nesta skill |
|---|---|
| `name` | `learn` — kebab-case, corresponde ao nome do diretório (`skills/agent-workflows/learn/`) |
| `description` | Descreve explicitamente quando disparar (`$learn`, `$learn <contexto>`, frases-gatilho em pt-BR) e quando **não** disparar (fatos efêmeros, edição de código de produção, pedido explícito de não perguntar) — seguindo a orientação da spec de "explain exactly when this skill should and should not trigger" |

Campos extras (`metadata.version`, `metadata.author`) são aditivos e não fazem parte do contrato
mínimo — não conflitam com a spec, que não proíbe metadados adicionais.

## Layout de diretórios

| Diretório da spec | Uso nesta skill |
|---|---|
| `SKILL.md` (obrigatório) | Fluxo completo, com profundidade progressiva (detalhe fica em `references/`) |
| `scripts/` (opcional) | 6 scripts Python determinísticos (CLI): alocação de ID, busca/dedup, lint de segurança, apply, rollback, auditoria — nenhum deles toma decisões de julgamento (classificação, causa raiz, resolução de conflito semântico), que permanecem no agente. `apply`/`rollback` compartilham a mecânica de patch via um módulo interno, `_learn_patch.py` (não é CLI, é a implementação por trás dos dois) |
| `references/` (opcional) | Documentação técnica profunda: arquitetura, versionamento, conflitos, escopo/segurança, rollback/migração, casos de teste, este arquivo |
| `assets/` (opcional) | `assets/templates/`: templates de proposta, de ficha de aprendizado, e JSON Schemas do índice e do log de histórico |
| `agents/openai.yaml` (opcional) | Ver seção dedicada abaixo |

## `agents/openai.yaml`

Campos usados, todos dentro do que a spec documenta (`interface`, `policy`, `dependencies`):

- `interface.display_name`, `interface.short_description`, `interface.default_prompt` — só texto,
  sem inventar assets. `icon_small`/`icon_large`/`brand_color` foram deliberadamente **omitidos**
  em vez de apontar para arquivos que não existem.
- `policy.allow_implicit_invocation: false` — justificativa: a spec documenta o campo com default
  `true`, mas este fluxo é pesado (analisa a sessão inteira, gera uma proposta de múltiplas
  etapas, interrompe a conversa pedindo aprovação). Disparar isso implicitamente por uma menção
  casual seria surpreendente para o usuário; a invocação explícita (`$learn`) é a UX correta aqui.
- `dependencies.tools: []` — não depende de nenhum servidor MCP; opera só sobre o filesystem do
  projeto (`AGENTS.md`, `.agents/skills`, `.agents/learn`) e os próprios scripts.

## Invocação

- Explícita: `$learn` ou `$learn <contexto>`, conforme a spec ("Users invoke skills directly via
  `$skill-name`").
- Implícita: desabilitada via `policy.allow_implicit_invocation: false` (ver acima) — a spec trata
  isso como opt-out documentado, não como uma restrição fora do padrão.

## Escaneamento hierárquico (REPO → USER → ADMIN → SYSTEM)

Esta skill não interfere nesse mecanismo — ela é descoberta como qualquer outra skill Codex,
seguindo a ordem documentada. O que esta skill *adiciona* é o diretório `.agents/learn/` (estado
runtime), que é deliberadamente **irmão** de `.agents/skills` (o diretório REPO oficial), nunca uma
sobreposição: nada dentro de `.agents/learn/` é varrido pelo carregador de skills do Codex, e nada
dentro de `.agents/skills` é gerenciado pelos scripts desta skill (quando um learning de categoria
`Skill` é aprovado, ele escreve um `SKILL.md` novo/atualizado ali, mas isso é o mesmo tipo de
edição que um humano faria manualmente — não um mecanismo paralelo).

## `AGENTS.md`

A spec documenta a hierarquia `~/.codex/AGENTS.md` (global) → `AGENTS.md` na raiz do projeto →
`AGENTS.md` em subdiretórios, mas **não especifica** regras de precedência/merge entre eles nem
uma API estruturada para editá-los — são arquivos Markdown de texto livre. Esta skill trata isso
como o que é: edita `AGENTS.md` via diffs de texto (`patch`), como um humano editaria, escrevendo
seções previsíveis (`## Regras`, `## Convenções`, `## Nunca fazer`, etc., ver `architecture.md`)
para que o resultado continue legível e editável manualmente, sem depender de nenhum parser
proprietário de `AGENTS.md` que a spec não define.

## O que esta skill deliberadamente não assume

- **Sem hooks/enforcement técnico de permissão.** Ao contrário de outros harnesses, a spec de
  Codex Skills não documenta um mecanismo de hook para bloquear ações antes da execução. Por isso
  o gate de aprovação (RF-06/RF-07) é implementado como uma regra comportamental explícita em
  `SKILL.md`, não como um script que "impede" tecnicamente a aplicação — é o próprio agente que se
  recusa a chamar `learn_apply.py` sem o token de aprovação. Isso é uma limitação de plataforma
  documentada aqui para transparência, não um bug de design.
- **Sem API estruturada de skills de terceiros.** Toda leitura de `.agents/skills/**/SKILL.md`
  feita por `learn_search.py` é um parse de texto simples do frontmatter, não uma chamada a uma
  API do Codex — porque a spec não expõe uma.
- **Dependência de `patch` (CLI, POSIX)** para aplicar/reverter diffs — padrão em macOS/Linux, fora
  do escopo da spec de Skills em si (que não prescreve como um script deve editar arquivos), mas
  documentado aqui como um requisito de ambiente explícito em vez de assumido silenciosamente.
