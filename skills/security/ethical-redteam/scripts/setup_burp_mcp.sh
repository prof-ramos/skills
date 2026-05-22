#!/usr/bin/env bash
# setup_burp_mcp.sh — Configuração do Burp Suite MCP Server (PLUS Feature)
#
# ⚠️  AVISO: Esta é uma funcionalidade OPCIONAL que requer Burp Suite.
# O ethical-redteam-skill funciona perfeitamente SEM esta integração.
#
# Requisitos adicionais:
#   - Burp Suite (Community ou Pro)
#   - Java Runtime (OpenJDK)
#   - MCP Server Extension da PortSwigger
#
# Uso: ./scripts/setup_burp_mcp.sh [install|check|status]

set -euo pipefail

# ── Cores ───────────────────────────────────────────────────────────────────────
CYAN="\033[0;36m"; GREEN="\033[0;32m"; YELLOW="\033[1;33m"; RED="\033[0;31m"; RESET="\033[0m"

log_info()  { echo -e "${CYAN}[SETUP]${RESET} $*"; }
log_ok()    { echo -e "${GREEN}[SETUP]${RESET} $*"; }
log_warn()  { echo -e "${YELLOW}[SETUP]${RESET} $*"; }
log_error() { echo -e "${RED}[SETUP]${RESET} $*"; }

# ── Configurações ───────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TOOLS_DIR="$PROJECT_ROOT/tools"
MCP_JAR="$TOOLS_DIR/burp-mcp-all.jar"
MCP_REPO="/tmp/mcp-server"
MCP_VERSION="latest"
BURP_MCP_HOST="127.0.0.1"
BURP_MCP_PORT="9876"
BURP_PROXY_PORT="8080"

# ── Funções ─────────────────────────────────────────────────────────────────────

check_java() {
    log_info "Verificando Java..."

    # Tentar usar JAVA_HOME do Homebrew
    if [ -d "/opt/homebrew/opt/openjdk" ]; then
        export JAVA_HOME="/opt/homebrew/opt/openjdk"
        export PATH="$JAVA_HOME/bin:$PATH"
    fi

    if ! command -v java &>/dev/null; then
        log_error "Java não encontrado. Instalando OpenJDK..."
        if command -v brew &>/dev/null; then
            brew install openjdk
            export JAVA_HOME="$(brew --prefix openjdk)"
            export PATH="$JAVA_HOME/bin:$PATH"
        else
            log_error "Homebrew não encontrado. Instale Java manualmente."
            return 1
        fi
    fi

    local java_version
    java_version=$(java -version 2>&1 | head -1)
    log_ok "Java encontrado: $java_version"
}

install_mcp_jar() {
    log_info "Verificando Burp MCP JAR..."

    if [ -f "$MCP_JAR" ]; then
        local size
        size=$(du -h "$MCP_JAR" | cut -f1)
        log_ok "JAR já existe: $MCP_JAR ($size)"
        return 0
    fi

    log_info "Baixando código fonte do Burp MCP Server..."
    if [ -d "$MCP_REPO" ]; then
        log_warn "Repositório já existe, atualizando..."
        (cd "$MCP_REPO" && git pull)
    else
        git clone --depth 1 https://github.com/PortSwigger/mcp-server.git "$MCP_REPO"
    fi

    log_info "Compilando JAR (isso pode levar alguns minutos)..."
    (
        cd "$MCP_REPO"
        export JAVA_HOME="$(brew --prefix openjdk)"
        export PATH="$JAVA_HOME/bin:$PATH"
        ./gradlew embedProxyJar
    )

    log_info "Copiando JAR para $TOOLS_DIR..."
    mkdir -p "$TOOLS_DIR"
    cp "$MCP_REPO/build/libs/burp-mcp-all.jar" "$MCP_JAR"

    local size
    size=$(du -h "$MCP_JAR" | cut -f1)
    log_ok "JAR criado: $MCP_JAR ($size)"
}

check_mcp_connection() {
    log_info "Verificando conexão com Burp MCP Server..."
    log_info "Endpoint: http://${BURP_MCP_HOST}:${BURP_MCP_PORT}"

    if curl -sf "http://${BURP_MCP_HOST}:${BURP_MCP_PORT}/" &>/dev/null; then
        log_ok "Burp MCP Server está rodando!"
        return 0
    else
        log_warn "Burp MCP Server NÃO está respondendo."
        return 1
    fi
}

