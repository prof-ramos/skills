#!/usr/bin/env bash
# install.sh — Instalador Inteligente para Ethical Red Team Skill
# Compatível com: macOS 13+ (Apple Silicon / Intel) | Ubuntu/Debian | Fedora/RHEL | Arch
# Uso: chmod +x scripts/install.sh && ./scripts/install.sh
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

# ── Cores ──────────────────────────────────────────────────────────
RED="\033[0;31m"; GREEN="\033[0;32m"; YELLOW="\033[1;33m"
CYAN="\033[0;36m"; BOLD="\033[1m"; RESET="\033[0m"

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

# ── Detecção de SO e Arquitetura ───────────────────────────────────
ARCH=$(uname -m)
OS=$(uname -s)
log_info "Sistema detectado: ${OS} / ${ARCH}"

if [[ "${OS}" == "Darwin" ]]; then
    PLATFORM="macos"
    if [[ "${ARCH}" == "arm64" ]]; then
        log_ok "macOS — Apple Silicon (M-series) ARM64 nativo."
        BREW_PREFIX="/opt/homebrew"
    else
        log_warn "macOS — Intel x86_64 (native, no Rosetta)."
        BREW_PREFIX="/usr/local"
    fi
    MACOS_VER=$(sw_vers -productVersion | cut -d. -f1)
    (( MACOS_VER >= 13 )) || log_error "macOS 13+ (Ventura) é necessário. Versão atual: $(sw_vers -productVersion)"
    log_ok "macOS $(sw_vers -productVersion) — compatível."

elif [[ "${OS}" == "Linux" ]]; then
    PLATFORM="linux"
    # Detectar distro
    if [[ -f /etc/os-release ]]; then
        # shellcheck disable=SC1091
        source /etc/os-release
        DISTRO_ID="${ID:-unknown}"
        DISTRO_LIKE="${ID_LIKE:-}"
        log_ok "Linux: ${PRETTY_NAME:-$DISTRO_ID} (${ARCH})"
    else
        DISTRO_ID="unknown"
        DISTRO_LIKE=""
        log_warn "Distribuição Linux não identificada — assumindo Debian/Ubuntu."
    fi

    # Classificar família de pacotes
    if [[ "$DISTRO_ID" =~ ^(ubuntu|debian|kali|parrot|mint)$ ]] || [[ "$DISTRO_LIKE" =~ debian ]]; then
        PKG_FAMILY="debian"
        PKG_INSTALL=(apt-get install -y -q)
        PKG_UPDATE=(apt-get update -q)
    elif [[ "$DISTRO_ID" =~ ^(fedora|rhel|centos|rocky|alma)$ ]] || [[ "$DISTRO_LIKE" =~ rhel|fedora ]]; then
        PKG_FAMILY="rhel"
        PKG_INSTALL=(dnf install -y -q)
        PKG_UPDATE=(dnf check-update -q)
    elif [[ "$DISTRO_ID" == "arch" ]] || [[ "$DISTRO_LIKE" =~ arch ]]; then
        PKG_FAMILY="arch"
        PKG_INSTALL=(pacman -S --noconfirm --needed)
        PKG_UPDATE=(pacman -Sy --noconfirm)
    else
        PKG_FAMILY="debian"
        log_warn "Distro não mapeada — usando apt-get como fallback."
        PKG_INSTALL=(apt-get install -y -q)
        PKG_UPDATE=(apt-get update -q)
    fi
    log_info "Gerenciador de pacotes: ${PKG_FAMILY}"
else
    log_error "Sistema operacional não suportado: ${OS}. Use macOS ou Linux."
fi

# ── Função: instalar pacote do sistema ────────────────────────────
install_pkg() {
    local pkg="$1"
    local desc="${2:-$1}"
    if command -v "$pkg" &>/dev/null; then
        log_ok "${pkg} já instalado — ${desc}"
        return
    fi
    log_info "Instalando ${pkg} — ${desc}..."
    if [[ "$PLATFORM" == "macos" ]]; then
        brew install "$pkg" 2>/dev/null || log_warn "Falha ao instalar ${pkg} via brew."
    else
        # Linux: tentar nome de pacote adaptado por família
        local linux_pkg="$pkg"
        case "$pkg" in
            httpx)    linux_pkg="httpx-toolkit" ;;   # Kali/Parrot
            dnsx)     linux_pkg=""               ;;   # via Go
            nuclei)   linux_pkg=""               ;;   # via Go
            subfinder) linux_pkg=""              ;;   # via Go
            amass)    linux_pkg=""               ;;   # via Go
            gobuster) linux_pkg="gobuster"       ;;
            whatweb)  linux_pkg="whatweb"        ;;
            masscan)  linux_pkg="masscan"        ;;
            nmap)     linux_pkg="nmap"           ;;
        esac
        if [[ -n "$linux_pkg" ]]; then
            sudo "${PKG_INSTALL[@]}" "$linux_pkg" 2>/dev/null || log_warn "Falha ao instalar ${pkg}. Instale manualmente."
        else
            log_warn "${pkg} requer instalação via Go: go install github.com/projectdiscovery/... — veja docs."
        fi
    fi
}

