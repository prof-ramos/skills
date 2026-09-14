---
id: "4295ae77-e7c8-4c42-8ce7-2235dc10781b"
name: "lgpd-instituicoes-financeiras"
title: "LGPD em Instituições Financeiras + Segurança Cibernética (Res. CMN 4.893/21)"
category: "materia"
materia: "bancario"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/bancario/lgpd-instituicoes-financeiras.md"
triggers:
  - "LGPD bancos"
  - "Lei 13.709"
  - "Resolução CMN 4.893"
  - "Resolução CMN 4.658"
  - "segurança cibernética banco"
  - "PSO política segurança operacional"
  - "incidente vazamento dados"
  - "LC 105"
  - "sigilo bancário"
  - "ANPD bancos"
  - "encarregado dados banco"
  - "DPO instituição financeira"
  - "SCR LGPD"
  - "portabilidade dados bancários"
description: "LGPD aplicada a IFs: Lei 13.709/18 + Res. CMN 4.893/21 (segurança\ncibernética e contratação de processamento em nuvem, que revogou a\nRes. CMN 4.658/18; atualizada pela Res. CMN 5.274/25); base legal\nart. 7 V (execução de contrato) + X (legítimo interesse); sigilo\nbancário LC 105/01 mantido como dever específico; competência\nconcorrente ANPD + BCB; comunicação tempestiva de incidentes\nrelevantes ao BCB e à ANPD (3 dias úteis, Reg. ANPD 15/2024)."
---

# LGPD em Instituições Financeiras

## Base normativa

| Norma | Conteúdo |
|---|---|
| **Lei 13.709/18 (LGPD)** | Marco geral de proteção de dados pessoais |
| **LC 105/01** | Sigilo das operações bancárias (lex specialis sobre dados financeiros) |
| **Res. CMN 4.893/21** | **Política de segurança cibernética** + contratação de processamento e armazenamento de dados em nuvem (revogou as Res. 4.658/18 e 4.752/19; atualizada pela Res. CMN 5.274/25) |
| **Res. BCB 85/21** | Política de segurança cibernética das **instituições de pagamento** (equivalente da 4.893 para IPs; atualizada pela Res. BCB 538/25) |
| **Termo de Cooperação ANPD-BCB (2021)** | Competência concorrente: BCB regula, ANPD fiscaliza |
| **Res. CMN 4.949/21** | Princípios e procedimentos no relacionamento com clientes (inclui transparência sobre dados) |
| **Res. Conj. CMN/BCB 1/2020** | Open Finance: compartilhamento por consentimento |
| **Súm. 297 STJ** | CDC às IFs (interage com LGPD) |
| **CF arts. 5 X + XII + LXXII** | Inviolabilidade da intimidade + sigilo de dados + habeas data |

## Bases legais aplicáveis a IFs

| Base | Hipótese típica |
|---|---|
| **Art. 7 V LGPD** | Execução de contrato: operações bancárias contratadas (conta, crédito, cartão) |
| **Art. 7 II + Art. 11 II "a"** | Consentimento: quando o tratamento extrapolar a execução (marketing, perfilamento, compartilhamento com parceiros) |
| **Art. 7 X** | Legítimo interesse: prevenção à fraude, modelos antifraude, monitoramento PLD/FT |
| **Art. 7 VI** | Cumprimento de obrigação legal: SCR, COAF, IRF (RFB), CCS-BCB |
| **Art. 7 IX** | Tutela de direitos: análise de crédito ressalvada |
| Art. 11 (dados sensíveis) | Consentimento qualificado para biometria, saúde, religião (raramente coletados por IF) |

## Sigilo bancário (LC 105/01) e LGPD

| | Conteúdo |
|---|---|
| Aplicação simultânea | LGPD + LC 105/01 incidem cumulativamente |
| Sigilo absoluto entre particulares | Mantido: terceiros não acessam sem autorização do cliente |
| Acesso por autoridade | LC 105 art. 6 (RFB direta: STF RE 601.314, Tema 225) + art. 5 (ordem judicial) |
| ANPD | Acesso a dados restrito à investigação de incidentes; não desfaz sigilo bancário |
| Open Finance | Compartilhamento com consentimento (afastamento explícito do sigilo pelo titular) |

