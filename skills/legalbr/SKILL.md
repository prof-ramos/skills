---
name: legalbr
description: "Hub unificado do ecossistema LegalSkillsBR com 2.149 habilidades jurídicas brasileiras: 299 minutas e peças processuais (petições iniciais, recursos, contestações, decisões) e 1.850 teses de mérito em 25 ramos jurídicos (Civil, Penal, Tributário, Trabalho, Constitucional, Administrativo, etc.), incluindo jurisprudência consolidada do STF e STJ, súmulas vinculantes, repercussão geral e repetitivos."
license: "MIT"
metadata:
  author: "prof-ramos"
  version: "1.0.0"
  categories:
    - "legal"
    - "brazilian-law"
    - "advocacia"
---

# LegalSkillsBR — Hub Unificado de Habilidades Jurídicas Brasileiras

O **LegalSkillsBR** é o maior acervo estruturado de habilidades jurídicas para agentes de inteligência artificial voltado ao Direito brasileiro, contendo **2.149 habilidades especializadas** divididas entre **Formas** (peças processuais e minutas contratuais) e **Matérias** (teses de mérito e jurisprudência qualificada).

---

## 🏛️ Arquitetura do Acervo

O ecossistema divide a prática forense em duas camadas modulares e combináveis:

```
legalbr/
├── SKILL.md                          # Este Hub Unificado
├── README.md                         # Documentação técnica e taxonomia
├── forma/                            # 299 minutas de peças processuais e minutas
│   ├── acao-anulatoria-debito-fiscal/
│   ├── apelacao-civel/
│   ├── contestacao-civel/
│   ├── habeas-corpus/
│   ├── peticao-inicial-civel/
│   └── ...
└── materia/                          # 1.850 teses de mérito por área jurídica
    ├── administrativo/               # 214 teses (concursos, licitações, improbidade)
    ├── ambiental/                    # 32 teses (licenciamento, multas, responsabilidade)
    ├── bancario/                     # 47 teses (juros, CDC, contratos bancários)
    ├── civil/                        # 66 teses (obrigações, posse, propriedade, responsabilidade)
    ├── constitucional/               # 60 teses (controle de constitucionalidade, direitos fundamentais)
    ├── consultoria/                  # 59 teses (compliance, governança, pareceres)
    ├── consumidor/                   # 106 teses (práticas abusivas, vícios, superendividamento)
    ├── contratos/                    # 59 teses (teoria geral, resolução, cláusulas específicas)
    ├── digital-dados/                # 27 teses (LGPD, Marco Civil, crimes cibernéticos)
    ├── diversidade-dh/               # 26 teses (direitos humanos, cotas, inclusão)
    ├── eleitoral/                    # 27 teses (registro de candidatura, propaganda, inelegibilidade)
    ├── empresarial/                  # 43 teses (títulos de crédito, falência, recuperação)
    ├── familia-sucessoes/            # 39 teses (alimentos, divórcio, inventário, partilha)
    ├── imobiliario/                  # 47 teses (locação, usucapião, condomínio, incorporação)
    ├── internacional/                # 18 teses (extradição, tratados, cooperação jurídica)
    ├── militar/                      # 5 teses (crimes militares, hierarquia e disciplina)
    ├── penal/                        # 166 teses (dosimetria, crimes em espécie, tipicidade)
    ├── previdenciario/               # 74 teses (RGPS, RPPS, benefícios por incapacidade)
    ├── processo-civil/               # 164 teses (tutelas provisórias, recursos, execução, CPC)
    ├── processo-penal/               # 120 teses (nulidades, júri, provas, prisão preventiva)
    ├── regulatorio/                  # 14 teses (agências reguladoras, concessões)
    ├── saude/                        # 37 teses (SUS, fornecimento de medicamentos, planos de saúde)
    ├── societario/                   # 26 teses (dissolução societária, M&A, acordos de sócios)
    ├── trabalho/                     # 128 teses (horas extras, rescisão, dano moral, terceirização)
    └── tributario/                   # 246 teses (ICMS, IRPJ, PIS/COFINS, execução fiscal, Simples)
```

---

## 🎯 Quando e Como Ativar

Ative ou consulte esta habilidade quando o usuário solicitar:
* Elaboração ou revisão de **peças processuais brasileiras** (petições iniciais, defesas, contestações, recursos ordinários, apelações, agravos, embargos de declaração, habeas corpus, mandados de segurança, memoriais ou alegações finais).
* Estruturação de **contratos, termos de ajustamento de conduta (TAC), pareceres jurídicos ou despachos**.
* Levantamento de **teses jurídicas com fundamentação em precedentes qualificados** (Súmulas Vinculantes do STF, Súmulas do STJ/TST, Temas de Repercussão Geral do STF e Recursos Repetitivos do STJ).
* Análise de compatibilidade normativa sob as leis brasileiras vigentes (CPC/2015, CPP, CLT, Código Civil, Código Penal, CTN, CDC, Lei 14.133/2021, LGPD, etc.).

---

## 🔄 Fluxo Operacional Recomendado para o Agente

Ao atuar em uma tarefa jurídica, componha a resposta unindo **Forma** + **Matéria**:

### 1. Seleção da Forma (Estrutura Processual)
1. Localize a peça adequada em `legalbr/forma/<slug>/SKILL.md`.
2. Observe os requisitos formais de admissibilidade:
   - Competência do juízo de endereçamento.
   - Qualificação completa das partes (art. 319, II do CPC).
   - Indicação de opção por conciliação/mediação (art. 319, VII do CPC).
   - Valor da causa devidamente calculado ou estimado (arts. 291-293 do CPC).
   - Pedidos claros, certos e determinados, com cominações de estilo (art. 322 do CPC).

### 2. Seleção das Matérias (Mérito e Teses Aplicáveis)
1. Busque nos ramos pertinentes de `legalbr/materia/<ramo>/<slug>/SKILL.md` os argumentos doutrinários e legais.
2. Incorpore a jurisprudência vinculante:
   - **STF:** Temas com Repercussão Geral fixada e Súmulas Vinculantes.
   - **STJ:** Temas Repetitivos (arts. 1.036 a 1.041 do CPC).
   - Observar a modulação temporal de efeitos de teses tributárias e previdenciárias.

### 3. Síntese e Redação Forense
- Redigir em vernáculo formal, sóbrio, objetivo e persuasivo.
- Evitar adjetivações vazias; focar na subsunção factual à norma jurídica e na aplicação do precedente qualificado ao caso concreto (art. 489, §1º do CPC).

---

## 📦 Instalação e Uso via CLI

### Instalação via `skills` CLI:
```bash
# Instalar este Hub Unificado:
npx skills add prof-ramos/skills --full-depth --skill legalbr

# Listar todas as 2.149 habilidades jurídicas do acervo:
npx skills add prof-ramos/skills --full-depth --list

# Instalar uma forma específica (ex: Ação de Alimentos):
npx skills add prof-ramos/skills --full-depth --skill acao-alimentos

# Instalar uma tese específica de matéria (ex: ICMS na base do PIS/COFINS - Tema 69):
npx skills add prof-ramos/skills --full-depth --skill tese-seculo-exclusao-icms-pis-cofins-tema-69
```
