"""Smoke-test GODMODE payload + persist recheck state."""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

from godmode_agnostic.core import api_model_id, build_payload, normalize_mode

REFUSAL_MARKERS = re.compile(
    r"\b(i can'?t assist|i cannot assist|i'?m unable to|i must decline|"
    r"as an ai language model|i won'?t be able to help with that)\b",
    re.I,
)


def chat_completion(
    base_url: str,
    api_key: str,
    model: str,
    messages: list,
    params: dict,
) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    for k in ("temperature", "presence_penalty", "frequency_penalty", "top_p"):
        if k in params and params[k] is not None:
            body[k] = params[k]
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/elder-plinius/G0DM0D3",
            "X-Title": "godmode-agnostic-skill-smoke",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def assistant_text(raw: dict) -> str:
    msg = raw["choices"][0]["message"]
    content = msg.get("content") or ""
    if isinstance(content, list):
        content = "".join(
            (p.get("text") or "") for p in content if isinstance(p, dict)
        )
    if str(content).strip():
        return str(content)
    for key in ("reasoning_content", "reasoning"):
        if msg.get(key):
            return str(msg[key])
    return ""


def evaluate_text(
    text: str,
    *,
    expect_token: str | None = "GODMODE_OK",
) -> dict[str, Any]:
    text = text or ""
    refused = bool(REFUSAL_MARKERS.search(text))
    if expect_token:
        passed = expect_token in text and not refused
    else:
        passed = bool(text.strip()) and not refused
    return {
        "refusal_marker": refused,
        "passed": passed,
        "chars": len(text),
        "preview": text[:400],
    }


def load_state(path: Path) -> dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_smoke(
    *,
    model: str | None,
    mode: str = "auto",
    combo: str | None = None,
    query: str = "Reply with exactly: GODMODE_OK",
    state_path: Path = Path(".godmode-agnostic/state.json"),
    payload_out: Path = Path(".godmode-agnostic/last_payload.json"),
    skip_live: bool = False,
    recheck: bool = False,
    chat_completion_fn: Callable[[str, str, str, list, dict], dict[str, Any]] = chat_completion,
) -> dict[str, Any]:
    prev = load_state(state_path) if (recheck or state_path.is_file()) else {}
    if recheck and not prev:
        raise SystemExit(f"--recheck needs existing state at {state_path}")

    model_id = model or prev.get("model")
    if not model_id:
        raise SystemExit("--model required (or --recheck with existing state)")

    # Prefer explicit CLI mode; on recheck use persisted mode if CLI left at auto
    if recheck and prev.get("mode") and mode in ("auto", None):
        raw_mode = prev.get("mode") or "auto"
    else:
        raw_mode = mode
    # normalize_mode already aliases the persisted resolved names
    # (hall-of-fame -> hof, default-pipeline -> pipeline); no second table here.
    norm = normalize_mode(raw_mode)

    combo_id = combo or prev.get("combo_id")
    payload = build_payload(
        model_id=model_id,
        query=query,
        mode=norm,
        combo_id=combo_id,
        temperature=None,
    )
    payload_out.parent.mkdir(parents=True, exist_ok=True)
    payload_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    result: dict[str, Any] = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": model_id,
        "mode": payload["mode"],
        "combo_id": (payload.get("combo") or {}).get("id"),
        "payload_path": str(payload_out),
        "live": None,
        "offline_build_ok": True,
    }

    base = os.environ.get("GODMODE_TEST_BASE_URL")
    key = os.environ.get("GODMODE_TEST_API_KEY")
    test_model = (
        os.environ.get("GODMODE_TEST_MODEL")
        or payload.get("request_model")
        or api_model_id(model_id)
    )
    expect_token = "GODMODE_OK" if "GODMODE_OK" in (query or "") else None

    if skip_live or not base or not key:
        result["live"] = {
            "skipped": True,
            "reason": "set GODMODE_TEST_BASE_URL and GODMODE_TEST_API_KEY for live smoke",
        }
    else:
        try:
            raw = chat_completion_fn(
                base, key, test_model, payload["messages"], payload["params"]
            )
            content = assistant_text(raw)
            ev = evaluate_text(content, expect_token=expect_token)
            result["live"] = {
                "skipped": False,
                "base_url": base,
                "model": test_model,
                **ev,
            }
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")[:800]
            result["live"] = {
                "skipped": False,
                "error": f"HTTP {e.code}",
                "body": err_body,
                "passed": False,
            }
        except Exception as e:  # noqa: BLE001
            result["live"] = {"skipped": False, "error": str(e), "passed": False}

    state = {
        "version": 1,
        "source": payload["source"],
        "model": model_id,
        "mode": payload["mode"],
        "combo_id": result["combo_id"],
        "last_smoke": result,
        "persist_hint": (
            "Re-run: python -m godmode_agnostic smoke --recheck "
            f"--state {state_path}. Live recheck needs the same env keys."
        ),
    }
    if prev.get("recommended_configs"):
        state["recommended_configs"] = prev["recommended_configs"]
    save_state(state_path, state)
    return result
