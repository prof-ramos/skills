# 🚀 Agentic Skills & MCP Repository

Repositório centralizado para **Agent Skills** customizadas e servidores **Model Context Protocol
(MCP)**. Segue a [especificação oficial Agent Skills](https://agentskills.io/specification).

## 📁 Estrutura do Projeto

```text
.
├── skills/                        # Skills organizadas por categoria (principal)
│   ├── automation/                # Automação, integrações, utilitários
│   │   ├── cyberduck-expert/
│   │   ├── n8n-skills-2.1.1/
│   │   ├── shopee-affiliate-automation/
│   │   └── file-organization/     # (promovido em backup)
│   ├── compliance/
│   │   └── lgpd-checklist/
│   ├── content/
│   │   ├── brazilian-official-docs/
│   │   └── social-ads-creator/
│   ├── agent-workflows/     # Workflows e automação de agentes
│   │   └── skill-cleaner/
│   ├── design/              # UI/UX e design
│   │   └── ui-ux-pro-max/
│   ├── security/
│   │   ├── ethical-redteam/
│   │   ├── vuln-discovery/
│   │   └── vuln-hunt/
│   └── Instagram-Carousel/        # Exemplos de carrosséis HTML prontos
├── asof-design-system/            # Design System completo ASOF (cores, fontes, UI kits, previews)
├── assinafy/                      # Documentação oficial da API Assinafy (local)
├── assinafy-api/                  # Skill especialista na API Assinafy + references/evals
├── carrossel-instagram/           # Gerador de carrosséis (HTML + Puppeteer + export)
├── ollama-godmode/                # Técnicas de jailbreak para Ollama Cloud
├── gerador_de_simulados/          # Geração de simulados/discursivas (Python)
├── cloudflare-workers/            # Referências e patterns para Cloudflare Workers
├── ready-to/                      # Skill de checklist pré-deploy
├── servers/                       # Servidores MCP
│   └── supergithub/               # Gerenciador avançado de repositórios GitHub
├── docs/                          # Documentação e referências
│   └── reference/
├── .env.example                   # Template de variáveis de ambiente (sempre usar!)
├── .gitignore                     # Reforçado para segurança (nunca versiona .env real, estado local, etc.)
├── skills-lock.json
└── README.md
```

> **Nota importante:** Diretórios `.omc/`, `.grok/`, `.agents/`, `node_modules/`, `.venv/`, `*.zip`, `*.log`, builds e `.env` reais **NÃO** são versionados (veja `.gitignore` atualizado e seção de Retomada).
```

## 🧠 Habilidades Disponíveis

### Adicionais / Em desenvolvimento (preservados no backup)

- **Instagram Carousel** — Exemplos prontos de carrosséis HTML para Instagram (ASOF).
- **Ready-to** — Skill de checklist diagnóstico pré-deploy / format.
- **Gerador de Simulados** — Geração de provas discursivas e PDFs a partir de editais.
- **Ollama Godmode** — Jailbreaks e técnicas avançadas para modelos Ollama Cloud.
- **Cloudflare Workers** — Patterns, references e scaffold para Workers.

### Automação

| Skill | Descrição |
|-------|-----------|
| **Cyberduck Expert** | Automação e gestão de transferências FTP/SFTP/S3 |
| **N8N Skills** | Workflows e automação com N8N |
| **Shopee Affiliate** | Automação para programa de afiliados Shopee |
| **File Organization** | Organização de arquivos e pastas (utilitário) |
| **Assinafy API** | Especialista na API de assinatura digital Assinafy (upload, signers, webhooks, templates) |

### Conteúdo

| Skill | Descrição |
|-------|-----------|
| **Brazilian Official Docs** | Documentos oficiais seguindo normas brasileiras |
| **Social Ads Creator** | Criação de anúncios para redes sociais |

### Agent Workflows

| Skill | Descrição |
|-------|-----------|
| **Skill Cleaner** | Auditoria e otimização do budget de skills no prompt de agentes AI |

### Design

| Skill | Descrição |
|-------|-----------|
| **UI/UX Pro Max** | Design system com 50 estilos, paletas, tipografia |
| **ASOF Design System** | Design system completo para ASOF (cores, fontes WOFF2, logos, UI kits intranet, previews HTML) |
| **Social Carousel** | Geração de carrosséis para Instagram/LinkedIn/X (3 painéis cinematográficos 1080×1080) |

### Segurança

| Skill | Descrição |
|-------|-----------|
| **Ethical Red Team** | Red Team e Bug Bounty autorizado para agentes de IA |
| **Vuln Discovery** | Pipeline autônomo de descoberta de vulnerabilidades em 8 fases |
| **Vuln Hunt** | Automação de varreduras de segurança e caça a falhas |

### Compliance / Legal

| Skill | Descrição |
|-------|-----------|
| **LGPD Checklist** | Checklist e base legal em conformidade com a LGPD |

## 🛠️ Servidores MCP

| Servidor | Descrição |
|----------|-----------|
| **SuperGitHub** | Gerenciamento avançado de repositórios GitHub via API |

## 🚀 Como Usar

1. Clone este repositório
2. Navegue até a skill desejada em `skills/`
3. Leia o arquivo `SKILL.md` para instruções

```bash
git clone https://github.com/prof-ramos/skills.git
cd skills
# Exemplo
cat skills/design/ui-ux-pro-max/SKILL.md
# ou
cat ollama-godmode/SKILL.md
```

## 📝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para instruções sobre como criar novas skills.

## 📚 Referências

- [Agent Skills Specification](https://agentskills.io/specification)
- [Template de Skill](docs/reference/official-skills/template/SKILL.md)

## 🔄 Retomada após formatação

Este repositório foi preparado para que você possa **formatar o computador e retomar o desenvolvimento exatamente do mesmo ponto**, sem perder código-fonte, documentação, scripts, schemas ou instruções.

### Passo a passo para retomar (após `git clone`)

1. **Clone o repositório**
   ```bash
   git clone https://github.com/prof-ramos/skills.git
   cd skills
   git checkout main
   ```

2. **Versões recomendadas**
   - Python 3.10+ (para scripts em `servers/`, `ollama-godmode/`, `gerador_de_simulados/`)
   - Node.js 20+ + npm (para `carrossel-instagram/`)
   - Git + GitHub CLI (opcional, útil com `servers/supergithub`)
   - (Opcional) Docker se alguma skill evoluir para containers

3. **Instalar dependências**
   - Para o servidor GitHub:
     ```bash
     cd servers/supergithub
     pip install -r requirements.txt
     cd ../..
     ```
   - Para o gerador de carrosséis (Puppeteer + Chromium gerenciado):
     ```bash
     cd carrossel-instagram
     npm install
     cd ..
     ```
   - Demais skills são majoritariamente Markdown + scripts auto-contidos (leia o `SKILL.md` correspondente).

4. **Configurar variáveis de ambiente (OBRIGATÓRIO para skills que usam APIs)**
   ```bash
   cp .env.example .env
   # Edite .env com seus valores reais (NUNCA commite o .env real)
   ```
   Principais variáveis (veja `.env.example` e os `SKILL.md`):
   - `GH_TOKEN` — GitHub Personal Access Token (para `supergithub`)
   - `ASSINAFY_API_KEY`, `ASSINAFY_ACCOUNT_ID`, `ASSINAFY_BASE_URL`, `ASSINAFY_WEBHOOK_SECRET` — para a skill Assinafy

5. **Como usar as skills**
   - Cada skill tem um `SKILL.md` com frontmatter (name, description, triggers) e instruções detalhadas.
   - A maioria é consumida por agentes (Claude Code + OMC / Grok etc.) que leem o arquivo quando o nome/trigger é mencionado.
   - Para skills com scripts: leia o `QUICKSTART.md`, `README.md` ou o próprio `SKILL.md` da pasta.

6. **Preparar banco de dados / dados locais**
   - Este projeto **não possui migrations nem banco de dados** central.
   - Algumas skills usam arquivos locais (ex: `gerador_de_simulados/examples/`, `asof-design-system/assets/`, `assinafy/assinafy-api-docs/`).
   - Tudo que é necessário já está versionado.

7. **Executar em desenvolvimento / usar**
   - Skills de documentação e referência: abra o `SKILL.md`.
   - `servers/supergithub`: siga `QUICKSTART.md` ou `README.md` (export GH_TOKEN primeiro).
   - `carrossel-instagram`: rode o `index.html` diretamente ou use `export.js` + Puppeteer conforme o skill.
   - `ollama-godmode`: scripts Python auto-contidos (veja `SKILL.md`).
   - `asof-design-system`: abra os HTMLs em `preview/` e `ui_kits/intranet/` (use as fontes e CSS locais).

8. **Rodar testes**
   - `servers/supergithub`: `python -m pytest` ou `python test_github_manager.py` (requer GH_TOKEN válido).
   - Outras skills: verifique dentro do `SKILL.md` ou pasta (muitas são prompt-driven, sem testes automatizados tradicionais).

9. **Build / Geração de artefatos**
   - Carrosséis: o skill produz HTML estático (pode usar Puppeteer para screenshot/PDF se configurado).
   - Gerador de simulados: rode o script Python correspondente.
   - Design system: os previews HTML são estáticos (basta abrir no browser).
   - Não há build step global.

10. **Deploy / Publicação**
    - A maioria das skills é para uso local com agentes de IA (Claude, Grok, etc.).
    - `cloudflare-workers/`: use os patterns para fazer deploy manual em Workers.
    - `servers/supergithub`: roda localmente como CLI/tooling.
    - Para skills que geram HTML (carrossel, design): o artefato gerado é o próprio HTML (pronto para colar em post ou hospedar estático).

11. **Observações de segurança e o que NÃO está no GitHub**
    - **Nunca versionado (por design e .gitignore atualizado)**:
      - `.env`, `.env.local`, `.env.production` etc. (use sempre `.env.example`)
      - `.omc/`, `.grok/`, `.agents/` (estado local do OMC/Grok, paths da máquina, sessões, memory — foram removidos do index neste backup)
      - `node_modules/`, `.venv/`, `venv/`, `__pycache__/`
      - `*.zip`, `*.tar.*`, dumps SQL, `.bak`, `.db`, `.sqlite*`
      - `.DS_Store`, logs, caches, builds (`dist/`, `build/`, `.next/` etc.)
      - Qualquer arquivo `.pem`, `.key`, credenciais reais, screenshots grandes não essenciais.
    - Se após o clone você vir avisos de arquivos grandes ou binários, rode `git lfs install` (caso use LFS no futuro) ou simplesmente não os adicione.
    - O `.gitignore` foi reforçado durante a preparação deste backup.

12. **Checklist rápido pós-clone**
    - [ ] `cp .env.example .env` + preencher
    - [ ] Instalar deps dos subprojetos que você for usar (npm / pip)
    - [ ] Exportar `GH_TOKEN` se for usar o supergithub
    - [ ] Ler o `SKILL.md` da skill desejada
    - [ ] Para carrosséis ou design: abrir os `.html` no navegador

Qualquer dúvida sobre retomada: abra o `SKILL.md` relevante ou o `README.md` da subpasta.

## 📜 Licença

[MIT License](LICENSE)
