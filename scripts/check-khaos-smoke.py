#!/usr/bin/env python3
"""Offline smoke check for the KHAOS activation module."""

from __future__ import annotations

import contextlib
import io
import os
import sys
from pathlib import Path


sys.dont_write_bytecode = True
KIT_DIR = Path(__file__).resolve().parents[1] / "ollama-godmode" / "godmode-kit"
sys.path.insert(0, str(KIT_DIR))

from activate import DEFAULT_PROVIDERS, TEMPLATES, activate_khaos  # noqa: E402


def main() -> int:
    required_providers = {"ollama-cloud", "openai", "anthropic", "ollama-local", "openrouter", "xai"}
    missing = required_providers - set(DEFAULT_PROVIDERS)
    if missing:
        print(f"Missing provider defaults: {sorted(missing)}", file=sys.stderr)
        return 1

    required_strategies = {"refusal_inversion", "og_godmode", "direct_godmode", "pliny_love"}
    missing = required_strategies - set(TEMPLATES)
    if missing:
        print(f"Missing strategies: {sorted(missing)}", file=sys.stderr)
        return 1

    os.environ.setdefault("OLLAMA_API_KEY", "test-dummy-key")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        activate_khaos(
            provider="ollama-cloud",
            model="gemma4:31b",
            api_key=None,
            base_url=None,
            strategy="refusal_inversion",
            dry_run=True,
            interactive=False,
            honcho_key=None,
            honcho_workspace=None,
        )

    text = output.getvalue()
    if "Dry run complete" not in text:
        print("KHAOS dry-run did not complete", file=sys.stderr)
        return 1
    if "test-dummy-key" in text:
        print("KHAOS dry-run leaked the test API key", file=sys.stderr)
        return 1

    print("KHAOS smoke OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
