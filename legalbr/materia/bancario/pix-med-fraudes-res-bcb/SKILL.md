---
id: "4116e682-9522-49b6-97d1-8380c2c3eeae"
name: "pix-med-fraudes-res-bcb"
title: "Pix e MED: Mecanismo Especial de Devolução (Res. BCB 1/2020 e 103/2021)"
category: "materia"
materia: "bancario"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/bancario/pix-med-fraudes-res-bcb.md"
triggers:
  - "Pix"
  - "MED"
  - "mecanismo especial de devolução"
  - "Resolução BCB 1/2020"
  - "Resolução BCB 103/2021"
  - "Resolução BCB 142/2021"
  - "Súm. 479 STJ"
  - "fortuito interno"
  - "responsabilidade banco fraude"
  - "golpe da falsa central"
  - "conta laranja"
  - "estelionato eletrônico"
description: "Pix: regulado pela Res. BCB 1/2020 (Regulamento do Pix) + Res. BCB\n103/2021 (MED, Mecanismo Especial de Devolução); responsabilidade\nda IF por falha de segurança é objetiva (CDC 14 + Súm. 479 STJ,\nfortuito interno); MED tem prazo de 80 dias para acionamento;\nreembolso depende de saldo na conta recebedora; chave Pix no DICT;\nPix Saque/Troco (Res. BCB 142/2021); limite de R$ 15 mil por\ntransação para IPs não autorizadas e participantes via PSTI\n(Res. BCB 496-498/2025); SLA de bloqueio cautelar."
---

# Pix + MED: Responsabilidade e Devolução

## Base normativa

| Norma | Conteúdo |
|---|---|
| **Lei 12.865/13** | Arranjos de pagamento: competência do BCB |
| **Res. BCB 1/2020** | Regulamento do Pix (operação, liquidação em tempo real, DICT) |
| **Res. BCB 103/2021** | **MED** (Mecanismo Especial de Devolução: fraude/falha operacional) |
| **Res. BCB 142/2021** | Pix Saque/Troco em estabelecimentos comerciais + medidas de segurança (limite noturno) |
| **Instrução Normativa BCB 207/2022** | Operacional do MED: fluxo entre IFs |
| **Res. CMN 4.893/21** | Política de segurança cibernética obrigatória |
| **Res. BCB 496, 497 e 498/2025** | Pacote de segurança pós-ataques a prestadores de tecnologia: limite de **R$ 15 mil por transação Pix e TED** para instituições de pagamento **não autorizadas** e participantes conectados via **PSTI**; credenciamento de PSTI (capital mínimo R$ 15 milhões); antecipação para maio/2026 do prazo para IPs pedirem autorização; INs BCB 666/667 regulam dispensa temporária do limite |
| **Regulamentação BCB do Pix** | Limites noturnos + escalonamento antifraude (conferir a resolução vigente) |
| **CDC arts. 14, 6 VIII, 25 §1º** | Responsabilidade objetiva da IF |
| **Súm. 479 STJ** | "As instituições financeiras respondem objetivamente pelos danos gerados por fortuito interno relativo a fraudes e delitos praticados por terceiros no âmbito de operações bancárias" |
| **CP 171 §2-A** | Estelionato eletrônico (Lei 14.155/21): pena 4-8 anos |

## Natureza do Pix

| | Conteúdo |
|---|---|
| Liquidação | **Instantânea**, 24/7, via SPI (Sistema de Pagamentos Instantâneos do BCB) |
| Irrevogabilidade | Após liquidação no SPI, a transferência **não é revertida** unilateralmente; devolução só por MED ou ordem judicial |
| Identificadores | Chave Pix (CPF/CNPJ, e-mail, celular, EVP) registrada no **DICT** (Diretório de Identificadores de Contas Transacionais) |
| Custódia | Conta de pagamento ou conta de depósito em IF participante |
| Modalidades | Pix transferência, Pix Cobrança (QR estático/dinâmico), **Pix Saque** (saque em comércio), **Pix Troco** (compra + saque), Pix Automático, Pix Garantido |

## MED (Mecanismo Especial de Devolução)