# ── macOS: Homebrew ────────────────────────────────────────────────
if [[ "$PLATFORM" == "macos" ]]; then
    if ! command -v brew &>/dev/null; then
        log_info "Homebrew não encontrado. Instalando..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        eval "$("${BREW_PREFIX}/bin/brew" shellenv)"
    else
        log_ok "Homebrew $(brew --version | head -1) já instalado."
    fi
fi

# ── Linux: atualizar índice de pacotes ────────────────────────────
if [[ "$PLATFORM" == "linux" ]]; then
    log_info "Atualizando índice de pacotes..."
    sudo $PKG_UPDATE 2>/dev/null || true
fi

# ── Python 3.11+ ───────────────────────────────────────────────────
PYTHON_CMD=""
PYTHON_OK=false
for py in python3.12 python3.11 python3; do
    if command -v "$py" &>/dev/null; then
        PY_VER=$($py --version 2>&1 | awk '{print $2}')
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
    if [[ "$PLATFORM" == "macos" ]]; then
        log_info "Instalando Python 3.12 via Homebrew..."
        brew install python@3.12
        PYTHON_CMD="${BREW_PREFIX}/bin/python3.12"
    else
        log_info "Instalando Python 3.12 via ${PKG_FAMILY}..."
        case "$PKG_FAMILY" in
            debian) sudo apt-get install -y python3.12 python3.12-venv python3-pip 2>/dev/null \
                        || sudo apt-get install -y python3 python3-venv python3-pip ;;
            rhel)   sudo dnf install -y python3.12 python3-pip 2>/dev/null \
                        || sudo dnf install -y python3 python3-pip ;;
            arch)   sudo pacman -S --noconfirm python python-pip ;;
        esac
        PYTHON_CMD=$(command -v python3.12 || command -v python3)
    fi
fi

# ── Ferramentas de Segurança ───────────────────────────────────────
log_info "Instalando ferramentas de segurança..."

declare -A SEC_TOOLS=(
    ["nmap"]="Scanner de portas e serviços"
    ["masscan"]="Scanner de alta velocidade"
    ["gobuster"]="Enumeração de diretórios/DNS"
    ["whatweb"]="Fingerprinting de tecnologias web"
)
# Ferramentas via Go (independente de OS — usam binários pré-compilados)
declare -A GO_TOOLS=(
    ["subfinder"]="go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    ["dnsx"]="go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
    ["httpx"]="go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
    ["nuclei"]="go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
    ["amass"]="go install -v github.com/owasp-amass/amass/v4/...@master"
)

for tool in "${!SEC_TOOLS[@]}"; do
    install_pkg "$tool" "${SEC_TOOLS[$tool]}"
done

# Ferramentas Go — apenas verifica/orienta (não instala automaticamente Go)
if command -v go &>/dev/null; then
    log_info "Go detectado — instalando ferramentas ProjectDiscovery..."
    for tool in "${!GO_TOOLS[@]}"; do
        if command -v "$tool" &>/dev/null; then
            log_ok "${tool} já instalado."
        else
            log_info "Instalando ${tool}..."
            eval "${GO_TOOLS[$tool]}" 2>/dev/null && log_ok "${tool} instalado." \
                || log_warn "Falha ao instalar ${tool}. Tente: ${GO_TOOLS[$tool]}"
        fi
    done
else
    log_warn "Go não encontrado — ferramentas ProjectDiscovery (subfinder, dnsx, httpx, nuclei, amass) não serão instaladas."
    if [[ "$PLATFORM" == "macos" ]]; then
        echo "     Instale: brew install go"
    else
        echo "     Instale: sudo apt-get install golang-go  (ou equivalente)"
    fi
fi

