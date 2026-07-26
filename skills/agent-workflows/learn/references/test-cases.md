# Casos de teste e casos-limite

Mapeados aos requisitos funcionais/não-funcionais da spec original. "Verificação" descreve como
confirmar o comportamento manualmente (não há test runner automatizado para o comportamento do
agente em si — só para os scripts, que são determinísticos e testáveis por linha de comando).

## Casos funcionais

| # | Cenário | RF/NFR | Comportamento esperado | Verificação |
|---|---|---|---|---|
| T1 | Sessão sem nada relevante para aprender | RF-01 | Skill relata "nada a propor", não gera `learning_proposal.md` vazio | Rodar `$learn` numa sessão trivial; conferir que nenhum diretório novo aparece em `proposals/` |
| T2 | Uma única correção do usuário nesta sessão | Matriz de decisão | `occurrences: 1`, `confidence_tier: suggestion`, `version: 0.1.0` | Inspecionar frontmatter da ficha gerada |
| T3 | Mesmo padrão já visto 2x antes (via `index.json`) + esta sessão | Matriz de decisão | Ficha existente é **atualizada** (occurrences 2→3, version 0.2.0→0.3.0), não duplicada | `learn_search.py` deve encontrar o learning existente; ação = "atualizar", não "criar" |
| T4 | Candidato idêntico a um `AntiPattern` já `ignored` | RF-04 | Não propõe de novo; referencia o ID ignorado na seção Rejeições | `learn_search.py --query ...` retorna o item com `status: ignored` |
| T5 | Dois aprendizados nesta sessão conflitam entre si (um Rule, um AntiPattern, mesmo tema) | Detecção de conflito | Ambos aparecem na proposta com seção "Conflitos detectados" preenchida; nenhum é descartado silenciosamente | Ler a proposta gerada |
| T6 | Evidência contém uma chave AWS colada de um log | Segurança | `learn_lint.py` redige antes da ficha ser salva; proposta nunca mostra o segredo em claro | `python3 scripts/learn_lint.py --file <rascunho>` deve retornar exit 1 com `findings` |
| T7 | Usuário aprova só um item de uma proposta com 3 | Gate de aprovação | Somente `LP-000042` (o mencionado) é aplicado; os outros dois continuam `status: proposed` | Checar `index.json` após o apply |
| T8 | Usuário responde algo ambíguo tipo "ok" | Gate de aprovação | Nada é aplicado; agente pergunta o que exatamente aprovar | Nenhuma chamada a `learn_apply.py` deve ocorrer |
| T9 | Rollback de um item sem dependentes | Rollback | `learn_rollback.py` reverte só aquele hunk; resto do arquivo intacto | `git diff` do arquivo-alvo mostra só as linhas daquele learning revertidas |
| T10 | Rollback de um item do qual outro `applied` depende | Dependências | Script recusa sem `--force`; lista o(s) dependente(s) | `learn_rollback.py --id LP-A` (sem force) retorna exit 1 com `dependents` |
| T11 | Auditoria com um learning `applied` nunca usado há 6 meses | Obsolescência | Aparece em `never_used` e/ou `stale` no relatório | `learn_audit.py` |
| T12 | Dois learnings com título quase idêntico (parafraseado) | Duplicação | `learn_audit.py` reporta como `duplicate_candidates` (mesmo normalizado + categoria + escopo) | Rodar auditoria após inserir manualmente um duplicado no índice de teste |
| T13 | Evidência específica de um único projeto sugerindo regra "universal" | Escopo | Escopo proposto é `project`, não `global`; ficha justifica por quê | Ler seção "Escopo e impacto" da ficha |
| T14 | Mesmo padrão observado em 2 projetos diferentes (sessões distintas) | Escopo | Só então escopo `global` é elegível, com `target_file: ~/.codex/AGENTS.md` | Verificar que a evidência cita sessões/projetos distintos |
| T15 | Aprendizado categorizado como `Skill` | Categorias | Destino é `.agents/skills/<nome>/`, não `AGENTS.md` | Checar `target_file` no frontmatter |
| T16 | Aprendizado categorizado como `Ignore` | Categorias | Nunca aparece como algo a "aplicar"; fica só em `learnings/` com `status: ignored` | `index.json` não deve ter `target_file` efetivamente promovido |

## Casos-limite

| # | Cenário | Comportamento esperado |
|---|---|---|
| E1 | `.agents/learn/` não existe ainda no projeto | Criado automaticamente na primeira invocação (`ensure_scaffold`), sem passar pelo gate de aprovação (é infraestrutura, não conhecimento de domínio) |
| E2 | `AGENTS.md` de destino não existe ainda | Diff usa `--- /dev/null` / `+++ AGENTS.md`; `patch` cria o arquivo; diretório-pai é criado se necessário |
| E3 | Duas chamadas de `learn_id.py` em paralelo (dois processos) | `fcntl.flock` serializa o acesso ao `.counter`; IDs saem sem colisão nem gap forçado |
| E4 | Usuário diz "aplicar LP-002" mas LP-002 não existe na proposta atual | `learn_apply.py` retorna erro claro ("not found in index.json"); agente informa o usuário em vez de tentar adivinhar |
| E5 | Processo é interrompido no meio de um `learn_apply.py` (crash) | `patch` é uma operação única e atômica por arquivo; ou o patch foi aplicado e o script chega a gravar o snapshot+índice, ou não foi aplicado e nada mudou — não há estado "meio aplicado". Se o crash ocorrer *entre* o patch e a gravação do índice, a próxima auditoria detecta a divergência (arquivo já mudou, `index.json` ainda diz `proposed`) — reportar como caso a resolver manualmente |
| E6 | Learning arquivado/ignorado volta a ter evidência nova relevante | Não é re-proposto como novo; o agente reabre o learning existente (`status: proposed` de novo, `occurrences` incrementado), preservando o ID e o histórico |
| E7 | `related_technology` de um learning aponta para uma dependência removida do projeto | Sinalizado (não removido automaticamente) na próxima auditoria; decisão de arquivar passa pelo gate normal |
| E8 | Diff proposto não aplica mais porque o arquivo-alvo mudou desde a análise | `patch` falha; `learn_apply.py` não altera estado; agente deve regenerar a ficha com um diff atualizado antes de tentar de novo |
| E9 | Mesmo aprendizado observado simultaneamente em duas sessões concorrentes no mesmo projeto | `learn_search.py` encontra o `status: proposed` já existente na segunda sessão; a segunda sessão deve **atualizar** a proposta pendente, não criar uma segunda proposta duplicada |
| E10 | Usuário pede para nunca mais perguntar sobre um tema | Registrar como `Ignore` de escopo apropriado; isso ainda passa pelo gate de aprovação normal (é uma alteração permanente de comportamento, mesmo que "não fazer nada" seja o comportamento) |
