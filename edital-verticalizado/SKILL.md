---
name: edital-verticalizado
version: 1.0.0
description: Transforma editais de concurso público em edital verticalizado estruturado (tabela por tópico estudável). Aceita PDF, HTML, Markdown, DOCX, TXT ou texto colado. Entrega Markdown, CSV, XLSX ou JSON.
tags:
  - concursos
  - edital
  - estudo
  - verticalizado
  - planejamento
---

# Edital Verticalizado

Extrai o conteúdo programático de um edital de concurso público e o transforma em uma tabela auditável linha a linha — uma linha por tópico estudável.

---

## O que é um edital verticalizado

Um edital verticalizado converte blocos extensos de texto em linhas e colunas estruturadas. Cada linha representa um item estudável independente. Cada coluna representa uma informação útil para controle de estudo:

| Coluna | Descrição |
|---|---|
| ID | Identificador único (prefixo + número, ex: DC-001) |
| Cargo | Cargo ao qual o tópico se aplica |
| Bloco | Conhecimentos Básicos / Específicos / Especializados |
| Disciplina | Nome padronizado da disciplina |
| Área/Eixo | Eixo temático (inferido quando ausente do edital) |
| Assunto | Agrupamento dentro da disciplina |
| Tópico | Item estudável principal |
| Subtópico | Detalhamento do tópico (quando presente no edital) |
| Texto original do edital | Redação exata do edital (preservada) |
| Página/Fonte | Referência à seção, item ou página do edital |
| Prioridade | Alta / Média / Baixa / A verificar |
| Status | Não iniciado / Estudando / Concluído / Revisar |
| Observações | Ambiguidades, OCR ruim, normas incompletas |

---

## Como usar

### Passo 1 — Forneça o edital

Aceita qualquer um destes formatos:

- Arquivo Markdown, TXT, HTML ou DOCX
- PDF (extraia o texto antes com `pdftotext` ou `pdfplumber`)
- Texto colado diretamente no prompt
- Link para página oficial (o agente busca e extrai)

### Passo 2 — Solicite a verticalização

Exemplos de prompts:

```
Verticalize este edital em Markdown.
```

```
Gere o edital verticalizado em CSV, separado por ponto e vírgula.
```

```
Processe apenas o cargo Analista Judiciário e entregue em JSON.
```

```
Verticalize e inclua colunas de controle de estudo (Revisão 1, 2, 3, Questões, Acertos, Erros).
```

### Passo 3 — Use o driver (via agente)

O agente pode rodar o driver diretamente para processar um arquivo local:

```bash
# Markdown (padrão)
.claude/skills/run-edital-verticalizado/driver.sh <arquivo_edital>

# CSV
.claude/skills/run-edital-verticalizado/driver.sh <arquivo_edital> csv

# JSON
.claude/skills/run-edital-verticalizado/driver.sh <arquivo_edital> json

# Filtrar por cargo
.claude/skills/run-edital-verticalizado/driver.sh <arquivo_edital> md "Analista Judiciário"
```

---

## Regras de extração

1. Localize o conteúdo programático (não processe outras seções do edital).
2. Separe blocos: Conhecimentos Básicos / Específicos / Complementares.
3. Identifique: Disciplina → Assunto → Tópico → Subtópico.
4. Preserve o texto original na coluna `Texto original do edital`.
5. Crie IDs únicos: 2 letras do prefixo da disciplina + número sequencial (LP-001, DC-001...).
6. Inclua referência de seção/item no campo `Página/Fonte`.
7. Não invente tópicos. Não remova conteúdo relevante.
8. Separe diplomas legais em linhas distintas quando listados por ponto e vírgula.
9. Não quebre expressões compostas consolidadas ("Administração Pública direta e indireta").
10. Use `Status: Não iniciado` e `Prioridade: A verificar` como padrão.
11. Sinalize ambiguidades ou OCR ruim no campo `Observações`.
12. Prioridade só pode ser Alta/Média/Baixa com critério declarado; sem estatística, use "A verificar".

---

## Formatos de entrega

| Formato | Como solicitar |
|---|---|
| Markdown | Padrão — não precisa especificar |
| CSV (`;` como separador, UTF-8) | `driver.sh <arquivo> csv` |
| JSON (schema validado) | `driver.sh <arquivo> json` |
| XLSX | Solicite ao agente gerar via script Python |

---

## Campos de controle de estudo (opcionais)

Quando o usuário pedir colunas de acompanhamento:

| Campo | Valores possíveis |
|---|---|
| Status | Não iniciado / Estudando / Concluído / Revisar |
| Revisão 1 / 2 / 3 | Data da revisão |
| Questões | Quantidade de questões resolvidas |
| Acertos / Erros | Contagem |
| % Acerto | Calculado |

---

## Campos de priorização

| Prioridade | Critério (sem estatística) |
|---|---|
| Alta | Tema muito extenso, central ou detalhado no edital |
| Média | Tema relevante, mas menos detalhado |
| Baixa | Tema acessório ou genérico |
| A verificar | Insuficiente para classificar |

Nunca afirme recorrência em provas anteriores sem fonte fornecida.

---

## Tratamento de leis e normas

- Preservar o nome exato da norma (Lei nº, Resolução CSJT, Decreto...).
- Separar diplomas listados por `;` em linhas distintas.
- Anotar em `Observações` quando a norma for infralegal (resolução, portaria).

---

## Tratamento de múltiplos cargos

- Usar coluna `Cargo` para separar conteúdo por cargo.
- Identificar conteúdo comum ("todos os cargos") vs. específico por cargo.
- Blocos possíveis: Conhecimentos Básicos / Específicos / Especializados / Prova Discursiva / Prova Prática / Títulos.

---

## Validação antes de entregar

- [ ] Todos os blocos do edital foram processados.
- [ ] Nenhuma disciplina relevante ficou de fora.
- [ ] Rastreabilidade mantida (Texto original + Página/Fonte).
- [ ] Sem linhas duplicadas desnecessárias.
- [ ] Sem conteúdo inventado.
- [ ] Siglas e nomes de leis preservados.
- [ ] IDs únicos.
- [ ] Tabela copiável para Excel, Google Sheets ou Notion.
