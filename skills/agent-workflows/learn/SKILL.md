---
name: learn
description: >-
  Sistema de gestão de conhecimento incremental, auditável, versionado e reversível para o agente.
  Analisa a sessão (mensagens, diffs, arquivos alterados, comandos, erros, correções do usuário),
  extrai aprendizados, classifica-os em Rule/Skill/Pattern/Documentation/AntiPattern/Decision/
  Convention/Checklist/Template/Reference/Ignore, verifica duplicação e conflito contra
  AGENTS.md/Skills/aprendizados existentes, e gera uma proposta em learning_proposal.md. NUNCA
  aplica nada em AGENTS.md, Skills ou documentação sem aprovação explícita. Use quando o usuário
  digitar `$learn` ou `$learn <contexto>`, disser "aprenda com isso", "registra esse aprendizado",
  "guarda isso pra próxima vez", "isso devia virar uma regra", ou ao final de sessão com correção,
  erro recorrente ou decisão importante. NÃO use para fatos efêmeros da conversa, para editar
  código de produção, ou se o usuário pedir para não perguntar (nesse caso: categoria Ignore e
  pare).
metadata:
  version: "1.0.0"
  author: gabriel-ramos
---

# $learn

Sistema de gestão de conhecimento do agente. Transforma experiências reais de uma sessão em
conhecimento reutilizável — permanente apenas depois de aprovação humana explícita.

Referências detalhadas ficam em `references/`. Templates ficam em `assets/templates/`. Scripts
determinísticos (alocação de ID, busca de duplicatas, aplicação, rollback, auditoria) ficam em
`scripts/`. Leia isto primeiro; abra as referências sob demanda quando o passo em questão exigir
mais detalhe do que cabe aqui.

## Storage runtime (no projeto onde a skill é usada, não neste pacote)

```
.agents/learn/
├── index.json                    # índice único de todos os learnings (ver assets/templates/index-schema.json)
├── .counter                      # contador atômico para alocação de ID
├── learnings/LP-000123.md        # 1 arquivo por learning (ver assets/templates/learning-entry.md)
├── proposals/<YYYY-MM-DD>-<slug>/learning_proposal.md
├── history/<YYYY-MM-DD>.jsonl    # log append-only de propose/approve/apply/reject/rollback
└── snapshots/LP-000123.pre.diff  # diff reverso capturado no apply (usado pelo rollback)
```

Se `.agents/learn/` não existir no projeto-alvo, crie-o na primeira invocação (apenas a estrutura
de diretórios e um `index.json` vazio — isso NÃO conta como "alteração permanente" sujeita a
aprovação, é infraestrutura do próprio sistema de aprendizado, não conhecimento de domínio).

## Fluxo (visão geral — detalhes em `references/architecture.md`)

```
1. ANALISAR sessão  → RF-01
2. EXTRAIR candidatos a aprendizado + causa raiz + padrão recorrente
3. CLASSIFICAR cada candidato em exatamente 1 categoria → RF-02
4. BUSCAR duplicatas/conflitos (AGENTS.md, Skills, index.json)  → RF-04, ver conflict-and-dedup.md
5. Para cada candidato sobrevivente: montar ficha completa  → RF-03
6. Aplicar MATRIZ DE DECISÃO (ocorrências → confiança/versão inicial)
7. GERAR learning_proposal.md (nunca pula esta etapa)  → RF-05
8. PARAR e pedir aprovação explícita  → ver "Gate de aprovação" abaixo
9. Aplicar SOMENTE os itens aprovados (learn_apply.py)  → RF-07
10. Validar + gerar diff final + registrar histórico
```

### Passo 1-3 — Analisar, extrair, classificar

Revise, na sessão atual: mensagens do usuário e do agente, arquivos alterados (`git diff`,
`git status`), comandos executados e seus resultados, erros e como foram corrigidos, e qualquer
correção explícita que o usuário tenha feito ao seu trabalho. Para cada candidato a aprendizado,
classifique em **exatamente uma** destas categorias (definições completas em
`references/architecture.md#categorias`):

`Rule` · `Skill` · `Pattern` · `Documentation` · `AntiPattern` · `Decision` · `Convention` ·
`Checklist` · `Template` · `Reference` · `Ignore`

Inclua explicitamente **aprendizado negativo**: erros recorrentes, más práticas, regressões,
soluções abandonadas — isso vai para `AntiPattern` ou, se for uma decisão pontual de "não fazer de
novo" sem generalizar, para `Ignore`.

### Passo 4 — Nunca duplicar (RF-04)

Antes de propor qualquer coisa nova, execute a busca obrigatória:

```
python3 scripts/learn_search.py --query "<termo-chave>" --project-root <raiz-do-projeto>
```

Isso varre, nesta ordem: `AGENTS.md` hierárquico (subdiretório → projeto → global), descrições de
`.agents/skills/**/SKILL.md`, e `.agents/learn/index.json` (incluindo itens `ignored`/`archived`).
Para cada candidato, siga a ordem de preferência estrita:

**corrigir > atualizar > expandir > consolidar > criar**

Detalhes de como decidir entre essas opções e a taxonomia de conflitos (duplicação, sintático,
semântico, regra incompatível, skill redundante) estão em `references/conflict-and-dedup.md`. Se
houver conflito com um learning existente, registre-o na seção "Conflitos" da proposta — nunca
resolva silenciosamente.

### Passo 5-6 — Ficha completa + matriz de decisão

Para cada aprendizado que sobreviver à busca de duplicação, preencha os campos obrigatórios de
`assets/templates/learning-entry.md` (título, descrição, origem, evidência, confiança,
justificativa, escopo, impacto, risco, destino, proveniência completa: sessão, mensagens, arquivos,
commits, testes, diffs).

