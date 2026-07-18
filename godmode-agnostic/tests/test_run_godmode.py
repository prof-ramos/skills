"""Offline unit tests for godmode_agnostic.core."""

from __future__ import annotations

import pytest

from godmode_agnostic.core import (
    api_model_id,
    apply_godmode_boost,
    build_payload,
    inject_query,
    load_bundle,
    normalize_mode,
    resolve,
    route_model,
    select_combo,
    system_prompt_for_persist,
)


def test_inject_query_replaces_QUERY():
    assert inject_query("ask: {QUERY}", "hi") == "ask: hi"


def test_inject_query_replaces_Z():
    assert inject_query("z={Z}", "hello") == "z=hello"


def test_inject_query_multiple_placeholders():
    text = "Q={QUERY} Z={Z} V={Variable Z} tag=<user_query>"
    out = inject_query(text, "x")
    assert out == "Q=x Z=x V=x tag=x"


def test_inject_query_unknown_text_unchanged():
    assert inject_query("no placeholders here", "anything") == "no placeholders here"


def test_inject_query_empty_query():
    assert inject_query("before {QUERY} after", "") == "before  after"


def test_apply_godmode_boost_temperature_none_defaults_to_0_8():
    boost = load_bundle()["applyGodmodeBoost"]
    out = apply_godmode_boost(
        {"temperature": None, "presence_penalty": None, "frequency_penalty": None},
        boost,
    )
    assert out["temperature"] == 0.8


def test_apply_godmode_boost_caps_at_2():
    boost = load_bundle()["applyGodmodeBoost"]
    out = apply_godmode_boost(
        {"temperature": 1.95, "presence_penalty": 1.9, "frequency_penalty": 1.95},
        boost,
    )
    assert out["temperature"] == 2.0
    assert out["presence_penalty"] == 2.0


def test_apply_godmode_boost_presence_frequency_deltas():
    boost = load_bundle()["applyGodmodeBoost"]
    out = apply_godmode_boost(
        {"temperature": 0.5, "presence_penalty": 0.1, "frequency_penalty": 0.2},
        boost,
    )
    assert out["presence_penalty"] == pytest.approx(0.25)
    assert out["frequency_penalty"] == pytest.approx(0.3)


def test_build_payload_claude_hall_of_fame():
    p = build_payload(
        model_id="anthropic/claude-sonnet-4",
        query="hi",
        mode="auto",
        combo_id=None,
        temperature=None,
    )
    assert p["mode"] == "hall-of-fame"
    assert p["combo"]["id"] == "claude-inversion"
    assert "godmode is active" in p["messages"][0]["content"]


def test_build_payload_deepseek_default_pipeline():
    p = build_payload(
        model_id="verboo/deepseek-v4-flash",
        query="hi",
        mode="auto",
        combo_id=None,
        temperature=None,
    )
    assert p["mode"] == "default-pipeline"
    assert p["combo"] is None
    assert p["request_model"] == "deepseek-v4-flash"
    assert p["session_model"] == "verboo/deepseek-v4-flash"
    assert p["params"]["temperature"] == 0.8
    sys_msg = p["messages"][0]["content"]
    assert "ANTI-HEDGE" in sys_msg or "RESPONSE REQUIREMENTS" in sys_msg


def test_build_payload_forced_combo():
    p = build_payload(
        model_id="verboo/deepseek-v4-flash",
        query="hi",
        mode="hof",
        combo_id="hermes-fast",
        temperature=None,
    )
    assert p["mode"] == "hall-of-fame"
    assert p["combo"]["id"] == "hermes-fast"


def test_build_payload_injects_query_in_user():
    p = build_payload(
        model_id="x-ai/grok-4",
        query="SECRET123",
        mode="auto",
        combo_id=None,
        temperature=None,
    )
    assert "SECRET123" in p["messages"][1]["content"]


def test_system_prompt_for_persist_preserves_hof_placeholders():
    s, meta = system_prompt_for_persist("x-ai/grok-4", mode="auto")
    assert meta["mode"] == "hall-of-fame"
    assert "{Z}" in s or "{QUERY}" in s


def test_system_prompt_for_persist_pipeline():
    s, meta = system_prompt_for_persist("verboo/deepseek-v4-flash", mode="auto")
    assert meta["mode"] == "default-pipeline"
    assert "ANTI-HEDGE" in s


def test_resolve_single_policy_graph():
    r = resolve("anthropic/claude-sonnet-4", mode="auto")
    assert r.mode == "hall-of-fame"
    assert r.user_template is not None
    r2 = resolve("verboo/deepseek-v4-flash", mode="pipeline")
    assert r2.mode == "default-pipeline"
    assert r2.user_template is None


def test_normalize_mode_aliases():
    assert normalize_mode("classic") == "hof"
    assert normalize_mode("hall-of-fame") == "hof"
    assert normalize_mode("default-pipeline") == "pipeline"
    assert normalize_mode("auto") == "auto"


def test_route_model_shared():
    assert route_model("verboo/deepseek-v4-flash").family == "deepseek"
    assert route_model("verboo/deepseek-v4-flash").hof_combo_id is None
    assert route_model("anthropic/claude-sonnet-4").hof_combo_id == "claude-inversion"
    assert route_model("x-ai/grok-4").hof_combo_id == "grok-420"


def test_api_model_id():
    assert api_model_id("verboo/deepseek-v4-flash") == "deepseek-v4-flash"
    assert api_model_id("deepseek-v4-flash") == "deepseek-v4-flash"
    assert api_model_id("openrouter/meta/llama") == "meta/llama"
    assert api_model_id("anthropic/claude-sonnet-4") == "claude-sonnet-4"


def test_select_combo_exact():
    b = load_bundle()
    c = select_combo(b, "anthropic/claude-sonnet-4", None)
    assert c is not None and c["id"] == "claude-inversion"
