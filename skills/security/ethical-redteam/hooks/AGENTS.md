<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-30 | Updated: 2026-03-30 -->

# hooks

## Purpose
Hooks de ciclo de vida da skill — inicializam e encerram serviços temporários (Tor, cleanup) automaticamente.

## Key Files

| File | Description |
|------|-------------|
| `on_start.sh` | Hook de inicialização — inicia Tor (se não rodando), verifica dependências (nmap, subfinder, httpx), exporta `TOR_PID` e `TOR_PROXY` |
| `on_end.sh` | Hook de encerramento — encerra Tor apenas se iniciado pela skill (usa `TOR_PID`), limpa arquivos temporários, unset de env vars |

## For AI Agents

### Working In This Directory
- Hooks são **bash scripts** — devem ser sourced, não executados diretamente, para preservar env vars
- Uso padrão: `source hooks/on_start.sh && on_start`
- **Idempotência:** `on_start.sh` verifica `pgrep -x tor` antes de iniciar nova instância — seguro chamar múltiplas vezes
- `on_start.sh` salva o PID do Tor em `$TOR_PID` para que `on_end.sh` saiba se deve encerrá-lo
- `on_end.sh` só mata o Tor se `$TOR_PID` existir — não encerrará instâncias do Tor que já estavam rodando

### Behavior

| Hook | When | Key Actions |
|------|------|-------------|
| `on_start.sh` | Antes de qualquer operação | Inicia Tor, verifica nmap/subfinder/httpx, exporta `TOR_PROXY` |
| `on_end.sh` | Após gerar relatório | Encerra Tor (se próprio), limpa `*.tmp` em `$XDG_RUNTIME_DIR/ethical-redteam-skill` |

### Error Handling

| Hook | Estratégia | Detalhe |
|------|-----------|---------|
| `on_start.sh` | Aviso se Tor falhar, return 1 se deps faltarem | `log_warn` para Tor ausente, `return 1` em `check_dependencies()` |
| `on_end.sh` | Tolerante a falhas de cleanup | `|| true` em todos os comandos de deleção/kill |

> Tor só é encerrado se `$TOR_PID` estiver definido (foi iniciado pelo hook) — não afeta instâncias externas do Tor.

### Environment Variables

| Variable | Set by | Purpose |
|----------|--------|---------|
| `TOR_PID` | `on_start.sh` | PID do processo Tor para cleanup seguro |
| `TOR_PROXY` | `on_start.sh` | URL do proxy SOCKS5 (`socks5://127.0.0.1:9050`) |

### Legal e Ética

Os hooks **não executam operações de scanning** — apenas inicializam/encerram Tor e verificam dependências. A validação legal é feita por cada módulo Python individualmente via `utils.exibir_disclaimer_e_validar()`, que requer autorização escrita, escopo definido e RoE documentado antes de qualquer ação.

## Dependencies

### Internal
- `scripts/install.sh` — Instala as dependências verificadas pelos hooks
- `check-deps.sh` — Verificação completa de dependências (mais abrangente que os hooks)

### External
- `tor` — Daemon Tor para anonimato (opcional — hooks emitem aviso se ausente, mas continuam execução)
- `nmap`, `subfinder`, `httpx` — Verificados por `on_start.sh` (falham se ausentes)

<!-- MANUAL: -->
