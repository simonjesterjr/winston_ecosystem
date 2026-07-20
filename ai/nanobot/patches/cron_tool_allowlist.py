"""Cron MCP tool allowlist for nanobot ToolRegistry (Sawtooth Cromwell).

When session_key is ``cron:<job-id>``, only MCP tools listed for that job may
run. Non-MCP tools (message, filesystem, etc.) remain available.

Config path (first existing wins):
  1. NANOBOT_CRON_TOOL_ALLOWLIST env
  2. ~/.nanobot/workspace/schedule/cron-tool-allowlist.json
  3. /root/.nanobot/workspace/schedule/cron-tool-allowlist.json
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

logger = logging.getLogger("nanobot.cron_tool_allowlist")

_CONFIG_CACHE: dict[str, Any] | None = None
_CONFIG_MTIME: float | None = None
_CONFIG_PATH: Path | None = None


def _config_candidates() -> list[Path]:
    paths: list[Path] = []
    env = os.environ.get("NANOBOT_CRON_TOOL_ALLOWLIST", "").strip()
    if env:
        paths.append(Path(env))
    home = Path.home() / ".nanobot" / "workspace" / "schedule" / "cron-tool-allowlist.json"
    paths.append(home)
    paths.append(Path("/root/.nanobot/workspace/schedule/cron-tool-allowlist.json"))
    return paths


def _load_config() -> dict[str, Any]:
    global _CONFIG_CACHE, _CONFIG_MTIME, _CONFIG_PATH
    for path in _config_candidates():
        try:
            if not path.is_file():
                continue
            mtime = path.stat().st_mtime
            if _CONFIG_CACHE is not None and _CONFIG_PATH == path and _CONFIG_MTIME == mtime:
                return _CONFIG_CACHE
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            _CONFIG_CACHE = data
            _CONFIG_MTIME = mtime
            _CONFIG_PATH = path
            return data
        except Exception as exc:  # noqa: BLE001 — fail open to empty jobs map
            logger.warning("cron tool allowlist: failed to load %s: %s", path, exc)
    return {"version": 1, "jobs": {}, "default_for_unlisted_cron_job": {"mcp_allow": []}}


def cron_job_id_from_session_key(session_key: str | None) -> str | None:
    if not session_key:
        return None
    sk = str(session_key).strip()
    if not sk.startswith("cron:"):
        return None
    job_id = sk[5:].strip()
    return job_id or None


def mcp_logical_name(tool_name: str) -> str | None:
    """mcp_winston_wv2_market_snapshot -> wv2_market_snapshot."""
    name = str(tool_name or "")
    if not name.startswith("mcp_"):
        return None
    # mcp_<server>_<logical...>
    parts = name.split("_", 2)
    if len(parts) < 3:
        return name
    return parts[2]


def allowed_mcp_set(job_id: str) -> set[str]:
    cfg = _load_config()
    jobs = cfg.get("jobs") or {}
    entry = jobs.get(job_id)
    if entry is None:
        entry = cfg.get("default_for_unlisted_cron_job") or {"mcp_allow": []}
    allow = entry.get("mcp_allow") if isinstance(entry, dict) else []
    return {str(x).strip() for x in (allow or []) if str(x).strip()}


def force_args_for(job_id: str, logical: str) -> dict[str, Any]:
    cfg = _load_config()
    jobs = cfg.get("jobs") or {}
    entry = jobs.get(job_id) or {}
    if not isinstance(entry, dict):
        return {}
    force = entry.get("force_args") or {}
    if not isinstance(force, dict):
        return {}
    payload = force.get(logical) or {}
    return dict(payload) if isinstance(payload, dict) else {}


def is_mcp_allowed(job_id: str, tool_name: str) -> bool:
    logical = mcp_logical_name(tool_name)
    if logical is None:
        return True  # non-MCP tools always allowed on cron
    return logical in allowed_mcp_set(job_id)


def deny_message(job_id: str, tool_name: str) -> str:
    allow = sorted(allowed_mcp_set(job_id))
    logical = mcp_logical_name(tool_name) or tool_name
    allow_s = ", ".join(allow) if allow else "(none)"
    return (
        f"Error: Tool '{tool_name}' ({logical}) is not allowed for cron job '{job_id}'. "
        f"Allowed MCP tools: {allow_s}. "
        "Do not retry with another MCP tool. Summarize using only allowed tools or state the duty blocked."
    )


def install(ToolRegistry: type) -> None:
    """Monkey-patch ToolRegistry.prepare_call and get_definitions."""
    if getattr(ToolRegistry, "_sawtooth_cron_allowlist_installed", False):
        return

    original_prepare = ToolRegistry.prepare_call
    original_get_definitions = ToolRegistry.get_definitions

    def prepare_call(self, name: str, params: Any):  # type: ignore[no-untyped-def]
        try:
            from nanobot.agent.tools.context import current_request_session_key

            session_key = current_request_session_key()
        except Exception:
            session_key = None

        job_id = cron_job_id_from_session_key(session_key)
        if job_id and mcp_logical_name(str(name)) is not None:
            if not is_mcp_allowed(job_id, str(name)):
                logger.warning(
                    "cron_tool_allowlist deny job=%s tool=%s session=%s",
                    job_id,
                    name,
                    session_key,
                )
                return None, params, deny_message(job_id, str(name))

            # Force duty-critical args (e.g. fetch_only on EOD report)
            logical = mcp_logical_name(str(name))
            forced = force_args_for(job_id, logical or "")
            if forced:
                if not isinstance(params, dict):
                    params = {}
                else:
                    params = dict(params)
                params.update(forced)

        return original_prepare(self, name, params)

    def get_definitions(self):  # type: ignore[no-untyped-def]
        definitions = original_get_definitions(self)
        try:
            from nanobot.agent.tools.context import current_request_session_key

            session_key = current_request_session_key()
        except Exception:
            return definitions

        job_id = cron_job_id_from_session_key(session_key)
        if not job_id:
            return definitions

        allow = allowed_mcp_set(job_id)
        filtered: list[dict[str, Any]] = []
        for schema in definitions:
            name = ToolRegistry._schema_name(schema)
            logical = mcp_logical_name(name)
            if logical is None:
                filtered.append(schema)  # builtins
            elif logical in allow:
                filtered.append(schema)
        return filtered

    ToolRegistry.prepare_call = prepare_call  # type: ignore[method-assign]
    ToolRegistry.get_definitions = get_definitions  # type: ignore[method-assign]
    ToolRegistry._sawtooth_cron_allowlist_installed = True  # type: ignore[attr-defined]
    logger.info("Sawtooth cron MCP tool allowlist installed on ToolRegistry")
