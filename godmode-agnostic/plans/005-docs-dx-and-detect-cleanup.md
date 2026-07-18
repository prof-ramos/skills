# Plan 005: README, license notice, detect cleanup, remove empty assets

> **Executor instructions**: Follow step by step. Verify each gate. Update
> `plans/README.md` when done.
>
> **Drift check**:
> `git diff --stat 3abca90..HEAD -- scripts/detect_session_model.py SKILL.md .gitignore`

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (can run parallel to 002–004; after 001 if you link
  README test command to pytest)
- **Category**: docs / dx / bugs
- **Planned at**: commit `3abca90`, 2026-07-18

## Why this matters

The skill package has no root README (onboarding is only SKILL.md for agents),
no package-level AGPL redistribution notice (vendor has LICENSE, root does not),
a dead `or True` in detect that always lists project `AGENTS.md`, and an empty
`assets/` directory left from a rejected “invented packs” design. These hurt
humans and agents executing the skill.

## Current state

- No root `README.md`
- No root `LICENSE` (vendor: `vendor/g0dm0d3/LICENSE` AGPL-3.0)
- `scripts/detect_session_model.py:164-165`:

```python
if (cwd / "AGENTS.md").exists() or True:
    targets.append(str(cwd / "AGENTS.md"))
```

- Empty `assets/` directory (may only appear as empty folder)
- `.gitignore` already ignores `.godmode-agnostic/` and `__pycache__`

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Detect dry | `python3 scripts/detect_session_model.py --pretty` | JSON SessionProfile |
| Tests | `PYTHONPATH=scripts python3 -m pytest tests/ -q` | exit 0 (if 001 landed) |
| List assets | `find assets -type f 2>/dev/null \| wc -l` | 0 before cleanup |

## Scope

**In scope**:
- `README.md` (create) — human install/use for the skill
- `LICENSE` (create) — either MIT/Apache for **skill code only** **plus**
  clear pointer that `vendor/g0dm0d3` is AGPL-3.0, **or** single AGPL-3.0 for
  the whole package if operator prefers one license.  
  **Default recommendation**: root `LICENSE` = MIT (or same as monorepo) for
  `scripts/` + `SKILL.md`, and `NOTICE` file stating vendor G0DM0D3 is AGPL-3.0
  under `vendor/g0dm0d3/`. If monorepo has a standard, match it.
- `NOTICE` at root (optional short) duplicating vendor attribution pointer
- `scripts/detect_session_model.py` — remove `or True`; only append AGENTS.md
  when file exists **or** when recommending create-able paths, document both
  as `existing` vs `suggested`
- Remove empty `assets/` if empty (or add `.gitkeep` only if needed — prefer
  **delete** empty tree)
- `SKILL.md` — one-line link to README for humans
- `tests/test_detect_session_model.py` — case: no AGENTS.md in temp cwd →
  path not forced as existing requirement

**Out of scope**:
- Changing GODMODE prompts
- Publishing to a skill marketplace
- Monorepo root README outside this skill folder

## Git workflow

- Branch: `advisor/005-docs-dx-detect`
- Commit: `docs(godmode-agnostic): README, license notice, fix detect targets`

## Steps

### Step 1: Fix detect targets

Replace:

```python
if (cwd / "AGENTS.md").exists() or True:
    targets.append(str(cwd / "AGENTS.md"))
```

With:

```python
# Suggested writable surfaces (may not exist yet)
suggested = [
    cwd / "AGENTS.md",
    cwd / ".opencode" / "agents" / "godmode.md",
    home / ".config" / "opencode" / "AGENTS.md",
    home / ".config" / "opencode" / "agents" / "godmode.md",
]
profile["config_targets"] = [str(p) for p in suggested]
profile["config_targets_existing"] = [str(p) for p in suggested if p.exists()]
```

Keep JSON backward compatible: `config_targets` remains the list recommend/apply
may write; add `config_targets_existing` for clarity.

**Verify**:

```bash
python3 scripts/detect_session_model.py --pretty | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'or True' not in open('scripts/detect_session_model.py').read(); print('targets', len(d.get('config_targets',[])))"
```

→ no `or True` in file; prints targets count ≥ 1

### Step 2: Remove empty assets/

```bash
rmdir assets 2>/dev/null || rm -rf assets
```

Only if no files remain. If something was added, STOP.

**Verify**: `test ! -d assets` → success

### Step 3: Write README.md

Minimum sections:

1. What this skill does (4 steps: detect → run G0DM0D3 GODMODE → smoke/persist → recommend)
2. Requirements: Python 3.10+
3. Quick start commands (copy from SKILL.md pipeline)
4. Verification: `PYTHONPATH=scripts python3 -m pytest tests/ -q`
5. Vendor / AGPL: see `vendor/g0dm0d3/LICENSE` and NOTICE
6. Security: never commit API keys; use env / OpenCode auth.json
7. Link to upstream G0DM0D3

**Verify**: `test -f README.md && wc -l README.md` → ≥ 40 lines

### Step 4: License / NOTICE

- Create root `LICENSE` matching monorepo default if known; else MIT for skill
  code with SPDX identifier in header comment optional
- Create root `NOTICE` or section in README:

```text
This package vendors G0DM0D3 materials under AGPL-3.0 in vendor/g0dm0d3/.
See vendor/g0dm0d3/LICENSE and vendor/g0dm0d3/NOTICE.
```

**Verify**: `test -f LICENSE && test -f vendor/g0dm0d3/LICENSE`

### Step 5: SKILL.md cross-link

Add near top after title:

```markdown
Human-oriented setup: see [README.md](./README.md).
```

**Verify**: `grep -n 'README.md' SKILL.md` → hit

### Step 6: Tests for detect

If plan 001 present, add:

```python
def test_config_targets_no_force_missing_agents(tmp_path, monkeypatch):
    # call detect(tmp_path, tmp_path) without AGENTS.md
    # assert tmp_path/'AGENTS.md' may appear in config_targets as suggestion
    # assert config_targets_existing does not require it
```

**Verify**: pytest exit 0

## Test plan

- Detect unit test above
- No network

## Done criteria

- [ ] No `or True` in `detect_session_model.py`
- [ ] `assets/` gone or documented if retained with real content
- [ ] README.md exists with quick start + AGPL pointer
- [ ] Root LICENSE + NOTICE (or LICENSE + README section)
- [ ] SKILL.md links README
- [ ] pytest still green if suite exists
- [ ] `plans/README.md` 005 → DONE

## STOP conditions

- Monorepo forbids nested LICENSE files — then only README attribution
- `assets/` contains user files not seen in audit — do not delete; report

## Maintenance notes

- Keep README command snippets in sync with SKILL.md
- Reviewer: AGPL obligations for network service use of modified vendor code
