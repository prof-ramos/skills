---
id: "3d825d26-efe1-40b3-bd53-acdf792357f6"
name: "vazamento-dados-lgpd-tema-1286"
title: "Vazamento de Dados Pessoais — Dano Moral (LGPD + STJ)"
category: "materia"
materia: "digital-dados"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/digital-dados/vazamento-dados-lgpd-tema-1286.md"
triggers:
  - "vazamento de dados"
  - "leak de dados"
  - "LGPD dano moral"
  - "dados sensíveis"
  - "Serasa leak"
  - "dano moral presumido dados"
  - "REsp 2.121.904"
  - "AREsp 2.130.619"
  - "REsp 2.201.694"
description: "Vazamento de dados pessoais (LGPD + CDC + CC): dado COMUM exige prova\ndo dano efetivo (STJ — AREsp 2.130.619/2023 + REsp 2.103.726/2024);\ndado SENSÍVEL (LGPD 5 II) — dano moral PRESUMIDO (in re ipsa) — STJ\nREsp 2.121.904/2025. Responsabilidade objetiva do controlador (LGPD\n42 + CDC 14); ANPD; inversão do ônus. O tema é definido por julgados\ndas Turmas, não por recurso repetitivo do STJ."
---

# Vazamento de Dados Pessoais — Dano Moral

## Base normativa

- **Lei 13.709/2018 (LGPD)**;
- **Dec. 11.058/2022** (regulamento parcial);
- **CF 5 X + LXXIX + 22 XXX**;
- **CC 186, 187, 927 parágrafo único**;
- **CDC 6, 14, 17** — relação aplicável quando há consumo subjacente;
- **Marco Civil da Internet (Lei 12.965/2014)** — armazenamento;
- **Res. CD/ANPD 15/2024** — comunicação de incidente de segurança (prazo de 3 dias úteis);
- **Res. CD/ANPD 4/2023** — dosimetria das sanções administrativas.

## Conceitos LGPD

| Art. | Conteúdo |
|---|---|
| **5 I** | **Dado pessoal**: informação relacionada a pessoa natural identificada ou identificável |
| **5 II** | **Dado pessoal sensível**: origem racial/étnica, convicção religiosa, opinião política, filiação sindical, dado referente a saúde, vida sexual, **dado genético ou biométrico** |
| **5 V** | **Titular**: pessoa natural a quem se referem os dados |
| **5 VI** | **Controlador**: pessoa natural/jurídica a quem competem decisões sobre o tratamento |
| **5 VII** | **Operador**: realiza tratamento em nome do controlador |
| **5 X** | **Tratamento**: toda operação realizada com dados pessoais |
| **5 XII** | **Consentimento**: manifestação livre, informada e inequívoca |
| **5 XIV** | **Anonimização** |
| **6** | Princípios — finalidade, adequação, necessidade, transparência, segurança, prevenção, não discriminação, responsabilização |

## Responsabilidade civil (arts. 42-45)

| Art. | Conteúdo |
|---|---|
| **42** | Controlador/operador responde pelos danos patrimoniais, morais, individuais ou coletivos causados em razão do tratamento |
| **42 §1** | **Solidariamente**: operador (se descumpriu obrigação) e controladores conjuntos |
| **42 §2** | **Eximentes**: I) não realizou tratamento; II) ausência de violação à LGPD; III) culpa exclusiva do titular ou terceiro |
| **43** | Reparação inclui dano patrimonial, moral, individual ou coletivo |
| **44** | Tratamento irregular — quando não fornece a segurança esperada |
| **45** | Reparação aplicação direta nas relações de consumo (CDC) |

## STJ — evolução jurisprudencial

### AREsp 2.130.619/SP (2ª Turma, 2023, Rel. Min. Francisco Falcão)

