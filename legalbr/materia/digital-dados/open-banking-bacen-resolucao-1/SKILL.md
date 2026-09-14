---
id: "41e40de0-fd08-4b54-9315-4769df8a2350"
name: "open-banking-bacen-resolucao-1"
title: "Open Finance (Open Banking BR): BACEN Resolução Conjunta 1/2020"
category: "materia"
materia: "digital-dados"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/digital-dados/open-banking-bacen-resolucao-1.md"
triggers:
  - "open finance"
  - "open banking"
  - "BACEN Resolução Conjunta 1"
  - "compartilhamento dados financeiros"
  - "API financeira"
  - "PISP iniciador de pagamento"
  - "DICT contas transacionais"
  - "iniciação de pagamento"
description: "Open Finance (renomeado de Open Banking, 2021): sistema de\ncompartilhamento padronizado de dados e serviços financeiros entre\ninstituições autorizadas pelo BACEN, mediante **consentimento\nexpresso e específico** do cliente. Marco: Resolução Conjunta\nBACEN+CMN nº 1/2020 + Reso BCB 32/2020. **4 fases**: (1) dados\nabertos das instituições, fev/2021; (2) dados cadastrais + extratos\n , ago/2021; (3) iniciação de pagamentos + serviços de proposta de\ncrédito, out/2021; (4) ampliação a câmbio, investimentos, seguros,\nprevidência e capitalização, dez/2021+. Consentimento: máx 12\nmeses + revogável. APIs padronizadas + autenticação reforçada.\nAplicação concomitante com LGPD + ANPD. CDC aplica-se."
---

# Open Finance Brasil

## Marco legal

- **Resolução Conjunta BACEN+CMN nº 1/2020** (04/05/2020), implementação;
- **Resolução BCB nº 32/2020** + atualizações;
- **Resolução BCB nº 109/2021** (Open Finance II);
- **Resolução BCB nº 357/2023** (facilitação compartilhamento);
- **LGPD** (Lei 13.709/2018), aplicação concomitante;
- **Lei 4.595/64** (SFN);
- **Lei 12.865/13** + LC 105/01 (sigilo bancário);
- **Lei 12.965** (Marco Civil, segurança da informação);
- Estrutura **OPIN / Open Finance Brasil** (governança privada).

## Renomeação

| Antes | Depois |
|---|---|
| **Open Banking** (2020) | **Open Finance** (set/2021) |
| Foco bancos | Foco amplo: SF + investimentos + seguros + câmbio |

## Conceito (Reso Conjunta 1)

> "Open Finance é o sistema que permite o **compartilhamento padronizado de dados e serviços financeiros** entre instituições autorizadas pelo BACEN, mediante consentimento expresso do cliente."

| | Conteúdo |
|---|---|
| **Princípio** | **Cliente como dono** dos seus dados |
| **Padrão** | API + protocolo seguro |
| **Voluntário** | Cliente escolhe compartilhar |
| **Reversível** | Consentimento revogável |

## 4 Fases de implementação

### Fase 1: fev/2021

| | Conteúdo |
|---|---|
| **Foco** | Dados **abertos** das instituições (canais, produtos, serviços) |
| **Sem dados pessoais** | Não exige consentimento |
| **Aplicação** | Disponibilidade pública via APIs |

### Fase 2: ago/2021

| | Conteúdo |
|---|---|
| **Dados cadastrais** | Nome, CPF, endereço |
| **Extratos** | Conta corrente + cartão + crédito |
| **Operações** | Histórico de movimentações |
| **Consentimento expresso** | Necessário |

### Fase 3: out/2021

| | Conteúdo |
|---|---|
| **Iniciação de pagamento (PISP)** | Pagamento direto da conta para terceiros |
| **Encaminhamento de propostas de operações de crédito** | "Marketplace" de crédito |
| **Aplicação** | Pix + TED + transferências |

### Fase 4: dez/2021+

| | Conteúdo |
|---|---|
| **Câmbio** | Operações cambiais |
| **Investimentos** | Aplicações financeiras |
| **Seguros** | Apólices |
| **Previdência aberta** | Planos |
| **Capitalização** | Títulos |

## Tipos de participação

| | Conteúdo |
|---|---|
| **Obrigatória** | Instituições S1 + S2 (grandes bancos) |
| **Voluntária** | Demais instituições |
| **Iniciadores de pagamento** | Autorização específica |
| **Receptores de dados** | Devem ser participantes autorizados |

## Consentimento (Reso Conjunta 1 + LGPD)

| | Conteúdo |
|---|---|
| **Forma** | **Livre + informada + prévia + inequívoca + por meio eletrônico** |
| **Finalidade** | Determinada e específica |
| **Prazo máximo** | **12 meses** |
| **Revogável** | A qualquer tempo + retroatividade limitada |
| **Renovação** | Necessária após 12 meses |
| **Granular** | Por escopo + finalidade |

## Procedimento de compartilhamento

| Etapa | Conteúdo |
|---|---|
| 1. **Solicitação** | Cliente solicita via instituição receptora |
| 2. **Autenticação** | Multifator |
| 3. **Direcionamento** | Para instituição detentora |
| 4. **Consentimento expresso** | Lavrado |
| 5. **Compartilhamento** | API → instituição receptora |
| 6. **Acompanhamento** | Cliente vê o que foi compartilhado |
| 7. **Revogação** | A qualquer tempo |

