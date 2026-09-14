---
id: "04aa2af7-298e-4236-aa62-3a8bc2b87d7b"
name: "mercado-livre-energia-ccee"
title: "Mercado Livre de Energia (Lei 9.074/95 + Lei 14.300/22 + CCEE)"
category: "materia"
materia: "consultoria"
documentType: null
version: 2
sourcePath: "lib/skills/official/materia/consultoria/contratos-b2b-disputas/mercado-livre-energia-ccee.md"
triggers:
  - "mercado livre de energia"
  - "migração para o mercado livre"
  - "ambiente de contratação livre"
  - "CCEE"
  - "consumidor livre"
  - "PPA de energia"
  - "power purchase agreement"
  - "Lei 14.300"
  - "geração distribuída"
  - "Decreto 13.097/2026 baixa tensão"
  - "perda tarifa social mercado livre"
description: "Contratação no ACL, CCEE e PPA. O Decreto 13.097/2026 abre a baixa tensão em 25/11/2027 (industrial/comercial) e 25/11/2028 (demais), exige varejista e afasta benefícios tarifários do ACR."
---

# Mercado Livre de Energia (Lei 9.074/95 + Lei 14.300/22 + CCEE)

## Marco normativo

- **Lei 9.074/95**: criou consumidor livre + autoprodução + produtor independente;
- **Lei 9.648/98**: aperfeiçoou mercado;
- **Lei 10.848/04 (Marco Setorial)**: dois ambientes (ACR + ACL);
- **Lei 14.300/22**: marco da geração distribuída (mini + microgeração solar);
- **Decreto 5.163/04**: regulamento;
- **Resoluções ANEEL**: REN 1.000/21 (condições de fornecimento, substituiu a REN 414/10) + REN 482/12 (GD, superada pela Lei 14.300/22) + REN 1.059/23 (regulamenta a Lei 14.300);
- **Resolução CCEE 1/22**: regras de mercado;
- **Lei 14.182/21 + Dec. 11.069/22**: privatização Eletrobras + setor;
- **Decreto 13.097/2026**: abertura da baixa tensão, representação varejista, SUI e retorno ao ACR;
- **Lei 14.026/20**: marco do saneamento (não-energia mas paralela).

## Estrutura do setor

| Ambiente | Conteúdo |
|---|---|
| **ACR (Ambiente de Contratação Regulada)** | Distribuidora compra para consumidor cativo via leilão |
| **ACL (Ambiente de Contratação Livre)** | Negociação direta entre comprador + gerador/comercializador |
| **MCP (Mercado de Curto Prazo)** | Liquidação das diferenças pela CCEE |
| **Self-dealing / Autoprodução** | Consumidor gera sua própria energia |
| **Geração distribuída (GD)** | Mini (75 kW a 5 MW) + microgeração (≤ 75 kW) |

## Consumidor livre

### Categorias
- **Consumidor especial**: 500 kW a 3 MW + fonte incentivada (eólica, solar, biomassa, PCH);
- **Consumidor livre**: > 3 MW (qualquer fonte);
- **Comercializador varejista**: representa consumidores menores na CCEE, sem adesão direta.

### Cronograma de abertura (Portaria MME 50/22)
- **2024**: todos os consumidores de alta tensão (Grupo A) podem migrar;
- **25/11/2027**: baixa tensão industrial e comercial pode migrar;
- **25/11/2028**: os demais consumidores de baixa tensão podem migrar.

As datas de 2027 e 2028 são futuras e decorrem do Decreto 13.097/2026. A migração de baixa tensão exige representação por agente varejista na CCEE, um por unidade consumidora.

### Migração
- **Comunicar distribuidora** com a antecedência aplicável; para baixa tensão, o Decreto 13.097/2026 prevê 90 dias, sujeito à simplificação pela ANEEL;
- **Adesão ao CCEE**;
- **Contrato bilateral** com gerador ou comercializador;
- **TUSD + TE** (tarifa de uso do sistema + tarifa de energia);
- **ESS (Encargos de Serviços do Sistema)** + **CDE** (conta de desenvolvimento energético);
- **PROINFA** (até 2024);
- **MMGD (Mini e Microgeração Distribuída)**.

### Efeitos tarifários e retorno ao ACR

