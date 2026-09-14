---
id: "26277a96-4bed-493c-b428-7782d8c5f46e"
name: "sanctions-screening-ofac-exportacao"
title: "Sanções Internacionais e Controle de Exportação"
category: "materia"
materia: "consultoria"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/consultoria/compliance-integridade/sanctions-screening-ofac-exportacao.md"
triggers:
  - "OFAC"
  - "sanctions"
  - "SDN list"
  - "export control"
  - "ITAR EAR"
  - "dual-use"
  - "Lei 13.810"
  - "sanções ONU"
  - "controle de exportação"
description: "Compliance de sanções internacionais (OFAC, EU, UN, Lei\n13.810/2019, UK HMT, OFSI) e controle de exportação (BR Lei   9.112/95, dual-use, regime ICP, ITAR/EAR USA, EU Regulation\n2021/821), sanctions screening multi-listas, due diligence\npor jurisdição (Rússia, Irã, Coreia do Norte, Cuba, Síria,\nVenezuela), secondary sanctions (extraterritoriais) e crypto\nsanctions (OFAC SDN com endereços crypto)."
---

# Sanções e Controle de Exportação

## Listas restritivas

### Internacionais
- **OFAC SDN List** (USA, Specially Designated Nationals);
- **OFAC SSI** (Sectoral Sanctions Identifications);
- **OFAC NS-PLC + Cuba + outros programas**;
- **OFAC Crypto wallets** (designações específicas);
- **EU Consolidated List** + **EU FSF** (frozen subjects);
- **UN Sanctions** (vinculantes, Lei 13.810/19);
- **UK HMT + OFSI** (Office of Financial Sanctions Implementation);
- **Canada SEMA + AML**;
- **Switzerland SECO**;
- **Australia DFAT**;
- **Japan METI**.

### Setoriais
- **BCBS sanctions**;
- **FATF black/grey list**;
- **EU dual-use catalogue**;
- **Wassenaar Arrangement**;
- **Missile Technology Control Regime (MTCR)**;
- **Nuclear Suppliers Group (NSG)**.

### Brasileiras
- **Lei 13.810/2019 + Decreto 9.825/2019**: implementam sanções ONU + bloqueio de ativos + designação nacional;
- **Resoluções do CSNU** e designações de seus comitês de sanções, de cumprimento imediato;
- **COAF + RFB + BCB**: aplicam congelamento;
- **MJSP** + CGAAR (autoridade central).

## Programas de sanções (USA, OFAC)

### Comprehensive sanctions (full embargo)
- **Cuba** (parcial);
- **Irã**;
- **Síria**;
- **Coreia do Norte**;
- **Crimeia + Donetsk + Luhansk + Zaporijia + Kherson** (Rússia/Ucrânia).

### Selective sanctions
- **Rússia** (sectoral + entity-list);
- **Venezuela**;
- **Mianmar**;
- **Belarus**;
- **Líbia**;
- **Sudão do Sul**;
- **Iemen**;
- **Zimbabwe**;
- **Conta gota** em outros.

### Specific programas
- **Counter-terrorism**;
- **Counter-narcotics** (Kingpin Act);
- **Cyber-related**;
- **Human rights** (Magnitsky Act + Global Magnitsky);
- **Election interference**;
- **Non-proliferation**;
- **Transnational criminal organizations**.

## Secondary sanctions (extraterritoriais)

- **Não-US persons** podem ser sancionados por transacionar com SDN;
- **Risco para empresas BR** que operem em dólar OU tenham nexus USA (empregado, filial, vendor);
- **Iran Sanctions Act + JCPOA snapback**;
- **CAATSA (Rússia)**;
- **Hong Kong Autonomy Act**;
- **Foreign Direct Product Rule (FDPR)**: bens fabricados com tecnologia USA podem ser controlados mesmo fabricados fora.

## 50% rule (OFAC)

- **Entidade detida em ≥ 50%** por SDN é **bloqueada** automaticamente (mesmo sem listagem expressa);
- **Controle** sem 50%: caso a caso;
- **Sub-50%** + **influência relevante**: análise EDD;
- **Cascade**: subsidiárias de SDN também bloqueadas.

## Lei 13.810/2019

- **Bloqueio imediato** de ativos de pessoas designadas pelo CSNU (Conselho de Segurança da ONU);
- **Sem ordem judicial** prévia (indisponibilidade administrativa, com posterior comunicação às autoridades);
- **Comunicação** ao MJSP (autoridade central);
- **Defesa**: pedido de delisting via canais ONU + judiciais BR;
- **Sanção**: multa + suspensão + autorização cassada (operadoras).

## Sanctions screening: operacional

### Quando
- **Onboarding** de cliente/fornecedor/parceiro;
- **Transação** específica (pré-pagamento);
- **Continuous monitoring** (diário, em real time se possível);
- **Re-screening** em mudança de UBO/diretoria;
- **Em DD de M&A**;
- **Cross-border payments**.

