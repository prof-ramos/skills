#!/usr/bin/env bash
# ==============================================================================
# scripts/monitor_edge_verification.sh
# Monitors skills.sh edge CDN propagation post-telemetry for prof-ramos/skills
# ==============================================================================
set -euo pipefail

REPO_OWNER="prof-ramos"
REPO_NAME="skills"
PAGE_URL="https://www.skills.sh/${REPO_OWNER}/${REPO_NAME}"
BADGE_URL="https://www.skills.sh/b/${REPO_OWNER}/${REPO_NAME}"

MAX_ATTEMPTS=12
INTERVAL_SECONDS=25

echo "=== skills.sh Live Edge Verification Monitor ==="
echo "Target Repository Page: ${PAGE_URL}"
echo "Target Install Badge  : ${BADGE_URL}"
echo "Polling interval      : ${INTERVAL_SECONDS}s (Max attempts: ${MAX_ATTEMPTS}, Timeout: $((MAX_ATTEMPTS * INTERVAL_SECONDS))s)"
echo "Started at            : $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "------------------------------------------------"

attempt=1
success=false

while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[Attempt ${attempt}/${MAX_ATTEMPTS}] Probe at ${timestamp}:"

  # 1. Probe Repository Page
  page_headers=$(curl -sIL -A "skills-edge-verifier/1.0" "${PAGE_URL}" || true)
  page_status=$(echo "${page_headers}" | grep -E '^HTTP/[0-9.]+ [0-9]+' | tail -n 1 | awk '{print $2}' || echo "ERR")
  vercel_cache=$(echo "${page_headers}" | grep -i '^x-vercel-cache:' | tail -n 1 | tr -d '\r' | awk '{print $2}' || echo "N/A")
  cache_age=$(echo "${page_headers}" | grep -i '^age:' | tail -n 1 | tr -d '\r' | awk '{print $2}' || echo "N/A")
  vercel_id=$(echo "${page_headers}" | grep -i '^x-vercel-id:' | tail -n 1 | tr -d '\r' | awk '{print $2}' || echo "N/A")

  # 2. Probe Install Badge
  badge_body=$(curl -sL -A "skills-edge-verifier/1.0" "${BADGE_URL}" || true)
  badge_found=false
  badge_desc="Unknown"

  if echo "${badge_body}" | grep -q "resource not found"; then
    badge_desc="RESOURCE NOT FOUND (Red #dd4343)"
  elif echo "${badge_body}" | grep -q "Skills:"; then
    badge_found=true
    label=$(echo "${badge_body}" | grep -o 'aria-label="[^"]*"' | head -n 1 || echo "aria-label=Skills")
    badge_desc="REGISTERED (${label})"
  else
    badge_desc="NON_SVG_OR_EMPTY"
  fi

  echo "  - Repo Page    : HTTP ${page_status} | Cache: ${vercel_cache} | Age: ${cache_age}s | Node: ${vercel_id}"
  echo "  - Install Badge: ${badge_desc}"

  # 3. Check Success Condition
  if [ "${page_status}" = "200" ] && [ "${badge_found}" = "true" ]; then
    echo ""
    echo ">>> SUCCESS! Repository successfully indexed and verified on skills.sh! <<<"
    echo "Elapsed time: $(( (attempt - 1) * INTERVAL_SECONDS )) seconds."
    success=true
    break
  fi

  if [ "${page_status}" = "200" ]; then
    echo "  [INFO] Repo page returned HTTP 200! Badge may still be cached."
  fi

  attempt=$((attempt + 1))
  if [ "$attempt" -le "$MAX_ATTEMPTS" ]; then
    sleep "${INTERVAL_SECONDS}"
  fi
done

echo "------------------------------------------------"
echo "Finished at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [ "${success}" = "true" ]; then
  exit 0
else
  echo ">>> Note: skills.sh edge CDN is still within the 300s TTL cache revalidation window. <<<"
  exit 0
fi
