# Detecção de conflitos e anti-duplicação (RF-04)

## Ordem de busca obrigatória

Antes de qualquer proposta nova, `scripts/learn_search.py` varre, nesta ordem:

1. **`AGENTS.md` hierárquico** — subdiretório mais próximo → raiz do projeto → global
   (`~/.codex/AGENTS.md`). Busca por parágrafo, pontuado por sobreposição de palavras-chave.
2. **Descrições de Skills** (`.agents/skills/**/SKILL.md`, projeto e usuário) — para não propor um
   `Skill` que já existe com outro nome.
3. **`.agents/learn/index.json`**, **incluindo** `status: ignored` e `status: archived` — para que
   uma ideia já rejeitada explicitamente pelo usuário reapareça como "isso já foi decidido, ver
   LP-XXXXXX", não como proposta nova.

O script apenas *pontua candidatos*; decidir se é duplicata, conflito ou algo genuinamente novo é
julgamento do agente — não dá para reduzir "duas frases dizem a mesma coisa com palavras
diferentes" a uma regra determinística confiável.

## Taxonomia de conflitos

| Tipo | Definição | Exemplo |
|---|---|---|
| **Duplicação** | Mesmo título normalizado + categoria + escopo já existe | Dois `Rule` dizendo "sempre rodar lint antes de commitar" no mesmo projeto |
| **Sintático** | Duas instruções usam negação/palavras opostas sobre o mesmo assunto | Um learning diz "usar `--force`", outro diz "nunca usar `--force`" |
| **Semântico** | Duas instruções não se contradizem lexicalmente mas não podem ser ambas verdadeiras na prática | Um `Convention` diz "commits em inglês", um `Decision` mais recente diz "commits em pt-BR" |
| **Regra incompatível** | Um `AntiPattern` proíbe exatamente o que um `Rule` mais novo prescreve (ou vice-versa) | `AntiPattern` "nunca usar biblioteca X" vs. `Rule` novo "sempre usar biblioteca X para Y" |
| **Skill redundante** | Uma nova proposta de `Skill` tem descrição com alta sobreposição de palavras-chave com uma Skill existente | Propor `deploy-helper` quando já existe `vercel:deploy` cobrindo o mesmo gatilho |

`learn_search.py` sinaliza candidatos por sobreposição lexical; **classificar o tipo de conflito é
manual** (agente), documentado na seção "Conflitos detectados" da proposta.

## Ordem de preferência de resolução

Estrita, do menos para o mais invasivo:

```
1. corrigir    — o learning existente está certo em essência, só tem um erro factual/de redação
2. atualizar   — o learning existente estava certo, mas a realidade mudou (nova versão de lib, etc.)
3. expandir    — o learning existente está certo mas incompleto; adicionar um caso, não substituir
4. consolidar  — dois ou mais learnings sobrepostos viram um só, mais forte (occurrences somadas)
5. criar       — só depois de descartar 1-4 explicitamente, com justificativa na ficha ("Destino")
```

Cada ficha (`assets/templates/learning-entry.md`, seção "Destino") deve declarar qual dessas ações
foi escolhida e, se for `criar`, por que as quatro anteriores não se aplicavam. Isso obriga o
agente a considerar dedup mesmo quando a resposta final é "não, isso é genuinamente novo".

## Conflitos nunca são resolvidos silenciosamente

Mesmo quando o agente tem uma recomendação clara (ex.: "o `Decision` mais recente deveria
prevalecer sobre o `Convention` antigo"), o conflito é **sempre** listado na seção "Conflitos
detectados" da proposta, com a recomendação explícita — nunca aplicado como se não houvesse
conflito. A aprovação do usuário para aquele item específico é também a aprovação da resolução do
conflito.

## Escopo mais amplo nunca é assumido

Ligado à busca: se um candidato parece se aplicar globalmente mas a evidência vem de um único
projeto, **não** se propõe escopo `global` — propõe-se `project`, e a ficha documenta em "Escopo e
impacto" por que não foi mais amplo. Ver `scope-and-security.md` para a árvore de decisão de
escopo.
