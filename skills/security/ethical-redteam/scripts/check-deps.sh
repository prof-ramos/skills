#!/usr/bin/env bash
# check-deps.sh — Verificador de Dependências Ethical Red Team Skill
# Valida todas as dependências e OBRIGATORIAMENTE verifica TOR
# Uso: ./check-deps.sh [comando]
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# Cores
RED="\033[0;31m"; GREEN="\033[0;32m"; YELLOW="\033[1;33m"
CYAN="\033[0;36m"; BLUE="\033[0;34m"; BOLD="\033[1m"; RESET="\033[0m"

# Contadores
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNINGS=0
MISSING_CRITICAL=()

log_info()  { echo -e "${CYAN}[INFO]${RESET}  $*"; }
log_ok()    { echo -e "${GREEN}[✓]${RESET}    $*"; ((++PASSED_CHECKS)); ((++TOTAL_CHECKS)); }
log_warn()  { echo -e "${YELLOW}[!]${RESET}    $*"; ((++WARNINGS)); ((++TOTAL_CHECKS)); }
log_error() { echo -e "${RED}[✗]${RESET}    $*"; ((++FAILED_CHECKS)); ((++TOTAL_CHECKS)); MISSING_CRITICAL+=("$1"); }

header() {
    echo -e "\n${BOLD}${BLUE}▶ $1${RESET}"
}

# Banner
echo -e "${BOLD}${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║    🔍 ETHICAL RED TEAM SKILL — VERIFICAÇÃO DE DEPENDÊNCIAS  ║"
echo "║    ⚠️  TOR NETWORK: OBRIGATÓRIO PARA TODAS AS OPERAÇÕES       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# 1. Verificar TOR (CRÍTICO - OBRIGATÓRIO)
header "1. Verificando Rede TOR (OBRIGATÓRIO)"

# Verificar se TOR está instalado (macOS e Linux)
TOR_SERVICE_CMD=""
if command -v tor &>/dev/null; then
    TOR_SERVICE_CMD="tor"
    log_ok "tor instalado ($(tor --version 2>&1 | head -1))"
elif command -v tor-service &>/dev/null; then
    TOR_SERVICE_CMD="tor-service"
    log_ok "tor-service instalado"
elif command -v brew &>/dev/null && brew list tor &>/dev/null 2>&1; then
    TOR_SERVICE_CMD="tor-service"
    log_ok "tor instalado via Homebrew"
else
    log_error "TOR não instalado" "tor"
    echo "     Instale: brew install tor (macOS) ou apt install tor (Linux)"
fi

# Verificar se TOR está rodando
TOR_RUNNING=false
if pgrep -x "tor" &>/dev/null; then
    log_ok "TOR daemon está rodando"
    TOR_RUNNING=true
else
    log_error "TOR daemon NÃO está rodando" "tor-running"
    if [[ "$(uname -s)" == "Linux" ]]; then
        echo "     Inicie: systemctl start tor"
    else
        echo "     Inicie: brew services start tor"
    fi
fi

# Verificar conexão com TOR (testar SOCKS5)
TOR_CHECK=false
if command -v curl &>/dev/null; then
    if curl --socks5 127.0.0.1:9050 --connect-timeout 5 https://check.torproject.org &>/dev/null 2>&1; then
        log_ok "Conexão TOR SOCKS5 funcionando"
        TOR_CHECK=true
    else
        log_error "Conexão TOR SOCKS5 falhou" "tor-connection"
    fi
fi

# 2. Sistema Operacional
header "2. Verificando Sistema"
OS=$(uname -s)
ARCH=$(uname -m)
MACOS_VER=$(sw_vers -productVersion 2>/dev/null || echo "N/A")

if [[ "$OS" == "Darwin" ]]; then
    log_ok "macOS $MACOS_VER ($ARCH)"
elif [[ "$OS" == "Linux" ]]; then
    DISTRO=$(cat /etc/os-release 2>/dev/null | grep "^PRETTY_NAME" | cut -d'"' -f2 || echo "Linux")
    log_ok "Linux ($DISTRO) - $ARCH"
else
    log_warn "Sistema não testado: $OS ($ARCH)"
fi

# 3. Gerenciador de Pacotes
header "3. Verificando Gerenciador de Pacotes"
if command -v brew &>/dev/null; then
    log_ok "Homebrew: $(brew --version | head -1)"
elif command -v apt &>/dev/null; then
    log_ok "APT (Debian/Ubuntu)"
elif command -v dnf &>/dev/null; then
    log_ok "DNF (Fedora/RHEL)"
elif command -v pacman &>/dev/null; then
    log_ok "Pacman (Arch)"
else
    log_warn "Nenhum gerenciador de pacotes conhecido detectado"
fi

# 4. Python
header "4. Verificando Python"
PYTHON_CMD=""
for py in python3.12 python3.11 python3; do
    if command -v "$py" &>/dev/null; then
        PY_VER=$($py --version 2>&1 | awk '{print $2}')
        PYTHON_CMD="$py"
        log_ok "Python $PY_VER"
        break
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    log_error "Python 3.11+ não encontrado" "python"
fi

# 5. Ambiente Virtual
header "5. Verificando Ambiente Virtual"
VENV_DIR="$(pwd)/.venv-redteam"

if [[ -d "$VENV_DIR" ]]; then
    log_ok "Ambiente virtual encontrado"
else
    log_error "Ambiente virtual não encontrado" "venv"
fi

# 6. Scripts Python
header "6. Verificando Scripts"
for script in recon.py scanner.py analyzer.py reporter.py utils.py; do
    if [[ -f "scripts/$script" ]]; then
        [[ -x "scripts/$script" ]] && log_ok "scripts/$script" || log_warn "scripts/$script (sem exec)"
    else
        log_error "scripts/$script não encontrado" "$script"
    fi
