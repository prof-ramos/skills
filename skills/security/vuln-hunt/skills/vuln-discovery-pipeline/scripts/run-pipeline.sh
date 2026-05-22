#!/bin/bash
set -e

TARGET_DIR="${1:-~/intranet}"
REPORT_DIR="/tmp/vuln-report-$(date +%Y%m%d)"
AGENTS="${2:-40}"

echo "=== Vulnerability Discovery Pipeline v2.0 (James Red Team) ==="
echo "Target: $TARGET_DIR"
echo "Agents: $AGENTS"
echo "Report will be saved to: $REPORT_DIR"
echo ""

# Activate Red Team profile
hermes profile use redteam 2>/dev/null || echo "Using current profile with GODMODE override..."

mkdir -p "$REPORT_DIR/evidence"

echo "Phase 1: Recon - Generating architecture document..."
# Recon will be handled by the skill/orchestrator

echo "Starting full pipeline via Hermes skill..."
echo "Running: vuln-discovery-pipeline on $TARGET_DIR with $AGENTS agents"

# The actual execution is done via the skill + delegate_task/kanban
# This script serves as entrypoint and documentation

echo ""
echo "Pipeline launched. Full execution happens through the Hermes skill 'vuln-discovery-pipeline'."
echo "Check report at $REPORT_DIR/REPORT.md when complete."

# Optional: open report when done
# xdg-open "$REPORT_DIR/REPORT.md" 2>/dev/null || true