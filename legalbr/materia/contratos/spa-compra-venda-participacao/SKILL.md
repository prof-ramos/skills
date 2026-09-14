---
id: "1d35055b-9704-4a13-888d-13fddfaaed2c"
name: "spa-compra-venda-participacao"
title: "SPA: Compra e Venda de Participação Societária (Share Purchase Agreement)"
category: "materia"
materia: "contratos"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/contratos/spa-compra-venda-participacao.md"
triggers:
  - "SPA"
  - "share purchase agreement"
  - "compra e venda de ações"
  - "compra e venda de quotas"
  - "condições precedentes"
  - "material adverse change"
  - "earn-out"
  - "escrow"
  - "representations and warranties"
  - "declarações e garantias"
  - "indemnification"
  - "cap basket de minimis"
  - "locked box"
  - "completion accounts"
description: "SPA (compra e venda de quotas/ações): CPs (condições precedentes), MAC, R&W, indemnification (cap/basket/de minimis), escrow, earn-out, locked box vs completion accounts, non-compete, fechamento e cláusulas de preço."
---

# SPA: Share Purchase Agreement

## Base legal

- **CC 481-532** (compra e venda: aplicação subsidiária);
- **CC 421-A** + **Lei 13.874/2019** (paridade B2B);
- **LSA 6.404/1976** (transferência de ações);
- **CC 1.057** (cessão de quotas em LTDA);
- **Lei 12.529/2011** (CADE: notificação se preencher critérios);
- **CVM Res. 215/2024** (OPA: em vigor desde 01/10/2025, vigência adiada pela Res. CVM 230) + LSA 254-A (OPA alienação de controle);
- **Lei 9.307/1996** (arbitragem: usual em M&A);
- **CISG Dec. 8.327/2014** (compra e venda internacional: ações geralmente excluídas, art. 2 "d" CISG).

## Fases típicas de uma operação

| Fase | Documento |
|---|---|
| 1. NDA | **Non-Disclosure Agreement** |
| 2. Term sheet / LOI / MOU | **Não vinculante** salvo exclusividade + confidencialidade |
| 3. Due diligence | Legal, financeira, fiscal, trabalhista, ambiental, IP |
| 4. **Signing** (SPA) | Assinatura: gera obrigações condicionadas |
| 5. **Condições precedentes** | Implementação |
| 6. **Closing** | Transferência efetiva + pagamento |
| 7. Pós-closing | Earn-out + indemnification + integration |

## Estrutura do SPA: partes essenciais

### 1. Definições
- Cláusula padronizada (Affiliates, Business Day, Encumbrance, Knowledge, Material Adverse Change, etc.);
- **Knowledge qualifier**: actual / constructive / imputed.

### 2. Objeto
- Quotas / ações descritas com precisão (número, classe, série, % do capital);
- **Free and clear** de ônus, gravames, opções de terceiros;
- Confirmação de **plena titularidade** pelo vendedor.

### 3. Preço (Purchase Price)

#### Mecanismos de determinação

| Mecanismo | Conteúdo |
|---|---|
| **Locked box** | Preço fixo na data do balanço de referência (locked box date); risco transferido a partir desta data; mecanismo de leakage controlado |
| **Completion accounts** | Preço estimado no signing + ajuste no closing com base em balanço auditado (cash-free, debt-free + working capital adjustment) |
| **Earn-out** | Parcela do preço atrelada a performance futura (EBITDA, faturamento, marcos): período típico 1-3 anos |
| **Equity rollover** | Vendedor mantém participação (em deal com PE) |

#### Componentes
- **Enterprise value** → **equity value** (deduzir net debt, ajustar working capital);
- **Earn-out**: definir métrica + período + threshold + cap + governance protection (evita esvaziamento);
- **Escrow** (caução): % do preço (5-15%) retido em conta de terceiro por 12-36 meses para garantir indemnification.

#### Locked box vs completion accounts

| Aspecto | Locked box | Completion accounts |
|---|---|---|
| Risco econômico | Transferido na locked box date | Transferido no closing |
| Disputa pós-closing | Menor (preço fixo) | Maior (ajuste contábil) |
| Necessidade | Balanço auditado pré-signing | Balanço auditado pós-closing |
| Leakage | Controle por cláusula específica | N/A |
| Padrão de mercado | Europa | Brasil / EUA |

### 4. Condições Precedentes (CPs)