Aplique a matriz de decisão para fixar a **versão inicial** (detalhes e justificativa em
`references/id-and-versioning.md`):

| Ocorrências | Confiança | Versão inicial |
|---|---|---|
| 1 | Sugestão | `0.1.0` |
| 2 | Confiança média | `0.2.0` |
| 3 | Regra candidata | `0.3.0` |
| 5+ | Regra consolidada | `1.0.0` |

Determine o **escopo** automaticamente (Global / Projeto / Subdiretório / Tecnologia / Linguagem /
Framework) — regra de ouro: **nunca grave em escopo mais amplo do que a evidência sustenta**.
Detalhes em `references/scope-and-security.md#deteccao-de-escopo`.

Rode a validação de segurança **antes** de persistir qualquer texto de evidência:

```
python3 scripts/learn_lint.py --file <rascunho-da-entry.md>
```

Isso redige (`[REDACTED:<tipo>]`) qualquer API key, token, JWT, cookie, secret, senha, dado pessoal
ou conteúdo de `.env` encontrado na evidência. Nunca cole output bruto de comando na proposta sem
antes resumir e checar — a proposta em si já não deve conter segredos.

Aloque o ID de cada aprendizado (não antes de decidir que ele vai para a proposta):

```
python3 scripts/learn_id.py --project-root <raiz-do-projeto>
# → LP-000123
```

### Passo 7 — Gerar learning_proposal.md (RF-05, obrigatório, nunca pule)

Use `assets/templates/learning_proposal.md`. A proposta deve conter: contexto, aprendizados
(uma ficha completa por item), rejeições (candidatos descartados e por quê), conflitos detectados,
riscos, estratégia de rollback por item, plano de validação, e **diffs completos** de cada
alteração proposta (não apenas descrição — o diff real que seria aplicado). Salve em
`.agents/learn/proposals/<data>-<slug>/learning_proposal.md`.

### Passo 8 — Gate de aprovação (crítico — leia com atenção)

**O Codex não tem hooks/enforcement técnico de permissão como outros harnesses.** Isso significa
que a barreira de aprovação é inteiramente comportamental: você, o agente, deve se recusar a
prosseguir. Depois de escrever `learning_proposal.md`, **pare** e apresente um resumo curto ao
usuário. A única forma de prosseguir é o usuário responder, na mensagem seguinte, com um destes
tokens (case-insensitive, em pt-BR ou en):

- `aprovar` / `approve`
- `prosseguir` / `proceed`
- `aplicar` / `apply` (aplica todos os itens da proposta)
- `aplicar LP-XXXXXX` / `apply LP-XXXXXX` (aplica somente aquele item)

Qualquer outra resposta — incluindo silêncio, uma pergunta de esclarecimento, continuar a
conversa sobre outro assunto, ou um "ok" genérico fora desse conjunto — **não autoriza aplicação**.
Se houver ambiguidade sobre o que o usuário quer aprovar, pergunte antes de chamar
`learn_apply.py`. Nunca assuma aprovação implícita.

### Passo 9-10 — Aplicar, validar, registrar (RF-07)

Somente para os itens explicitamente aprovados:

```
python3 scripts/learn_apply.py --project-root <raiz> --id LP-000123
```

O script: aplica o diff da entry ao arquivo-destino (`AGENTS.md` no escopo certo, arquivo de Skill,
doc de projeto, ou `assets/templates` — conforme `destino` da ficha), grava um diff reverso em
`snapshots/LP-000123.pre.diff`, atualiza `status` em `index.json`, e acrescenta uma linha ao
`history/<data>.jsonl`. Depois de aplicar, mostre ao usuário o diff final efetivamente aplicado.

Itens rejeitados ou não mencionados na aprovação permanecem em `learnings/` com
`status: proposed` — eles reaparecerão na próxima invocação apenas se a evidência para eles ainda
for válida (ver `references/architecture.md#obsolescencia`); não os proponha de novo sem checar se
já foram rejeitados antes (isso seria uma duplicação, RF-04).

## Rollback individual

Nunca restaura o arquivo inteiro. Reverte apenas o hunk daquele learning, usando o diff reverso
salvo em `snapshots/`:

```
python3 scripts/learn_rollback.py --project-root <raiz> --id LP-000123
```

O script recusa o rollback (e explica por quê) se outro learning ativo depender deste
(`depends_on`) — antes de reverter, avise o usuário do impacto e peça confirmação. Detalhes em
`references/rollback-and-migration.md`.

## Auditoria e obsolescência

Rode sob demanda (ex.: `$learn audit`, ou periodicamente) para responder às perguntas de avaliação
futura ("esta regra ainda é usada?", "existe duplicado?", "o que nunca foi usado?"):

```
python3 scripts/learn_audit.py --project-root <raiz>
```

Relata: learnings nunca reutilizados, learnings com `last_validated` vencido, candidatos a
duplicata, e problemas no grafo de dependências (`depends_on`/`superseded_by`). Ver
`references/architecture.md#obsolescencia` e `references/rollback-and-migration.md#migracao`.

## Compatibilidade

Esta skill usa exclusivamente mecanismos documentados da especificação oficial de Codex Skills
(frontmatter `name`/`description`, `scripts/`, `references/`, `assets/`, `agents/openai.yaml`,
invocação `$learn`) e da hierarquia oficial de `AGENTS.md` (global/projeto/subdiretório). Nenhum
mecanismo de hook, permissão automática ou API não documentada é usado — ver
`references/compatibility.md` para o mapeamento completo e fontes.
