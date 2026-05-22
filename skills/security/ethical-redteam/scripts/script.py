
import os
import zipfile

BASE = "ethical-redteam-skill"
os.makedirs(f"{BASE}/scripts", exist_ok=True)
os.makedirs(f"{BASE}/references/examples", exist_ok=True)
os.makedirs(f"{BASE}/assets", exist_ok=True)

# ─────────────────────────────────────────────
# 1. SKILL.md
# ─────────────────────────────────────────────
skill_md = '''---
name: ethical-redteam-bugbounty
description: Conduz testes de segurança éticos (Red Team / Bug Bounty) com reconhecimento, scanning, análise e geração de relatórios OWASP/NIST. Use quando o usuário solicitar "teste de penetração", "pentest", "varredura de vulnerabilidades", "reconhecimento OSINT", "bug bounty", "relatório de segurança", "scan de portas" ou "análise de rede". Exige confirmação de autorização antes de qualquer ação.
license: MIT
compatibility: macOS 13+ (Apple Silicon M1/M2/M3 ARM64), Python 3.11+, Homebrew. Requer autorização explícita do alvo antes de execução.
metadata:
  author: Ethical RedTeam Skill
  version: 1.0.0
  category: security
  tags: [redteam, bugbounty, pentest, osint, security, owasp, nist]
---

# Ethical Red Team & Bug Bounty Skill

> ⚠️ **DISCLAIMER OBRIGATÓRIO**
> Esta SKILL é destinada **exclusivamente** para testes de segurança autorizados em ambientes controlados.
> O uso não autorizado contra sistemas de terceiros é **ilegal** e viola leis como LGPD, Marco Civil da Internet e legislações internacionais equivalentes (CFAA, Computer Misuse Act).
> **SEMPRE** solicite e documente a autorização escrita antes de qualquer teste.

## Fluxo de Ativação

### Passo 0: Validação de Autorização (OBRIGATÓRIO)

Antes de executar qualquer módulo, SEMPRE pergunte:

```
Antes de prosseguir, preciso confirmar:
1. Você possui autorização ESCRITA do proprietário do sistema alvo?
2. O escopo do teste está claramente definido?
3. Existe um Rules of Engagement (RoE) documentado?

Responda SIM para todas as perguntas para continuar.
```

Se qualquer resposta for NÃO, interrompa e oriente sobre como obter autorização legal.

---

## Módulos Disponíveis

### Módulo 1: Reconhecimento (OSINT/DNS/IP)

Execute o reconhecimento passivo e ativo:

```bash
python scripts/recon.py --target ALVO --mode [passive|active|full] --output recon_output/
```

**Opções:**
- `--mode passive`: Apenas OSINT (sem contato direto com o alvo)
- `--mode active`: DNS enumeration, IP range mapping
- `--mode full`: Passive + Active combinados

**Saídas esperadas:** `recon_output/ALVO_recon_TIMESTAMP.json`

### Módulo 2: Scanning (Portas/Serviços/Vulnerabilidades)

```bash
python scripts/scanner.py --target ALVO --profile [quick|standard|deep] --output scan_output/
```

**Perfis:**
- `quick`: Top 100 portas, detecção de SO
- `standard`: Top 1000 portas + banner grabbing (recomendado)
- `deep`: Todas as portas + detecção de CVEs conhecidos

**Limites de recursos:** Configurado para máx. 4GB RAM no M3.

### Módulo 3: Análise

```bash
python scripts/analyzer.py --recon recon_output/ARQUIVO.json --scan scan_output/ARQUIVO.json --output analysis/
```

Gera análise consolidada com classificação de severidade CVSS v3.1.

### Módulo 4: Geração de Relatório

```bash
python scripts/reporter.py --analysis analysis/ARQUIVO.json --target "Nome do Alvo" --tester "Seu Nome" --output reports/
```

Gera relatório em Markdown + PDF nos formatos:
- `ALVO_executive_report.md` — Sumário executivo
- `ALVO_technical_report.md` — Detalhamento técnico
- `ALVO_full_report.pdf` — Relatório completo exportado

---

## Instalação Rápida

```bash
chmod +x scripts/install.sh && ./scripts/install.sh
```

O instalador detecta automaticamente a arquitetura M3 e instala dependências nativas ARM64.

---

## Exemplos de Uso

### Cenário 1: Bug Bounty — Reconhecimento Inicial
```bash
# Alvo: domínio fictício para teste
python scripts/recon.py --target testphp.vulnweb.com --mode passive --output ./saida/
```

### Cenário 2: Red Team Interno — Scan Completo
```bash
python scripts/scanner.py --target 192.168.1.0/24 --profile standard --output ./saida/
python scripts/analyzer.py --scan ./saida/scan_*.json --output ./saida/
python scripts/reporter.py --analysis ./saida/analysis_*.json --target "Rede Interna Lab" --tester "Pentester A"
```

---

## Troubleshooting

**Erro: `nmap not found`**
Causa: nmap não instalado via Homebrew.
Solução: `brew install nmap`

**Erro: `Permission denied` no install.sh**
Causa: Arquivo sem permissão de execução.
Solução: `chmod +x scripts/install.sh`

**Erro: memória excedida**
Causa: Scan `deep` em redes grandes.
Solução: Reduza o range ou use `--profile standard`.

**Erro: `theHarvester` timeout**
Causa: APIs externas lentas.
Solução: Use `--mode passive --timeout 30`

---

## Conformidade

Consulte `references/ethics-guide.md` para orientações legais completas.
Consulte `references/owasp-checklist.md` para cobertura metodológica OWASP WSTG.
'''

with open(f"{BASE}/SKILL.md", "w", encoding="utf-8") as f:
    f.write(skill_md)