### Como
- **Match exato** de nomes;
- **Fuzzy match** (variações de transliteração, typos);
- **Aliases** (AKA);
- **DOB + nacionalidade + endereço**;
- **Match por endereço** (sanctions on locations);
- **Vessel/aircraft** screening;
- **Crypto wallet** screening;
- **Tools**: World-Check, Refinitiv, Dow Jones, ICIJ, internas.

### Falsos positivos
- Padronização de nomes (transliterações);
- Validação manual em hit;
- Mantém log para defesa em fiscalização;
- Documentação de decisão (cleared/rejected).

## Em ocorrência de hit

1. **Suspender transação** imediatamente;
2. **Validar** o hit (true match × false positive);
3. **Confirmar** com listas oficiais primárias;
4. **Compliance review** + decisão;
5. **Bloquear** ativos (Lei 13.810 + OFAC blocking + EU/UN);
6. **Reportar** ao MJSP/COAF/BCB conforme aplicável;
7. **OFAC reporting** (within 10 days for blocking);
8. **Não tipping off** (cliente não pode ser avisado de investigação);
9. **Cooperar** com authorities;
10. **Solicitar licença** (OFAC license) se transação necessária por razões humanitárias/contratuais.

## Controle de exportação (BR)

- **Lei 9.112/95**: regime de exportação de bens sensíveis;
- **Regulamentação MD + MRE + MCTI + MDIC**;
- **CIBES** (Comissão Interministerial de Bens e Serviços Sensíveis);
- **Bens de uso dual** (civil/militar);
- **Tecnologias sensíveis**: nuclear, química, biológica, mísseis;
- **Pré-aprovação** + **licença de exportação**;
- **Penalidades**: multa + apreensão + criminal (Lei 9.112/95 + Lei 8.137).

## ITAR (USA, defense)

- **International Traffic in Arms Regulations** (DOS);
- **USML** (US Munitions List);
- **End-user certification**;
- **Re-export** controlado;
- **Brokers** registrados;
- **Sanções altas** + criminal.

## EAR (USA, dual-use)

- **Export Administration Regulations** (DOC/BIS);
- **CCL** (Commerce Control List);
- **EAR99** (default);
- **License determination** (ECCN);
- **Entity List + MEU + UVL** (restrições adicionais);
- **De minimis rule**: bens com componentes USA acima de % trigger EAR;
- **FDPR**: bens estrangeiros feitos com software USA podem trigger;
- **Deemed export**: transferência de tecnologia a non-US person dentro dos EUA = exportação.

## EU dual-use (Regulation 2021/821)

- **Annex I** (lista de itens);
- **General Export Authorizations** (GEA);
- **Individual licenses**;
- **Catch-all clause** (item não listado mas risco trigger).

## Cláusulas contratuais

- **Sanctions compliance covenant** mútuo;
- **Right to suspend** em sanções subsequentes;
- **Right to terminate** + indenidade;
- **Audit rights**;
- **Self-disclosure** obrigatório;
- **End-use certificates** em bens de exportação;
- **Re-export restrictions**;
- **Sanctions exclusion** em insurance/coverage.

## Crypto

- **OFAC SDN com endereços crypto**: rastreamento blockchain;
- **Chainalysis + Elliptic + TRM**: tools de screening;
- **Travel rule** (Recomendação 16 FATF): VASPs trocam dados de remetente/beneficiário em transferências > USD 1k;
- **Resoluções BCB 519-521/2025**: prestadoras de serviços de ativos virtuais (SPSAVs) sujeitas a PLD/FT + sanções;
- **Mixers + tumblers** + **DeFi**: alto risco;
- **Stablecoins** (USDT, USDC): emissoras congelam wallets sancionadas.

## Erros a evitar

- **Screening** apenas em uma lista (OFAC sem EU/UN/UK);
- **Fuzzy match** com threshold baixo (false negatives);
- **50% rule** ignorado em UBO chain (cascade missed);
- **Continuous screening** ausente (após onboarding, novo SDN não detectado);
- **Tipping off** ao cliente (crime, Lei 9.613);
- **Bloqueio tardio** (Lei 13.810 exige imediato);
- **OFAC reporting** > 10 dias (multa);
- **Secondary sanctions** ignoradas (BR sem nexus USA aparente, mas dólar/dual-use trigger);
- **Crypto sanctions** sem screening de endereços;
- **Re-export** sem controle (ITAR/EAR violation);
- **De minimis EAR** sem cálculo (FDPR risk);
- **Deemed export** sem assess (engenheiro estrangeiro acessando tecnologia USA na BR sede);
- **End-user certification** ausente;
- **Catch-all clause** EU dual-use ignorada;
- **Lei 9.112/95 BR** sem licença em bens sensíveis (criminal);
- **CIBES** não consultado em itens dual-use;
- **DPA com vendor** sem cláusula de re-export;
- **Sanctions clause** unilateral (apenas a favor de uma parte);
- **OFAC license** não solicitada quando necessária;
- **Snap-back** (Iran JCPOA) não monitorado (mudança regulatória rápida);
- **Subsidiária local** em jurisdição sancionada sem ringfence (parent USA exposed);
- **Em M&A**: target com exposure a SDN não mapeado.
