<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2025-03-10 | Updated: 2026-03-30 -->

# scripts

## Purpose
Contém todos os módulos Python executáveis da skill de Red Team, cada um responsável por uma fase do teste de segurança: reconhecimento, enumeração de subdomínios, scanning, análise de web apps, análise de vulnerabilidades e geração de relatórios.

## Key Files

| File | Description |
|------|-------------|
| `recon.py` | Reconhecimento OSINT/DNS/IP — modos passive/active/full com 7 tipos de registro DNS |
| `subfinder.py` | Enumeração de subdomínios via ProjectDiscovery subfinder — bloqueio ético de TLDs governamentais |
| `scanner.py` | Scanning de portas/serviços — nmap com 3 perfis (quick/standard/deep) otimizados para M3 |
| `burp_mcp.py` | Web app scanner via Burp Suite MCP (Community) — análise passiva de proxy history, **probing ativo de caminhos sensíveis (requer autorização escrita)** |
| `analyzer.py` | Análise e correlação — consolida resultados, classifica por CVSS v3.1, base de conhecimento interna |
| `reporter.py` | Gerador de relatórios — Executivo + Técnico (MD) + PDF com hash integridade, Jinja2 templates |
| `utils.py` | Funções compartilhadas — logging, validação de autorização, salvar JSON, detectar ambiente |
| `install.sh` | Instalador inteligente — detecta Apple Silicon, instala 9 ferramentas Brew + 11 pacotes Python |
| `setup_burp_mcp.sh` | Setup do Burp Suite MCP — clone, build Gradle e instruções de configuração da extensão |
| `script.py` | Empacotador da skill — gera estrutura completa de diretórios e arquivos .zip |
| `script_1.py` | Gerador alternativo — versão de contingência para criar módulos da skill |

## For AI Agents

### Working In This Directory
- Todos os scripts Python são executáveis e começam com shebang `#!/usr/bin/env python3`
- Cada módulo pode ser executado independentemente ou em pipeline
- **OBRIGATÓRIO:** Usar `utils.exibir_disclaimer_e_validar()` antes de qualquer ação
- Output JSON é salvo com timestamp para rastreabilidade

### Module Execution Order (Standard Pipeline)
1. **recon.py** — Coleta informações passivas/ativas: subdomínios, DNS, WHOIS, geolocalização IP
2. **subfinder.py** — Enumeração de subdomínios via ProjectDiscovery (pode ser standalone ou integrado ao recon.py `--mode full`)
3. **burp_mcp.py** — Web app scanning via Burp Suite MCP (Community): análise passiva de proxy history + probing ativo de caminhos sensíveis
4. **scanner.py** — Varre portas/serviços: 3 perfis (quick=100 portas, standard=1000, deep=todas + NSE)
5. **analyzer.py** — Correlaciona achados: base conhecimento CVSS, severidade, recomendações OWASP
6. **reporter.py** — Gera relatório: executivo (management) + técnico (detalhamento) + PDF

> **Nota sobre ordenação:** `burp_mcp.py` executa antes de `scanner.py` pois trabalha com alvos web conhecidos (domínios/URLs do recon), não com resultados de port scan. Para análise de vulnerabilidades em portas específicas, use `analyzer.py` após `scanner.py`.

### Scanner Profiles (scanner.py) — M3 Optimized
| Profile | Ports | RAM | Timeout | Nmap Args | Use Case |
|---------|-------|-----|---------|-----------|----------|
| `quick` | Top 100 | ~200MB | 120s | `-sV -O --top-ports 100 -T3` | Recon rápido, redes grandes |
| `standard` | Top 1000 | ~512MB | 300s | `-sV -sC --top-ports 1000 -T3` | **Recomendado** — equilíbrio |
| `deep` | All 65535 | ~2GB | 600s | `-sV -sC -p- --script=vuln -T2` | Completo, alvos críticos |