Ao optar pelo ACL, o consumidor de baixa tensão deixa de receber benefícios tarifários vinculados ao ACR, inclusive Tarifa Social de Energia Elétrica e descontos de irrigação e aquicultura. A distribuidora e o varejista devem informar previamente esse efeito. O retorno ao ACR exige aviso de um ano, prazo que a distribuidora pode reduzir.

O Supridor de Última Instância será regulado pela ANEEL. Distribuidoras atuam com exclusividade até 31/12/2030; a abertura a outros supridores começa em 01/01/2031.

Fonte: [Decreto 13.097/2026](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/d13097.htm).

## ACL: estrutura

### Agentes
- **Gerador** (térmica, hidrelétrica, solar, eólica, biomassa);
- **Comercializador** (intermediário);
- **Consumidor livre/especial**;
- **CCEE** (compensação + liquidação);
- **ANEEL** (regulação);
- **MCP** (mercado de curto prazo).

### Modelos contratuais
- **PPA físico** (com lastro): entrega física + tomada do risco regulatório;
- **PPA financeiro / synthetic PPA**: hedge financeiro (sem entrega física);
- **VPP (variable price)**: preço variável + indexação;
- **Take or pay**: comprador paga mesmo sem consumir;
- **Pay or play**: pagar ou consumir;
- **Sleeve PPA**: comercializador absorve risco;
- **Aggregator**: agrega múltiplos consumidores menores.

## PPA (Power Purchase Agreement)

### Cláusulas essenciais
- **Identificação** das partes + fonte + UF/sub-mercado;
- **Volume** + sazonalidade + flexibilidade;
- **Preço** + fórmula de reajuste (IPCA + IGPM + híbrida);
- **Prazo** (5-20 anos típico);
- **Entrega**: ponto de entrega + medição + perdas;
- **Garantias** (PPA é contrato long-tail);
- **Force majeure** + atos governamentais;
- **MAC** + change of control;
- **Lei aplicável + arbitragem**;
- **Tributação** (preço pode ser bruto ou líquido de tributos);
- **PROINFA + ESS** (encargos);
- **Sustentabilidade**: certificação de origem (REC, CEC, GO).

### Riscos típicos
- **Risco de geração** (curtailment, indisponibilidade);
- **Risco de preço** (mercado spot);
- **Risco regulatório** (mudanças tarifárias);
- **Risco de crédito** (contraparte);
- **Risco de submercado** (preços diferenciados por região);
- **Risco GSF (Generation Scaling Factor)** em hidrelétricas;
- **Risco de transmissão**.

## Geração distribuída (Lei 14.300/22 + Res. ANEEL 1.000/21)

### Modalidades
- **Microgeração**: até 75 kW (solar, eólica, hidráulica, biomassa);
- **Minigeração**: 75 kW a 5 MW;
- **Geração compartilhada**: múltiplos consumidores compartilham geração;
- **Autoconsumo remoto**: geração em local distinto do consumo (mesma titularidade);
- **Empreendimento de múltiplas unidades consumidoras (EMUC)**;
- **Geração local**: telhado próprio.

### Sistema de compensação (Lei 14.300)
- **Net metering**: créditos descontados em ciclos futuros (5 anos);
- **Validade**: 60 meses;
- **Transição (2023-2045)**: pagamento progressivo de **TUSD + TE** para sistemas novos;
- **Sistemas antigos** (cadastrados pré-2023): isenção até 2045;
- **Bandeiras tarifárias**: não compensam.

### Compensação de uso do sistema
- **TUSD Geração** + **TUSD Consumo**;
- **Mini e micro**: descontos progressivos até 2031;
- **Cobrança Fio B** (sistemas protocolados a partir de 07/01/2023): 2023 (15%); 2024 (30%); 2025 (45%); 2026 (60%); 2027 (75%); 2028 (90%); estabiliza em 90% a partir de 2029 (sistemas protocolados até 06/01/2023 mantêm isenção até 2045).

## CCEE: funções

- **Liquidação** das diferenças entre contratado e realizado;
- **Cálculo do PLD** (Preço de Liquidação das Diferenças);
- **Câmara de Compensação**;
- **Padrão de medição** + apuração;
- **Garantias financeiras** dos agentes;
- **Penalidades** por inadimplência;
- **Mercado de curto prazo (MCP)**: arena de spot.

## ANEEL: regulação