test_burp_script() {
    log_info "Testando script burp_mcp.py..."

    if [ ! -f "$PROJECT_ROOT/scripts/burp_mcp.py" ]; then
        log_error "burp_mcp.py não encontrado em $PROJECT_ROOT/scripts/"
        return 1
    fi

    python3 "$PROJECT_ROOT/scripts/burp_mcp.py" --check
}

show_manual_setup() {
    cat <<'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║              ⚠️  BURP SUITE MCP - FUNCIONALIDADE PLUS                      ║
║                                                                            ║
║  Esta é uma integração OPCIONAL para usuários avançados.                   ║
║  O ethical-redteam-skill funciona PERFEITAMENTamente sem Burp Suite.      ║
║                                                                            ║
║  Use apenas se você já possui Burp Suite e deseja recursos extras.        ║
╚════════════════════════════════════════════════════════════════════════════╝

📦 O JAR está compilado e pronto em: tools/burp-mcp-all.jar

Para usar, siga estes passos MANUAIS (requer Burp Suite aberto):

1️⃣  ABRIR BURP SUITE
   • Use Burp Suite Community (grátis) ou Pro
   • Certifique-se que o proxy está em 127.0.0.1:8080

2️⃣  CARREGAR EXTENSÃO MCP
   • Vá para: Extensions → Add → Java
   • Selecione: ]]EOF
echo -n "$MCP_JAR"
cat <<'EOF'
   • Clique "Next" e "Finish"

3️⃣  HABILITAR MCP SERVER
   • Nova aba "MCP" aparecerá
   • Configure:
     - Server Host: 127.0.0.1
     - Server Port: 9876
   • Clique "Start Server"

4️⃣  TESTAR
   python3 scripts/burp_mcp.py --check

╔════════════════════════════════════════════════════════════════════════════╗
║                         FLUXO DE USO                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

1. Configure browser para usar proxy 127.0.0.1:8080
2. Navegue no alvo para gerar tráfego
3. Execute:
   python3 scripts/burp_mcp.py --mode history --output scan_output/

EOF
}

show_status() {
    # Setup Java from Homebrew if available
    local java_bin=""
    local java_ver=""

    if [ -x "/opt/homebrew/opt/openjdk/bin/java" ]; then
        java_bin="/opt/homebrew/opt/openjdk/bin/java"
        java_ver=$("$java_bin" -version 2>&1 | head -1)
    elif [ -n "${JAVA_HOME:-}" ] && [ -x "$JAVA_HOME/bin/java" ]; then
        java_bin="$JAVA_HOME/bin/java"
        java_ver=$("$java_bin" -version 2>&1 | head -1)
    fi

    echo ""
    echo "┌─────────────────────────────────────────────────────────────────┐"
    echo "│                    BURP MCP STATUS                             │"
    echo "├─────────────────────────────────────────────────────────────────┤"

    # Java
    if [ -n "$java_ver" ]; then
        echo "│ Java          │ ✅ $java_ver"
    else
        echo "│ Java          │ ❌ Não encontrado (instale: brew install openjdk)"
    fi

    # JAR
    if [ -f "$MCP_JAR" ]; then
        size=$(du -h "$MCP_JAR" | cut -f1)
        echo "│ MCP JAR       │ ✅ $MCP_JAR ($size)"
    else
        echo "│ MCP JAR       │ ❌ Não encontrado (execute: ./scripts/setup_burp_mcp.sh install)"
    fi

    # MCP Server
    local mcp_running=false
    if curl -sf "http://${BURP_MCP_HOST}:${BURP_MCP_PORT}/" &>/dev/null; then
        mcp_running=true
    fi

    if [ "$mcp_running" = true ]; then
        echo "│ MCP Server    │ ✅ Rodando em :$BURP_MCP_PORT"
    else
        echo "│ MCP Server    │ ⚠️  Não rodando (requer Burp Suite + extensão MCP)"
    fi

    echo "└─────────────────────────────────────────────────────────────────┘"
    echo ""
}

# ── Main ────────────────────────────────────────────────────────────────────────

main() {
    local command="${1:-status}"

    case "$command" in
        install)
            log_info "Iniciando instalação do Burp MCP..."
            check_java
            install_mcp_jar
            show_status
            show_manual_setup
            ;;

        check)
            check_java
            check_mcp_connection || true
            test_burp_script || true
            show_status
            ;;

        status)
            show_status
            ;;

        *)
            echo "Uso: $0 {install|check|status}"
            echo ""
            echo "Comandos:"
            echo "  install   Baixa e compila o Burp MCP JAR"
            echo "  check     Verifica conectividade com o MCP Server"
            echo "  status    Mostra status da instalação"
            exit 1
            ;;
    esac
}

main "$@"
