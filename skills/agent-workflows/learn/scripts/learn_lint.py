#!/usr/bin/env python3
"""Scan a draft learning entry for secrets/PII before it is persisted.

Redacts unambiguous secrets in place (API keys, tokens, JWTs, private key
blocks, .env-style KEY=VALUE assignments, Brazilian CPF numbers) and *flags*
lower-confidence matches (bare email addresses) for manual review instead of
auto-redacting them, since those have a real false-positive rate in
legitimate documentation. See references/scope-and-security.md for the full
rationale and the complete pattern list.

Usage:
    python3 learn_lint.py --file /path/to/draft-entry.md

Exit code 0: clean. Exit code 1: something was redacted or flagged -- the
agent must re-read the file and confirm it is safe before proceeding.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# (name, pattern, replacement) -- applied in order, redaction is unconditional.
REDACT_PATTERNS = [
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "generic_secret_assignment",
        re.compile(
            r"(?i)\b(api[_-]?key|secret|token|password|passwd|access[_-]?key)\s*[:=]\s*"
            r"['\"]?[A-Za-z0-9\-_/+=]{8,}['\"]?"
        ),
    ),
    ("bearer_token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9\-_.=]{10,}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")),
    (
        "private_key_block",
        re.compile(
            r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----.*?"
            r"-----END (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
    ("dotenv_line", re.compile(r"(?im)^[A-Z_][A-Z0-9_]*=.{4,}$")),
    ("cpf", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
]

# Flagged but not auto-redacted: real false-positive risk in legit docs.
FLAG_PATTERNS = [
    ("email_address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]


def lint(text: str) -> tuple[str, list[dict]]:
    findings: list[dict] = []
    redacted = text

    for name, pattern in REDACT_PATTERNS:
        matches = list(pattern.finditer(redacted))
        if not matches:
            continue
        findings.append({"type": name, "action": "redacted", "count": len(matches)})
        redacted = pattern.sub(f"[REDACTED:{name}]", redacted)

    for name, pattern in FLAG_PATTERNS:
        matches = list(pattern.finditer(redacted))
        if matches:
            findings.append({"type": name, "action": "flagged", "count": len(matches)})

    return redacted, findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, help="Path to the draft learning entry")
    parser.add_argument(
        "--no-fix",
        action="store_true",
        help="Report only, do not write redactions back to the file",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"error: {path} is not a file", file=sys.stderr)
        return 1

    original = path.read_text(encoding="utf-8")
    redacted, findings = lint(original)

    if not args.no_fix and redacted != original:
        path.write_text(redacted, encoding="utf-8")

    print(json.dumps({"file": str(path), "findings": findings}, indent=2, ensure_ascii=False))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
