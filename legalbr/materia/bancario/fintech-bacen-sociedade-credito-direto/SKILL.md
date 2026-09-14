---
id: "52694bc3-4b4e-47f2-a16b-c48563c40451"
name: "fintech-bacen-sociedade-credito-direto"
title: "Fintechs e Regulação BACEN (SCD, SEP, IP, Sandbox)"
category: "materia"
materia: "bancario"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/bancario/fintech-bacen-sociedade-credito-direto.md"
triggers:
  - "fintech"
  - "SCD"
  - "sociedade de crédito direto"
  - "sociedade de empréstimo entre pessoas"
  - "instituição de pagamento"
  - "PagSeguro"
  - "sandbox BACEN"
  - "Res. CMN 4.656"
  - "arranjo de pagamento"
  - "banking as a service"
description: "Regulação de fintechs no BACEN: SCD (Res. CMN 4.656/18), SEP (Res.\nCMN 4.656/18, consolidada pela Res. CMN 5.050/22), IP (Lei 12.865/13\n+ Res. BCB 80/21), ESC (LC 167/2019), Open Finance (Res. Conjunta\nCMN/BCB 1/20), sandbox regulatório do SFN (LC 182/2021 + regulamentação\nCMN/BCB), PIX (Res. BCB 1/20), banking as a service e bigtech."
---

# Fintechs e Regulação BACEN

## Mapa regulatório

| Modelo | Regime | Marco |
|---|---|---|
| **Banco múltiplo** | Banco | Lei 4.595/64 + Res. CMN 4.595 |
| **Banco digital** | Banco com canais digitais | Idem |
| **SCD (Sociedade de Crédito Direto)** | Crédito por conta própria (sem captação) | Res. CMN 4.656/18, consolidada pela Res. CMN 5.050/22 |
| **SEP (Sociedade de Empréstimo entre Pessoas)** | P2P lending | Res. CMN 4.656/18 |
| **IP (Instituição de Pagamento)** | Conta de pagamento + adquirência | Lei 12.865/13 + Res. BCB 80/21 |
| **Cooperativa de crédito** | Cooperativismo | LC 130/09 |
| **SCFI** (Sociedade de Crédito, Financiamento e Investimento) | Crédito + funding | Res. CMN 4.595 |
| **Corretora + DTVM** | Mercado de capitais | Res. CMN 1.655 |
| **ESC (Empresa Simples de Crédito)** | Crédito com capital próprio a MEI, microempresas e EPPs, em âmbito municipal | LC 167/2019 |
| **Bigtech (Apple/Google Pay)** | Sem regime específico (atuação como IP via parceiro) | RCVM/BCB ad hoc |

## Sociedade de Crédito Direto (SCD)

### Características (Res. CMN 4.656/18)
- **Concede crédito** com recursos **próprios**;
- **Não capta** poupança popular (regra geral);
- Pode captar via **emissão de letras de crédito + debêntures + fundo**;
- Atua via **plataforma eletrônica**;
- **Capital mínimo**: R$ 1 milhão;
- **Sem captação direta** de poupança;
- Pode atuar como **agente** de outras instituições.

### Vantagens
- Estrutura simplificada;
- Foco em **fintech de crédito** (cartão, empréstimo, pessoa, microcrédito);
- Sem necessidade de banco completo;
- Permite cessão de carteira (FIDC + CRI).

### Restrições
- Não pode oferecer **conta corrente**;
- Não opera **câmbio** sem autorização adicional;
- Sujeito a **controles de risco** (Res. CMN 4.557/17; regime consolidado pela Res. CMN 5.050/22).

## Sociedade de Empréstimo entre Pessoas (SEP)

### Características (Res. CMN 4.656/18)
- **Plataforma de intermediação** entre tomadores e investidores;
- **Sem risco próprio**: a SEP **não financia**, apenas conecta;
- **Limites** por investidor + por operação;
- **Marketplace lending** (P2P);
- **Capital mínimo**: R$ 1 milhão;
- **Diligência de tomadores** + análise de crédito + cobrança;
- **Inadimplência**: assumida pelos investidores.

### Comparativo SCD × SEP

| | SCD | SEP |
|---|---|---|
| Risco | Da SCD | Do investidor |
| Funding | Própria | Investidores conectados |
| Volume | Sem limite per se | Limites por operação |
| Modelo | Balance sheet | Marketplace |

## Instituição de Pagamento (IP)

### Marco (Lei 12.865/13 + Res. BCB 80/21 + 24/22)
- **Lei 12.865/13**: arranjos de pagamento + IP;
- **Res. BCB 80/21** + 24/22: requisitos operacionais + capital;
- **Não é banco**: não capta depósito remunerado;
- Pode oferecer **conta de pagamento** + **emissão de cartão** + **adquirência** + **transferência**.

