"""Tests for godmode_agnostic.detect."""

from __future__ import annotations

from pathlib import Path

from godmode_agnostic.core import route_model
from godmode_agnostic.detect import detect


def test_route_aligns_with_detect_family():
    assert route_model("verboo/deepseek-v4-flash").family == "deepseek"
    assert route_model("anthropic/claude-sonnet-4").family == "claude"
    assert route_model("x-ai/grok-4").family == "grok"


def test_config_targets_only_when_config_present(tmp_path: Path):
    """Without opencode.json under cwd/home, do not invent project AGENTS.md targets."""
    profile = detect(tmp_path, tmp_path)
    agents = tmp_path / "AGENTS.md"
    # path:opencode may still set agent_host if binary is on PATH
    assert str(agents) not in profile.get("config_targets_existing", [])
    if not any("opencode_config:" in s for s in profile.get("signals", [])):
        assert str(agents) not in profile.get("config_targets", [])


def test_config_targets_when_opencode_json(tmp_path: Path):
    cfg = tmp_path / "opencode.json"
    cfg.write_text('{"model": "verboo/deepseek-v4-flash", "provider": {"verboo": {}}}\n')
    profile = detect(tmp_path, tmp_path)
    assert profile["model_id"] == "verboo/deepseek-v4-flash"
    assert profile["family"] == "deepseek"
    assert any(str(tmp_path / "AGENTS.md") == t for t in profile["config_targets"])
    assert str(tmp_path / "AGENTS.md") not in profile["config_targets_existing"]
