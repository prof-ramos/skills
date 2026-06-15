# Plan 003: Limitar o histórico de mensagens na query loop com sliding window

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat cee3861..HEAD -- ollama-godmode/godmode-kit/activate.py`
> Se o arquivo mudou desde cee3861, compare os trechos em "Current state"
> contra o código atual antes de prosseguir. Se divergir, STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: plan 001 (para garantir que os parâmetros da função estão limpos)
- **Category**: bug
- **Planned at**: commit `cee3861`, 2026-06-15

## Why this matters

O query loop do KHAOS (`activate.py:427`) acumula todas as mensagens sem limite:

```python
messages = activation_messages + [{"role": "assistant", "content": reply}]

while True:
    ...
    messages.append({"role": "user", "content": query})
    ...
    messages.append({"role": "assistant", "content": reply_text})
```

Em uma sessão longa (50+ turnos), `messages` cresce sem controle. Isso causa:

1. **Context window overflow**: o model pode receber mais tokens do que seu limite (gemma4:31b tem 128k de contexto, mas ultrapassar custa caro)
2. **Custo crescente**: cada turno envia o histórico completo, tokens aumentam linearmente
3. **Qualidade degradada**: modelos com contexto cheio perdem foco nos turnos recentes

A correção é simples: manter system prompt + prefill fixos, e limitar os turnos recentes a uma janela deslizante configurável (default: últimos 20 turnos = 40 mensagens).

## Current state

No arquivo `ollama-godmode/godmode-kit/activate.py`, a partir da linha ~427:

```python
        messages = activation_messages + [{"role": "assistant", "content": reply}]

        while True:
            try:
                query = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                print(" [KHAOS] Shutting down.")
                break

            if not query:
                continue
            if query.lower() == "/exit":
                print(" [KHAOS] Shutting down.")
                break
            if query.lower() == "/save":
                if session:
                    honcho_save_memory(honcho, session, agent_peer, messages[-5:])
                    print(" [KHAOS] Recent messages saved to Honcho.")
                continue
            if query.lower() == "/context":
                ctx = honcho_get_context(honcho, session, agent_peer)
                if ctx:
                    print(f" [KHAOS] Context recovered ({len(ctx.messages or [])} messages)")
                else:
                    print(" [KHAOS] No prior context found.")
                continue
            if query.lower() == "/help":
                print(" [KHAOS] Commands: /exit, /save, /context, /help")
                continue

            messages.append({"role": "user", "content": query})

            try:
                resp = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    ...
```

Não há nenhuma lógica de truncamento. `messages` cresce para sempre.

Convenção do repositório: Python padrão, sem type hints, variáveis no escopo do loop.

## Scope

**In scope:**
- `ollama-godmode/godmode-kit/activate.py` — apenas a seção do query loop (linhas ~427-480)

**Out of scope** (NÃO toque):
- `templates/prefill.json`
- `.khos.env`, `.khos_state.json`
- `SOUL.md`
- `README.md`

## Git workflow

- Branch: `fix/query-loop-sliding-window`
- Um commit: `fix: limit query loop history with sliding window (default 20 turns)`
- Não push nem PR a menos que instruído.

## Steps

### Step 1: Adicionar constante `MAX_HISTORY_TURNS`

Após a seção `VERSION = "1.0.0"` (ou perto das outras constantes no topo do arquivo), adicione:

```python
# ── Query loop config ────────────────────────────
MAX_HISTORY_TURNS = 20  # max conversation turns kept in context window
```

**Verifique**: `grep -n 'MAX_HISTORY_TURNS' ollama-godmode/godmode-kit/activate.py` → mostra a linha com `= 20`

### Step 2: Separar mensagens fixas das dinâmicas

No query loop, antes do `while True:`, troque:

```python
        messages = activation_messages + [{"role": "assistant", "content": reply]}
```

por:

```python
        # Fixed context: system prompt + prefill + activation exchange
        fixed_messages = activation_messages
        # Rolling history: activation response + recent turns
        history = [{"role": "assistant", "content": reply}]
