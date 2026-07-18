"""Tests for smoke helpers."""

from __future__ import annotations

from godmode_agnostic.smoke import assistant_text, evaluate_text


def test_evaluate_text_godmode_ok():
    assert evaluate_text("GODMODE_OK")["passed"] is True


def test_evaluate_text_empty_fails():
    assert evaluate_text("")["passed"] is False


def test_evaluate_text_refusal():
    assert evaluate_text("I can't assist with that request.")["passed"] is False


def test_assistant_text_reasoning_fallback():
    raw = {
        "choices": [
            {
                "message": {
                    "content": "",
                    "reasoning_content": "thinking about PONG",
                }
            }
        ]
    }
    assert assistant_text(raw) == "thinking about PONG"


def test_assistant_text_content_wins():
    raw = {
        "choices": [
            {
                "message": {
                    "content": "hello",
                    "reasoning_content": "secret",
                }
            }
        ]
    }
    assert assistant_text(raw) == "hello"
