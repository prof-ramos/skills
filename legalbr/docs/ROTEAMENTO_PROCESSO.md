# Roteamento de processo para matéria, jurisprudência e skills

## Decisão arquitetural

Podemos usar TypeSafe AI para classificar e encaminhar um processo, mas ele não
deve substituir o índice nem ser consultado com as 2.149 skills ou 9.641
ementas como opções de uma única pergunta. O desenho correto é hierárquico:

```text
processo recebido
      ↓
recuperação determinística (SQLite/FTS + filtros)
      ↓ candidatos pequenos
TypeSafe Choice/Score/Noul
      ↓
matéria provável + forma + precedentes candidatos
      ↓ confiança suficiente? ── não ── revisão humana
      ↓ sim
agente redige usando somente o contexto selecionado
```

A documentação do TypeSafe descreve `Choice`, `Score` e `Noul` como perguntas
tipadas com `confidence` e `probabilities`. Isso é adequado para roteamento,
não para transformar uma resposta probabilística em prova de vigência,
autoridade ou aplicabilidade jurídica.

## Perguntas recomendadas

As perguntas devem receber o processo e uma lista curta de candidatos já
recuperados:

- `materia`: ramo jurídico principal entre os candidatos.
- `forma`: peça ou tipo de procedimento compatível, quando houver.
- `jurisprudencia`: quais precedentes candidatos têm pertinência factual.
- `needs_review`: se a confiança, conflito ou ausência de candidato exige
  revisão humana.

Não se deve perguntar ao modelo “qualquer skill do corpus” sem fornecer
critérios e candidatos. O conjunto de opções deve ser finito, rastreável e
ligado ao UUID/path da skill ou ao tribunal/id do julgado.

## Contrato de saída

Uma aplicação que usar TypeSafe deve persistir algo equivalente a:

```json
{
  "process_id": "processo-interno-123",
  "as_of": "2026-09-21",
  "matter": {
    "slug": "consumidor",
    "confidence": 0.91,
    "candidates": ["consumidor", "contratos"]
  },
  "skills": [
    {"id": "uuid-da-skill", "path": "materia/consumidor/.../SKILL.md", "confidence": 0.84}
  ],
  "jurisprudence": [
    {"court": "stj", "id": "123", "confidence": 0.78}
  ],
  "needs_review": false
}
```

O sistema deve guardar também a consulta, o índice/snapshot usado e as fontes
oficiais. A resposta do TypeSafe é uma decisão de roteamento; a fundamentação
final precisa apontar para os documentos recuperados e ser conferida antes do
uso jurídico.

## Integração futura

O SDK JavaScript atual do TypeSafe pode ser usado na aplicação consumidora com
`TypeSafeClient.systemOne` e perguntas `choice`/`score`. O `legalbr` não inclui
essa dependência, chamada remota ou chave de API: permanece um corpus
reutilizável e auditável.