### Recon Modes (recon.py)
| Mode | Contact | DNS Types | Techniques | Use Case |
|------|---------|-----------|------------|----------|
| `passive` | None | — | OSINT, WHOIS, geolocalização | **Fase inicial** — sem alertar |
| `active` | DNS queries | A/AAAA/MX/NS/TXT/SOA/CNAME | Enumeração DNS, resolver IPs | Após passive |
| `full` | DNS + HTTP | All 7 types | passive + active combinados | **Completo** em uma execução |

### Report Types (reporter.py)
| Report | Audience | Sections | Format | Purpose |
|--------|----------|----------|--------|---------|
| `executive` | Management/Non-technical | Risk overview, top findings, conclusion | MD | Stakeholder communication |
| `technical` | Security team | Full findings, CVSS, recommendations, evidence | MD | Remediation guidance |
| `full` | All parties | executive + technical combined | PDF (via MD) | Official deliverable |

**Report features:**
- Hash de integridade SHA-256 para não-repúdio
- Classificação CONFIDENCIAL automática
- Conformidade OWASP WSTG v4.2 e NIST SP 800-115
- Seções: achados por severidade, CVSS detalhado, evidências

### Subfinder Modes (subfinder.py)
| Mode | Sources | Description |
|------|---------|-------------|
| `all` | All available | Todas as fontes (padrão) — mais lento, mais completo |
| `rapid` | Fast sources only | Fontes rápidas apenas — para recon inicial |

**Ethical safeguards:** Bloqueio automático de TLDs governamentais (`.gov`, `.mil`, `.gov.br`, `.jus.br`, `.leg.br`, `.mp.br`, `.gc.ca`, `.gov.uk`, `.gob.mx`, `.gob.ar`, `.gov.au`, `.gov.in`, `.gov.my`, `.gov.sg`, `.gov.il`) via `RESTRICTED_TLDS`. A validação usa `dominio.endswith(tld)`, bloqueando subdomínios (ex: `portal.gov.br`).

### Burp MCP Modes (burp_mcp.py)
| Mode | Tipo | Description | Use Case |
|------|------|-------------|----------|
| `history` | **Passivo** | Análise passiva do proxy history do Burp | Após navegar no alvo com Burp como proxy |
| `active` | **Ativo** | Probing ativo de caminhos sensíveis (20+ paths) — requer autorização escrita | Enumeração de arquivos/configurações expostas |
| `full` | **Híbrido** | history + active combinados | **Recomendado** — máxima cobertura Community |

**Detecções por tipo:**

**Passivas (mode `history`):**
- Security headers ausentes (HSTS, CSP, X-Frame-Options, etc.)
- Cookies sem HttpOnly/Secure/SameSite
- Dados sensíveis em URLs (tokens, senhas, session IDs)
- CORS wildcard (`Access-Control-Allow-Origin: *`)
- Server version disclosure

**Ativas (mode `active` ou `full`):**
- Caminhos sensíveis: `/.git/HEAD`, `/.env`, `/admin`, `/phpinfo.php`, etc.
- Métodos HTTP perigosos (PUT, DELETE, TRACE) via OPTIONS

> **Nota:** Análise automática de SQLi/XSS requer Burp Pro (não usado aqui — apenas Community Edition).

### Output File Convention
- `recon_output/TARGET_recon_TIMESTAMP.json` — Dados brutos de reconhecimento
- `subfinder_output/TARGET_subfinder_TIMESTAMP.json` — Subdomínios enumerados
- `scan_output/TARGET_burp_mcp_TIMESTAMP.json` — Achados do web app scanner
- `scan_output/TARGET_scan_TIMESTAMP.json` — Resultados do nmap estruturados
- `analysis/TARGET_analysis_TIMESTAMP.json` — Achados consolidados com CVSS
- `reports/TARGET_executive_report.md` — Sumário para stakeholders
- `reports/TARGET_technical_report.md` — Detalhes técnicos para equipe de segurança

