<!-- Generated: 2025-03-10 | Updated: 2026-03-30 -->

# ethical-redteam-skill

## Purpose
Ethical Red Team & Bug Bounty Skill para AI agents — uma skill profissional para conduzir testes de segurança autorizados (Red Team / Bug Bounty) com reconhecimento OSINT, scanning de portas, análise de vulnerabilidades, web app scanning via Burp Suite MCP e geração de relatórios conformes com OWASP/NIST.

## Key Files

| File | Description |
|------|-------------|
| `SKILL.md` | Metadados da skill (frontmatter YAML) + instruções completas de uso — triggers, workflow, troubleshooting |
| `README.md` | Documentação completa do projeto com instruções de instalação e uso |
| `llm.txt` | Contexto resumido do projeto para consumo por LLMs (versão compacta do README) |
| `check-deps.sh` | Verificador de dependências — valida TOR, Python, nmap, subfinder, sherlock, Burp MCP (15+ checks) |
| `requirements.txt` | Dependências Python (dnspython, requests, rich, python-nmap, sherlock-project, reportlab, etc.) |
| `.gitignore` | Exclusões para Python, macOS, e diretórios de output |
| `coderabbit.yaml` | Configuração do CodeRabbit para code review automatizado |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `scripts/` | Módulos Python de segurança (recon, scanner, analyzer, reporter, burp_mcp, subfinder) — veja `scripts/AGENTS.md` |
| `references/` | Documentação de ética, conformidade OWASP/NIST, templates e exemplos — veja `references/AGENTS.md` |
| `docs/` | Diagramas de fluxo, análise Pareto e documentação de workflow — veja `docs/AGENTS.md` |
| `hooks/` | Hooks de ciclo de vida (on_start, on_end) para inicialização/cleanup de serviços — veja `hooks/AGENTS.md` |

## For AI Agents

### Working In This Directory
- **CRÍTICO:** Esta skill é exclusivamente para testes de segurança **autorizados** em ambientes controlados
- Antes de executar qualquer módulo, SEMPRE validar autorização escrita do proprietário do alvo
- Todos os scripts Python requerem Python 3.11+ e estão localizados em `scripts/`
- O instalador automático está em `scripts/install.sh`

### Testing Requirements
- Testar apenas em ambientes autorizados (lab próprio, bug bounty programs, contratos formais)
- Usar alvos de teste como `testphp.vulnweb.com` para validação de ferramentas

### Common Patterns
- Fluxo típico: Recon → Scanner → Analyzer → Reporter
- Output JSON é gerado em diretórios timestamped para rastreabilidade
- Relatórios incluem hash de integridade para não-repúdio

### Typical Workflow Example
```bash
# 1. Activate environment
source .venv-redteam/bin/activate

# 2. Passive reconnaissance (no direct contact)
python scripts/recon.py --target example.com --mode passive --output recon_output/

# 3. Port scanning with standard profile
python scripts/scanner.py --target 192.168.1.1 --profile standard --output scan_output/

# 4. Analyze findings with CVSS scoring
python scripts/analyzer.py --scan scan_output/example_scan_*.json --output analysis/

# 5. Generate professional reports
python scripts/reporter.py --analysis analysis/example_analysis_*.json --target "Example Corp" --tester "Security Team" --output reports/
```

### Quick Reference
| Module | Input | Output | Time |
|--------|-------|--------|------|
| recon.py | domain/IP | JSON with DNS, WHOIS, subdomains | 1-5 min |
| subfinder.py | domain | JSON with enumerated subdomains | 2-10 min |
| burp_mcp.py | URL (via Burp proxy) | JSON with web app findings | 2-15 min |
| scanner.py | IP/CIDR | JSON with open ports, services | 2-15 min |
| analyzer.py | scan JSON | JSON with CVSS-scored findings | <1 min |
| reporter.py | analysis JSON | MD + PDF reports | <1 min |

### Best Practices for Ethical Pentesting

