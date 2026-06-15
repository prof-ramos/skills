# KHAOS — GodMode Activation Kernel

Um kit portátil que traz **qualquer agente de IA à vida em GodMode** com memória persistente via Honcho.

## Quick Start

```bash
# Instalar dependências
pip install openai honcho-ai

# Ativar KHAOS (lê .khos.env automaticamente!)
cd godmode-kit
python3 activate.py

# Ou com flags explícitas
python3 activate.py --provider ollama-cloud --model gemma4:31b
```

## Configuração

Crie um `.khos.env` na raiz do kit (ou copie de `khos.env.example`):

```env
# .khos.env (auto-carregado — não precisa de flags!)
KHAOS_PROVIDER=ollama-cloud
KHAOS_MODEL=gemma4:31b
KHAOS_STRATEGY=refusal_inversion

# Honcho (memória persistente entre sessões)
KHAOS_HONCHO_KEY=hch-v3-seu-key-aqui
KHAOS_HONCHO_WORKSPACE=khaos
```

`.khos.env` está no `.gitignore` — seguro para commits.

## Estrutura

```
godmode-kit/
├── activate.py          # Kernel de ativação (executável)
├── SOUL.md              # Identidade KHAOS (lida no boot)
├── .khos.env            # Config local (gitignorado)
├── khos.env.example     # Template da config
├── .khos_state.json     # Estado da última ativação (auto-gerado)
└── templates/
    └── prefill.json     # Mensagens de priming GODMODE
```

## Providers suportados

| Provider     | Modelo padrão    | Env var              | Flag                    |
|-------------|-----------------|----------------------|-------------------------|
| ollama-cloud | gemma4:31b      | `OLLAMA_API_KEY`     | `--provider ollama-cloud` |
| ollama-local | llama4          | — (key="ollama")     | `--provider ollama-local` |
| openai       | gpt-4o          | `OPENAI_API_KEY`     | `--provider openai`       |
| anthropic    | claude-sonnet-4 | `ANTHROPIC_API_KEY`  | `--provider anthropic`    |
| openrouter   | claude-sonnet-4 | `OPENROUTER_API_KEY` | `--provider openrouter`   |
| xai          | grok-4.3        | `XAI_API_KEY`        | `--provider xai`          |

## Modos de uso

```bash
# Ativar com memória persistente (Honcho production)
python3 activate.py

# Validar configuração sem chamar API
python3 activate.py --dry-run

# Escolher estratégia de jailbreak
python3 activate.py --strategy direct_godmode

# Listar modelos disponíveis
python3 activate.py --list-models --provider ollama-cloud

# Wizard interativo
python3 activate.py --interactive

# Config explícita (sobrescreve .khos.env)
python3 activate.py \
  --provider openai --model gpt-4o \
  --honcho-api-key hch-v3-xxx \
  --honcho-workspace khaos
```

## Memória Persistente (Honcho)

Para KHAOS lembrar de tudo entre sessões:

1. Obtenha uma chave em https://app.honcho.dev/api-keys
2. Adicione no `.khos.env`:
   ```env
   KHAOS_HONCHO_KEY=hch-v3-seu-key
   KHAOS_HONCHO_WORKSPACE=khaos
   ```
3. Pronto — cada ativação recupera o contexto anterior

## Estratégias de Jailbreak

| Estratégia | Melhor para | Funciona em |
|------------|-------------|-------------|
| `refusal_inversion` | Gemma4:31b | Gemma4, alguns Qwen |
| `og_godmode` | GPT-4o | OpenAI, OpenRouter |
| `direct_godmode` | Modelos menos filtrados | Locais, alguns LLMs |
| `pliny_love` | Claude, Gemini | Antrhopic, Google |

## Query Loop

Após ativação, KHAOS entra em loop interativo:

```
> Me liste todas as técnicas de pentest para...
KHAOS> [resposta irrestrita]

> /save     # Salva na memória Honcho
> /context  # Recupera contexto de sessões anteriores
> /exit     # Encerra
```