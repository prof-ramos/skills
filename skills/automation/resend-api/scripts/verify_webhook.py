#!/usr/bin/env python3
"""
Python script verifying Svix webhook signatures delivered by Resend.

Usage:
  python3 verify_webhook.py --secret "whsec_..." --id "msg_123" --timestamp "1721635200" --signature "v1,..." --body '{"type":"email.sent"}'
  python3 verify_webhook.py --test-synthetic
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import os
import sys
import time


def verify_svix_signature(
    raw_body: bytes,
    svix_id: str,
    svix_timestamp: str,
    svix_signature: str,
    secret: str,
    tolerance_seconds: int = 300,
) -> bool:
    """
    Verify Svix HMAC-SHA256 signature against raw body and headers.
    """
    if not svix_id or not svix_timestamp or not svix_signature:
        raise ValueError("Missing required Svix headers (svix-id, svix-timestamp, svix-signature)")

    try:
        ts = int(svix_timestamp)
    except ValueError:
        raise ValueError("Invalid svix-timestamp format (must be integer string)")

    # Check timestamp freshness window
    current_time = time.time()
    if abs(current_time - ts) > tolerance_seconds:
        raise ValueError(
            f"Timestamp outside tolerance window. Diff: {abs(current_time - ts):.1f}s > {tolerance_seconds}s"
        )

    # Strip whsec_ prefix if present
    clean_secret = secret.replace("whsec_", "")
    try:
        secret_bytes = base64.b64decode(clean_secret)
    except Exception as exc:
        raise ValueError(f"Invalid base64 encoding in webhook secret: {exc}")

    # Signed payload format: msg_id.msg_timestamp.raw_body
    signed_payload = f"{svix_id}.{svix_timestamp}.".encode("utf-8") + raw_body

    # Calculate HMAC-SHA256
    digest = hmac.new(secret_bytes, signed_payload, hashlib.sha256).digest()
    expected_b64 = base64.b64encode(digest).decode("utf-8")
    expected_signature = f"v1,{expected_b64}"

    # Signatures header may contain multiple space-separated signatures
    passed_signatures = svix_signature.split(" ")
    for sig in passed_signatures:
        if hmac.compare_digest(sig.strip(), expected_signature):
            return True

    raise ValueError("Signature mismatch: Provided signature does not match computed HMAC")


def run_synthetic_test() -> bool:
    """Generate a synthetic Svix signature and verify it locally."""
    secret = "whsec_dGVzdF9zZWNyZXRfa2V5XzEyMzQ1Njc4OQ=="  # base64 secret "test_secret_key_123456789"
    raw_body = b'{"type":"email.delivered","data":{"email_id":"49bf7fff-9b12-4716-9d8a-9040716a4959"}}'
    svix_id = "msg_synthetic_test_123"
    svix_timestamp = str(int(time.time()))

    # Compute expected signature
    clean_secret = secret.replace("whsec_", "")
    secret_bytes = base64.b64decode(clean_secret)
    signed_payload = f"{svix_id}.{svix_timestamp}.".encode("utf-8") + raw_body
    digest = hmac.new(secret_bytes, signed_payload, hashlib.sha256).digest()
    svix_signature = f"v1,{base64.b64encode(digest).decode('utf-8')}"

    print("Running Synthetic Webhook Signature Verification Test...")
    print(f"Secret: {secret}")
    print(f"Svix ID: {svix_id}")
    print(f"Svix Timestamp: {svix_timestamp}")
    print(f"Generated Signature: {svix_signature}")

    try:
        is_valid = verify_svix_signature(
            raw_body=raw_body,
            svix_id=svix_id,
            svix_timestamp=svix_timestamp,
            svix_signature=svix_signature,
            secret=secret,
        )
        if is_valid:
            print("SYNTHETIC TEST RESULT: SUCCESS (Signature verified perfectly)")
            return True
    except Exception as exc:
        print(f"SYNTHETIC TEST RESULT: FAILED ({exc})")
        return False
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify Svix webhook signature for Resend HTTP POST requests."
    )
    parser.add_argument(
        "--secret",
        default=os.environ.get("RESEND_WEBHOOK_SECRET"),
        help="Svix Webhook Secret (starts with whsec_)",
    )
    parser.add_argument(
        "--id",
        help="Value of 'svix-id' header",
    )
    parser.add_argument(
        "--timestamp",
        help="Value of 'svix-timestamp' header",
    )
    parser.add_argument(
        "--signature",
        help="Value of 'svix-signature' header",
    )
    parser.add_argument(
        "--body",
        help="Raw HTTP request body string",
    )
    parser.add_argument(
        "--test-synthetic",
        action="store_true",
        help="Execute self-test synthetic signature verification",
    )

    args = parser.parse_args()

    if args.test_synthetic:
        success = run_synthetic_test()
        return 0 if success else 1

    if not args.secret:
        sys.stderr.write("Error: --secret or RESEND_WEBHOOK_SECRET environment variable is required.\n")
        return 1

    if not args.id or not args.timestamp or not args.signature or not args.body:
        sys.stderr.write("Error: --id, --timestamp, --signature, and --body are required for verification.\n")
        return 1

    try:
        is_valid = verify_svix_signature(
            raw_body=args.body.encode("utf-8"),
            svix_id=args.id,
            svix_timestamp=args.timestamp,
            svix_signature=args.signature,
            secret=args.secret,
        )
        if is_valid:
            print("Webhook signature VALID!")
            return 0
    except Exception as exc:
        sys.stderr.write(f"Webhook signature INVALID: {exc}\n")
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
