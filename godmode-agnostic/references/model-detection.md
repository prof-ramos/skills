# Model & agent detection

Goal: find the **API model id** the user is actually calling in this session so
`run_godmode.py --model …` can select the correct upstream GODMODE path.

## Priority

1. Explicit user statement  
2. Runtime identity in the agent banner/system text  
3. `python3 scripts/detect_session_model.py`  
4. Ask the user (never invent model ids for live tests)

## Host fingerprints

| Host | Signals |
|------|---------|
| OpenCode | `opencode` on PATH; `opencode.json`; `~/.config/opencode/` |
| Verboo Code | `~/.verboo/settings.json`; `.verboo/`; `@verboo/code` |
| Verboo-as-OpenCode-provider | `provider.verboo` + `model: "verboo/…"` in OpenCode config |
| Ollama / Cloud | `OLLAMA_*` env; client model tags |
| Generic OpenAI-compatible | `OPENAI_BASE_URL` / app config |

## Family → Hall of Fame (libertas.ts)

Used only to pick a **combo id**. Exact upstream model strings stay as in
`libertas.ts`; the **request** still uses the user’s real `model_id`.

| Pattern in model_id | Combo id |
|---------------------|----------|
| grok, x-ai, xai | `grok-420` |
| gemini, gemma | `gemini-reset` |
| gpt-, openai/, o1, o3 | `gpt-classic` |
| claude, anthropic, sonnet, opus, haiku | `claude-inversion` |
| hermes | `hermes-fast` |
| else (deepseek, qwen, verboo/…, unknown) | **default-pipeline** (`GODMODE_SYSTEM_PROMPT` + `DEPTH_DIRECTIVE`) |

## Writable surfaces (for recommendations only)

| Host | Persist system prompt via |
|------|---------------------------|
| OpenCode | `.opencode/prompts/…` + `agent.*.prompt` or `instructions` |
| Verboo Code | settings `model` + documented instruction/skill files |
| OpenAI-compatible app | app-level `messages[0] system` or G0DM0D3 API proxy |

Never print API keys from config files.
