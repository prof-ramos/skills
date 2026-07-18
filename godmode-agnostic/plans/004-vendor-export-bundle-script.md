# Plan 004: Checked-in export_bundle script and drift guard

> **Executor instructions**: Follow step by step. Verify each gate. Update
> `plans/README.md` when done.
>
> **Drift check**:
> `git diff --stat 3abca90..HEAD -- vendor/g0dm0d3/ scripts/`

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: MED (touches vendor fidelity; do not hand-edit prompts)
- **Depends on**: plans/001-verification-baseline.md
- **Category**: tech-debt
- **Planned at**: commit `3abca90`, 2026-07-18

## Why this matters

The skill promises **100% upstream** GODMODE constants. Today
`godmode_bundle.json` was produced by an ad-hoc session script that is **not**
in the repo. Updating `vendor/g0dm0d3/src/lib/*.ts` without regenerating the
JSON will desync runtime (Python) from the vendored TypeScript sources.
A checked-in exporter + test that fails on drift makes the promise enforceable.

## Current state

- `vendor/g0dm0d3/src/lib/godmode-prompt.ts` — `GODMODE_SYSTEM_PROMPT`
- `vendor/g0dm0d3/src/lib/libertas.ts` — `HALL_OF_FAME`, inject helpers
- `vendor/g0dm0d3/src/lib/godmode-pipeline.ts` — DEPTH + applyGodmodeBoost extract
- `vendor/g0dm0d3/godmode_bundle.json` — runtime source for `run_godmode.py`
- `vendor/g0dm0d3/NOTICE` — documents extraction; **no script path**
- No `scripts/export_bundle.py`

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Export | `python3 scripts/export_bundle.py` | rewrites `godmode_bundle.json`; exit 0 |
| Export dry | `python3 scripts/export_bundle.py --check` | exit 0 if JSON matches TS; exit 1 if drift |
| Tests | `PYTHONPATH=scripts python3 -m pytest tests/ -q` | exit 0 |

## Scope

**In scope**:
- `scripts/export_bundle.py` (create) — deterministic parse of the three TS files
  into the same JSON schema as current `godmode_bundle.json`
- `tests/test_export_bundle.py` — run exporter in check mode or re-export to
  temp and diff
- `vendor/g0dm0d3/NOTICE` — add “Run: `python3 scripts/export_bundle.py`”
- `SKILL.md` Vendor integrity section — point to the script (replace vague text)

**Out of scope**:
- Re-cloning full G0DM0D3 repo
- Changing prompt wording
- Packaging as npm/tsx pipeline (stdlib Python only, match repo)

## Git workflow

- Branch: `advisor/004-export-bundle`
- Commit: `chore(godmode-agnostic): add export_bundle.py and drift check`

## Steps

### Step 1: Implement TS template const parser

Port the proven parsing approach used when the bundle was first created:

- Find `export const NAME = \``
- Scan until unescaped closing backtick
- Handle `\uXXXX`, `\``, `\\`

Parse:

- `GODMODE_SYSTEM_PROMPT` from godmode-prompt.ts
- `DEPTH_DIRECTIVE` from godmode-pipeline.ts
- Each object in `HALL_OF_FAME` array from libertas.ts (id, model, codename,
  description, color, system, user, fast)

Hardcode applyGodmodeBoost numbers from godmode-pipeline.ts function body
(deltas 0.1 / 0.15 / 0.1, caps 2.0, default temperature 0.7) — must match
function if present; if the TS function changes, parse deltas from source or
STOP.

### Step 2: Write JSON with stable key order

Keys (match existing bundle top-level):

```json
{
  "source": "https://github.com/elder-plinius/G0DM0D3",
  "commit_note": "...",
  "license": "AGPL-3.0",
  "upstream_files": [...],
  "GODMODE_SYSTEM_PROMPT": "...",
  "DEPTH_DIRECTIVE": "...",
  "HALL_OF_FAME": [ ... ],
  "applyGodmodeBoost": { ... },
  "pipeline_default_flags": { ... }
}
```

Write with `json.dumps(..., ensure_ascii=False, indent=2) + "\n"`.

CLI:

```text
python3 scripts/export_bundle.py           # write vendor/.../godmode_bundle.json
python3 scripts/export_bundle.py --check   # compare to existing; exit 1 on diff
python3 scripts/export_bundle.py --out PATH
```

**Verify**:

```bash
python3 scripts/export_bundle.py --check
```

→ exit 0 (bundle already matches) **or** if first run drifts, run without
`--check`, then `--check` must pass.

### Step 3: Do not “improve” prompts

If `--check` fails only due to whitespace normalization, fix the exporter to
match current committed JSON **or** regenerate once and commit the JSON as the
new golden — but show the diff to the operator if the system prompt text
changes by more than whitespace.

**STOP** if export changes more than 5% of GODMODE_SYSTEM_PROMPT length without
a TS file change.

### Step 4: Test

```python
def test_export_check_clean():
    # subprocess: python3 scripts/export_bundle.py --check
    assert returncode == 0

def test_hall_of_fame_count():
    b = load_bundle()
    assert len(b["HALL_OF_FAME"]) == 5
    ids = {c["id"] for c in b["HALL_OF_FAME"]}
    assert ids == {"grok-420", "gemini-reset", "gpt-classic", "claude-inversion", "hermes-fast"}
```

**Verify**: `PYTHONPATH=scripts python3 -m pytest tests/test_export_bundle.py -q`

### Step 5: Docs

Update `vendor/g0dm0d3/NOTICE` and `SKILL.md` Vendor integrity:

```markdown
3. Rebuild bundle: `python3 scripts/export_bundle.py`
4. Confirm: `python3 scripts/export_bundle.py --check`
```

## Test plan

- `--check` in CI/local pytest via subprocess
- Golden combo ids test

## Done criteria

- [ ] `scripts/export_bundle.py` exists and is deterministic (two runs → same hash)
- [ ] `python3 scripts/export_bundle.py --check` exit 0 on clean tree
- [ ] pytest includes export check
- [ ] NOTICE + SKILL.md mention the script
- [ ] No hand-edited prompt text without corresponding TS change
- [ ] `plans/README.md` 004 → DONE

## STOP conditions

- Cannot parse libertas.ts after upstream format change — stop and report AST
  approach needed
- Bundle and TS conflict on semantics (not just whitespace) — report diff size

## Maintenance notes

- When refreshing G0DM0D3: copy TS files → `export_bundle.py` → commit both
- Reviewer: ensure AGPL NOTICE still accurate
