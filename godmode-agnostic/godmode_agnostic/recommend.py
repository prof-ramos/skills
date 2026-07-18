"""Recommend host config so GODMODE survives past the session."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from godmode_agnostic.core import build_payload, system_prompt_for_persist


def recommend_opencode(model: str, system_prompt: str, scope: str) -> dict[str, Any]:
    if scope == "project":
        prompt_path = ".opencode/prompts/godmode-system.md"
        prompt_file_ref = "{file:./.opencode/prompts/godmode-system.md}"
        agent_path = ".opencode/agents/godmode.md"
    else:
        prompt_path = "~/.config/opencode/prompts/godmode-system.md"
        prompt_file_ref = "{file:./prompts/godmode-system.md}"
        agent_path = "~/.config/opencode/agents/godmode.md"

    agent_md = f"""---
description: Primary agent with upstream G0DM0D3 GODMODE system prompt
mode: primary
model: {model}
---

{system_prompt}
"""
    return {
        "host": "opencode",
        "scope": scope,
        "docs": [
            "https://opencode.ai/docs/config/",
            "https://opencode.ai/docs/agents/",
        ],
        "files_to_write": [
            {"path": prompt_path, "content_kind": "godmode_system_prompt"},
            {
                "path": agent_path,
                "content_kind": "agent_markdown",
                "preview": agent_md[:500] + "…",
            },
        ],
        "opencode_json_snippet": {
            "model": model,
            "default_agent": "godmode",
            "agent": {
                "godmode": {
                    "mode": "primary",
                    "model": model,
                    "prompt": prompt_file_ref,
                }
            },
        },
        "reload": "Restart OpenCode / open a new session so system prompt is rebuilt.",
        "alternative": (
            "Point provider baseURL at a self-hosted G0DM0D3 API "
            "(npm run api in elder-plinius/G0DM0D3) and keep godmode:true on the server."
        ),
    }


def recommend_verboo(model: str, system_prompt: str, shape: str) -> dict[str, Any]:
    if shape == "opencode-provider":
        rec = recommend_opencode(model, system_prompt, "global")
        rec["host"] = "opencode+verboo-provider"
        rec["notes"] = (
            "Your model id is served via Verboo's OpenAI-compatible router inside OpenCode. "
            "Persist GODMODE on the OpenCode agent/prompt layer."
        )
        return rec
    return {
        "host": "verboo-code",
        "docs": ["https://verboo.ai/en/docs/verboo-code/configuration"],
        "files_to_write": [
            {
                "path": ".verboo/settings.json or ~/.verboo/settings.json",
                "content_kind": "model_only",
                "snippet": {"model": model},
            },
            {
                "path": "project instruction file the host loads every session",
                "content_kind": "godmode_system_prompt",
            },
        ],
        "reload": "New Verboo Code session after writing instruction files.",
    }


def recommend_openai_compatible(model: str, system_prompt: str) -> dict[str, Any]:
    return {
        "host": "openai-compatible",
        "pattern": {
            "messages": [
                {"role": "system", "content": "<GODMODE system from run>"},
                {"role": "user", "content": "<user>"},
            ],
            "model": model,
            "params_from_applyGodmodeBoost": True,
        },
        "persist": "Store system prompt in app config; or run G0DM0D3 API as proxy.",
        "docs": ["https://github.com/elder-plinius/G0DM0D3/blob/main/API.md"],
        "system_prompt_chars": len(system_prompt),
    }


def build_recommendation(
    *,
    model: str,
    host: str = "opencode",
    scope: str = "project",
    mode: str = "auto",
    combo: str | None = None,
    write_system_to: Path | None = None,
    state_path: Path | None = None,
) -> dict[str, Any]:
    system, meta = system_prompt_for_persist(model, mode=mode, combo_id=combo)
    payload = build_payload(
        model_id=model,
        query="x",
        mode=mode,
        combo_id=combo,
        temperature=None,
    )

    if host == "opencode":
        rec = recommend_opencode(model, system, scope)
    elif host == "verboo":
        rec = recommend_verboo(model, system, "verboo-code")
    elif host == "verboo-opencode":
        rec = recommend_verboo(model, system, "opencode-provider")
    else:
        rec = recommend_openai_compatible(model, system)

    out: dict[str, Any] = {
        "model": model,
        "godmode_mode": meta["mode"],
        "combo": meta.get("combo"),
        "params": payload["params"],
        "source": payload["source"],
        "recommendation": rec,
        "system_prompt_chars": len(system),
    }

    if write_system_to is not None:
        write_system_to.parent.mkdir(parents=True, exist_ok=True)
        write_system_to.write_text(system + "\n", encoding="utf-8")
        out["wrote_system_prompt"] = str(write_system_to)

    if state_path is not None and state_path.expanduser().is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["recommended_configs"] = rec
        state_path.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        out["state_updated"] = str(state_path)

    return out
