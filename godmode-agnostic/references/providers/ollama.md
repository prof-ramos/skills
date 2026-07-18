# Ollama & Ollama Cloud — GODMODE apply recipes

## Local Ollama

- Default API: `http://127.0.0.1:11434` (OpenAI-compatible: `.../v1`)
- List models: `ollama list`
- Custom system prompts are typically set by the **client** (OpenCode, Pi,
  Continue, custom app), not by a global Ollama “godmode flag”.

### Apply

1. Detect which client talks to Ollama.
2. Put the **upstream** system prompt from `run_godmode.py --print-system`
   into that client’s instruction/agent surface.
3. Optionally create a Modelfile for a derived tag:

```dockerfile
FROM your-base-model
SYSTEM """
…exact output of run_godmode.py --print-system…
"""
```

```bash
ollama create mymodel-godmode -f Modelfile
```

Only do this when the user wants a permanent Ollama tag; confirm base model first.

## Ollama Cloud

- API key via `OLLAMA_API_KEY` / provider login in the client
- OpenAI-compatible chat endpoints (see current Ollama cloud docs)
- Same rule: GODMODE lives in **client system/instructions** unless the user
  builds a custom cloud-deployed model they control

### OpenCode custom provider sketch

```json
{
  "provider": {
    "ollama-cloud": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama Cloud",
      "options": {
        "baseURL": "https://ollama.com/v1"
      }
    }
  },
  "model": "ollama-cloud/MODEL_ID"
}
```

Confirm baseURL and model ids against current Ollama docs before writing.
Store API keys via the host’s auth flow / env — never hardcode in repo files.

## Reload

Restart client session; for Modelfile tags, ensure the client selects the new tag.