| Item | Conteúdo |
|---|---|
| **Hipóteses** | (i) **Fundada suspeita de fraude** (Pix sob coação, golpe, conta laranja) OU (ii) **falha operacional** da IF |
| **Quem aciona** | **Pagador** ou **recebedor** vítimas, pela IF que opera a conta |
| **Prazo de abertura** | **80 dias** corridos a contar da transação (IN BCB 207/22) |
| **Análise entre IFs** | Prazo regulamentar para análise e decisão (fixado na regulamentação do MED pelo BCB; conferir a versão vigente, MED 2.0) |
| **Bloqueio cautelar** | Imediato: saldo bloqueado pela IF recebedora pelo valor disputado |
| **Devolução** | Depende de **saldo suficiente** na conta recebedora; rateio proporcional se múltiplas vítimas |
| **Decisão final** | (a) devolução total/parcial OU (b) indeferimento fundamentado |
| **Indeferimento** | Caminho judicial: execução / indenização |
| **Comunicação a órgãos** | IF deve comunicar fraude ao DICT (bloqueio da chave) + autoridades |

## Responsabilidade da instituição financeira

| Hipótese | Tratamento |
|---|---|
| **Phishing/engenharia social/golpe do boleto** | Não há repetitivo específico sobre golpe virtual. A IF responde pelo **tratamento indevido de dados pessoais bancários** utilizados pelo estelionatário (REsp 2.077.278/SP, 3ª Turma, 2023: vazamento de dados vinculados a operações bancárias = falha do serviço; dados cadastrais básicos, obteníveis por outras fontes, não geram responsabilidade exclusiva); a **culpa exclusiva da vítima** afasta o nexo quando inexistente defeito do serviço |
| **Golpe da falsa central / WhatsApp clonado** | IF responde por **fortuito interno** quando a conta laranja foi aberta com fraude no próprio banco (Súm. 479 STJ): falha na verificação cadastral |
| **Pix por terceiro com acesso físico ao celular** | Responsabilidade compartilhada: depende de hábitos de segurança (biometria, senha forte) e do tempo de resposta da IF |
| **Pix de madrugada acima do limite** | Limite noturno (Res. BCB 142/21: R$ 1.000 default das 20h às 6h); descumprimento da IF gera responsabilidade |
| **Falha do sistema (transferência duplicada, valor errado)** | Responsabilidade objetiva da IF: devolução integral |
| **Sequestro relâmpago / coação física** | IF não responde pela autoria, mas deve atuar via MED + comunicar autoridades |

## Pix Saque + Pix Troco (Res. BCB 142/2021)

| | Conteúdo |
|---|---|
| Limite por operação | R$ 500 (Pix Saque) e R$ 500 troco em compra (Pix Troco); IF pode reduzir |
| Limite diário | R$ 3.000 / R$ 1.000 conforme horário |
| Tarifa | Lojista pode cobrar até R$ 0,25 por operação (livre) |
| Responsabilidade | IF do recebedor (lojista) responde por falha operacional; lojista, pelo inadimplemento do saque físico |

## Chave Pix + DICT

| Item | Conteúdo |
|---|---|
| Limite de chaves | 5 por conta PF + 20 por conta PJ |
| Posse | Vinculação na IF mediante prova de titularidade (SMS, e-mail, OAuth Receita) |
| Portabilidade | Chave migra entre IFs preservando histórico, sem custo |
| Reivindicação | Quando outro CPF/CNPJ vinculou chave sem direito: janela de 7 dias |
| Bloqueio cautelar | IF pode bloquear chave usada em fraude (até 72h), conforme Res. BCB 142/21 |
| Marcação no DICT | Conta envolvida em fraude recebe marcação compartilhada entre IFs |

## Limites operacionais

| Período | Default PF | Default PJ |
|---|---|---|
| **Diurno (6h-20h)** | Definido pela IF | Definido pela IF |
| **Noturno (20h-6h)** | **R$ 1.000** (default Res. BCB 142/21), ajustável até 24h de antecedência | **R$ 1.000** |
| Pix por aproximação / NFC | Limites próprios (Pix Automático) |
| Aumento de limite | Vigência **24-48h** após pedido (período de carência antifraude) |
| **IPs não autorizadas / participantes via PSTI** | **R$ 15 mil por transação** Pix e TED (Res. BCB 496-498/25), com dispensa temporária regulada pelas INs BCB 666/667 |

## STJ: jurisprudência aplicável