## APIs + padronização

| | Conteúdo |
|---|---|
| **OPIN** | Organização que gere o Open Finance |
| **Padrão técnico** | OAuth 2 + FAPI (Financial Grade API) |
| **Especificações** | OpenAPI 3.0 |
| **Performance** | SLAs definidos |
| **Sandbox** | Para testes |
| **DICT** | Diretório de Identificadores de Contas Transacionais (infraestrutura do Pix) |

## Estrutura de governança

| | Conteúdo |
|---|---|
| **BACEN** | Supervisor + autoridade competente |
| **OPIN** | Organização (associação privada) |
| **Comitês** | Estratégico + técnico + segurança + experiência cliente |
| **Conselho deliberativo** | Decisões estratégicas |

## Segurança

| | Conteúdo |
|---|---|
| **MFA** | Autenticação multifator |
| **Certificados digitais** | ICP-Brasil |
| **Criptografia** | TLS 1.2+ |
| **API key + secret** | Por instituição |
| **Auditoria** | Trilhas + monitoramento |
| **DICT** | Diretório central |

## LGPD + Open Finance

| | Conteúdo |
|---|---|
| **Dado pessoal financeiro** | Sensível em parte |
| **Base legal** | Consentimento (LGPD 7 I) |
| **Direitos do titular** | Plenamente aplicáveis |
| **DPO/Encarregado** | Necessário |
| **Vazamento** | Notificação ANPD + cliente |
| **Princípio da finalidade** | Reforçado |

## Sanções por descumprimento

| | Conteúdo |
|---|---|
| **BACEN** | Multa + suspensão + cassação |
| **ANPD** | Multa LGPD (até 2% receita ou R$ 50M) |
| **CDC** | Aplicação concomitante |
| **Civil** | Responsabilidade por dano material/moral |

## CDC + Open Finance

| | Conteúdo |
|---|---|
| **Relação de consumo** | Aplicável |
| **Informação clara** | CDC 6 III |
| **Cláusulas abusivas** | Anuláveis |
| **Inversão do ônus** | CDC 6 VIII |
| **Senacon + Procons** | Atuam |

## DICT e Pix integrados

| | Conteúdo |
|---|---|
| **DICT** | Diretório de Identificadores de Contas Transacionais |
| **Pix** | Sistema de pagamento instantâneo |
| **Iniciação via Open Finance** | Combina Pix + autenticação Open |
| **Fraudes** | Atenção (MED, Mecanismo Especial de Devolução; Reso BCB 103/2021) |
| **Segurança 2025** | Res. BCB 496/497/498 (set/2025): limite de **R$ 15 mil** por transação Pix/TED para instituições de pagamento não autorizadas e participantes conectados via PSTI; credenciamento de PSTI |

## Comparativo internacional

| | Conteúdo |
|---|---|
| **PSD2 (UE)** | Modelo inspirador |
| **Brasil: Open Finance** | Mais amplo (não só pagamentos) |
| **Open Banking UK** | Pioneiro |
| **Austrália CDR** | Consumer Data Right (mais amplo) |
| **EUA** | CFPB Rule 1033: em desenvolvimento |

## Open Insurance: Susep

| | Conteúdo |
|---|---|
| **CNSP + SUSEP** | Regulam Open Insurance |
| **Fases** | Implementação progressiva 2022+ |
| **Foco** | Seguros + previdência aberta + capitalização |
| **Sincronia** | Com Open Finance |

## Aplicações práticas

| | Conteúdo |
|---|---|
| **PFM** (Personal Finance Management) | Apps de gerenciamento |
| **Crédito personalizado** | Análise por score próprio |
| **Pagamento direto** | PISP: alternativa ao cartão |
| **Investimentos** | Cross-instituição |
| **Câmbio** | Comparação de taxas |
| **Cobrança automatizada** | B2B |

## Riscos + atenção

| | Conteúdo |
|---|---|
| **Fraude** | Engenharia social + phishing |
| **Vazamento** | Falhas em receptores |
| **Cancelamento difícil** | Por designs ruins |
| **Concentração** | Risco sistêmico |
| **Cyber attacks** | Em massa |
| **Privacy** | Falhas no consentimento |

## STJ + tendências

| | Conteúdo |
|---|---|
| Casos ainda escassos | Em formação |
| **MED + Pix** | Casos crescentes (devolução) |
| **Negativa indevida** | Aplicação CDC |
| **MED** | Não se confunde com chargeback de cartão (mecanismos distintos) |

## Erros a evitar

- Compartilhar dados **sem consentimento** específico (Reso Conjunta 1 + LGPD);
- Aceitar consentimento **superior a 12 meses** (Reso Conjunta 1, máximo);
- Esquecer **revogabilidade** + facilidade de cancelamento;
- Aplicar Open Finance a **dados não cobertos** (categorias específicas);
- Não aplicar **LGPD** concomitantemente (ANPD + BACEN);
- Esquecer **CDC** (relação de consumo);
- Atuar como **PISP** sem autorização BACEN;
- Não aplicar **autenticação multifator**;
- Esquecer **fases** + escopo (cada fase tem escopo próprio);
- Confundir **Open Finance** (geral) com **Open Insurance** (SUSEP);
- Tratar **dados abertos** (fase 1) como pessoais, não são;
- Aplicar **PSD2 UE** diretamente: regime distinto.
