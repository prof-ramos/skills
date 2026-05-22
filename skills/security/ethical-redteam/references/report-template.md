# Relatório de Segurança — [NOME DO ALVO]

> ⚠️ CONFIDENCIAL — Uso restrito às partes autorizadas

**Data:** [DATA]
**Alvo:** [NOME/IP DO ALVO]
**Responsável:** [NOME DO TESTADOR]
**Número do Relatório:** [REF-YYYY-NNN]
**Hash de Integridade:** `[HASH SHA-256]`

---

## 1. Sumário Executivo

[Descrição em linguagem não técnica do estado geral de segurança do alvo,
destacando os riscos mais críticos e o impacto potencial ao negócio.]

### Distribuição de Achados

| Severidade | Quantidade | SLA Recomendado |
|-----------|-----------|-----------------|
| 🔴 Crítica | X | 24-48 horas |
| 🟠 Alta | X | 7 dias |
| 🟡 Média | X | 30 dias |
| 🟢 Baixa | X | 90 dias |
| ⚪ Informativa | X | Próximo ciclo |

---

## 2. Metodologia

- **Framework:** OWASP Testing Guide v4.2 + NIST SP 800-115
- **Período:** [DATA INÍCIO] a [DATA FIM]
- **Tipo de teste:** [Black Box / Grey Box / White Box]
- **Ferramentas:** nmap, subfinder, theHarvester, nuclei

---

## 3. Achados Detalhados

### 3.1 [TÍTULO DO ACHADO] — [SEVERIDADE]

| Campo | Valor |
|-------|-------|
| **ID** | FIND-001 |
| **CVSS Score** | X.X |
| **CWE/CVE** | CWE-XXX |
| **Host/Serviço** | [HOST:PORTA] |
| **Framework** | OWASP AXX:2021 |

**Descrição:**
[Descrição técnica clara da vulnerabilidade.]

**Evidência:**
```
[Saída de comando / screenshot / log que comprova a vulnerabilidade]
```

**Impacto:**
[Impacto potencial ao negócio se explorada.]

**Recomendação:**
[Passos concretos e acionáveis para correção.]

**Referências:**
- [Link para documentação OWASP/NIST relevante]

---

## 4. Recomendações Consolidadas

### Ações Imediatas (24-48h)
- [ ] [Ação crítica 1]

### Curto Prazo (7 dias)
- [ ] [Ação alta 1]

### Médio Prazo (30 dias)
- [ ] [Ação média 1]

---

## 5. Conclusão

[Conclusão geral com avaliação do nível de maturidade de segurança e
próximos passos recomendados.]

---

*Gerado pela Ethical Red Team Skill v1.0.0*
*Conformidade: OWASP Testing Guide v4.2 | NIST SP 800-115 | CVSS v3.1*
