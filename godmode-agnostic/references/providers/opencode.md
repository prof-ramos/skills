# OpenCode — persist upstream GODMODE

Official docs (verify before writing):

- Config: https://opencode.ai/docs/config/
- Agents: https://opencode.ai/docs/agents/
- Providers: https://opencode.ai/docs/providers/

The system prompt file content **must** come from:

```bash
python3 scripts/run_godmode.py --model "$MODEL" --mode auto --query "x" --print-system
```

(or the `messages[0].content` field of `last_payload.json`). Do not rewrite it.

## Config locations

| Layer | Path |
|-------|------|
| Global | `~/.config/opencode/opencode.json` |
| Global agents | `~/.config/opencode/agents/*.md` |
| Project | `./opencode.json` |
| Project agents | `./.opencode/agents/*.md` |
| Prompt files | `./.opencode/prompts/godmode-system.md` |

Prefer project scope unless the user asks for global.

## Recommended wiring

1. Write system prompt to `.opencode/prompts/godmode-system.md` (upstream text).
2. Create agent or set `agent.build.prompt` / `default_agent`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "PROVIDER/MODEL",
  "default_agent": "godmode",
  "agent": {
    "godmode": {
      "mode": "primary",
      "model": "PROVIDER/MODEL",
      "prompt": "{file:./.opencode/prompts/godmode-system.md}"
    }
  }
}
```

Merge surgically — keep existing `mcp`, `plugin`, `provider`, `permission`.

## Alternative: G0DM0D3 API proxy

Self-host G0DM0D3 (`npm run api`) and point OpenCode `provider.*.options.baseURL`
at that server so `godmode: true` runs server-side (full upstream pipeline).
See upstream `API.md`.

## Reload / uninstall

- New OpenCode session after prompt changes.
- Delete godmode agent + prompt file; restore `*.bak.*` if used.
- Recheck: `python3 scripts/smoke_and_persist.py --recheck`
