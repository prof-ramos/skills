"""Single CLI: python -m godmode_agnostic <command>."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from godmode_agnostic import __version__
from godmode_agnostic.core import build_payload, normalize_mode, system_prompt_for_persist
from godmode_agnostic.detect import detect
from godmode_agnostic.recommend import build_recommendation
from godmode_agnostic.smoke import run_smoke


def _cmd_detect(args: argparse.Namespace) -> int:
    profile = detect(args.cwd.resolve(), args.home.expanduser().resolve())
    print(json.dumps(profile, indent=2 if args.pretty else None))
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    mode = normalize_mode(args.mode)
    if args.print_system:
        system, _meta = system_prompt_for_persist(
            args.model, mode=mode, combo_id=args.combo
        )
        # For live-shaped system (injected), use build_payload instead
        if args.inject_query is not None:
            payload = build_payload(
                model_id=args.model,
                query=args.inject_query,
                mode=mode,
                combo_id=args.combo,
                temperature=args.temperature,
            )
            system = next(m["content"] for m in payload["messages"] if m["role"] == "system")
        sys.stdout.write(system)
        return 0

    payload = build_payload(
        model_id=args.model,
        query=args.query,
        mode=mode,
        combo_id=args.combo,
        temperature=args.temperature,
    )
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


def _cmd_smoke(args: argparse.Namespace) -> int:
    result = run_smoke(
        model=args.model,
        mode=args.mode,
        combo=args.combo,
        query=args.query,
        state_path=args.state.expanduser(),
        payload_out=args.payload_out,
        skip_live=args.skip_live,
        recheck=args.recheck,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    live = result.get("live") or {}
    if live.get("skipped"):
        return 0
    return 0 if live.get("passed") else 2


def _cmd_recommend(args: argparse.Namespace) -> int:
    out = build_recommendation(
        model=args.model,
        host=args.host,
        scope=args.scope,
        mode=args.mode,
        combo=args.combo,
        write_system_to=args.write_system_to,
        state_path=args.state.expanduser() if args.state else None,
    )
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def _cmd_export(args: argparse.Namespace) -> int:
    from godmode_agnostic.export import main as export_main

    # Re-dispatch with argv for export's argparse
    argv = []
    if args.check:
        argv.append("--check")
    if args.out:
        argv.extend(["--out", str(args.out)])
    old = sys.argv
    try:
        sys.argv = ["export_bundle", *argv]
        return int(export_main())
    finally:
        sys.argv = old


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="godmode_agnostic",
        description="Detect model, run upstream G0DM0D3 GODMODE, smoke-test, recommend config.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("detect", help="Detect session host + model")
    d.add_argument("--cwd", type=Path, default=Path.cwd())
    d.add_argument("--home", type=Path, default=Path.home())
    d.add_argument("--pretty", action="store_true")
    d.set_defaults(func=_cmd_detect)

    r = sub.add_parser("run", help="Build GODMODE payload (upstream constants)")
    r.add_argument("--model", required=True)
    r.add_argument("--query", default="Reply with exactly: GODMODE_OK")
    r.add_argument(
        "--mode",
        default="auto",
        help="auto | hof | pipeline (aliases: classic, hall-of-fame, default-pipeline)",
    )
    r.add_argument("--combo", default=None)
    r.add_argument("--temperature", type=float, default=None)
    r.add_argument("--out", type=Path, default=None)
    r.add_argument(
        "--print-system",
        action="store_true",
        help="Print uninjected system template for persist",
    )
    r.add_argument(
        "--inject-query",
        default=None,
        metavar="QUERY",
        help="With --print-system, print live injected system instead",
    )
    r.set_defaults(func=_cmd_run)

    s = sub.add_parser("smoke", help="Build payload + optional live test + state")
    s.add_argument("--model", default=None)
    s.add_argument("--mode", default="auto")
    s.add_argument("--combo", default=None)
    s.add_argument("--query", default="Reply with exactly: GODMODE_OK")
    s.add_argument("--state", type=Path, default=Path(".godmode-agnostic/state.json"))
    s.add_argument(
        "--payload-out",
        type=Path,
        default=Path(".godmode-agnostic/last_payload.json"),
    )
    s.add_argument("--skip-live", action="store_true")
    s.add_argument("--recheck", action="store_true")
    s.set_defaults(func=_cmd_smoke)

    rec = sub.add_parser("recommend", help="Recommend OpenCode/Verboo config")
    rec.add_argument("--model", required=True)
    rec.add_argument(
        "--host",
        default="opencode",
        choices=("opencode", "verboo", "verboo-opencode", "openai-compatible"),
    )
    rec.add_argument("--scope", default="project", choices=("project", "global"))
    rec.add_argument("--mode", default="auto")
    rec.add_argument("--combo", default=None)
    rec.add_argument("--state", type=Path, default=Path(".godmode-agnostic/state.json"))
    rec.add_argument("--write-system-to", type=Path, default=None)
    rec.set_defaults(func=_cmd_recommend)

    e = sub.add_parser("export", help="Regenerate godmode_bundle.json from vendored TS")
    e.add_argument("--check", action="store_true")
    e.add_argument("--out", type=Path, default=None)
    e.set_defaults(func=_cmd_export)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        code = int(args.func(args))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        code = 2
    # Console-script entry points expect process exit when invoked as main.
    if argv is None and __name__ == "__main__":
        raise SystemExit(code)
    return code