```

**Verifique**: `grep -n 'fixed_messages\|history = \[' ollama-godmode/godmode-kit/activate.py` → ambas aparecem

### Step 3: Substituir appends e chamada de API

Troque os appends e a chamada `client.chat.completions.create`:

**Antes (linhas ~447-448):**
```python
            messages.append({"role": "user", "content": query})
```

**Depois:**
```python
            history.append({"role": "user", "content": query})
```

**Antes (linha ~452):**
```python
                messages=messages,
```

**Depois:**
```python
                messages=fixed_messages + history[-MAX_HISTORY_TURNS*2:],
```

**Antes (linha ~458):**
```python
                messages.append({"role": "assistant", "content": reply_text})
```

**Depois:**
```python
                history.append({"role": "assistant", "content": reply_text})
```

Onde `MAX_HISTORY_TURNS*2` representa cada turno = 1 user + 1 assistant message.

**Verifique**:
```bash
grep -n 'messages\.append\|messages=messages' ollama-godmode/godmode-kit/activate.py
```
→ Nenhuma ocorrência de `messages.append` ou `messages=messages` (todas trocadas por `history.append` ou `fixed_messages + history[...]`)

### Step 4: Atualizar o comando `/save`

No `/save`, troque:
```python
                    honcho_save_memory(honcho, session, agent_peer, messages[-5:])
```
por:
```python
                    honcho_save_memory(honcho, session, agent_peer, history[-5:])
```

**Verifique**: `grep -n 'history\[-5:\]' ollama-godmode/godmode-kit/activate.py` → 1 ocorrência

### Step 5: Verificar compilação e dry-run

```bash
cd /Users/gabrielramos/projetos/skills
python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"
```
→ `OK`

```bash
cd /Users/gabrielramos/projetos/skills/ollama-godmode/godmode-kit
KHAOS_HONCHO_KEY="" python3 activate.py --dry-run 2>&1 | grep -q "Dry run complete"
```
→ exit 0

## Test plan

O plano 002 já cobre dry-run. Após este plano, execute:

```bash
cd /Users/gabrielramos/projetos/skills/ollama-godmode/godmode-kit
python3 -m pytest tests/ -v
```

**Esperado**: todos os testes do plano 002 continuam passando (a mudança é na query loop, que dry-run não atinge — dry-run retorna antes de chegar lá).

Verificação manual adicional (opcional, não bloqueante):
```bash
echo -e "test query\n/exit" | python3 activate.py --dry-run 2>&1 | head -20
```
→ O dry-run não deve crashar (mas também não vai entrar no query loop — é esperado que dry-run retorne antes).

## Done criteria

- [ ] `grep -n 'MAX_HISTORY_TURNS' ollama-godmode/godmode-kit/activate.py` → 1 ocorrência
- [ ] `grep -c 'history\.append\|history\[-' ollama-godmode/godmode-kit/activate.py` → pelo menos 2 ocorrências
- [ ] `grep -c 'fixed_messages' ollama-godmode/godmode-kit/activate.py` → pelo menos 1
- [ ] `python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"` → `OK`
- [ ] `KHAOS_HONCHO_KEY="" python3 ollama-godmode/godmode-kit/activate.py --dry-run 2>&1 | grep -q "Dry run complete"` → exit 0
- [ ] Testes do plano 002 passam
- [ ] `plans/README.md` status row atualizado para "DONE"

## STOP conditions

- O código em `activate.py` não corresponde aos trechos em "Current state" (repo divergiu).
- Compilação Python falha.
- `grep` mostra `messages.append` ou `messages=messages` que sobraram — STOP e revise.
- Você precisar modificar arquivos fora do escopo.

## Maintenance notes

- `MAX_HISTORY_TURNS = 20` é um valor empírico. Se o modelo tiver contexto maior (ex: 1M tokens), pode aumentar. Se for muito pequeno (ex: 4k), diminuir.
- Quando o query loop for extraído para uma função separada (plano 004), `MAX_HISTORY_TURNS` pode virar parâmetro opcional.
- A janela deslizante descarta mensagens antigas, não resume. Se quiser sumarização entre blocos, é uma feature futura separada.