# Plan 001: Establish pytest verification baseline for pure GODMODE helpers

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer maintains the index.
>
> **Drift check (run first)**:
> `git diff --stat 3abca90..HEAD -- scripts/run_godmode.py scripts/detect_session_model.py vendor/g0dm0d3/godmode_bundle.json`
> If those files changed since this plan was written, compare "Current state"
> excerpts against live code before proceeding; on mismatch, STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tests
- **Planned at**: commit `3abca90`, 2026-07-18

## Why this matters

This skill’s claim is that payloads come from **upstream G0DM0D3 constants**,
not invented prompts. There is **no automated test command** today: only
`evals/evals.json` (manual skill-creator prompts). Without a baseline, later
fixes (model-id strip, recommend, export_bundle) can silently change inject
behavior or Hall of Fame selection. This plan adds a one-command offline test
suite for pure functions that need no API keys.

## Current state

- `scripts/run_godmode.py` — builds payloads from `vendor/g0dm0d3/godmode_bundle.json`
  - `inject_query` (≈39–54): multi-placeholder replace matching libertas.ts
  - `apply_godmode_boost` (≈57–69): temperature/presence/frequency deltas
  - `select_combo` / `build_payload` (≈72–155): HoF vs default-pipeline
- `scripts/detect_session_model.py` — `classify_family`, `combo_for_family`
- `vendor/g0dm0d3/godmode_bundle.json` — machine dump of GODMODE_SYSTEM_PROMPT,
  DEPTH_DIRECTIVE, HALL_OF_FAME, applyGodmodeBoost config
- **No** `tests/` directory, **no** `pyproject.toml` / `requirements*.txt`,
  **no** root test script
- Conventions: stdlib-only Python 3, argparse CLIs, JSON stdout; match that
  style (no heavy frameworks)

Excerpt — inject_query:

```python
# scripts/run_godmode.py ~39-54
def inject_query(text: str, query: str) -> str:
    return (
        text.replace("{QUERY}", query)
        .replace("{Z}", query)
        # ... more placeholders ...
    )
```

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Run tests | `python3 -m pytest -q` (from skill root) | exit 0, all pass |
| Run without install | `python3 -m pytest tests/ -q` | same if pytest available |
| Offline smoke (existing) | `python3 scripts/run_godmode.py --model verboo/deepseek-v4-flash --query x 2>/dev/null \| python3 -c "import sys,json; json.load(sys.stdin)"` | exit 0 |

If `pytest` is missing: `python3 -m pip install pytest` **only if the operator
allows installs**; otherwise document `pytest` as a dev dependency in README
(plan 005) and use `python3 -m unittest` with the same cases.

**Prefer**: add `tests/test_run_godmode.py` runnable via:

```bash
cd /path/to/godmode-agnostic
PYTHONPATH=scripts python3 -m pytest tests/ -q
```

## Scope

**In scope**:
- `tests/test_run_godmode.py` (create)
- `tests/test_detect_session_model.py` (create)
- `tests/conftest.py` (optional; only if needed for path setup)
- `pyproject.toml` **or** `requirements-dev.txt` listing `pytest` (minimal)
- Update `SKILL.md` Scripts index or Vendor section with one line:
  `python3 -m pytest tests/ -q` as verification (one short addition only)

**Out of scope**:
- Live HTTP tests against Verboo/OpenRouter
- Changing prompt text in `godmode_bundle.json` or vendored TS
- `scripts/smoke_and_persist.py` behavior (plan 002)
- `recommend_config.py` (plan 003)

## Git workflow

- Branch: `advisor/001-verification-baseline` (or implement on current skill
  branch if the monorepo treats this folder as untracked WIP)
- Commit style (from monorepo log): conventional commits, e.g.
  `test(godmode-agnostic): add pytest baseline for inject and HoF select`
- Do NOT push/PR unless the operator asks

## Steps

### Step 1: Add pytest path setup

Create `tests/` at skill root. Ensure imports work:

