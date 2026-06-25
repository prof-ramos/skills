---
description: Run the autoreview closeout reviewer (read-only) on a change bundle — local, branch, or commit.
argument-hint: [local | branch <base> | commit <ref> | auto]
allowed-tools: Task, Read, Grep, Glob, Bash(git diff:*), Bash(git show:*), Bash(git log:*), Bash(git status:*), Bash(git rev-parse:*), Bash(git merge-base:*), Bash(git ls-files:*), Bash(gh pr view:*), Bash(gh pr diff:*), Bash(.claude/skills/autoreview/scripts/diff-bundle.sh:*)
---

Run the **autoreview** closeout structured review now by delegating to the
`autoreview` subagent.

## Parse the target mode from $ARGUMENTS

- Empty → `auto` (dirty local changes first; else current PR base via `gh pr view`;
  else `origin/main`).
- `local` or `uncommitted` → dirty worktree.
- `branch` → diff vs base; if a second token is given, use it as the base ref
  (e.g. `branch origin/main`).
- `commit` → single committed change; if a second token is given, use it as the
  commit ref (e.g. `commit HEAD`).
- `auto` → let the helper auto-resolve.

## Delegate

Call the **Task** tool with subagent_type `autoreview` and a prompt that contains:

1. The resolved target mode (and base/commit ref if provided).
2. Instruction to generate the bundle with
   `bash .claude/skills/autoreview/scripts/diff-bundle.sh --mode <mode> [--base <ref>] [--commit <ref>]`
   and then apply the rubric at
   `.claude/skills/autoreview/references/rubric.md` and schema at
   `.claude/skills/autoreview/references/schema.json`.
3. A reminder that the subagent is read-only and must return exactly one JSON object
   matching the schema, followed by a short human summary.

Return the subagent's JSON and human summary to the user verbatim. Do not edit,
write, commit, or push. Do not apply findings; the review is advisory.

If the subagent reports `patch is correct` with empty `findings`, report
`autoreview clean: no accepted/actionable findings reported` and stop — do not run
a second review for nicer wording.