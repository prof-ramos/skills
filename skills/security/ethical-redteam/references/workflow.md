# Workflow da Ethical Red Team Skill

## Diagrama de Fluxo

```mermaid
flowchart TB
    subgraph AUTH["🔐 Fase 0: Autorização"]
        A1[Alvo Solicitado] --> A2{Autorização<br/>Verificada?}
        A2 -->|NÃO| A3[❌ Interromper<br/>Orientar sobre<br/>legalização]
        A2 -->|SIM| START
    end

    subgraph RECON["🔍 Módulo 1: Reconhecimento"]
        START[Iniciar Teste] --> R1[OSINT Passivo<br/>crt.sh]
        R1 --> R2[Subfinder<br/>ProjectDiscovery]
        R2 --> R3[DNS Enumeration]
        R3 --> R4[IP Range Mapping]
        R4 --> R5[WHOIS Lookup]
        R5 --> R6[HTTPX/Nuclei<br/>Hosts Vivos]

        R1 -.->|via TOR| TOR1[🌐 Rede TOR]
        R2 -.->|via TOR| TOR1
        R3 -.->|via TOR| TOR1
        R4 -.->|via TOR| TOR1
        R5 -.->|via TOR| TOR1
        R6 -.->|via TOR| TOR1

        R6 --> R_OUT[recon_output/<br/>ALVO_recon.json]
    end

    subgraph SCAN["🛡️ Módulo 2: Scanning"]
        R_OUT --> S1{Perfil?}
        S1 -->|quick| S2[Top 100 portas<br/>+ OS detection]
        S1 -->|standard| S3[Top 1000 portas<br/>+ banner grabbing]
        S1 -->|deep| S4[Todas portas<br/>+ CVE detection]
        
        S2 --> S5[nmap scan]
        S3 --> S5
        S4 --> S5
        
        S5 -.->|via TOR| TOR2[🌐 Rede TOR]
        
        S5 --> S_OUT[scan_output/<br/>ALVO_scan.json]
    end

    subgraph ANALYZE["📊 Módulo 3: Análise"]
        R_OUT --> AN1[Correlação de Dados]
        S_OUT --> AN1
        AN1 --> AN2[Classificação CVSS v3.1]
        AN2 --> AN3[Identificação OWASP]
        AN3 --> AN4[Priorização de Riscos]
        AN4 --> AN_OUT[analysis/<br/>ALVO_analysis.json]
    end

    subgraph REPORT["📄 Módulo 4: Relatório"]
        AN_OUT --> RP1[Template Engine<br/>Jinja2]
        RP1 --> RP2[Executive Summary]
        RP1 --> RP3[Technical Report]
        RP1 --> RP4[Full PDF Report]
        
        RP2 --> OUT1[ALVO_executive_report.md]
        RP3 --> OUT2[ALVO_technical_report.md]
        RP4 --> OUT3[ALVO_full_report.pdf]
    end

    subgraph OUTPUTS["📁 Entregáveis"]
        OUT1 --> FINAL[✅ Teste Concluído]
        OUT2 --> FINAL
        OUT3 --> FINAL
    end

    style AUTH fill:#ffcccc,stroke:#cc0000
    style RECON fill:#cce5ff,stroke:#0066cc
    style SCAN fill:#ffebb3,stroke:#cc9900
    style ANALYZE fill:#d4edda,stroke:#28a745
    style REPORT fill:#e2d5f1,stroke:#6f42c1
    style OUTPUTS fill:#d1ecf1,stroke:#0c5460
```

---

## Fluxo Resumido

| Fase | Módulo | Input | Output |
|------|--------|-------|--------|
| 0 | Autorização | Alvo | Confirmação ✅ |
| 1a | Subdomain Enum | Domínio | `subfinder_output/*.json` (standalone) ou integrado ao recon |
| 1 | Reconhecimento | Domínio/IP | `recon_output/ALVO_recon.json` |
| 2 | Scanning | IP/CIDR | `scan_output/ALVO_scan.json` |
| 3 | Análise | recon + scan | `analysis/ALVO_analysis.json` |
| 4 | Relatório | analysis | `reports/ALVO_*.md/.pdf` |

> **Nota:** Arquivos JSON intermediários usam timestamp: `{prefixo}_YYYYMMDD_HHMMSS.json`
> Gerados pela função `salvar_json()` em `scripts/utils.py`. Aplicam-se a artefatos JSON das fases 1-3 (recon, scan, analysis).

---

## Comandos Correspondentes

### Fase 1a: Enumeração de Subdomínios

```bash
# Como módulo standalone
python scripts/subfinder.py --target alvo.com --output subfinder_output/

# Ou integrado ao recon.py (modo full)
python scripts/recon.py --target alvo.com --mode full --output recon_output/
```

**Requisitos:**
- `subfinder` instalado: `go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest`
- Autorização escrita do proprietário

**Validações éticas:**
- Bloqueio automático de TLDs governamentais (`.gov`, `.mil`, `.gov.br`, etc.)
- Log completo para auditoria

### Fase 1: Reconhecimento

```bash
python scripts/recon.py --target alvo.com --mode full --output recon_output/
```

**Modos disponíveis:**
- `passive` — Apenas OSINT (sem contato direto)
- `active` — DNS + IP mapping
- `full` — Passive + Active

### Fase 2: Scanning

```bash
python scripts/scanner.py --target 192.168.1.1 --profile standard --output scan_output/
```

**Perfis disponíveis:**
- `quick` — Top 100 portas + detecção de SO
- `standard` — Top 1000 portas + banner grabbing
- `deep` — Todas portas + CVE detection

### Fase 3: Análise

```bash
python scripts/analyzer.py \
  --recon recon_output/ALVO_recon_*.json \
  --scan scan_output/ALVO_scan_*.json \
  --output analysis/
```

### Fase 4: Relatório

```bash
python scripts/reporter.py \
  --analysis analysis/ALVO_analysis_*.json \
  --target "Nome do Alvo" \
  --tester "Nome do Pentester" \
  --output reports/
```

---

## Requisitos OBRIGATÓRIOS

- ✅ **TOR** deve estar rodando (todas as operações usam TOR)
- ✅ **Autorização escrita** do proprietário do sistema
- ✅ **Escopo definido** (Rules of Engagement)
- ✅ Ambiente virtual Python ativado (`.venv-redteam`)

---

## Estrutura de Diretórios

```
ethical-redteam-skill/
├── scripts/
│   ├── recon.py          # Módulo 1
│   ├── scanner.py        # Módulo 2
│   ├── analyzer.py       # Módulo 3
│   └── reporter.py       # Módulo 4
├── recon_output/         # Saídas do reconhecimento
├── scan_output/          # Saídas do scanning
├── analysis/             # Saídas da análise
├── reports/              # Relatórios finais
└── logs/                 # Logs de execução
```
