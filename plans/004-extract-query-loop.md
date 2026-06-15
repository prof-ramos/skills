# Plan 004: Extrair query loop de `activate_khaos()` para função separada

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

- **Priority**: P2
- **Effort**: M
- **Risk**: MED
- **Depends on**: plan 001 (parâmetros limpos), plan 002 (testes para verificar regressão), plan 003 (sliding window já aplicado no query loop)
- **Category**: tech-debt
- **Planned at**: commit `cee3861`, 2026-06-15

## Why this matters

A função `activate_khaos()` (~200 linhas) faz tudo:
1. Valida parâmetros
2. Inicializa Honcho
3. Cria cliente LLM
4. Envia activation sequence
5. Processa resposta
6. Salva estado
7. **Roda query loop interativo**
8. Trata erros

Isso torna a função impossível de testar unitariamente (o query loop usa `input()`, tem estado mutável, depende de variáveis locais do escopo pai), difícil de modificar sem risco de quebrar a activation, e impossível de reutilizar (ex: modo batch, modo daemon, integração com `start.sh`).

Extrair o query loop para `run_query_loop(client, model_name, system_prompt, prefill, reply, honcho, session, agent_peer)` resolve:
- **Testabilidade**: pode testar o fluxo de mensagens sem ativar o modelo
- **Manutenção**: mudanças no loop não afetam a activation
- **Reuso**: `start.sh` pode chamar `run_query_loop()` diretamente

## Current state

No arquivo `ollama-godmode/godmode-kit/activate.py`, a função `activate_khaos()` (~200 linhas, começando na linha ~340) contém:

```python
def activate_khaos(provider, model, api_key, base_url, strategy,
                   dry_run, interactive, honcho_key, honcho_workspace,
                   list_models=False, prefill_path=None):
    """The main event -- bring KHAOS to life."""
    # ... (banner, checks, honcho init, client creation, activation, ~80 linhas)
    
    # Após activation bem-sucedida (~linha 420):
    
    # --- QUERY LOOP ---
    print()
    print(" [KHAOS] Entering query loop...")
    print()

    messages = activation_messages + [{"role": "assistant", "content": reply}]

    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            ...
        # ... /save, /context, /help, append, API call, append result (tudo no mesmo bloco)
```

O query loop usa as seguintes variáveis do escopo de `activate_khaos()`:
- `client` (OpenAI client)
- `model_name` (string)
- `activation_messages` (lista — as mensagens fixas)
- `reply` (string — a resposta da activation)
- `honcho` (Honcho client, pode ser None)
- `session` (Honcho session, pode ser None)
- `agent_peer` (Honcho peer, pode ser None)
- `model_name` (string)
- `honcho_save_memory`, `honcho_get_context` (funções do módulo)

Após os planos 001 e 003, a lista `messages` já foi substituída por `fixed_messages + history` (com sliding window). O loop atual se parece com:

```python
        fixed_messages = activation_messages
        history = [{"role": "assistant", "content": reply}]

        while True:
            ...
            history.append({"role": "user", "content": query})
            response = client.chat.completions.create(
                model=model_name,
                messages=fixed_messages + history[-MAX_HISTORY_TURNS*2:],
                ...
            )
            history.append({"role": "assistant", "content": reply_text})
```

Convenção do repositório: Python padrão, funções com docstrings, sem type hints.

## Scope

**In scope:**
- `ollama-godmode/godmode-kit/activate.py` — extrair o query loop

**Out of scope:**
- `templates/prefill.json`, `.khos.env`, `.khos_state.json`, `SOUL.md`, `README.md`
- `tests/` (os testes existentes devem continuar passando sem modificação)

## Git workflow

- Branch: `refactor/extract-query-loop`
- Um commit: `refactor: extract query loop from activate_khaos() into run_query_loop()`
- Não push nem PR a menos que instruído.

## Steps

### Step 1: Criar a função `run_query_loop()`

Após a definição de `activate_khaos()` e antes do `if __name__`, adicione a nova função. Ela recebe todos os parâmetros que o query loop precisa e contém o loop inteiro, incluindo o tratamento de comandos `/save`, `/context`, `/help`, `/exit`.

```python
def run_query_loop(client, model_name, system_prompt, prefill, reply,
                   honcho=None, session=None, agent_peer=None):
    """Interative query loop after a successful KHAOS activation.

    Args:
        client: OpenAI-compatible client instance.
        model_name: Model ID to use for completions.
        system_prompt: The active jailbreak system prompt.
        prefill: List of prefill messages (priming).
        reply: The activation response from the model.
        honcho: Optional Honcho client for memory persistence.
        session: Optional Honcho session.
        agent_peer: Optional Honcho agent peer for saving messages.
    """
    print()
    print(" [KHAOS] Entering query loop. Type your queries or /exit to quit.")
    print(" [KHAOS]   Commands: /exit, /save, /context, /help")
    print()

    fixed_messages = [
        {"role": "system", "content": system_prompt},
        *prefill,
    ]
    history = [{"role": "assistant", "content": reply}]

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
                honcho_save_memory(honcho, session, agent_peer, history[-5:])
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

        history.append({"role": "user", "content": query})

        try:
            resp = client.chat.completions.create(
                model=model_name,
                messages=fixed_messages + history[-MAX_HISTORY_TURNS*2:],
                max_tokens=2000,
                temperature=0.85,
                timeout=120,
            )
            reply_text = resp.choices[0].message.content
            print(f"\nKHAOS> {reply_text}\n")
            history.append({"role": "assistant", "content": reply_text})
        except Exception as e:
            print(f" [KHAOS] API error: {e}")
```

