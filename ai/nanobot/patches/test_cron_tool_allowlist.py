"""Unit tests for cron tool allowlist (no nanobot install required)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
MOD_PATH = ROOT / "cron_tool_allowlist.py"


def _load_mod():
    spec = importlib.util.spec_from_file_location("cron_tool_allowlist", MOD_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cron_tool_allowlist"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def mod(tmp_path, monkeypatch):
    m = _load_mod()
    cfg = {
        "version": 1,
        "default_for_unlisted_cron_job": {"mcp_allow": []},
        "jobs": {
            "market-snapshot-open": {
                "mcp_allow": ["wv2_market_snapshot"],
                "force_args": {},
            },
            "eod-daily-report": {
                "mcp_allow": ["wv2_get_daily_activity_report"],
                "force_args": {
                    "wv2_get_daily_activity_report": {"fetch_only": True}
                },
            },
        },
    }
    path = tmp_path / "cron-tool-allowlist.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    monkeypatch.setenv("NANOBOT_CRON_TOOL_ALLOWLIST", str(path))
    m._CONFIG_CACHE = None
    m._CONFIG_MTIME = None
    m._CONFIG_PATH = None
    return m


def test_session_key_parse(mod):
    assert mod.cron_job_id_from_session_key("cron:market-snapshot-open") == "market-snapshot-open"
    assert mod.cron_job_id_from_session_key("telegram:-100") is None


def test_mcp_logical_name(mod):
    assert mod.mcp_logical_name("mcp_winston_wv2_market_snapshot") == "wv2_market_snapshot"
    assert mod.mcp_logical_name("mcp_winston_dm_get_cromwell_events") == "dm_get_cromwell_events"
    assert mod.mcp_logical_name("message") is None


def test_market_snapshot_allows_only_snapshot(mod):
    assert mod.is_mcp_allowed("market-snapshot-open", "mcp_winston_wv2_market_snapshot")
    assert not mod.is_mcp_allowed("market-snapshot-open", "mcp_winston_wv2_perform_daily_analysis")
    assert mod.is_mcp_allowed("market-snapshot-open", "message")  # non-MCP


def test_eod_force_fetch_only(mod):
    forced = mod.force_args_for("eod-daily-report", "wv2_get_daily_activity_report")
    assert forced.get("fetch_only") is True


def test_unknown_cron_denies_mcp(mod):
    assert not mod.is_mcp_allowed("brand-new-job", "mcp_winston_wv2_list_portfolios")
