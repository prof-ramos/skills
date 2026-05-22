<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2025-03-10 | Updated: 2025-03-10 -->

# references

## Purpose
Documentação de referência legal e metodológica para garantir que testes de segurança sejam conduzidos de forma ética e conforme padrões da indústria (OWASP, NIST).

## Key Files

| File | Description |
|------|-------------|
| `ethics-guide.md` | Guia completo de ética e conformidade legal — leis brasileiras (LGPD, Carolina Dieckmann, Marco Civil) e internacionais (CFAA) |
| `owasp-checklist.md` | Checklist baseado em OWASP WSTG v4.2 para cobertura metodológica completa |
| `report-template.md` | Template padrão para relatórios de segurança com seções obrigatórias |
| `sample-report.md` | Exemplo de relatório com dados fictícios para formatação e estrutura |

## Legal Framework Summary

### Brazilian Laws
| Law | Scope | Key Points |
|------|-------|------------|
| **Lei 12.737/2012** (Carolina Dieckmann) | Invasão de dispositivos | Art. 154-A: invasão ilegal = 3 meses a 1 ano prisão |
| **Lei 12.965/2014** (Marco Civil Internet) | Responsabilidade ISPs | Neutralidade, privacidade, retenção de dados |
| **Lei 13.709/2018** (LGPD) | Proteção de dados pessoais | Multas até 2% do faturamento |
| **Código Penal Art. 154-A** | Acesso não autorizado | Invasão de dispositivo alheio |

### International Laws
| Law | Country | Scope |
|------|---------|-------|
| **CFAA** | EUA | Computer Fraud and Abuse Act |
| **Computer Misuse Act** | UK | Acesso não autorizado a sistemas |
| **GDPR** | EU | Proteção de dados (similar à LGPD) |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `examples/` | Documentação adicional e exemplos de uso — veja `examples/AGENTS.md` |

## For AI Agents

### Working In This Directory
- Estes documentos são **referência apenas** — não contêm código executável
- Ao orientar usuários sobre testes de segurança, sempre referenciar `ethics-guide.md`
- O checklist OWASP garante cobertura adequada dos testes

### Legal Compliance
Antes de qualquer teste, o usuário deve confirmar:
1. Autorização escrita do proprietário do sistema
2. Escopo do teste claramente definido
3. Rules of Engagement (RoE) documentados

### Methodology
- OWASP WSTG (Web Security Testing Guide) — padrão para testes web
- NIST SP 800-115 — guía técnica para avaliação de segurança
- CVSS v3.1 — sistema de pontuação de severidade

## Report Template Structure

The `report-template.md` follows industry-standard security report format:

| Section | Content | Audience |
|---------|---------|----------|
| **1. Executive Summary** | Business risk overview, key findings | Management |
| **2. Methodology** | Framework, tools, timeline (OWASP/NIST) | All stakeholders |
| **3. Detailed Findings** | Each vulnerability with CVSS, evidence, remediation | Technical team |
| **4. Consolidated Recommendations** | Prioritized action items (Immediate/Short/Medium term) | All stakeholders |
| **5. Conclusion** | Security maturity assessment, next steps | Management |

### Report Integrity Features
- **SHA-256 Hash** — Non-repudiation of report contents
- **Classification** — CONFIDENTIAL marking for restricted access
- **Timestamp** — ISO format for audit trail
- **Reference Number** — REF-YYYY-NNN format for tracking
- **SLA Recommendations** — Time-based remediation priorities

### Finding Format (per vulnerability)
```
ID: FIND-001
CVSS: X.X (Crítica/Alta/Média/Baixa)
CWE/CVE: CWE-XXX / CVE-YYYY-XXXX
Host: 192.168.1.1:22
Evidence: [command output / screenshot]
Impact: [Business impact description]
Recommendation: [Actionable remediation steps]
References: [OWASP/NIST links]
```

## OWASP Coverage

The `owasp-checklist.md` maps security testing to OWASP Top 10 (2021):

| OWASP Category | Skill Module | Coverage |
|---------------|--------------|----------|
| **A01: Broken Access Control** | scanner + analyzer | IDOR, endpoint exposure detection |
| **A02: Cryptographic Failures** | recon + scanner | HTTP without TLS, weak ciphers |
| **A03: Injection** | scanner (NSE) | SQLi detection via nmap scripts |
| **A04: Insecure Design** | analyzer | Architecture analysis from findings |
| **A05: Security Misconfiguration** | scanner + analyzer | HTTP headers, unnecessary ports |
| **A06: Vulnerable Components** | scanner | Version detection vs known CVEs |
| **A07: Authentication Failures** | scanner | Unauth services (Redis, MongoDB, FTP) |
| **A08: Software Integrity** | recon | Unauthorized subdomains, takeover |
| **A09: Logging Failures** | (manual) | System logging verification |
| **A10: Server-Side Request Forgery** | recon (HTTP) | Response headers, redirects |

### NIST SP 800-115 Testing Phases

| Phase | Module | Activities |
|-------|--------|------------|
| **1. Planning** | — | Scope definition, authorization |
| **2. Discovery** | recon.py | Passive recon, host identification, service enumeration |
| **3. Attack** | scanner.py | Controlled exploitation, privilege escalation (authorized) |
| **4. Reporting** | reporter.py | Documentation, classification, recommendations |

<!-- MANUAL: -->
