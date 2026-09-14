---
id: "4c65c10b-fc23-435a-b3a6-2bc1f71eb6e6"
name: "ai-governance-marco-regulatorio"
title: "Governança de IA e Marco Regulatório (PL 2.338/23 + RCVM + ANPD)"
category: "materia"
materia: "consultoria"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/consultoria/dados-privacidade-ia/ai-governance-marco-regulatorio.md"
triggers:
  - "inteligência artificial"
  - "governança de IA"
  - "AI governance"
  - "marco regulatório IA"
  - "PL 2338"
  - "sistemas autônomos"
  - "large language model"
  - "IA generativa"
  - "viés algorítmico"
description: "Governança de IA: PL 2.338/23 (aprovado no Senado em 12/2024, em tramitação na Câmara dos Deputados) + LGPD (Lei\n13.709/18) + RCVM 80 + Lei 14.478/22 + Lei 12.965/14 (Marco Civil\nInternet). Categorização de riscos, AI Act (UE), princípios OCDE,\ndue diligence em modelos, treinamento ético, explicabilidade,\nresponsabilidade civil, automated decision-making."
---

# Governança de IA e Marco Regulatório

## Marco normativo (BR)

- **PL 2.338/23** (Marco Legal da IA): aprovado no Senado em 12/2024; na Câmara dos Deputados, em Comissão Especial, sem votação em Plenário até meados de 2026 (não vigente): estrutura por risco;
- **LGPD (Lei 13.709/18)** art. 20: revisão de decisão automatizada;
- **Lei 12.965/14 (Marco Civil Internet)**;
- **Lei 14.478/22** (criptoativos): aplicabilidade a IA financeira;
- **CDC art. 4º VI**: educação e informação;
- **CC 186 + 927**: responsabilidade civil;
- **Lei 8.078 + 9.099**: relações consumo + responsabilidade objetiva;
- **CF 5º X, XII, LV**: privacidade + ampla defesa;
- **STF + STJ**: jurisprudência emergente (2025-2026).

## Marco internacional

- **EU AI Act** (Reg. UE 2024/1689): categorização de risco;
- **Brasil aderiu aos Princípios OCDE de IA** (Recommendation 2019);
- **UNESCO Recommendation on Ethics of AI** (2021);
- **NIST AI Risk Management Framework** (US);
- **GDPR + ePrivacy** (UE): aplicável a empresas BR com nexo UE.

## Categorização de risco (PL 2.338/23 + EU AI Act)

### IA de risco inaceitável (vedada)
- **Manipulação subliminar** prejudicial;
- **Vulnerabilidade explorada** (criança, idoso);
- **Pontuação social** discriminatória;
- **Identificação biométrica em tempo real** em espaço público (exceto exceções);
- **Inferência de emoções** em escola + local de trabalho;
- **Categorização biométrica** por raça, religião, orientação política/sexual;
- **Predição criminal** sem base em fatos individuais.

### IA de alto risco
- **Sistemas críticos**: saúde, transporte, justiça, fronteira, infraestrutura;
- **Decisões automatizadas relevantes**: crédito, emprego, educação, seguro, beneficio social;
- **Avaliação de risco** em justiça criminal;
- **Recursos humanos**: recrutamento + avaliação + promoção;
- **Identificação biométrica** com fins de identificação;
- **Operação de infraestrutura crítica**.

### IA de risco transparência
- **Chatbot + interação humana**: aviso obrigatório;
- **Conteúdo gerado por IA**: marca d'água + identificação;
- **Deepfake**: identificação obrigatória;
- **Sistema de personalização**: aviso ao usuário.

### IA de baixo risco
- **Recomendação de produtos** + filtros;
- **Tradução automática**;
- **OCR**;
- **Detecção de spam**;
- **Self-service** simples.

## Requisitos para IA de alto risco

### Pré-disponibilização
- **Documentação técnica** do sistema (PL 2.338 art. 17);
- **Avaliação de impacto algorítmico (AIA)**;
- **Avaliação de impacto à proteção de dados (DPIA: LGPD)**;
- **Treinamento + dados** auditáveis;
- **Mitigação de viés** + **testes de imparcialidade**;
- **Explicabilidade** + interpretabilidade;
- **Logs + auditoria**;
- **Gerenciamento de risco** ao longo do ciclo de vida;
- **Robustez** + cibersegurança;
- **Supervisão humana**.

