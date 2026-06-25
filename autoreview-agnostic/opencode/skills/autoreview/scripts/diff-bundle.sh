#!/usr/bin/env bash
# diff-bundle.sh — minimal, engine-agnostic port of the OpenClaw autoreview
# target-selection step. It only gathers the change bundle for review; it never
# calls an external review engine, never edits files, never commits, never pushes.
#
# Usage:
#   diff-bundle.sh --mode local              # unstaged + staged + untracked (dirty)
#   diff-bundle.sh --mode uncommitted        # alias for --mode local
#   diff-bundle.sh --mode branch --base origin/main
#   diff-bundle.sh --mode commit --commit HEAD
#   diff-bundle.sh --mode auto               # auto-resolve (default)
#
# Output: a single text bundle on stdout, containing metadata, status, stat, the
# patch, and untracked file contents. Redirect to a file or pipe to the reviewer.
#
# Safety: read-only. No git mutations. Fails closed on unknown mode or missing ref.
set -eo pipefail

mode="auto"
base=""
commit="HEAD"

usage() {
  cat <<'EOF'
diff-bundle.sh [--mode auto|local|uncommitted|branch|commit] [--base REF] [--commit REF]
  --mode auto                 auto-resolve: dirty local first, else PR base, else origin/main
  --mode local|uncommitted   dirty worktree (unstaged + staged + untracked)
  --mode branch --base REF   diff of current branch vs base ref
  --mode commit --commit REF diff of a single commit (default HEAD)
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --mode)
      if [ $# -lt 2 ] || [ -z "${2:-}" ]; then
        echo "diff-bundle: --mode requires an argument (auto|local|uncommitted|branch|commit)" >&2; exit 2
      fi
      mode="$2"; shift 2 ;;
    --base)
      if [ $# -lt 2 ] || [ -z "${2:-}" ]; then
        echo "diff-bundle: --base requires an argument" >&2; exit 2
      fi
      base="$2"; shift 2 ;;
    --commit)
      if [ $# -lt 2 ] || [ -z "${2:-}" ]; then
        echo "diff-bundle: --commit requires an argument" >&2; exit 2
      fi
      commit="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "diff-bundle: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

# Guard: must be inside a git repository
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "diff-bundle: not a git repository" >&2; exit 1
fi

# Resolve mode=auto: dirty first, else current PR base if available, else origin/main.
resolve_auto() {
  if ! git diff --quiet HEAD -- || ! git diff --quiet --cached || [ -n "$(git ls-files --others --exclude-standard)" ]; then
    mode="local"
    return
  fi
  if command -v gh >/dev/null 2>&1 && gh pr view --json baseRefName >/dev/null 2>&1; then
    local b
    b="$(gh pr view --json baseRefName --jq .baseRefName 2>/dev/null || true)"
    if [ -n "$b" ]; then base="origin/$b"; mode="branch"; return; fi
  fi
  base="origin/main"
  mode="branch"
}

case "$mode" in
  auto) resolve_auto ;;
  local|uncommitted) mode="local" ;;
  branch) [ -n "$base" ] || { echo "diff-bundle: --mode branch requires --base" >&2; exit 2; } ;;
  commit) : ;;
  *) echo "diff-bundle: unknown mode: $mode" >&2; exit 2 ;;
esac

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
current_branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '(detached)')"

# Validate refs before emitting any output
case "$mode" in
  branch)
    if ! git rev-parse --verify "$base" >/dev/null 2>&1; then
      echo "diff-bundle: base ref '$base' not resolvable locally. Run: git fetch origin && git rev-parse --verify '$base'" >&2
      exit 3
    fi
    ;;
  commit)
    if ! git rev-parse --verify "$commit" >/dev/null 2>&1; then
      echo "diff-bundle: commit ref '$commit' not resolvable" >&2; exit 3
    fi
    ;;
esac

print_meta() {
  echo "# autoreview change bundle"
  echo "mode: $mode"
  echo "base: ${base:-none}"
  echo "commit: ${commit:-none}"
  echo "repo: $repo_root"
  echo "branch: $current_branch"
  echo "generated_at: $(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo unknown)"
  echo
}

print_meta

case "$mode" in
  local)
    echo "## status (porcelain)"; git status --porcelain=v1 --untracked-files=all || true; echo
    echo "## stat (unstaged + staged)"; git diff --stat HEAD -- || true; echo
    echo "## patch (unstaged + staged vs HEAD)"; git diff HEAD -- || true; echo
    echo "## untracked files (full contents)"
    git ls-files --others --exclude-standard -z | while IFS= read -r -d '' f; do
      [ -f "$f" ] || continue
      echo "--- UNTRACKED: $f ---"
      cat -- "$f" 2>/dev/null || true
      echo
    done
    ;;
  branch)
    echo "## status (porcelain vs $base)"; git status --porcelain=v1 --untracked-files=all || true; echo
    echo "## stat vs $base"; git diff --stat "$base"...HEAD -- || true; echo
    echo "## patch vs $base (merge-base..HEAD)"; git diff "$(git merge-base "$base" HEAD)"..HEAD -- || true; echo
    echo "## untracked files (full contents)"
    git ls-files --others --exclude-standard -z | while IFS= read -r -d '' f; do
      [ -f "$f" ] || continue
      echo "--- UNTRACKED: $f ---"
      cat -- "$f" 2>/dev/null || true
      echo
    done
    ;;
  commit)
    echo "## stat ($commit)"; git show --stat --format=oneline "$commit" -- || true; echo
    echo "## patch ($commit)"; git show "$commit" -- || true; echo
    ;;
esac

echo "# end of bundle"