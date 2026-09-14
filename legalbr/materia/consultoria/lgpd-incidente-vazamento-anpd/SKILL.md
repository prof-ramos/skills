---
id: "e09abb77-6ad0-4808-8270-30cf8c9f8ac9"
name: "lgpd-incidente-vazamento-anpd"
title: "LGPD: Resposta a Incidente e Comunicação à ANPD"
category: "materia"
materia: "consultoria"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/consultoria/dados-privacidade-ia/lgpd-incidente-vazamento-anpd.md"
triggers:
  - "incidente de segurança"
  - "vazamento de dados"
  - "data breach"
  - "notificação ANPD"
  - "comunicação ao titular"
  - "Resolução CD 15"
  - "incident response"
  - "cibersegurança"
description: "Resposta a incidente de segurança e vazamento de dados sob LGPD\n(art. 48 + Resolução ANPD CD 15/2024): definição de incidente,\ntriagem de gravidade, comunicação à ANPD (prazo 3 dias úteis em\ngraves), comunicação ao titular, investigação forense, medidas\nmitigantes, retenção de evidências, coordenação com BCB\n(cibersegurança) + SUSEP + CVM, indenização e multa (até R$ 50M\nou 2% faturamento, Resolução CD/ANPD 4/2023 dosimetria)."
---

# LGPD: Incidente e Vazamento de Dados

## Bases legais

- **LGPD Lei 13.709 art. 48-49**;
- **Resolução ANPD CD 15/2024** (comunicação de incidentes);
- **Resolução ANPD CD 4/2023** (dosimetria + aplicação de sanções administrativas);
- **Resolução CMN 4.893/2021** (cibersegurança em IFs; substituiu a Resolução 4.658/18);
- **Resolução BCB 85/2021** (cibersegurança em instituições de pagamento);
- **CVM RCVM 80/2022 + 175** (cibersegurança em cias. abertas);
- **Circular SUSEP 638/2021** (cibersegurança em seguradoras);
- **Marco Civil art. 7 + 10**;
- **CC 186 + 927** (responsabilidade civil: base subsidiária; natureza da responsabilidade do LGPD art. 42 é controvertida na doutrina/jurisprudência);
- **CDC art. 14** (consumidor: responsabilidade objetiva).

## Definição de incidente (Resolução CD 15)

- **Evento adverso** confirmado relacionado à **violação de segurança**;
- Resulta em:
  - **Acesso não autorizado**;
  - **Destruição não autorizada**;
  - **Perda**;
  - **Alteração**;
  - **Comunicação** acidental ou ilícita;
  - **Difusão** não autorizada;
- A dados pessoais **transmitidos, armazenados ou tratados** de outra forma.

## Triagem de gravidade

### Risco relevante (Resolução CD 15 art. 5 §2)
- Dados sensíveis;
- Dados de crianças/adolescentes/idosos;
- Volume significativo;
- Possibilidade de identificação dos titulares;
- Categorias específicas (dados financeiros, de saúde, de geolocalização);
- Probabilidade de utilização indevida.

### Critérios técnicos
- **Confidencialidade**: dados acessados?
- **Integridade**: alterados?
- **Disponibilidade**: serviços impactados?
- **Quantidade**: número de titulares;
- **Sensibilidade**: tipos de dados.

## Resposta: fases (ciclo NIST SP 800-61)

### 1. Detecção
- SIEM/SOC alerts;
- Denúncia (interna ou externa);
- Threat intelligence;
- Vendor notification;
- Bug bounty;
- Imprensa.

### 2. Contenção
- **Isolar** sistemas afetados;
- **Bloquear acessos** comprometidos;
- **Preservar evidências** (chain of custody);
- **Comunicação interna** controlada;
- **Não destruir** logs ou sistemas (forense).

### 3. Erradicação
- Remover malware;
- Patch de vulnerabilidades;
- Reset de credenciais;
- Rotação de chaves;
- Hardening adicional.

### 4. Recuperação
- Restaurar serviços;
- Monitoramento intensivo;
- Verificação de integridade;
- Comunicação aos stakeholders.

### 5. Lições aprendidas
- Postmortem;
- Atualização de runbooks;
- Treinamento;
- Investimentos adicionais.

## Comunicação à ANPD (Resolução CD 15 art. 5)

### Prazo
- **3 dias úteis** após o conhecimento (para incidentes com risco relevante);
- Antes de comunicar ao titular (regra);
- Formato eletrônico via portal ANPD.

### Conteúdo
1. **Identificação** do controlador + DPO;
2. **Descrição** da natureza do incidente;
3. **Categorias** + número estimado de titulares afetados;
4. **Categorias** + volume de dados;
5. **Medidas técnicas + organizacionais** de proteção em vigor;
6. **Causa** (preliminar + confirmada);
7. **Riscos** prováveis aos titulares;
8. **Medidas adotadas** + planejadas para reverter/mitigar;
9. **Razões** se comunicação fora do prazo;
10. **Atualização** posterior se informações iniciais incompletas.

### Quando NÃO comunicar
- Dados **anonimizados** confirmadamente;
- Sem **risco relevante** (mas justificativa documentada);
- Mas ANPD pode determinar comunicação posteriormente.

## Comunicação ao titular (LGPD art. 48 §2)

- **Sempre que** houver risco relevante;
- **Imediatamente** após ANPD ou em paralelo (boas práticas);
- **Conteúdo**:
  - Natureza do incidente + dados afetados;
  - Medidas técnicas adotadas;
  - Riscos + medidas que o titular pode adotar;
  - Forma de obter mais informações + suporte;
