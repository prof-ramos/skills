# AGENTS.md — autoreview (OpenCode)

> Append-only guidance for projects adopting the `autoreview` skill. Merge into
> your project's own `AGENTS.md` if one already exists.

## autoreview — closeout code review

`autoreview` is a **read-only, advisory** closeout reviewer. It runs as the
`autoreview` subagent (configured in `opencode.json`) and emits a JSON findings
bundle against a fixed schema.

### When to use

- After non-trivial code edits, before commit/ship.
- Reviewing a local branch or PR branch after fixes.
- Second-model / autoreview / closeout check requests.

### How to invoke

```text
/autoreview                    # auto target
/autoreview local               # dirty worktree
/autoreview branch origin/main  # diff vs base
/autoreview commit HEAD         # single committed change
```

### What it must never do

- Edit, write, commit, push, or run destructive commands.
- Replace, expose, or transmit secrets/tokens/credentials.
- Invoke nested reviewers or reviewer panels from inside a review.
- Switch or override the requested model.
- Push just to review; push only when the user requested push/ship/PR update.
- Modify files outside the reviewed project.
- Mask validation failures or suggest unsafe fixes.

### Output

Exactly one JSON object matching `.opencode/skills/autoreview/references/schema.json`.
See `.opencode/skills/autoreview/references/rubric.md` for what to report/reject.

### Scope governor

Freeze a scope baseline before reviewing. Classify each finding as in-scope
blocker, follow-up, or stop-and-escalate. Stop and report a scope break when a
narrow PR turns into an architecture/protocol/migration/release-process change,
when the diff grows past 2x the original files or non-test LOC, or after two
non-converging patch cycles. Full rules in `SKILL.md` → *Scope governor*.