### Modalidades
- **Emissor de moeda eletrônica** (e-money);
- **Emissor de cartão pré-pago/pós-pago**;
- **Adquirente**;
- **Iniciador de transação de pagamento** (PIX iniciador);
- **Operador de carteira digital**.

### Capital mínimo
- **R$ 2 milhões** (até R$ 25 mi processados);
- **Aumenta** progressivamente conforme volume processado;
- **Garantias** financeiras adicionais (Fundo Garantidor de Créditos não aplicável a IP).

## Open Finance (Res. Conjunta CMN/BCB 1/20 + Inst. BCB 32/20)

### Estrutura
- **Compartilhamento** de dados entre instituições financeiras + IPs + fintechs;
- **Fases**:
  - **Fase 1** (fev/2021): canais + produtos + serviços;
  - **Fase 2** (ago/2021): dados cadastrais + transacionais (consentimento);
  - **Fase 3** (out/2021): serviços de iniciação de pagamento;
  - **Fase 4** (dez/2021): câmbio + seguros + previdência + investimentos + outros;
- **Consentimento** do cliente: granular + revogável + auditável;
- **Padrão técnico**: API REST + autenticação OAuth 2.0 / Cliente FAPI 2.0;
- **Identidade**: ICP-Brasil + autenticação multi-fator.

### Obrigações
- **Capacidade técnica**: 99% uptime + segurança LGPD + cibersegurança;
- **Atendimento ao titular**: prazo + canal + documentação;
- **Comunicação de incidente** (ANPD + BACEN);
- **Relacionamento**: cláusulas-padrão BACEN.

## Sandbox regulatório (ambiente regulatório experimental do SFN)

### Estrutura
- **Ambiente experimental** para testes de produtos inovadores;
- **BACEN** + **CVM** + **SUSEP** + **ANPD** + **ANS** + **ANATEL**;
- **Critérios**:
  - Inovação genuína;
  - Benefício ao consumidor;
  - Limites quantitativos (clientes + volume + tempo);
- **Período**: até 12 meses (prorrogável);
- **Reporte periódico**;
- **Saída**: registro regular ou descontinuação.

### Sandbox BACEN
- **Ciclo 1** (iniciado em 2021, Res. BCB 50): **7 projetos** selecionados (pagamentos multimoeda interbancários, crédito via Pix, mercado secundário de CCBs, rede de aporte em espécie, entre outros);
- Duração de 1 ano, prorrogável por igual período, com acompanhamento do Comitê Estratégico de Gestão do Sandbox (Cesb);
- Não houve abertura formal de novo ciclo do sandbox do BCB até 2026;
- **Critérios**: TI + governança + compliance.

### Sandbox CVM (RCVM 19/22)
- Operação especial em valores mobiliários;
- 3-6 meses experimentais;
- **Tokenização** + crowdfunding + robotrading.

## PIX (Res. BCB 1/20 + Manual de Operação)

### Estrutura
- **Pagamento instantâneo** (24/7/365);
- **PIX Brasil**: chaves (CPF/CNPJ/email/celular/aleatória);
- **Cobrança PIX**: split + parcelamento (PIX Crédito);
- **PIX Automático** (em operação desde 2025): pagamentos recorrentes com autorização prévia;
- **PIX Saque + Troco**;
- **PIX Internacional** (em estudo);
- **Tokenização**: substituição de chaves físicas;
- **DICT (Diretório de Identificadores de Contas Transacionais)**.

### Compliance
- **MED (Mecanismo Especial de Devolução)**: golpe + erro + fraude;
- **Res. BCB 496, 497 e 498/25** (pacote de segurança pós-ataques a prestadores de tecnologia): limite de **R$ 15 mil por transação Pix e TED** para instituições de pagamento não autorizadas e participantes conectados via PSTI; credenciamento de PSTI com capital mínimo de R$ 15 milhões; antecipação para maio/2026 do prazo para IPs pedirem autorização;
- **PLD-FT** (Lei 9.613 + Circular BCB 3.978);
- **Limites** definidos pela instituição (BACEN aprova);
- **Disponibilização ao consumidor** (CDC + Lei 10.962);
- **Cibersegurança** + Manual de Operação BACEN.

## Banking as a Service (BaaS)

### Modelo
- **Provedor de licença** bancária + IP licenciados;
- **Fintech parceira** (sem licença própria);
- **White-label** ou **embedded finance**;
- **Compartilhamento de responsabilidades** (KYC + AML + suitability + LGPD).