# ─────────────────────────────────────────────
# 2. scripts/install.sh
# ─────────────────────────────────────────────
install_sh = '''#!/usr/bin/env bash
# install.sh — Instalador Inteligente para Ethical Red Team Skill
# Compatível com: macOS 13+ / Apple Silicon M3 (ARM64)
# Uso: chmod +x install.sh && ./install.sh
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# ── Cores ──────────────────────────────────────────────────────────
RED="\\033[0;31m"; GREEN="\\033[0;32m"; YELLOW="\\033[1;33m"
CYAN="\\033[0;36m"; BOLD="\\033[1m"; RESET="\\033[0m"

log_info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
log_ok()      { echo -e "${GREEN}[OK]${RESET}    $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
log_error()   { echo -e "${RED}[ERROR]${RESET} $*"; exit 1; }

# ── Disclaimer ─────────────────────────────────────────────────────
echo -e "${BOLD}${RED}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          ⚠️  ETHICAL RED TEAM SKILL — DISCLAIMER ⚠️           ║"
echo "║                                                              ║"
echo "║  Esta ferramenta é destinada EXCLUSIVAMENTE para testes de   ║"
echo "║  segurança AUTORIZADOS em ambientes CONTROLADOS.             ║"
echo "║                                                              ║"
echo "║  O uso não autorizado é ILEGAL e sujeito a processos         ║"
echo "║  criminais conforme LGPD, Marco Civil da Internet e          ║"
echo "║  legislações internacionais equivalentes.                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

read -rp "$(echo -e "${BOLD}Você confirma que usará esta ferramenta apenas em ambientes autorizados? [sim/não]: ${RESET}")" CONFIRM
[[ "${CONFIRM,,}" == "sim" ]] || log_error "Instalação cancelada. Autorização necessária."

# ── Detecção de Arquitetura ─────────────────────────────────────────
ARCH=$(uname -m)
OS=$(uname -s)
log_info "Sistema detectado: ${OS} / ${ARCH}"

[[ "${OS}" == "Darwin" ]] || log_error "Este instalador suporta apenas macOS."

if [[ "${ARCH}" == "arm64" ]]; then
    log_ok "Apple Silicon (M-series) detectado — instalando binários ARM64 nativos."
    BREW_PREFIX="/opt/homebrew"
else
    log_warn "Intel x86_64 detectado — instalando com compatibilidade Rosetta 2."
    BREW_PREFIX="/usr/local"
fi

# ── macOS Version Check ────────────────────────────────────────────
MACOS_VER=$(sw_vers -productVersion | cut -d. -f1)
(( MACOS_VER >= 13 )) || log_error "macOS 13+ (Ventura) é necessário. Versão atual: $(sw_vers -productVersion)"
log_ok "macOS $(sw_vers -productVersion) — compatível."

# ── Homebrew ───────────────────────────────────────────────────────
if ! command -v brew &>/dev/null; then
    log_info "Homebrew não encontrado. Instalando..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$("${BREW_PREFIX}/bin/brew" shellenv)"
else
    log_ok "Homebrew $(brew --version | head -1) já instalado."
fi

# ── Python 3.11+ ───────────────────────────────────────────────────
PYTHON_OK=false
for py in python3.12 python3.11 python3; do
    if command -v "$py" &>/dev/null; then
        PY_VER=$($py --version 2>&1 | awk \'{print $2}\')
        PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
        PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
        if (( PY_MAJOR >= 3 && PY_MINOR >= 11 )); then
            PYTHON_CMD="$py"
            PYTHON_OK=true
            log_ok "Python ${PY_VER} encontrado em: $(command -v $py)"
            break
        fi
    fi
done

if ! $PYTHON_OK; then
    log_info "Instalando Python 3.12 via Homebrew (ARM64 nativo)..."
    brew install python@3.12
    PYTHON_CMD="${BREW_PREFIX}/bin/python3.12"
fi

# ── Ferramentas de Segurança ───────────────────────────────────────
declare -A BREW_TOOLS=(
    ["nmap"]="Scanner de portas e serviços"
    ["masscan"]="Scanner de alta velocidade"
    ["dnsx"]="Resolução e enumeração DNS"
    ["httpx"]="Probe HTTP/HTTPS"
    ["nuclei"]="Scanner de vulnerabilidades baseado em templates"
    ["subfinder"]="Enumeração de subdomínios"
    ["amass"]="Mapeamento de superfície de ataque"
    ["whatweb"]="Fingerprinting de tecnologias web"
    ["gobuster"]="Enumeração de diretórios/DNS"
)

log_info "Verificando e instalando ferramentas de segurança..."
for tool in "${!BREW_TOOLS[@]}"; do
    if command -v "$tool" &>/dev/null; then
        log_ok "${tool} já instalado — ${BREW_TOOLS[$tool]}"
    else
        log_info "Instalando ${tool} — ${BREW_TOOLS[$tool]}..."
        brew install "$tool" 2>/dev/null || log_warn "Falha ao instalar ${tool} via brew. Tente manualmente."
    fi
done

# ── theHarvester (pip) ────────────────────────────────────────────
if ! command -v theHarvester &>/dev/null; then
    log_info "Instalando theHarvester via pip..."
    $PYTHON_CMD -m pip install theHarvester --quiet || log_warn "Falha ao instalar theHarvester."
else
    log_ok "theHarvester já instalado."
fi

# ── Ambiente Virtual Python ────────────────────────────────────────
VENV_DIR="$(pwd)/.venv-redteam"
if [[ ! -d "$VENV_DIR" ]]; then
    log_info "Criando ambiente virtual isolado em ${VENV_DIR}..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

log_info "Instalando dependências Python no venv..."
pip install --quiet --upgrade pip
pip install --quiet \\
    dnspython==2.6.1 \\
    shodan==1.31.0 \\
    requests==2.31.0 \\
    rich==13.7.1 \\
    reportlab==4.1.0 \\
    markdown2==2.4.13 \\
    jinja2==3.1.4 \\
    python-nmap==0.7.1 \\
    ipwhois==1.3.0 \\
    beautifulsoup4==4.12.3 \\
    pyfiglet==1.0.2 \\
    cryptography==42.0.8

log_ok "Dependências Python instaladas."

# ── Estrutura de Diretórios ────────────────────────────────────────
for dir in logs reports scan_output recon_output analysis; do
    mkdir -p "$dir"
    log_ok "Diretório criado: ${dir}/"
done

# ── Resumo da Instalação ───────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════════╗"
echo -e "║          ✅  INSTALAÇÃO CONCLUÍDA COM SUCESSO               ║"
echo -e "╚══════════════════════════════════════════════════════════════╝${RESET}"
echo ""
log_info "Para ativar o ambiente virtual: source .venv-redteam/bin/activate"
log_info "Para executar o reconhecimento: python scripts/recon.py --help"
log_info "Para executar o scanner:        python scripts/scanner.py --help"
log_info "Para gerar relatório:           python scripts/reporter.py --help"
echo ""
log_warn "LEMBRE-SE: Use apenas em ambientes com autorização documentada."
'''

with open(f"{BASE}/scripts/install.sh", "w", encoding="utf-8") as f:
    f.write(install_sh)

