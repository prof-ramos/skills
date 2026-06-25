---
name: run-edital-verticalizado
description: Run, test, and drive the edital-verticalizado tool. Processes Brazilian public exam announcements (editais) into structured study tables. Use to verticalizar an edital, generate CSV/JSON output, or verify the driver works.
---

# run-edital-verticalizado

Drives `driver.sh` — a shell script that calls `claude -p --system-prompt` with the verticalização prompt and a user-supplied edital file. No server, no GUI. Input is a text file; output is a structured Markdown/CSV/JSON table printed to stdout.

All paths below are relative to `edital-verticalizado/`.

---

## Prerequisites

```bash
# Already available on this machine (verified 2026-06-25):
which claude   # /opt/homebrew/bin/claude (Claude Code 2.1.178)
which uv       # /opt/homebrew/bin/uv (uv 0.11.23)
```

No extra `apt-get` or `npm install` needed. The driver uses only `claude` and standard POSIX shell.

---

## Run (agent path)

The driver accepts: `driver.sh <edital_file> [format: md|csv|json] [cargo_filter]`

```bash
# Markdown (default) — use the bundled example
.claude/skills/run-edital-verticalizado/driver.sh examples/edital_exemplo.md

# CSV output
.claude/skills/run-edital-verticalizado/driver.sh examples/edital_exemplo.md csv

# JSON output
.claude/skills/run-edital-verticalizado/driver.sh examples/edital_exemplo.md json

# Filter by cargo
.claude/skills/run-edital-verticalizado/driver.sh examples/edital_exemplo.md md "Analista Judiciário"
```

Progress is printed to stderr; the table goes to stdout. Redirect stdout to save:

```bash
.claude/skills/run-edital-verticalizado/driver.sh examples/edital_exemplo.md > output.md
```

Typical runtime: 30–90 seconds depending on edital size.

---

## Smoke test (verified 2026-06-25)

```bash
cd /Users/gabrielramos/skills/edital-verticalizado
.claude/skills/run-edital-verticalizado/driver.sh examples/edital_exemplo.md md 2>&1 | tail -20
```

Expected tail output (confirmed):
```
| DT-033 | Analista Judiciário — Área Judiciária | ... | greve | ...
---
| Total de linhas | 103 |
| Conhecimentos Básicos | 41 (LP: 10 · RL: 12 · DC: 15 · LG: 4) |
| Conhecimentos Específicos | 62 (PT: 29 · DT: 33) |
| Ambiguidades sinalizadas | 3 |
```

---

## Using a real edital

Paste an edital or point at a local file:

```bash
# From a PDF (requires pdftotext)
pdftotext edital.pdf - | tee edital.txt
.claude/skills/run-edital-verticalizado/driver.sh edital.txt

# From a local file
.claude/skills/run-edital-verticalizado/driver.sh /path/to/edital.md csv
```

---

## Gotchas

- **Output captured mid-table in background mode**: when run via `run_in_background`, the first streaming tokens from `claude -p` may appear truncated in the captured file. Run synchronously (without `run_in_background`) for full output, or redirect stdout to a file inside the driver call.
- **No ANTHROPIC_API_KEY needed**: the driver uses `claude` (Claude Code CLI), which authenticates via the user's Claude Code session — not a raw API key.
- **Large editais (50+ pages)**: split by cargo or bloco before passing; `claude -p` has a context limit and will silently truncate very large prompts.
- **PDF input**: `pdftotext` (from `poppler-utils`) is required for PDF extraction. The driver itself does not call `pdftotext` — convert first, then pass the `.txt` file.
- **System prompt length**: the system prompt is embedded in the driver script. If claude changes its flag syntax, update the `claude -p --system-prompt` call in `driver.sh`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Erro: arquivo não encontrado` | Check path; run from `edital-verticalizado/` root or use absolute path |
| Output is JSON preamble instead of table | Remove `--output-format` if you manually added it; driver sets format via prompt |
| Driver hangs after printing `---` | `claude -p` is processing — wait up to 2 minutes for a large edital |
| Empty output | Check that `claude` CLI is authenticated (`claude --version` works) |
