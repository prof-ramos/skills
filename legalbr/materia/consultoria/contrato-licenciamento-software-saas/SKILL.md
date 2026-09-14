---
id: "5988ee88-b462-46b4-9b5a-0c96392828ae"
name: "contrato-licenciamento-software-saas"
title: "Contratos de Licenciamento de Software e SaaS"
category: "materia"
materia: "consultoria"
documentType: null
version: 1
sourcePath: "lib/skills/official/materia/consultoria/contratos-b2b-disputas/contrato-licenciamento-software-saas.md"
triggers:
  - "licenciamento de software"
  - "SaaS"
  - "software as a service"
  - "EULA"
  - "cloud"
  - "PaaS IaaS"
  - "acordo de nível de serviço"
  - "software escrow"
description: "Contratos de licenciamento de software (Lei 9.609/98 + 9.610/98)\ne SaaS/PaaS/IaaS: licença × cessão, escopo (named users +\nconcurrent users + processador), updates + upgrades + suporte,\nSLA + penalidades, dados em nuvem (LGPD + transferência\ninternacional), IP indemnity, source code escrow, audit rights,\nopen source compliance, termination + transition + suspension\ne tributação (ISS LC 116 + reforma EC 132)."
---

# Licenciamento de Software e SaaS

## Base legal

- **Lei 9.609/1998** (Lei de Software);
- **Lei 9.610/1998** (Direitos Autorais: aplica subsidiariamente);
- **Lei 9.279/1996 art. 195** (concorrência desleal: segredo);
- **LGPD Lei 13.709/2018**;
- **CDC** (Lei 8.078) se consumidor;
- **CC 421-A** (B2B paritário);
- **Marco Civil da Internet Lei 12.965/2014**;
- **Regulamentação INPI** (registro de software opcional: Lei 9.609 art. 2);
- **CVM RCVM 80 + LGPD** (cias. abertas);
- **ANPD Resoluções** + Guias.

## Tipos

| | Conteúdo |
|---|---|
| **On-premise license** | Software instalado no servidor do cliente |
| **SaaS** | Software-as-a-Service: acesso via internet |
| **PaaS** | Platform-as-a-Service: ambiente de desenvolvimento |
| **IaaS** | Infrastructure-as-a-Service: recursos computacionais |
| **Custom development** | Desenvolvimento sob encomenda |
| **Software escrow** | Depósito de código-fonte com 3º (acesso em triggers) |
| **OEM license** | Embutido em hardware |

## Licença × Cessão

| | Licença | Cessão |
|---|---|---|
| Natureza | **Direito de uso** | **Transferência de titularidade** |
| IP rights | Mantidos pelo licenciador | Vão ao cessionário |
| Escopo | Restrito a uso permitido | Pleno (modificação, sublicenciamento) |
| Default | Não-exclusiva + non-transferable | Cessão exige forma escrita (Lei 9.609 art. 9 + Lei 9.610 art. 50) |
| Averbação | INPI (opcional) | INPI (necessário para oponibilidade a 3º) |

## Escopo da licença

### Critérios

| | Conteúdo |
|---|---|
| **Named users** | Usuários nominados |
| **Concurrent users** | Sessões simultâneas |
| **Per device** | Por dispositivo |
| **Per CPU/processor/core** | Capacidade |
| **Per transaction** | Volume |
| **Site license** | Instalação ilimitada em local |
| **Enterprise** | Empresa inteira + afiliadas |

### Restrições típicas
- Sem reverse engineering (Lei 9.609 art. 6 §1);
- Sem descompilação salvo interoperabilidade (Lei 9.609 art. 6 II);
- Sem sublicenciamento;
- Sem uso por terceiros;
- Sem cópia além de backup;
- Sem benchmark sem autorização;
- Uso apenas no propósito definido.

## SaaS: características

- **Hospedado pelo fornecedor**;
- **Acesso via internet**;
- **Multi-tenant** (mesmo software para múltiplos clientes);
- **Dados do cliente** processados em infraestrutura do fornecedor;
- **Updates automáticos** + uma versão única;
- **Subscription** (mensal/anual);
- **API integrations**;
- **SLA** crítico.

