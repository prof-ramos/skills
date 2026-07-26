<!--
Template para .agents/learn/proposals/<YYYY-MM-DD>-<slug>/learning_proposal.md

Este documento é o único artefato que a skill $learn produz antes de pedir
aprovação -- ver SKILL.md "Passo 7" e "Gate de aprovação". Nada além deste
arquivo é escrito em AGENTS.md/Skills/documentação até o usuário responder
com um dos tokens de aprovação.
-->
# Proposta de Aprendizado — {{data}}

## Contexto

<!-- O que estava sendo feito nesta sessão, por que essa análise de aprendizado
     foi disparada agora (invocação explícita $learn, ou gatilho contextual). -->

## Resumo executivo

| ID | Título | Categoria | Confiança | Escopo | Destino |
|----|--------|-----------|-----------|--------|---------|
| LP-000000 | ... | rule | Sugestão (1 ocorrência) | projeto | AGENTS.md |

## Aprendizados propostos

<!-- Uma subseção por ID, cada uma sendo o conteúdo completo do respectivo
     learnings/<id>.md (não um resumo -- a ficha inteira, para que aprovar
     "aplicar LP-000123" seja uma decisão informada). -->

### LP-000000 — {{título}}

{{conteúdo completo de learnings/LP-000000.md}}

## Rejeições

<!-- Candidatos que foram descartados durante a análise e por quê (ex.: já
     existia um learning idêntico ignorado/arquivado, evidência insuficiente,
     é efêmero demais para category != Ignore). -->

- **Candidato descartado**: <descrição breve> — **Motivo**: <motivo>

## Conflitos detectados

<!-- Resultado de scripts/learn_search.py para cada candidato. Se um candidato
     conflita com um learning/regra existente, isso NUNCA é resolvido
     silenciosamente -- é listado aqui para o usuário decidir. -->

- **LP-000000** conflita com `<caminho ou ID>` — **Natureza do conflito**: <duplicação | sintático | semântico | regra incompatível | skill redundante> — **Recomendação**: <corrigir | atualizar | expandir | consolidar | manter ambos e pedir decisão do usuário>

## Riscos

<!-- Riscos agregados de aplicar esta proposta como um todo, além dos riscos
     individuais já listados em cada ficha. -->

## Estratégia de rollback

<!-- Resumo por item: todos usam o mecanismo padrão (diff reverso automático,
     scripts/learn_rollback.py --id LP-XXXXXX). Liste aqui apenas exceções ou
     dependências entre itens desta mesma proposta que afetam a ordem de
     rollback. -->

## Plano de validação

<!-- Como confirmar que a aplicação funcionou: comando a rodar, arquivo a
     inspecionar, comportamento esperado na próxima sessão. -->

## Diffs completos

<!-- Concatenação de todos os blocos ```diff``` propostos, para revisão rápida
     sem abrir cada ficha individual. -->

```diff
<diff de LP-000000>
```

---

## Aprovação

Para prosseguir, responda com um destes tokens (ver SKILL.md "Gate de
aprovação"):

- `aprovar` / `aplicar` — aplica **todos** os itens desta proposta
- `aplicar LP-XXXXXX` — aplica **apenas** aquele item
- qualquer outra resposta **não autoriza aplicação**
