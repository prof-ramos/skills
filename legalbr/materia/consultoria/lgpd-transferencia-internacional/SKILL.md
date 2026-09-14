---
id: "1de0ce31-d8b2-4f8f-8d34-6ed9365df930"
name: "lgpd-transferencia-internacional"
title: "LGPD: Transferência Internacional de Dados"
category: "materia"
materia: "consultoria"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/consultoria/dados-privacidade-ia/lgpd-transferencia-internacional.md"
triggers:
  - "transferência internacional"
  - "cross-border data"
  - "SCC LGPD"
  - "cláusulas-padrão"
  - "decisão de adequação"
  - "BCR"
  - "GDPR adequacy"
  - "Schrems"
description: "Transferência internacional de dados pessoais (LGPD art. 33-36\n+ Resolução ANPD CD 19/2024): hipóteses (decisão de adequação,\ncláusulas-padrão SCC, BCR, contrato, consentimento, cooperação\ninternacional), data residency, adequação Brasil-UE (Res. CD/ANPD\n32/2026, reconhecimento mútuo), Schrems II + risk assessment,\nhierarchical structures (grupos econômicos) e fluxos comuns\n(SaaS + cloud + intercompany)."
---

# LGPD: Transferência Internacional

## Quando é transferência internacional?

- **Fluxo de dados** para fora do território nacional;
- **Acesso remoto** por agente estrangeiro (operador em outro país);
- **Hospedagem** em servidor fora do Brasil;
- **Intercompany sharing** com matriz/subsidiária estrangeira;
- **Backup** em cloud regional/global;
- **Devolução** ao final também é transferência.

## Hipóteses (LGPD art. 33)

| | Conteúdo |
|---|---|
| **I. Adequação** | País com nível de proteção adequado, conforme ANPD |
| **II. Garantias específicas** | SCC, BCR, certificações, códigos de conduta |
| **III. Cooperação internacional** | Entre órgãos de inteligência/investigação |
| **IV. Proteção da vida** | Do titular ou terceiro |
| **V. Autoridade nacional** | Autorização |
| **VI. Compromissos assumidos em acordo de cooperação internacional** | |
| **VII. Execução de política pública** | Pelo Poder Público |
| **VIII. Consentimento específico** | Com informação destacada sobre transferência |
| **IX. Cumprimento de obrigação legal** | Pelo controlador |
| **X. Execução de contrato** | Em que titular é parte |
| **XI. Exercício regular de direito** | Em processo |

## Resolução ANPD CD 19/2024 (SCC + cláusulas-padrão)

- **Cláusulas-padrão contratuais publicadas** (anexo ao Regulamento de Transferências Internacionais, Res. CD 19/24); contratos anteriores tiveram prazo de adequação;
- **Cláusulas-padrão ANPD** terão presunção de adequação;
- **GDPR SCC** (Decisão UE 2021/914) podem ser aceitas com adaptações;
- **BCR** (Binding Corporate Rules) aplicáveis a grupos econômicos com aprovação ANPD.

## Decisão de adequação

- **ANPD avalia** país por:
  - Estado de direito + respeito a DH;
  - Legislação geral + setorial de proteção de dados;
  - Autoridade independente de supervisão;
  - Compromissos internacionais;
  - Garantias dos direitos do titular;
- **União Europeia reconhecida** como detentora de nível adequado de proteção (Res. CD/ANPD 32/2026, art. 33 I da LGPD): fluxos Brasil-UE/EEE dispensam cláusulas-padrão e demais mecanismos;
- **Exclusão**: transferências para fins exclusivos de segurança pública, defesa, segurança do Estado e persecução penal ficam fora do reconhecimento; reavaliação periódica prevista;
- **Demais países**: sem decisão de adequação publicada; usar garantias específicas (SCC, BCR).

## GDPR adequacy (UE-BR)

- **Reconhecimento mútuo em 2026**: a Comissão Europeia adotou decisão de adequação do Brasil de forma coordenada com a Res. CD/ANPD 32/2026 (que reconheceu a UE): fluxos UE-Brasil e Brasil-UE dispensam SCC/BCR nas hipóteses cobertas;
- **Fora do escopo da adequação** (ex.: persecução penal) ou para países terceiros: empresas seguem usando **SCC UE** ou **BCR**;
- **Schrems II** (CJUE 2020, C-311/18): SCC + risk assessment + supplementary measures continuam relevantes para outros destinos.

## BCR (Binding Corporate Rules)

- **Regras vinculantes intragrupo**;
- **Aprovação por ANPD** (procedimento em desenvolvimento);
- **GDPR BCR** podem ser ponto de partida;
- **Compromissos**: tratamento conforme LGPD + direitos do titular + accountability;
- **Estrutura**: controlador BR + operadores intragrupo no exterior;
- **Vantagem**: flexibilidade para fluxos globais.

## SCC: cláusulas contratuais padrão

### Conteúdo típico
- Identificação das partes (controlador + operador);
- Categorias de dados;
- Categorias de titulares;
- Finalidades;
- Direitos do titular (atendimento conjunto);
- Medidas técnicas + organizacionais;
- Sub-processamento;
- Auditoria;
- Notificação de incidente;
- Lei aplicável + foro;
- Responsabilidade + indemnidade;
- Devolução/destruição.

