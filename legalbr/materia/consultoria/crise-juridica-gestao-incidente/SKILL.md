---
id: "c0cb4adc-ca8e-4d4f-8949-10d772465c63"
name: "crise-juridica-gestao-incidente"
title: "Gestão de Crise Jurídica e Resposta a Incidente"
category: "materia"
materia: "consultoria"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/consultoria/compliance-integridade/crise-juridica-gestao-incidente.md"
triggers:
  - "gestão de crise"
  - "crisis management"
  - "resposta a incidente"
  - "war room"
  - "litigation hold"
  - "investigação corporativa"
  - "exposição reputacional"
  - "recall"
  - "dawn raid"
  - "busca e apreensão na empresa"
  - "acidente corporativo"
  - "vazamento midiático"
description: "Gestão de crise jurídica corporativa: ativação do war room\n(jurídico + compliance + PR + RH + CEO + board), preservação\nde evidências (litigation hold), privilege EAOAB 7 II,\ncoordenação multi-frente (reguladores, MPF, PF, CGU, CVM,\nANPD, CADE, BCB), interface com mídia, comunicação interna,\nfato relevante (RCVM 44), proteção a executivos (D&O), self-\nreporting estratégico, classes de crise (regulatória, criminal,\ncibernética, reputacional, ambiental, trabalhista, produto)."
---

# Gestão de Crise Jurídica

## Classes de crise

| | Conteúdo |
|---|---|
| **Regulatória** | Autuação, suspensão, intervenção (CVM, BCB, ANPD, ANS, CADE) |
| **Criminal** | Investigação PF/MPF, busca e apreensão, prisão de executivo |
| **Cibernética** | Vazamento, ransomware, sequestro de dados (LGPD + Resolução CD/ANPD 15/2024) |
| **Reputacional** | Exposição midiática, redes sociais, denúncia em programa |
| **Ambiental** | Acidente, vazamento, dano material a comunidade |
| **Trabalhista** | Acidente fatal, assédio sistêmico, lista suja MTE |
| **Produto** | Recall, defeito, dano ao consumidor (CDC + ANVISA + ANATEL) |
| **Financeira** | Default, fraude contábil, restatement |
| **Geopolítica** | Sanção (OFAC, EU), expropriação, golpe, embargo |
| **Saúde pública** | Surto, contaminação, evento adverso |

## Primeiras 72 horas (golden window)

### 0-2h
- **Notificar** Compliance Officer + General Counsel + CEO;
- **Verificar autenticidade** do evento (não reagir a rumor);
- **Ativar war room**;
- **Engajar conselheiro externo** (privilege);
- **Litigation hold** preliminar emitido.

### 2-24h
- **Preservação de evidências** (forense digital + documentos físicos);
- **Mapear exposure** preliminar (regulatório + criminal + civil + reputacional);
- **Coordenar autoridades** (se mandado, busca em curso, intimação);
- **Plano de comunicação** rascunhado;
- **Notice a seguradoras** (D&O + cyber + general liability + recall);
- **Conselho** alertado (Comitê de Auditoria + Presidente);
- **Stakeholders críticos** identificados.

### 24-72h
- **Investigação interna** estruturada (escopo + lead + plano);
- **Self-reporting** decision (CGU, CVM, ANPD, CADE conforme aplicável);
- **Fato relevante** (RCVM 44) se material para mercado;
- **Comunicação ao mercado** + mídia coordenada;
- **Empregados** informados (alinhamento + não-falar com imprensa);
- **Fornecedores/clientes críticos** alertados se necessário;
- **Roadmap** dos próximos 30 dias.

## War room

### Composição
- **General Counsel** (lead operacional);
- **Compliance Officer**;
- **CEO** + **CFO** + **COO** (rotativo conforme tema);
- **Head de Comunicação / PR**;
- **Head de RH**;
- **Head de IT/CISO** (se cyber);
- **Investor Relations** (se cia. aberta);
- **Conselheiro externo** (privilege + estratégia jurídica);
- **PR externa** especializada em gestão de crise;
- **Forensic externo** independente;
- **Lobista / Government affairs** se regulatório;
- **Conselho** representado (board liaison).

