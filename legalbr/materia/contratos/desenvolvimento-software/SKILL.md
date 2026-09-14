---
id: "8717238c-56f4-4d36-bd9c-432faf8f9424"
name: "desenvolvimento-software"
title: "Desenvolvimento de Software sob Encomenda"
category: "materia"
materia: "contratos"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/contratos/desenvolvimento-software.md"
triggers:
  - "desenvolvimento de software"
  - "software sob encomenda"
  - "work for hire"
  - "cessão de código"
  - "Lei 9.609"
  - "Lei 9.610"
  - "escrow de código"
  - "código-fonte"
  - "bibliotecas pré-existentes"
  - "open source"
  - "propriedade intelectual em software"
  - "fábrica de software"
description: "Desenvolvimento de software sob encomenda: titularidade (Lei\n9.609/98 art. 4 + Lei 9.610/98 arts. 49-52), cessão autoral,\nescrow, open source, work-for-hire, aceitação, reps."
---

# Desenvolvimento de Software

## Base legal

| Diploma | Conteúdo |
|---|---|
| **Lei 9.609/98** | Software: proteção e regime especial |
| **Lei 9.609 art. 4** | **Titularidade do empregador/contratante** quando obra de encomenda OU empregado (com causa) |
| **Lei 9.610/98 arts. 49-52** | Cessão de direitos patrimoniais: escrita, expressa, com escopo definido |
| Lei 9.279/96 | Patentes (algoritmos elegíveis sob requisitos restritos) |
| Marco Civil (12.965/14) | Privacidade no produto |
| LGPD | Privacy by design (art. 46) |
| Lei 14.063/20 | Assinatura eletrônica |
| CC 421-A | Paridade B2B |

## Natureza

| Aspecto | Conteúdo |
|---|---|
| Modalidade | **Empreitada de obra intelectual** (CC 610) + cessão de direitos |
| Distinção | Diferente de **prestação contínua** (alocação de body shop): esta é prestação de serviços (CC 593) |
| Bem produzido | Obra autoral (Lei 9.610) protegida + software (Lei 9.609) |

## Estrutura mínima

| Bloco | Conteúdo |
|---|---|
| Escopo | Especificação técnica anexa + critérios de aceitação |
| Cronograma | Marcos (milestones) + entregáveis |
| Preço | Fixo / por hora / per milestone |
| **Titularidade do código** | Cliente OU desenvolvedor (definir) |
| Bibliotecas pré-existentes | Inventário + licenças |
| **Open source** | Compatibilidade + obrigações copyleft |
| Aceitação | Critérios + prazo + presunção |
| Garantia | Bugs + correções |
| Escrow | Em hipóteses críticas |
| Manutenção pós-entrega | Opcional / SLA |
| Confidencialidade | Recíproca |
| Indenidade | Por violação de PI de terceiros |

## Cláusulas obrigatórias

| # | Cláusula | Norma |
|---|---|---|
| 1 | **Escopo detalhado** + especificações anexas | Empreitada CC 610 |
| 2 | **Titularidade** do código encomendado | Lei 9.609 art. 4 (default = contratante): **explicitar mesmo assim** |
| 3 | **Cessão expressa** de direitos autorais (Lei 9.610 art. 49) | Cessão escrita, com escopo |
| 4 | **Bibliotecas pré-existentes**: inventário + licença | Inventário em anexo |
| 5 | **Open Source**: declaração + compatibilidade | Vedar GPL contagiante se proprietário |
| 6 | **Reps de não-infração** de PI de terceiros | Indenidade |
| 7 | Aceitação por critérios objetivos | CC 615-616 |
| 8 | Garantia de **bugs** (60-90 dias mínimo) | Vícios |
| 9 | **Código-fonte + documentação** entregues | Inclui build instructions + dependências |
| 10 | **Confidencialidade** | CC 422 + Lei 9.279 art. 195 |

## Cláusulas acidentais críticas

| Cláusula | Função |
|---|---|
| **Escrow de código** | Depósito em terceiro neutro: liberação por triggers (insolvência, descontinuação) |
| **Work-for-hire enhanced** | Reforço de cessão + renúncia de morais (eficácia limitada: Lei 9.610 art. 27) |
| **Background IP / Foreground IP** | Distinção entre PI pré-existente e nova |
| **Reverse engineering** | Lei 9.609 art. 6 III: interoperabilidade admitida |
| **Non-compete** do desenvolvedor | Limitado e remunerado (CC 422 + CLT 482 g, se empregado) |
| **Não-solicitação** de empregados | 12-24 meses |
| **Manutenção pós-entrega** | SLA + tarifa |
| **Atualizações** | Cliente recebe melhorias gerais (definir) |
| **Cap de responsabilidade** | 100-200% do contrato |