### Limitações
- Não substituem **assessment de risco país** (Schrems II);
- **Lei do país receptor** pode prevalecer (especialmente acesso governamental);
- **Supplementary measures**: criptografia, pseudonimização, contratos adicionais.

## Risk assessment (Transfer Impact Assessment, TIA)

### Inspirado em Schrems II
- **Lei do país receptor** (acesso governamental, intel, lawful intercept);
- **Práticas das autoridades** (Snowden disclosures, FISA 702);
- **Mecanismos de redress** para titulares;
- **Medidas suplementares** se necessário (criptografia E2E, pseudonimização);
- **Documentação** do assessment para defesa em fiscalização.

## Países sensíveis (high risk)

- **USA**: FISA 702 + EO 12333: Schrems II derrubou Privacy Shield; novo EU-US Data Privacy Framework (2023);
- **China**: Lei de Segurança Nacional + Cybersecurity Law: alto risco;
- **Rússia**: Lei de Soberania Digital + sanctions;
- **Índia**: DPDP Act 2023 (recente) + acesso governamental;
- **UAE**: relaxando, mas check setorial;
- **Países com sanções OFAC/EU/UN**: vedação total.

## Mecanismos comuns

### SaaS / Cloud
- **DPA** + SCC (ANPD ou GDPR) + assessment;
- **Data Processing Addendum** padrão dos provedores (AWS, Google, Microsoft);
- **Sub-processor list** + objeção;
- **Notificação de incidente**;
- **Data residency**: opção de armazenamento regional (cuidado: pode não bastar se acesso de outras regiões);
- **Encryption** + key management.

### Intercompany (grupos)
- **BCR** preferido (única aprovação);
- **DPA intragrupo** + SCC se sem BCR;
- **Política de privacidade global** harmonizada;
- **Encarregado regional** + global DPO;
- **Auditoria interna**.

### M&A / DD
- **Sharing de dados** sob NDA + cláusulas LGPD;
- **Anonimização** quando possível;
- **Data room** em jurisdição compatível;
- **Pós-closing**: integração + atualização de políticas.

## Data localization

- **LGPD não exige** localização (regra geral);
- **Setoriais**:
  - **Saúde**: discussão (não obrigatório, mas pratica);
  - **Financeiro** (BCB): localização recomendada + outsourcing aprovado (Resolução BCB 4.893);
  - **Gov/Dados sensíveis**: discussão;
- **Cloud providers** oferecem regiões BR (AWS São Paulo, Google São Paulo, Azure São Paulo).

## Cláusulas contratuais: checklist

- [ ] **Identification das partes** (controlador + operador);
- [ ] **Escopo + finalidade** restritos;
- [ ] **Bases legais** da transferência (LGPD art. 33);
- [ ] **Mecanismo de transferência** (adequação, SCC, BCR);
- [ ] **Subprocessors** (lista + aviso + objeção);
- [ ] **Direitos do titular** (atendimento conjunto);
- [ ] **Medidas de segurança** específicas;
- [ ] **Notificação de incidente** (prazo);
- [ ] **Auditoria** pelo controlador;
- [ ] **Devolução/destruição** ao final;
- [ ] **Indenidade** + cap;
- [ ] **Lei aplicável + foro**;
- [ ] **Encarregado** das partes;
- [ ] **Atualização** periódica.

## Erros a evitar

- **Cloud SaaS** sem identificar transferência (assumir "BR" sem checar regiões);
- **DPA padrão do provedor** sem revisão LGPD;
- **GDPR SCC** sem adaptações BR (LGPD art. 33);
- **BCR** sem aprovação ANPD (verificar procedimento na Res. CD 19/24);
- **TIA** ausente em país sensível (Schrems II analógico);
- **Decisão de adequação** assumida para país sem reconhecimento publicado (fora da UE, verificar lista da ANPD);
- **Consentimento como base** padrão (frágil: revogável);
- **Subprocessing** sem aviso + objeção;
- **Notificação de incidente** sem prazo definido;
- **Data residency** assumido com cloud (acesso de outras regiões existe);
- **Sub-processor list** desatualizada (cliente surpreendido);
- **Adequação Brasil-UE** invocada fora do escopo (segurança pública, defesa e persecução penal ficam de fora da Res. CD/ANPD 32/2026);
- **Backup global** sem mapear;
- **Intercompany sharing** sem DPA (matriz × subsidiária);
- **Encryption** sem segregação de chaves (provedor acessa);
- **Auditoria** sem direito real (SOC 2 report como única evidência);
- **OFAC/EU sanctions** ignoradas em destino;
- **Lei do país receptor** ignorada (acesso governamental imprevisto);
- **Política global** sem addendum BR (LGPD específico ignorado);
- **DPO global** sem encarregado BR (LGPD art. 41: pessoa identificável);
- **Direito do titular** com canal apenas estrangeiro (idioma + jurisdição);
- **Devolução** sem confirmação certificada;
- **Cláusulas-padrão ANPD** ignoradas quando publicadas (Resolução CD 19/2024).
