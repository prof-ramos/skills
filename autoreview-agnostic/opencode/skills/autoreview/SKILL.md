---
name: autoreview
description: Closeout structured code review. Use after non-trivial edits before commit/ship, or to review a local branch/PR/commit. The reviewer is read-only, returns a JSON findings bundle against a fixed schema, verifies every finding against real code, and rejects speculative/broad/unrealistic findings.
version: 1.0.0
---

# Autoreview (OpenCode)

Structured closeout code review for OpenCode. This is a review skill, not approval
routing and not a license to rewrite the task.

## When to use

- After non-trivial code edits, before final/commit/ship.
- User asks for a second-model review, autoreview, or closeout check.
- Reviewing a local branch or PR branch after fixes.

## Invocation

Run it as a command (delegates to the `autoreview` subagent):

```text
/autoreview                    # auto target (dirty local → PR base → origin/main)
/autoreview local              # dirty worktree (unstaged + staged + untracked)
/autoreview branch origin/main # diff of current branch vs origin/main
/autoreview commit HEAD        # single committed change
```

The `autoreview` agent is configured in `opencode.json` as `mode: subagent` with
`edit: deny` and read-only git/bash permissions.

## Contract (preserved from the OpenClaw original)

- Review output is **advisory**. Never blindly apply it.
- **Verify every finding** by reading the real code path and adjacent files; read
  dependency docs/source/types when a finding depends on external behavior.
- **Reject** unrealistic edge cases, speculative risks, broad rewrites, and fixes
  that over-complicate the codebase.
- Prefer the **smallest fix at the correct ownership boundary**; no refactor unless
  it clearly improves the bug class.
- When an accepted finding shows a bug class or repeated pattern, inspect the
  current PR scope for **sibling instances** before fixing.
- Keep reviewing until the structured output returns no accepted/actionable
  findings — but only while the work stays inside the original task scope.
- If a review-triggered fix changes code, rerun focused tests and rerun the review.
- Never switch or override the requested model. If the review hits capacity, retry
  the same command a few times with the same model.
- Do not invoke nested reviewers or reviewer panels from inside the review. One
  bundle, one review, one structured result, stop.
- Stop as soon as the review exits with no accepted/actionable findings. Do not run
  an extra review just to get nicer "clean" wording.
- Do not push just to review. Push only when the user requested push/ship/PR update.

## Scope governor

Freeze a scope baseline before the first review: original request, target branch,
intended behavior, owner boundary, changed files, non-test LOC. For inherited or
already-bloated branches, use the **intended PR diff** as the baseline, not all
branch drift.

Classify each finding before acting:

- **In-scope blocker** — introduced by the current diff, same owner boundary,
  fixable without changing the task's contract.
- **Follow-up** — real, but adjacent bug class / sibling surface / broader track.
- **Stop-and-escalate** — requires a new protocol/config/storage/public API
  contract, a different owner boundary, a release-process change, or a design
  choice outside the original request.

Stop and report a scope break instead of continuing when:

- a narrow PR turns into an architecture/protocol/migration/release-process change;
- the diff grows past 2x the original files or non-test LOC without explicit
  approval to expand scope;
- two review-triggered patch cycles have not converged (pause and reclassify every
  remaining finding before another edit);
- the best fix is "define the canonical contract first" rather than another local
  inference layer;
- fixing the accepted finding would make the PR no longer describe the same
  behavior, issue, or owner boundary.

**Release branches**: apply freeze discipline even when the branch name is not
release-like. Fix only release blockers, failed release infra, exact backports,
install/upgrade breakage, data loss, crashes, or concrete security exposure.
Non-blocking findings are follow-ups for `main`.

## Pick target

Use `shared/diff-bundle.sh` (read-only) to gather the bundle:

```bash
bash .opencode/skills/autoreview/scripts/diff-bundle.sh --mode local
bash .opencode/skills/autoreview/scripts/diff-bundle.sh --mode branch --base origin/main
bash .opencode/skills/autoreview/scripts/diff-bundle.sh --mode commit --commit HEAD
```

If an open PR exists, use its actual base:

```bash
base=$(gh pr view --json baseRefName --jq .baseRefName)
bash .opencode/skills/autoreview/scripts/diff-bundle.sh --mode branch --base "origin/$base"
```

## Output

Exactly one JSON object matching `references/schema.json`. See `references/rubric.md`
for what to report and what to reject. Empty `findings` + `patch is correct` is the
clean result; report it as `autoreview clean: no accepted/actionable findings reported`.

## Final report

Include: review command/mode used, tests/proof run (if any), findings
accepted/rejected with one-line reasons, and the clean/incorrect verdict from the
final run. Do not run another review solely to improve final-report wording.

## Safety

- Never replace, expose, or transmit secrets/tokens/credentials. If one appears in
  the bundle, flag the risk as a `security` finding and do not reproduce its value.
- Never edit, write, commit, push, or run destructive commands (reviewer is
  read-only).
- Never send data to external services beyond read-only doc lookups the user can see.
- Never modify files outside the reviewed project.
- Always separate facts (from read code/docs) from inferences.
- Never mask validation failures or suggest unsafe fixes.