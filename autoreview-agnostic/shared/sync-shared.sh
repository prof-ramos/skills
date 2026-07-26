#!/usr/bin/env bash
# sync-shared.sh — propagate shared/ into the OpenCode and Claude Code copies
# so they stay identical (schema.json, rubric.md, diff-bundle.sh: verbatim
# copies; agent.md: rendered from shared/agent-prompt.template.md, since the
# two runtimes' agent-definition frontmatter and tool-enforcement mechanisms
# genuinely differ -- see shared/agent-prompt.template.md's header comment).
#
# Usage: bash shared/sync-shared.sh
# Run from autoreview-agnostic/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"

cp "$ROOT/shared/schema.json" "$ROOT/opencode/skills/autoreview/references/schema.json"
cp "$ROOT/shared/schema.json" "$ROOT/claude-code/.claude/skills/autoreview/references/schema.json"

cp "$ROOT/shared/rubric.md" "$ROOT/opencode/skills/autoreview/references/rubric.md"
cp "$ROOT/shared/rubric.md" "$ROOT/claude-code/.claude/skills/autoreview/references/rubric.md"

cp "$ROOT/shared/diff-bundle.sh" "$ROOT/opencode/skills/autoreview/scripts/diff-bundle.sh"
cp "$ROOT/shared/diff-bundle.sh" "$ROOT/claude-code/.claude/skills/autoreview/scripts/diff-bundle.sh"
chmod +x "$ROOT/opencode/skills/autoreview/scripts/diff-bundle.sh"
chmod +x "$ROOT/claude-code/.claude/skills/autoreview/scripts/diff-bundle.sh"

"$PYTHON" "$ROOT/shared/render_agent_prompt.py" opencode ".opencode/skills/autoreview" \
  > "$ROOT/opencode/agent/autoreview.md"
"$PYTHON" "$ROOT/shared/render_agent_prompt.py" claude-code ".claude/skills/autoreview" \
  > "$ROOT/claude-code/.claude/agents/autoreview.md"

echo "Shared files synced. Verifying..."
diff "$ROOT/shared/schema.json" "$ROOT/opencode/skills/autoreview/references/schema.json"
diff "$ROOT/shared/schema.json" "$ROOT/claude-code/.claude/skills/autoreview/references/schema.json"
diff "$ROOT/shared/rubric.md" "$ROOT/opencode/skills/autoreview/references/rubric.md"
diff "$ROOT/shared/rubric.md" "$ROOT/claude-code/.claude/skills/autoreview/references/rubric.md"
diff "$ROOT/shared/diff-bundle.sh" "$ROOT/opencode/skills/autoreview/scripts/diff-bundle.sh"
diff "$ROOT/shared/diff-bundle.sh" "$ROOT/claude-code/.claude/skills/autoreview/scripts/diff-bundle.sh"

# agent.md files are generated, not copied -- verify by re-rendering to a
# scratch file and diffing, so a hand-edit made directly to the generated
# file (bypassing the template) is caught instead of silently drifting.
tmp_opencode="$(mktemp)"
tmp_claude="$(mktemp)"
trap 'rm -f "$tmp_opencode" "$tmp_claude"' EXIT
"$PYTHON" "$ROOT/shared/render_agent_prompt.py" opencode ".opencode/skills/autoreview" > "$tmp_opencode"
"$PYTHON" "$ROOT/shared/render_agent_prompt.py" claude-code ".claude/skills/autoreview" > "$tmp_claude"
diff "$tmp_opencode" "$ROOT/opencode/agent/autoreview.md"
diff "$tmp_claude" "$ROOT/claude-code/.claude/agents/autoreview.md"

echo "OK: all copies match shared/."
