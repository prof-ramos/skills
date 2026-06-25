#!/usr/bin/env bash
# test-diff-bundle.sh — smoke tests for diff-bundle.sh
# Usage: bash shared/test-diff-bundle.sh
# Run from autoreview-agnostic/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE="$ROOT/shared/diff-bundle.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fail() { echo "FAIL: $1" >&2; exit 1; }
pass() { echo "PASS: $1"; }

# Test 1: syntax check
bash -n "$BUNDLE" || fail "syntax check"
pass "syntax check"

# Test 2: help works
"$BUNDLE" --help >/dev/null || fail "--help"
pass "--help"

# Test 3: unknown argument fails closed
if "$BUNDLE" --bogus 2>/dev/null; then
  fail "unknown argument should exit non-zero"
fi
pass "unknown argument fails closed"

# Test 4: missing --mode value fails closed
if "$BUNDLE" --mode 2>/dev/null; then
  fail "missing --mode value should exit non-zero"
fi
pass "missing --mode value fails closed"

# Test 5: --mode branch without --base fails closed
if "$BUNDLE" --mode branch 2>/dev/null; then
  fail "--mode branch without --base should exit non-zero"
fi
pass "--mode branch without --base fails closed"

# Test 6: outside git repo fails with exit 1
(
  cd "$TMP"
  if "$BUNDLE" --mode local 2>/dev/null; then
    fail "outside git repo should exit non-zero"
  fi
)
pass "outside git repo fails closed"

# Test 7: --mode commit HEAD succeeds inside repo
"$BUNDLE" --mode commit --commit HEAD >"$TMP/commit.out" 2>"$TMP/commit.err" || fail "commit HEAD"
grep -q "# autoreview change bundle" "$TMP/commit.out" || fail "bundle header missing"
grep -q "# end of bundle" "$TMP/commit.out" || fail "end-of-bundle marker missing"
pass "--mode commit HEAD produces valid bundle"

# Test 8: --mode auto resolves to commit when clean tree
"$BUNDLE" --mode auto >"$TMP/auto.out" 2>"$TMP/auto.err" || fail "mode auto"
grep -qE "mode: (commit|branch|local)" "$TMP/auto.out" || fail "auto mode not resolved"
pass "--mode auto resolves"

# Test 9: unresolvable base ref fails with exit 3
if "$BUNDLE" --mode branch --base origin/nonexistent-ref-for-test 2>/dev/null; then
  fail "unresolvable base should exit non-zero"
fi
pass "unresolvable base ref fails closed"

# Test 10: unresolvable commit ref fails with exit 3
if "$BUNDLE" --mode commit --commit deadbeef 2>/dev/null; then
  fail "unresolvable commit should exit non-zero"
fi
pass "unresolvable commit ref fails closed"

echo
echo "All tests passed."