# ─────────────────────────────────────────────
# 3. scripts/utils.py
# ─────────────────────────────────────────────
utils_py = '''#!/usr/bin/env python3
"""
utils.py — Utilitários compartilhados para a Ethical Red Team Skill.

Fornece funções de logging, validação de autorização, tratamento de erros
e helpers de saída para todos os módulos.

Autor: Ethical RedTeam Skill
Versão: 1.0.0
Compatibilidade: Python 3.11+ / macOS 13+ / Apple Silicon M3
"""

import json
import logging
import os
import platform
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.text import Text

console = Console()

# ── Configuração de Logging ────────────────────────────────────────────────────

def configurar_logger(nome_modulo: str, nivel: int = logging.DEBUG) -> logging.Logger:
    """
    Configura e retorna um logger com handlers para arquivo e console.

    Parâmetros:
        nome_modulo: Nome do módulo que está sendo logado.
        nivel: Nível de logging (padrão: DEBUG para auditoria completa).

    Retorna:
        logging.Logger: Logger configurado com handlers de arquivo e console.
    """
    Path("logs").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{nome_modulo}_{timestamp}.log"

    logger = logging.getLogger(nome_modulo)
    logger.setLevel(nivel)

    # Handler para arquivo (auditoria completa)
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger, log_file


# ── Disclaimer e Validação de Autorização ─────────────────────────────────────

DISCLAIMER = """
╔══════════════════════════════════════════════════════════════════════════╗
║         ⚠️  ETHICAL RED TEAM SKILL — AVISO LEGAL OBRIGATÓRIO ⚠️          ║
║                                                                          ║
║  Esta ferramenta é destinada EXCLUSIVAMENTE para testes de segurança     ║
║  AUTORIZADOS em ambientes CONTROLADOS.                                   ║
║                                                                          ║
║  O uso não autorizado é ILEGAL e sujeito a processos criminais           ║
║  conforme:                                                               ║
║    • LGPD (Lei 13.709/2018)                                              ║
║    • Marco Civil da Internet (Lei 12.965/2014)                           ║
║    • Código Penal Brasileiro (Art. 154-A - invasão de dispositivos)      ║
║    • CFAA (Computer Fraud and Abuse Act) — para alvos nos EUA            ║
║                                                                          ║
║  SEMPRE obtenha autorização ESCRITA antes de iniciar qualquer teste.     ║
╚══════════════════════════════════════════════════════════════════════════╝
"""


def exibir_disclaimer_e_validar(logger: logging.Logger) -> bool:
    """
    Exibe o disclaimer legal e solicita confirmação interativa do usuário.

    Solicita confirmação para três itens obrigatórios:
    1. Autorização escrita do proprietário do sistema.
    2. Escopo de teste claramente definido.
    3. Rules of Engagement (RoE) documentado.

    Parâmetros:
        logger: Logger para registrar a validação.

    Retorna:
        bool: True se todas as confirmações forem positivas, False caso contrário.
    """
    console.print(Panel(
        Text(DISCLAIMER, style="bold red"),
        title="⚠️ AVISO LEGAL", border_style="red"
    ))

    perguntas = [
        "Você possui autorização ESCRITA do proprietário do sistema alvo?",
        "O escopo do teste está claramente definido e documentado?",
        "Existe um Rules of Engagement (RoE) formal documentado?",
    ]

    for pergunta in perguntas:
        if not Confirm.ask(f"[bold yellow]{pergunta}[/bold yellow]"):
            console.print(
                "[bold red]❌ Operação cancelada. Obtenha autorização adequada antes de prosseguir.[/bold red]"
            )
            logger.warning("AUTORIZAÇÃO NEGADA: Usuário não confirmou requisitos legais.")
            return False

    logger.info("AUTORIZAÇÃO CONFIRMADA: Usuário confirmou todos os requisitos legais.")
    return True


# ── Validação de Alvos ─────────────────────────────────────────────────────────

def validar_alvo(alvo: str) -> dict:
    """
    Valida e classifica o tipo de alvo fornecido.

    Detecta se o alvo é um endereço IP, range CIDR, domínio ou URL
    e retorna metadados para uso nos módulos.

    Parâmetros:
        alvo: String com IP, CIDR, domínio ou URL do alvo.

    Retorna:
        dict: Dicionário com keys 'tipo', 'valor', 'valido'.

    Exemplo:
        >>> validar_alvo("192.168.1.1")
        {'tipo': 'ip', 'valor': '192.168.1.1', 'valido': True}
    """
    alvo = alvo.strip()

    # IP simples
    padrao_ip = r"^(\\d{1,3}\\.){3}\\d{1,3}$"
    # CIDR
    padrao_cidr = r"^(\\d{1,3}\\.){3}\\d{1,3}/\\d{1,2}$"
    # Domínio
    padrao_dominio = r"^([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,}$"
    # URL
    padrao_url = r"^https?://"

    if re.match(padrao_cidr, alvo):
        return {"tipo": "cidr", "valor": alvo, "valido": True}
    elif re.match(padrao_ip, alvo):
        partes = [int(p) for p in alvo.split(".")]
        valido = all(0 <= p <= 255 for p in partes)
        return {"tipo": "ip", "valor": alvo, "valido": valido}
    elif re.match(padrao_url, alvo):
        return {"tipo": "url", "valor": alvo, "valido": True}
    elif re.match(padrao_dominio, alvo):
        return {"tipo": "dominio", "valor": alvo, "valido": True}
    else:
        return {"tipo": "desconhecido", "valor": alvo, "valido": False}


# ── Detecção de Ambiente ───────────────────────────────────────────────────────

def detectar_ambiente() -> dict:
    """
    Detecta informações do ambiente de execução para compatibilidade.

    Verifica arquitetura do processador, versão do sistema operacional
    e disponibilidade de memória RAM para otimização de parâmetros.

    Retorna:
        dict: Informações do ambiente com keys 'arch', 'os', 'versao_os',
              'python', 'apple_silicon', 'ram_gb'.
    """
    arch = platform.machine()
    sistema = platform.system()
    versao = platform.version()
    python_ver = platform.python_version()

    ram_gb = 8  # padrão conservador
    if sistema == "Darwin":
        try:
            import subprocess
            resultado = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True, timeout=5
            )
            ram_bytes = int(resultado.stdout.strip())
            ram_gb = ram_bytes / (1024 ** 3)
        except Exception:
            pass

    return {
        "arch": arch,
        "os": sistema,
        "versao_os": versao,
        "python": python_ver,
        "apple_silicon": arch == "arm64" and sistema == "Darwin",
        "ram_gb": round(ram_gb, 1),
    }


# ── Persistência de Resultados ────────────────────────────────────────────────

def salvar_json(dados: dict, prefixo: str, diretorio: str = ".") -> str:
    """
    Salva dados em arquivo JSON com timestamp no nome.

    Parâmetros:
        dados: Dicionário com os dados a serem salvos.
        prefixo: Prefixo para o nome do arquivo.
        diretorio: Diretório de destino (padrão: diretório atual).

    Retorna:
        str: Caminho completo do arquivo salvo.
    """
    Path(diretorio).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = Path(diretorio) / f"{prefixo}_{timestamp}.json"
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    return str(caminho)


def calcular_severidade_cvss(score: float) -> str:
    """
    Converte score CVSS v3.1 numérico para classificação textual.

    Parâmetros:
        score: Score CVSS entre 0.0 e 10.0.

    Retorna:
        str: Classificação de severidade (Crítica/Alta/Média/Baixa/Informativa).
    """
    if score >= 9.0:
        return "Crítica"
    elif score >= 7.0:
        return "Alta"
    elif score >= 4.0:
        return "Média"
    elif score > 0.0:
        return "Baixa"
    else:
        return "Informativa"
'''