### Funcionamento
- **Sala física + virtual** dedicada;
- **Daily standups** nas primeiras 2 semanas (24/7 se crítico);
- **Workstreams** definidos (regulatório, criminal, civil, comunicação, operacional);
- **Decision log** documentado;
- **Reporting ao Conselho** semanal ou diário;
- **Need-to-know** estrito.

## Litigation hold

### Função
- Suspende **descarte de documentos** relevantes;
- **Preserva** evidência para futuras ações + investigações;
- **Mitiga risco** de spoliation (destruição → presunção contrária).

### Procedimento
1. **Identificar custodians** (pessoas + sistemas com info relevante);
2. **Comunicação formal** (e-mail + acknowledgment);
3. **TI**: pausa de retention policies + e-mail purging + backup rotation;
4. **Documentação** de implementação;
5. **Reminders periódicos**;
6. **Atualização** conforme escopo evolui;
7. **Release** ao final (com nova comunicação formal).

### Escopo
- E-mails + Slack/Teams + WhatsApp corporativo;
- Documentos físicos + digitais;
- Sistemas (ERP, CRM, financeiro);
- Logs (auth, network, application);
- Backups;
- Mobile devices (BYOD com cuidado LGPD).

### Risco se descumprido
- **Spoliation**: presunção contrária + multa;
- **CPC 400 §ú**: ônus invertido se documento ocultado;
- **Obstrução de justiça** (CP 343 + 347) se intencional;
- **Sanção administrativa** (CGU + CVM + CADE) por ocultação.

## Privilege

### EAOAB art. 7 II + XIX
- **Sigilo profissional** advogado-cliente inviolável;
- **Jurisprudência do STJ e do STF**: comunicações advogado-cliente protegidas (EAOAB art. 7 §§ 6-7);
- **Busca em escritório**: exige decisão judicial fundamentada e específica + acompanhamento de representante da OAB.

### Boas práticas
- **Advogado externo** envolvido desde o início (privilege mais robusta);
- **In-house counsel** registrado na OAB (privilege parcial mas reforça);
- **Marcar "Privileged & Confidential / Attorney-Client Communication"**;
- **Need-to-know** restrito;
- **Não misturar** com fato administrativo (perda de privilege);
- **Cross-border**: privilege em cada jurisdição (USA mais restritiva para in-house);
- **Work product doctrine** (trabalho consultivo).

### Riscos de waiver
- **Compartilhamento** com terceiros sem common interest agreement;
- **Disclosure parcial** (subject matter waiver);
- **Cooperação com autoridade** sem cuidado (selective waiver);
- **Auditor externo**: compartilhamento controlado (acordos específicos).

## Self-reporting estratégico

### Quando avaliar
- **Anticorrupção**: leniência CGU/AGU (race to courthouse: primeiro tem benefício máximo);
- **Concorrencial**: leniência CADE (imunidade ao 1º colaborador);
- **LGPD**: comunicação ANPD obrigatória em 3 dias úteis em risco relevante;
- **CVM**: fato relevante + autodenúncia em violação detectada;
- **BCB**: comunicação em 48h em incidentes relevantes;
- **Criminal**: ANPP (Acordo de Não-Persecução Penal, CPP 28-A) + ANPC (Não-Persecução Civil, Lei 8.429 art. 17-B);
- **FCPA/UKBA**: voluntary self-disclosure DOJ/SFO + DPA/NPA.

### Análise antes de self-report
- **Mapear fatos** via investigação interna prévia;
- **Avaliar exposure** multi-jurisdicional;
- **Risk vs benefit**: redução de multa + atenuante × admissão usada em civil/criminal;
- **Ordem de prioridade** entre autoridades (coordenar);
- **Privilege protection** ao apresentar fatos;
- **NDA** antes de proffer;
- **Coordenação MPF + CGU + AGU + CADE + DOJ + SEC** se cross-border.

### Riscos
- **Race to the courthouse**: não ser primeiro perde benefício;
- **Self-incrimination** em outras esferas;
- **Class actions** civis (CDC + LACP);
- **Reputacional** (mesmo com acordo);
- **Empregados envolvidos** demitidos sem coordenação (perda de colaboração).

## Comunicação ao mercado e mídia

### Cia. aberta: fato relevante (RCVM 44)
- **DRI** assina e divulga;
- **Sistema Empresas.NET** + B3 + site RI;
- **Tempestivo + simultâneo** ao mercado;
- **Conteúdo claro** + sem omissão material;
- **Atualização periódica** conforme fatos evoluem;
- **Trading halt** se necessário (B3).