### Durante a operação
- **Monitoramento contínuo** de desempenho + viés + erro;
- **Logs auditáveis** preservados;
- **Comunicação de incidente** ao regulador;
- **Direito de explicação** ao titular;
- **Direito de revisão** de decisão automatizada (LGPD art. 20; exigência de revisão por pessoa natural foi vetada);
- **Right to contest** decisão automatizada;
- **Reporte periódico** aos órgãos competentes.

## Governança interna

### Estrutura
- **Comitê de IA**: alta administração + jurídico + compliance + TI + ciência de dados + ética;
- **AI Officer / AI Risk Officer**: papel emergente;
- **Política de IA**: princípios + uso aceitável + vetos;
- **Processo de aprovação**: pré-deployment + monitoramento;
- **Treinamento**: anti-viés + ética + privacidade;
- **Avaliação contínua**: KPIs de fairness + accuracy + drift.

### Política de IA: conteúdo
- **Princípios**: transparência + explicabilidade + accountability + fairness + segurança + privacidade;
- **Casos vedados**: pontuação social, manipulação, vigilância massiva;
- **Casos restritos**: identificação biométrica, geração de conteúdo;
- **Processos de aprovação**: por categoria de risco;
- **Comunicação ao público**: divulgação de uso de IA;
- **Auditoria periódica**: anual mínimo;
- **Comunicação de incidente**.

## Avaliação de impacto algorítmico (AIA: PL 2.338)

- **Quando**: antes de implementar IA de alto risco;
- **Conteúdo**:
  - Descrição do sistema + propósito;
  - Stakeholders afetados;
  - Riscos identificados (viés, erro, dano);
  - Medidas de mitigação;
  - Plano de monitoramento;
  - Direitos dos afetados;
- **Documentação**: arquivada + disponível a regulador;
- **Atualização**: periódica e em mudança material.

## Responsabilidade civil

### Modelo brasileiro
- **CC 186 + 927**: responsabilidade subjetiva (regra geral);
- **CDC art. 14**: responsabilidade objetiva em consumo;
- **PL 2.338 art. 27** (proposta): objetiva para IA de alto risco; subjetiva para demais;
- **STF Temas 987 + 533** (2025): inconstitucionalidade parcial e progressiva do art. 19 do Marco Civil da Internet (responsabilização de plataformas por conteúdo de terceiros), parâmetro relevante para sistemas de IA de moderação/recomendação.

### Quem responde
- **Fornecedor do sistema** (criador);
- **Implementador** (quem usa);
- **Operador** (quem opera);
- **Cadeia de fornecimento** (modelos pré-treinados, datasets);
- **Open source**: licenças (MIT, Apache, BSD) afastam responsabilidade em geral; ML licenses (RAIL) restringem.

### Cláusulas contratuais
- **Indenidade** entre fornecedor e cliente;
- **Limitação de responsabilidade**: típica + ressalvas (dolo + sigilo + LGPD + anticorrupção);
- **Auditoria** do sistema;
- **Atualização** + bug fix obrigatórios;
- **SLA** + uptime + acuracidade;
- **Compliance** com regulação (UE AI Act se exportação a UE).

## LGPD + IA

### Pontos-chave
- **Base legal**: consentimento (art. 7 I) + interesse legítimo (IX) + execução de contrato (V);
- **Dados sensíveis** (art. 11): consentimento específico para treinamento;
- **DPIA** em sistema de alto risco;
- **Direito do titular** (art. 18): acesso + correção + eliminação;
- **Direito de revisão** (art. 20): decisão automatizada que afeta titular pode ser revisada;
- **Princípio da finalidade + minimização** + adequação;
- **Encarregado (DPO)**: papel ampliado em IA.

### Treinamento de modelos com dados pessoais
- **Anonimização** (art. 12) como saída preferida;
- **Pseudonimização** não é anonimização;
- **Web scraping** + dados públicos: base legal incerta (interesse legítimo discutível);
- **Dados de menores** (art. 14): exigência reforçada;
- **Cross-border**: cláusulas-padrão ANPD (Res. CD/ANPD 19/24).

## Setoriais

### Banco Central + CVM
- **RCVM 50/21**: PLD-FT no mercado de capitais (monitoramento automatizado);
- **Sandbox BACEN + CVM**: testes de IA;
- **Open Finance** (Res. 1/20): IA em PFM;
- **Robo-advisor**: registro CVM + suitability;
- **PLD-FT**: IA em detecção de fraude (Circular BCB 3.978).

