#!/usr/bin/env python3
"""
Script to list, add, and verify domain DKIM/SPF TXT/CNAME records with Resend API.

Usage:
  python3 domain_manage.py --action list
  python3 domain_manage.py --action add --name mail.yourdomain.com --region us-east-1
  python3 domain_manage.py --action verify --domain-id "d91cd95f-6947-4a6f-a964-00c401be29c6"
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
        "User-Agent": "resend-domain-cli/1.0",
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
        description="List, create, or verify custom sending domains via Resend REST API."
    )
    parser.add_argument(
        "--action",
        choices=["list", "get", "add", "verify", "delete"],
        required=True,
        help="Domain management action to perform",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("RESEND_API_KEY"),
        help="Resend API Key (defaults to RESEND_API_KEY env var)",
    )
    parser.add_argument(
        "--name",
        help="Domain name (e.g. mail.yourdomain.com) - required for 'add'",
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        choices=["us-east-1", "eu-west-1", "ap-southeast-1"],
        help="Infrastructure AWS region for sending domain",
    )
    parser.add_argument(
        "--domain-id",
        help="Domain ID - required for 'get', 'verify', and 'delete'",
    )

    args = parser.parse_args()

    if not args.api_key:
        sys.stderr.write("Error: RESEND_API_KEY environment variable or --api-key argument is required.\n")
        return 1

    try:
        if args.action == "list":
            res = make_api_request(args.api_key, "/domains", method="GET")
            print(json.dumps(res, indent=2))

        elif args.action == "get":
            if not args.domain_id:
                parser.error("--domain-id is required for 'get' action.")
            res = make_api_request(args.api_key, f"/domains/{args.domain_id}", method="GET")
            print(json.dumps(res, indent=2))

        elif args.action == "add":
            if not args.name:
                parser.error("--name is required for 'add' action.")
            payload = {"name": args.name, "region": args.region}
            res = make_api_request(args.api_key, "/domains", method="POST", payload=payload)
            print("Domain created! Required DNS records:")
            print(json.dumps(res, indent=2))

        elif args.action == "verify":
            if not args.domain_id:
                parser.error("--domain-id is required for 'verify' action.")
            res = make_api_request(
                args.api_key, f"/domains/{args.domain_id}/verify", method="POST"
            )
            print("Domain verification triggered:")
            print(json.dumps(res, indent=2))

        elif args.action == "delete":
            if not args.domain_id:
                parser.error("--domain-id is required for 'delete' action.")
            res = make_api_request(
                args.api_key, f"/domains/{args.domain_id}", method="DELETE"
            )
            print("Domain deleted:")
            print(json.dumps(res, indent=2))

        return 0
    except Exception as exc:
        sys.stderr.write(f"Operation failed: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
