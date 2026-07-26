<!--
Template for .agents/learn/learnings/<id>.md -- one file per learning.

Fill every frontmatter field before this leaves "draft" status. Frontmatter
is parsed by scripts/_learn_common.py:parse_learning_entry() -- keep it flat
scalars + simple `[a, b]` lists only (see index-schema.json for the type of
each field). Everything discursive goes in the body below the frontmatter,
never in the frontmatter itself.

Run scripts/learn_lint.py on this file before it leaves draft status.
-->
---
id: LP-000000
title: "<título curto e específico, não genérico>"
category: rule
status: proposed
version: "0.1.0"
scope: project
target_file: "AGENTS.md"
tags: [tag-um, tag-dois]
confidence_tier: suggestion
occurrences: 1
created_at: "2026-01-01T00:00:00+00:00"
related_technology: []
depends_on: []
superseded_by: null
last_used: null
last_validated: null
---

## Descrição

<!-- O que é este aprendizado, em 1-3 frases. Deve fazer sentido lido isoladamente,
     sem precisar da sessão original para ser entendido. -->

## Origem

<!-- De onde isso veio: qual sessão, qual tarefa, o que disparou a observação. -->

## Evidência

<!-- Trechos concretos (já passados por learn_lint.py) que sustentam o aprendizado:
     mensagens do usuário, diffs, comandos, erros, correções. Cite proveniência
     exata (ver seção Proveniência abaixo) em vez de parafrasear. -->

## Justificativa

<!-- Por que isso deveria virar conhecimento permanente. Qual erro isso evita,
     qual padrão isso reforça, por que confiar nisso agora (ver matriz de decisão
     em references/id-and-versioning.md). -->

## Escopo e impacto

- **Escopo detectado**: <global | projeto | subdiretório | tecnologia | linguagem | framework>
- **Por que este escopo e não um mais amplo**: <justificativa>
- **Impacto esperado**: <o que muda no comportamento do agente>
- **Risco se aplicado**: <o que pode dar errado>
- **Risco se ignorado**: <o que continua dando errado>

## Destino

- **Arquivo-alvo**: `<mesmo valor de target_file no frontmatter>`
- **Ação**: <criar | corrigir | atualizar | expandir | consolidar>
- **Motivo de não ser uma das ações anteriores na ordem de preferência**: <se "criar", justifique por que corrigir/atualizar/expandir/consolidar não se aplicavam -- ver references/conflict-and-dedup.md>

## Proveniência

- **Sessão**: <identificador ou data/hora da sessão de origem>
- **Mensagens**: <referências às mensagens relevantes, resumidas -- nunca cole segredos>
- **Arquivos**: <arquivos lidos/alterados que embasam este aprendizado>
- **Commits**: <hashes, se houver>
- **Testes**: <testes executados/relevantes, se houver>
- **Diffs**: <diffs de código observados que embasam este aprendizado -- distintos do diff proposto abaixo>

## Conflitos e duplicação verificados

<!-- Resultado de scripts/learn_search.py: o que foi encontrado, por que isso não é
     duplicata, e com o que isso pode conflitar. "Nenhum encontrado" é uma resposta
     válida, mas só depois de rodar a busca. -->

## Rollback

- **Estratégia**: reversão automática via diff reverso capturado no apply (não requer ação manual).
- **Dependências que quebram se isto for revertido**: <ver campo depends_on / rodar learn_audit.py>

## Diff proposto

<!-- Cabeçalhos --- / +++ devem usar o NOME DE ARQUIVO NU de target_file (sem caminho),
     pois learn_apply.py roda `patch` com cwd = diretório-pai de target_file.
     Use "--- /dev/null" quando o destino ainda não existir. -->
```diff
--- AGENTS.md
+++ AGENTS.md
@@ -0,0 +0,0 @@
```