```python
# tests/test_run_godmode.py
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_godmode import inject_query, apply_godmode_boost, build_payload, select_combo, load_bundle
```

**Verify**: `python3 -c "import sys; sys.path.insert(0,'scripts'); from run_godmode import inject_query; print(inject_query('{QUERY}','hi'))"` → prints `hi`

### Step 2: Write tests for inject_query

Cases (all must pass):

1. `{QUERY}` replaced
2. `{Z}` replaced
3. Multiple placeholders in one string
4. Unknown text unchanged
5. Empty query replaces with empty string

**Verify**: run the inject tests only after step 3–4 if using one file; else
`pytest tests/test_run_godmode.py -k inject -q` → pass

### Step 3: Write tests for apply_godmode_boost

Load boost config from `load_bundle()["applyGodmodeBoost"]`.

Cases:

1. `temperature=None` → default 0.7 + 0.1 = **0.8** (use rounded compare:
   `abs(x-0.8) < 1e-9` or prefer plan 002 float fix first — if float is still
   binary, assert `pytest.approx(0.8)`)
2. Caps at 2.0 when starting near 2.0
3. presence_penalty / frequency_penalty deltas applied

**Verify**: `pytest tests/test_run_godmode.py -k boost -q` → pass

### Step 4: Write tests for select_combo / build_payload mode routing

Cases:

1. `anthropic/claude-sonnet-4` + mode classic → `mode == "hall-of-fame"`,
   combo id `claude-inversion`
2. `verboo/deepseek-v4-flash` + mode classic → `mode == "default-pipeline"`,
   combo is None
3. Forced `--combo hermes-fast` with unrelated model still returns hermes-fast
   when combo_id set
4. default-pipeline system content starts with a known prefix from bundle
   (`GODMODE_SYSTEM_PROMPT` first 40 chars) and contains a known DEPTH phrase
   (`ANTI-HEDGE` or `RESPONSE REQUIREMENTS`)
5. Hall of Fame system for claude does **not** need to equal entire bundle;
   assert `"godmode is active"` in system (upstream claude-inversion marker)

**Verify**: `pytest tests/test_run_godmode.py -q` → all pass

### Step 5: Write tests for classify_family / combo_for_family

Import from `detect_session_model.py` the same way.

Cases:

1. `verboo/deepseek-v4-flash` → family `deepseek`, hof_combo None
2. `anthropic/claude-sonnet-4` → family `claude`, combo `claude-inversion`
3. `x-ai/grok-4` → `grok` / `grok-420`

**Verify**: `python3 -m pytest tests/ -q` → exit 0

### Step 6: Document the command

Add to `SKILL.md` under Scripts index (or new ## Verification):

```markdown
## Verification

```bash
PYTHONPATH=scripts python3 -m pytest tests/ -q
```
```

**Verify**: `grep -n pytest SKILL.md` → at least one hit

## Test plan

- New files as above; cases listed in steps 2–5
- No existing test pattern — this plan **creates** the pattern
- Full command: `PYTHONPATH=scripts python3 -m pytest tests/ -q` → all pass

## Done criteria

- [ ] `PYTHONPATH=scripts python3 -m pytest tests/ -q` exits 0
- [ ] At least 10 distinct test functions/cases covering inject, boost, payload
      mode, and family classification
- [ ] No live network calls in tests
- [ ] No files outside in-scope list modified
- [ ] `plans/README.md` row for 001 → DONE

## STOP conditions

- `godmode_bundle.json` missing or missing `HALL_OF_FAME` / `GODMODE_SYSTEM_PROMPT`
- pytest cannot be installed and unittest port would require redesign beyond
  this plan — report and ask operator
- Drift: `inject_query` / `build_payload` signatures changed incompatibly

## Maintenance notes

- Any change to libertas placeholders must update inject tests
- Plan 004 will add a drift hash test; keep these behavioral tests
- Reviewer: ensure tests assert **upstream markers**, not paraphrased prompts
