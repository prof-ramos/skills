---
id: "476be851-2575-41f3-8675-08a90b574f69"
name: "manipulacao-mercado-cvm"
title: "Manipulação de Mercado (CVM e Criminal)"
category: "materia"
materia: "empresarial"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/empresarial/manipulacao-mercado-cvm.md"
triggers:
  - "manipulação de mercado"
  - "art. 27-C Lei 6.385"
  - "Resolução CVM 62"
  - "spoofing"
  - "layering"
  - "wash trade"
  - "pump and dump"
  - "marking the close"
  - "operação fraudulenta"
  - "condições artificiais"
  - "prática não equitativa"
description: "Manipulação de mercado de valores mobiliários: tipo penal (Lei 6.385\nart. 27-C: reclusão 1 a 8 anos + multa de até 3x vantagem) + ilícito\nadministrativo (Lei 6.385 art. 4; Res. CVM 62/22, substituiu Inst. CVM\n8/79). Quatro tipos clássicos: (i) condições artificiais de demanda,\noferta ou preço; (ii) manipulação de preços; (iii) operação fraudulenta;\n(iv) prática não equitativa. Modalidades: spoofing, layering, wash trade,\nmarking the close, pump and dump, churning, front-running, short squeeze.\nDetecção pela BSM (B3 Supervisão). Coordenação BSM, CVM, MPF, SEC, ESMA."
---

# Manipulação de Mercado (CVM e Criminal)

## Base normativa

| Diploma | Conteúdo |
|---|---|
| **Lei 6.385/76 art. 4 IV** | Competência CVM |
| **Lei 6.385/76 art. 27-C** | Crime: reclusão 1 a 8 anos + multa até 3x vantagem |
| **Resolução CVM 62/2022** (substituiu Inst. CVM 8/79) | Define ilícitos administrativos |
| **Resolução CVM 45/21** | PAS: procedimento |
| **Regulamento BSM** | Supervisão B3, comunicação à CVM |
| **CP arts. 18 + 71** | Continuidade delitiva |
| **Convenções IOSCO MMoU** | Cooperação internacional |

## Tipo penal (Lei 6.385 art. 27-C)

| Elemento | Conteúdo |
|---|---|
| **Conduta** | Realizar operações simuladas ou executar manobras fraudulentas |
| **Finalidade** | Alterar artificialmente o regular funcionamento do mercado |
| **Tipo subjetivo** | Dolo (intenção manipulativa) |
| **Pena** | Reclusão **1 a 8 anos** + multa de até **3x** a vantagem ilícita |
| **Tentativa** | Cabível |
| **Ação penal pública incondicionada** | Regra |

## Tipos administrativos (Res. CVM 62/22)

### Art. 2 II: Condições artificiais de demanda, oferta ou preço
Cria, simula ou influencia artificialmente a demanda, oferta ou preço.

### Art. 2 III: Manipulação de preços
Utiliza qualquer processo ou artifício destinado, direta ou indiretamente, a elevar, manter ou baixar a cotação de valor mobiliário, induzindo terceiros à compra ou venda.

### Art. 2 IV: Operação fraudulenta
Uso de ardil ou artifício para enganar terceiros, com o fim de obter vantagem indevida.

### Art. 2 V: Prática não equitativa
Tratamento desigual entre clientes, beneficiando-se do exercício de função ou poder.

## Modalidades

### Spoofing (envio de ordens com cancelamento)
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Insere ordens grandes (compra ou venda) sem intenção real de execução, criando falsa percepção de oferta/demanda |
| **Objetivo** | Mover preço para executar ordens em outro lado a preço favorável |
| **Detecção** | Padrão de cancelamento elevado + posicionamento de ordens em book |
| **Casos CVM/BSM** | Diversos PAS recentes |
| **Casos internacionais** | Navinder Sarao (Flash Crash 2010); JPMorgan settlement (2020, US$ 920 mi) |

### Layering (camadas sucessivas)
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Insere múltiplas camadas de ordens em diferentes níveis de preço, sem intenção de execução |
| **Objetivo** | Criar falsa profundidade no book |
| **Detecção** | Análise de book histórico + razão ordens canceladas/executadas |

### Wash trade (operação cruzada)
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Compra e venda simultânea entre contas do mesmo beneficiário final ou entre coordenados, sem mudança real de titularidade |
| **Objetivo** | Inflar volume artificialmente (sinalizar liquidez); influenciar preço |
| **Detecção** | Cruzamento de comitentes + timing |
| **Regulação** | Vedação expressa em Res. CVM 62 + Regulamento B3 |

