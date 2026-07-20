"""Unit tests for cron duty guards (no nanobot install required)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

ROOT = Path(__file__).resolve().parent
MOD_PATH = ROOT / "cron_tool_allowlist.py"


def _load_mod():
    # Fresh module each fixture — avoid sticky ContextVars / install flags across tests.
    name = "cron_tool_allowlist_under_test"
    sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(name, MOD_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def mod(tmp_path, monkeypatch):
    m = _load_mod()
    cfg = {
        "version": 1,
        "defaults": {"identical_fail_limit": 2},
        "default_for_unlisted_cron_job": {"mcp_allow": []},
        "jobs": {
            "market-snapshot-open": {
                "mcp_allow": ["wv2_market_snapshot"],
                "mcp_require": ["wv2_market_snapshot"],
                "builtin_deny": ["read_file", "write_file", "edit_file"],
                "force_args": {},
                "identical_fail_limit": 2,
            },
            "market-snapshot-hourly": {
                "mcp_allow": ["wv2_market_snapshot"],
                "mcp_require": ["wv2_market_snapshot"],
                "builtin_deny": ["read_file", "write_file", "edit_file"],
                "force_args": {},
            },
            "eod-daily-report": {
                "mcp_allow": ["wv2_get_daily_activity_report"],
                "mcp_require": ["wv2_get_daily_activity_report"],
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
    m.reset_turn_state()
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
    assert mod.is_mcp_allowed("market-snapshot-open", "message")  # non-MCP unless builtin_deny


def test_builtin_deny_read_file(mod):
    assert mod.is_builtin_denied("market-snapshot-hourly", "read_file")
    assert not mod.is_builtin_denied("market-snapshot-hourly", "message")
    assert not mod.is_builtin_denied("market-snapshot-hourly", "mcp_winston_wv2_market_snapshot")


def test_eod_force_fetch_only(mod):
    forced = mod.force_args_for("eod-daily-report", "wv2_get_daily_activity_report")
    assert forced.get("fetch_only") is True


def test_unknown_cron_denies_mcp(mod):
    assert not mod.is_mcp_allowed("brand-new-job", "mcp_winston_wv2_list_portfolios")


def test_placeholder_paths(mod):
    assert mod.is_placeholder_path("path/to/file.txt")
    assert mod.is_placeholder_path("/path/to/file.txt")
    assert mod.is_placeholder_path("path/to/your/file.txt")
    assert not mod.is_placeholder_path("memory/MEMORY.md")
    assert not mod.is_placeholder_path("skills/winston-market-snapshot/SKILL.md")


def test_path_ask_detector(mod):
    assert mod.looks_like_path_ask(
        "It seems that the file path/to/file.txt was not found. "
        "Could you please provide the correct file path so I can attempt reading the file again?"
    )
    assert not mod.looks_like_path_ask(
        "Active books well inside 1× ATR of prior close — nothing asking for attention."
    )


def test_required_mcp_set(mod):
    assert mod.required_mcp_set("market-snapshot-hourly") == {"wv2_market_snapshot"}
    assert mod.required_mcp_set("brand-new-job") == set()


def test_enforce_final_missing_mcp(mod):
    mod.reset_turn_state()
    out = mod.enforce_cron_final_content(
        "Markets look stable with no movers today.",
        session_key="cron:market-snapshot-hourly",
    )
    assert out is not None
    assert out.startswith("OPS ERROR:")
    assert "wv2_market_snapshot" in out
    assert "stable" not in out.lower() or "OPS ERROR" in out


def test_enforce_final_ok_after_mcp(mod):
    mod.reset_turn_state()
    mod._get_ok_mcp().add("wv2_market_snapshot")
    quiet = "Active books are well inside 1× ATR of prior close — nothing asking for attention yet."
    out = mod.enforce_cron_final_content(quiet, session_key="cron:market-snapshot-hourly")
    assert out == quiet


def test_enforce_final_path_ask_suppressed(mod):
    mod.reset_turn_state()
    mod._get_ok_mcp().add("wv2_market_snapshot")
    ask = (
        "It seems that the file path/to/file.txt was not found. "
        "Could you please provide the correct file path?"
    )
    out = mod.enforce_cron_final_content(ask, session_key="cron:market-snapshot-hourly")
    assert out is not None
    assert out.startswith("OPS ERROR:")
    assert "path-ask" in out.lower() or "path" in out.lower()


def test_enforce_final_non_cron_passthrough(mod):
    text = "Could you please provide the correct file path?"
    assert (
        mod.enforce_cron_final_content(text, session_key="telegram:-1003884714483") == text
    )


def test_circuit_break_signature(mod):
    a = mod.call_signature("read_file", {"path": "path/to/file.txt"})
    b = mod.call_signature("read_file", {"path": "path/to/file.txt"})
    c = mod.call_signature("read_file", {"path": "memory/MEMORY.md"})
    assert a == b
    assert a != c


def test_identical_fail_limit(mod):
    assert mod.identical_fail_limit("market-snapshot-open") == 2
    assert mod.identical_fail_limit("unknown-job") == 2


@pytest.mark.asyncio
async def test_execute_circuit_break_identical_failures(mod, monkeypatch):
    """After N identical Error results, execute returns CIRCUIT_BREAK (no retry spiral)."""

    class FakeRegistry:
        def __init__(self):
            self.calls = 0

        def prepare_call(self, name, params):
            return SimpleNamespace(name=name), params, None

        async def execute_original(self, name, params):
            self.calls += 1
            return f"Error: File not found: {params.get('path')}"

    # Minimal install without nanobot imports for execute wrap logic.
    # Exercise counters the same way install's execute does.
    mod.reset_turn_state()
    job_id = "market-snapshot-hourly"
    name = "read_file"
    params = {"path": "path/to/file.txt"}
    sig = mod.call_signature(name, params)
    limit = mod.identical_fail_limit(job_id)

    results = []
    for _ in range(limit + 1):
        counts = mod._get_fail_counts()
        if counts.get(sig, 0) >= limit:
            results.append(mod.circuit_break_message(job_id, name, counts[sig]))
            continue
        # Simulate error result
        counts[sig] = counts.get(sig, 0) + 1
        if counts[sig] >= limit:
            results.append(mod.circuit_break_message(job_id, name, counts[sig]))
        else:
            results.append("Error: File not found: path/to/file.txt")

    assert any("CIRCUIT_BREAK" in r for r in results)
    # Trips on the Nth identical failure (limit=2 → second failure)
    assert results[1].startswith("Error: CIRCUIT_BREAK")
    assert results[2].startswith("Error: CIRCUIT_BREAK")


def test_install_patches_registry(mod, monkeypatch):
    """install() wraps prepare_call/execute and is idempotent."""

    class ToolRegistry:
        _tools = {}

        def prepare_call(self, name, params):
            return object(), params, None

        def get_definitions(self):
            return [
                {"function": {"name": "mcp_winston_wv2_market_snapshot"}},
                {"function": {"name": "mcp_winston_wv2_perform_daily_analysis"}},
                {"function": {"name": "read_file"}},
                {"function": {"name": "message"}},
            ]

        async def execute(self, name, params):
            return "ok-payload"

        @staticmethod
        def _schema_name(schema):
            fn = schema.get("function") or {}
            return fn.get("name") or ""

    # Avoid progress-hook import failure in bare env
    monkeypatch.setattr(mod, "_install_progress_hook_guards", lambda: None)

    session = {"key": "cron:market-snapshot-hourly"}

    def fake_session_key():
        return session["key"]

    monkeypatch.setattr(mod, "_session_key", fake_session_key)

    mod.install(ToolRegistry)
    assert ToolRegistry._sawtooth_cron_allowlist_installed is True

    reg = ToolRegistry()
    # Forbidden MCP
    tool, params, err = reg.prepare_call(
        "mcp_winston_wv2_perform_daily_analysis", {}
    )
    assert err is not None
    assert "not allowed" in err

    # Denied builtin
    tool, params, err = reg.prepare_call("read_file", {"path": "memory/MEMORY.md"})
    assert err is not None
    assert "denied" in err.lower() or "not allowed" in err.lower() or "Refusing" in err

    # Placeholder path (even if not in deny — FS tools)
    # read_file already denied; test placeholder helper path via open job without deny
    session["key"] = "cron:eod-daily-report"
    tool, params, err = reg.prepare_call("read_file", {"path": "path/to/file.txt"})
    assert err is not None
    assert "placeholder" in err.lower() or "path/to" in err.lower()

    # Allowed MCP
    session["key"] = "cron:market-snapshot-hourly"
    tool, params, err = reg.prepare_call("mcp_winston_wv2_market_snapshot", {})
    assert err is None

    # get_definitions filters
    defs = reg.get_definitions()
    names = [ToolRegistry._schema_name(s) for s in defs]
    assert "mcp_winston_wv2_market_snapshot" in names
    assert "mcp_winston_wv2_perform_daily_analysis" not in names
    assert "read_file" not in names
    assert "message" in names

    # message blocked without required MCP
    mod.reset_turn_state()
    tool, params, err = reg.prepare_call(
        "message",
        {"content": "Markets stable, no movers.", "channel": "telegram", "chat_id": "-100"},
    )
    assert err is not None
    assert "required" in err.lower() or "MCP" in err

    # After successful MCP, message with path-ask still blocked
    mod._get_ok_mcp().add("wv2_market_snapshot")
    tool, params, err = reg.prepare_call(
        "message",
        {
            "content": "Could you please provide the correct file path?",
            "channel": "telegram",
            "chat_id": "-100",
        },
    )
    assert err is not None
    assert "path" in err.lower()

    # Idempotent
    mod.install(ToolRegistry)


@pytest.mark.asyncio
async def test_execute_tracks_ok_mcp_and_circuit_break(mod, monkeypatch):
    class ToolRegistry:
        def prepare_call(self, name, params):
            return SimpleNamespace(execute=AsyncMock()), params, None

        def get_definitions(self):
            return []

        async def execute(self, name, params):
            if name.startswith("mcp_"):
                return json.dumps({"movers": [], "as_of": "2026-07-20"})
            return f"Error: File not found: {params.get('path')}"

        @staticmethod
        def _schema_name(schema):
            return ""

    monkeypatch.setattr(mod, "_install_progress_hook_guards", lambda: None)
    monkeypatch.setattr(mod, "_session_key", lambda: "cron:market-snapshot-hourly")
    mod.install(ToolRegistry)
    mod.reset_turn_state()
    reg = ToolRegistry()

    # Successful MCP tracked
    # install wraps execute; original_execute is the method above
    # But prepare_call in original execute path of ToolRegistry uses prepare_call which we wrapped.
    # Our wrap calls original_execute which is the class's execute before wrap — wait,
    # install saved original_execute before reassignment. The FakeRegistry.execute is the original.
    # However original_execute on real registry does prepare_call internally. Our FakeRegistry.execute
    # does NOT call prepare_call — it just returns. Good for unit test of our wrapper body.

    out = await reg.execute("mcp_winston_wv2_market_snapshot", {})
    assert "movers" in out
    assert "wv2_market_snapshot" in mod._get_ok_mcp()

    # Identical failures → circuit break
    mod.reset_turn_state()
    r1 = await reg.execute("read_file", {"path": "path/to/file.txt"})
    r2 = await reg.execute("read_file", {"path": "path/to/file.txt"})
    r3 = await reg.execute("read_file", {"path": "path/to/file.txt"})
    # first may still be Error from original; second trips; third pre-denied
    assert "CIRCUIT_BREAK" in r2 or "CIRCUIT_BREAK" in r3
    assert "CIRCUIT_BREAK" in r3