with open(f"{BASE}/scripts/utils.py", "w", encoding="utf-8") as f:
    f.write(utils_py)

print("utils.py criado.")

# ─────────────────────────────────────────────
# 4. scripts/recon.py
# ─────────────────────────────────────────────
recon_py = '''#!/usr/bin/env python3
"""
recon.py — Módulo de Reconhecimento (OSINT / DNS / IP Enumeration).

Realiza coleta de informações passiva e ativa sobre o alvo, incluindo
enumeração de subdomínios, consultas DNS, registros WHOIS, geolocalização
de IP e busca em fontes OSINT públicas.

Requisitos: Python 3.11+, dnspython, ipwhois, requests, rich
Uso: python scripts/recon.py --target alvo.com --mode passive --output ./saida/

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import json
import socket
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import dns.resolver
    import requests
    from ipwhois import IPWhois
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.panel import Panel
except ImportError as e:
    print(f"[ERRO] Dependência ausente: {e}. Execute: pip install -r requirements.txt")
    sys.exit(1)

# Importação condicional de utils (mesmo diretório)
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    configurar_logger, exibir_disclaimer_e_validar,
    validar_alvo, salvar_json, detectar_ambiente
)

console = Console()


class ModuloReconhecimento:
    """
    Módulo de reconhecimento passivo e ativo para testes de segurança.

    Encapsula todas as técnicas de coleta de informações, garantindo
    que o disclaimer e a validação de autorização sejam exibidos antes
    de qualquer operação.
    """

    TIMEOUT_DNS = 10
    TIMEOUT_HTTP = 15
    TIPOS_DNS = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]

    def __init__(self, alvo: str, modo: str, diretorio_saida: str):
        """
        Inicializa o módulo de reconhecimento.

        Parâmetros:
            alvo: IP, domínio ou URL do alvo autorizado.
            modo: Modo de operação ('passive', 'active' ou 'full').
            diretorio_saida: Diretório para salvar os resultados.
        """
        self.alvo = alvo
        self.modo = modo
        self.diretorio_saida = diretorio_saida
        self.timestamp_inicio = datetime.now().isoformat()
        self.logger, self.log_file = configurar_logger("recon")
        self.resultados: dict = {
            "alvo": alvo,
            "modo": modo,
            "timestamp_inicio": self.timestamp_inicio,
            "ambiente": detectar_ambiente(),
            "dns": {},
            "whois": {},
            "subdomains": [],
            "ips_encontrados": [],
            "osint": {},
            "metadata": {}
        }

        validacao = validar_alvo(alvo)
        if not validacao["valido"]:
            self.logger.error(f"Alvo inválido: {alvo}")
            console.print(f"[bold red]❌ Alvo inválido: {alvo}[/bold red]")
            sys.exit(1)

        self.tipo_alvo = validacao["tipo"]
        self.logger.info(f"Módulo de reconhecimento iniciado | alvo={alvo} | modo={modo}")

    def consultar_dns(self) -> dict:
        """
        Realiza consultas DNS para múltiplos tipos de registro.

        Consulta registros A, AAAA, MX, NS, TXT, SOA e CNAME
        para o domínio alvo e registra os resultados.

        Retorna:
            dict: Dicionário com registros DNS organizados por tipo.
        """
        registros = {}
        console.print("[bold cyan]→ Consultando registros DNS...[/bold cyan]")

        for tipo in self.TIPOS_DNS:
            try:
                respostas = dns.resolver.resolve(self.alvo, tipo, lifetime=self.TIMEOUT_DNS)
                registros[tipo] = [str(r) for r in respostas]
                self.logger.info(f"DNS {tipo}: {registros[tipo]}")
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
                    dns.resolver.NoNameservers, dns.exception.Timeout):
                registros[tipo] = []
            except Exception as e:
                registros[tipo] = []
                self.logger.warning(f"DNS {tipo} erro: {e}")

        return registros

    def resolver_ip(self) -> list:
        """
        Resolve o domínio alvo para seus endereços IP.

        Retorna:
            list: Lista de endereços IP associados ao domínio.
        """
        ips = []
        try:
            infos = socket.getaddrinfo(self.alvo, None)
            ips = list({info[4][0] for info in infos})
            self.logger.info(f"IPs resolvidos: {ips}")
        except socket.gaierror as e:
            self.logger.warning(f"Falha ao resolver IPs: {e}")
        return ips

    def consultar_whois_ip(self, ip: str) -> dict:
        """
        Consulta informações WHOIS de um endereço IP.

        Parâmetros:
            ip: Endereço IP a ser consultado.

        Retorna:
            dict: Informações de registro, ASN e geolocalização do IP.
        """
        try:
            obj = IPWhois(ip)
            resultado = obj.lookup_rdap(depth=1)
            return {
                "asn": resultado.get("asn"),
                "asn_description": resultado.get("asn_description"),
                "country": resultado.get("asn_country_code"),
                "network_name": resultado.get("network", {}).get("name"),
                "cidr": resultado.get("network", {}).get("cidr"),
            }
        except Exception as e:
            self.logger.warning(f"WHOIS falhou para {ip}: {e}")
            return {}

    def enumerar_subdomains_passivo(self) -> list:
        """
        Enumera subdomínios usando fontes OSINT passivas (sem contato direto).

        Consulta APIs públicas como crt.sh (Certificate Transparency Logs)
        para descobrir subdomínios registrados.

        Retorna:
            list: Lista de subdomínios encontrados.
        """
        subdomains = set()
        console.print("[bold cyan]→ Enumerando subdomínios (OSINT passivo)...[/bold cyan]")

        # Fonte 1: crt.sh (Certificate Transparency)
        try:
            url = f"https://crt.sh/?q=%.{self.alvo}&output=json"
            resp = requests.get(url, timeout=self.TIMEOUT_HTTP, headers={
                "User-Agent": "EthicalRedTeamSkill/1.0 (Authorized Security Testing)"
            })
            if resp.status_code == 200:
                dados = resp.json()
                for entrada in dados:
                    nome = entrada.get("name_value", "")
                    for sub in nome.split("\\n"):
                        sub = sub.strip().lower().replace("*.", "")
                        if sub.endswith(self.alvo) and sub != self.alvo:
                            subdomains.add(sub)
                self.logger.info(f"crt.sh: {len(subdomains)} subdomínios encontrados")
        except Exception as e:
            self.logger.warning(f"crt.sh falhou: {e}")

        return sorted(list(subdomains))

    def coletar_headers_http(self) -> dict:
        """
        Coleta cabeçalhos HTTP do alvo para fingerprinting passivo.

        Retorna:
            dict: Cabeçalhos HTTP da resposta e código de status.
        """
        try:
            url = self.alvo if self.alvo.startswith("http") else f"https://{self.alvo}"
            resp = requests.get(url, timeout=self.TIMEOUT_HTTP, allow_redirects=True, headers={
                "User-Agent": "EthicalRedTeamSkill/1.0 (Authorized Security Testing)"
            })
            return {
                "status_code": resp.status_code,
                "url_final": resp.url,
                "headers": dict(resp.headers),
                "server": resp.headers.get("Server", "N/A"),
                "x_powered_by": resp.headers.get("X-Powered-By", "N/A"),
            }
        except Exception as e:
            self.logger.warning(f"HTTP headers falhou: {e}")
            return {}

    def executar(self) -> str:
        """
        Orquestra a execução completa do módulo de reconhecimento.

        Executa passive, active ou full conforme o modo configurado
        e salva os resultados em arquivo JSON.

        Retorna:
            str: Caminho do arquivo JSON com os resultados.
        """
        console.print(Panel(
            f"[bold green]🔍 Reconhecimento iniciado[/bold green]\\n"
            f"Alvo: [cyan]{self.alvo}[/cyan] | Modo: [yellow]{self.modo}[/yellow]",
            border_style="green"
        ))

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            # Passive
            if self.modo in ("passive", "full"):
                t = p.add_task("OSINT: subdomínios (crt.sh)...")
                self.resultados["subdomains"] = self.enumerar_subdomains_passivo()
                p.remove_task(t)

            # Active
            if self.modo in ("active", "full") and self.tipo_alvo in ("dominio", "url"):
                t = p.add_task("DNS: consultando registros...")
                self.resultados["dns"] = self.consultar_dns()
                p.remove_task(t)

                t = p.add_task("Resolvendo IPs...")
                ips = self.resolver_ip()
                self.resultados["ips_encontrados"] = ips
                p.remove_task(t)

                for ip in ips[:3]:  # Limitar para M3 com 4GB RAM
                    t = p.add_task(f"WHOIS: {ip}...")
                    self.resultados["whois"][ip] = self.consultar_whois_ip(ip)
                    p.remove_task(t)

            # HTTP Fingerprinting (ambos os modos)
            if self.tipo_alvo in ("dominio", "url", "url"):
                t = p.add_task("HTTP: coletando cabeçalhos...")
                self.resultados["osint"]["http_headers"] = self.coletar_headers_http()
                p.remove_task(t)

        self.resultados["timestamp_fim"] = datetime.now().isoformat()

        # Exibir resumo
        tabela = Table(title="📊 Resumo do Reconhecimento", border_style="cyan")
        tabela.add_column("Métrica", style="bold")
        tabela.add_column("Valor", style="green")
        tabela.add_row("Subdomínios encontrados", str(len(self.resultados["subdomains"])))
        tabela.add_row("IPs resolvidos", str(len(self.resultados["ips_encontrados"])))
        tabela.add_row("Registros DNS coletados", str(len(self.resultados["dns"])))
        tabela.add_row("Log de auditoria", self.log_file)
        console.print(tabela)

        caminho = salvar_json(self.resultados, f"{self.alvo.replace('.', '_')}_recon", self.diretorio_saida)
        console.print(f"[bold green]✅ Resultados salvos em: {caminho}[/bold green]")
        return caminho


def main():
    """Ponto de entrada principal do módulo de reconhecimento."""
    parser = argparse.ArgumentParser(
        description="Módulo de Reconhecimento — Ethical Red Team Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exemplo: python recon.py --target example.com --mode passive --output ./saida/"
    )
    parser.add_argument("--target", required=True, help="Alvo: IP, CIDR, domínio ou URL")
    parser.add_argument(
        "--mode", choices=["passive", "active", "full"], default="passive",
        help="Modo: passive (só OSINT), active (DNS+IP), full (completo)"
    )
    parser.add_argument("--output", default="recon_output", help="Diretório de saída")
    parser.add_argument("--skip-disclaimer", action="store_true",
                        help="Pular disclaimer (apenas para ambientes CI/CD autorizados)")
    args = parser.parse_args()

    # Logger temporário para validação
    logger, _ = configurar_logger("recon_auth")

    if not args.skip_disclaimer:
        if not exibir_disclaimer_e_validar(logger):
            sys.exit(1)

    modulo = ModuloReconhecimento(args.target, args.mode, args.output)
    modulo.executar()


if __name__ == "__main__":
    main()
'''

