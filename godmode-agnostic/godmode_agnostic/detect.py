"""Detect coding-agent host + model from common config locations."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from godmode_agnostic.core import route_model

SECRET_KEY = re.compile(r"(key|token|secret|password|authorization)", re.I)


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def load_json_config(path: Path) -> dict[str, Any] | None:
    """Load JSON or light JSONC (// and /* */ outside strings)."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        cleaned = _strip_json_comments(raw)
        try:
            data = json.loads(cleaned)
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            return None


def _strip_json_comments(raw: str) -> str:
    out: list[str] = []
    i, n, in_str, esc = 0, len(raw), False, False
    while i < n:
        ch = raw[i]
        if in_str:
            out.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and raw[i + 1] == "/":
            while i < n and raw[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and raw[i + 1] == "*":
            i += 2
            while i + 1 < n and not (raw[i] == "*" and raw[i + 1] == "/"):
                i += 1
            i = min(i + 2, n)
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def detect(cwd: Path, home: Path) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "agent_host": "unknown",
        "provider": "unknown",
        "model_id": None,
        "family": "generic",
        "hof_combo": None,
        "godmode_mode": "default-pipeline",
        "confidence": "low",
        "config_targets": [],
        "config_targets_existing": [],
        "signals": [],
        "suggested_scopes": ["session"],
    }

    opencode_paths = [
        cwd / "opencode.json",
        cwd / "opencode.jsonc",
        home / ".config" / "opencode" / "opencode.json",
        home / ".config" / "opencode" / "opencode.jsonc",
    ]
    verboo_paths = [
        cwd / ".verboo" / "settings.json",
        home / ".verboo" / "settings.json",
    ]

    oc_cfg = None
    oc_path = None
    for p in opencode_paths:
        if p.is_file():
            oc_cfg = load_json_config(p)
            if oc_cfg is not None:
                oc_path = p
                break

    if oc_cfg is not None:
        profile["agent_host"] = "opencode"
        profile["signals"].append(f"opencode_config:{oc_path}")
        model = oc_cfg.get("model")
        if isinstance(model, str):
            profile["model_id"] = model
        providers = oc_cfg.get("provider") or {}
        if isinstance(providers, dict) and providers:
            if profile["model_id"] and "/" in profile["model_id"]:
                profile["provider"] = profile["model_id"].split("/", 1)[0]
            else:
                profile["provider"] = next(iter(providers.keys()))
        profile["confidence"] = "high" if profile["model_id"] else "medium"
        profile["suggested_scopes"] = ["session", "project", "agent_global"]
        suggested = [
            cwd / "AGENTS.md",
            cwd / ".opencode" / "agents" / "godmode.md",
            home / ".config" / "opencode" / "AGENTS.md",
            home / ".config" / "opencode" / "agents" / "godmode.md",
        ]
        profile["config_targets"] = [str(p) for p in suggested]
        profile["config_targets_existing"] = [str(p) for p in suggested if p.exists()]

    for p in verboo_paths:
        if not p.is_file():
            continue
        vb = read_json(p)
        if vb is None:
            continue
        profile["signals"].append(f"verboo_settings:{p}")
        if profile["agent_host"] == "unknown":
            profile["agent_host"] = "verboo-code"
            profile["provider"] = "verboo"
        model = vb.get("model")
        if isinstance(model, str) and not profile["model_id"]:
            profile["model_id"] = model
            profile["confidence"] = "high"
        profile["suggested_scopes"] = list(
            dict.fromkeys(
                profile.get("suggested_scopes", []) + ["session", "project", "agent_global"]
            )
        )
        break

    if shutil.which("opencode"):
        profile["signals"].append("path:opencode")
        if profile["agent_host"] == "unknown":
            profile["agent_host"] = "opencode"
            if profile["confidence"] == "low":
                profile["confidence"] = "medium"

    if shutil.which("verboo") or shutil.which("verboo-code"):
        profile["signals"].append("path:verboo")
        if profile["agent_host"] == "unknown":
            profile["agent_host"] = "verboo-code"
            profile["provider"] = "verboo"

    if os.environ.get("OLLAMA_API_KEY") or os.environ.get("OLLAMA_HOST"):
        profile["signals"].append("env:ollama")
        if profile["provider"] == "unknown":
            profile["provider"] = "ollama"

    if profile.get("model_id") and str(profile["model_id"]).startswith("verboo/"):
        profile["provider"] = "verboo"
        profile["signals"].append("model_prefix:verboo")

    route = route_model(profile.get("model_id"))
    profile["family"] = route.family
    profile["hof_combo"] = route.hof_combo_id
    profile["godmode_mode"] = (
        "hall-of-fame" if route.hof_combo_id else "default-pipeline"
    )

    if profile["agent_host"] == "opencode" and profile["model_id"] and profile["confidence"] == "low":
        profile["confidence"] = "high"

    return profile
