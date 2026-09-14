---
id: "fed88a8f-a771-4fe0-9cfe-ae9fe95f219f"
name: "contrato-saas"
title: "Contrato SaaS (Software as a Service B2B)"
category: "materia"
materia: "contratos"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/contratos/contrato-saas.md"
triggers:
  - "SaaS"
  - "software as a service"
  - "licença de uso de software"
  - "software em nuvem"
  - "assinatura de software"
  - "service level agreement"
  - "uptime"
  - "Lei 9.609"
  - "Lei 12.965"
  - "LGPD operador"
  - "dados do cliente"
description: "SaaS B2B: licença Lei 9.609/98 + prestação contínua; SLA com\nuptime e créditos; dados do cliente; operador LGPD; suporte;\nMarco Civil (Lei 12.965/14); limitação de responsabilidade."
---

# Contrato SaaS

## Base legal

| Diploma | Conteúdo |
|---|---|
| **Lei 9.609/98** | Software: proteção e uso |
| Lei 9.610/98 | Direito autoral (subsidiário) |
| **Lei 12.965/14** | Marco Civil: guarda, neutralidade, jurisdição |
| **LGPD (13.709/18)** | Proteção de dados: fornecedor como **operador** (ou controlador, em algumas hipóteses) |
| **Lei 13.709 art. 39** | Operador trata segundo as instruções do controlador (fundamento do DPA) |
| CC 421-A | B2B paritário |
| Res. ANPD 15/2024 | Comunicação de incidentes |

## Natureza jurídica

| Aspecto | Conteúdo |
|---|---|
| Qualificação | **Híbrido**: licença de uso (Lei 9.609 art. 9) + prestação contínua de serviço |
| **Não há cessão** | Cliente recebe direito de **uso**, não cópia |
| Tributação | **ISS** (LC 116/03 item 1.05): STF ADIs 1.945 + 5.659 |
| EC 132/23 | Migração para IBS/CBS (gradual 2026-2033) |

## Estrutura mínima

| Bloco | Conteúdo |
|---|---|
| Definições | Serviço, Usuário, Conta, Conteúdo do Cliente |
| Licença / acesso | Não exclusiva, intransferível, revogável |
| **SLA** | Uptime, suporte, tempo de resposta, créditos |
| Preço / Tarifação | Modelo (per-seat, consumo, flat) + reajuste |
| Dados do Cliente | **Propriedade do cliente** + uso restrito |
| LGPD | Papéis + DPA anexo |
| **Encerramento + portabilidade** | Exportação em formato estruturado |
| Limitação de responsabilidade | Cap |
| Foro / arbitragem | Conforme porte |

## Cláusulas obrigatórias

| # | Cláusula | Função |
|---|---|---|
| 1 | **Licença de uso** não exclusiva | Lei 9.609 art. 9 |
| 2 | **Restrições** (reverse engineering, descompilação) | Lei 9.609 art. 6: exceções restritas |
| 3 | **Propriedade do código** mantida com o fornecedor | Reservation of rights |
| 4 | **Conta de usuário** + responsabilidade por credenciais | Indenidade |
| 5 | **SLA com uptime + créditos** | Métrica objetiva |
| 6 | Suporte por nível | P1/P2/P3 com SLAs distintos |
| 7 | **Manutenção e janelas** | Pré-aviso obrigatório |
| 8 | **Dados do cliente são do cliente** | Cláusula essencial |
| 9 | LGPD + **DPA** anexo | Lei 13.709 art. 39 |
| 10 | Confidencialidade recíproca | CC 422 |
| 11 | **Portabilidade na saída** | Em formato estruturado, 30-90 dias |
| 12 | Limitação de responsabilidade | Cap em 12 meses de fees |
| 13 | Indenidade por violação de PI por uso indevido | |
| 14 | Auditoria | Direito do fornecedor a fiscalizar uso |

## SLA: métricas essenciais

| Métrica | Definição típica |
|---|---|
| **Uptime** | 99,5% a 99,99% (excluindo janelas planejadas) |
| Cálculo | Mensal: minutos disponíveis / minutos totais |
| **Exclusões** | Manutenção planejada, força maior, falha do cliente, ataques DDoS volumétricos |
| **Créditos** | Escalonados: 99% = 5%, 95% = 25%, < 90% = rescisão |
| Suporte P1 (down) | Resposta < 1h + restauração < 4h |
| Suporte P2 (degradação) | Resposta < 4h |
| Suporte P3 (dúvida) | Resposta < 1 dia útil |

> **Crédito de SLA** = remédio **exclusivo** salvo má-fé / dolo / culpa grave.

## Dados do cliente