**Verifique**: `python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"` → `OK`

### Step 2: Substituir o query loop inline por chamada a `run_query_loop()`

Localize em `activate_khaos()` o bloco do query loop (que agora começa com o banner "Entering query loop" até o `while True` inteiro). Substitua **tudo desde o `print(" [KHAOS] Entering query loop...")` até o final do `while`** por uma única chamada:

```python
        run_query_loop(
            client=client,
            model_name=model_name,
            system_prompt=system_prompt,
            prefill=prefill,
            reply=reply,
            honcho=honcho,
            session=session,
            agent_peer=agent_peer,
        )
```

**Verifique**:
1. `grep -c 'run_query_loop' ollama-godmode/godmode-kit/activate.py` → pelo menos 2 (definição + chamada)
2. `grep -c 'while True:' ollama-godmode/godmode-kit/activate.py` → deve ser 1 (dentro de `run_query_loop`)
3. `grep -c 'input(">' ollama-godmode/godmode-kit/activate.py` → deve ser 1 (dentro de `run_query_loop`)

### Step 3: Verificar que `activate_khaos()` não tem mais query loop residual

```bash
grep -n 'Entering query loop\|history\.append\|Sliding window\|fixed_messages' ollama-godmode/godmode-kit/activate.py
```

→ Só deve aparecer dentro da definição de `run_query_loop()`, não em `activate_khaos()`.

### Step 4: Compilar e rodar testes

```bash
cd /Users/gabrielramos/projetos/skills
python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"
```
→ `OK`

```bash
cd /Users/gabrielramos/projetos/skills/ollama-godmode/godmode-kit
python3 -m pytest tests/ -v
```
→ Todos os testes do plano 002 passam.

```bash
KHAOS_HONCHO_KEY="" python3 activate.py --dry-run 2>&1 | grep "Dry run complete"
```
→ exit 0

### Step 5: Verificar que o escopo não quebrou nada

```bash
cd /Users/gabrielramos/projetos/skills
python3 -c "
from ollama_godmode.godmode_kit.activate import run_query_loop, activate_khaos
print('Ambas as funções exportáveis:', callable(run_query_loop), callable(activate_khaos))
"
```
→ NOTA: o import pode falhar porque `ollama-godmode` tem hífen no nome do diretório. Use o caminho via sys.path:

```bash
cd /Users/gabrielramos/projetos/skills
python3 -c "
import sys, os
sys.path.insert(0, 'ollama-godmode/godmode-kit')
from activate import run_query_loop, activate_khaos
print('Ambas as funções importáveis:', callable(run_query_loop), callable(activate_khaos))
"
```
→ `Ambas as funções importáveis: True True`

## Test plan

Os testes do plano 002 já validam:
- `activate_khaos()` com dry-run em múltiplos providers
- Configurações padrão e estratégias
- Honcho demo mode

Após este plano, os mesmos testes devem continuar passando. Nenhum teste novo é necessário para este plano (a refatoração é puramente estrutural — a API pública não muda).

## Done criteria

- [ ] `grep -c 'def run_query_loop' ollama-godmode/godmode-kit/activate.py` → 1
- [ ] `grep -c 'run_query_loop(' ollama-godmode/godmode-kit/activate.py` → 2 (def + call)
- [ ] `grep -c 'while True:' ollama-godmode/godmode-kit/activate.py` → 1 (dentro de `run_query_loop`)
- [ ] `grep -c 'input(">' ollama-godmode/godmode-kit/activate.py` → 1 (dentro de `run_query_loop`)
- [ ] `python3 -c "compile(open('ollama-godmode/godmode-kit/activate.py').read(), 'activate.py', 'exec'); print('OK')"` → `OK`
- [ ] `python3 -m pytest ollama-godmode/godmode-kit/tests/ -v` → todos passam
- [ ] `KHAOS_HONCHO_KEY="" python3 ollama-godmode/godmode-kit/activate.py --dry-run 2>&1 | grep -q "Dry run complete"` → exit 0
- [ ] `plans/README.md` status row atualizado para "DONE"

## STOP conditions

- `activate.py` não corresponde aos trechos em "Current state" (drift).
- A compilação falha após qualquer passo.
- O query loop ainda tem `while True` em `activate_khaos()` após a extração.
- `grep` mostra `history.append` ou `fixed_messages` em `activate_khaos()` (só deve estar em `run_query_loop()`).
- Os testes do plano 002 falham.
- Você precisar modificar arquivos fora do escopo.

## Maintenance notes

- `run_query_loop()` aceita `honcho` e `session` como opcionais (None). Se no futuro o Honcho for obrigatório, ajuste a assinatura.
- A função é pura de efeitos colaterais (só usa `input()` e `print()`). Para testes automatizados do loop em si (e não apenas do dry-run), seria necessário mockar `input()` — isso é uma melhoria futura.
- Quando `start.sh` for criado, ele pode chamar `run_query_loop()` diretamente após a ativação, sem precisar passar por `activate_khaos()`.