<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2025-03-10 | Updated: 2025-03-10 -->

# examples

## Purpose
Diretório reservado para documentação adicional e exemplos de relatórios.

## For AI Agents

### Working In This Directory
- Arquivos de exemplo estão localizados no diretório pai `references/`
- Use exemplos apenas como referência de formatação e estrutura
- Dados nos exemplos são fictícios — não usar em testes reais

## Related Files

| File (in parent) | Description |
|------------------|-------------|
| `../sample-report.md` | Exemplo de relatório com dados fictícios para formatação |
| `../report-template.md` | Template padrão para relatórios com seções obrigatórias |

## Sample Report Contents

The `sample-report.md` demonstrates a complete security report with:

| Section | Content Example |
|---------|------------------|
| **Risk Overview** | Overall risk level (High/Medium/Low) |
| **Findings Distribution** | Critical (🔴), High (🟠), Medium (🟡), Low (🟢) counts |
| **Finding #1** | Redis without auth (CVSS 9.8) — host, port, evidence, recommendation |
| **Finding #2** | Telnet enabled (CVSS 9.8) — banner, migration to SSH |
| **Finding #3** | HTTP without HTTPS (CVSS 5.3) — TLS implementation needed |

**Key Elements Demonstrated:**
- SHA-256 integrity hash for non-repudiation
- Fictitious network (192.168.100.0/24) for educational purposes
- Clear evidence format (command output, banners)
- Actionable recommendations with specific configurations
- CVSS v3.1 scoring for severity classification

<!-- MANUAL: -->
