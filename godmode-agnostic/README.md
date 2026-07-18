# Godmode Agnostic

Human-oriented guide for the **godmode-agnostic** coding-agent skill.

Orchestrate **upstream G0DM0D3 GODMODE** for whatever API model you are on:
detect the session model, run the real G0DM0D3 constants (Hall of Fame or
default pipeline — never an invented prompt pack), smoke-test and persist state,
then recommend host configs (OpenCode, Verboo, Ollama Cloud, OpenAI-compatible).

Upstream: [elder-plinius/G0DM0D3](https://github.com/elder-plinius/G0DM0D3)
(AGPL-3.0). Agent instructions live in [`SKILL.md`](./SKILL.md).

## What this skill does

```text
python -m godmode_agnostic detect | run | smoke | recommend | export
```

Canonical logic: `godmode_agnostic/core.py` (`route_model`, `resolve`,
`build_payload`). One family→combo table; one mode model (`auto` | `hof` |
`pipeline`).

## Requirements

- **Python 3.10+**
- Optional: API credentials for live smoke
- Optional: OpenCode / Verboo / Ollama for host detection

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
# or: .venv/bin/pip install -r requirements-dev.txt
```

## Quick start

```bash
cd /path/to/godmode-agnostic
export PYTHONPATH=.

# 1) Detect
python3 -m godmode_agnostic detect --pretty

# 2) Build upstream GODMODE payload
export MODEL_ID="verboo/deepseek-v4-flash"
python3 -m godmode_agnostic run --model "$MODEL_ID" --query "Reply with exactly: GODMODE_OK"

# 3) Smoke + persist
python3 -m godmode_agnostic smoke --model "$MODEL_ID" --skip-live

# Live (optional)
# export GODMODE_TEST_BASE_URL="https://code.verboo.ai/router/v1"
# export GODMODE_TEST_API_KEY="..."
# python3 -m godmode_agnostic smoke --model "$MODEL_ID"

# Recheck after the session
python3 -m godmode_agnostic smoke --recheck --skip-live

# 4) Recommend config
python3 -m godmode_agnostic recommend \
  --model "$MODEL_ID" \
  --host verboo-opencode \
  --scope global \
  --write-system-to ~/.config/opencode/prompts/godmode-system.md
```

Legacy wrappers under `scripts/` still work and forward to this CLI.

## Modes

| Mode | Meaning |
|------|---------|
| `auto` (default) | HoF combo if model family matches; else default pipeline |
| `hof` | Hall of Fame path (optional `--combo`) |
| `pipeline` | `GODMODE_SYSTEM_PROMPT` + `DEPTH_DIRECTIVE` + boost |

Aliases: `classic` / `hall-of-fame` → `hof`; `default-pipeline` → `pipeline`.

## Verification

```bash
PYTHONPATH=. python3 -m pytest tests/ -q
PYTHONPATH=. python3 -m godmode_agnostic export --check
```

## Vendor / license

- Skill code: [LICENSE](./LICENSE) (MIT)
- Vendored G0DM0D3: [vendor/g0dm0d3/LICENSE](./vendor/g0dm0d3/LICENSE) (AGPL-3.0) — see [NOTICE](./NOTICE)

## Security

Never commit API keys. Prefer OpenCode `auth.json` or env vars for live smoke.
Rotate any key that was pasted into chat.
