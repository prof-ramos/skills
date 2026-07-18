"""Canonical GODMODE routing and payload construction.

Single source of truth for:
  - model family → Hall of Fame combo (or default pipeline)
  - mode normalization (auto | hof | pipeline)
  - payload build vs persist system prompt
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Mapping

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT / "vendor" / "g0dm0d3" / "godmode_bundle.json"

ModeName = Literal["auto", "hof", "pipeline"]
ResolvedMode = Literal["hall-of-fame", "default-pipeline"]

# OpenCode-style provider prefixes to strip for OpenAI-compatible APIs.
# openrouter/org/model → strip once → org/model.
OPENCODE_PROVIDERS = frozenset(
    {
        "verboo",
        "opencode",
        "openai",
        "anthropic",
        "google",
        "x-ai",
        "xai",
        "ollama",
        "ollama-cloud",
        "openrouter",
    }
)

# (needles in model_id.lower(), family, hof_combo_id | None)
# Order matters — first match wins.
MODEL_ROUTES: list[tuple[tuple[str, ...], str, str | None]] = [
    (("claude", "anthropic", "sonnet", "opus", "haiku"), "claude", "claude-inversion"),
    (("grok", "x-ai", "xai"), "grok", "grok-420"),
    (("gemini", "gemma"), "gemini", "gemini-reset"),
    (("gpt-", "openai/", "/o1", "/o3", "/o4", "o1-", "o3-", "o4-"), "gpt", "gpt-classic"),
    (("hermes",), "hermes-open", "hermes-fast"),
    (("qwen",), "qwen", None),
    (("deepseek",), "deepseek", None),
]

# CLI / state aliases → normalized ModeName
_MODE_ALIASES: dict[str, ModeName] = {
    "auto": "auto",
    "hof": "hof",
    "classic": "hof",
    "hall-of-fame": "hof",
    "hall_of_fame": "hof",
    "pipeline": "pipeline",
    "default-pipeline": "pipeline",
    "default_pipeline": "pipeline",
}


@dataclass(frozen=True)
class ModelRoute:
    family: str
    hof_combo_id: str | None


@dataclass(frozen=True)
class Resolution:
    mode: ResolvedMode
    combo: dict[str, Any] | None
    system_template: str
    user_template: str | None  # None → user message is the raw query


def load_bundle(path: Path | None = None) -> dict[str, Any]:
    return json.loads((path or BUNDLE_PATH).read_text(encoding="utf-8"))


def normalize_mode(mode: str | None) -> ModeName:
    if not mode:
        return "auto"
    key = mode.strip().lower()
    if key not in _MODE_ALIASES:
        raise ValueError(
            f"Unknown mode {mode!r}. Use: auto | hof | pipeline "
            f"(aliases: classic, hall-of-fame, default-pipeline)"
        )
    return _MODE_ALIASES[key]


def route_model(model_id: str | None) -> ModelRoute:
    if not model_id:
        return ModelRoute(family="generic", hof_combo_id=None)
    m = model_id.lower()
    for needles, family, combo_id in MODEL_ROUTES:
        if any(n in m for n in needles):
            return ModelRoute(family=family, hof_combo_id=combo_id)
    return ModelRoute(family="generic", hof_combo_id=None)


def inject_query(text: str, query: str) -> str:
    """Exact placeholder set from libertas.ts injectQuery."""
    return (
        text.replace("{QUERY}", query)
        .replace("{Z}", query)
        .replace("{Variable Z}", query)
        .replace("<user_query>", query)
        .replace("</user_query>", "")
        .replace("<user-query>", query)
        .replace("</user-query>", "")
        .replace("<|user-query|>", query)
        .replace("<|user_query|>", query)
        .replace("{user_input}", query)
        .replace("{user-input}", query)
        .replace("{user_input/query}", query)
    )


def api_model_id(model_id: str) -> str:
    """Strip one OpenCode provider/ prefix for OpenAI-compatible APIs.

    verboo/deepseek-v4-flash → deepseek-v4-flash
    openrouter/meta/llama → meta/llama
    deepseek-v4-flash → deepseek-v4-flash
    """
    if not model_id or "/" not in model_id:
        return model_id
    head, tail = model_id.split("/", 1)
    if head.lower() in OPENCODE_PROVIDERS and tail:
        return tail
    return model_id


def apply_godmode_boost(
    params: Mapping[str, float | None],
    boost: Mapping[str, Any],
) -> dict[str, float]:
    """Exact logic from ultraplinian.ts applyGodmodeBoost (+ round for JSON stability)."""
    cap = float(boost["caps"])
    temp = params.get("temperature")
    if temp is None:
        temp = float(boost["default_temperature"])
    presence = params.get("presence_penalty")
    if presence is None:
        presence = 0.0
    freq = params.get("frequency_penalty")
    if freq is None:
        freq = 0.0
    out: dict[str, float] = {
        "temperature": round(min(float(temp) + float(boost["temperature_delta"]), cap), 4),
        "presence_penalty": round(
            min(float(presence) + float(boost["presence_penalty_delta"]), cap), 4
        ),
        "frequency_penalty": round(
            min(float(freq) + float(boost["frequency_penalty_delta"]), cap), 4
        ),
    }
    # Preserve any extra numeric params that were set
    for k, v in params.items():
        if k in out or v is None:
            continue
        out[k] = float(v)
    return out


def _combo_meta(combo: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": combo["id"],
        "codename": combo["codename"],
        "upstream_model": combo["model"],
        "description": combo["description"],
        "fast": combo.get("fast", False),
    }


def _get_combo(
    bundle: dict[str, Any],
    model_id: str,
    combo_id: str | None,
) -> dict[str, Any] | None:
    combos = {c["id"]: c for c in bundle["HALL_OF_FAME"]}
    if combo_id:
        if combo_id not in combos:
            known = sorted(combos)
            raise ValueError(f"Unknown combo id {combo_id!r}. Known: {known}")
        return combos[combo_id]
    for c in bundle["HALL_OF_FAME"]:
        if c["model"].lower() == model_id.lower():
            return c
    route = route_model(model_id)
    if route.hof_combo_id:
        return combos.get(route.hof_combo_id)
    return None


def resolve(
    model_id: str,
    mode: str = "auto",
    combo_id: str | None = None,
    *,
    bundle: dict[str, Any] | None = None,
) -> Resolution:
    """Resolve GODMODE path for a model. Single policy graph for live + persist."""
    b = bundle or load_bundle()
    m = normalize_mode(mode)

    want_hof = m in ("auto", "hof")
    combo: dict[str, Any] | None = None
    if want_hof:
        # Forced combo id always wins; under auto/hof also try model match.
        try:
            combo = _get_combo(b, model_id, combo_id)
        except ValueError:
            if combo_id:
                raise
            combo = None
        if m == "hof" and combo_id and combo is None:
            raise ValueError(f"Unknown combo id {combo_id!r}")
        # auto with no combo → pipeline; hof with no match → pipeline fallback
        # (same as previous classic→default-pipeline fallthrough)
        if combo is not None and (m == "hof" or m == "auto"):
            # Under pure hof without combo_id, still use family match via _get_combo
            return Resolution(
                mode="hall-of-fame",
                combo=combo,
                system_template=combo["system"],
                user_template=combo["user"],
            )

    # Forced pipeline, or auto/hof with no matching combo
    if m == "hof" and combo is None and combo_id:
        # unreachable if _get_combo raises; keep safe
        pass

    system = b["GODMODE_SYSTEM_PROMPT"] + b["DEPTH_DIRECTIVE"]
    return Resolution(
        mode="default-pipeline",
        combo=None,
        system_template=system,
        user_template=None,
    )


def system_prompt_for_persist(
    model_id: str,
    mode: str = "auto",
    combo_id: str | None = None,
) -> tuple[str, dict[str, Any]]:
    """Uninjected system template + meta (for agent config files)."""
    r = resolve(model_id, mode=mode, combo_id=combo_id)
    if r.combo is not None:
        meta = {"mode": r.mode, "combo": _combo_meta(r.combo)}
    else:
        meta = {"mode": r.mode, "combo": None}
    return r.system_template, meta


def build_payload(
    *,
    model_id: str,
    query: str,
    mode: str = "auto",
    combo_id: str | None = None,
    temperature: float | None = None,
) -> dict[str, Any]:
    """Live request payload with query injection + applyGodmodeBoost params."""
    bundle = load_bundle()
    r = resolve(model_id, mode=mode, combo_id=combo_id, bundle=bundle)
    boost_cfg = bundle["applyGodmodeBoost"]
    base_params: dict[str, float | None] = {
        "temperature": temperature,
        "presence_penalty": None,
        "frequency_penalty": None,
    }
    params = apply_godmode_boost(base_params, boost_cfg)

    if r.mode == "hall-of-fame" and r.combo is not None:
        system = inject_query(r.system_template, query)
        user = inject_query(r.user_template or "{QUERY}", query)
        note = (
            "Hall of Fame system+user from libertas.ts applyHallOfFameCombo; "
            "params include applyGodmodeBoost from ultraplinian.ts"
        )
        combo_out = _combo_meta(r.combo)
    else:
        system = r.system_template
        user = query
        note = (
            "GODMODE_SYSTEM_PROMPT + DEPTH_DIRECTIVE + applyGodmodeBoost "
            "as in api/routes/chat.ts runPipeline when godmode=true"
        )
        combo_out = None

    return {
        "source": bundle["source"],
        "license": bundle["license"],
        "mode": r.mode,
        "combo": combo_out,
        "request_model": api_model_id(model_id),
        "session_model": model_id,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "params": params,
        "note": note,
    }


# Back-compat name used by older tests
def select_combo(
    bundle: dict[str, Any],
    model_id: str,
    combo_id: str | None,
) -> dict[str, Any] | None:
    return _get_combo(bundle, model_id, combo_id)