## Encarregado (DPO) e governança

| | Conteúdo |
|---|---|
| Encarregado | Obrigatório (art. 41 LGPD); pode ser interno ou terceirizado |
| Diretor responsável | Res. CMN 4.893: diretor responsável pela política de segurança cibernética |
| Comitê | Composição estabelecida pela IF para tratar de incidentes |
| Programa de governança | Análise de impacto (LIA) + DPIA + auditoria periódica |
| Política de retenção | Definir prazos por finalidade: operação principal vs. defesa em juízo (até prescrição) |

## Direitos do titular (art. 18 LGPD)

| Direito | Aplicação a IFs |
|---|---|
| **Confirmação + acesso** | Cliente pode pedir extrato de dados; IF responde em até 15 dias |
| **Correção** | Atualização cadastral imediata |
| **Anonimização/eliminação** | Ressalva da obrigação legal (LC 105: retenção de 5+ anos) e do interesse público (PLD/FT) |
| **Portabilidade** | Open Finance + portabilidade de crédito (Res. CMN 5.057/22) |
| **Informação sobre compartilhamento** | Direito de saber com quem dados foram compartilhados |
| **Revogação do consentimento** | A qualquer tempo, com efeito ex nunc |
| **Decisões automatizadas** | Cliente pode pedir revisão (art. 20 LGPD): relevante em análise de crédito, score, antifraude |

## Score de crédito

| | Conteúdo |
|---|---|
| Cadastro Positivo (Lei 12.414/11 atualizada Lei 14.181/21) | Inclusão automática salvo opt-out |
| Score | Permitido: STJ Tema 710 (REsp 1.419.697), prática comercial lícita autorizada pela Lei 12.414/2011 |
| Direito do titular | Acesso aos critérios e fontes dos dados considerados (não ao algoritmo proprietário): Tema 710 STJ |
| Transparência | Lei 12.414 art. 3 §1: fontes e finalidade |
| Negação de crédito | Cliente tem direito à motivação da recusa (Lei 12.414 + LGPD 20) |

## Compartilhamento com terceiros

| Cenário | Tratamento |
|---|---|
| **Empresas do mesmo conglomerado** | Compartilhamento permitido com consentimento ou contrato |
| **Birôs (Serasa, Boa Vista)** | Lei 12.414 + LGPD art. 7 X (interesse legítimo) |
| **Cessão de carteira (FIDC, securitizadora)** | Cessão de crédito implica cessão dos dados necessários (CC 287) |
| **Operadora de cartão** | Compartilhamento operacional (legítimo interesse) |
| **Parceiros comerciais** | Exige consentimento específico |
| **Transferência internacional** | Art. 33 LGPD: só para países adequados (decisão ANPD) ou com garantias contratuais |

## Segurança cibernética (Res. CMN 4.893/21)

| Componente | Conteúdo |
|---|---|
| **PSO (Política de Segurança Operacional)** | Aprovada pelo conselho/diretoria |
| **Plano de ação e resposta a incidentes** | Inclui cenários (DDoS, ransomware, fraude interna, vazamento) |
| **Testes** | Pentest periódico + simulações |
| **Contratação de nuvem** | Devida diligência + cláusulas mínimas (capacidade técnica, residência de dados, auditoria); comunicação da contratação relevante ao BCB em até 10 dias (Res. CMN 4.893) |
| **Comunicação ao BCB** | Comunicação **tempestiva** de incidentes relevantes, conforme a regulamentação do BCB; relatório anual do plano de resposta a incidentes à administração |
| Reporte cumulativo | LGPD: à ANPD em prazo razoável + ao titular afetado |
| Segregação | Ambientes (produção, homologação, desenvolvimento); princípio do menor privilégio |
| **Diretor responsável** | Estatutário, perante o BCB |

## Incidentes: tratamento

