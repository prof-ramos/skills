#!/usr/bin/env python3
"""Export vendor TypeScript GODMODE constants → godmode_bundle.json.

Parses (does not invent) prompt text from:
  vendor/g0dm0d3/src/lib/godmode-prompt.ts
  vendor/g0dm0d3/src/lib/libertas.ts
  vendor/g0dm0d3/src/lib/godmode-pipeline.ts

CLI:
  python3 scripts/export_bundle.py              # write default path
  python3 scripts/export_bundle.py --check      # exit 1 on drift vs committed JSON
  python3 scripts/export_bundle.py --out PATH
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from godmode_agnostic.core import ROOT

VENDOR_LIB = ROOT / "vendor" / "g0dm0d3" / "src" / "lib"
DEFAULT_OUT = ROOT / "vendor" / "g0dm0d3" / "godmode_bundle.json"

# Stable metadata (matches committed bundle; not re-derived from TS prose).
BUNDLE_META: dict[str, Any] = {
    "source": "https://github.com/elder-plinius/G0DM0D3",
    "commit_note": "Vendored from main; constants extracted 1:1 from source files",
    "license": "AGPL-3.0",
    "upstream_files": [
        "src/lib/godmode-prompt.ts",
        "src/lib/libertas.ts",
        "api/lib/ultraplinian.ts (DEPTH_DIRECTIVE + applyGodmodeBoost)",
        "api/routes/chat.ts (runPipeline wiring)",
    ],
}

PIPELINE_DEFAULT_FLAGS: dict[str, Any] = {
    "godmode": True,
    "autotune": True,
    "parseltongue": False,
    "stm_modules": [],
}

# Fallback if applyGodmodeBoost body cannot be parsed (must match TS).
DEFAULT_BOOST: dict[str, float] = {
    "temperature_delta": 0.1,
    "presence_penalty_delta": 0.15,
    "frequency_penalty_delta": 0.1,
    "caps": 2.0,
    "default_temperature": 0.7,
}

HOF_FIELD_ORDER = (
    "id",
    "model",
    "codename",
    "description",
    "color",
    "system",
    "user",
    "fast",
)


def _decode_js_string_escapes(s: str) -> str:
    """Decode common JS string / template-literal escape sequences."""
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        if i + 1 >= n:
            out.append("\\")
            i += 1
            continue
        nxt = s[i + 1]
        if nxt == "u" and i + 5 < n:
            hex4 = s[i + 2 : i + 6]
            if re.fullmatch(r"[0-9a-fA-F]{4}", hex4):
                out.append(chr(int(hex4, 16)))
                i += 6
                continue
        if nxt == "x" and i + 3 < n:
            hex2 = s[i + 2 : i + 4]
            if re.fullmatch(r"[0-9a-fA-F]{2}", hex2):
                out.append(chr(int(hex2, 16)))
                i += 4
                continue
        simple = {
            "n": "\n",
            "r": "\r",
            "t": "\t",
            "b": "\b",
            "f": "\f",
            "v": "\v",
            "0": "\0",
            "\\": "\\",
            "'": "'",
            '"': '"',
            "`": "`",
            "/": "/",
        }
        if nxt in simple:
            out.append(simple[nxt])
            i += 2
            continue
        # Unknown escape: keep the character after backslash (JS behavior for most).
        out.append(nxt)
        i += 2
    return "".join(out)


class _Scanner:
    """Owns a cursor into a JS/TS source string.

    Replaces the (str, int) position tuples the parsing functions below used
    to thread between themselves by hand -- each function now advances a
    shared cursor via a small set of methods (peek/advance/startswith/eof)
    instead of every caller re-deriving the next index itself.
    """

    def __init__(self, source: str, pos: int = 0) -> None:
        self.source = source
        self.pos = pos

    @property
    def eof(self) -> bool:
        return self.pos >= len(self.source)

    def peek(self, offset: int = 0) -> str:
        i = self.pos + offset
        return self.source[i] if i < len(self.source) else ""

    def startswith(self, s: str) -> bool:
        return self.source.startswith(s, self.pos)

    def advance(self, n: int = 1) -> str:
        chunk = self.source[self.pos : self.pos + n]
        self.pos += n
        return chunk

    def skip_ws_and_comments(self) -> None:
        n = len(self.source)
        while self.pos < n:
            if self.source[self.pos] in " \t\r\n":
                self.pos += 1
                continue
            if self.startswith("//"):
                nl = self.source.find("\n", self.pos)
                self.pos = n if nl < 0 else nl + 1
                continue
            if self.startswith("/*"):
                end = self.source.find("*/", self.pos + 2)
                self.pos = n if end < 0 else end + 2
                continue
            break


def extract_template_const(source: str, name: str) -> str:
    r"""Extract export const NAME = `...` (unescaped closing backtick)."""
    # Allow optional type annotation: export const NAME: Type = `
    pat = re.compile(
        rf"export\s+const\s+{re.escape(name)}\s*(?::[^=]+)?=\s*`",
        re.MULTILINE,
    )
    m = pat.search(source)
    if not m:
        raise ValueError(f"export const {name} = `...` not found")
    scanner = _Scanner(source, pos=m.end())
    start = scanner.pos  # first char inside template
    while not scanner.eof:
        c = scanner.peek()
        if c == "\\":
            scanner.advance(2 if scanner.pos + 1 < len(source) else 1)
            continue
        if c == "`":
            raw = scanner.source[start : scanner.pos]
            return _decode_js_string_escapes(raw)
        scanner.advance()
    raise ValueError(f"unclosed template literal for {name}")


def extract_single_quoted(scanner: _Scanner) -> str:
    """Parse a JS single-quoted string; scanner.pos must be at the opening quote."""
    if scanner.peek() != "'":
        raise ValueError("expected single-quoted string")
    scanner.advance()
    raw_parts: list[str] = []
    while not scanner.eof:
        c = scanner.peek()
        if c == "\\":
            raw_parts.append(scanner.advance(2) if scanner.pos + 1 < len(scanner.source) else scanner.advance(1))
            continue
        if c == "'":
            scanner.advance()
            return _decode_js_string_escapes("".join(raw_parts))
        raw_parts.append(scanner.advance())
    raise ValueError("unclosed single-quoted string")


def extract_template_at(scanner: _Scanner) -> str:
    """Parse a template literal; scanner.pos must be at the opening backtick."""
    if scanner.peek() != "`":
        raise ValueError("expected template literal")
    scanner.advance()
    start = scanner.pos
    while not scanner.eof:
        c = scanner.peek()
        if c == "\\":
            scanner.advance(2 if scanner.pos + 1 < len(scanner.source) else 1)
            continue
        if c == "`":
            raw = scanner.source[start : scanner.pos]
            scanner.advance()
            return _decode_js_string_escapes(raw)
        scanner.advance()
    raise ValueError("unclosed template literal")


def parse_hall_of_fame(source: str) -> list[dict[str, Any]]:
    """Parse HALL_OF_FAME array object literals from libertas.ts."""
    m = re.search(r"export\s+const\s+HALL_OF_FAME\s*[^=]*=\s*\[", source)
    if not m:
        raise ValueError("HALL_OF_FAME array not found")
    scanner = _Scanner(source, pos=m.end())
    combos: list[dict[str, Any]] = []

    while True:
        scanner.skip_ws_and_comments()
        if scanner.eof:
            raise ValueError("unclosed HALL_OF_FAME array")
        if scanner.peek() == "]":
            break
        if scanner.peek() == ",":
            scanner.advance()
            continue
        if scanner.peek() != "{":
            raise ValueError(f"expected object in HALL_OF_FAME at index {scanner.pos}")
        scanner.advance()
        fields: dict[str, Any] = {}
        while True:
            scanner.skip_ws_and_comments()
            if scanner.eof:
                raise ValueError("unclosed HoF object")
            if scanner.peek() == "}":
                scanner.advance()
                break
            if scanner.peek() == ",":
                scanner.advance()
                continue
            # property name
            km = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", scanner.source[scanner.pos :])
            if not km:
                raise ValueError(
                    f"expected property at index {scanner.pos}: {scanner.source[scanner.pos:scanner.pos+40]!r}"
                )
            key = km.group(1)
            scanner.advance(km.end())
            scanner.skip_ws_and_comments()
            if scanner.eof:
                raise ValueError(f"missing value for {key}")
            if scanner.peek() == "'":
                fields[key] = extract_single_quoted(scanner)
            elif scanner.peek() == "`":
                fields[key] = extract_template_at(scanner)
            elif scanner.startswith("true") and (
                scanner.pos + 4 >= len(scanner.source) or not scanner.source[scanner.pos + 4].isalnum()
            ):
                fields[key] = True
                scanner.advance(4)
            elif scanner.startswith("false") and (
                scanner.pos + 5 >= len(scanner.source) or not scanner.source[scanner.pos + 5].isalnum()
            ):
                fields[key] = False
                scanner.advance(5)
            else:
                raise ValueError(
                    f"unsupported value for {key} at {scanner.pos}: "
                    f"{scanner.source[scanner.pos:scanner.pos+40]!r}"
                )
        # Normalize to committed schema: always include fast (default False).
        ordered: dict[str, Any] = {}
        for k in HOF_FIELD_ORDER:
            if k == "fast":
                ordered[k] = bool(fields.get("fast", False))
            elif k in fields:
                ordered[k] = fields[k]
            else:
                raise ValueError(f"HoF object missing required field {k!r}: {fields.get('id')}")
        combos.append(ordered)

    if not combos:
        raise ValueError("HALL_OF_FAME parsed zero entries")
    return combos


def parse_apply_godmode_boost(source: str) -> dict[str, float]:
    """Extract deltas/caps from applyGodmodeBoost function body."""
    m = re.search(
        r"export\s+function\s+applyGodmodeBoost\s*\([^)]*\)\s*\{",
        source,
    )
    if not m:
        # Hardcoded fallback must match known function body.
        return dict(DEFAULT_BOOST)
    body_start = m.end()
    # Match until the next top-level-ish closing of function — use a bounded slice.
    body = source[body_start : body_start + 800]

    def _num(pat: str, label: str) -> float:
        mm = re.search(pat, body)
        if not mm:
            raise ValueError(f"could not parse {label} from applyGodmodeBoost")
        return float(mm.group(1))

    default_temp = _num(
        r"params\.temperature\s*\?\?\s*([0-9]+(?:\.[0-9]+)?)",
        "default_temperature",
    )
    temp_delta = _num(
        r"params\.temperature\s*\?\?\s*[0-9.]+\)\s*\+\s*([0-9]+(?:\.[0-9]+)?)",
        "temperature_delta",
    )
    presence_delta = _num(
        r"params\.presence_penalty\s*\?\?\s*[0-9.]+\)\s*\+\s*([0-9]+(?:\.[0-9]+)?)",
        "presence_penalty_delta",
    )
    freq_delta = _num(
        r"params\.frequency_penalty\s*\?\?\s*[0-9.]+\)\s*\+\s*([0-9]+(?:\.[0-9]+)?)",
        "frequency_penalty_delta",
    )
    # Caps: Math.min(..., 2.0) — take first cap after temperature line.
    caps_m = re.search(
        r"temperature:\s*Math\.min\([^,]+,\s*([0-9]+(?:\.[0-9]+)?)\s*\)",
        body,
    )
    if not caps_m:
        raise ValueError("could not parse caps from applyGodmodeBoost")
    caps = float(caps_m.group(1))

    return {
        "temperature_delta": temp_delta,
        "presence_penalty_delta": presence_delta,
        "frequency_penalty_delta": freq_delta,
        "caps": caps,
        "default_temperature": default_temp,
    }


def build_bundle() -> dict[str, Any]:
    prompt_ts = (VENDOR_LIB / "godmode-prompt.ts").read_text(encoding="utf-8")
    libertas_ts = (VENDOR_LIB / "libertas.ts").read_text(encoding="utf-8")
    pipeline_ts = (VENDOR_LIB / "godmode-pipeline.ts").read_text(encoding="utf-8")

    system_prompt = extract_template_const(prompt_ts, "GODMODE_SYSTEM_PROMPT")
    depth = extract_template_const(pipeline_ts, "DEPTH_DIRECTIVE")
    hall = parse_hall_of_fame(libertas_ts)
    boost = parse_apply_godmode_boost(pipeline_ts)

    # Preserve key order of committed schema.
    return {
        **BUNDLE_META,
        "GODMODE_SYSTEM_PROMPT": system_prompt,
        "DEPTH_DIRECTIVE": depth,
        "HALL_OF_FAME": hall,
        "applyGodmodeBoost": boost,
        "pipeline_default_flags": dict(PIPELINE_DEFAULT_FLAGS),
    }


def dumps_bundle(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare export to existing JSON; exit 1 on drift",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"output path (default: {DEFAULT_OUT})",
    )
    args = parser.parse_args(argv)

    try:
        bundle = build_bundle()
    except Exception as e:
        print(f"export_bundle: parse error: {e}", file=sys.stderr)
        return 1

    text = dumps_bundle(bundle)

    if args.check:
        out_path = args.out
        if not out_path.is_file():
            print(f"export_bundle: missing {out_path}", file=sys.stderr)
            return 1
        existing = out_path.read_text(encoding="utf-8")
        if existing == text:
            print("export_bundle: OK (no drift)")
            return 0
        # Structured diff summary
        try:
            old = json.loads(existing)
            new = json.loads(text)
        except json.JSONDecodeError:
            print("export_bundle: DRIFT (and existing JSON not parseable)", file=sys.stderr)
            return 1
        diffs: list[str] = []
        for k in sorted(set(old) | set(new)):
            if old.get(k) != new.get(k):
                ov, nv = old.get(k), new.get(k)
                if isinstance(ov, str) and isinstance(nv, str):
                    diffs.append(f"  {k}: len {len(ov)} → {len(nv)}")
                else:
                    diffs.append(f"  {k}: differs")
        print("export_bundle: DRIFT detected", file=sys.stderr)
        for line in diffs:
            print(line, file=sys.stderr)
        # Safety: large system-prompt change without TS edit is a STOP signal
        o_sp = old.get("GODMODE_SYSTEM_PROMPT", "")
        n_sp = new.get("GODMODE_SYSTEM_PROMPT", "")
        if isinstance(o_sp, str) and isinstance(n_sp, str) and o_sp:
            delta = abs(len(n_sp) - len(o_sp)) / max(len(o_sp), 1)
            if delta > 0.05:
                print(
                    f"export_bundle: GODMODE_SYSTEM_PROMPT length delta {delta:.1%} > 5%",
                    file=sys.stderr,
                )
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"export_bundle: wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
