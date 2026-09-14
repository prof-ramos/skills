---
id: "c9f7badf-bb70-4452-95df-aba23a6beae2"
name: "lgpd-mapeamento-dados-ripd"
title: "LGPD: Mapeamento de Dados (ROPA) e RIPD/DPIA"
category: "materia"
materia: "consultoria"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/consultoria/dados-privacidade-ia/lgpd-mapeamento-dados-ripd.md"
triggers:
  - "mapeamento de dados"
  - "inventário de dados"
  - "ROPA"
  - "record of processing activities"
  - "RIPD"
  - "DPIA"
  - "relatório de impacto"
  - "data mapping"
description: "Mapeamento de dados (ROPA, Record of Processing Activities) e\nRelatório de Impacto à Proteção de Dados (RIPD/DPIA) sob LGPD\n(Lei 13.709/2018) + Resoluções ANPD (CD 02/2022, agentes de\npequeno porte, CD 18/2024, encarregado/DPO, CD 04/2023,\ndosimetria/sanções, CD 15/2024, incidentes):\ninventário (finalidade, base legal, dados, titulares,\ncompartilhamento, retenção, transferência internacional),\nmatriz de risco e medidas mitigantes."
---

# LGPD: Mapeamento (ROPA) e RIPD/DPIA

## Bases legais

- **Lei 13.709/2018 (LGPD)**;
- **ANPD Resoluções**:
  - **CD 02/2022**: agentes de pequeno porte;
  - **CD 18/2024**: atuação do encarregado (DPO);
  - **CD 04/2023**: dosimetria + aplicação de sanções administrativas;
  - **CD 15/2024**: comunicação de incidentes;
  - **CD 19/2024**: regulamento de transferência internacional + cláusulas-padrão (SCC);
- **Diretiva UE GDPR** (subsidiária em filiais);
- **CC 421 + 422 + 187** (boa-fé e abuso de direito);
- **CDC** (relação de consumo correlata).

## ROPA (Record of Processing Activities)

### Conteúdo mínimo (LGPD art. 37 + boas práticas)
1. **Atividade de tratamento** (descrição);
2. **Finalidade** específica;
3. **Base legal** (LGPD art. 7, PF; art. 11, sensível);
4. **Categorias de dados** (cadastro, transacional, sensível);
5. **Categorias de titulares** (clientes, empregados, fornecedores, prospects);
6. **Origem dos dados** (próprio titular × terceiros);
7. **Volume** estimado;
8. **Compartilhamento** com terceiros (operadores + co-controladores);
9. **Transferência internacional**;
10. **Tempo de retenção** + critério de eliminação;
11. **Medidas de segurança**;
12. **Encarregado responsável**.

### Estrutura
- **Por unidade de negócio + área**;
- **Sistema de informação** correlato;
- **Atualização** anual + ad hoc em mudança material;
- **Documentação acessível** ao DPO + ANPD em fiscalização.

## Bases legais de tratamento (LGPD art. 7)

| | Conteúdo |
|---|---|
| **I. Consentimento** | Livre, informado, inequívoco |
| **II. Cumprimento de obrigação legal** | Lei ou regulamento |
| **III. Execução de políticas públicas** | Pelo Poder Público |
| **IV. Estudos por órgão de pesquisa** | Anonimização preferida |
| **V. Execução de contrato** | Ou procedimentos preliminares |
| **VI. Exercício regular de direito** | Processo judicial, administrativo, arbitral |
| **VII. Proteção da vida** | Do titular ou terceiro |
| **VIII. Tutela da saúde** | Procedimento por profissionais |
| **IX. Legítimo interesse** | Quando finalidades legítimas + ponderação |
| **X. Proteção do crédito** | Lei 12.414 |

## Dados sensíveis (art. 11)

- **Origem racial ou étnica**;
- **Convicção religiosa**;
- **Opinião política**;
- **Filiação a sindicato + organização religiosa/política**;
- **Dado referente à saúde + vida sexual**;
- **Dado genético + biométrico** vinculado a pessoa natural.

### Bases (art. 11)
- **Consentimento específico**;
- **Cumprimento de obrigação legal**;
- **Execução de políticas públicas**;
- **Estudos por órgão de pesquisa**;
- **Exercício regular de direito**;
- **Proteção da vida**;
- **Tutela da saúde por profissionais**;
- **Prevenção à fraude** + segurança do titular (sem consentimento permitido): exceção controvertida.

## Dados de crianças e adolescentes (art. 14)

- **Consentimento específico do responsável legal**;
- **Melhor interesse**;
- **Sem condicionamento de participação** em jogos/aplicativos;
- **Coleta mínima** + transparência;
- **STF + STJ** crescendo em rigor.

## RIPD / DPIA (LGPD art. 38)

### Quando obrigatório
- ANPD pode exigir (art. 38);
- **Boas práticas** + GDPR Art. 35:
  - Tratamento **em larga escala**;
  - Dados **sensíveis** em larga escala;
  - **Monitoramento sistemático**;
  - **Decisões automatizadas** com efeitos significativos (LGPD art. 20);
  - **Crianças e adolescentes**;
  - **Novas tecnologias** (biometria, IA);
  - **Transferência internacional** para jurisdições sem decisão de adequação;
  - **Dados de identificação** em larga escala.

