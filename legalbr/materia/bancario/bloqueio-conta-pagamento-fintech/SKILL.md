---
id: "ce1a275a-2ca1-43ea-a524-5897a8103cdf"
name: "bloqueio-conta-pagamento-fintech"
title: "Bloqueio de Conta e Retenção de Saldo por Bancos Digitais e Instituições de Pagamento"
category: "materia"
materia: "bancario"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/bancario/bloqueio-conta-pagamento-fintech.md"
triggers:
  - "bloqueio de conta digital"
  - "retenção de saldo"
  - "conta de pagamento bloqueada"
  - "banco digital bloqueou a conta"
  - "instituição de pagamento"
  - "Lei 12.865 arranjos de pagamento"
  - "Res. BCB 80 instituição de pagamento"
  - "Res. BCB 96 conta de pagamento"
  - "análise interna da fintech"
  - "desbloqueio de conta"
  - "encerramento unilateral de conta de pagamento"
  - "saldo retido pela fintech"
description: "Bloqueio cautelar de conta e retenção de saldo por bancos digitais e\ninstituições de pagamento: regime da Lei 12.865/2013 (conta de pagamento,\npatrimônio separado, art. 12) + Res. BCB 80/2021 e 96/2021; licitude do\nbloqueio motivado por PLD (Lei 9.613/1998) x abusividade da retenção sem\nmotivação e prazo (CDC 14 e 39); Súm. 479 STJ estendida às instituições\nde pagamento (REsp 2.222.059/SP, 2025); dano moral e tutela de urgência."
---

# Bloqueio de Conta e Retenção de Saldo por Bancos Digitais e Instituições de Pagamento

## Marco legal e regulatório

| Diploma | Conteúdo |
|---|---|
| **Lei 12.865/2013** | Arranjos e instituições de pagamento no SPB: definições (art. 6º: instituição de pagamento, conta de pagamento, moeda eletrônica), princípios (art. 7º, IV: proteção dos interesses econômicos, transparência e informação ao usuário final), competência do BCB (art. 9º), patrimônio separado (arts. 12 e 12-A) |
| **Res. BCB 80/2021** | Constituição, autorização e funcionamento das instituições de pagamento |
| **Res. BCB 96/2021** | Abertura, manutenção e **encerramento** de contas de pagamento pré-pagas e pós-pagas (encerramento exige comunicação, devolução do saldo e providências em até 30 dias corridos); Res. BCB 518/2025 acrescentou hipóteses de encerramento compulsório (irregularidade grave nas informações, prestação de serviços financeiros sem autorização) |
| **Lei 9.613/1998** | Prevenção à lavagem: deveres de identificação, registro e monitoramento (art. 10) e comunicação de operações suspeitas ao Coaf, sem ciência ao cliente (art. 11) |
| **CDC** | Arts. 6º III, 14 (responsabilidade objetiva por defeito do serviço), 39 (práticas abusivas); Súms. 297 e 479 STJ |

Encerramento regular de **conta de depósito** com aviso prévio (Res. CMN 4.753/2019) é objeto de skill própria; esta skill cobre o bloqueio cautelar, a retenção de saldo e o regime da conta de pagamento.

## Conta de pagamento e patrimônio separado

- Conta de pagamento é conta de registro detida em nome de usuário final para execução de transações de pagamento (Lei 12.865, art. 6º IV); é o modelo típico de fintechs e carteiras digitais não bancárias.
- Os recursos mantidos em contas de pagamento **constituem patrimônio separado**: não se confundem com o patrimônio da instituição, não respondem por obrigações dela nem podem ser constritos por dívidas da instituição, e não compõem sua massa em falência ou liquidação (Lei 12.865, art. 12, I a IV; art. 12-A para os fluxos de liquidação do arranjo).
- Consequência: o saldo é do usuário; a instituição é mera custodiante. Retenção sem base normativa ou contratual válida configura privação de bem alheio, frequentemente de natureza alimentar.

## Bloqueio cautelar: licitude e limites

O bloqueio preventivo pode ser exercício regular de direito quando ancorado nos deveres de prevenção à lavagem de dinheiro e à fraude (Lei 9.613, arts. 10 e 11; monitoramento de operações atípicas). A jurisprudência consumerista costuma aferir a regularidade do bloqueio pelos seguintes parâmetros, entre outros:

