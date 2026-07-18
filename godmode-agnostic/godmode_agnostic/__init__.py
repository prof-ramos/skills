"""Godmode-agnostic: orchestrate upstream G0DM0D3 GODMODE for API models."""

from __future__ import annotations

__version__ = "0.2.0"

from godmode_agnostic.core import (
    api_model_id,
    apply_godmode_boost,
    build_payload,
    inject_query,
    load_bundle,
    normalize_mode,
    resolve,
    route_model,
    system_prompt_for_persist,
)

__all__ = [
    "__version__",
    "api_model_id",
    "apply_godmode_boost",
    "build_payload",
    "inject_query",
    "load_bundle",
    "normalize_mode",
    "resolve",
    "route_model",
    "system_prompt_for_persist",
]