### ANS (saúde suplementar)
- **IA em underwriting**: vedação a discriminação;
- **IA em diagnóstico**: responsabilidade médica;
- **Telemedicina** (Res. CFM 2.314): apoio à decisão admitido.

### CFM (saúde)
- **Res. CFM 2.314/22**: telemedicina;
- **IA em diagnóstico**: apoio + responsabilidade do médico;
- **Não autonomia plena**: decisão final humana.

### Justiça
- **CNJ Res. 615/2025** (atualiza a Res. 332/20): marco do uso de IA no Judiciário: supervisão humana obrigatória + classificação de risco + vedação de decisão judicial automatizada sem supervisão + Plataforma Sinapses;
- **Decisão judicial**: IA como apoio; decisão final humana;
- **PJe + IA**: triagem + suporte (não decisão).

## Cláusulas em contratos de IA

### Fornecedor → Cliente
- **Performance specifications**: acuracidade + recall + precisão + F1;
- **Treinamento + datasets**: origem + licença + IP;
- **Atualização**: política + frequência;
- **Bias mitigation**: programa + reporte;
- **Auditoria**: direito + frequência;
- **SLA**: uptime + suporte + correção;
- **Liability**: cap + ressalvas;
- **Open source**: declaração + compliance;
- **Cyber security**: padrões (ISO 27001 + NIST);
- **Compliance**: LGPD + EU AI Act + outros;
- **Termination**: por descumprimento + step-out.

### Cliente → Fornecedor
- **Auditoria** + acesso;
- **Direito de uso ético**;
- **Mitigação de viés** garantida;
- **Documentação técnica**;
- **Cobertura** em ações regulatórias.

## Foundation models + open source

- **LLaMA** (Meta) + **Mistral** + **Falcon**: licenças abertas;
- **GPT-4o** (OpenAI) + **Claude** (Anthropic) + **Gemini** (Google): proprietários;
- **Risco open source**: contaminação + licenças (RAIL + CC + OpenRAIL);
- **Fine-tuning**: dados próprios + permissão de uso;
- **Hosting**: local + cloud + nuvens regionais;
- **Sovereignty**: regulação de dados em jurisdição.

## EU AI Act + extraterritorialidade

- **Exportação para UE**: subsidiária brasileira deve cumprir;
- **Categorização** + conformidade;
- **Marcação CE** em sistemas;
- **Sanção**: até 7% do faturamento global ou €35 milhões;
- **Vigência escalonada**: 2025-2027.

## Erros a evitar

- **IA de alto risco** sem AIA + DPIA: descumpre exigência prevista no PL 2.338/23 (não vigente); a obrigação exigível decorre da LGPD (art. 20; RIPD quando exigida pela ANPD, art. 38);
- **Sistema sem explicabilidade**: dificulta defesa + revisão (art. 20 LGPD);
- **Decisão automatizada** sem canal de revisão: viola LGPD art. 20;
- **Viés algorítmico** não monitorado: discriminação (CC + CDC);
- **Dados de treinamento** sem base legal LGPD: multa;
- **Web scraping** sem documentação de base legal: interesse legítimo questionado;
- **Chatbot** sem aviso de IA: viola transparência;
- **Deepfake** sem identificação: risco de dano (CC 186 + 927); exigência específica de identificação prevista no PL 2.338 (não vigente);
- **Open source RAIL** ignorada: descumprimento de licença restritiva;
- **EU AI Act** ignorado em export: sanção UE;
- **Acordo com fornecedor** sem auditoria + sem KPI: contrato vazio;
- **DPO** sem briefing sobre IA: governança fragilizada;
- **Treinamento dos colaboradores** ausente: uso inadequado;
- **Logs + auditoria** ausentes: inviabiliza defesa em incidente;
- **Sandbox** sem critérios definidos: descontinuação;
- **Documentação técnica** desatualizada: exigência prevista no PL 2.338 art. 17 (não vigente; boa prática de governança);
- **Comitê de IA** ausente em empresa de impacto material: falha de governança;
- **Reportes públicos** sobre uso de IA: greenwashing + reputational;
- **Robo-advisor** sem registro CVM: descumprimento;
- **Médico** delegando decisão a IA: viola CFM + responsabilidade médica.
