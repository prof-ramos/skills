---
name: skill-cleaner
description: >-
  Audit and trim AI agent skill prompt budget across OpenCode, Codex, and Claude
  Code. Use when trimming skill prompt budget, finding duplicate skills across
  roots, auditing enabled/disabled skill roots, inspecting token pressure from
  the pre-budget skill list, or deciding which skills, plugins, or personal
  repos to remove. Detects oversized descriptions nearing truncation, body-hash
  duplicates, unused skills with no recent usage trace, and budget exhaustion
  before descriptions are truncated or skills omitted.
license: MIT
compatibility: >-
  Requires Node.js 20+ with --experimental-strip-types. Works on macOS and
  Linux. Reads session logs from OpenCode, Codex, and Claude Code
  automatically.
metadata:
  author: prof-ramos
  version: "1.0.0"
  topic: agent-workflows
---

# Skill Cleaner

Audit and trim your AI agent's skill prompt budget. The analyzer mirrors the
same rendering rules agents use: 2% budget from context window, `ceil(utf8 / 4)`
token cost, then proportional description truncation or skill omission.

## Quick start

```bash
node --experimental-strip-types scripts/skill-cleaner.ts --months 3
```

Scans all skill roots (`~/.codex/skills`, `~/.config/opencode/skills`,
`~/.claude/skills`, project `.agents/skills/`, and plugins) for the last 3
months, then prints:

- **Skill Budget** — context window, 2% budget, token costs, pre-budget
  full-list pressure, remaining budget
- **Description candidates** — long descriptions where trimming saves budget
- **Duplicates** — same name or near-identical body across roots
- **Unused candidates** — no `$skill` mention or SKILL.md read in recent logs
- **Root summary** — origin and enabled/disabled status per root

## Workflows

### 1. Full audit with deep log scanning

```bash
node --experimental-strip-types scripts/skill-cleaner.ts --months 6 --max-log-mb 800 --deep-logs
```

Scans archived Codex sessions, OpenClaw, Clawd, and Claude Code task JSONs.
Use quarterly or when budget pressure is high.

### 2. Quick budget-only check

```bash
node --experimental-strip-types scripts/skill-cleaner.ts --no-logs
```

Skips session log scanning — only analyzes SKILL.md files, descriptions, and
config. Use for a fast budget check without heavy I/O.

### 3. Audit a custom skill root

```bash
node --experimental-strip-types scripts/skill-cleaner.ts --root ~/Dropbox/boxd/skills --no-logs
```

Scans additional skill directories beyond the standard roots.

### 4. Budget-constrained audit

```bash
node --experimental-strip-types scripts/skill-cleaner.ts --context-tokens 272000 --budget-percent 2 --no-logs
```

Override context window (default: GPT-5.5 at 272K) and budget percentage
(default: 2%).

## Reading the report

Read sections **in this order**:

| Section | What to look for |
|---------|-----------------|
| **Skill Budget** | High pre-budget pressure → descriptions will be truncated or skills omitted |
| **Description candidates** | Skills with long descriptions where trimming saves meaningful budget |
| **Duplicates** | Same name or near-identical content across roots. Delete local copies when built-ins cover it. **Keep** local skills that encode project policy or live operations |
| **Unused candidates** | No `$skill`, `Use $skill`, or SKILL.md read trace in recent logs |
| **Root summary** | Where skills loaded from; which roots are disabled in config |

## Before deleting or editing

- **Verify** the kept copy loads correctly before deleting the duplicate.
- **Prefer deleting** repo-local or agent-scripts duplicates when agent built-ins
  cover them.
- **Keep** repo-local maintainer skills that encode project policy, domain
  language, or live operations.
- **Preserve trigger nouns** in descriptions: product, tool, action, object —
  removing these breaks auto-triggering.

## Analyzer behavior

The script mirrors the agent's model-visible line shape (`- name: description
(file: path)`) and applies the same rendering rules from `render.rs`:

- YAML frontmatter only; default name = parent directory
- Budget: 2% of `context_window`; token cost = `ceil(utf8_bytes / 4)`
- Description rendering: full descriptions → equal truncation → omitted to
  minimum lines
- Reads `~/.codex/models_cache.json` for context_window (fallback: 272K)
- Scans default roots plus `--root` extras
- Dedupes by realpath — symlinked roots don't create false duplicates
- For duplicate names: reports description/body similarity; suggests deletion
  only when bodies are near copies
- Log scanning: `~/.codex/history.jsonl`, `~/.codex/sessions/`,
  `~/.config/opencode/sessions/`, `~/.claude/projects/` by default

## All flags

```
--months <n>         Look back N months for usage (default: 3)
--no-logs            Skip log scanning (budget-only check)
--deep-logs          Scan archived sessions, OpenClaw, Clawd logs
--max-log-mb <n>     Max log bytes to scan (default: 300)
--model <name>       Model name for context window (default: gpt-5.5)
--budget-percent <n> Skills budget percent (default: 2)
--context-tokens <n> Override context window size
--chars-per-token <n> UTF-8 bytes per token (default: 4)
--all                Include disabled skills
--root <path>        Add extra skill root (repeatable)
--json               Output JSON instead of report
--help               This help
```

## Output policy

- **Suggest first** — print findings and recommendations. Do NOT delete or edit
  without confirmation.
- **When asked to apply**: make small grouped commits per action (descriptions,
  deletes, config disables).
- **Do not delete** ignored/untracked skill directories without naming the
  destination and confirming they are disposable.
