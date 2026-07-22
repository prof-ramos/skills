#!/usr/bin/env python3
"""
Command-line script to construct and send transactional email requests to Resend API.

Usage:
  python3 send_email.py --to user@example.com --subject "Hello" --html "<p>World</p>"
  python3 send_email.py --from "Acme <app@yourdomain.com>" --to user@example.com --subject "Test" --text "Plain text body"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def send_email(
    api_key: str,
    from_email: str,
    to_emails: list[str],
    subject: str,
    html: str | None = None,
    text: str | None = None,
    reply_to: str | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    tags: list[dict[str, str]] | None = None,
) -> dict:
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "resend-python-cli/1.0",
    }

    payload: dict[str, object] = {
        "from": from_email,
        "to": to_emails,
        "subject": subject,
    }

    if html:
        payload["html"] = html
    if text:
        payload["text"] = text
    if reply_to:
        payload["reply_to"] = [reply_to] if isinstance(reply_to, str) else reply_to
    if cc:
        payload["cc"] = cc
    if bcc:
        payload["bcc"] = bcc
    if tags:
        payload["tags"] = tags

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
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
        description="Construct and dispatch single transactional email via Resend REST API."
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("RESEND_API_KEY"),
        help="Resend API Key (defaults to RESEND_API_KEY env var)",
    )
    parser.add_argument(
        "--from-email",
        default=os.environ.get("RESEND_DEFAULT_FROM", "Acme <onboarding@resend.dev>"),
        help="Sender email address with optional display name",
    )
    parser.add_argument(
        "--to",
        nargs="+",
        required=True,
        help="Recipient email address(es)",
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="Email subject line",
    )
    parser.add_argument(
        "--html",
        help="HTML body content string",
    )
    parser.add_argument(
        "--text",
        help="Plain text body content string",
    )
    parser.add_argument(
        "--reply-to",
        help="Reply-to email address",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print JSON request body without dispatching HTTP call",
    )

    args = parser.parse_args()

    if not args.html and not args.text:
        parser.error("At least one of --html or --text must be specified.")

    if args.dry_run:
        dry_payload = {
            "from": args.from_email,
            "to": args.to,
            "subject": args.subject,
            "html": args.html,
            "text": args.text,
            "reply_to": args.reply_to,
        }
        print("Dry Run - Request Payload:")
        print(json.dumps(dry_payload, indent=2))
        return 0

    if not args.api_key:
        sys.stderr.write("Error: RESEND_API_KEY environment variable or --api-key argument is required.\n")
        return 1

    try:
        res = send_email(
            api_key=args.api_key,
            from_email=args.from_email,
            to_emails=args.to,
            subject=args.subject,
            html=args.html,
            text=args.text,
            reply_to=args.reply_to,
        )
        print("Email dispatched successfully!")
        print(json.dumps(res, indent=2))
        return 0
    except Exception as exc:
        sys.stderr.write(f"Failed to send email: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
