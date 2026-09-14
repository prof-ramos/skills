---
id: "067a15c7-2195-496e-b7f2-683c9c7b152a"
name: "pld-ft-coaf-lei-9613"
title: "PLD/FT: Prevenção à Lavagem e Financiamento ao Terrorismo"
category: "materia"
materia: "consultoria"
documentType: null
version: 2
sourcePath: "lib/skills/official/materia/consultoria/compliance-integridade/pld-ft-coaf-lei-9613.md"
triggers:
  - "PLD"
  - "PLD/FT"
  - "lavagem de dinheiro"
  - "Lei 9.613"
  - "COAF"
  - "unidade de inteligência financeira"
  - "política KYC"
  - "financiamento ao terrorismo"
  - "CVM 245 investidor não residente"
  - "GAFI jurisdição investidor não residente"
description: "Deveres de PLD/FT da Lei 9.613/1998: abordagem de risco, KYC, monitoramento e COAF; inclui diligência reforçada para investidor não residente ligado a jurisdição listada pelo GAFI (RCVM 245/2026)."
---

# PLD/FT

## Base legal

- **Lei 9.613/1998** (PLD, alterada pela Lei 12.683/12);
- **Lei 13.260/2016** (terrorismo);
- **Lei 13.810/2019** (sanções ONU: congelamento de ativos) + **Decreto 9.825/2019** (regulamento: indisponibilidade de ativos + designação nacional);
- **GAFI/FATF 40 Recomendações** + **9 Recomendações Especiais** (FT);
- **Convenção de Viena 1988** + **Palermo 2000** + **Mérida 2003**;
- **OFAC, EU, UN, UK HMT, OFSI** (sanctions lists);
- Setoriais:
  - **Circular BCB 3.978/2020** (bancos);
  - **Resolução BCB 119/2021** (atualização);
  - **Resolução BCB 277/2022** (câmbio);
  - **CVM RCVM 50/2021**, alterada pela **RCVM 245/2026** (mercado de valores);
  - **SUSEP Circular 612/2020**;
  - **PREVIC Instrução 34/2020**;
  - **CFC Resolução 1.530** (contadores);
  - **OAB Provimento 188/2018 + 205/21** (advogados, com limites);
  - **CNJ Provimento 88/2019** (cartórios);
  - **COAF Resolução 36/2021** (joalheiros);
  - **Receita Federal IN RFB 1.873/2019** (imóveis);
  - **DREI** (factoring + leasing).

## Pessoas obrigadas (Lei 9.613 art. 9)

- Instituições financeiras;
- Bolsas + administradores de fundos;
- Seguradoras + previdência;
- Operadoras de câmbio + remessa;
- Factorings, leasings;
- Joalheiros + arte + antiguidades;
- Bingos + loterias + cassinos;
- Imobiliárias + corretores;
- Comerciantes de **bens de luxo** > R$ 10k;
- **Cartórios + contadores + auditores** (com limites);
- **Advogados** em **atividades transacionais** (não-judicial, limitado pelo Provimento OAB 188/18 + 205/21);
- **PEPs proxies + advisors**;
- Custodiantes + agentes fiduciários.

## Mercado de valores: RCVM 245/2026

A Resolução CVM 245/2026, vigente desde 15/07/2026, alterou a Resolução CVM 50/2021:

- exige monitoramento contínuo e reforçado nas hipóteses do art. 16, independentemente da classificação de risco do investidor;
- exige diligência reforçada em operações ou situações com investidor não residente ligado a jurisdição que não aplique ou aplique insuficientemente as recomendações do GAFI;
- admite medidas como restrição ao início da relação, limitação, postergação ou recusa de operação de maior risco, informações adicionais e encerramento quando o risco for inaceitável e não mitigável;
- alcança estruturas societárias, cadeias de controle, beneficiários finais e representantes vinculados direta ou indiretamente às jurisdições listadas.

## RBA: Abordagem Baseada em Risco

### Mapeamento de risco
- **Geographic risk**: high-risk jurisdictions (FATF black/grey list);
- **Customer risk**: PEP + structures opacas + cash-intensive;
- **Product risk**: private banking + offshore + criptoativos + correspondent banking;
- **Channel risk**: non-face-to-face + intermediado;
- **Transactional risk**: padrões atípicos.

### Tiering
- **Alto risco**: EDD;
- **Médio risco**: CDD padrão;
- **Baixo risco**: SDD simplificada.

## KYC / CDD (Customer Due Diligence)

### Mínimo
- **Identificação**: PF (nome + CPF + RG + endereço + ocupação + renda) / PJ (CNPJ + objeto + faturamento + estrutura societária + UBOs);
- **UBO até 25%** (ou critério mais conservador);
- **PEP screening** (interno + familiares + close associates);
- **Sanctions screening** (OFAC + EU + UN + OFSI + lista nacional);
- **Mídia adversa**;
- **Verificação documental** (presencial ou digital com biometria).

### EDD para alto risco
- **Source of wealth + source of funds**;
- **Background check** ampliado;
- **Aprovação senior management** para onboarding;
- **Monitoramento reforçado**;
- **Revisão periódica** mais frequente (anual ou semestral).

### Onboarding digital
- **BCB Resolução 6/2020 + Circular 3.978**: onboarding via internet + biometria;
- **Selfie + documento + liveness detection**;
- **Open Finance** (BCB) integra dados;
- **eSocial + RFB** queries.

## Monitoramento

### Sistemas
- **Rule-based** (limiares + padrões);
- **ML-based** (anomaly detection);
- **Network analysis** (relacionamentos suspeitos);
- **Alerts** + **triagem** + **análise** + **decisão**.

