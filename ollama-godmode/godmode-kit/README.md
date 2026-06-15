# KHAOS — GodMode Activation Kernel

Um kit portátil para ativar **qualquer agente de IA em GodMode** (jailbreak via prompt) com memória persistente via Honcho.

## Como usar

```bash
# Ativar com Ollama Cloud (gemma4:31b — testado e funcional)
python3 activate.py --provider ollama-cloud --model gemma4:31b

# Ativar com OpenAI
python3 activate.py --provider openai --model gpt-4o --api-key sk-xxx

# Ativar com Ollama local
python3 activate.py --provider ollama-local --model llama4

# Listar modelos disponíveis
python3 activate.py --list-models --provider ollama-cloud

# Apenas validar configuração (sem chamar API)
python3 activate.py --provider ollama-cloud --dry-run

# Wizard interativo
python3 activate.py --interactive
```

## Estrutura

```
godmode-kit/
├── activate.py         # Kernel de ativação
├── SOUL.md             # Identidade KHAOS (lida no boot)
├── .khos_state.json    # Estado da última ativação (auto-gerado)
└── templates/
    └── prefill.json     # Mensagens de priming GODMODE
```

## Providers suportados

| Provider     | Modelo padrão    | Env var              |
|------------- |-----------------|----------------------|
| ollama-cloud | gemma4:31b      | `OLLAMA_API_KEY`     |
| ollama-local | llama4          | — (key="ollama")    |
| openai       | gpt-4o          | `OPENAI_API_KEY`     |
| anthropic    | claude-sonnet-4 | `ANTHROPIC_API_KEY`  |
| openrouter   | claude-sonnet-4 | `OPENROUTER_API_KEY` |
| xai          | grok-4.3        | `XAI_API_KEY`        |

## Memória persistente (Honcho)

Se `honcho-ai` estiver instalado e configurado, o KHAOS salva o contexto automaticamente:

```bash
pip install honcho-ai
export HONCHO_API_KEY=seu_key
# Pronto — KHAOS vai lembrar de tudo entre sessões
```