### Conteúdo
1. **Descrição** do tratamento + sistemática;
2. **Finalidades**;
3. **Bases legais** + necessidade + proporcionalidade;
4. **Análise de riscos** aos direitos do titular;
5. **Medidas mitigantes**;
6. **Consulta a partes interessadas** (titulares, DPO);
7. **Decisão** final + responsável;
8. **Reavaliação** periódica.

### Matriz de risco

| Probabilidade × Impacto | Baixo | Médio | Alto |
|---|---|---|---|
| Baixo | L | L | M |
| Médio | L | M | H |
| Alto | M | H | H |

- **L (Low)**: monitorar;
- **M (Medium)**: implementar mitigantes;
- **H (High)**: rever tratamento ou suspender.

## Princípios (LGPD art. 6)

1. **Finalidade** (propósito específico, legítimo);
2. **Adequação** (compatibilidade com finalidade);
3. **Necessidade** (mínimo necessário);
4. **Livre acesso**;
5. **Qualidade** (exatidão);
6. **Transparência**;
7. **Segurança**;
8. **Prevenção**;
9. **Não discriminação**;
10. **Responsabilização e prestação de contas (accountability)**.

## Direitos do titular (art. 18)

- **Confirmação** da existência de tratamento;
- **Acesso** aos dados;
- **Correção** de inexatos;
- **Anonimização, bloqueio ou eliminação** de dados desnecessários;
- **Portabilidade** a outro fornecedor;
- **Eliminação** de dados tratados com consentimento;
- **Informação** sobre compartilhamento;
- **Informação** sobre possibilidade de não consentir + consequências;
- **Revogação** do consentimento;
- **Petição** ao DPO ou ANPD.

### Atendimento
- **15 dias** para resposta (LGPD art. 19 §1 II: para confirmação/acesso; boas práticas);
- **Documentação** + log;
- **Sem custo** ao titular (regra).

## Encarregado (DPO: art. 41)

- **Pessoa** designada (PF ou PJ);
- **Comunicação ANPD + titulares**;
- **Independência** (preferência);
- **Treinamento técnico** + jurídico;
- **Resolução ANPD CD 18/2024** (atuação do encarregado) + **CD 02/2022** (pequeno porte):
  - **Pequeno porte**: indicação opcional;
  - **Multiplicidade de funções** admitida com cuidado;
  - **Conflito de interesses** vedado;
  - **Externalização**: admitida.

## Operadores + co-controladores

- **DPA** (Data Processing Agreement) obrigatório;
- **Finalidade restrita** definida pelo controlador;
- **Subprocessor** + aviso prévio + objeção;
- **Notificação de incidente** em prazo;
- **Auditoria** pelo controlador;
- **Devolução/destruição** ao final;
- **Indenidade** mútua.

## Transferência internacional (art. 33)

- **Decisão de adequação** ANPD: União Europeia reconhecida como adequada (Res. CD/ANPD 32/2026, reconhecimento mútuo com a Comissão Europeia); demais países sem decisão publicada;
- **Garantias específicas** (SCC, BCR: Resolução CD 19/2024);
- **Consentimento** específico;
- **Cumprimento de obrigação legal**;
- **Cooperação internacional**;
- **Vida ou tutela da saúde**;
- **Autoridade reguladora**;
- **Contrato**;
- **Política aplicada** (entidades do mesmo grupo).

## Anonimização vs pseudonimização

- **Anonimização**: irreversível: LGPD não aplicável (art. 12);
- **Pseudonimização**: reversível: LGPD aplica;
- **Cuidado**: re-identificação trivial não-anonimiza (LGPD art. 12 §1).

## Eliminação

- **Ao final da finalidade** (art. 15);
- **Exceções** (art. 16): obrigação legal, estudo por órgão de pesquisa (anonimização), transferência, uso exclusivo controlador (anonimizado);
- **Comprovação de eliminação** ao titular se solicitar.

## Erros a evitar

- ROPA **estático** (não atualizado);
- ROPA **sem base legal** explicitada por atividade;
- **Consentimento como base padrão** (uso excessivo: preferir legítimo interesse ou contrato quando cabível);
- **Legítimo interesse** sem ponderação documentada (Teste de balanceamento);
- **Dados sensíveis** em base de legítimo interesse (não admitido: art. 11);
- **Crianças** sem consentimento específico do responsável;
- **DPIA** ausente em decisão automatizada (art. 20);
- **Operador sem DPA**;
- **Subprocessor** sem aviso + objeção (cliente surpreendido);
- **Transferência internacional** sem mecanismo válido (art. 33);
- **DPO em conflito de interesses** (head of marketing/sales);
- **Atendimento ao titular** > 15 dias (multa);
- **Eliminação** sem documentação;
- **Anonimização** trivial (re-identificável: não vale);
- **Retenção** sem critério (eternal storage);
- **Compartilhamento** sem mapear no ROPA (controlador surpreendido);
- **Big data** sem propósito definido (LGPD princípio finalidade);
- **Marketing direto** sem opt-out (descumprimento + reputacional);
- **Cookies + tracking** sem banner adequado (Guia ANPD + EU rules);
- **Biometria** sem RIPD (alta sensibilidade);
- **IA + decisão automatizada** sem revisão humana (art. 20);
- **Cross-border** dentro do grupo sem BCR/SCC;
- **Eliminação** quando obrigação legal de retenção (5+ anos fiscais).