# ── theHarvester (pip) ────────────────────────────────────────────
if ! command -v theHarvester &>/dev/null; then
    log_info "Instalando theHarvester via pip..."
    $PYTHON_CMD -m pip install theHarvester --quiet || log_warn "Falha ao instalar theHarvester."
else
    log_ok "theHarvester já instalado."
fi

# ── Sherlock (pip) ────────────────────────────────────────────────
if ! command -v sherlock &>/dev/null; then
    log_info "Instalando Sherlock (OSINT username) via pip..."
    $PYTHON_CMD -m pip install sherlock-project --quiet || log_warn "Falha ao instalar sherlock-project."
else
    log_ok "sherlock já instalado."
fi

# ── Blackbird (git clone) ─────────────────────────────────────────
BLACKBIRD_DIR="$(pwd)/blackbird"
BLACKBIRD_VERSION="v0.2.0"  # Pinned to specific tag for security
if [[ -d "$BLACKBIRD_DIR" ]]; then
    log_info "Verificando Blackbird..."
    CURRENT_REF=$(git -C "$BLACKBIRD_DIR" rev-parse --short HEAD 2>/dev/null || echo "unknown")
    log_info "Blackbird atual: ${CURRENT_REF}"
    if ! git -C "$BLACKBIRD_DIR" describe --tags --exact-match &>/dev/null; then
        log_warn "Blackbird não está em um tag release — considere reinstalar."
    fi
else
    log_info "Clonando Blackbird ${BLACKBIRD_VERSION} (OSINT username/email)..."
    if git clone --quiet --branch "$BLACKBIRD_VERSION" --depth 1 https://github.com/p1ngul1n0/blackbird.git "$BLACKBIRD_DIR" 2>/dev/null; then
        ACTUAL_REF=$(git -C "$BLACKBIRD_DIR" rev-parse --short HEAD)
        log_ok "Blackbird ${BLACKBIRD_VERSION} clonado em ${BLACKBIRD_DIR} (${ACTUAL_REF})."
    else
        log_warn "Tag ${BLACKBIRD_VERSION} não encontrado — tentando clone padrão..."
        git clone --quiet https://github.com/p1ngul1n0/blackbird.git "$BLACKBIRD_DIR" \
            && log_ok "Blackbird clonado (latest). Verifique a versão manualmente." \
            || log_warn "Falha ao clonar Blackbird. Verifique sua conexão ou clone manualmente."
    fi
fi

if [[ -f "${BLACKBIRD_DIR}/requirements.txt" ]]; then
    log_info "Instalando dependências do Blackbird..."
    $PYTHON_CMD -m pip install --quiet -r "${BLACKBIRD_DIR}/requirements.txt" \
        || log_warn "Falha ao instalar dependências do Blackbird."
fi

# ── Ambiente Virtual Python ────────────────────────────────────────
VENV_DIR="$(pwd)/.venv-redteam"
if [[ ! -d "$VENV_DIR" ]]; then
    log_info "Criando ambiente virtual isolado em ${VENV_DIR}..."
    # Linux pode precisar de python3-venv instalado
    if [[ "$PLATFORM" == "linux" ]] && ! $PYTHON_CMD -m venv --help &>/dev/null; then
        log_info "Instalando python3-venv..."
        case "$PKG_FAMILY" in
            debian) sudo apt-get install -y python3-venv ;;
            rhel)   sudo dnf install -y python3 python3-libs ;;
            arch)   sudo pacman -S --noconfirm python ;;
        esac
    fi
    $PYTHON_CMD -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

log_info "Instalando dependências Python no venv..."
pip install --quiet --upgrade pip
pip install --quiet \
    dnspython>=2.7.0 \
    shodan>=1.31.0 \
    requests>=2.32.0 \
    rich>=13.9.0 \
    reportlab>=4.2.0 \
    markdown2>=2.5.3 \
    jinja2>=3.1.5 \
    python-nmap>=0.7.1 \
    ipwhois>=1.3.0 \
    beautifulsoup4>=4.13.0 \
    pyfiglet>=1.0.2 \
    cryptography>=46.0.0 \
    sherlock-project>=0.15.0 \
    sublist3r>=1.1

log_ok "Dependências Python instaladas (versões seguras)."

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
log_info "Para enumerar subdomínios:      subfinder -d DOMINIO -o saida.txt"
log_info "Para OSINT de username:         sherlock USERNAME"
log_info "Para OSINT avançado:            python blackbird/blackbird.py -u USERNAME --json"
echo ""
log_warn "LEMBRE-SE: Use apenas em ambientes com autorização documentada."
