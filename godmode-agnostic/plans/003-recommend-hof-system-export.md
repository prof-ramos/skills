# Plan 003: Export clean system prompts for recommend/apply (no query injection)

> **Executor instructions**: Follow step by step. Verify each gate. Update
> `plans/README.md` when done.
>
> **Drift check**:
> `git diff --stat 3abca90..HEAD -- scripts/recommend_config.py scripts/run_godmode.py`

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: plans/001-verification-baseline.md
- **Category**: bug
- **Planned at**: commit `3abca90`, 2026-07-18

## Why this matters

`recommend_config.py` builds a payload with `query="{QUERY}"` then takes the
system message. For **default-pipeline** that is fine (system has no
placeholders). For **Hall of Fame** combos (e.g. grok-420), `inject_query`
replaces `{Z}` / `{QUERY}` **inside the system template** with the literal
string `{QUERY}`, corrupting the system prompt written to
`godmode-system.md` for OpenCode. Persistence then installs a broken prompt.

Also fix OpenCode global prompt path: use paths **relative to the config file**
(`./prompts/godmode-system.md`), not `{file:~/.config/...}` which OpenCode may
not resolve (finding #6).

## Current state

```python
# scripts/recommend_config.py ~129-136
payload = build_payload(
    model_id=args.model,
    query="{QUERY}",
    mode=args.mode if args.mode != "auto" else "classic",
    combo_id=args.combo,
    temperature=None,
)
system = next(m["content"] for m in payload["messages"] if m["role"] == "system")
```

```python
# scripts/recommend_config.py ~53-64 — broken global path form
"prompt": "{file:./.opencode/prompts/godmode-system.md}"
if scope == "project"
else "{file:~/.config/opencode/prompts/godmode-system.md}",
```

Repro (must fail before fix, pass after):

```bash
PYTHONPATH=scripts python3 -c "
from run_godmode import build_payload
p=build_payload(model_id='x-ai/grok-4', query='{QUERY}', mode='classic', combo_id=None, temperature=None)
sys=p['messages'][0]['content']
assert '{QUERY}' in sys  # pollution today
"
```

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Tests | `PYTHONPATH=scripts python3 -m pytest tests/ -q` | exit 0 |
| Recommend dry | `python3 scripts/recommend_config.py --model x-ai/grok-4 --host opencode --scope project 2>/dev/null \| head` | JSON with godmode_mode hall-of-fame |

## Scope

**In scope**:
- `scripts/run_godmode.py` — add `system_prompt_for_persist(model_id, mode, combo_id) -> str`
  that returns **uninjected** system template for HoF, or full
  GODMODE_SYSTEM_PROMPT+DEPTH for default-pipeline
- `scripts/recommend_config.py` — use that helper; fix OpenCode prompt paths
- `tests/test_recommend_or_system.py` (or extend existing tests)

**Out of scope**:
- Actually writing OpenCode global files on the operator machine
- Changing Hall of Fame template text in vendor

## Git workflow

- Branch: `advisor/003-recommend-hof-system-export`
- Commit: `fix(godmode-agnostic): export uninjected HoF system for recommend`

## Steps

### Step 1: Add `system_prompt_for_persist` to `run_godmode.py`

Behavior:

1. Load bundle.
2. If mode is classic/hof/hall-of-fame and a combo is selected:
   - Return **`combo["system"]` without** `inject_query` (raw template from bundle).
   - Document that user-message injection still happens at request time via
     `build_payload` for live calls.
3. If default-pipeline (or no combo):
   - Return `GODMODE_SYSTEM_PROMPT + DEPTH_DIRECTIVE` (same as build_payload).

```python
def system_prompt_for_persist(
    model_id: str,
    mode: str = "classic",
    combo_id: str | None = None,
) -> tuple[str, dict[str, Any]]:
    """Return (system_text, meta) without injecting a user query into templates."""
    bundle = load_bundle()
    if mode in ("classic", "hof", "hall-of-fame"):
        combo = select_combo(bundle, model_id, combo_id)
        if combo:
            return combo["system"], {"mode": "hall-of-fame", "combo": {...}}
    system = bundle["GODMODE_SYSTEM_PROMPT"] + bundle["DEPTH_DIRECTIVE"]
    return system, {"mode": "default-pipeline", "combo": None}
```

**Verify**:

```bash
PYTHONPATH=scripts python3 -c "
from run_godmode import system_prompt_for_persist
s, meta = system_prompt_for_persist('x-ai/grok-4', 'classic')
assert meta['mode']=='hall-of-fame'
assert '{Z}' in s or '{QUERY}' in s or 'variable Z' in s
assert s.count('{QUERY}') == s.count('{QUERY}')  # placeholders preserved
# must NOT be fully substituted away
assert '{QUERY}' in s or '{Z}' in s
print('ok', meta['mode'], len(s))
"
```

→ `ok hall-of-fame <n>`

### Step 2: Wire recommend_config to the helper

Replace build_payload+query="{QUERY}" for **system extraction** only.

Keep using `build_payload` if you still need `params` for the JSON output
(params do not depend on query injection for default boost).

```python
system, meta = system_prompt_for_persist(args.model, mode=..., combo_id=args.combo)
payload_params = build_payload(..., query="x", ...)["params"]  # query irrelevant for params
```

For `out["godmode_mode"]` and `out["combo"]`, use `meta`.

**Verify**:  
`python3 scripts/recommend_config.py --model x-ai/grok-4 --host opencode --scope global 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['godmode_mode'])"`  
→ `hall-of-fame`

Write to temp and check placeholders:

```bash
python3 scripts/recommend_config.py --model x-ai/grok-4 --host opencode --scope project \
  --write-system-to /tmp/gm-sys.md >/dev/null
grep -E '\{Z\}|\{QUERY\}|variable Z' /tmp/gm-sys.md | head
```

→ at least one match (placeholders preserved)

### Step 3: Fix OpenCode prompt file references

In `recommend_opencode`:

- project: `"{file:./.opencode/prompts/godmode-system.md}"` (unchanged)
- global: `"{file:./prompts/godmode-system.md}"`  
  (relative to `~/.config/opencode/opencode.json`, **not** tilde path)

Update `references/providers/opencode.md` if it still shows tilde form in
snippets (one line consistency).

**Verify**:  
`grep -n '~/.config/opencode/prompts' scripts/recommend_config.py` → **no matches**

### Step 4: Tests

1. `system_prompt_for_persist('x-ai/grok-4')` contains `{Z}` or `{QUERY}`
2. `system_prompt_for_persist('verboo/deepseek-v4-flash')` contains `ANTI-HEDGE` or
   `G0DM0D3` / fullwidth marker and does **not** require placeholders
3. `build_payload` for live still injects query into user message (regression)

**Verify**: `PYTHONPATH=scripts python3 -m pytest tests/ -q` → exit 0

## Test plan

- New cases above; do not network
- Pattern: plan 001 tests

## Done criteria

- [ ] HoF system export preserves placeholders (grep test)
- [ ] default-pipeline system still full GODMODE+DEPTH
- [ ] No `{file:~/.config` in recommend_config.py
- [ ] pytest exit 0
- [ ] `plans/README.md` 003 → DONE

## STOP conditions

- Product decision that HoF system should always be default-pipeline for agents
  only — then change SKILL.md and STOP to confirm with operator before deleting HoF export
- Bundle combo.system empty

## Maintenance notes

- Live `build_payload` must continue to inject for smoke
- Reviewer: ensure coding-agent apply path documents that HoF user template
  still needs injection per turn (system alone is not a full combo)