## Titularidade: Lei 9.609 art. 4

| Hipótese | Titular |
|---|---|
| **Encomenda** (sem vínculo empregatício) | **Contratante** (presunção): salvo pacto em contrário |
| **Empregado** durante vínculo + relacionado à função | **Empregador** |
| Empregado **fora** da função + sem recursos do empregador | **Empregado** |
| Pesquisador acadêmico | Regulamento institucional |

> **Reforço contratual**: ainda que a lei já atribua ao contratante, cláusula explícita de cessão **reduz litígio** e ativa Lei 9.610 art. 50 (forma escrita).

## Direitos morais (Lei 9.610 art. 27)

| | Conteúdo |
|---|---|
| Regra | **Inalienáveis e irrenunciáveis** |
| Implicação | Autor mantém **direito ao nome** mesmo após cessão patrimonial |
| Software | Lei 9.609 art. 2 §1: **limita direitos morais** ao nome e oposição a modificações desautorizadas |
| Cláusula útil | Renúncia ao exercício de moral + autorização de modificações |

## Open Source: risco crítico

| Licença | Compatibilidade com produto proprietário |
|---|---|
| MIT, BSD, Apache 2.0 | **Permissivas**: compatíveis (Apache requer NOTICE) |
| LGPL | Dinâmica permitida; estática gera contágio |
| **GPL v2/v3** | **Copyleft contagiante**: exige abertura do produto |
| AGPL | Contagiante mesmo em SaaS |
| MPL | Per-file copyleft |

> **Cláusula obrigatória**: vedar inclusão de bibliotecas **GPL/AGPL** sem autorização prévia. Exigir SBOM (Software Bill of Materials).

## Escrow de código

| Aspecto | Conteúdo |
|---|---|
| Quando exigir | Software crítico para operação do cliente |
| Depositário | Terceiro neutro (cartório, escrow agent) |
| Conteúdo | Código-fonte + dependências + build instructions + credenciais |
| **Triggers de liberação** | Falência, descontinuação, breach material não sanado |
| Atualização | Periódica (trimestral / por release) |
| Direitos pós-liberação | Cliente recebe licença para **manter** (não para revender) |

## Aceitação (CC 615-616)

| Modelo | Conteúdo |
|---|---|
| Aceitação por marcos | Cada milestone tem critérios objetivos |
| Prazo de teste | 15-30 dias após entrega |
| Presunção de aceitação | Silêncio após prazo = aceito |
| Recusa | Fundamentada + lista de não-conformidades |
| Vícios ocultos | Prazo decadencial conta da ciência, limitado a 180 dias em bens móveis (CC 445 §1); 90 dias se relação de consumo (CDC 26 II) |

## Roteiro de redação

1. **Especificação técnica** anexa: vincular à empreitada;
2. **Cronograma com milestones** + entregáveis + pagamento per milestone;
3. **Titularidade**: cliente (default) com cessão expressa OU desenvolvedor com licença;
4. **Inventário de background IP** + open source (SBOM);
5. **Aceitação** com critérios objetivos + prazo;
6. **Garantia** + correção de bugs;
7. **Escrow** se crítico;
8. **Confidencialidade** + non-solicit;
9. **Indenidade por PI** de terceiros (cap diferenciado);
10. **Cap geral** de responsabilidade.

## Erros a evitar

- Não regular **titularidade**: Lei 9.609 art. 4 ajuda, mas cláusula evita disputa;
- Esquecer **cessão expressa** (Lei 9.610 art. 49: formal);
- Não inventariar **open source** (risco de contágio GPL);
- Aceitar inclusão de **GPL/AGPL** em produto proprietário;
- Aceitação **sem critérios objetivos** (gera litígio);
- Garantia contratual de bugs inferior a 90 dias (CDC 26 II em consumo; CC 445 nas relações civis);
- Esquecer **build instructions** na entrega (código sem reproduzibilidade);
- Não regular **manutenção** pós-entrega (cliente fica refém);
- Escrow **sem trigger objetivo** (inútil);
- Confundir **empreitada** com prestação contínua (regimes distintos);
- Renúncia genérica a direitos morais (inválida: Lei 9.610 art. 27);
- Tratar desenvolvedor como funcionário sem cumprir CLT (passivo trabalhista);
- Não exigir **SBOM** + reps de não-infração;
- Cap igual ou maior em **PI/LGPD/dolo** (devem ser ilimitados).
