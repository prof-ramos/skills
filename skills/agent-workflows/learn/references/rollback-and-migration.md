# Rollback e migração

## Rollback individual — mecanismo

A mecânica de aplicar/reverter é um único módulo profundo, `scripts/_learn_patch.py`
(`apply_patch_to_target(target_path, diff_text) -> PatchResult`), usado por `learn_apply.py` e
`learn_rollback.py` como dois adapters finos — a direção (aplicar o diff original ou o reverso)
nunca aparece na interface do módulo, só na escolha de qual `diff_text` o chamador passa. Cada
aplicação bem-sucedida já retorna, em `PatchResult.reverse_diff`, o diff reverso calculado a partir
do conteúdo do arquivo-alvo *antes* e *depois* do patch (via `difflib.unified_diff`, comparando
"depois" → "antes"); `learn_apply.py` grava esse valor em `.agents/learn/snapshots/<id>.pre.diff`.
`learn_rollback.py` lê esse snapshot e passa seu conteúdo de volta para o mesmo
`apply_patch_to_target()` — mesma máquina, sentido invertido, sem duplicar a chamada a `patch`.

Isso satisfaz o requisito "rollback nunca depende de restaurar o arquivo inteiro" em um sentido
preciso: o rollback é um patch escopado às linhas (hunks) que aquele learning específico tocou, não
uma cópia de backup do arquivo inteiro sendo jogada por cima. Consequência prática importante: se
uma edição **não relacionada** (feita depois, por outro learning ou pelo usuário) tocar linhas
fora daquele hunk, o rollback continua funcionando normalmente. Se ela tocar as **mesmas** linhas,
`patch` vai falhar em aplicar o diff reverso (contexto não bate) — e `learn_rollback.py` aborta com
erro em vez de forçar, que é o comportamento seguro: um rollback que "empurra" um patch conflitante
seria pior que não reverter, porque corromperia silenciosamente conteúdo não relacionado.

### Por que não guardar uma cópia inteira do arquivo como snapshot

Foi considerado e descartado: guardar `AGENTS.md.bak` inteiro no momento do apply e simplesmente
`cp` de volta no rollback. Problema: se **qualquer outra coisa** mudou aquele arquivo entre o apply
e o rollback (outro learning aplicado, edição manual do usuário), restaurar o arquivo inteiro
apagaria essas mudanças não relacionadas — exatamente o que o requisito proíbe. O diff reverso
escopado evita isso por construção.

## Dependências e impacto antes de reverter

Antes de reverter `LP-A`, `learn_rollback.py` verifica se algum outro learning `applied` declara
`depends_on: [LP-A, ...]`. Se sim, recusa por padrão e lista os dependentes — o agente deve
explicar o impacto ao usuário (ex.: "reverter LP-A também invalida a premissa de LP-B, que
continuará aplicado mas potencialmente incorreto") e só usar `--force` após confirmação explícita
do usuário para *aquele* rollback específico (o mesmo padrão de aprovação explícita do apply
original, não uma segunda categoria de exceção).

## Falha durante o apply

Se `patch` retornar erro (contexto não bate, arquivo mudou de forma inesperada desde que a ficha
foi escrita), `learn_apply.py` não atualiza `index.json` nem grava snapshot — o estado antes e
depois da tentativa falha é idêntico, exceto por uma entrada `result: failed` no histórico (para
auditoria: sabemos que foi tentado e falhou, mesmo que nada tenha mudado). O item permanece
`status: proposed`; o agente relata o erro ao usuário e, se a causa for a ficha estar desatualizada
(ex.: `AGENTS.md` mudou desde a análise), sugere regenerar aquele item da proposta.

## Migração de schema (`index.json` / `learning-entry.md`)

`index.json.schema_version` (hoje `1`, ver `assets/templates/index-schema.json`) muda só quando o
*shape* de um registro de learning muda de forma incompatível (ex.: um campo que era string vira
lista). Quando isso acontecer:

1. A nova versão da skill inclui, em `scripts/`, uma migração pontual (`learn_migrate_v1_to_v2.py`
   ou similar) que lê `index.json` no schema antigo, transforma cada registro, e escreve o novo
   `index.json` com `schema_version` atualizado — nunca in-loco sem backup: grava
   `index.json.pre-migration-v1` antes de sobrescrever.
2. `learnings/<id>.md` individuais são migrados sob demanda (lazy): um campo de frontmatter ausente
   é tratado como "precisa de migração" na próxima vez que o arquivo for lido por qualquer script,
   e o agente propõe a atualização de frontmatter como um `Rule`/`Documentation` interno de baixa
   prioridade, passando pelo mesmo gate de aprovação — a migração de dados do próprio sistema de
   aprendizado não é diferente de qualquer outra alteração permanente.
3. Versões antigas de `.agents/learn/` sem `schema_version` são tratadas como `schema_version: 1`
   implícito (o valor introduzido nesta versão inicial da skill).

Este projeto (o pacote da skill) não versiona automaticamente estados runtime de terceiros — a
migração é sempre executada dentro do projeto-alvo, nunca neste repositório de catálogo.
