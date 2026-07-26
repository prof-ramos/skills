# IDs e versionamento

## Formato de ID

`LP-` + 6 dígitos com zero à esquerda (`LP-000001`, `LP-000123`, ...). Alocado por
`scripts/learn_id.py`, que incrementa `.agents/learn/.counter` sob lock de arquivo (`fcntl.flock`)
para evitar colisão entre chamadas concorrentes.

**IDs podem ter lacunas.** Um ID é alocado quando um candidato *entra* na proposta (passo 6-7 do
fluxo em `architecture.md`), não antes. Se, por algum motivo, um ID alocado acabar não sendo usado
(ex.: o candidato foi descartado entre a alocação e a escrita da proposta), esse número nunca é
reaproveitado. Isso é deliberado: reaproveitar IDs quebraria a garantia de que um ID sempre aponta
para o mesmo conteúdo histórico, mesmo que esse conteúdo nunca tenha sido promovido — o que
importa para auditoria é que `LP-000042` signifique sempre a mesma coisa, não que a sequência seja
contígua.

## Versionamento = confiança, não arbitrário

Cada learning tem `MAJOR.MINOR.REVISION`. Em vez de um esquema semver genérico desconectado do
domínio, a versão inicial é fixada diretamente pela matriz de decisão do RF (número de ocorrências
independentes de evidência observadas):

| Ocorrências | Nível de confiança (`confidence_tier`) | Versão inicial |
|---|---|---|
| 1 | `suggestion` (Sugestão) | `0.1.0` |
| 2 | `medium` (Confiança média) | `0.2.0` |
| 3 | `candidate_rule` (Regra candidata) | `0.3.0` |
| 5+ | `consolidated_rule` (Regra consolidada) | `1.0.0` |

Justificativa: sem essa amarração, a versão seria só um contador cosmético. Amarrando-a à matriz de
decisão, **a versão por si só já responde "o quão validado é isto?"** sem precisar abrir a ficha —
útil tanto para o agente decidir se deve propor promoção automática de um `Rule` de `0.3.0` para
`1.0.0` quando uma quinta ocorrência aparecer, quanto para um humano auditando `index.json`.

Depois da versão inicial, os bumps seguem semver convencional dentro desse domínio:

- **REVISION** (`x.y.Z`): correção cosmética — texto, formatação, exemplo adicionado — sem mudar o
  que o learning efetivamente prescreve.
- **MINOR** (`x.Y.z`): a evidência/confiança cresce (nova ocorrência observada) **sem** mudar o
  significado do learning. Uma nova ocorrência sempre dispara, no mínimo, um bump de MINOR e uma
  reavaliação do `confidence_tier` contra a tabela acima.
- **MAJOR** (`X.y.z`): o comportamento prescrito muda de fato, ou a `category`/`scope` muda (ex.:
  um `AntiPattern` que virou `Rule` porque ganhou uma forma positiva de agir, ou um learning que
  subiu de escopo `project` para `global` com evidência cross-projeto).

## Por que não usar hash de conteúdo como ID

Um ID sequencial e humano-legível (`LP-000123`) é o que aparece em comandos de aprovação
(`aplicar LP-000123`) e em texto livre de commits/proposta — precisa ser curto o suficiente para o
usuário digitar de cabeça. Um hash de conteúdo serviria para deduplicação automática, mas isso já é
coberto por `learn_search.py` (RF-04) de forma mais robusta (compara por título normalizado +
categoria + escopo, não por igualdade byte-a-byte, que quebraria com qualquer parafraseio).
