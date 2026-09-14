# 🚀 Agentic Skills & MCP Repository

<div align="center">

[![skills.sh](https://skills.sh/b/prof-ramos/skills)](https://skills.sh/prof-ramos/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Specification-blue)](https://agentskills.io/specification)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Node.js Version](https://img.shields.io/badge/Node.js-20%2B-green?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Validation Status](https://img.shields.io/badge/Validation-make%20check%20%E2%9C%93-brightgreen)](Makefile)

**Repositório oficial de Agent Skills e servidores Model Context Protocol (MCP).**  
Compatível com a plataforma [skills.sh](https://skills.sh), com a especificação [Agent Skills Specification](https://agentskills.io/specification) e com os principais agentes de codificação por IA: **Claude Code**, **Cursor**, **Windsurf**, **Antigravity**, **Codex**, **OpenCode**, **GitHub Copilot**, **Gemini**, **Cline** e **AMP**.

[Instalação Rápida](#-instalação-e-uso-via-cli-skillssh) • [Catálogo de Skills](#-catálogo-de-skills) • [LegalSkillsBR](#️-legalskillsbr--2149-skills-jurídicas) • [Servidores MCP](#%EF%B8%8F-servidores-mcp) • [Validação](#-testes--validação)

</div>

---

## 📌 Sumário

- [✨ Visão Geral](#-visão-geral)
- [⚡ Instalação e Uso via CLI skills.sh](#-instalação-e-uso-via-cli-skillssh)
- [📁 Estrutura do Repositório](#-estrutura-do-repositório)
- [🧠 Catálogo de Skills](#-catálogo-de-skills)
  - [⚡ Automação & Integrações](#-automação--integrações)
  - [🛠️ Agent Workflows & Dev Tools](#%EF%B8%8F-agent-workflows--dev-tools)
  - [🎨 Design & Conteúdo](#-design--conteúdo)
  - [🛡️ Segurança & Offensive AI](#%EF%B8%8F-segurança--offensive-ai)
  - [📜 Compliance, Educação & Concursos](#-compliance-educação--concursos)
- [⚖️ LegalSkillsBR (2.149 Skills Jurídicas)](#️-legalskillsbr--2149-skills-jurídicas)
- [🛠️ Servidores MCP](#%EF%B8%8F-servidores-mcp)
- [🧪 Testes & Validação](#-testes--validação)
- [🔄 Configuração e Retomada de Ambiente](#-configuração-e-retomada-de-ambiente)
- [📝 Contribuição e Licença](#-contribuição-e-licença)

---

## ✨ Visão Geral

Este repositório reúne um acervo modular e versionado de habilidades procedurais (**Agent Skills**) e servidores **MCP (Model Context Protocol)**. Cada skill opera como um pacote autocontido com instruções em Markdown (`SKILL.md`), frontmatter YAML padronizado (`name` e `description`), além de scripts executáveis, templates e documentação de referência.

### Padrões e Boas Práticas do [skills.sh](https://skills.sh/docs)
- **Descoberta Nativa**: Estruturado para indexação direta pela CLI oficial `skills` (`npx skills add`).
- **Curadoria via `skills.sh.json`**: Agrupamentos temáticos no arquivo de configuração raiz de acordo com as regras do [Schema Draft 2020-12](https://skills.sh/schemas/skills.sh.schema.json) (máximo de 50 grupos, até 500 skills por grupo, títulos válidos e paridade estrita de slugs).
- **Telemetria Transparente**: Participa do ranking público do `skills.sh` através da telemetria anônima de instalação coletada pela CLI.

---

## ⚡ Instalação e Uso via CLI `skills.sh`

A CLI oficial [`skills`](https://www.skills.sh/docs/cli) permite instalar, usar e gerenciar as habilidades sem necessidade de clonar o repositório manualmente:

### 1. Instalação de Skills

```bash
# Listar todas as skills disponíveis no repositório
npx skills add prof-ramos/skills --list

# Instalar uma skill específica (exemplo: resend-api)
npx skills add prof-ramos/skills --skill resend-api

# Ou usando a sintaxe abreviada:
npx skills add prof-ramos/skills@resend-api

# Instalar para agentes específicos (ex: claude-code, cursor)
npx skills add prof-ramos/skills@ui-ux-pro-max -a claude-code cursor -y

# Instalar para todos os agentes configurados no sistema
npx skills add prof-ramos/skills@skill-cleaner --all
```

### 2. Uso Efêmero sem Instalação (`skills use`)
Você pode gerar o prompt de contexto de uma skill sob demanda sem instalá-la permanentemente:

```bash
# Injetar skill diretamente no Claude Code
npx skills use prof-ramos/skills@resend-api | claude

# Abrir interativamente com um agente suportado
npx skills use prof-ramos/skills@vuln-discovery --agent claude-code
```

### 3. Busca e Atualização
```bash
# Buscar skills no repositório interativamente
npx skills find --owner prof-ramos

# Atualizar skills instaladas para as versões mais recentes
npx skills update
```

> [!TIP]
> **Privacidade de Telemetria**: Por padrão, a CLI envia métricas agregadas e anônimas para contabilizar instalações no ranking do `skills.sh`. Para desativar, defina `DISABLE_TELEMETRY=1`.

---

## 📁 Estrutura do Repositório

```text
.
├── skills.sh.json                 # Configuração oficial de agrupamentos para o skills.sh (31 grupos)
├── skills/                        # Contêiner canônico de skills categorizadas
│   ├── automation/                # Cyberduck, N8N, File Organization, Resend API
│   ├── agent-workflows/           # Skill Cleaner, Learn (gestão incremental de memória)
│   ├── compliance/                # LGPD Checklist
│   ├── content/                   # Brazilian Official Docs, Social Ads Creator
│   ├── design/                    # UI/UX Pro Max
│   ├── security/                  # Red Team, Supabase Security, Vuln Discovery
│   └── gh-cli/                    # GitHub CLI Expert
├── legalbr/                       # Coleção LegalSkillsBR (2.149 skills jurídicas)
│   ├── forma/                     # 299 minutas e peças processuais
│   └── materia/                   # 1.850 teses jurídicas em 25 ramos do direito
├── assinafy-api/                  # Skill especialista na API Assinafy
├── cloudflare-workers/            # Scaffolds e patterns para Cloudflare Workers
├── edital-verticalizado/          # Verticalização de editais de concursos
├── gerador-de-simulados/          # Geração de simulados e questões em PDF
├── godmode-agnostic/              # Técnicas de refinamento comportamental de LLMs
├── ollama-godmode/                # Testes de robustez para modelos Ollama Cloud
├── ready-to/                      # Diagnóstico e checklist pré-deploy
├── social-carousel/               # Geração automatizada de carrosséis (Puppeteer)
├── servers/                       # Servidores Model Context Protocol (MCP)
│   └── supergithub/               # Gestão avançada do GitHub via API
├── scripts/                       # Linters e utilitários de validação
│   ├── validate_skills_sh.py      # Validador determinístico do schema skills.sh.json e paridade
│   └── validate-skills.py         # Validador de frontmatter e integridade
├── tests/                         # Suíte de testes unitários automatizados (19 testes)
└── Makefile                       # Pipeline de testes e auditoria local
```

---

## 🧠 Catálogo de Skills

### ⚡ Automação & Integrações

| Skill | Slug / Instalação | Descrição |
| :--- | :--- | :--- |
| **[Cyberduck Expert](skills/automation/cyberduck-expert/SKILL.md)** | `cyberduck-expert` | Automação e transferências FTP/SFTP/S3/WebDAV via `duck` CLI. |
| **[N8N Skills](skills/automation/n8n-skills/SKILL.md)** | `n8n-skills` | Construção, nós avançados e integração de workflows no n8n. |
| **[File Organization](skills/automation/file-organization/SKILL.md)** | `file-organization` | Padrões de organização de projetos, convenções e refatoração de pastas. |
| **[Assinafy API](assinafy-api/SKILL.md)** | `assinafy-api` | Integração completa com API Assinafy (upload, signers, webhooks, templates). |
| **[Cloudflare Workers](cloudflare-workers/SKILL.md)** | `cloudflare-workers` | Patterns, scaffolds e deploy de aplicações serverless na Cloudflare. |
| **[Resend API](skills/automation/resend-api/SKILL.md)** | `resend-api` | Envio de e-mails transacionais, domínios, chaves de API, webhooks Svix e contatos. |

### 🛠️ Agent Workflows & Dev Tools

| Skill | Slug / Instalação | Descrição |
| :--- | :--- | :--- |
| **[Skill Cleaner](skills/agent-workflows/skill-cleaner/SKILL.md)** | `skill-cleaner` | Auditoria e corte de budget de tokens de skills nos prompts de agentes. |
| **[Ready-to](ready-to/SKILL.md)** | `ready-to` | Diagnóstico pré-deploy, verificação de linters, testes e sanidade de código. |
| **[Autoreview](autoreview-agnostic/opencode/skills/autoreview/SKILL.md)** | `autoreview` | Revisão de código estruturada e agnóstica para agentes autônomos. |
| **[GitHub CLI](skills/gh-cli/SKILL.md)** | `gh-cli` | Operações completas de repositórios, PRs, issues e releases via terminal. |
| **[Learn](skills/agent-workflows/learn/SKILL.md)** | `learn` | Sistema incremental e auditável de aprendizado de agente com suporte a rollback. |

### 🎨 Design & Conteúdo

| Skill | Slug / Instalação | Descrição |
| :--- | :--- | :--- |
| **[UI/UX Pro Max](skills/design/ui-ux-pro-max/SKILL.md)** | `ui-ux-pro-max` | Design system com 50 estilos, paletas harmônicas, tipografia e checklist de entrega. |
| **[Social Carousel](social-carousel/SKILL.md)** | `social-carousel` | Geração cinematográfica de carrosséis para redes sociais (HTML + Puppeteer). |
| **[Social Ads Creator](skills/content/social-ads-creator/SKILL.md)** | `social-ads-creator` | Redação estratégica de copy e conteúdo orgânico/pago (AIDA, PAS). |
| **[Brazilian Official Docs](skills/content/brazilian-official-docs/SKILL.md)** | `brazilian-official-docs` | Redação de ofícios, pareceres e notas segundo o Manual da Presidência da República. |

### 🛡️ Segurança & Offensive AI

| Skill | Slug / Instalação | Descrição |
| :--- | :--- | :--- |
| **[Ethical Red Team](skills/security/ethical-redteam/SKILL.md)** | `ethical-redteam` | Testes autorizados de Red Team e Bug Bounty (OSINT, scanning, relatórios OWASP). |
| **[Temp Mail Pentest](skills/security/temp-mail-pentest/SKILL.md)** | `temp-mail-pentest` | Gerenciamento de e-mails temporários para auditorias de endpoints e cadastros. |
| **[Vuln Discovery](skills/security/vuln-discovery/SKILL.md)** | `vuln-discovery` | Pipeline de descoberta de vulnerabilidades em 8 fases em bases de código. |
| **[Supabase Security](skills/security/supabase-security/SKILL.md)** | `supabase-security` | Auditoria pericial de Row Level Security (RLS), JWTs e políticas no Supabase. |
| **[Ollama Godmode](ollama-godmode/SKILL.md)** | `ollama-godmode` | Pesquisa controlada de segurança e robustez para LLMs locais/nuvem. |
| **[Godmode Agnostic](godmode-agnostic/SKILL.md)** | `godmode-agnostic` | Análise agnóstica de guardrails e alinhamento de modelos de IA. |

### 📜 Compliance, Educação & Concursos

| Skill | Slug / Instalação | Descrição |
| :--- | :--- | :--- |
| **[LGPD Checklist](skills/compliance/lgpd-checklist/SKILL.md)** | `lgpd-checklist` | Checklists operacionais, mapeamento de risco e conformidade com a LGPD. |
| **[Gerador de Simulados](gerador-de-simulados/SKILL.md)** | `gerador-de-simulados` | Criação de simulados, questões objetivas/discursivas e exportação PDF. |
| **[Edital Verticalizado](edital-verticalizado/SKILL.md)** | `edital-verticalizado` | Estruturação e controle de matérias para concursos públicos. |

---

## ⚖️ LegalSkillsBR — 2.149 Skills Jurídicas

A coleção [`legalbr/`](legalbr/) contém o maior acervo aberto de habilidades jurídicas brasileiras estruturadas para agentes de IA, cobrindo peças processuais, teses dos tribunais superiores (STF/STJ) e conformidade normativa:

```bash
# Listar acervo completo de minutas e peças processuais
npx skills add prof-ramos/skills/legalbr/forma --list

# Instalar uma tese jurídica ou peça específica
npx skills add prof-ramos/skills/legalbr@recurso-extraordinario-rg-tema-69-cf-102 -a claude-code -y

# Instalar explorando toda a árvore via subpastas profundas
npx skills add prof-ramos/skills/legalbr/materia/tributario --list
```

| Ramo / Categoria | Skills | Destaques |
| :--- | :---: | :--- |
| [Formas & Peças](legalbr/forma/) | **299** | Petições iniciais, contestações, recursos, pareceres e contratos |
| [Tributário](legalbr/materia/tributario/) | **246** | Temas repetitivos e repercussão geral, ICMS-ST, PIS/COFINS, imunidades |
| [Administrativo](legalbr/materia/administrativo/) | **214** | Nova Lei de Licitações (14.133/21), improbidade, regime de servidores |
| [Penal & Processo Penal](legalbr/materia/penal/) | **286** | Audiências de custódia, tribunal do júri, recursos, execução penal |
| [Processo Civil](legalbr/materia/processo-civil/) | **164** | Cumprimento de sentença, tutelas de urgência, agravo de instrumento |
| [Trabalhista & Previdenciário](legalbr/materia/trabalho/) | **202** | Terceirização, compliance trabalhista, revisões de aposentadoria |
| [Demais 19 Ramos do Direito](legalbr/materia/) | **738** | Consumidor, Constitucional, Ambiental, Eleitoral, Digital e Empresarial |

---

## 🛠️ Servidores MCP

Os servidores [Model Context Protocol (MCP)](https://modelcontextprotocol.io) expõem ferramentas de sistema diretamente aos agentes:

| Servidor | Caminho | Protocolo | Recursos |
| :--- | :--- | :--- | :--- |
| **SuperGitHub** | [`servers/supergithub`](servers/supergithub/SKILL.md) | Stdio MCP / Python | Criação e merge de PRs, gestão de issues, automação de branches e workflows |

---

## 🧪 Testes & Validação

Para garantir integridade contínua, o repositório conta com scripts de validação automatizada e testes unitários:

```bash
# Executar a suíte de validação completa
make check

# Validar skills.sh.json contra o schema oficial da Vercel
make check-skills-sh

# Executar a validação em modo estrito (paridade de diretórios obrigatória)
make check-skills-sh-strict

# Executar os testes unitários do validador (19 testes)
make test-validation
```

---

## 🔄 Configuração e Retomada de Ambiente

Para clonar e configurar o repositório em uma máquina limpa:

```bash
# 1. Clonar o repositório
git clone https://github.com/prof-ramos/skills.git
cd skills

# 2. Configurar variáveis de ambiente base
cp .env.example .env

# 3. Validar a integridade dos arquivos e schemas
make check-skills-sh-strict
```

---

## 📝 Contribuição e Licença

Contribuições, correções e novas skills são muito bem-vindas! Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de formatação de `SKILL.md`.

Distribuído sob a licença **MIT**. Consulte [`LICENSE`](LICENSE) para mais detalhes.

<div align="center">
  <sub>Mantido por <a href="https://github.com/prof-ramos">Prof. Ramos</a> • Listado no <a href="https://skills.sh/prof-ramos/skills">skills.sh</a></sub>
</div>