### Pump and dump
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Inflar artificialmente o preço de ativo (geralmente de baixa liquidez) + venda em massa após pico |
| **Objetivo** | Lucro na venda; perdas para investidores tardios |
| **Modalidades** | Salas de chat, redes sociais (Telegram, X, Discord); mídia paga |
| **Casos** | Ações de microcap; criptomoedas |
| **Regulação** | Lei 6.385 art. 27-C + Lei 14.478 (cripto) |

### Marking the close
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Operações no final do pregão para influenciar preço de fechamento (referência para opções, fundos, índices) |
| **Objetivo** | Influenciar valor de carteira, opções, derivativos |
| **Detecção** | Análise dos minutos finais + comparação com média histórica |

### Churning (giro excessivo)
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Operações excessivas em conta de cliente para gerar comissão |
| **Sujeito** | Corretora ou agente autônomo |
| **Regulação** | Res. CVM 35 (corretoras) + suitability |

### Front-running
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Negociação por agente que sabe de ordem grande pendente de cliente |
| **Sujeito** | Corretora, mesa de operações, gestor |
| **Regulação** | Vedação clara: Res. CVM 35 + Lei 6.385 |

### Short squeeze
| Elemento | Conteúdo |
|---|---|
| **Mecânica** | Compra agressiva forçando descobertura de posições vendidas |
| **Lícito** | Quando reflete dinâmica normal |
| **Ilícito** | Quando coordenado para artificializar (cuidado: Reddit/GameStop) |

## Detecção: BSM (B3 Supervisão)

| Função | Conteúdo |
|---|---|
| **Monitoramento** algorítmico do book em tempo real |  |
| **Análise** ex post de padrões anômalos |  |
| **Alertas** automatizados |  |
| **Comunicação** à CVM (instauração de PA) |  |
| **Procedimentos próprios** | Regulamento BSM: pode aplicar advertência, multa, suspensão |
| **Coordenação com CVM** | PAS posterior |

## Procedimento administrativo

| Fase | Conteúdo |
|---|---|
| **BSM Procedimento Administrativo** | Análise inicial; aplicação de sanções leves |
| **CVM PAS** | Acusação formal (Termo de Acusação) |
| **Defesa** | 30 dias (rito comum) ou 10 dias úteis (simplificado) |
| **Instrução** | Perícia, oitivas, dados de mercado |
| **Sustentação oral** | 15 min |
| **Decisão colegiada** | CVM |
| **Recurso** | EDcl, CRSFN (em hipóteses) |
| **Ação anulatória judicial** | JF |

## Algoritmos e high-frequency trading (HFT)

| Tópico | Conteúdo |
|---|---|
| **Responsabilidade** | De quem desenha + opera + supervisiona |
| **Programa de monitoramento** | Obrigatório em corretoras + gestores |
| **Auditoria de algoritmos** | Documentação dos parâmetros |
| **Kill switch** | Mecanismo de interrupção em anomalia |
| **Co-location** | Risco de assimetria de informação |
| **Conflito de interesse** | Mesa proprietária x clientes |

## Defesa em PAS

### Defesa material
1. **Ausência de dolo** (operação rotineira, automática);
2. **Justificativa econômica legítima** (hedge, arbitragem, rebalanceamento);
3. **Ausência de manipulação** efetiva (preço não foi alterado significativamente);
4. **Operação dentro de programa** algorítmico documentado;
5. **Erro técnico** (fat finger, glitch);
6. **Ausência de vantagem** (operação sem lucro ou com perda);
7. **Padrão estatístico não atípico** (comparação com mercado).

### Defesa processual
1. **Prescrição** (PAS 5 anos; penal 12 anos);
2. **Cerceamento** de defesa;
3. **Nulidade** por vício formal;
4. **Bis in idem** com BSM;
5. **Acesso aos dados** brutos para análise própria.

## Termo de Compromisso (TC)

- Cabível (Lei 6.385 art. 11 §5 + Res. CVM 45);
- **Cessação + valor pecuniário** + indenização (se aplicável);
- **Sem confissão**;
- **Coordenar com defesa criminal**;
- **Casos repetidos**: TC pode ser indeferido por desinteresse público.

## Sanções