with open(f"{BASE}/scripts/recon.py", "w", encoding="utf-8") as f:
    f.write(recon_py)
print("recon.py criado.")

# ─────────────────────────────────────────────
# 5. scripts/scanner.py
# ─────────────────────────────────────────────
scanner_py = '''#!/usr/bin/env python3
"""
scanner.py — Módulo de Scanning (Portas / Serviços / Vulnerabilidades).

Realiza varredura de portas, detecção de serviços e sistema operacional
usando nmap via python-nmap. Otimizado para Apple Silicon M3 com limite
de 4GB de RAM.

Perfis disponíveis:
    quick    — Top 100 portas, detecção rápida de SO
    standard — Top 1000 portas + banner grabbing (recomendado)
    deep     — Todas as portas + scripts NSE de vulnerabilidades

Uso: python scripts/scanner.py --target 192.168.1.1 --profile standard

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import nmap
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError as e:
    print(f"[ERRO] Dependência ausente: {e}. Execute o install.sh primeiro.")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    configurar_logger, exibir_disclaimer_e_validar,
    validar_alvo, salvar_json, detectar_ambiente,
    calcular_severidade_cvss
)

console = Console()


# Perfis de scan otimizados para M3 (máx. 4GB RAM)
PERFIS_SCAN = {
    "quick": {
        "descricao": "Top 100 portas, sem scripts (rápido, baixo consumo)",
        "args": "-sV -O --top-ports 100 -T3 --host-timeout 120s",
        "ram_estimada_mb": 200,
    },
    "standard": {
        "descricao": "Top 1000 portas + banner grabbing (recomendado)",
        "args": "-sV -sC --top-ports 1000 -T3 --host-timeout 300s",
        "ram_estimada_mb": 512,
    },
    "deep": {
        "descricao": "Todas as portas + scripts NSE de vulnerabilidades",
        "args": "-sV -sC -p- --script=vuln -T2 --host-timeout 600s",
        "ram_estimada_mb": 2048,
    },
}


class ModuloScanner:
    """
    Módulo de varredura de portas e serviços para testes de segurança.

    Utiliza python-nmap como interface para o nmap, com otimizações
    específicas para Apple Silicon M3 e limite de 4GB de RAM.
    """

    def __init__(self, alvo: str, perfil: str, diretorio_saida: str):
        """
        Inicializa o módulo de scanning.

        Parâmetros:
            alvo: IP, CIDR ou hostname do alvo autorizado.
            perfil: Perfil de scan ('quick', 'standard' ou 'deep').
            diretorio_saida: Diretório para salvar os resultados.
        """
        self.alvo = alvo
        self.perfil = perfil
        self.config_perfil = PERFIS_SCAN[perfil]
        self.diretorio_saida = diretorio_saida
        self.logger, self.log_file = configurar_logger("scanner")
        self.nm = nmap.PortScanner()
        self.resultados: dict = {
            "alvo": alvo,
            "perfil": perfil,
            "config_perfil": self.config_perfil,
            "timestamp_inicio": datetime.now().isoformat(),
            "ambiente": detectar_ambiente(),
            "hosts": [],
            "resumo": {},
        }

        validacao = validar_alvo(alvo)
        if not validacao["valido"]:
            console.print(f"[bold red]❌ Alvo inválido: {alvo}[/bold red]")
            sys.exit(1)

        self.logger.info(f"Scanner iniciado | alvo={alvo} | perfil={perfil}")
        self._verificar_ram()

    def _verificar_ram(self):
        """
        Verifica se há RAM suficiente para o perfil selecionado.

        Emite aviso se a RAM estimada do scan ultrapassar 3.5GB,
        prevenindo degradação de performance no M3 com 8GB.
        """
        ram_necessaria = self.config_perfil["ram_estimada_mb"]
        if ram_necessaria > 3500:
            console.print(
                f"[bold yellow]⚠️  O perfil '{self.perfil}' pode consumir ~{ram_necessaria}MB RAM. "
                f"Considere usar 'standard' para preservar 4GB no M3.[/bold yellow]"
            )
            self.logger.warning(f"Uso de RAM estimado alto: {ram_necessaria}MB")

    def executar_scan(self) -> dict:
        """
        Executa o scan nmap com os parâmetros do perfil selecionado.

        Retorna:
            dict: Resultado bruto do scan organizado por host.
        """
        console.print(Panel(
            f"[bold green]🔬 Scanner iniciado[/bold green]\\n"
            f"Alvo: [cyan]{self.alvo}[/cyan] | Perfil: [yellow]{self.perfil}[/yellow]\\n"
            f"{self.config_perfil['descricao']}",
            border_style="green"
        ))

        hosts_resultado = []

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            t = p.add_task(f"Executando nmap ({self.perfil})...")
            try:
                self.nm.scan(hosts=self.alvo, arguments=self.config_perfil["args"])
                p.remove_task(t)
            except nmap.PortScannerError as e:
                p.remove_task(t)
                self.logger.error(f"Erro no nmap: {e}")
                console.print(f"[bold red]❌ Erro no nmap: {e}[/bold red]")
                console.print("[yellow]Verifique se o nmap está instalado: brew install nmap[/yellow]")
                return {}

        for host in self.nm.all_hosts():
            info_host = {
                "ip": host,
                "hostname": self.nm[host].hostname(),
                "estado": self.nm[host].state(),
                "os_match": [],
                "portas": [],
            }

            # Detecção de SO
            if "osmatch" in self.nm[host]:
                info_host["os_match"] = [
                    {"nome": m["name"], "acuracia": m["accuracy"]}
                    for m in self.nm[host]["osmatch"][:3]
                ]

            # Portas e serviços
            for proto in self.nm[host].all_protocols():
                portas = sorted(self.nm[host][proto].keys())
                for porta in portas:
                    dados_porta = self.nm[host][proto][porta]
                    info_porta = {
                        "porta": porta,
                        "protocolo": proto,
                        "estado": dados_porta.get("state", "unknown"),
                        "servico": dados_porta.get("name", ""),
                        "produto": dados_porta.get("product", ""),
                        "versao": dados_porta.get("version", ""),
                        "extra": dados_porta.get("extrainfo", ""),
                        "scripts": dados_porta.get("script", {}),
                    }
                    info_host["portas"].append(info_porta)

            hosts_resultado.append(info_host)
            self.logger.info(f"Host {host}: {len(info_host['portas'])} portas encontradas")

        return hosts_resultado

    def _gerar_resumo(self, hosts: list) -> dict:
        """
        Gera um resumo estatístico dos resultados do scan.

        Parâmetros:
            hosts: Lista de hosts com informações de portas e serviços.

        Retorna:
            dict: Resumo com contadores de hosts, portas e serviços.
        """
        total_portas_abertas = sum(
            len([p for p in h["portas"] if p["estado"] == "open"])
            for h in hosts
        )
        servicos_unicos = set(
            p["servico"] for h in hosts for p in h["portas"] if p["estado"] == "open"
        )
        return {
            "total_hosts": len(hosts),
            "hosts_ativos": len([h for h in hosts if h["estado"] == "up"]),
            "total_portas_abertas": total_portas_abertas,
            "servicos_detectados": sorted(list(servicos_unicos)),
        }

    def executar(self) -> str:
        """
        Orquestra a execução completa do scan e salva os resultados.

        Retorna:
            str: Caminho do arquivo JSON com os resultados do scan.
        """
        hosts = self.executar_scan()
        self.resultados["hosts"] = hosts if hosts else []
        self.resultados["resumo"] = self._gerar_resumo(self.resultados["hosts"])
        self.resultados["timestamp_fim"] = datetime.now().isoformat()

        # Exibir tabela de resultados
        tabela = Table(title="📊 Resumo do Scan", border_style="cyan")
        tabela.add_column("Métrica", style="bold")
        tabela.add_column("Valor", style="green")
        tabela.add_row("Hosts escaneados", str(self.resultados["resumo"]["total_hosts"]))
        tabela.add_row("Hosts ativos", str(self.resultados["resumo"]["hosts_ativos"]))
        tabela.add_row("Portas abertas encontradas", str(self.resultados["resumo"]["total_portas_abertas"]))
        tabela.add_row("Serviços detectados", str(len(self.resultados["resumo"]["servicos_detectados"])))
        tabela.add_row("Log de auditoria", self.log_file)
        console.print(tabela)

        caminho = salvar_json(
            self.resultados,
            f"{self.alvo.replace('/', '_').replace('.', '_')}_scan",
            self.diretorio_saida
        )
        console.print(f"[bold green]✅ Resultados salvos em: {caminho}[/bold green]")
        return caminho


def main():
    """Ponto de entrada principal do módulo de scanning."""
    parser = argparse.ArgumentParser(
        description="Módulo de Scanning — Ethical Red Team Skill",
    )
    parser.add_argument("--target", required=True, help="Alvo: IP, CIDR ou hostname")
    parser.add_argument(
        "--profile", choices=["quick", "standard", "deep"], default="standard",
        help="Perfil de scan (padrão: standard)"
    )
    parser.add_argument("--output", default="scan_output", help="Diretório de saída")
    parser.add_argument("--skip-disclaimer", action="store_true")
    args = parser.parse_args()

    logger, _ = configurar_logger("scanner_auth")
    if not args.skip_disclaimer:
        if not exibir_disclaimer_e_validar(logger):
            sys.exit(1)

    modulo = ModuloScanner(args.target, args.profile, args.output)
    modulo.executar()


if __name__ == "__main__":
    main()
'''

