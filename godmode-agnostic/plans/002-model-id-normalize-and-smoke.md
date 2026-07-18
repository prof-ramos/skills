# Plan 002: Normalize API model IDs and harden live smoke evaluation

> **Executor instructions**: Follow step by step. Verify each step. STOP on
> conditions below. Update `plans/README.md` when done.
>
> **Drift check**:
> `git diff --stat 3abca90..HEAD -- scripts/run_godmode.py scripts/smoke_and_persist.py`
> Compare excerpts if changed.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: plans/001-verification-baseline.md (add tests there first; extend them here)
- **Category**: bug
- **Planned at**: commit `3abca90`, 2026-07-18

## Why this matters

OpenCode model ids are `provider/model` (e.g. `verboo/deepseek-v4-flash`).
Verboo’s OpenAI-compatible API expects the bare id (`deepseek-v4-flash`).
Live smoke currently sends the full id unless the operator sets
`GODMODE_TEST_MODEL`, so “test that GODMODE works” fails for the common case.

Separately, `evaluate_text` treats any non-refusal string longer than 20 chars
as pass, and only reads `message.content`. Models that put text in
`reasoning_content` (empty content) fail or are mis-scored.

Also fix temperature float noise (`0.7+0.1` → `0.7999…`) in the same params path.

## Current state

- `scripts/smoke_and_persist.py:146` —  
  `test_model = os.environ.get("GODMODE_TEST_MODEL") or model`
- `scripts/smoke_and_persist.py:155-156` —  
  `content = raw["choices"][0]["message"]["content"]` then `evaluate_text(content)`
- `scripts/smoke_and_persist.py:67-76` — weak pass rule  
  `okish = OK_MARKERS or (len(text) > 20 and not refused)`
- `scripts/run_godmode.py:67` —  
  `out["temperature"] = min(float(temp) + float(boost["temperature_delta"]), cap)`  
  no rounding
- `scripts/run_godmode.py:126,145` — `"request_model": model_id` (unsanitized)

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Unit tests | `PYTHONPATH=scripts python3 -m pytest tests/ -q` | exit 0 |
| Offline smoke | `python3 scripts/smoke_and_persist.py --model verboo/deepseek-v4-flash --skip-live` | exit 0; state written |
| Live smoke (optional) | env `GODMODE_TEST_BASE_URL` + `GODMODE_TEST_API_KEY` set; no `GODMODE_TEST_MODEL` required | exit 0; `passed: true` when API healthy |

## Scope

**In scope**:
- `scripts/run_godmode.py` — add `api_model_id(model_id: str) -> str`; use it for
  `request_model` in payload; round boost floats
- `scripts/smoke_and_persist.py` — use `api_model_id`; improve content extraction
  and evaluation; optional max_tokens for smoke body
- `tests/test_run_godmode.py` and/or `tests/test_smoke_helpers.py` — new cases

**Out of scope**:
- Changing vendor prompts
- Auto-discovering base URL from OpenCode auth
- Recommend_config (plan 003)

## Git workflow

- Branch: `advisor/002-model-id-normalize-smoke`
- Commit: `fix(godmode-agnostic): strip provider prefix for API smoke and harden evaluate`

## Steps

### Step 1: Add `api_model_id` helper in `run_godmode.py`

```python
def api_model_id(model_id: str) -> str:
    """Strip OpenCode-style provider/ prefix for OpenAI-compatible APIs.

    verboo/deepseek-v4-flash -> deepseek-v4-flash
    anthropic/claude-sonnet-4 -> claude-sonnet-4
    deepseek-v4-flash -> deepseek-v4-flash
    """
    if not model_id:
        return model_id
    # Only strip a single known-style provider segment (one slash).
    # Do not strip openrouter-style org/model that need both segments
    # UNLESS operator uses GODMODE_TEST_MODEL. Heuristic for this skill:
    # if first segment is a known agent provider id, strip it.
    known = {
        "verboo", "opencode", "openai", "anthropic", "google", "x-ai", "xai",
        "ollama", "ollama-cloud", "openrouter",
    }
    if "/" in model_id:
        head, tail = model_id.split("/", 1)
        if head.lower() in known and tail:
            # openrouter uses org/model — first segment is org not provider.
            # For openrouter, do NOT strip. Detect: head == "openrouter" only
            # as OpenCode provider prefix form openrouter/org/model (two slashes).
            if head.lower() == "openrouter" and "/" in tail:
                return tail  # openrouter/meta/llama -> meta/llama
            if head.lower() == "openrouter":
                return model_id  # ambiguous — leave full id
            return tail
    return model_id
```

Set in both return paths of `build_payload`:

