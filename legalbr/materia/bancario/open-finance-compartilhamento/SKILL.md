---
id: "6354646f-dcbd-40c6-970d-f89e7b3f5fce"
name: "open-finance-compartilhamento"
title: "Open Finance: Compartilhamento de Dados e Serviços (Res. Conj. CMN/BCB 1/2020)"
category: "materia"
materia: "bancario"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/bancario/open-finance-compartilhamento.md"
triggers:
  - "Open Finance"
  - "Open Banking"
  - "Resolução Conjunta 1/2020"
  - "Res. BCB 32/2020"
  - "Instrução Normativa BCB 117"
  - "compartilhamento de dados bancários"
  - "iniciador de pagamento"
  - "ITP iniciador de transação"
  - "LGPD bancos"
  - "portabilidade de dados bancários"
  - "sandbox regulatório"
description: "Open Finance: regulado pela Res. Conj. CMN/BCB 1/2020 + Res. BCB\n32/2020 (governança) + Instrução Normativa BCB 117/2021 (escopo);\ncompartilhamento de dados em 4 fases (cadastrais, transacionais,\nprodutos e serviços, incluindo o ITP, iniciador de transação de\npagamento); consentimento granular do cliente por até 12 meses;\nLGPD aplicável (bases legais específicas e consentimento\nqualificado para dados sensíveis); responsabilidade solidária das\nIFs participantes."
---

# Open Finance: Compartilhamento de Dados e Serviços

## Base normativa

| Norma | Conteúdo |
|---|---|
| **Res. Conj. CMN/BCB 1/2020** | Marco regulatório do Open Finance |
| **Res. BCB 32/2020** | Estrutura de governança (Secretariado, Conselho Deliberativo, Grupos Técnicos) |
| **IN BCB 117/2021** | Escopo dos dados e serviços por fase |
| **Res. CMN 4.893/21** | Política de segurança cibernética e nuvem (revogou a Res. 4.658/18) |
| **LGPD (Lei 13.709/18)** | Base legal específica: art. 7 V (execução de contrato) + art. 11 II "a" (consentimento qualificado para dados sensíveis) |
| **Marco Civil da Internet (Lei 12.965/14)** | Registro de conexão e log de aplicação |
| **CDC arts. 4, 6, 14, 43, 73** | Direitos do consumidor: informação, segurança, base de dados |
| Sandbox regulatório financeiro | Ambiente regulatório experimental do SFN (LC 182/2021 e regulamentação do CMN/BCB; conferir a resolução vigente) |

## Conceito

| | Conteúdo |
|---|---|
| Definição | Padronização e abertura, por API, do **compartilhamento de dados e serviços** de instituições financeiras autorizadas pelo BCB |
| Beneficiário | **Cliente** (titular dos dados) decide o quê, com quem e por quanto tempo compartilhar |
| Participantes | IFs e instituições de pagamento autorizadas + ITPs (iniciadores) |
| Princípio | "Os dados são do cliente, não do banco": efetivação do art. 18 LGPD |
| Modelo | Reciprocidade: quem recebe dados deve compartilhar (4 maiores conglomerados são obrigatórios; demais opcional) |

## Fases de implementação

| Fase | Conteúdo | Data |
|---|---|---|
| **1** | Dados públicos das IFs (canais, produtos, condições gerais) | 01.02.2021 |
| **2** | **Dados cadastrais e transacionais** do cliente (saldo, extrato, faturas, conta-corrente, cartão, crédito) | 13.08.2021 → 15.10.2021 |
| **3** | **Iniciação de pagamentos** (ITP) e propostas de crédito | 29.10.2021 → 15.06.2022 |
| **4** | **Demais serviços**: investimentos, seguros, câmbio, previdência, conta-salário | 15.12.2021 → 2023 |
| Próximas evoluções | Open Insurance, Open Capital, Open Health: alinhamento com CVM/Susep/ANS |

## Consentimento

| Requisito | Conteúdo |
|---|---|
| **Granularidade** | Cliente seleciona dados específicos (não há "tudo ou nada") |
| **Finalidade** | Determinada, expressa e informada (art. 6 LGPD) |
| **Prazo máximo** | **12 meses** (renovável); ITP: single use ou recorrente até 12 meses |
| **Revogação** | A qualquer tempo, pelos canais da IF transmissora E receptora |
| **Autenticação** | Forte (2FA, biometria) com redirecionamento do receptor para o transmissor |
| **Registro** | Audit log obrigatório (IN BCB 117/2021) |
| **Linguagem** | Clara, em português, livre de tecnicismos (CDC 6 III + 31) |

