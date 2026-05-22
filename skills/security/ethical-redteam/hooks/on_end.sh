#!/usr/bin/env bash
# on_end.sh — Hook executado após gerar relatório
# Encerra serviços e limpa temporários
# Uso: source hooks/on_end.sh && on_end

CYAN="\033[0;36m"; GREEN="\033[0;32m"; RESET="\033[0m"

log_info()  { echo -e "${CYAN}[HOOK]${RESET} $*"; }
log_ok()    { echo -e "${GREEN}[HOOK]${RESET} $*"; }

on_end() {
    local ORIG_OPTS="$-"
    set -euo pipefail

    # Diretório temporário controlado
    local TEMP_DIR="${XDG_RUNTIME_DIR:-/tmp}/ethical-redteam-skill"
    mkdir -p "$TEMP_DIR" 2>/dev/null || true

    # ── Parar Tor se foi iniciado pela skill ────────────────────────────
    cleanup_tor() {
        if [[ -n "${TOR_PID:-}" ]] && kill -0 "$TOR_PID" 2>/dev/null; then
            log_info "Encerrando Tor (PID: $TOR_PID)..."
            kill "$TOR_PID" 2>/dev/null || true
            wait "$TOR_PID" 2>/dev/null || true
            log_ok "Tor encerrado"
        fi
        unset TOR_PID TOR_PROXY 2>/dev/null || true
    }

    # ── Limpar arquivos temporários ─────────────────────────────────────
    cleanup_temp() {
        if [[ -d "$TEMP_DIR" ]]; then
            find "$TEMP_DIR" -name "*.tmp" -type f -delete 2>/dev/null || true
            log_ok "Arquivos temporários removidos de $TEMP_DIR"
        fi
    }

    # ── Executar cleanup ────────────────────────────────────────────────
    log_info "Iniciando hook on_end (cleanup)..."
    cleanup_tor
    cleanup_temp
    log_ok "Hook on_end concluído — ambiente limpo"

    eval "set -${ORIG_OPTS}"
}

# Executar se chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    on_end
fi