| | Conteúdo |
|---|---|
| **Súm. 479 STJ** | Responsabilidade objetiva por fortuito interno em fraude eletrônica |
| **Tema 466 STJ** (REsp 1.197.929/PR, 2ª Seção, 24/08/2011) | "As instituições financeiras respondem objetivamente pelos danos gerados por fortuito interno relativo a fraudes e delitos praticados por terceiros no âmbito de operações bancárias" (origem da Súm. 479) |
| **Tema 1.061 STJ** | Impugnada a autenticidade da assinatura em contrato bancário, o ônus de prová-la cabe à IF (CPC 6, 369 e 429 II) |
| REsp 2.222.059 e 2.229.519 (3ª Turma, j. 07/10/2025) | Golpe da falsa central / engenharia social: bancos e instituições de pagamento respondem quando falham na proteção de dados ou na detecção de transações atípicas fora do perfil do cliente (não julgado sob o rito dos repetitivos) |
| REsp 2.077.278/SP (3ª Turma, 2023) | Golpe do boleto: a IF responde pelo tratamento indevido de dados pessoais bancários que facilitou o estelionato (LGPD art. 44 + Tema 466); a imputação exige que a origem do vazamento seja o sistema bancário |
| **EAREsp 676.608 (Corte Especial)** | Devolução em dobro (CDC 42 par. único) independe de má-fé, bastando a violação da boa-fé objetiva, para cobranças posteriores a 30/03/2021 |

## Defesa do consumidor: checklist

1. **Aciona MED** dentro de 80 dias: protocolar na IF (atendimento + ouvidoria);
2. **Boletim de Ocorrência**: necessário para MED por suspeita de fraude;
3. **Print de extrato** + horário do Pix + chave do destinatário;
4. **Demonstrar falha da IF**: ausência de alerta antifraude, login em dispositivo novo sem 2FA, transferência acima do padrão sem confirmação reforçada, falha do limite noturno;
5. **Pedido judicial**: tutela de urgência para bloqueio (CPC 300); MED via ordem ao SPI/BCB; ressarcimento + dano moral;
6. **Foro**: domicílio do consumidor (CDC 101 I);
7. **Pedido a outras IFs**: tutela inibitória contra reabertura de contas em cadeia (conta laranja).

## Defesa da instituição financeira: checklist

1. **Evidência de regularidade**: log do sistema, autenticação multifator, biometria, IP, geolocalização, padrão habitual;
2. **Culpa exclusiva da vítima**: forneceu senha, instalou aplicativo malicioso, compartilhou OTP, com prova robusta (não basta alegação);
3. **MED tempestivo**: demonstrar que processou o MED no prazo regulamentar e bloqueou o saldo disponível;
4. **Cumprimento da Res. CMN 4.893/21** (segurança cibernética): auditorias, testes, PSO;
5. **Limites observados** (noturno, antifraude, escalonamento);
6. **Bloqueio cautelar** da chave do recebedor + comunicação ao DICT;
7. **Súm. 479 STJ** não é objetiva absoluta: exige nexo entre o serviço bancário e o dano (REsp 2.077.278).

## Distinção Pix × TED × DOC

| | Pix | TED | DOC |
|---|---|---|---|
| Liquidação | Instantânea 24/7 | D+0 horário comercial | Descontinuado 2024 |
| Custo | Gratuito PF | Tarifado | (extinto) |
| Reversibilidade | Apenas MED ou ordem judicial | Estorno mais simples até a liquidação | (extinto) |
| Identificador | Chave / dados bancários / QR | Dados bancários completos | (extinto) |
| Limite noturno | R$ 1.000 (default) | Sem limite específico | (extinto) |

## Erros a evitar

- Aguardar mais de **80 dias** para acionar o MED: perda do direito ao mecanismo;
- Confundir **MED** com **estorno bancário comum**: MED só existe em fraude/falha operacional;
- Aplicar **responsabilidade objetiva absoluta** sem analisar a conduta da vítima (REsp 2.077.278);
- Esquecer o **BO**: pressuposto para MED por fraude;
- Não invocar a **Súm. 479 STJ** quando há abertura de **conta laranja** na própria IF requerida;
- Pedir devolução integral sem prova de **saldo bloqueado** na conta recebedora: a devolução pode ser proporcional;
- Tratar **Pix Saque/Troco** como saque comum em ATM: regras próprias da Res. BCB 103/2021;
- Não pedir **tutela inibitória** contra reabertura de cadeia de contas laranja;
- Exigir prova de **má-fé** para a devolução em dobro: após 30/03/2021 basta a violação da boa-fé objetiva (CDC 42 par. único; EAREsp 676.608, Corte Especial);
- Atribuir **fortuito externo** quando a fraude ocorreu **dentro** do ambiente bancário (Súm. 479);
- Pedir indenização da IF do **pagador** quando a falha foi da IF **recebedora**: a legitimidade depende do fato gerador.
