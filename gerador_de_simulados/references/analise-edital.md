---
title: Guia de Análise de Editais
description: Metodologia detalhada para extração de informações de editais de concursos públicos
type: reference
---

# Guia de Análise de Editais

Metodologia detalhada para extração de informações de editais de concursos públicos.

## Estrutura Típica de um Edital

### 1. Cabeçalho e Identificação

Localizar no início do documento:

- Nome do órgão/instituição
- Número do edital (ex: "Edital nº 01/2024")
- Modalidade do concurso (público, seletivo, processo simplificado)
- Banca organizadora (geralmente no rodapé ou logo)

### 2. Seção de Provas e Avaliações

Buscar por termos:

- "Das Provas"
- "Da Avaliação"
- "Das Etapas do Concurso"
- "Do Processo de Seleção"

**Informações a extrair:**

```text
PROVA OBJETIVA
├── Total de questões: [número]
├── Conhecimentos Gerais: [número] questões
│   ├── Língua Portuguesa: [X] questões
│   ├── Raciocínio Lógico: [X] questões
│   ├── Informática: [X] questões
│   └── [Outras disciplinas...]
├── Conhecimentos Específicos: [número] questões
│   ├── [Disciplina 1]: [X] questões
│   ├── [Disciplina 2]: [X] questões
│   └── [Outras disciplinas...]
└── Peso/Pontuação: [valor por questão ou total]

PROVA DISCURSIVA (se houver)
├── Tipo: [redação, estudo de caso, peça técnica]
├── Número de questões: [número]
└── Critérios de avaliação: [lista]
```

### 3. Conteúdo Programático

Geralmente em anexo separado ou seção específica. Buscar por:

- "Conteúdo Programático"
- "Programa das Disciplinas"
- "Anexo I" ou "Anexo II"

**Estrutura de extração:**

Para cada disciplina, listar:

1. Nome da disciplina
2. Tópicos/subtópicos detalhados
3. Referências bibliográficas (quando informadas)

### 4. Identificação da Banca

**Locais comuns:**

- Logotipo no cabeçalho/rodapé
- Seção "Da Banca Examinadora"
- "Organização e Realização"
- Rodapé das páginas
- Site de inscrição

**Formato típico:**

> "A organização, elaboração e aplicação das provas serão de responsabilidade da [NOME DA BANCA]"

## Checklist de Extração

```text
[ ] Órgão contratante identificado
[ ] Cargo(s) de interesse identificado(s)
[ ] Banca examinadora identificada
[ ] Total de questões objetivas
[ ] Distribuição conhecimentos gerais/específicos
[ ] Disciplinas de conhecimentos gerais listadas
[ ] Disciplinas de conhecimentos específicos listadas
[ ] Peso/pontuação por questão ou área
[ ] Presença de prova discursiva (sim/não)
[ ] Formato da prova discursiva (se aplicável)
[ ] Duração da prova
[ ] Data prevista de aplicação
```

## Tabela de Distribuição Padrão

Montar tabela no seguinte formato:

| Área        | Disciplina   | Qtd. Questões | Peso | Total Pontos |
| ----------- | ------------ | ------------- | ---- | ------------ |
| Gerais      | Português    | 10            | 1,0  | 10,0         |
| Gerais      | Matemática   | 5             | 1,0  | 5,0          |
| Específicos | [Disciplina] | 20            | 2,0  | 40,0         |
| **TOTAL**   |              | **35**        |      | **55,0**     |

## Casos Especiais

### Edital sem Detalhamento de Questões por Disciplina

Quando o edital informa apenas "30 questões de Conhecimentos Gerais" sem especificar quantas de cada disciplina:

1. Verificar provas anteriores do mesmo órgão/banca
2. Estimar distribuição proporcional baseada na extensão do conteúdo programático
3. Informar ao usuário que a distribuição é estimada

### Múltiplos Cargos no Mesmo Edital

Identificar e separar:

- Provas comuns a todos os cargos
- Provas específicas por cargo
- Conteúdo programático diferenciado

### Editais com Blocos de Conhecimento

Alguns editais organizam por "blocos" em vez de disciplinas:

- Bloco I: Conhecimentos Básicos
- Bloco II: Conhecimentos Complementares
- Bloco III: Conhecimentos Específicos

Manter a estrutura original do edital.

## Validação Final

Antes de prosseguir para a pesquisa de questões, confirmar:

1. **Soma de questões:** O total parcial deve ser igual ao total geral
2. **Banca identificada:** Sem esta informação, não prosseguir
3. **Conteúdo programático completo:** Listar todas as disciplinas
4. **Formato da prova claro:** Objetiva, discursiva, mista
