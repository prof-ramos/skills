---
id: "8f312ed0-6d9e-4f0a-93ac-86e874367b06"
name: "urna-eletronica-votacao"
title: "Urna Eletrônica + Processo de Votação e Apuração"
category: "materia"
materia: "eleitoral"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/eleitoral/urna-eletronica-votacao.md"
triggers:
  - "urna eletrônica"
  - "voto secreto"
  - "ADI 5.889"
  - "voto impresso"
  - "biometria eleitoral"
  - "totalização de votos"
  - "Boletim de Urna"
description: "Voto eletrônico, urna eletrônica e processo de votação e apuração\nsob a CF 14 §1, o Código Eleitoral e a Lei 9.504/97:\nfuncionamento da urna DRE, RDV, boletim de urna e cadeia de\ncustódia; auditabilidade, biometria e CTE; identificação,\nvotação, apuração e totalização; jurisprudência do STF sobre\nvoto impresso e diplomação."
---

# Urna Eletrônica + Votação + Apuração

## Bases legais

- **CF 14 caput** (voto direto e secreto: cláusula pétrea, CF 60 §4 II);
- **CE Lei 4.737/65** (arts. 132-141, 159-169, 179-200, 215-216);
- **Lei 9.504/97** (arts. 59-73);
- **Lei 10.740/2003** (RDV);
- **Lei 13.165/2015** (instituiu o voto impresso do art. 59-A, depois declarado inconstitucional na ADI 5.889);
- **Res. TSE 23.673/2021** (fiscalização e auditoria dos sistemas eleitorais), alterada para as Eleições 2026 pela **Res. TSE 23.758/2026**;
- **Portaria TSE 578/2021** (instituiu a Comissão de Transparência das Eleições, CTE).

## Urna eletrônica

| | Conteúdo |
|---|---|
| Modelo | **DRE** (Direct Recording Electronic) |
| Implantação | Desde 1996; totalidade desde 2000 |
| Voto impresso | **Não há** (art. 59-A declarado inconstitucional, ADI 5.889) |
| Zerésimo | Na abertura |
| BU | Boletim de Urna + QR Code |
| RDV | Embaralhado (proteção do segredo) |
| Conectividade | **Sistema fechado**, não conectado à internet |
| Segurança | **HSM** + assinatura digital + criptografia |

## Auditabilidade

- **Código-fonte aberto** para inspeção;
- **TPS** Testes Públicos de Segurança bianuais;
- **Teste de integridade** no dia (urnas sorteadas), com cédulas previamente preenchidas digitadas na urna (Res. 23.673/2021, com a redação da Res. 23.758/2026);
- **CTE** (Portaria TSE 578/2021): especialistas + representantes de instituições públicas e da sociedade civil (OAB, MP, TCU, Forças Armadas, PF);
- Fiscalização e auditoria dos sistemas: **Res. TSE 23.673/2021**, atualizada para as Eleições 2026 pela **Res. TSE 23.758/2026** (relatórios de auditoria dos TREs em até 30 dias e relatório consolidado do TSE em até 90 dias após o 2º turno);
- Auditoria FFAA 2022: **não apontou fraude**.

## Biometria

- Implantada **progressivamente pelo TSE** (revisões biométricas do eleitorado);
- Cobertura amplamente universalizada na década de 2020;
- Reconhecimento por impressão digital, com identificação manual pelo mesário em caso de falha;
- **e-Título** aceito como documento de identificação.

## Votação

| | Conteúdo |
|---|---|
| Horário | **8h-17h horário de Brasília** (único nacional desde 2022) |
| Identificação | Título + documento oficial com foto / e-Título |
| Falha biométrica | Manual pelo mesário |
| Voto em trânsito | Capitais e municípios com **+100 mil eleitores** (CE 233-A): fora da UF do domicílio, só para **Presidente**; dentro da UF, para todos os cargos da eleição geral |
| Voto no exterior | Só Presidente |
| Contingência | Cédulas (Lei 9.504 art. 59 §4) |

## Apuração

1. **BU local** emitido ao final;
2. **MR** transportada ao TRE;
3. Transmissão criptografada **TRE → TSE** via rede privada;
4. **Totalização** no TSE com logs auditáveis;
5. **Divulgação aberta** (DivulgaCand).

## Jurisprudência STF

| | Conteúdo |
|---|---|
| **ADI 5.889** (2020) | Declarou inconstitucional o voto impresso (art. 59-A): risco ao segredo do voto |
| **Jurisprudência consolidada** | STF e TSE afirmam a confiabilidade e auditabilidade do sistema eletrônico |
| **PEC 135/2019** | Rejeitada pela Câmara em 2021 |
| **Inq 4.781** | Fake news/milícias digitais (Min. Moraes) |
| **Tema 987** (RE 1.037.396) | Art. 19 do Marco Civil parcialmente inconstitucional: responsabilidade das plataformas ampliada |
| **ADPF 572** (julgada improcedente, 2020) | Afirmada a constitucionalidade e a legalidade do Inq. 4.781 (fake news) |

## Diplomação e posse

| Cargo | Posse |
|---|---|
| Presidente/Vice | **5 de janeiro** a partir dos eleitos em 2026 (EC 111/2021, CF 82); até então, 1º de janeiro |
| Governadores/Vices | **6 de janeiro** a partir dos eleitos em 2026 (EC 111/2021, CF 28) |
| Deputados Federais/Senadores | 1º de fevereiro |
| Prefeitos/Vereadores | 1º de janeiro |

## Erros a evitar

- O **voto impresso** foi declarado inconstitucional por violar o segredo do voto (ADI 5.889 STF);
- Tratar urna como **conectada à internet** (insulada);
- Considerar BU como **inacessível ao cidadão** (afixado + QR Code);
- Esquecer **horário único de Brasília** (desde 2022);
- Permitir voto em trânsito **fora da UF** para cargos que não o de Presidente (CE 233-A §1 II);
- Esquecer a votação de **contingência** por cédulas em caso de falha da urna;
- Tratar a identificação biométrica como dispensável onde implantada;
- Considerar relatório das FFAA 2022 como apontando fraude (não apontou);
- Aplicar resoluções de ciclos anteriores sem conferir a atualização do TSE (para 2026: Res. 23.758/2026 sobre fiscalização e auditoria);
- Confundir diplomação (ato da JE) com posse (na Câmara/Senado/Executivo);
- Ignorar as novas datas de posse da **EC 111/2021** (5 e 6 de janeiro, a partir dos eleitos em 2026).
