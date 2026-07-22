#!/usr/bin/env python3
"""
Batch email sending helper script for Resend API.

Usage:
  python3 send_batch.py --json-file batch_emails.json
  python3 send_batch.py --dry-run --json-file batch_emails.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def send_batch(api_key: str, batch_list: list[dict]) -> dict:
    if len(batch_list) > 100:
        raise ValueError("Resend batch API allows maximum 100 emails per request.")

    url = "https://api.resend.com/emails/batch"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "resend-python-cli/1.0",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(batch_list).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            resp_body = resp.read().decode("utf-8")
            return json.loads(resp_body)
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8")
        sys.stderr.write(f"HTTP Error {err.code}: {error_body}\n")
        raise
    except urllib.error.URLError as err:
        sys.stderr.write(f"URL Error: {err.reason}\n")
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dispatch batch transactional email payloads via Resend REST API."
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("RESEND_API_KEY"),
        help="Resend API Key (defaults to RESEND_API_KEY env var)",
    )
    parser.add_argument(
        "--json-file",
        required=True,
        help="Path to JSON file containing array of email request objects",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate JSON payload without making network calls",
    )

    args = parser.parse_args()

    if not os.path.exists(args.json_file):
        sys.stderr.write(f"Error: Specified JSON file '{args.json_file}' does not exist.\n")
        return 1

    try:
        with open(args.json_file, "r", encoding="utf-8") as f:
            batch_data = json.load(f)
    except Exception as exc:
        sys.stderr.write(f"Failed to read or parse JSON file: {exc}\n")
        return 1

    if not isinstance(batch_data, list):
        sys.stderr.write("Error: Batch JSON file must contain a top-level JSON list of email objects.\n")
        return 1

    if len(batch_data) == 0:
        sys.stderr.write("Error: Batch list is empty.\n")
        return 1

    if len(batch_data) > 100:
        sys.stderr.write(f"Error: Batch contains {len(batch_data)} items, exceeding limit of 100.\n")
        return 1

    if args.dry_run:
        print(f"Dry Run OK: Validated {len(batch_data)} email items.")
        print(json.dumps(batch_data[:2], indent=2))
        if len(batch_data) > 2:
            print(f"... and {len(batch_data) - 2} more items.")
        return 0

    if not args.api_key:
        sys.stderr.write("Error: RESEND_API_KEY environment variable or --api-key argument is required.\n")
        return 1

    try:
        res = send_batch(api_key=args.api_key, batch_list=batch_data)
        print("Batch email dispatched successfully!")
        print(json.dumps(res, indent=2))
        return 0
    except Exception as exc:
        sys.stderr.write(f"Failed to send batch email: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