## SLA (Service Level Agreement)

### Métricas
- **Uptime / availability** (99.5%, 99.9%, 99.99%: "9s");
- **Response time**;
- **Resolution time** (P1/P2/P3: gravidade);
- **Throughput**;
- **Data backup + RTO + RPO**;
- **Disaster recovery**.

### Penalidades
- **Service credits** (% da fatura mensal);
- **Cap**: 100% da fatura do período;
- **Exclusive remedy** vs **adicional**;
- **Force majeure** carve-out;
- **Right to terminate** se SLA crônico (3 meses consecutivos abaixo do mínimo).

## Suporte + atualizações

- **Tiered support**: 24/7, business hours, e-mail only;
- **Update** (patch + minor): incluído;
- **Upgrade** (major version): debatido;
- **Roadmap** + early access;
- **Custom development**: cobrado separadamente;
- **EOL** (end of life) com notice (geralmente 12-24 meses).

## Dados em nuvem (LGPD)

### Papéis
- **Controlador**: cliente (decide finalidade);
- **Operador**: provedor SaaS (LGPD art. 5);
- **DPA** (Data Processing Agreement) obrigatório.

### Cláusulas DPA
- Finalidade do tratamento;
- Categorias de dados;
- Categorias de titulares;
- Duração;
- Direitos do titular (atendimento conjunto);
- Encarregado/DPO do provedor;
- Sub-processadores (lista + aviso prévio + objeção do controlador);
- Transferência internacional (SCC + decisão de adequação ANPD);
- Medidas de segurança (anonimização, criptografia, controle de acesso);
- Notificação de incidente (24-72h);
- Auditoria pelo controlador;
- Devolução/destruição de dados ao final;
- Indenidade entre as partes.

## Transferência internacional

- **LGPD art. 33**: hipóteses (decisão adequação ANPD, garantias específicas, consentimento, contrato, política aplicada);
- **SCC ANPD** (Resolução CD/ANPD 19/2024: regulamento de transferências e cláusulas-padrão aprovados);
- **EU GDPR SCC** (Decisão de Execução UE 2021/914) aplicável para EU subsidiary;
- **Adequação Brasil-UE reconhecida** (Resolução CD/ANPD 32/2026 + decisão de adequação da Comissão Europeia, reconhecimento mútuo): fluxos Brasil-UE/EEE dispensam SCCs e demais mecanismos, excluídas transferências para fins exclusivos de segurança pública, defesa e persecução penal;
- **Schrems II + risk assessment**;
- **Data localization**: alguns setores (saúde, financeiro);
- **Reforma tributária ICMS/ISS** afeta SaaS hospedado externo.

## IP indemnity

- Provedor garante que software **não infringe IP de terceiros**;
- Indemnity por infração + defesa de litígio;
- **Carve-outs**:
  - Uso em desconformidade com licença;
  - Modificação pelo cliente;
  - Combinação com software/hardware não autorizado;
  - Open source não autorizado;
- **Remedy**: substituição + retorno do valor + indemnização.

## Open source compliance

- **Componentes OSS** identificados (SBOM: Software Bill of Materials);
- **Licenças**: MIT/BSD/Apache (permissivas) × GPL/AGPL (copyleft);
- **GPL/AGPL contamination**: obriga abertura do código derivado;
- **Compliance** + atribuição (notice files);
- **Audit** + scanning tools (FOSSA, Black Duck);
- **SaaS + AGPL**: trigger de obrigação de disclosure (AGPL art. 13);
- **R&W** específica em SaaS contract.

## Source code escrow

- **Trigger events**: insolvência, abandono, M&A, descumprimento crítico;
- **Agente escrow** (Iron Mountain, Lloyds);
- **Atualizações periódicas** do código depositado;
- **Verification** (escrow + testing);
- **Limited license** ao licenciado em trigger (mantenção + bugfix sem distribuição);
- **Útil em** software crítico ou estratégico.