## Iniciador de Transação de Pagamento (ITP)

| | Conteúdo |
|---|---|
| Definição | Instituição autorizada pelo BCB que inicia pagamento (Pix, TED, transferência) sem deter conta do cliente |
| Habilitação | Autorização específica pelo BCB (Circ. BCB 4.015/20) + adesão ao Open Finance |
| Responsabilidade | **Solidária** com a IF detentora da conta por falhas de iniciação (Res. Conj. 1/2020 art. 12) |
| Modelo de receita | Tarifa do estabelecimento (não do cliente) |
| Restrições | Não pode reter recursos do cliente; pagamento entra direto na conta destino |

## Responsabilidade entre participantes

| Hipótese | Responsabilidade |
|---|---|
| Vazamento na IF **transmissora** | Transmissora responde (LGPD 42, CDC 14) |
| Vazamento na IF **receptora** | Receptora responde + transmissora subsidiariamente se houve falha de autenticação |
| Falha técnica da API | IF detentora do dado responde, com direito de regresso |
| Uso de dados além do escopo do consentimento | Receptora: caracteriza desvio de finalidade (LGPD 6 I) |
| ITP: pagamento errado | Solidária ITP + IF detentora da conta |
| Cliente lesado | **Súm. 479 STJ** + CDC 14: responsabilidade objetiva |

## LGPD aplicada ao Open Finance

| | Conteúdo |
|---|---|
| Base legal | **Art. 7 V LGPD** (execução de contrato) E **art. 7 X** (legítimo interesse), combinada com **consentimento específico** para dados não vinculados ao contrato |
| Dados sensíveis | Tratamento exige **consentimento qualificado** (art. 11 II "a"): biometria, saúde, religião |
| Transferência internacional | Apenas para países adequados ou com garantias (art. 33 LGPD) |
| ANPD | Competência **concorrente** com BCB (Termo de Cooperação 2021): BCB regula, ANPD fiscaliza incidentes |
| DPO | Encarregado obrigatório (art. 41 LGPD) + reporte a BCB e ANPD em incidentes graves |
| Direitos do titular | Acesso, correção, eliminação, portabilidade (art. 18 LGPD), exercitáveis via canal Open Finance |

## Segurança técnica

| Item | Conteúdo |
|---|---|
| API | Padrão **FAPI** (Financial-grade API) + OAuth 2.0 + OpenID Connect |
| Diretório | Cadastro centralizado de participantes mantido pela estrutura de governança do Open Finance |
| Certificação | mTLS + assinatura digital com certificado ICP-Brasil ou equivalente |
| Mecanismo de descoberta | Diretório central: clientes acham IFs e serviços disponíveis |
| Incidentes | Comunicação **tempestiva** ao BCB (Res. CMN 4.893 e regulamentação do BCB); à ANPD em **3 dias úteis** (Regulamento de Comunicação de Incidentes, Res. CD/ANPD 15/2024) |

## Erros a evitar

- Tratar Open Finance como **portabilidade simples**: é arquitetura permanente, não evento único;
- Coletar consentimento **genérico ou em massa**: viola granularidade (LGPD 6 I);
- Ultrapassar **12 meses** sem renovação: consentimento extinto;
- Esquecer **revogação imediata** pelo cliente em ambos os lados: risco de multa BCB + ANPD;
- Confundir **ITP** com **PISP/PSP estrangeiro**: regime brasileiro próprio;
- Atribuir vazamento à **receptora** quando a falha de autenticação ocorreu na **transmissora** (responsabilidade conjunta, mas regredível);
- Ignorar **autenticação forte** (2FA + redirecionamento): descumprimento da Res. BCB 32/2020;
- Tratar **dados públicos da Fase 1** como dados pessoais: não exigem consentimento;
- Não registrar **audit log**: pressuposto fiscalizatório (IN BCB 117/21);
- Permitir transferência internacional sem **garantias da LGPD** (art. 33);
- Coletar dados sensíveis (saúde, biometria) sob **base legal de contrato**: exige consentimento qualificado (LGPD 11 II "a");
- Tratar incidentes do Open Finance **apenas pela LGPD**: há reporte cumulativo ao BCB.
