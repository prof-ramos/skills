#!/usr/bin/env python3
"""
Script to list/add contacts and audiences with Resend REST API.

Usage:
  python3 contact_manage.py --action list-audiences
  python3 contact_manage.py --action create-audience --name "Beta Testers"
  python3 contact_manage.py --action add-contact --audience-id "78261ee2..." --email "user@example.com" --first-name "Alice"
  python3 contact_manage.py --action list-contacts --audience-id "78261ee2..."
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def make_api_request(
    api_key: str, path: str, method: str = "GET", payload: dict | None = None
) -> dict:
    url = f"https://api.resend.com{path}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "resend-contact-cli/1.0",
    }

    data_bytes = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            resp_body = resp.read().decode("utf-8")
            return json.loads(resp_body) if resp_body else {}
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8")
        sys.stderr.write(f"HTTP Error {err.code}: {error_body}\n")
        raise
    except urllib.error.URLError as err:
        sys.stderr.write(f"URL Error: {err.reason}\n")
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage audiences and contacts via Resend REST API."
    )
    parser.add_argument(
        "--action",
        choices=["list-audiences", "create-audience", "delete-audience", "list-contacts", "add-contact", "delete-contact"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("RESEND_API_KEY"),
        help="Resend API Key (defaults to RESEND_API_KEY env var)",
    )
    parser.add_argument(
        "--name",
        help="Audience name (required for 'create-audience')",
    )
    parser.add_argument(
        "--audience-id",
        help="Audience ID (required for contact operations and 'delete-audience')",
    )
    parser.add_argument(
        "--contact-id",
        help="Contact ID (required for 'delete-contact')",
    )
    parser.add_argument(
        "--email",
        help="Contact email (required for 'add-contact')",
    )
    parser.add_argument(
        "--first-name",
        help="Contact first name",
    )
    parser.add_argument(
        "--last-name",
        help="Contact last name",
    )
    parser.add_argument(
        "--unsubscribed",
        action="store_true",
        help="Mark contact as unsubscribed initially",
    )

    args = parser.parse_args()

    if not args.api_key:
        sys.stderr.write("Error: RESEND_API_KEY environment variable or --api-key argument is required.\n")
        return 1

    try:
        if args.action == "list-audiences":
            res = make_api_request(args.api_key, "/audiences", method="GET")
            print(json.dumps(res, indent=2))

        elif args.action == "create-audience":
            if not args.name:
                parser.error("--name is required for 'create-audience'.")
            payload = {"name": args.name}
            res = make_api_request(args.api_key, "/audiences", method="POST", payload=payload)
            print("Audience created successfully:")
            print(json.dumps(res, indent=2))

        elif args.action == "delete-audience":
            if not args.audience_id:
                parser.error("--audience-id is required for 'delete-audience'.")
            res = make_api_request(args.api_key, f"/audiences/{args.audience_id}", method="DELETE")
            print(json.dumps(res, indent=2))

        elif args.action == "list-contacts":
            if not args.audience_id:
                parser.error("--audience-id is required for 'list-contacts'.")
            res = make_api_request(args.api_key, f"/audiences/{args.audience_id}/contacts", method="GET")
            print(json.dumps(res, indent=2))

        elif args.action == "add-contact":
            if not args.audience_id:
                parser.error("--audience-id is required for 'add-contact'.")
            if not args.email:
                parser.error("--email is required for 'add-contact'.")
            payload = {
                "email": args.email,
                "unsubscribed": args.unsubscribed,
            }
            if args.first_name:
                payload["first_name"] = args.first_name
            if args.last_name:
                payload["last_name"] = args.last_name

            res = make_api_request(
                args.api_key,
                f"/audiences/{args.audience_id}/contacts",
                method="POST",
                payload=payload,
            )
            print("Contact added successfully:")
            print(json.dumps(res, indent=2))

        elif args.action == "delete-contact":
            if not args.audience_id or not args.contact_id:
                parser.error("Both --audience-id and --contact-id are required for 'delete-contact'.")
            res = make_api_request(
                args.api_key,
                f"/audiences/{args.audience_id}/contacts/{args.contact_id}",
                method="DELETE",
            )
            print("Contact deleted:")
            print(json.dumps(res, indent=2))

        return 0
    except Exception as exc:
        sys.stderr.write(f"Operation failed: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