### Testing Requirements
- Testar cada módulo independentemente antes de usar em pipeline
- Validar output JSON schema antes de passar para próximo módulo

### Common Patterns
- Uso de `rich` para output colorido e tabelas formatadas
- Argumentos via `argparse` com `--help` documentado
- Salvar JSON com `salvar_json()` do utils

## Dependencies

### Internal
- `utils.py` — Todos os módulos importam funções compartilhadas:
  - `configurar_logger()` — Logging com arquivo (auditoria) + console
  - `exibir_disclaimer_e_validar()` — **OBRIGATÓRIO** — Valida autorização legal (3 questões)
  - `validar_alvo()` — Detecta tipo de alvo (IP/CIDR/domínio/URL) com regex
  - `detectar_ambiente()` — Detecta arch, OS, RAM para otimização M3
  - `salvar_json()` — Persiste resultados com timestamp em nome do arquivo
  - `calcular_severidade_cvss()` — Converte score 0-10 para Crítica/Alta/Média/Baixa/Informativa
  - `DISCLAIMER` — Constante com aviso legal LGPD/Marco Civil/CFAA

### External (install via `install.sh`)
**System packages (Homebrew):**
- nmap — Port scanning e detecção de serviços
- masscan — Scanner de alta velocidade
- dnsx — Resolução e enumeração DNS
- httpx — Probe HTTP/HTTPS
- nuclei — Scanner de vulnerabilidades baseado em templates
- subfinder — Enumeração de subdomínios
- amass — Mapeamento de superfície de ataque
- whatweb — Fingerprinting de tecnologias web
- gobuster — Enumeração de diretórios/DNS
- theHarvester — OSINT via pip

**Python packages (venv):**
- dnspython==2.6.1 — Consultas DNS
- shodan==1.31.0 — OSINT Shodan API
- requests==2.31.0 — HTTP client
- rich==13.7.1 — Terminal formatting
- reportlab==4.1.0 — PDF generation
- jinja2==3.1.4 — Template engine
- python-nmap==0.7.1 — Nmap wrapper
- ipwhois==1.3.0 — WHOIS queries
- beautifulsoup4==4.12.3 — HTML parsing

**Installation process:**
1. Validates Apple Silicon (arm64) vs Intel
2. Checks macOS 13+ (Ventura or later)
3. Installs Python 3.11+ if missing
4. Creates isolated venv at `.venv-redteam/`
5. Creates output directories: `logs/`, `reports/`, `scan_output/`, `recon_output/`, `analysis/`

## Code Conventions

### Authorização Legal (CRÍTICO)
```python
from utils import exibir_disclaimer_e_validar
if not exibir_disclaimer_e_validar(logger):
    sys.exit(1)  # Abortar se não autorizado
```

### Padrão de Output JSON
```python
from utils import salvar_json
resultado = {"target": "alvo.com", "findings": [...]}
caminho = salvar_json(resultado, "recon", "recon_output/")
# Salva: recon_output/recon_20250310_143052.json
```

### Validação de Alvo
```python
from utils import validar_alvo
info = validar_alvo("192.168.1.0/24")
# {'tipo': 'cidr', 'valor': '192.168.1.0/24', 'valido': True}
```

## JSON Data Structures

### recon.py Output Schema
```json
{
  "alvo": "exemplo.com",
  "modo": "full",
  "timestamp_inicio": "2025-03-10T14:30:00",
  "ambiente": {"arch": "arm64", "os": "Darwin", "ram_gb": 8.0},
  "dns": {"A": ["1.2.3.4"], "MX": ["mail.exemplo.com"]},
  "whois": {"registrant": "Org Name", "created": "2020-01-01"},
  "subdomains": ["www", "api", "staging"],
  "ips_encontrados": ["1.2.3.4", "5.6.7.8"],
  "osint": {"shodan": "...", "censys": "..."}
}
```