| Etapa | Conteúdo |
|---|---|
| 1. Identificação + contenção | Resposta imediata (CSIRT) |
| 2. Avaliação de impacto | Quantidade de titulares + categoria de dados + risco |
| 3. Notificação ao BCB (Res. CMN 4.893) | Comunicação **tempestiva** se relevante, conforme regulamentação do BCB |
| 4. Notificação à ANPD (LGPD 48) | Prazo razoável; entendimento ANPD: 3 dias úteis (Reg. 15/2024) |
| 5. Notificação aos titulares afetados | Sempre que houver risco relevante (art. 48 LGPD) |
| 6. Forense + medidas corretivas | Mantidas até remediação |
| 7. Documentação | Conservada para auditoria |

## Sanções

| Autoridade | Sanções |
|---|---|
| **ANPD (LGPD 52)** | Advertência + multa simples (até 2% do faturamento, máx R$ 50 mi por infração) + multa diária + publicização + bloqueio + eliminação |
| **BCB (Lei 13.506/17)** | Advertência + multa (até R$ 2 bi ou 0,5% do PR) + inabilitação de diretores + cassação de autorização |
| **CDC arts. 12, 14, 25** | Responsabilidade civil objetiva |
| **CC arts. 186, 927** | Responsabilidade subjetiva (atos do encarregado) |

## STJ: jurisprudência

| | Conteúdo |
|---|---|
| **Tema 710** (REsp 1.419.697) | Score de crédito: desnecessário o consentimento do consumidor consultado; direito a esclarecimentos sobre fontes e critérios; respeito à privacidade e à máxima transparência (CDC + Lei 12.414/2011) |
| **Súm. 359 STJ** | Cabe ao órgão mantenedor do cadastro de proteção ao crédito a notificação do devedor antes de proceder à inscrição |
| **Tema 922 STJ** | A inscrição indevida comandada pelo credor, quando preexistente legítima anotação, não enseja indenização por dano moral, ressalvado o direito ao cancelamento (inteligência da Súm. 385) |
| **Súm. 385 STJ** | Negativação preexistente legítima afasta dano moral por nova negativação indevida |
| **Súm. 548 STJ** | Quitação ≠ exclusão automática: credor deve providenciar baixa em 5 dias úteis |
| **Súm. 479** | Fortuito interno em fraude: responsabilidade objetiva |
| REsp 2.013.929 | Vazamento de dados: dano moral exige prova do efetivo prejuízo (dano in re ipsa só em hipóteses graves) |

## Erros a evitar

- Coletar dados além do necessário à **execução do contrato** sem base legal (art. 6 III LGPD: necessidade);
- Aplicar **consentimento** quando a base correta é **execução de contrato** ou **obrigação legal**: risco de revogação indevida;
- Esquecer a **comunicação tempestiva de incidentes relevantes ao BCB** (Res. CMN 4.893);
- Tratar a comunicação **ANPD** como facultativa em vazamento relevante (art. 48 LGPD);
- Compartilhar com terceiros **fora do mesmo conglomerado** sem consentimento específico ou outra base legal;
- Negar acesso aos critérios do score: o Tema 710 STJ assegura o direito;
- Eliminar dados quando há **obrigação legal de retenção** (5 anos LC 105 + 5 anos COAF + tempo de prescrição da pretensão);
- Considerar **sigilo bancário** afastado por consentimento genérico: exige autorização específica;
- Aplicar **transferência internacional** sem garantia adequada (art. 33);
- Considerar **dados pessoais sensíveis** sob base legal de contrato: exige consentimento qualificado (art. 11 II "a");
- Esquecer **PSO** estatutário + **diretor responsável** (Res. CMN 4.893);
- Acionar **ação coletiva LGPD** sem demonstrar nexo entre incidente e dano efetivo (REsp 2.013.929);
- Tratar **Open Finance** como exceção ao sigilo: é compartilhamento por consentimento (não relativiza LC 105);
- Confundir **ANPD** com **BCB**: competências concorrentes, reportes cumulativos.