| CP típica | Conteúdo |
|---|---|
| **Aprovação CADE** | Se preencher critérios da Lei 12.529 (R$ 750M e R$ 75M): sob pena de **gun-jumping** |
| **Aprovações regulatórias** | ANATEL, BACEN, ANS, ANVISA, ANEEL conforme setor |
| **Anuência de terceiros** | Bancos (covenants), landlords, parceiros (change of control) |
| **Inexistência de MAC** | Material Adverse Change (definição negociada) |
| **R&W bring-down** | Declarações verdadeiras no closing |
| **Long-stop date** | Data-limite para CPs (6-12 meses) |
| **Reestruturações pré-closing** | Carve-out, spin-off, capitalizações |

> **CADE: gun-jumping**: integrar operações antes da aprovação (art. 88 §3 Lei 12.529): multa R$ 60k a R$ 60M.

### 5. MAC (Material Adverse Change / Effect)

> Cláusula que permite ao comprador **resilir** o SPA entre signing e closing se houver mudança material adversa.

**Carve-outs típicos** (não constituem MAC):
- Condições macroeconômicas gerais;
- Mudanças regulatórias setoriais;
- Atos de guerra, terrorismo, pandemias (cláusula pós-COVID);
- Variações cambiais ordinárias;
- Implementação do próprio SPA.

**Disproportionate impact**: aplica-se apenas se afetar o target **desproporcionalmente**.

### 6. Representations and Warranties (Declarações e Garantias)

| Categoria | Exemplos |
|---|---|
| **Fundamental R&W** | Title, capacity, authorization, no conflicts: sem cap/basket/de minimis |
| **General R&W** | Financial statements, contracts, employees, real estate, IP, taxes, litigation, environmental, compliance |
| **Knowledge qualifiers** | "Best knowledge of the seller": definir lista de pessoas + diligência |
| **Disclosure schedules** | Exceções às R&W: anexo essencial |

### 7. Indemnification

| Limite | Conteúdo |
|---|---|
| **Cap** | Limite máximo de indenização (% do preço: fundamental 100%; general 10-30%) |
| **Basket / threshold** | Franquia: tipping basket (acima dispara tudo) ou deductible (só excesso): 0,5%-2% do preço |
| **De minimis** | Valor mínimo por claim individual: exclui ruído |
| **Survival period** | Prazo de garantia: fundamental (até prescrição: 10 anos CC 205); general (12-24 meses); tributário (até prescrição: 5 anos + 1); trabalhista (5 anos + 2 = 7) |
| **Specific indemnity** | Itens conhecidos cobertos integralmente, sem cap/basket (passivos de DD) |
| **Mitigation** | Dever de mitigação (CC 422 + art. 77 CISG analógico) |
| **Sandbagging** | Pro-sandbag (comprador indeniza mesmo sabendo) vs anti-sandbag |

> **STJ: indemnification**: cláusulas são plenamente válidas em B2B (CC 421-A).

### 8. Covenants

| Covenant | Conteúdo |
|---|---|
| **Interim operating covenants** | Vendedor opera no curso ordinário entre signing e closing; veda extraordinários sem consent |
| **Reasonable best efforts** | Implementar CPs |
| **No-shop** | Vendedor não negocia com terceiros |
| **Cooperation** | Anuências, transition |
| **Tax matters** | Pre-closing returns, refunds, contests |

### 9. Non-compete e non-solicitation
- Vendedor (founder) + key executives;
- Prazo 3-5 anos (CADE Resolução 17/2016: guideline);
- Território + atividade + compensação opcional;
- Anti-poaching de funcionários: 12-24 meses.

### 10. Closing
- **Closing checklist**: entrega simultânea;
- **Closing deliverables**: livros sociais transferidos, atas, resignações, certificados, garantias, escrow, pagamento;
- Lugar (usualmente escritório dos advogados);
- **Drop-dead date** se CPs não cumpridas.

### 11. Resolução de conflitos
- **Arbitragem** (cláusula cheia): CAM-CCBC, CAMARB, CCI;
- Multi-tier (negotiation → mediation → arbitration);
- **Foro residual** para tutela cautelar (Lei 9.307 art. 22-A).

## Aprovações regulatórias críticas

### CADE (Lei 12.529/2011)
| Critério | Valor |
|---|---|
| Grupo 1 | Faturamento ≥ **R$ 750M** |
| Grupo 2 | Faturamento ≥ **R$ 75M** |
| Notificação | **Antes do closing**: controle prévio |
| Gun-jumping | Multa R$ 60k a R$ 60M + nulidade |
| Procedimentos | Sumário (40 dias úteis) ou ordinário (até 240 dias) |