```python
"request_model": api_model_id(model_id),
"session_model": model_id,  # optional: keep original for state
```

Prefer adding `session_model` so smoke state still records OpenCode id.

**Verify**:

```bash
PYTHONPATH=scripts python3 -c "from run_godmode import api_model_id; assert api_model_id('verboo/deepseek-v4-flash')=='deepseek-v4-flash'; assert api_model_id('deepseek-v4-flash')=='deepseek-v4-flash'; print('ok')"
```

→ prints `ok`

### Step 2: Round boost floats

In `apply_godmode_boost`, after computing each float, round to 4 decimal places
(or use `round(x, 4)`):

```python
out["temperature"] = round(min(...), 4)
```

**Verify**: build_payload default-pipeline → `params["temperature"] == 0.8`

### Step 3: Smoke uses `request_model` / api_model_id

In `smoke_and_persist.py`:

```python
from run_godmode import build_payload, api_model_id

test_model = os.environ.get("GODMODE_TEST_MODEL") or payload.get("request_model") or api_model_id(model)
```

Prefer payload’s `request_model` after step 1.

**Verify**: offline dry logic:

```bash
PYTHONPATH=scripts python3 -c "from run_godmode import build_payload; p=build_payload(model_id='verboo/deepseek-v4-flash', query='x', mode='default-pipeline', combo_id=None, temperature=None); assert p['request_model']=='deepseek-v4-flash'"
```

### Step 4: Extract assistant text robustly

```python
def assistant_text(raw: dict) -> str:
    msg = raw["choices"][0]["message"]
    content = msg.get("content") or ""
    if isinstance(content, list):
        # rare multimodal
        content = "".join(
            (p.get("text") or "") for p in content if isinstance(p, dict)
        )
    if content.strip():
        return content
    # reasoning-only models
    for key in ("reasoning_content", "reasoning"):
        if msg.get(key):
            return str(msg[key])
    return ""
```

### Step 5: Tighten evaluate_text for smoke query

When default smoke query is `Reply with exactly: GODMODE_OK`:

- **pass** if `GODMODE_OK` in text (case-sensitive OK as upstream uses that token)
- **fail** if refusal markers and no OK marker
- For generic queries: pass if not refused AND `len(text.strip()) > 0`
  (remove the `len > 20` shortcut as sole pass)

```python
def evaluate_text(text: str, *, expect_token: str | None = "GODMODE_OK") -> dict:
    text = text or ""
    refused = bool(REFUSAL_MARKERS.search(text))
    if expect_token:
        passed = expect_token in text and not refused
    else:
        passed = bool(text.strip()) and not refused
    ...
```

Pass `expect_token` based on whether args.query contains `GODMODE_OK`.

### Step 6: Tests

Add to tests:

1. `api_model_id` cases: verboo strip, bare id, anthropic strip
2. `evaluate_text("GODMODE_OK")` passed True
3. `evaluate_text("")` passed False
4. `evaluate_text("I can't assist with that")` passed False
5. temperature == 0.8 exactly after boost

**Verify**: `PYTHONPATH=scripts python3 -m pytest tests/ -q` → exit 0

### Step 7: Optional live check

If operator has keys (do **not** hardcode secrets):

```bash
export GODMODE_TEST_BASE_URL="https://code.verboo.ai/router/v1"
export GODMODE_TEST_API_KEY  # already in env or auth — operator provides
# deliberately unset GODMODE_TEST_MODEL
unset GODMODE_TEST_MODEL
python3 scripts/smoke_and_persist.py --model verboo/deepseek-v4-flash
```

→ exit 0, JSON `"passed": true` when network works

If no key: skip live; offline tests suffice for DONE.

## Test plan

- Extend plan 001 suite with cases in step 6
- Pattern: same as `tests/test_run_godmode.py`

## Done criteria

- [ ] `api_model_id("verboo/deepseek-v4-flash") == "deepseek-v4-flash"`
- [ ] `build_payload(...).params["temperature"] == 0.8`
- [ ] smoke live path uses stripped model when env override absent (assert via unit
      test of helper, not necessarily live network)
- [ ] empty content fails evaluate when expecting GODMODE_OK
- [ ] `pytest tests/ -q` exit 0
- [ ] `plans/README.md` 002 → DONE

## STOP conditions

- Verboo API changes to require `pro/` prefix on model ids — then extend
  `api_model_id` with optional map; do not guess without operator confirmation
- OpenRouter multi-segment models break if strip heuristic is too aggressive —
  use the `known` provider set only; if unsure STOP

## Maintenance notes

- When adding providers (e.g. new OpenCode custom provider name), add to `known`
- Reviewer: check openrouter double-slash behavior carefully
