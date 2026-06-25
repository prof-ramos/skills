---
description: Run the autoreview closeout reviewer on a change bundle (local | branch | commit).
agent: autoreview
---

Run the autoreview closeout review now.

Target mode: $ARGUMENTS
- If empty, use `auto` (dirty local changes first; else current PR base via `gh pr view`; else `origin/main`).
- Accepts: `local` (or `uncommitted`), `branch`, `commit`, or `auto`.
- For `branch`, also accept a base ref as the second token, e.g. `branch origin/main`.
- For `commit`, also accept a commit ref as the second token, e.g. `commit HEAD`.

Steps:

1. Generate and read the change bundle:
   `bash .opencode/skills/autoreview/scripts/diff-bundle.sh --mode <mode> [--base <ref>] [--commit <ref>]`
2. Apply the rubric (`.opencode/skills/autoreview/references/rubric.md`) and emit
   exactly one JSON object matching `.opencode/skills/autoreview/references/schema.json`.
3. Verify every finding against real code and adjacent files before reporting it.
4. After the JSON, print a short human summary: command/mode used, findings
   accepted/rejected with one-line reasons, and the clean/incorrect verdict.

Safety: read-only. Never edit, write, commit, push, or run destructive commands.
If a secret/credential appears in the bundle, flag it as a `security` finding and
never reproduce the secret value in the output.