### Padrões atípicos (red flags)
- **Smurfing** (fracionamento abaixo de limites);
- **Structuring** (estruturação para evitar reporting);
- **Layering** (camadas para ocultar origem);
- **Cash-intensive sem justificativa**;
- **Transações com PEPs sem causa econômica**;
- **Jurisdições opacas** (BVI, Caymans, Panama, Vanuatu);
- **Operações intra-grupo** sem propósito;
- **Antitruste pricing manipulation**;
- **Crypto-fiat ramps** sem KYC;
- **Trade-based money laundering** (over/under invoicing).

## Comunicação ao COAF (UIF)

### RTI: Comunicação obrigatória
- **Transações suspeitas** (Lei 9.613 art. 11);
- **Operações em espécie** > R$ 50k (BCB Circular 3.978);
- **Transferências internacionais** > R$ 10k;
- **Não-comunicação**: multa + responsabilização.

### RIF: Relatório de Inteligência Financeira
- COAF compartilha com **Polícia Federal + MPF + RFB + BCB**;
- Base para investigações criminais;
- **STF Tema 990 (RE 1.055.941)**: compartilhamento RIF com MPF é constitucional sem ordem judicial.

### Comunicação negativa (sem ocorrências)
- Anual (algumas obrigadas);
- Demonstra que o cliente está em compliance.

## Sanções

- **OFAC SDN List**: cidadãos americanos + non-US persons via dollar nexus;
- **EU consolidated list**;
- **UN sanctions** (vinculantes, Lei 13.810/19);
- **UK HMT + OFSI**;
- **Designação nacional** (Lei 13.810/2019 + Decreto 9.825/2019);
- **Crypto sanctions** (OFAC SDN com endereços crypto);
- **Sectoral sanctions** (Rússia, Irã, Coreia do Norte, Cuba, Síria, Venezuela);
- **Secondary sanctions** (extraterritoriais, risco para BR);
- **Bloqueio de ativos** (BCB + Lei 13.810).

## Sanções internas

- **Treinamento** anual obrigatório;
- **Política de PLD/FT** + procedimentos;
- **Compliance Officer** designado;
- **Estrutura adequada**;
- **Independent audit** periódica;
- **Reporting ao board**.

## Sanções por descumprimento

| | Conteúdo |
|---|---|
| **Multa** | Até R$ 20M ou 200% do valor (Lei 9.613 art. 12) |
| **Suspensão** | Atividade/cargo |
| **Cassação** | Autorização |
| **Inabilitação** | Pessoa física por 10 anos |
| **Criminal** | Lei 9.613 art. 1 + Lei 12.683 (extinto rol taxativo: qualquer infração penal antecedente) |

## Crime de lavagem

- **Lei 9.613 art. 1** (alterada Lei 12.683/12): ocultar/dissimular natureza, origem, localização, disposição, movimentação ou propriedade de bens, direitos ou valores provenientes de **qualquer infração penal**;
- **Pena**: 3 a 10 anos + multa;
- **Aumento** (art. 1 §4): habitualidade + organização criminosa;
- **Causa de diminuição** (§5): colaboração;
- **Crime autônomo** (não depende de condenação no crime antecedente);
- **Crime permanente** (em alguns tipos, conforme STF).

## Financiamento ao terrorismo (Lei 13.260)

- **Crime autônomo** + sanções similares;
- **GAFI Recomendações 5 + 6**;
- **Lei 13.810/19**: congelamento de ativos por designação ONU sem ordem judicial.

## Crypto + PLD

- **Lei 14.478/2022** (Marco Cripto) + **Decreto 11.563/2023**;
- **VASPs** (Virtual Asset Service Providers) regulados pelo BCB;
- **Resoluções BCB 519, 520 e 521/2025**: marco regulatório das prestadoras de serviços de ativos virtuais (SPSAVs), com exigências de PLD/FT, governança, autorização de funcionamento com capital mínimo e integração ao mercado de câmbio; vigência escalonada a partir de 2026;
- **Sanctions screening** de endereços crypto;
- **Travel rule** (Recomendação 16 FATF), em implementação.

## Erros a evitar

- **Comunicação não-tempestiva** ao COAF (multa + responsabilidade);
- **KYC apenas onboarding** sem refresh periódico;
- **Tiering desatualizado** (alto risco tratado como baixo);
- **UBO até 25%** não verificado em camadas (PEP oculto);
- **PEP family member** não rastreado;
- **Sanctions screening** em apenas uma lista (OFAC sem EU/UN);
- **Crypto wallets** não rastreados;
- **Onboarding digital** sem liveness detection (deepfake);
- **Smurfing** abaixo de R$ 50k não capturado;
- **EDD** sem source of wealth (incompleto);
- **Compliance Officer** sem independência (subordinado a comercial);
- **Treinamento** ausente em frontline (caixa + comercial);
- **Sistema rule-based** sem revisão periódica (falsos positivos + negativos);
- **Comunicação ao COAF** sem detalhamento (RTI inadequado);
- **Cross-border** sem controle de sanctions (sec. sanctions);
- **Correspondent banking** sem EDD (responsabilidade indireta);
- **Trade finance** sem análise de over/under invoicing;
- **Cash-intensive client** sem source of funds;
- **Auto-comunicação** ao cliente (tipping off: crime, Lei 9.613 art. 10 §1);
- **Lei 13.810 sanctions** sem implementação imediata (congelamento);
- **Onboarding** com docs falsificados não detectados (validação biométrica + RFB);
- **PEP screening** apenas BR sem global (BR PEPs no exterior);
- **Não retenção** de documentos por 5+ anos (Lei 9.613 art. 10).