| | Conteúdo |
|---|---|
| Tese | Vazamento de **dado comum** (nome, CPF, e-mail) **NÃO** gera dano moral presumido |
| Exige | Comprovação de **dano efetivo** (prova concreta) |
| Lógica | Mero acesso ou exposição não basta — exige uso indevido + repercussão |

### REsp 2.103.726/SP (2ª Turma, 2024)

| | Conteúdo |
|---|---|
| Reafirma | Dado **comum** → exige prova do dano |
| Ressalva | Caso a caso pode haver dano moral se circunstâncias mostrarem dor/abalo |

### REsp 2.121.904/SP (3ª Turma, fev/2025, Rel. Min. Nancy Andrighi)

| | Conteúdo |
|---|---|
| Tese | Vazamento de **dado SENSÍVEL** (seguro de vida → saúde) gera dano moral **PRESUMIDO** (in re ipsa) |
| Fundamento | LGPD 5 II + tratamento mais rigoroso para sensíveis |
| Aplicação | Saúde, biometria, genética, orientação sexual, religião, dado bancário (em alguns casos), credenciais |

### Estado da jurisprudência (Turmas do STJ)

- A matéria é definida por **julgados das Turmas** (REsp 2.121.904; AREsp 2.130.619; REsp 2.201.694), **não** por recurso repetitivo;
- Distinção consolidada entre **dado comum** (exige prova de dano) e **dado sensível** (dano presumido);
- **Atenção**: NÃO existe tema repetitivo do STJ sobre vazamento de dados/dano moral. O "Tema 1.286 do STJ" trata de **limite de consignação em folha de militares das Forças Armadas** (REsp 2.145.185/RJ + 2.145.550/RJ), assunto distinto — não citar como precedente de vazamento.

## Síntese operacional

| Tipo de dado | Dano moral | Ônus da prova |
|---|---|---|
| **Sensível** (saúde, biometria, vida sexual, religião) | **Presumido** (in re ipsa) | Controlador (afastar) |
| **Sigiloso** (credenciais bancárias, senhas, dados financeiros) | Tendência a presumir (caso) | Controlador |
| **Comum** (nome, CPF, e-mail, endereço) | **Não presumido** | Titular (prova do dano) |
| Combinado (dado comum + uso para fraude) | Configurado pelo uso fraudulento | Titular |
| Acesso por agente público sem finalidade | Presumido (ofensa à autodeterminação) | Controlador |

## Hipóteses de incidente de segurança

| Hipótese | Tratamento |
|---|---|
| **Vazamento massivo** (megaleak Serasa, Caixa, OAB) | Caso a caso — sensível presume |
| **Acesso indevido por funcionário** | Dever de segurança da empresa (CDC 14) |
| **Phishing facilitado por falha de IF** | Banco responde solidariamente (Súm. 479 STJ) |
| **Vazamento médico** (prontuário, exames) | Dano moral in re ipsa |
| **Anúncio em darkweb / Telegram** | Indício forte de dano |
| **Notificação ANPD obrigatória** (Res. 15/2024) | Falha → reforça responsabilidade |
| Vazamento sem notificação ANPD | Indício de descumprimento (LGPD 48) |

## Responsabilidade objetiva (LGPD + CDC)

| Elemento | Conteúdo |
|---|---|
| Atividade de risco (CC 927 par. único) | Tratamento massivo de dados |
| CDC 14 — fato do serviço | Aplicável quando há consumo |
| LGPD 42 — independente de culpa | Eximentes do § 2 (taxativas) |
| Solidariedade | Controlador + operador (§ 1) |

## Eximentes (LGPD 42 §2)

| Hipótese | Conteúdo |
|---|---|
| I — Não realizou tratamento | Comprovar não atuação |
| II — Ausência de violação à LGPD | Conformidade com a lei (medidas de segurança art. 46) |
| III — Culpa exclusiva do titular ou terceiro | Phishing em que titular forneceu voluntariamente |