## Audit rights

### Provedor → cliente
- **Auditoria de licenças** (compliance com user count);
- **Notice** (30 dias);
- **Frequência** (anual);
- **Confidentiality**;
- **Settlement** se under-licensing detectado;
- **Não interferir** na operação.

### Cliente → provedor (SaaS)
- **Compliance LGPD + segurança** + SLA;
- **SOC 2 + ISO 27001 reports** em vez de audit on-site;
- **DPA** com audit rights.

## Termination

- **For convenience**: notice 30-90 dias;
- **For cause**: breach material não sanado (15-30 dias cure period);
- **Insolvency**: cláusula resolutiva comum, mas a Lei 11.101 art. 117 permite ao administrador judicial optar pelo cumprimento (cláusula ipso facto controvertida);
- **Change of control**: trigger negociável;
- **Data export** + portability (15-30 dias pós-termination);
- **Destruction certificate**;
- **Transition assistance** (TSA) opcional + cobrada;
- **Pagamento de pro-rata** + fees pendentes.

## Suspension

- **Non-payment** após cure period;
- **Breach de uso** (security violation);
- **Court order**;
- **Restoration** após cura.

## Tributação

### ISS / LC 116
- **LC 116/2003 subitem 1.05**: licenciamento ou cessão de direito de uso de software;
- **Município do tomador** (regra) ou **estabelecimento prestador**;
- **STF Tema 590**: é constitucional o ISS no licenciamento ou cessão de uso de programas desenvolvidos de forma personalizada (subitem 1.05 da LC 116);
- **STF ADIs 1.945 + 5.659** (2021): software por download = serviço (ISS), superada a divergência com o ICMS.

### Reforma tributária (EC 132 + LC 214)
- **CBS + IBS** substituirão PIS/COFINS/ICMS/ISS;
- **Transição 2026-2033**;
- SaaS: tributado pelos novos impostos;
- Contratos longos: cláusula de **tax pass-through** + **tax change** ajuste.

### IRPF + remessas
- **IRRF 15%** + **CIDE 10%** (royalty + assistência técnica internacional);
- **PIS/COFINS importação 9,25%**;
- **ISS** sobre importação em alguns municípios;
- **Lei 14.596/23** (transfer pricing) afeta intercompany.

## Erros a evitar

- Licença sem **definição clara de escopo** (named users vs concurrent);
- **Sem audit rights** do provedor (over-use sem detecção);
- **Reverse engineering** vedado sem exceção legal de interoperabilidade (Lei 9.609 art. 6);
- **SaaS sem SLA** ou **SLA sem service credits**;
- **Service credits cap** acima de 100% (impraticável);
- **LGPD DPA** ausente em SaaS (operador sem regulamento);
- **Sub-processors** sem lista + objeção;
- **Transferência internacional** sem SCC (LGPD art. 33);
- **IP indemnity** sem cap proporcional;
- **OSS compliance** ignorado (GPL contamination + AGPL SaaS trigger);
- **Source code escrow** sem verification (depósito desatualizado);
- **EOL** sem aviso adequado (cliente em corner);
- **Termination** sem data portability + destruction certificate;
- **Suspension** abusiva (CDC + CC 423 desproporcional);
- **ISS** mal calculado (município errado);
- **Reforma tributária** não considerada em contratos longos;
- **IRRF + CIDE** em remessas internacionais sem gross-up (provedor recebe menos);
- **Cláusula de mudança unilateral** ampla demais (CC 423 nula);
- **Update vs upgrade** confundido (cliente sem direito a major version);
- **Custom dev** sem definição de IP ownership;
- **Marca + branding** sem cessão clara (white label);
- **Data ownership** ambígua (provedor reivindica dados do cliente);
- **Multi-tenant** sem segregação real (incidente de um cliente afeta outros);
- **Disaster recovery** sem testing periódico (RTO/RPO ilusório);
- **EULA click-wrap** sem consentimento expresso (litígio sobre validade: STJ).