### Estrutura contratual
- **Acordo principal** entre provedor + parceiro;
- **Padrões operacionais** + SLA;
- **Compliance** + auditoria;
- **Responsabilidade conjunta** perante BACEN + clientes.

### Risco regulatório
- BACEN **pode requalificar** parceiro como IP/SCD se exercer atividade nuclear;
- **Lei 4.595 + 7.492 (crimes contra SFN)**: atuação ilegal de mercado financeiro;
- **Lei 9.613 (PLD-FT)**: ambos responsáveis;
- **CDC + LGPD**: fintech parceira responde diretamente ao cliente.

## Open finance + LGPD

- **Consentimento** específico + granular + revogável;
- **Base legal** = consentimento (LGPD art. 7º I);
- **Comunicação a ANPD** em incidente material;
- **Direitos do titular** (art. 18) preservados;
- **Encarregado**: obrigatório para IP + SCD + SEP;
- **Cláusulas-padrão BACEN** para compartilhamento;
- **Subcontratação** vedada sem autorização do titular.

## Tributação fintech

- **IRPJ + CSLL**: Lucro Real (em geral);
- **PIS + COFINS**: serviço financeiro = não cumulativo;
- **ISS**: sobre serviços (LC 116), com interpretações divergentes;
- **IOF**: empréstimo + câmbio (Lei 8.894 + Dec. 6.306);
- **CIDE**: pagamento ao exterior (Lei 10.168);
- **Lei do Bem (11.196)**: incentivo a P&D em fintech.

## CADE + concorrência

- **Atos de concentração**: fintech + banco grande → notificação CADE;
- **Tying** (banco impõe produto financeiro casado) → investigação CADE;
- **Big tech + finanças** (Apple Pay, Google Pay): atenção regulatória CADE + BCB;
- **Open finance**: redução de barreiras + aumento de competição.

## CVM × BACEN: sobreposição

- **Token de crédito**: BCB (se crédito) ou CVM (se valor mobiliário), a depender da estrutura;
- **Crowdfunding** (RCVM 88) + **Sandbox CVM**;
- **Tokenização de ativos**: análise caso a caso;
- **Stablecoin pareada a real**: CVM se valor mobiliário; BCB se moeda eletrônica.

## Lei 14.478/22 (Marco Cripto)

- **Prestadoras de serviços de ativos virtuais**: autorização do BCB (Decreto 11.563/2023 designou o BCB como regulador);
- **Res. BCB 519, 520 e 521/25**: marco infralegal dos ativos virtuais: a 519 disciplina a prestação de serviços (proteção ao cliente, PLD/FT, governança, cibersegurança) e cria as **SPSAVs** (intermediárias, custodiantes e corretoras); a 520 trata da autorização de funcionamento (capital mínimo escalonado) e prazos de regularização; a 521 integra os ativos virtuais ao mercado de câmbio (Lei 14.286/21); vigência escalonada a partir de 02/02/2026, com vedação de operações não autorizadas a partir de 30/10/2026;
- **Supervisor**: BCB para cripto-pagamento; CVM quando o token for valor mobiliário;
- **PLD-FT** (Lei 9.613): vedação a anonimato;
- **Lei do Bem**: aplicável a P&D blockchain.

## Erros a evitar

- **Operar sem licença** BCB (banco/SCD/IP): crime (Lei 7.492 art. 16);
- **Captação sem autorização**: Lei 7.492 + sanção;
- **Open finance** sem consentimento: ANPD + BACEN;
- **Sandbox** sem critérios atendidos: descontinuação;
- **BaaS** com fintech operando atividade nuclear sem licença → BACEN requalifica;
- **PLD-FT** descumprida: COAF + multa material;
- **PIX** com falhas de segurança: dano + ação coletiva;
- **Tokenização** sem classificação correta CVM × BCB: regulação dupla ou indevida;
- **Cripto** sem registro PSAV: multa;
- **Lei 14.478** ignorada por exchange operando no Brasil;
- **Compliance LGPD** com base legal incorreta: ANPD autua;
- **Cláusulas-padrão BACEN** modificadas: nulidade;
- **Ato de concentração** CADE não notificado: gun jumping (Lei 12.529);
- **Tributação errada** (Lucro Presumido em SCD com receita > R$ 78mi);
- **Tarifa abusiva** em conta de IP: Senacon + Procon;
- **Big tech** sem licença em pagamentos: BCB pode autuar (em curso);
- **Cyber incident** sem comunicação ao BCB em 24h;
- **PIX Automático** sem consentimento granular;
- **Crowdfunding** acima de R$ 15mi/ano sem migrar para oferta restrita ou ampla;
- **Stablecoin** pareada a real sem aprovação BCB.