**STJ pacífico**: força maior + caso fortuito **NÃO afastam** em si — depende de o controlador comprovar a robustez das medidas (art. 46 — fortuito interno).

## ANPD (Lei 13.853/2019)

| Função | Conteúdo |
|---|---|
| Fiscalização | Aplica sanções administrativas (LGPD 52) |
| **Notificação obrigatória** | Incidente que possa acarretar risco/dano (LGPD 48) — em **3 dias úteis** (Res. ANPD 15/2024) |
| Multa | Até 2% do faturamento do grupo, limitada a R$ 50 mi por infração |
| Esfera independente | Sanção administrativa **NÃO substitui** indenização civil |

## Quantum

| Caso | Valor referencial |
|---|---|
| Dado comum vazado, sem uso comprovado | R$ 0 a R$ 5.000 (caso a caso) |
| Dado comum + uso para fraude (negativação, abertura de conta) | R$ 5.000 a R$ 15.000 |
| Dado sensível (saúde, genético) | R$ 5.000 a R$ 30.000 |
| Vazamento massivo com repercussão pública | R$ 10.000 a R$ 50.000 |
| Vazamento + estelionato + dano financeiro | + dano material |

## Tutela coletiva

- **ACP** (Lei 7.347/85) — MP, defensoria, associações com pertinência;
- **Dano moral coletivo** — aplicável (Súm. 643 STJ);
- **Liquidação individual** — [[execucao-individual-sentenca-coletiva-lacp-cdc]];
- ANPD pode atuar como interveniente.

## Prescrição

| Pretensão | Prazo |
|---|---|
| LGPD pura (sem consumo) | **3 anos** (CC 206 §3 V — reparação civil) **ou** 5 (controvérsia) |
| Relação de consumo (CDC 27) | **5 anos** — fato do serviço |
| LGPD coletiva (ACP) | **5 anos** (Lei 7.347) |

## Competência

| Foro | Hipótese |
|---|---|
| **JEC** (até 40 SM) | Individual contra empresa privada |
| **Justiça Estadual comum** | Acima de 40 SM ou complexa |
| **Justiça Federal** | Vazamento em órgão federal (CF 109 I) |
| **JEF** (até 60 SM) | Federal sem complexidade |
| **Foro do consumidor** (CDC 101 I) | Em relação de consumo |

## Súmulas correlatas

| | Conteúdo |
|---|---|
| **Súm. 297 STJ** | CDC aplica-se a IFs |
| **Súm. 477 STJ** | CDC compatível com regulamentação setorial |
| **Súm. 479 STJ** | Bancos respondem por fraudes em operações eletrônicas (fortuito interno) |
| **Súm. 643 STJ** | Cabe **dano moral coletivo** |

## Erros a evitar

- O vazamento de **dado comum** não gera dano moral in re ipsa, exigindo prova do dano (STJ);
- O vazamento de **dado sensível** presume o dano moral (REsp 2.121.904);
- A **força maior** depende da aferição da robustez das medidas técnicas (LGPD 46, fortuito interno);
- O **operador** não se exonera quando descumpriu as instruções do controlador (LGPD 42 §1);
- A sanção da ANPD não se confunde com a indenização civil (esferas independentes);
- A pretensão reparatória sujeita-se a prazo **prescricional**, não decadencial;
- A **notificação obrigatória à ANPD** (LGPD 48) é elemento de aferição de descumprimento;
- O ônus da prova negativa sobre uso indevido não recai sobre o titular (CDC 6 VIII; LGPD 42);
- O leak não configura **caso fortuito externo** quando há falha de segurança;
- O **dado sensível** distingue-se do comum (LGPD 5 II);
- A dobra do CDC 42 par. único exige **pagamento efetivo**, não se confundindo a reparação por LGPD com a repetição em dobro;
- O **CDC 14** incide quando o tratamento ocorre em relação de consumo;
- A **competência da Justiça Federal** não alcança vazamento em empresa privada sem ente federal envolvido.
