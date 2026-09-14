# 🚀 Agentic Skills & MCP Repository

<div align="center">

[![skills.sh](https://skills.sh/b/prof-ramos/skills)](https://skills.sh/prof-ramos/skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Specification-blue)](https://agentskills.io/specification)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Node.js Version](https://img.shields.io/badge/Node.js-20%2B-green?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Validation Status](https://img.shields.io/badge/Validation-make%20check%20%E2%9C%93-brightgreen)](Makefile)

**Repositório centralizado para Agent Skills customizadas e servidores Model Context Protocol (MCP).**  
Compatível com o ecossistema [skills.sh](https://skills.sh), Claude Code, Cursor, Windsurf, OpenCode, e a especificação oficial [Agent Skills Specification](https://agentskills.io/specification).

[Instalação Rápida](#-como-usar) • [Habilidades Disponíveis](#-habilidades-disponíveis) • [Servidores MCP](#%EF%B8%8F-servidores-mcp-1) • [Estrutura](#-estrutura-do-projeto) • [Retomada & Setup](#-retomada-após-formatação)

</div>

---

## 📌 Índice

- [✨ Visão Geral](#-visão-geral)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🧠 Habilidades Disponíveis](#-habilidades-disponíveis)
  - [⚡ Automação & Integrações](#-automação--integrações)
  - [🛠️ Agent Workflows & Dev Tools](#%EF%B8%8F-agent-workflows--dev-tools)
  - [🎨 Design & Conteúdo](#-design--conteúdo)
  - [🛡️ Segurança & Offensive AI](#%EF%B8%8F-segurança--offensive-ai)
  - [📜 Compliance, Educação & Concursos](#-compliance-educação--concursos)
  - [⚖️ Legal Skills (LegalSkillsBR)](#️-legal-skills-legalskillsbr)
- [🛠️ Servidores MCP](#%EF%B8%8F-servidores-mcp-1)
- [🚀 Como Usar](#-como-usar)
  - [1. Instalação via CLI skills.sh (Recomendado)](#1-instalação-direta-via-cli-skillssh-recomendado)
  - [2. Instalação Local (Git Clone)](#2-uso-local--clonando-o-repositório)
- [🧪 Testes & Validação](#-testes--validação)
- [🔄 Retomada após Formatação](#-retomada-após-formatação)
- [📝 Contribuindo & Licença](#-contribuindo)

---

## ✨ Visão Geral

Este repositório reúne um catálogo completo de habilidades modulares (**Skills**) e servidores de protocolo de contexto (**MCP**) desenhados para expandir os recursos de agentes autônomos de IA. Cada skill contém instruções determinísticas (`SKILL.md`), scripts operacionais, templates e referências técnicas.

> [!NOTE]
> Todas as skills deste repositório possuem validação sintática automatizada via `make check` e estão indexadas no arquivo [`skills.sh.json`](skills.sh.json).

---

## 📁 Estrutura do Projeto

```text
.
├── skills.sh.json                 # Configuração de categorias e agrupamentos do ecossistema skills.sh
├── legalbr/                       # Acervo LegalSkillsBR: 2.149 skills jurídicas
│   ├── forma/                     # 299 minutas e peças processuais
│   └── materia/                   # 1.850 teses jurídicas em 25 ramos do direito
├── skills/                        # Coleção principal de Agent Skills por categoria
│   ├── automation/                # Transferências de arquivos, N8N, utilitários
│   │   ├── cyberduck-expert/
│   │   ├── n8n-skills/
│   │   ├── file-organization/
│   │   └── resend-api/
│   ├── compliance/
│   │   └── lgpd-checklist/
│   ├── content/
│   │   ├── brazilian-official-docs/
│   │   └── social-ads-creator/
│   ├── agent-workflows/           # Otimização de prompts, auditoria de budget de tokens
│   │   ├── skill-cleaner/
│   │   └── learn/                 # Sistema de aprendizado incremental/auditável para Codex
│   ├── design/
│   │   └── ui-ux-pro-max/
│   ├── security/                  # Red Team, auditoria Supabase, RLS, pentest
│   │   ├── ethical-redteam/
│   │   ├── temp-mail-pentest/
│   │   ├── vuln-discovery/
│   │   ├── supabase-security/
│   │   └── vuln-hunt/
│   └── gh-cli/
├── assinafy/                      # Documentação oficial da API Assinafy (local)
├── assinafy-api/                  # Skill especialista na API Assinafy + references/evals
├── social-carousel/               # Gerador de carrosséis (HTML + Puppeteer + export + exemplos)
├── ollama-godmode/                # Técnicas de jailbreak e testes para Ollama Cloud
├── gerador-de-simulados/          # Geração de simulados/discursivas (Python)
├── cloudflare-workers/            # Referências e patterns para Cloudflare Workers
├── ready-to/                      # Skill de checklist pré-deploy
├── autoreview-agnostic/           # Autoreview para Claude Code e OpenCode
├── edital-verticalizado/          # Verticalização de editais de concursos públicos
├── servers/                       # Servidores MCP (Model Context Protocol)
│   └── supergithub/               # Gerenciador avançado de repositórios GitHub via API
├── scripts/                       # Scripts de validação local e sintaxe (Python/Shell/Node)
├── docs/                          # Documentação geral e guias de referência
│   └── reference/
├── Makefile                       # Suíte de automação (make check)
├── .env.example                   # Template de variáveis de ambiente
├── .gitignore                     # Filtros de segurança e arquivos locais
├── skills-lock.json               # Lockfile de dependências de skills
└── README.md
```

---

## 🧠 Habilidades Disponíveis

### ⚡ Automação & Integrações

| Skill | Status | Descrição |
|-------|--------|-----------|
| **[Cyberduck Expert](skills/automation/cyberduck-expert/SKILL.md)** | `Stable` | Automação e gestão de transferências FTP/SFTP/S3/WebDAV via duck CLI |
| **[N8N Skills](skills/automation/n8n-skills/SKILL.md)** | `Stable` | Construção e otimização de workflows automatizados no N8N |
| **[File Organization](skills/automation/file-organization/SKILL.md)** | `Stable` | Organização inteligente de arquivos e estruturas de diretórios |
| **[Assinafy API](assinafy-api/SKILL.md)** | `Stable` | Especialista na API de assinatura digital Assinafy (upload, signers, webhooks, templates) |
| **[Cloudflare Workers](cloudflare-workers/SKILL.md)** | `Stable` | Patterns, scaffolds e operações para aplicações serverless em Cloudflare Workers |
| **[Resend API](skills/automation/resend-api/SKILL.md)** | `Stable` | Automação especialista na API Resend para e-mails transacionais, gestão de domínios, chaves de API, webhooks, templates e contatos. |

### 🛠️ Agent Workflows & Dev Tools

| Skill | Status | Descrição |
|-------|--------|-----------|
| **[Skill Cleaner](skills/agent-workflows/skill-cleaner/SKILL.md)** | `Stable` | Auditoria e otimização do budget de tokens de skills no prompt do agente |
| **[Ready-to](ready-to/SKILL.md)** | `Stable` | Checklist diagnóstico pré-deploy e validações da codebase |
| **[Autoreview Agnostic](autoreview-agnostic/opencode/skills/autoreview/SKILL.md)** | `Stable` | Code review estruturado para Claude Code, OpenCode e agentes CLI |
| **[GitHub CLI Expert](skills/gh-cli/SKILL.md)** | `Stable` | Automação de operações no GitHub via `gh` CLI |
| **[Learn](skills/agent-workflows/learn/SKILL.md)** | `Stable` | Sistema de gestão de conhecimento incremental para o agente: analisa a sessão, classifica aprendizados, verifica duplicação/conflito e só aplica em `AGENTS.md`/Skills após aprovação explícita, com rollback individual por item |

### 🎨 Design & Conteúdo

| Skill | Status | Descrição |
|-------|--------|-----------|
| **[UI/UX Pro Max](skills/design/ui-ux-pro-max/SKILL.md)** | `Stable` | Design system completo com 50 estilos, paletas HSL e tipografia moderna |
| **[Social Carousel](social-carousel/SKILL.md)** | `Stable` | Geração de carrosséis cinematográficos para Instagram/LinkedIn/X (1080×1080) |
| **[Social Ads Creator](skills/content/social-ads-creator/SKILL.md)** | `Stable` | Criação de anúncios e estratégias de copy para redes sociais |
| **[Brazilian Official Docs](skills/content/brazilian-official-docs/SKILL.md)** | `Stable` | Formatação de documentos oficiais seguindo normas brasileiras |

### 🛡️ Segurança & Offensive AI

| Skill | Status | Descrição |
|-------|--------|-----------|
| **[Ethical Red Team](skills/security/ethical-redteam/SKILL.md)** | `Authorized` | Testes éticos de Red Team e Bug Bounty (OSINT, recon, port scan, relatórios OWASP) |
| **[Temp Mail Pentest](skills/security/temp-mail-pentest/SKILL.md)** | `Authorized` | Gestão de e-mails temporários em fluxos autorizados de pentest |
| **[Vuln Discovery](skills/security/vuln-discovery/SKILL.md)** | `Authorized` | Pipeline autônomo de descoberta de vulnerabilidades em 8 fases |
| **[Supabase Security](skills/security/supabase-security/SKILL.md)** | `Authorized` | Auditoria completa de segurança RLS, policies e JWT no Supabase |
| **[Vuln Hunt](skills/security/vuln-hunt/skills/vuln-discovery-pipeline/SKILL.md)** | `Authorized` | Pipeline com múltiplos agentes para auditoria massiva de código |
| **[Ollama Godmode](ollama-godmode/SKILL.md)** | `Research` | Testes de robustez e jailbreaks controlados para modelos Ollama Cloud |
| **[Godmode Agnostic](godmode-agnostic/SKILL.md)** | `Research` | Técnicas agnósticas de refinamento de comportamento para LLMs |

### 📜 Compliance, Educação & Concursos

| Skill | Status | Descrição |
|-------|--------|-----------|
| **[LGPD Checklist](skills/compliance/lgpd-checklist/SKILL.md)** | `Stable` | Checklists operacionais e conformidade legal com a LGPD |
| **[Gerador de Simulados](gerador-de-simulados/SKILL.md)** | `Stable` | Geração de simulados e questões de provas anteriores com exportação PDF |
| **[Edital Verticalizado](edital-verticalizado/SKILL.md)** | `Stable` | Verticalização e acompanhamento de editais de concursos públicos |

### ⚖️ Legal Skills (LegalSkillsBR)

Acervo de **2.149 skills jurídicas** em [`legalbr/`](legalbr/), compatível com a [Agent Skills Specification](https://agentskills.io/specification) (frontmatter `name` + `description` validado). Instalável via `npx skills add prof-ramos/skills`.

| Categoria | Skills | Descrição |
|-----------|-------:|-----------|
| [Formas](legalbr/forma/) | 299 | Minutas e peças processuais: petições iniciais, recursos, contestações, pareceres, contratos e decisões judiciais |
| [Administrativo](legalbr/materia/administrativo/) | 214 | Licitações, improbidade, concursos, servidores e controle social |
| [Tributário](legalbr/materia/tributario/) | 246 | Impostos, imunidades, FPE/FPM, execução fiscal e planejamento |
| [Penal](legalbr/materia/penal/) | 166 | Crimes, tipos penais e teses de defesa |
| [Processo Civil](legalbr/materia/processo-civil/) | 164 | Recursos, cumprimento de sentença, tutelas e procedimentos |
| [Trabalho](legalbr/materia/trabalho/) | 128 | Vínculo, terceirização, TAC/MPT e compliance trabalhista |
| [Processo Penal](legalbr/materia/processo-penal/) | 120 | Prisões, provas, recursos e nulidades |
| [Consumidor](legalbr/materia/consumidor/) | 106 | Relações de consumo, transporte aéreo e planos de saúde |
| [Previdenciário](legalbr/materia/previdenciario/) | 74 | Benefícios, aposentadorias e revisões |
| [Civil](legalbr/materia/civil/) | 66 | Obrigações, responsabilidade civil e contratos |
| [Constitucional](legalbr/materia/constitucional/) | 60 | Controle de constitucionalidade e direitos fundamentais |
| [Consultoria](legalbr/materia/consultoria/) | 59 | Pareceres e opiniões jurídicas |
| [Contratos](legalbr/materia/contratos/) | 59 | Elaboração, revisão e extinção contratual |
| [Bancário](legalbr/materia/bancario/) | 47 | Contratos bancários, tarifas e superendividamento |
| [Imobiliário](legalbr/materia/imobiliario/) | 47 | Compra e venda, locação e incorporação |
| [Empresarial](legalbr/materia/empresarial/) | 43 | Sociedades, falência e recuperação |
| [Família & Sucessões](legalbr/materia/familia-sucessoes/) | 39 | Inventário, guarda, alimentos e divórcio |
| [Saúde](legalbr/materia/saude/) | 37 | Planos de saúde, medicamentos e responsabilidade médica |
| [Ambiental](legalbr/materia/ambiental/) | 32 | Licenciamento, dano ambiental e responsabilidade |
| [Eleitoral](legalbr/materia/eleitoral/) | 27 | Registro de candidatura, prestação de contas e propaganda |
| [Digital & Dados](legalbr/materia/digital-dados/) | 27 | LGPD, crimes digitais e responsabilidade de plataformas |
| [Diversidade & DH](legalbr/materia/diversidade-dh/) | 26 | Direitos humanos, igualdade e antidiscriminação |
| [Societário](legalbr/materia/societario/) | 26 | Estatutos, assembleias e governança |
| [Internacional](legalbr/materia/internacional/) | 18 | Direito internacional público e privado |
| [Regulatório](legalbr/materia/regulatorio/) | 14 | Agências reguladoras e setores regulados |
| [Militar](legalbr/materia/militar/) | 5 | Direito penal e administrativo militar |

---

## 🛠️ Servidores MCP

| Servidor | Descrição | Linguagem / Protocolo |
|----------|-----------|-----------------------|
| **[SuperGitHub](servers/supergithub/SKILL.md)** | Gerenciamento avançado de repositórios, PRs e issues do GitHub via API | Python / Stdio MCP |

---

## 🚀 Como Usar

### 1. Instalação Direta via CLI `skills.sh` (Recomendado)

O ecossistema [`skills.sh`](https://skills.sh) permite instalar as habilidades diretamente na sua máquina ou ambiente de agente:

#### Skills Gerais e Ferramentas de Desenvolvedor (23 skills):
```bash
# Listar skills gerais disponíveis no repositório
npx skills add prof-ramos/skills --list

# Instalar skill específica (exemplo: resend-api)
npx skills add prof-ramos/skills@resend-api -a claude-code -y
```

#### LegalSkillsBR — 2.149 Skills Jurídicas Brasileiras:
```bash
# Listar todas as 2.149 skills jurídicas via subpath
npx skills add prof-ramos/skills/legalbr --list

# Instalar skill jurídica específica via subpath
npx skills add prof-ramos/skills/legalbr@acao-alimentos -a claude-code -y

# Instalar explorando toda a árvore do repositório via flag --full-depth
npx skills add prof-ramos/skills@acao-alimentos --full-depth -a claude-code -y

# Listar por matéria jurídica específica (ex: Tributário, 246 skills)
npx skills add prof-ramos/skills/legalbr/materia/tributario --list
```

### 2. Uso Local / Clonando o Repositório

```bash
# 1. Clone o repositório
git clone https://github.com/prof-ramos/skills.git
cd skills

# 2. Inspecione uma skill
cat skills/design/ui-ux-pro-max/SKILL.md

# 3. Configure as variáveis de ambiente base
cp .env.example .env
```

---

## 🧪 Testes & Validação

O repositório inclui uma suíte automatizada de checagem para garantir sintaxe válida e conformidade de frontmatter em todas as skills:

```bash
# Executar todas as validações (Python + Shell + Node + Frontmatter + KHAOS smoke)
make check
```

Output esperado:
```text
Python syntax OK (56 files)
Shell syntax OK (16 files)
Skill frontmatter & skills.sh.json OK (26 files, 0 warnings)
KHAOS smoke OK
```

---

## 🔄 Retomada após Formatação

Este repositório foi otimizado para permitir a retomada imediata do ambiente de desenvolvimento em máquinas limpas:

### Checklist Rápido pós-clone

1. **Clonar repositório:**
   ```bash
   git clone https://github.com/prof-ramos/skills.git && cd skills
   ```
2. **Requisitos de ambiente:**
   - **Python 3.10+** (necessário para `supergithub`, `ollama-godmode`, `gerador-de-simulados`)
   - **Node.js 20+ + npm** (necessário para `social-carousel`)
3. **Instalação de dependências dos subprojetos:**
   ```bash
   # Para o servidor SuperGitHub:
   cd servers/supergithub && pip install -r requirements.txt && cd ../..

   # Para o gerador de carrosséis:
   cd social-carousel && npm install && cd ..
   ```
4. **Variáveis de ambiente:**
   ```bash
   cp .env.example .env
   ```
   > [!WARNING]
   > **Nunca versione o arquivo `.env` real.** O arquivo `.gitignore` já está configurado para bloquear `.env`, `.venv`, `node_modules` e credenciais.

5. **Executar verificação global:**
   ```bash
   make check
   ```

---

## 📝 Contribuindo

Contribuições para novas skills e melhorias são super bem-vindas! Consulte o guia de contribuição em [CONTRIBUTING.md](CONTRIBUTING.md) antes de enviar um Pull Request.

---

## 📜 Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE) para mais detalhes.

<div align="center">
  <sub>Desenvolvido com 💚 por <a href="https://github.com/prof-ramos">Prof. Ramos</a></sub>
</div>
