#!/usr/bin/env python3
"""Back-compat wrapper → python -m godmode_agnostic detect ..."""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from godmode_agnostic.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["detect", *sys.argv[1:]]))