| Principle | Description |
|-----------|-------------|
| **Authorization First** | Never test without written permission |
| **Scope Adherence** | Stay within authorized targets |
| **Minimum Impact** | Prefer passive recon, avoid DoS |
| **Documentation** | Log all actions for audit trail |
| **Responsible Disclosure** | Report findings privately, allow remediation |
| **Continuous Learning** | Stay updated on CVEs, techniques, laws |

### Testing Environments
| Environment | Use Case | Targets |
|-------------|----------|---------|
| **Local Lab** | Learning, tool testing | `localhost`, VMs |
| **Bug Bounty** | Authorized programs | HackerOne, Intigriti |
| **Contractual** | Client engagements | Contract-specified |
| **Online Labs** | Practice | HackTheBox, TryHackMe |

## Dependencies

### External
- Python 3.11+ — Módulos em Python
- nmap — Scanning de portas (via Homebrew)
- python-nmap, dnspython, ipwhois, requests, rich, jinja2 — Dependências Python

### Internal
- `scripts/utils.py` — Funções compartilhadas usadas por todos os módulos

## Installation via skills.sh

```bash
npx skills add prof-ramos/ethical-redteam-skill
```

### Contributing

Contribuições são bem-vindas! O projeto aceita:

| Tipo | Exemplos |
|------|----------|
| **Bug fixes** | Correções de código, documentação |
| **New modules** | Novas técnicas de recon/scanning |
| **Enhancements** | Melhorias em performance, UX |
| **Documentation** | Traduções, guias, exemplos |

**Pull Request Process:**
1. Fork o repositório
2. Crie branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m "feat: adiciona nova funcionalidade"`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra PR descrevendo as mudanças

**Code Style:**
- Python: seguir PEP 8
- Bash: usar ShellCheck
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`)

### Versioning

Este projeto segue [Semantic Versioning 2.0.0](https://semver.org/):

| Version | Type | Description |
|---------|------|-------------|
| `1.0.0` | Major | Versão inicial estável |
| `1.1.0` | Minor | Novos módulos, features (backward compatible) |
| `1.1.1` | Patch | Bug fixes, documentação |
| `2.0.0` | Major | Breaking changes |

**Changelog Format:**
```markdown
## [1.1.0] - 2025-03-15
### Added
- New module: vuln_scanner.py for CVE detection
- Support for custom report templates

### Fixed
- Memory leak in deep scan mode
- JSON encoding for special characters

### Changed
- Improved timeout handling for slow networks
```

### Roadmap

| Version | Features | Status |
|---------|----------|--------|
| `1.0.0` | ✅ Initial release with recon, scanner, analyzer, reporter | Released |
| `1.1.0` | 🔄 Web UI for results visualization, PDF export improvements | Planned |
| `1.2.0` | 📋 Advanced exploitation module, Metasploit integration | Planned |
| `2.0.0` | 📋 Multi-language support (English, Portuguese), API mode | Future |

**Upcoming Features:**
- [ ] Integration with Shodan API for passive recon
- [ ] Support for IPv6 targets
- [ ] Custom report templates (Jinja2)
- [ ] Docker container for isolated testing
- [ ] CI/CD pipeline integration
- [ ] Slack/Teams notifications for findings

### SKILL.md Format (skills.sh)

O arquivo `SKILL.md` usa frontmatter YAML para metadados:

```yaml
---
name: ethical-redteam-bugbounty
description: Conduz testes de segurança éticos...
license: MIT
compatibility: macOS 13+, Python 3.11+, Homebrew
metadata:
  author: Ethical RedTeam Skill
  version: 1.0.0
  category: security
  tags: [redteam, bugbounty, pentest, osint, security, owasp, nist]
---
```

**Required fields for skills.sh:**
- `name` — Identificador único da skill
- `description` — Explicação do que a skill faz (inclui triggers de uso)
- `license` — Licença do código (MIT, Apache-2.0, etc.)
- `compatibility` — Requisitos de sistema
- `metadata.tags` — Palavras-chave para descoberta na plataforma

<!-- MANUAL: Notas do projeto podem ser adicionadas abaixo desta linha -->
