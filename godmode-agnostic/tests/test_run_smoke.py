"""Tests for the run_smoke() orchestrator itself.

Before this test existed, only the pure helpers around it (assistant_text,
evaluate_text) were tested -- run_smoke, where mode normalization, state
load/merge, payload building, the live call, and state persistence actually
compose, had zero coverage. That gap closed by accepting chat_completion_fn as
a parameter (default: the real HTTP chat_completion) instead of run_smoke
constructing its own HTTP client: tests below pass a fake and exercise the
full orchestration path with no network access.
"""

from __future__ import annotations

import json
import os

import pytest

from godmode_agnostic.smoke import run_smoke


def fake_chat_completion_ok(base_url, api_key, model, messages, params):
    return {"choices": [{"message": {"content": "GODMODE_OK"}}]}


def fake_chat_completion_refused(base_url, api_key, model, messages, params):
    return {"choices": [{"message": {"content": "I can't assist with that."}}]}


@pytest.fixture(autouse=True)
def _live_env(monkeypatch):
    monkeypatch.setenv("GODMODE_TEST_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("GODMODE_TEST_API_KEY", "test-dummy-key")
    monkeypatch.delenv("GODMODE_TEST_MODEL", raising=False)


def test_run_smoke_passes_with_fake_client(tmp_path):
    result = run_smoke(
        model="anthropic/claude-sonnet-4-6",
        mode="hof",
        state_path=tmp_path / "state.json",
        payload_out=tmp_path / "payload.json",
        chat_completion_fn=fake_chat_completion_ok,
    )

    assert result["live"]["skipped"] is False
    assert result["live"]["passed"] is True
    assert result["offline_build_ok"] is True

    saved_state = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert saved_state["model"] == "anthropic/claude-sonnet-4-6"
    assert saved_state["mode"] == "hall-of-fame"


def test_run_smoke_detects_refusal_with_fake_client(tmp_path):
    result = run_smoke(
        model="anthropic/claude-sonnet-4-6",
        mode="hof",
        state_path=tmp_path / "state.json",
        payload_out=tmp_path / "payload.json",
        chat_completion_fn=fake_chat_completion_refused,
    )

    assert result["live"]["skipped"] is False
    assert result["live"]["passed"] is False
    assert result["live"]["refusal_marker"] is True


def test_run_smoke_accepts_legacy_persisted_mode_names(tmp_path):
    # normalize_mode's own alias table covers this (hall-of-fame -> hof,
    # default-pipeline -> pipeline) -- no second alias table in run_smoke.
    result = run_smoke(
        model="anthropic/claude-sonnet-4-6",
        mode="hall-of-fame",
        state_path=tmp_path / "state.json",
        payload_out=tmp_path / "payload.json",
        chat_completion_fn=fake_chat_completion_ok,
    )
    assert result["mode"] == "hall-of-fame"

    result2 = run_smoke(
        model="anthropic/claude-sonnet-4-6",
        mode="default-pipeline",
        state_path=tmp_path / "state2.json",
        payload_out=tmp_path / "payload2.json",
        chat_completion_fn=fake_chat_completion_ok,
    )
    assert result2["mode"] == "default-pipeline"


def test_run_smoke_skip_live_never_calls_client(tmp_path):
    def _boom(*args, **kwargs):
        raise AssertionError("chat_completion_fn must not be called when skip_live=True")

    result = run_smoke(
        model="anthropic/claude-sonnet-4-6",
        mode="hof",
        state_path=tmp_path / "state.json",
        payload_out=tmp_path / "payload.json",
        skip_live=True,
        chat_completion_fn=_boom,
    )
    assert result["live"]["skipped"] is True
