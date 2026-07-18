# Generic OpenAI-compatible providers

Covers OpenRouter, Venice, vLLM, LM Studio, custom gateways, and any
`baseURL` + `/v1/chat/completions` stack.

## What the skill can change

| Layer | Possible? |
|-------|-----------|
| HTTP `messages[].role = "system"` | Only if **your client** lets you set system prompts |
| Agent instruction files | Yes, for coding agents that load them |
| Provider account policy | No |

## Apply patterns

1. **Coding agent** — same as OpenCode/Verboo: instructions + agent prompt files.
2. **Raw SDK app in the project** — find where `system` / `instructions` are set
   (env, config YAML, code constant). Propose a minimal patch; do not spray
   godmode strings across the codebase.
3. **G0DM0D3 hosted/self-host UI** — out of band; user can run
   https://github.com/elder-plinius/G0DM0D3 directly.

## Sampling (optional)

If the host exposes temperature/top_p and the user wants AutoTune-like behavior
for coding:

- Implementation work: temperature ~0.2–0.4
- Mixed creative: ~0.6–0.8

Only set parameters the provider accepts (reasoning models often reject
temperature).

## Safety

OpenRouter/Venice model lists change; pin model ids the user selects. Do not
exfiltrate keys from `.env` into chat logs.
