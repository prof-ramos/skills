# Checklist OWASP Testing Guide v4.2 + NIST SP 800-115

> Referência para cobertura metodológica dos testes de segurança.

## OWASP Top 10 (2021) — Verificações por Módulo

| ID | Categoria | Módulo da Skill | Verificações |
|----|-----------|-----------------|--------------|
| A01 | Broken Access Control | scanner + analyzer | Exposição de endpoints autenticados, IDOR |
| A02 | Cryptographic Failures | recon + scanner | HTTP sem TLS, cifras fracas, FTP/Telnet aberto |
| A03 | Injection | scanner (NSE scripts) | SQLi via nmap NSE, cabeçalhos de erro |
| A04 | Insecure Design | analyzer | Análise de arquitetura baseada nos achados |
| A05 | Security Misconfiguration | scanner + analyzer | Cabeçalhos HTTP, portas desnecessárias, banners |
| A06 | Vulnerable Components | scanner (versões) | Versões detectadas vs CVEs conhecidos |
| A07 | Auth Failures | scanner | Serviços sem auth (Redis, MongoDB, FTP anon) |
| A08 | Software Integrity Failures | recon | Subdomínios não autorizados, takeover |
| A09 | Logging Failures | (manual) | Verificar se sistema loga adequadamente |
| A10 | SSRF | recon (HTTP) | Cabeçalhos de resposta, redirecionamentos |

---

## NIST SP 800-115 — Fases de Teste

### Fase 1: Planejamento
- [ ] Definir escopo e objetivos
- [ ] Obter autorização formal
- [ ] Identificar restrições operacionais

### Fase 2: Descoberta (recon.py)
- [ ] Reconhecimento de rede passivo
- [ ] Identificação de hosts ativos
- [ ] Enumeração de serviços
- [ ] Identificação de vulnerabilidades

### Fase 3: Ataque (scanner.py)
- [ ] Exploração controlada de vulnerabilidades
- [ ] Escalação de privilégios (se autorizado)
- [ ] Pivotamento (se autorizado no escopo)

### Fase 4: Relatório (reporter.py)
- [ ] Documentar todas as vulnerabilidades
- [ ] Classificar por severidade (CVSS)
- [ ] Fornecer recomendações acionáveis
- [ ] Revisão de qualidade

---

## CVSS v3.1 — Escala de Severidade

| Score | Severidade | Cor | SLA Recomendado |
|-------|-----------|-----|-----------------|
| 9.0–10.0 | Crítica | 🔴 | 24-48 horas |
| 7.0–8.9 | Alta | 🟠 | 7 dias |
| 4.0–6.9 | Média | 🟡 | 30 dias |
| 0.1–3.9 | Baixa | 🟢 | 90 dias |
| 0.0 | Informativa | ⚪ | Próximo ciclo |

---

## Referências

- [OWASP Testing Guide v4.2](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800/115/final)
- [CVSS v3.1 Specification](https://www.first.org/cvss/specification-document)
- [OWASP Top 10 2021](https://owasp.org/Top10/)
