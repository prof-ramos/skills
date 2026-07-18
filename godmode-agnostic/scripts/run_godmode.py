#!/usr/bin/env python3
"""Back-compat wrapper → python -m godmode_agnostic run ..."""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running from skill root without install
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from godmode_agnostic.cli import main

if __name__ == "__main__":
    # Map legacy flags: scripts/run_godmode.py → run subcommand
    argv = ["run", *sys.argv[1:]]
    # legacy --mode classic still works via normalize_mode aliases
    raise SystemExit(main(argv))
