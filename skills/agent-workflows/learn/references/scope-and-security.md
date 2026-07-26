# Escopo e segurança

## Detecção de escopo

Regra de ouro: **nunca gravar em escopo mais amplo do que a evidência sustenta.** Árvore de
decisão, aplicada nesta ordem (primeira condição que bate vence):

1. **Subdiretório** — a evidência é inteiramente local a um subdiretório que já tem seu próprio
   `AGENTS.md` (ou claramente deveria ter um, ex.: um monorepo com `packages/api/`). `target_file`
   aponta para o `AGENTS.md` daquele subdiretório.
2. **Tecnologia / Linguagem / Framework** — a evidência é específica de uma stack usada só em
   parte do projeto (ex.: uma convenção só faz sentido para código Python, e o projeto também tem
   TypeScript). Grava-se como uma subseção rotulada por tecnologia dentro do `AGENTS.md` mais
   próximo que já cobre aquele código, não um arquivo novo — evita fragmentação excessiva.
3. **Projeto** (default) — a evidência vem de uma única sessão neste projeto e não há sinal de que
   se aplicaria a outros. `target_file` = `AGENTS.md` da raiz do projeto. **Esta é a escolha padrão
   sempre que houver dúvida.**
4. **Global** (`~/.codex/AGENTS.md`) — só quando há evidência **cross-projeto** explícita: o mesmo
   padrão foi observado em mais de um projeto (occurrences vindas de sessões em raízes de projeto
   diferentes), ou o usuário disse explicitamente algo como "isso vale pra todo projeto meu". Um
   único projeto, não importa quão convincente a evidência, nunca justifica sozinho escopo global.

Promover um learning existente de escopo mais estreito para mais amplo (ex.: `project` → `global`)
é tratado como qualquer outra mudança: precisa de nova evidência cross-projeto, dispara bump de
`version` MAJOR (mudança de escopo, ver `id-and-versioning.md`), e passa pelo mesmo gate de
aprovação — nunca é automático.

## Segurança: o que nunca persistir

`scripts/learn_lint.py` roda antes de qualquer texto de evidência ser escrito em
`learnings/<id>.md` ou em `learning_proposal.md`. Dois níveis:

### Redigido automaticamente (alta confiança, baixo risco de falso positivo)

| Tipo | Padrão (resumo) |
|---|---|
| AWS access key | `AKIA[0-9A-Z]{16}` |
| Atribuição genérica de segredo | `(api_key\|secret\|token\|password\|access_key)\s*[:=]\s*...` |
| Bearer token | `Bearer <token>` |
| JWT | `eyJ...\...\....` (três segmentos base64url) |
| Bloco de chave privada | `-----BEGIN ... PRIVATE KEY-----` ... `-----END ...-----` |
| Linha estilo `.env` | `CHAVE_MAIUSCULA=valor` |
| CPF brasileiro | `\d{3}\.\d{3}\.\d{3}-\d{2}` |

### Sinalizado, não redigido automaticamente (risco real de falso positivo)

| Tipo | Motivo de não redigir automaticamente |
|---|---|
| Endereço de e-mail | Aparece legitimamente em documentação técnica (ex.: "reporte para X@..."); redigir sempre destruiria contexto útil com frequência. Fica **flagged** no relatório do `learn_lint.py` para o agente decidir caso a caso. |

Isso é uma escolha deliberada de trade-off entre "nunca persistir dado pessoal" (NFR) e "não
destruir evidência legítima às cegas" — resolvida sinalizando em vez de agir automaticamente
quando o padrão tem alta taxa de falso positivo.

### Regra de ouro para o agente (SKILL.md)

Nunca colar output bruto de comando (logs, respostas de API, variáveis de ambiente) diretamente em
uma ficha ou proposta sem antes resumir e rodar `learn_lint.py`. O objetivo de `learn_lint.py` é a
segunda linha de defesa, não a primeira — a primeira é o próprio agente nunca copiar segredo para
começo de conversa.
