# 🚀 Agentic Skills & MCP Repository

Repositório centralizado para **Agent Skills** customizadas e servidores **Model Context Protocol
(MCP)**. Segue a [especificação oficial Agent Skills](https://agentskills.io/specification).

## 📁 Estrutura do Projeto

```text
.
├── skills/                  # Skills organizadas por categoria
│   ├── automation/          # Automação e integração
│   │   ├── cyberduck-expert/
│   │   ├── n8n-skills-2.1.1/
│   │   └── shopee-affiliate-automation/
│   ├── compliance/          # Conformidade jurídica e técnica
│   │   └── lgpd-checklist/
│   ├── content/             # Documentação e conteúdo
│   │   ├── brazilian-official-docs/
│   │   └── social-ads-creator/
│   ├── agent-workflows/     # Workflows e automação de agentes
│   │   └── skill-cleaner/
│   ├── design/              # UI/UX e design
│   │   └── ui-ux-pro-max/
│   └── security/            # Red teaming e segurança ofensiva
│       ├── ethical-redteam/
│       ├── vuln-discovery/
│       └── vuln-hunt/
├── servers/                 # Servidores MCP
│   └── supergithub/         # Gerenciador de repositórios GitHub
├── docs/                    # Documentação e referências
│   └── reference/           # Spec oficial e templates
├── dist/                    # Arquivos de distribuição
└── README.md
```

## 🧠 Habilidades Disponíveis

### Automação

| Skill | Descrição |
|-------|-----------|
| **Cyberduck Expert** | Automação e gestão de transferências FTP/SFTP/S3 |
| **N8N Skills** | Workflows e automação com N8N |
| **Shopee Affiliate** | Automação para programa de afiliados Shopee |

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
git clone https://github.com/prof-ramos/skills-gfcr.git
cd skills-gfcr/skills/design/ui-ux-pro-max
cat SKILL.md
```

## 📝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para instruções sobre como criar novas skills.

## 📚 Referências

- [Agent Skills Specification](https://agentskills.io/specification)
- [Template de Skill](docs/reference/official-skills/template/SKILL.md)

## 📜 Licença

[MIT License](LICENSE)