- **Canal**: e-mail + carta + push notification + aviso no site (combinados);
- **Linguagem clara**;
- **Tradução** se aplicável.

### Quando dispensar comunicação direta
- Impossibilidade de identificar todos;
- Custo desproporcional;
- Comunicação pública alternativa (boas práticas: anúncio em mídia + site);
- ANPD avalia adequação.

## Investigação forense

### Preservação
- **Imagens forenses** de discos;
- **Logs** preservados (auth, network, system, application);
- **Memory dump** se sistema ainda ativo;
- **Network captures**;
- **Chain of custody** documentada.

### Análise
- **Vetor inicial** (phishing, exploração de vuln, insider);
- **Lateral movement**;
- **Exfiltration** (volume + dados);
- **Persistência** (backdoors);
- **Timeline** completa.

### Atribuição
- IOCs (Indicators of Compromise);
- TTPs (Tactics, Techniques, Procedures);
- Threat actor profiling;
- Cooperação com authorities (PF + Interpol).

## Coordenação setorial

### BCB (Resolução CMN 4.893 + BCB 85)
- **48h** para comunicação ao BCB de incidentes relevantes;
- **DEPED + DESEG**;
- **Plano de resposta** obrigatório;
- **Testes periódicos**;
- **Outsourcing** controlado (Resolução 85).

### CVM (RCVM 80 + 175)
- **Fato relevante** (CVM RCVM 44) se material;
- **Comunicação ao mercado**;
- **Cibersegurança** divulgada em formulário de referência;
- **Insider trading window** + blackout.

### SUSEP, ANS, BCB, ANATEL
- Cada regulador tem prazos próprios;
- **Coordenação** com counsel especializado.

### MPF + PF
- Crimes cibernéticos (Lei 12.737/12 + 13.718/18 + 14.155/21);
- **Notitia criminis** facultativa (regra);
- Cooperação se requerida.

## Sanções (LGPD art. 52 + Resolução CD/ANPD 4/2023)

### Tipos
- **Advertência** + prazo para correção;
- **Multa**:
  - **Simples**: até 2% do faturamento (ano anterior, excluído tributos) limitado a **R$ 50M por infração**;
  - **Diária**;
- **Publicação** da decisão;
- **Bloqueio** dos dados objeto;
- **Eliminação** dos dados;
- **Suspensão parcial** do banco de dados (até 6 meses);
- **Suspensão** do tratamento (até 6 meses);
- **Proibição parcial ou total** do tratamento.

### Dosimetria (Resolução CD/ANPD 4/2023)
- **Gravidade** da infração;
- **Boa-fé**;
- **Vantagem auferida**;
- **Condição econômica**;
- **Reincidência**;
- **Cooperação** com ANPD;
- **Adoção** de medidas corretivas;
- **Adoção** de programa de governança em proteção de dados;
- **Pronta adoção** de medidas para reparar dano;
- **Comprovação** de programa de boas práticas.

### Programa de boas práticas e governança (atenuante)
- Demonstrar compliance + governance;
- DPO formal;
- Mapeamento atualizado;
- RIPD em alto risco;
- Treinamento;
- Auditoria periódica;
- Resposta a incidente testada.

## Indenização civil

- **LGPD art. 42**: responsabilidade civil **direta** do controlador + operador;
- **Solidária** entre controladores conjuntos (art. 42 §1);
- **Operador**: solidária se descumprir instruções legais ou descumprir LGPD (art. 42 §1 II);
- **Inversão do ônus** (LGPD art. 42 §2);
- **CC 186 + 927 + CDC 14** subsidiários;
- **Class actions** (CDC + LACP) crescendo;
- **Dano moral**: STJ admitindo + valoração caso a caso.

## Cyber insurance

- Cobertura: investigação + notificação + remediação + multas (em alguns países) + indenização;
- **Brasil**: cobertura de multas LGPD controvertida (ordem pública);
- **Indemnity de terceiros** + first-party costs;
- **Retroactive coverage** importante;
- **Sub-limits** + retentions.

## Erros a evitar

- **3 dias úteis** não cumprido (multa);
- **Comunicação ao titular antes da ANPD** sem justificativa (irregularidade procedimental);
- **Subnotificação** (omitir incidentes para evitar exposure);
- **Negar incidente** quando há evidência clara (perda de boa-fé);
- **Forense interno** sem chain of custody (evidência imprestável);
- **Restauração antes da forense** (perde análise);
- **Comunicação ao titular** vaga (CC 422 + risco reputacional);
- **Tipping off** ao atacante (se ainda dentro da rede);
- **Não preservar logs** (perda de causa raiz);
- **Não comunicar ao BCB/CVM/SUSEP** quando aplicável (multa setorial);
- **Cyber insurance** sem retroactive (incidente pré-apólice descoberto = sem coverage);
- **Class actions** não preparadas (litigation hold);
- **Sem programa de governança** (atenuante perdido: Resolução CD/ANPD 4/2023);
- **Treinamento ausente** em phishing + SE (vetor principal);
- **MFA não implementado** (credential theft trivial);
- **Backup sem testing** (recuperação inviável: ransomware);
- **Vendor notification** ignorada (cascading breach);
- **Sub-processor breach** sem coordenação;
- **PR + comunicação** dessincronizada (mensagens divergentes);
- **Resposta** demorada (janela de exfiltração ampliada);
- **Postmortem** sem implementação de lições;
- **Reincidência** (Resolução CD/ANPD 4/2023 agravante).