### scanner.py Output Schema
```json
{
  "alvo": "192.168.1.1",
  "perfil": "standard",
  "config_perfil": {"descricao": "...", "args": "..."},
  "hosts": [
    {
      "ip": "192.168.1.1",
      "ports": {
        "22/tcp": {"state": "open", "service": "ssh"},
        "80/tcp": {"state": "open", "service": "http"}
      },
      "os_match": ["Linux 5.x"]
    }
  ]
}
```

### analyzer.py Output Schema
```json
{
  "alvo": "exemplo.com",
  "timestamp_analise": "2025-03-10T15:00:00",
  "achados": [
    {
      "host": "192.168.1.1",
      "porta": 22,
      "servico": "SSH",
      "descricao": "SSH exposto publicamente",
      "cvss_score": 3.7,
      "severidade": "Baixa",
      "cve_ref": "CWE-284",
      "recomendacao": "Restringir acesso por IP"
    }
  ],
  "resumo": {"critica": 0, "alta": 1, "media": 2, "baixa": 3}
}
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `nmap not found` | nmap não instalado via Homebrew | `brew install nmap` |
| `Permission denied` install.sh | Arquivo sem permissão de execução | `chmod +x scripts/install.sh` |
| `Memory exceeded` | Scan `deep` em redes grandes | Reduza o range ou use `--profile standard` |
| `theHarvester timeout` | APIs externas lentas | Use `--mode passive --timeout 30` |
| `Module not found` | Venv não ativado | `source .venv-redteam/bin/activate` |
| `dnspython import error` | Dependências não instaladas | Rode `./scripts/install.sh` novamente |

## CVSS Scoring Reference

### Severity Classification (CVSS v3.1)
| Score Range | Severity | Color | Action Required |
|-------------|----------|-------|-----------------|
| 9.0 - 10.0 | Crítica | 🔴 Red | Immediate remediation (<24h) |
| 7.0 - 8.9 | Alta | 🟠 Orange | Urgent (within 7 days) |
| 4.0 - 6.9 | Média | 🟡 Yellow | Important (within 30 days) |
| 0.1 - 3.9 | Baixa | 🟢 Green | Routine (within 90 days) |
| 0.0 | Informativa | ⚪ White | No action needed |

### Common Service CVSS Scores (analyzer.py knowledge base)
| Port | Service | CVSS | Key Issue |
|------|---------|------|-----------|
| 21 | FTP | 7.5 | Cleartext transmission (CWE-319) |
| 22 | SSH | 3.7 | Public exposure (mitigate with keys/IP restriction) |
| 23 | Telnet | 9.8 | Cleartext + legacy (disable immediately) |
| 25 | SMTP | 6.5 | No auth/TLS (CWE-306) |
| 80 | HTTP | 5.3 | No encryption (redirect to HTTPS) |
| 3306 | MySQL | 8.8 | Database exposed (CWE-284) |
| 3389 | RDP | 9.8 | BlueKeep vulnerability (CVE-2019-0708) |
| 5432 | PostgreSQL | 8.8 | Database exposed (CWE-284) |
| 6379 | Redis | 9.8 | No auth by default (CWE-306) |
| 27017 | MongoDB | 9.8 | No auth by default (CWE-306) |

### Security Headers Recommendations (analyzer.py)
| Header | Recommendation | Purpose |
|--------|---------------|---------|
| `Server` | Remove/obfuscate | Hide technology stack |
| `X-Powered-By` | Remove | Don't reveal framework |
| `X-Frame-Options` | Add: DENY | Prevent Clickjacking |
| `X-Content-Type-Options` | Add: nosniff | Prevent MIME sniffing |
| `Strict-Transport-Security` | Add: max-age=31536000; includeSubDomains | Force HTTPS |
| `Content-Security-Policy` | Add restrictive policy | Prevent XSS |

<!-- MANUAL: -->