### Administrativas (Lei 6.385 art. 11)
| Sanção | Conteúdo |
|---|---|
| **Multa** | Até o maior entre R$ 50 mi, 2x o valor da emissão/operação irregular ou 3x a vantagem obtida/perda evitada (Lei 6.385, art. 11, §1º, I-III) |
| **Suspensão** | Até 20 anos |
| **Inabilitação** | Até 20 anos |
| **Cassação** | Intermediários, auditores |
| **Proibição** | De praticar atividades de mercado |
| **Cumulação** | Em hipóteses graves |

### Criminais (art. 27-C)
| Sanção | Conteúdo |
|---|---|
| **Reclusão** | 1 a 8 anos |
| **Multa** | Até 3x vantagem |
| **Perdimento** | CP 91 II b |
| **Continuidade delitiva** (CP 71) | Aumento de 1/6 a 2/3 |

### Cível
| Sanção | Conteúdo |
|---|---|
| **Indenização** | CC 186 + 927; investidores |
| **Restituição** | CC 884 |
| **Class action** | CDC 81 + Lei 7.347 |
| **Dano coletivo** | A mercado, transparência, confiabilidade |

## Coordenação interagências

| Esfera | Coordenação |
|---|---|
| **BSM** | Detecção primária |
| **CVM** | PAS administrativo |
| **MPF** | Persecução penal |
| **PF** | Investigação |
| **BACEN** | Em corretoras e DTVMs |
| **COAF** | Lavagem associada (Lei 9.613) |
| **SEC** (EUA) | Coordenação via IOSCO MMoU |
| **FCA** (UK) | Idem |
| **ESMA** (UE) | Idem |
| **CFTC** (EUA) | Em derivativos |

## Programa de compliance anti-manipulação

| Pilar | Conteúdo |
|---|---|
| **Política de operações** | Vedações claras + procedimentos |
| **Monitoramento** algorítmico interno | Em corretoras, gestoras, tesourarias |
| **Treinamento** | Periódico |
| **Kill switch** + auditoria de algoritmos | Em HFT e estratégias automatizadas |
| **Canal de denúncia** | Whistleblower |
| **Reporte ao Comitê de Compliance** | Sistema formal |
| **Documentação** | Razão para cada operação atípica |
| **Análise ex post** | De operações que disparem alertas |
| **Segregação** mesa proprietária x clientes | Sem fluxo de informação |
| **Suitability** | Adequação de operações ao perfil |

## Erros a evitar

- **Operar sem documentar** racional econômico de operação atípica.
- **Ignorar alertas internos** de compliance: cumulação de risco.
- **Em PAS**: defender por "boa-fé" sem analisar padrão de book.
- **Em algoritmos**: tratar como "caixa preta" sem documentação dos parâmetros.
- **Em HFT**: ausência de kill switch ou supervisão humana.
- **Em mesa proprietária**: ausência de segregação com fluxo de clientes.
- **Em criptomoedas**: ignorar Lei 14.478 (regulamentação BACEN/CVM em construção).
- **Em pump and dump**: comunicações em redes sociais: prova robusta.
- **Confessar em TC** sem coordenar com defesa criminal.
- **Em wash trade**: cruzamento de comitentes do mesmo beneficiário: vedação clara.
- **Em marking the close**: operações finais sem justificativa: presunção forte.
- **Em short squeeze**: coordenar com terceiros: cartel + manipulação.
- **Cross-border**: descoordenar com SEC, FCA, ESMA, CFTC.
- **Em BSM**: ignorar procedimento próprio: cumulação com CVM.
- **Não articular** prescrição (5 anos PAS; 12 anos penal).
- **Em derivativos**: ignorar a regulação da CVM sobre derivativos (futuros, opções, swaps).
- **Em corretora**: aceitar churning de cliente: PAS contra a IF.
- **Em front-running**: ausência de barreira chinesa: PAS robusta.
- **Em recuperação de operação**: ausência de book completo: dificulta defesa.
- **Em arbitragem legítima**: confundir com manipulação: defesa documentada.
- **Em flash crash**: ausência de circuit breakers: PAS contra B3 + envolvidos.
- **Em algoritmo defeituoso**: ausência de teste pré-deploy: agravante.
- **Em delação premiada**: oferecer sem preparo: risco em outras esferas.
- **Em coordenação BSM-CVM**: tratar como instâncias separadas: bis in idem fático.