### Mídia
- **Holding statement** em 2-4 horas;
- **Spokesperson único** designado (CEO ou Comunicação);
- **Treinamento prévio** (media training);
- **Mensagens-chave**: 3-5 alinhados a fatos verificáveis;
- **Empatia primeiro** (se há vítima);
- **Compromisso com investigação + transparência**;
- **Sem especular** sobre causas pendentes;
- **Sem culpar terceiros** sem provas;
- **Atualizações periódicas** (silêncio prolongado piora).

### Comunicação interna
- **Empregados primeiro** (antes da mídia se possível);
- **Mensagem do CEO**;
- **Town hall** virtual;
- **FAQ** para gestores;
- **Diretrizes**: não falar com imprensa, redirecionar contatos a PR;
- **Canal aberto** para dúvidas (compliance + RH).

### Redes sociais
- **Monitoring** 24/7;
- **Response protocol** (não discutir mérito; redirecionar);
- **Tom respeitoso** + empático;
- **Suspensão de campanhas** publicitárias em curso;
- **Influencers + KOLs** alinhados.

## Interface com autoridades

### Mandado de busca e apreensão (dawn raid)
1. **Verificar mandado** (escopo + autoridade + assinatura);
2. **Acompanhar** com advogados;
3. **Privilege protection** (separar documentos privilegiados);
4. **Documentar** o que foi apreendido (cópia da lista);
5. **Cooperar** sem renunciar privilege;
6. **Não destruir** documentos durante busca;
7. **Comunicação interna**: orientações claras;
8. **Pos-raid**: assess + investigação interna + estratégia.

### Intimação para depoimento
- **Análise** antes de comparecer;
- **Advogado** acompanha (CF 5 LXIII);
- **Direito ao silêncio** se autoincriminação;
- **Preparação** prévia com revisão de fatos.

### Operação policial
- **Coordenação** com criminal counsel;
- **HC preventivo** se necessário;
- **Custódia** + audiência de custódia em 24h;
- **Comunicação familiar**;
- **D&O insurance** acionada.

## Investigação interna

### Estrutura
- **Lead**: advogado externo (privilege + independência);
- **Forensic accountant** + IT forensics;
- **Plano + escopo + cronograma** documentados;
- **Preservação** de evidências (legal hold);
- **Entrevistas** com Upjohn warning;
- **Documentação** rigorosa.

### Outcomes
- **Procedente**: sanção + remediação + comunicação;
- **Improcedente**: arquivamento + feedback;
- **Inconclusiva**: monitoring + redobro de controles.

## Proteção a executivos (D&O)

- **D&O insurance** acionada imediatamente;
- **Notice** dentro do prazo da apólice (geralmente 30-60 dias);
- **Counsel próprio** para cada executivo (potencial conflito com empresa);
- **Indemnification** corporativa (LSA 159 §ú + estatuto + acordo de indemnification);
- **Advancement of fees** (pagamento antecipado de defesa);
- **Side A coverage** (executivo não-indenizado pela empresa);
- **Side B** (empresa reembolsada por indenizar);
- **Side C** (entity coverage, securities claims).

## Recall (CDC + setoriais)

### CDC art. 10
- **Periculosidade descoberta após** colocação no mercado → comunicar:
  - **Imediatamente** às autoridades;
  - **Imprensa** + meios eficazes;
  - Suportar custos;
- **CDC art. 12-13**: responsabilidade objetiva por defeito.

### Setoriais
- **ANVISA**: medicamentos + alimentos + cosméticos + saneantes;
- **ANATEL**: telecom;
- **ANEEL**: equipamentos elétricos;
- **DENATRAN**: veículos;
- **INMETRO**: produtos certificados.

### Procedimento
- **Senacon** (Secretaria Nacional do Consumidor) comunicada;
- **Plano de recall** aprovado;
- **Comunicação ao consumidor** (imprensa + site + canais);
- **Logística reversa**;
- **Reembolso/substituição/reparo**;
- **Reporting** periódico ao Senacon.

## Insurance coverage

