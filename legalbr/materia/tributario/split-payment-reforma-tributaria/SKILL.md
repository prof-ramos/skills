---
id: "896c9098-e383-476c-960b-bd98d6a9d447"
name: "split-payment-reforma-tributaria"
title: "Split Payment (CF 156-A §5 II + LC 214/2025 arts. 31-35)"
category: "materia"
materia: "tributario"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/tributario/reforma-tributaria/split-payment-reforma-tributaria.md"
triggers:
  - "split payment"
  - "pagamento segregado"
  - "CF 156-A §5 II"
  - "LC 214 arts. 31 a 35"
  - "IBS CBS recolhimento"
  - "liquidação financeira"
  - "meios de pagamento"
description: "Split payment CF 156-A §5 II + LC 214 arts. 31-35: arranjo em que\nIBS+CBS são debitados DIRETAMENTE ao CG-IBS/RFB no INSTANTE da\nliquidação financeira da operação; reduz inadimplência + vincula\ncrédito ao recolhimento efetivo; modalidades INTELIGENTE (regra)\n+ SIMPLIFICADO; sistema integrado a PIX/cartões/boleto/TED."
---

# Split Payment

## Base constitucional + legal

| | Conteúdo |
|---|---|
| **CF 156-A §5 II** | Permite o split como mecanismo essencial do IBS |
| **LC 214/2025 arts. 31-35** | Regulamentação integral (regra geral no art. 31) |
| **Decreto 12.955/2026 + Resolução CGIBS 6/2026** | Regulamentos da CBS e do IBS detalham o split payment (normas comuns no Livro I do Decreto 12.955/2026) |
| **Ato Conjunto RFB/CGIBS 2/2026** | Documentação técnica oficial da **Plataforma Pública do Split Payment** (manual de integração + especificação de API), no Portal Nacional de Tributação de Bens e Serviços |
| **Lei 12.865/2013** + regulação **BACEN** | Integração com **arranjos de pagamento** |

## Conceito

| | Conteúdo |
|---|---|
| Mecânica | Adquirente faz **dois pagamentos** simultâneos: (a) valor líquido ao fornecedor; (b) **IBS+CBS** diretamente ao CG-IBS+RFB |
| Quem opera | **Instituição** liquidante (banco/adquirente/PIX/boleto), que repassa automaticamente |
| Quando | **No exato instante** da liquidação financeira |

## Cronograma de implantação

| | Conteúdo |
|---|---|
| **2026** | Ano-teste (CBS 0,9% + IBS 0,1%, recolhimento dispensado se cumpridas as acessórias); split payment **ainda não opera** |
| **27/05/2026** | **Ato Conjunto RFB/CGIBS 2/2026** publica a documentação técnica da Plataforma Pública do Split Payment (manual de integração + API) |
| **2º semestre de 2027** | Início de operação previsto nos regulamentos |

## Modalidades (LC 214 arts. 31-35)

| | Conteúdo |
|---|---|
| **Inteligente (regra)** | Sistema do CG-IBS calcula tributo devido em tempo real (NF-e + cadastro do fornecedor + alíquotas), debita a parcela e repassa |
| **Simplificado** | Apuração padronizada (percentual fixo da operação), usado quando dados em tempo real não estão disponíveis (ex.: boletos longos ou transações cross-border) |
| **Manual** | Em operações fora dos arranjos (cheque/dinheiro): fornecedor recolhe pelo regime ordinário |

## Crédito do adquirente (LC 214 arts. 31-35 + 47-56)

| | Conteúdo |
|---|---|
| Regra | **Crédito = IBS+CBS efetivamente recolhidos** pelo fornecedor (≠ destacado em NF) |
| Confirmação | Pelo sistema CG-IBS após split |
| Pagamento fora do split | Crédito **liberado após recolhimento confirmado** ou em caráter provisório (regulamento) |
| Fornecedor inadimplente | Adquirente **não perde crédito** se a operação foi via split (sistema garante) |

## Efeitos

| | Conteúdo |
|---|---|
| Caixa do fornecedor | **Recebe valor líquido** (sem o tributo), fluxo ajustado |
| Inadimplência fiscal | **Praticamente eliminada** em operações via split |
| Sonegação | Combate via vinculação NF + liquidação |
| Compensação | Crédito do adquirente entra automaticamente na conta-corrente fiscal |

## Aplicação por meios de pagamento

| Meio | Aplicação |
|---|---|
| **Cartão** (crédito/débito) | Adquirente do meio (Cielo/Rede/etc.) realiza o split |
| **PIX** | BACEN integra (PIX inteligente); alíquota debitada em tempo real |
| **Boleto bancário** | Banco emissor segrega no recebimento |
| **TED/TEF** | Banco da conta destino segrega |
| Dinheiro/cheque | Fora do split; recolhimento ordinário |