- **Resolução normativa** (REN) + **resolução homologatória** (REH) + **despacho**;
- **Audiência pública** prévia;
- **Tarifa**: revisão ordinária quadrienal + revisão extraordinária;
- **Concessão**: outorga + indenização (Lei 12.783/13);
- **Fiscalização**: multas + advertências + caducidade.

## Cláusulas de sustentabilidade

- **REC (Renewable Energy Certificate)**: certifica energia renovável;
- **I-REC**: padrão internacional;
- **Lei 14.300/22**: ampliou GD + sustainability;
- **PPA verde**: foco em fonte renovável + REC associada;
- **Scope 2 (GHG Protocol)**: redução de emissões via PPA verde;
- **Estratégia ESG**: PPA verde como ferramenta de descarbonização.

## Tributação

- **ICMS sobre energia**: estadual (alíquotas + isenções);
- **PIS/COFINS sobre energia**: cumulativo ou não-cumulativo;
- **ICMS no ACL**: aplicação em consumidor livre + GD;
- **Créditos de ICMS**: LC 87/96 (Lei Kandir) + LC 102/00;
- **Geração distribuída**: ICMS sobre o **complemento** (geração - consumo);
- **Reforma tributária (EC 132/23)**: IBS + CBS sobre energia (alíquota a definir).

## CADE + setor

- **Ato de concentração** em geração: notificação CADE;
- **Verticalização** (geração + distribuição): vedada (Lei 10.848 art. 8º);
- **Self-dealing**: permitido quando há propósito + transparência;
- **Mercado relevante**: SIN (Sistema Interligado Nacional): todo o Brasil;

## Aspectos contratuais: riscos

- **Hedge** via instrumentos derivativos (NDFs + swap);
- **Margem inicial + variação**: garantia financeira;
- **Step-in right** do credor em projeto financiado;
- **Direct agreement**: financiador + comprador + gerador;
- **Bring-down** entre signing e closing;
- **MAC** clima/regulatório.

## Trade compliance

- **Origem da energia** + certificação ambiental;
- **Greenwashing**: REC em dupla contagem (vedado);
- **CADE/ANPD**: análise de mercado;
- **Segurança do trabalho**: NR-10 (eletricidade) + NR-35 (trabalho em altura);
- **LGPD**: dados de consumo + adesão a programas.

## Estruturas usuais

### Self-dealing via SPE
1. Consumidor cria SPE de geração;
2. SPE recebe geração + repassa ao consumidor com tarifa preferencial;
3. **Cuidado**: substância (verticalização vedada se distribuidora estiver no grupo);
4. **CADE** se grupo for relevante.

### PPA via comercializador
1. Comercializador agrega geração;
2. PPA com consumidor por prazo definido;
3. **Hedge** entre PPA físico e financeiro;
4. **Garantias** financeiras.

### Geração distribuída remota
1. Consumidor cria UFV em terreno arrendado;
2. Geração compensa consumo via crédito (Lei 14.300);
3. **CDE Fio B** progressivo até 2029;
4. **Crédito por 60 meses**.

## Erros a evitar

- **Migrar** sem cumprir prazo de aviso (6 meses) à distribuidora;
- Esquecer **TUSD + TE** + **CDE** + outros encargos;
- Em PPA, **preço sem indexação** clara: disputa em longo prazo;
- **Force majeure** sem cobertura para evento regulatório;
- Em GD, ignorar **cronograma Fio B** (Lei 14.300): economia irreal;
- **Crédito GD** vencido (60 meses): perda;
- **Compensação ICMS** em GD: varia por UF;
- **Self-dealing** sem propósito ou substância: desconsideração + CADE;
- **PPA verde** com REC de dupla contagem: greenwashing;
- Em PPA financeiro, esquecer **risk profile** + **collateral**;
- **CCEE garantias** insuficientes: penalidade;
- **GSF** em hidrelétrica não modelado: risco material;
- Esquecer **ANEEL fiscalização** + multa por descumprimento;
- Em projeto novo, esquecer **outorga ANEEL** + estudo ambiental + ICMBio se necessário;
- **Lei 14.182** (Eletrobras) ignorada em transações com ela;
- **Conversão de moeda** em PPA internacional sem hedge;
- **Lei 14.300** ignorada em GD pós-2023;
- **CADE** notificação em consolidação de comercializadores;
- **NR-10 + NR-35** ignoradas em obra de instalação;
- **Tributação ICMS** no submercado de instalação errado.