with open(f"{BASE}/scripts/scanner.py", "w", encoding="utf-8") as f:
    f.write(scanner_py)
print("scanner.py criado.")

# ─────────────────────────────────────────────
# 6. scripts/analyzer.py
# ─────────────────────────────────────────────
analyzer_py = '''#!/usr/bin/env python3
"""
analyzer.py — Módulo de Análise e Correlação de Resultados.

Consolida os resultados de reconhecimento e scanning, classifica
vulnerabilidades por severidade CVSS v3.1, e gera recomendações
baseadas nas diretrizes OWASP e NIST SP 800-115.

Uso:
    python scripts/analyzer.py --scan scan_output/arquivo.json
    python scripts/analyzer.py --recon recon_output/arquivo.json --scan scan_output/arquivo.json

Autor: Ethical RedTeam Skill
Versão: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError as e:
    print(f"[ERRO] {e}. Execute o install.sh primeiro.")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from utils import configurar_logger, salvar_json, calcular_severidade_cvss

console = Console()

# Mapeamento de portas/serviços para achados comuns (base de conhecimento interna)
BASE_CONHECIMENTO = {
    21: {"servico": "FTP", "descricao": "FTP sem criptografia", "cvss": 7.5,
         "cve_ref": "CWE-319", "recomendacao": "Migrar para SFTP ou FTPS"},
    22: {"servico": "SSH", "descricao": "SSH exposto publicamente", "cvss": 3.7,
         "cve_ref": "CWE-284", "recomendacao": "Restringir acesso por IP, usar chaves SSH, desabilitar senha"},
    23: {"servico": "Telnet", "descricao": "Telnet sem criptografia", "cvss": 9.8,
         "cve_ref": "CWE-319", "recomendacao": "Desabilitar Telnet imediatamente, usar SSH"},
    25: {"servico": "SMTP", "descricao": "SMTP sem autenticação/TLS", "cvss": 6.5,
         "cve_ref": "CWE-306", "recomendacao": "Configurar STARTTLS e autenticação obrigatória"},
    80: {"servico": "HTTP", "descricao": "HTTP não criptografado", "cvss": 5.3,
         "cve_ref": "CWE-319", "recomendacao": "Redirecionar para HTTPS, implementar HSTS"},
    443: {"servico": "HTTPS", "descricao": "HTTPS — verificar certificado e versão TLS", "cvss": 0.0,
          "cve_ref": None, "recomendacao": "Verificar TLS 1.2+, certificado válido, HSTS habilitado"},
    3306: {"servico": "MySQL", "descricao": "Banco de dados MySQL exposto na rede", "cvss": 8.8,
           "cve_ref": "CWE-284", "recomendacao": "Restringir acesso ao banco por firewall, nunca expor publicamente"},
    3389: {"servico": "RDP", "descricao": "Remote Desktop Protocol exposto", "cvss": 9.8,
           "cve_ref": "CVE-2019-0708", "recomendacao": "Usar VPN, habilitar NLA, aplicar patches BlueKeep"},
    5432: {"servico": "PostgreSQL", "descricao": "PostgreSQL exposto na rede", "cvss": 8.8,
           "cve_ref": "CWE-284", "recomendacao": "Restringir acesso, usar pg_hba.conf corretamente"},
    6379: {"servico": "Redis", "descricao": "Redis sem autenticação exposto", "cvss": 9.8,
           "cve_ref": "CWE-306", "recomendacao": "Habilitar AUTH, bind apenas localhost, usar TLS"},
    27017: {"servico": "MongoDB", "descricao": "MongoDB sem autenticação", "cvss": 9.8,
            "cve_ref": "CWE-306", "recomendacao": "Habilitar autenticação, bind localhost, usar TLS"},
    8080: {"servico": "HTTP-Alt", "descricao": "Servidor HTTP alternativo", "cvss": 5.3,
           "cve_ref": "CWE-319", "recomendacao": "Verificar se é necessário, adicionar autenticação"},
}

RECOMENDACOES_CABECALHOS = {
    "Server": "Remover/ofuscar cabeçalho Server para não revelar tecnologia",
    "X-Powered-By": "Remover cabeçalho X-Powered-By (revela tecnologia)",
    "X-Frame-Options": "Adicionar X-Frame-Options: DENY para prevenir Clickjacking",
    "X-Content-Type-Options": "Adicionar X-Content-Type-Options: nosniff",
    "Strict-Transport-Security": "Implementar HSTS: max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "Implementar Content-Security-Policy restritiva",
}


class ModuloAnalyzer:
    """
    Módulo de análise e correlação de vulnerabilidades.

    Processa resultados de reconhecimento e scanning para gerar
    achados classificados por severidade com recomendações OWASP/NIST.
    """

    def __init__(self, arquivo_recon: Optional[str], arquivo_scan: Optional[str], diretorio_saida: str):
        """
        Inicializa o módulo de análise.

        Parâmetros:
            arquivo_recon: Caminho para o JSON de reconhecimento (opcional).
            arquivo_scan: Caminho para o JSON de scanning (opcional).
            diretorio_saida: Diretório para salvar a análise consolidada.
        """
        self.arquivo_recon = arquivo_recon
        self.arquivo_scan = arquivo_scan
        self.diretorio_saida = diretorio_saida
        self.logger, self.log_file = configurar_logger("analyzer")
        self.dados_recon = self._carregar_json(arquivo_recon) if arquivo_recon else {}
        self.dados_scan = self._carregar_json(arquivo_scan) if arquivo_scan else {}
        self.achados: list = []

    def _carregar_json(self, caminho: str) -> dict:
        """
        Carrega e valida um arquivo JSON de entrada.

        Parâmetros:
            caminho: Caminho para o arquivo JSON.

        Retorna:
            dict: Dados carregados do arquivo.
        """
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Arquivo não encontrado: {caminho}")
            console.print(f"[bold red]❌ Arquivo não encontrado: {caminho}[/bold red]")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON inválido em {caminho}: {e}")
            console.print(f"[bold red]❌ JSON inválido: {e}[/bold red]")
            sys.exit(1)

    def analisar_portas(self):
        """
        Analisa portas abertas do scan e gera achados baseados na base de conhecimento.

        Correlaciona cada porta aberta com a base de conhecimento interna
        para identificar configurações potencialmente inseguras.
        """
        if not self.dados_scan:
            return

        for host in self.dados_scan.get("hosts", []):
            for porta in host.get("portas", []):
                if porta["estado"] != "open":
                    continue

                num_porta = porta["porta"]
                info_bk = BASE_CONHECIMENTO.get(num_porta)

                if info_bk:
                    achado = {
                        "id": f"SCAN-{num_porta:05d}",
                        "tipo": "Porta/Serviço",
                        "host": host["ip"],
                        "porta": num_porta,
                        "servico": porta.get("servico", info_bk["servico"]),
                        "produto": porta.get("produto", ""),
                        "versao": porta.get("versao", ""),
                        "descricao": info_bk["descricao"],
                        "cvss_score": info_bk["cvss"],
                        "severidade": calcular_severidade_cvss(info_bk["cvss"]),
                        "cve_ref": info_bk.get("cve_ref"),
                        "recomendacao": info_bk["recomendacao"],
                        "evidencia": f"Porta {num_porta}/tcp aberta em {host['ip']}",
                        "frameworks": ["OWASP A05:2021", "NIST SP 800-115 §6.1"],
                    }
                    self.achados.append(achado)
                    self.logger.info(f"Achado: {achado['id']} | {achado['severidade']} | {achado['descricao']}")

    def analisar_cabecalhos_http(self):
        """
        Analisa cabeçalhos HTTP do reconhecimento para identificar ausências de segurança.

        Verifica a presença de cabeçalhos de segurança recomendados pela
        OWASP Secure Headers Project.
        """
        if not self.dados_recon:
            return

        headers = self.dados_recon.get("osint", {}).get("http_headers", {}).get("headers", {})
        headers_lower = {k.lower(): v for k, v in headers.items()}

        cabecalhos_seguranca = {
            "strict-transport-security": ("HSTS ausente", 6.1, "OWASP A05:2021"),
            "x-frame-options": ("X-Frame-Options ausente (Clickjacking)", 4.3, "OWASP A05:2021"),
            "x-content-type-options": ("X-Content-Type-Options ausente", 3.7, "OWASP A05:2021"),
            "content-security-policy": ("Content-Security-Policy ausente", 5.4, "OWASP A03:2021"),
        }

        for cabecalho, (descricao, cvss, framework) in cabecalhos_seguranca.items():
            if cabecalho not in headers_lower:
                achado = {
                    "id": f"HTTP-{cabecalho.upper()[:10]}",
                    "tipo": "Cabeçalho HTTP",
                    "host": self.dados_recon.get("alvo", "N/A"),
                    "descricao": descricao,
                    "cvss_score": cvss,
                    "severidade": calcular_severidade_cvss(cvss),
                    "recomendacao": RECOMENDACOES_CABECALHOS.get(
                        cabecalho, f"Implementar cabeçalho {cabecalho}"
                    ),
                    "evidencia": f"Cabeçalho '{cabecalho}' não encontrado na resposta HTTP",
                    "frameworks": [framework, "NIST CSF PR.PT-4"],
                }
                self.achados.append(achado)

    def _calcular_risco_geral(self) -> str:
        """
        Calcula o nível de risco geral baseado nos achados identificados.

        Retorna:
            str: Classificação de risco geral (Crítico/Alto/Médio/Baixo/Mínimo).
        """
        if any(a["severidade"] == "Crítica" for a in self.achados):
            return "Crítico"
        elif any(a["severidade"] == "Alta" for a in self.achados):
            return "Alto"
        elif any(a["severidade"] == "Média" for a in self.achados):
            return "Médio"
        elif any(a["severidade"] == "Baixa" for a in self.achados):
            return "Baixo"
        return "Mínimo"

    def executar(self) -> str:
        """
        Executa a análise completa e salva o relatório consolidado.

        Retorna:
            str: Caminho do arquivo JSON com a análise consolidada.
        """
        console.print(Panel("[bold green]🔎 Análise iniciada[/bold green]", border_style="green"))

        self.analisar_portas()
        self.analisar_cabecalhos_http()

        # Ordenar por severidade
        ordem_severidade = {"Crítica": 0, "Alta": 1, "Média": 2, "Baixa": 3, "Informativa": 4}
        self.achados.sort(key=lambda x: ordem_severidade.get(x["severidade"], 5))

        alvo = (self.dados_scan or self.dados_recon).get("alvo", "desconhecido")
        analise = {
            "alvo": alvo,
            "timestamp": datetime.now().isoformat(),
            "risco_geral": self._calcular_risco_geral(),
            "total_achados": len(self.achados),
            "distribuicao_severidade": {
                sev: len([a for a in self.achados if a["severidade"] == sev])
                for sev in ["Crítica", "Alta", "Média", "Baixa", "Informativa"]
            },
            "achados": self.achados,
            "log_auditoria": self.log_file,
        }

        # Exibir resumo
        tabela = Table(title="📊 Resumo da Análise", border_style="cyan")
        tabela.add_column("Severidade", style="bold")
        tabela.add_column("Quantidade", style="green")
        cores = {"Crítica": "red", "Alta": "orange1", "Média": "yellow", "Baixa": "cyan", "Informativa": "white"}
        for sev, qtd in analise["distribuicao_severidade"].items():
            cor = cores.get(sev, "white")
            tabela.add_row(f"[{cor}]{sev}[/{cor}]", str(qtd))
        tabela.add_row("[bold]Risco Geral[/bold]", f"[bold]{analise['risco_geral']}[/bold]")
        console.print(tabela)

        caminho = salvar_json(analise, f"{alvo.replace('.', '_')}_analysis", self.diretorio_saida)
        console.print(f"[bold green]✅ Análise salva em: {caminho}[/bold green]")
        return caminho


def main():
    """Ponto de entrada principal do módulo de análise."""
    parser = argparse.ArgumentParser(description="Módulo de Análise — Ethical Red Team Skill")
    parser.add_argument("--recon", help="Arquivo JSON do reconhecimento")
    parser.add_argument("--scan", help="Arquivo JSON do scanning")
    parser.add_argument("--output", default="analysis", help="Diretório de saída")
    args = parser.parse_args()

    if not args.recon and not args.scan:
        parser.error("Forneça pelo menos --recon ou --scan")

    modulo = ModuloAnalyzer(args.recon, args.scan, args.output)
    modulo.executar()


if __name__ == "__main__":
    main()
'''

with open(f"{BASE}/scripts/analyzer.py", "w", encoding="utf-8") as f:
    f.write(analyzer_py)
print("analyzer.py criado.")