## Regimes especiais (LC 214)

| | Conteúdo |
|---|---|
| Exportação | **Sem split** (imune); crédito mantido |
| Operação imune/zero | Sem retenção (calculada como zero) |
| Regime monofásico (combustíveis) | Split centralizado na refinaria/distribuidora |
| Simples Nacional | Recolhe pelo regime único; **não** entra no split (regra); pode optar pelo regime regular |
| Cashback | Opera **após** o split confirmar arrecadação |

## Casos de não aplicação

| | Conteúdo |
|---|---|
| Operação sem meio de pagamento bancário | Recolhimento padrão pelo fornecedor |
| Antecipação de recebíveis | Tributo já segregado na operação original |
| Operação cross-border B2B com retenção | Regras específicas (reverse charge) |

## Conta-corrente fiscal (LC 214)

| | Conteúdo |
|---|---|
| Cada contribuinte | Conta unificada no CG-IBS para IBS + na RFB para CBS |
| Saldo credor | Compensação automática + restituição nos prazos da LC 214 (até **60 dias** em hipóteses qualificadas) |
| Saldos credores de **ICMS** ao final de 2032 | 240 parcelas mensais com IPCA (ADCT, EC 132) |

## Penalidades + erros

| | Conteúdo |
|---|---|
| Adquirente que **deixa de fazer split** quando obrigado | Multa + responsabilidade solidária pelo IBS+CBS |
| Instituição liquidante negligente | Multa + responsabilidade |
| Fornecedor que **declara alíquota inferior** | Diferença + multa de ofício (qualificada em caso de fraude) |

## Síntese operacional

| Hipótese | Saída |
|---|---|
| Compra B2B paga por cartão | **Split inteligente**: a credenciadora retém IBS+CBS |
| PIX entre empresas | **PIX inteligente**: retenção no arranjo |
| Boleto | Banco emissor retém |
| Exportação | **Sem split** (imune) |
| Operação em dinheiro | Sem split; recolhe pelo regime ordinário |
| Fornecedor inadimplente, operação via split | Adquirente **mantém crédito** |
| Fornecedor inadimplente, **sem** split | Crédito **suspenso** até confirmação |
| Combustíveis | Split centralizado na refinaria |
| Simples Nacional | Regime único; sem split (regra) |
| Conta-corrente saldo credor | Restituição nos prazos da LC 214 (até 60 dias em hipóteses qualificadas) |

## Distinções essenciais

| | ICMS atual | Split IBS/CBS |
|---|---|---|
| Recolhimento | Fornecedor mensal | **Instantâneo na liquidação** |
| Risco inadimplência | Alto | **Quase zero** |
| Crédito | Sobre NF destacada | **Sobre tributo efetivamente recolhido** |
| Adquirente | Não responde | **Solidário** se omitir split |

| | Substituição tributária ICMS | Split |
|---|---|---|
| Sujeito | Industrial/atacadista | **Instituição liquidante** |
| Antecipação | Cadeia inteira | **Operação a operação** |

## Erros a evitar

- Confundir **destaque em NF** com **recolhimento efetivo**: o crédito do adquirente depende do **recolhimento** (LC 214 arts. 31-35 + 47);
- Deixar de **fazer split** em operação obrigada (multa + solidariedade);
- Tratar Simples Nacional como obrigado ao split (regime único, sem split como regra);
- Aplicar split a **exportações** (imunes, sem retenção);
- Esquecer que **PIX inteligente** integra split (BACEN);
- Considerar que **dinheiro/cheque** entra no split (não entra; recolhimento ordinário);
- Acreditar que o adquirente **perde crédito** se o fornecedor for inadimplente em operação via split (não perde);
- Ignorar a **conta-corrente fiscal unificada** (saldo credor compensável/restituível nos prazos da LC 214);
- Tratar a instituição liquidante como **agente comum** (é responsável tributário, LC 214);
- Aplicar split sobre **operação imune/zero** (não há tributo a reter);
- Penhorar/cobrar do fornecedor o tributo **já recolhido** via split (bis in idem);
- A restituição de saldo credor é devida nos prazos da LC 214;
- Tratar split como mera "antecipação" (é **regime de pagamento direto**);
- Esquecer de cadastrar **alíquotas reduzidas** (60%/30%) no sistema do CG-IBS (o split aplicaria a cheia);
- Ignorar a transição: o split payment **não opera em 2026** (ano-teste, com recolhimento dispensado se cumpridas as acessórias); a operação da plataforma está prevista para o **2º semestre de 2027** (Ato Conjunto RFB/CGIBS 2/2026).
