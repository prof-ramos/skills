#!/usr/bin/env bash
# sync-shared.sh — propagate shared/schema.json, shared/rubric.md and shared/diff-bundle.sh
# to the OpenCode and Claude Code copies so the three copies stay identical.
#
# Usage: bash shared/sync-shared.sh
# Run from autoreview-agnostic/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cp "$ROOT/shared/schema.json" "$ROOT/opencode/skills/autoreview/references/schema.json"
cp "$ROOT/shared/schema.json" "$ROOT/claude-code/.claude/skills/autoreview/references/schema.json"

cp "$ROOT/shared/rubric.md" "$ROOT/opencode/skills/autoreview/references/rubric.md"
cp "$ROOT/shared/rubric.md" "$ROOT/claude-code/.claude/skills/autoreview/references/rubric.md"

cp "$ROOT/shared/diff-bundle.sh" "$ROOT/opencode/skills/autoreview/scripts/diff-bundle.sh"
cp "$ROOT/shared/diff-bundle.sh" "$ROOT/claude-code/.claude/skills/autoreview/scripts/diff-bundle.sh"
chmod +x "$ROOT/opencode/skills/autoreview/scripts/diff-bundle.sh"
chmod +x "$ROOT/claude-code/.claude/skills/autoreview/scripts/diff-bundle.sh"

echo "Shared files synced. Verifying..."
diff "$ROOT/shared/schema.json" "$ROOT/opencode/skills/autoreview/references/schema.json"
diff "$ROOT/shared/schema.json" "$ROOT/claude-code/.claude/skills/autoreview/references/schema.json"
diff "$ROOT/shared/rubric.md" "$ROOT/opencode/skills/autoreview/references/rubric.md"
diff "$ROOT/shared/rubric.md" "$ROOT/claude-code/.claude/skills/autoreview/references/rubric.md"
diff "$ROOT/shared/diff-bundle.sh" "$ROOT/opencode/skills/autoreview/scripts/diff-bundle.sh"
diff "$ROOT/shared/diff-bundle.sh" "$ROOT/claude-code/.claude/skills/autoreview/scripts/diff-bundle.sh"
echo "OK: all copies match shared/."