| | Conteúdo |
|---|---|
| **D&O** | Defesa + indemnização de administradores |
| **General liability** | Danos a terceiros (PI + DM) |
| **Product liability** | Defeito de produto |
| **Cyber liability** | Incidente cibernético |
| **E&O / professional** | Erro profissional |
| **Recall** | Custos de recall |
| **Crime + fidelity** | Fraude interna |
| **Environmental** | Dano ambiental |
| **Reputational** | Algumas seguradoras especializadas |
| **Political risk** | Expropriação + golpe + embargo |
| **K&R** | Sequestro e resgate (executivos em jurisdição de risco) |

### Notice
- **Tempestivo** (geralmente 30-60 dias);
- **Documentação** completa;
- **Reservation of rights** comum (seguradora preserva defesas);
- **Counsel** aprovado pela seguradora.

## Plano de continuidade (BCP)

- **Identificar processos críticos**;
- **RTO / RPO**;
- **Backup sites + remote work**;
- **Cadeia de suprimentos** alternativa;
- **Comunicação** redundante;
- **Treinamento + simulação** anual;
- **Atualização** periódica.

## Pós-crise

### Lições aprendidas
- **Postmortem** estruturado;
- **Root cause analysis**;
- **Plano de remediação** com responsáveis e prazos;
- **Atualização** de políticas + treinamentos + controles;
- **Reporting** ao Conselho;
- **Auditoria** da remediação.

### Reputação
- **Stakeholder mapping**;
- **Plano de reconstrução** de confiança (12-24 meses);
- **Transparência** continuada;
- **ESG initiatives** alinhadas;
- **Medição** de sentiment + brand health.

### Disciplinar
- **Sanções** proporcionais;
- **Demissões** com coordenação criminal/civil;
- **Disclosure** ao mercado se material;
- **Reporting** a autoridades sobre remediação.

## Treinamento + simulação

- **Tabletop exercises** anuais (executivos + war room);
- **Live drills** (cyber, recall, dawn raid);
- **Media training** para spokespersons;
- **Crisis communications** atualizada periodicamente.

## Erros a evitar

- **Reagir antes de verificar fatos** (rumor vira admissão);
- **Comunicação fragmentada** (porta-vozes múltiplos, mensagens divergentes);
- **Silêncio prolongado** sem holding statement (mídia preenche o vazio);
- **Litigation hold** tardio (spoliation + presunção contrária);
- **Privilege quebrado** (sem advogado externo + comunicação não marcada);
- **Self-reporting** sem investigação interna prévia (sem domínio dos fatos);
- **Não ser primeiro** a reportar quando leniência cabível (perde benefício);
- **Admissão pública** sem cap de exposição (boomerang em civil + criminal);
- **Tipping off** ao atacante em incidente cyber (perde forense);
- **Empregados envolvidos** demitidos antes de obter colaboração;
- **D&O notice** fora do prazo (perde cobertura);
- **Spokesperson sem media training** (gafes virais);
- **Culpar terceiros** sem provas (defamação + retaliação);
- **Speculate sobre causa** com investigação em curso (futuro contradiz);
- **Insurance reservations of rights** ignoradas (cobertura indeferida);
- **Fato relevante** atrasado em cia. aberta (sanção CVM RCVM 44);
- **Trading window** sem blackout em crise material (insider trading risk);
- **Comunicação interna depois** da mídia (empregados sabem por terceiros);
- **Mandado de busca** sem advogado presente (privilege em risco);
- **Documentos destruídos** durante busca (obstrução CP 343);
- **Cooperação plena** sem privilege estratégico (waiver indevida);
- **Cross-border** sem coordenação de privilege em cada jurisdição;
- **Recall** tardio (CDC art. 10 + Senacon: multa + criminal);
- **PR sem alinhamento jurídico** (declaração que admite culpa);
- **Postmortem ausente** (mesmo problema recorre);
- **Plano de continuidade** sem testes (RTO/RPO ilusório);
- **D&O sem Side A** (executivo desprotegido se empresa não indeniza);
- **Class actions** não preparadas (provisão contábil + defesa coordenada);
- **Mídia social** sem monitoramento (escala incontrolada);
- **Stakeholders críticos** (clientes + reguladores + investidores) descobrem por imprensa;
- **Investigação interna** com management investigado conduzindo (conflito);
- **Encerramento prematuro** da crise (efeito de longo prazo subestimado).