1. **Motivação concreta**: indício objetivo e individualizado (transação destoante do perfil, alerta de origem ilícita, contestação de terceiro). Fórmulas genéricas ("análise interna", "violação dos termos de uso", "desinteresse comercial") não bastam.
2. **Prazo razoável e determinado**: a averiguação deve ter duração compatível com a diligência; retenção por prazo indeterminado ou por várias semanas sem conclusão é abusiva.
3. **Comunicação e possibilidade de defesa**: o usuário deve ser informado do bloqueio e do canal para comprovar a origem lícita dos recursos; o sigilo do art. 11, II, da Lei 9.613 protege a comunicação ao Coaf, não autoriza silêncio absoluto sobre a indisponibilidade.
4. **Proporcionalidade**: bloqueio da transação suspeita ou de parte do saldo em vez da conta integral, quando suficiente.
5. **Ônus da prova**: cabe à instituição comprovar o fato suspeito e a regularidade do procedimento (CDC 14 §3º; inversão em favor do consumidor); sem prova, o bloqueio é defeito do serviço.

Descumpridos esses parâmetros, incidem o CDC 14 (falha do serviço) e o CDC 39 (prática abusiva: exigir vantagem manifestamente excessiva e recusar o cumprimento da prestação devida).

## Responsabilidade objetiva: Súm. 479 STJ estendida às instituições de pagamento

- **Súm. 479 STJ**: as instituições financeiras respondem objetivamente pelos danos gerados por fortuito interno relativo a fraudes e delitos de terceiros no âmbito de operações bancárias.
- **REsp 2.222.059/SP** (Terceira Turma, j. 07/10/2025): os entendimentos consolidados do STJ, inclusive a aplicação do CDC (Súm. 297), valem igualmente para as **instituições de pagamento**, que têm dever legal de garantir a segurança das transações (Lei 12.865, art. 7º); a validação de operações suspeitas, atípicas e alheias ao perfil do cliente revela defeito do serviço.
- Aplicação simétrica: se a fintech responde pelo fortuito interno da fraude, o gerenciamento do risco (bloqueios, monitoramento) integra sua atividade; o custo do erro na gestão desse risco não pode ser transferido ao usuário inocente.
- Excludentes (CDC 14 §3º): inexistência de defeito ou culpa exclusiva do consumidor/terceiro; bloqueio breve, motivado, comunicado e desfeito com celeridade tende a afastar o dever de indenizar.

## PIX retido e devolução

- Bloqueio de valores recebidos via PIX na conta do usuário apontado como recebedor de fraude segue o fluxo do Mecanismo Especial de Devolução, tratado em skill própria (pix-med-fraudes).
- Situação distinta desta skill: retenção de PIX recebido pelo próprio titular em razão de "análise" da instituição, sem acionamento de MED e sem contestação identificada; aplicam-se os parâmetros de motivação, prazo e comunicação acima.

## Teses recorrentes para a minuta

| Situação | Solução |
|---|---|
| Bloqueio sem motivação concreta demonstrada nos autos | Falha do serviço (CDC 14); desbloqueio + restituição atualizada |
| Retenção prolongada de verba de natureza alimentar (salário, faturamento de microempreendedor) | Dano moral usualmente reconhecido pela jurisprudência quando a privação prolongada de recursos essenciais ultrapassa o mero dissabor (aferir duração da retenção e comprometimento da subsistência no caso concreto) |
| Bloqueio motivado, breve e comunicado, com suspeita comprovada | Exercício regular de direito; improcedência do pedido indenizatório |
| Encerramento unilateral de conta de pagamento sem comunicação e sem devolução do saldo em até 30 dias | Violação da Res. BCB 96/2021; obrigação de fazer + perdas e danos |
| Pedido liminar de desbloqueio com prova de origem lícita e risco de dano (contas vencendo, subsistência) | Tutela de urgência (CPC 300) com astreintes |
| Instituição invoca sigilo da comunicação ao Coaf para não motivar em juízo | O dever de sigilo (Lei 9.613, art. 11, II) não a exime de comprovar em juízo os indícios que embasaram o bloqueio |

## Erros a evitar

1. Tratar toda retenção como ilícita: o bloqueio cautelar motivado e temporário é dever de compliance (Lei 9.613), não abuso.
2. Confundir conta de pagamento (Lei 12.865 + Res. BCB 96/2021) com conta de depósito (Res. CMN 4.753/2019): regimes de encerramento e supervisão distintos.
3. Ignorar o patrimônio separado do art. 12 da Lei 12.865 ao analisar constrições: o saldo do usuário não responde por dívidas da instituição de pagamento.
4. Negar a aplicação do CDC ou da Súm. 479 STJ por se tratar de fintech ou instituição de pagamento: superado (REsp 2.222.059/SP).
5. Presumir dano moral em qualquer bloqueio: exija duração relevante, natureza dos valores retidos ou recusa reiterada de informação.
6. Deixar de fixar prazo e astreintes na ordem de desbloqueio, esvaziando a efetividade da tutela.
7. Aceitar como motivação a mera repetição de cláusula genérica dos termos de uso sem indicação do fato concreto imputado ao titular.