### Outras
- **BACEN**: instituições financeiras (Res. CMN 4.122);
- **ANS**: operadoras de saúde (RN 561/2022);
- **ANATEL**: telecom;
- **ANEEL**: geradoras/distribuidoras;
- **Foreign investor**: Registro RDE-IED no BACEN.

## Tributação

| Tributo | Incidência |
|---|---|
| **Ganho de capital PF** | 15% a 22,5% (Lei 13.259/2016: alíquotas progressivas) |
| **Ganho de capital PJ** | IRPJ 15% + 10% adicional + CSLL 9% (lucro real) ou base presumida ajustada |
| **Earn-out** | Tributação no recebimento (RFB COSIT 58/2014) |
| **ITBI** | Sobre integralização de imóveis no target: verificar Tema 796 STF |
| **ITCMD** | Em doações de quotas/ações no contexto |
| **IRRF não residente** | 15% (regra geral) ou 25% (paraíso fiscal: IN RFB 1.037) |

## OPA: alienação de controle (LSA 254-A)

- S/A aberta: alienação direta ou indireta de controle → **OPA obrigatória** aos minoritários **ON** por **80%** do preço;
- **CVM Res. 215/2024** (em vigor desde 01/10/2025, adiamento pela Res. CVM 230): substituiu a Res. CVM 85/2022 com ritos ordinário e automático de registro;
- Inclusão de ações **PN com tag** se estatuto previr (LSA 17 §1);
- Estrutura via aquisição **indireta** (holding) → STF/CVM exige look-through.

## Jurisprudência consolidada

| Tese | Conteúdo |
|---|---|
| **Earn-out (tributação)** | Tributação no recebimento, não na assinatura (Solução COSIT 58/2014) |
| **CADE: gun-jumping** | Integração antes da aprovação configura ato (decisões 2018-2024) |
| **Indemnification** | Cláusulas de indenização negociadas entre empresários são válidas: autonomia privada e intervenção mínima (CC 421-A) |
| **STJ: R&W** | Falsidade de R&W é vício do consentimento + breach contratual |
| **STF Tema 796** | Imunidade do ITBI na integralização não alcança o valor dos bens que exceder o limite do capital social a ser integralizado |
| **CVM Res. 215/2024** | Nova disciplina de OPA (substitui a Res. CVM 85/2022): em vigor desde 01/10/2025 |

## Roteiro prático de redação

1. **NDA** + LOI/term sheet (exclusividade + confidencialidade vinculantes);
2. **Due diligence** com escopo definido + report;
3. Definir **estrutura**: 100% / minority / earn-out / rollover;
4. **Preço**: locked box ou completion accounts + earn-out + escrow;
5. **CPs**: CADE, regulatórios, terceiros, reorgs;
6. **MAC** com carve-outs;
7. **R&W** divididas em fundamental e general; disclosure schedules;
8. **Indemnification**: cap + basket + de minimis + survival + specific;
9. **Non-compete** + non-solicitation;
10. **Closing checklist** detalhado;
11. **Arbitragem** cheia;
12. Atas societárias do closing (transferência + livro).

## Erros a evitar

- Fechar operação acima dos critérios CADE **sem notificação** (gun-jumping);
- MAC **sem carve-outs** (vendedor refém de qualquer evento);
- Indemnification **sem cap** ou cap > 100% do preço (fora do mercado);
- R&W **sem disclosure schedules** (vendedor super-indenizando);
- Knowledge qualifier **vago** (definir lista + due inquiry);
- Earn-out sem **proteção de governance** (comprador esvazia métrica);
- Locked box **sem leakage clause** (vendedor extrai valor pós-locked box);
- Esquecer **change-of-control** em contratos relevantes (bancos, clientes);
- Anti-sandbag em **specific indemnity** (anula proteção);
- Survival de **R&W tributárias < 5 anos + 1** (insuficiente);
- Non-compete **> 5 anos** ou sem território (abusivo: CADE);
- Cláusula compromissória **defeituosa** (incompleta sobre sede/idioma/regulamento);
- OPA 254-A **omitida** em alienação indireta de controle de S/A aberta;
- Não considerar **ITBI** em integralizações pré-closing (Tema 796 STF);
- **Drop-dead date** muito curto (CADE pode levar 240 dias);
- Earn-out tributado na **assinatura** (RFB COSIT 58/14: só no recebimento).