done

# 6b. Ferramentas OSINT Adicionais
header "6b. Verificando Ferramentas OSINT (subfinder / sherlock / blackbird)"

# subfinder (Go)
if command -v subfinder &>/dev/null; then
    log_ok "subfinder: $(subfinder -version 2>&1 | head -1)"
else
    log_warn "subfinder não encontrado — instale: go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    echo "     Alternativa Python: pip install sublist3r"
fi

# sherlock
if command -v sherlock &>/dev/null; then
    log_ok "sherlock: $(sherlock --version 2>&1 | head -1)"
elif python3 -m pip show sherlock-project &>/dev/null; then
    log_ok "sherlock (pacote sherlock-project instalado)"
else
    log_warn "sherlock não encontrado — instale: pip install sherlock-project"
fi

# blackbird
BLACKBIRD_DIR=""
for loc in "./blackbird" "$HOME/blackbird" "/opt/blackbird"; do
    if [[ -f "$loc/blackbird.py" ]]; then
        BLACKBIRD_DIR="$loc"
        break
    fi
done

if [[ -n "$BLACKBIRD_DIR" ]]; then
    log_ok "blackbird encontrado em $BLACKBIRD_DIR"
else
    log_warn "blackbird não encontrado — instale: git clone https://github.com/p1ngul1n0/blackbird.git"
fi

# 7. Burp Suite MCP (opcional — necessário para web app scanning)
header "7. Verificando Burp Suite MCP (Web App Scanner)"

BURP_MCP_HOST="127.0.0.1"
BURP_MCP_PORT="9876"

if command -v java &>/dev/null; then
    JAVA_VER=$(java -version 2>&1 | head -1)
    log_ok "Java disponível: $JAVA_VER"
else
    log_warn "Java não encontrado — necessário para compilar extensão MCP do Burp"
    echo "     Instale: brew install openjdk (macOS) ou apt install default-jdk (Linux)"
fi

# Verificar se Burp MCP está rodando na porta 9876
if command -v curl &>/dev/null; then
    if curl -s --connect-timeout 2 "http://${BURP_MCP_HOST}:${BURP_MCP_PORT}" -o /dev/null 2>&1; then
        log_ok "Burp Suite MCP Server respondendo em ${BURP_MCP_HOST}:${BURP_MCP_PORT}"
    else
        log_warn "Burp MCP Server não detectado em ${BURP_MCP_HOST}:${BURP_MCP_PORT}"
        echo "     Para ativar:"
        echo "       1. git clone https://github.com/portswigger/mcp-server"
        echo "       2. cd mcp-server && ./gradlew embedProxyJar"
        echo "       3. Burp Suite → Extensions → Add → Java → build/libs/mcp-server-all.jar"
        echo "       4. Aba MCP → Enable Server"
        echo "     Verificar: python scripts/burp_mcp.py --check"
    fi
else
    log_warn "curl não disponível — não foi possível verificar Burp MCP"
fi

if [[ -f "scripts/burp_mcp.py" ]]; then
    log_ok "scripts/burp_mcp.py (módulo Burp MCP Community)"
else
    log_warn "scripts/burp_mcp.py não encontrado"
fi

# 8. SKILL.md
header "8. Verificando Metadados"
if [[ -f "SKILL.md" ]]; then
    grep -q "^name:" SKILL.md && log_ok "SKILL.md: name" || log_error "SKILL.md: name ausente" "SKILL.md"
    grep -q "^description:" SKILL.md && log_ok "SKILL.md: description" || log_error "SKILL.md: description ausente" "SKILL.md"
    grep -q "^license:" SKILL.md && log_ok "SKILL.md: license" || log_error "SKILL.md: license ausente" "SKILL.md"
else
    log_error "SKILL.md não encontrado" "SKILL.md"
fi

# Resumo
echo ""
echo -e "${BOLD}════════════════════════════════════════════════════════════${RESET}"

if [[ $FAILED_CHECKS -eq 0 && $TOR_RUNNING == true && $TOR_CHECK == true ]]; then
    echo -e "${GREEN}${BOLD}✅ TODAS AS VERIFICAÇÕES PASSARAM!${RESET}"
    echo -e "${GREEN}   Dependências OK, TOR ativo e conectado${RESET}"
    echo -e "   Verificações: $PASSED_CHECKS/$TOTAL_CHECKS passaram, $WARNINGS avisos"

    # Executar comando fornecido
    if [[ -n "${1:-}" ]]; then
        echo ""
        log_info "Executando via TOR: $@"
        exec "$@"
    fi
    exit 0
elif [[ $FAILED_CHECKS -gt 0 ]]; then
    echo -e "${RED}${BOLD}❌ FALTAM ${FAILED_CHECKS} DEPENDÊNCIA(S) CRÍTICA(S)${RESET}"
    echo ""
    echo -e "${BOLD}Dependências Críticas Faltando:${RESET}"
    for dep in "${MISSING_CRITICAL[@]}"; do
        echo -e "  ${RED}✗${RESET} $dep"
    done
    echo ""
    echo -e "${CYAN}Execute './install.sh' para instalar dependências${RESET}"
    if [[ "$(uname -s)" == "Linux" ]]; then
        echo -e "${CYAN}Execute 'systemctl start tor' para iniciar TOR${RESET}"
    else
        echo -e "${CYAN}Execute 'brew services start tor' para iniciar TOR${RESET}"
    fi
    exit 1
else
    echo -e "${YELLOW}${BOLD}⚠️  AVISOS: TOR não está configurado corretamente${RESET}"
    echo -e "${YELLOW}   Esta skill OBRIGATORIAMENTE requer TOR para funcionar${RESET}"
    exit 1
fi
