#!/usr/bin/env bash
# on_start.sh — Hook executado ao iniciar a skill
# Inicializa dependências temporárias (Tor, etc)
# Uso: source hooks/on_start.sh && on_start

CYAN="\033[0;36m"; GREEN="\033[0;32m"; YELLOW="\033[1;33m"; RESET="\033[0m"

log_info()  { echo -e "${CYAN}[HOOK]${RESET} $*"; }
log_ok()    { echo -e "${GREEN}[HOOK]${RESET} $*"; }
log_warn()  { echo -e "${YELLOW}[HOOK]${RESET} $*"; }
log_error() { echo -e "\033[0;31m[HOOK]${RESET} $*"; }

on_start() {
    # Salvar opções originais da shell
    local ORIG_OPTS="$-"

    set -euo pipefail

    # ── Tor (opcional, para anonimato) ─────────────────────────────────
    setup_tor() {
        if command -v tor &>/dev/null; then
            if ! pgrep -x tor &>/dev/null; then
                log_info "Iniciando Tor..."
                tor --daemon 2>/dev/null || tor --RunAsDaemon 1 &

                # Verificar se Tor está realmente rodando
                sleep 3
                if ! pgrep -x tor &>/dev/null; then
                    log_error "Falha ao iniciar Tor"
                    return 1
                fi

                # Exportar PID para cleanup seguro
                export TOR_PID=$!
                export TOR_PROXY="socks5://127.0.0.1:9050"
                log_ok "Tor ativo em 127.0.0.1:9050 (PID: $TOR_PID)"
            else
                log_ok "Tor já está rodando"
                export TOR_PROXY="socks5://127.0.0.1:9050"
            fi
        else
            log_warn "Tor não instalado — pulando configuração de proxy"
        fi
    }

    # ── Verificar dependências críticas ─────────────────────────────────
    check_dependencies() {
        local missing=()
        for tool in nmap subfinder httpx; do
            if ! command -v "$tool" &>/dev/null; then
                missing+=("$tool")
            fi
        done

        if [[ ${#missing[@]} -gt 0 ]]; then
            log_warn "Dependências faltando: ${missing[*]}"
            log_info "Execute: ./scripts/install.sh"
            return 1
        fi
        log_ok "Todas dependências estão disponíveis"
    }

    # ── Executar setup ──────────────────────────────────────────────────
    log_info "Iniciando hook on_start..."
    setup_tor || return $?
    check_dependencies
    log_ok "Hook on_start concluído"

    # Restaurar opções originais
    eval "set -${ORIG_OPTS}"
}

# Executar se chamado diretamente (não sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    on_start
fi