| Item | Regra |
|---|---|
| **Propriedade** | Permanecem do cliente: fornecedor é **mero custodiante / operador** |
| Uso | Apenas para prestar o serviço (não para treinar IA / vender) |
| **Anonimização para analytics** | Permitida apenas se contratualizado e LGPD-aderente |
| **Backup** | Frequência e retenção definidos |
| **Devolução / portabilidade** | Formato estruturado (CSV, JSON, SQL dump): 30-90 dias |
| **Destruição** | Certidão escrita após período de retenção |

## LGPD: papéis

| Cenário | Papel típico do SaaS |
|---|---|
| SaaS multi-tenant padrão | **Operador** (segue instruções do cliente) |
| SaaS com analytics próprio para terceiros | **Controlador** sobre esses dados |
| Marketing/anúncios | **Co-controle** ou controlador independente |

> DPA **obrigatório** sempre que operador. Anexar e cobrir: finalidades, instruções, subprocessadores, transferência internacional, incidentes, devolução.

## Marco Civil (Lei 12.965/14)

| Item | Aplicação |
|---|---|
| Art. 7 X | Exclusão definitiva de dados ao término |
| Art. 11 | Lei brasileira se houver coleta no Brasil |
| Art. 15 | Guarda de registros de aplicação por **6 meses** (se aplicação de internet) |
| Art. 19 | Responsabilidade por conteúdo de terceiros: **STF Tema 987** declarou a **inconstitucionalidade parcial e progressiva** do art. 19; enquanto não houver nova lei, provedores respondem nos termos do **art. 21 do MCI**, de forma **solidária** com o autor do conteúdo, salvo dúvida razoável quanto à ilicitude após diligência qualificada (ED julgados em 17/06/2026, com trânsito em julgado); ordem judicial prévia segue exigível para crimes/ilícitos contra a honra, e-mail, reuniões fechadas e mensageria sob sigilo; anúncios pagos e disseminação artificial inorgânica atraem **presunção relativa de culpa**, independentemente de notificação; conteúdo já declarado ofensivo por decisão judicial é removível por notificação judicial ou extrajudicial; **sem responsabilidade objetiva**; efeitos ex nunc desde 05/08/2025 |

## Cláusulas acidentais úteis

| Cláusula | Função |
|---|---|
| **Force majeure** | CC 393 + força maior digital (ataques, falhas de cloud upstream) |
| **Sub-processadores** | Lista + direito de oposição |
| **Audit right** do cliente | Sobre LGPD/segurança: limitado a 1x ano |
| **Beta/preview features** | Sem SLA, sem garantia |
| **AI features** | Direitos sobre **outputs**, política de não-treinar com dados do cliente |
| **Reps de segurança** | ISO 27001, SOC 2, NIST |
| **Insurance** | Cyber + E&O |
| **Multi-cloud / DR** | Plano de continuidade |

## Encerramento: fluxo crítico

| Fase | Conteúdo |
|---|---|
| Notificação | 30-90 dias |
| **Período de transição** | Acesso somente leitura |
| **Portabilidade** | Exportação em formato estruturado |
| **Retenção** | 30-90 dias após encerramento para resgate |
| **Destruição** | Com certidão escrita |
| Subprocessadores | Notificados |

## Roteiro de redação

1. Modelo de **tarifação** (per-seat, consumo, flat) + reajuste;
2. **SLA**: uptime + suporte + créditos + exclusivo;
3. **Dados do cliente são do cliente** + restrição de uso;
4. **DPA** anexo (LGPD);
5. **Subprocessadores** listados + oposição;
6. **Portabilidade** em saída;
7. **Limitação de responsabilidade** (cap em 12 meses);
8. Exceções ao cap (LGPD, PI, dolo, indenidade);
9. **AI features**: política de não-treinar;
10. Foro / arbitragem conforme porte.

## Erros a evitar

- Tratar como **compra de licença permanente** (é assinatura);
- SLA **sem exclusões** (uptime de 99,9% inalcançável);
- **Crédito de SLA** sem limite: vira sangria mensal;
- Não regular **propriedade dos dados** (presunção é do cliente, mas explicitar);
- Esquecer **DPA** quando operador (LGPD art. 39: tratamento segundo as instruções do controlador);
- Permitir **treinar IA** com dados do cliente sem base legal explícita;
- Portabilidade em formato **proprietário** (vendor lock-in abusivo);
- Limitação de responsabilidade **inferior aos fees** anuais (desbalanceado);
- Não excluir **LGPD/PI/dolo** do cap;
- **Manutenção** sem janela definida;
- Subprocessadores **sem lista** ou direito de oposição;
- Esquecer **lei brasileira** se houver coleta no Brasil (Marco Civil art. 11);
- Tratar SaaS B2B como **relação de consumo** (CC 421-A: paritário).
