"""Cron duty guards for nanobot ToolRegistry + finalize (Sawtooth Cromwell).

When session_key is ``cron:<job-id>``:

1. **MCP allowlist** — only listed MCP tools may run (non-MCP remain unless denied).
2. **builtin_deny** — optional hard deny of named builtins (e.g. read_file).
3. **Placeholder path block** — docs-style paths like ``path/to/file.txt`` rejected.
4. **Identical-fail circuit-break** — after N identical failed tool calls (name+args),
   hard-stop with ops guidance (no "try a different approach" death spiral).
5. **mcp_require** — finalize_content rewrites hallucinated completion if required
   MCP tools never succeeded this turn (never invent "stable / no movers").
6. **No human path-asks** — message tool + final text blocked if they ask for paths.

Config path (first existing wins):
  1. NANOBOT_CRON_TOOL_ALLOWLIST env
  2. ~/.nanobot/workspace/schedule/cron-tool-allowlist.json
  3. /root/.nanobot/workspace/schedule/cron-tool-allowlist.json
"""

from __future__ import annotations

import json
import logging
import os
import re
from contextvars import ContextVar
from pathlib import Path
from typing import Any

logger = logging.getLogger("nanobot.cron_tool_allowlist")

_CONFIG_CACHE: dict[str, Any] | None = None
_CONFIG_MTIME: float | None = None
_CONFIG_PATH: Path | None = None

# Per-agent-turn state (reset in AgentProgressHook.before_run).
_fail_counts: ContextVar[dict[str, int] | None] = ContextVar(
    "sawtooth_cron_fail_counts", default=None
)
_ok_mcp: ContextVar[set[str] | None] = ContextVar("sawtooth_cron_ok_mcp", default=None)

_DEFAULT_IDENTICAL_FAIL_LIMIT = 2

# Docs / textbook placeholders the small model invents after truncation.
_PLACEHOLDER_PATH_EXACT = frozenset(
    {
        "path/to/file.txt",
        "path/to/file",
        "/path/to/file.txt",
        "/path/to/file",
        "path/to/your/file.txt",
        "/path/to/your/file.txt",
        "file.txt",
        "example.txt",
        "/path/to/filename",
        "path/to/filename",
    }
)
_PLACEHOLDER_PATH_RE = re.compile(
    r"(?i)^(?:\.?/)?(?:path/to(?:/your)?/|your[_/ -]?path(?:/|$)|"
    r"<[^>]*path[^>]*>|example(?:_file)?\.txt$)"
)

# Human-facing recovery asks that must never leave cron turns.
_PATH_ASK_RE = re.compile(
    r"(?is)("
    r"(could you|can you|please)\s+(provide|send|share|give).{0,60}"
    r"(file\s*)?path"
    r"|provide the correct (file\s*)?path"
    r"|what is the (correct\s+)?(file\s*)?path"
    r"|path/to/file"
    r")"
)

_FS_TOOLS = frozenset(
    {
        "read_file",
        "write_file",
        "edit_file",
        "list_dir",
        "find_files",
    }
)


def reset_turn_state() -> None:
    """Clear per-turn counters (call at start of each agent run)."""
    _fail_counts.set({})
    _ok_mcp.set(set())


def _get_fail_counts() -> dict[str, int]:
    d = _fail_counts.get()
    if d is None:
        d = {}
        _fail_counts.set(d)
    return d


def _get_ok_mcp() -> set[str]:
    s = _ok_mcp.get()
    if s is None:
        s = set()
        _ok_mcp.set(s)
    return s


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


def _job_entry(job_id: str) -> dict[str, Any]:
    cfg = _load_config()
    jobs = cfg.get("jobs") or {}
    entry = jobs.get(job_id)
    if entry is None:
        entry = cfg.get("default_for_unlisted_cron_job") or {}
    return entry if isinstance(entry, dict) else {}


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
    entry = _job_entry(job_id)
    allow = entry.get("mcp_allow") or []
    return {str(x).strip() for x in allow if str(x).strip()}


def required_mcp_set(job_id: str) -> set[str]:
    entry = _job_entry(job_id)
    req = entry.get("mcp_require") or []
    return {str(x).strip() for x in req if str(x).strip()}


def builtin_deny_set(job_id: str) -> set[str]:
    entry = _job_entry(job_id)
    deny = entry.get("builtin_deny") or []
    return {str(x).strip() for x in deny if str(x).strip()}


def identical_fail_limit(job_id: str | None) -> int:
    if not job_id:
        return _DEFAULT_IDENTICAL_FAIL_LIMIT
    entry = _job_entry(job_id)
    raw = entry.get("identical_fail_limit")
    if raw is None:
        cfg = _load_config()
        raw = (cfg.get("defaults") or {}).get("identical_fail_limit")
    try:
        n = int(raw) if raw is not None else _DEFAULT_IDENTICAL_FAIL_LIMIT
    except (TypeError, ValueError):
        n = _DEFAULT_IDENTICAL_FAIL_LIMIT
    return max(1, n)


def force_args_for(job_id: str, logical: str) -> dict[str, Any]:
    entry = _job_entry(job_id)
    force = entry.get("force_args") or {}
    if not isinstance(force, dict):
        return {}
    payload = force.get(logical) or {}
    return dict(payload) if isinstance(payload, dict) else {}


def is_mcp_allowed(job_id: str, tool_name: str) -> bool:
    logical = mcp_logical_name(tool_name)
    if logical is None:
        return True  # non-MCP: see builtin_deny
    return logical in allowed_mcp_set(job_id)


def is_builtin_denied(job_id: str, tool_name: str) -> bool:
    if mcp_logical_name(tool_name) is not None:
        return False
    return str(tool_name) in builtin_deny_set(job_id)


def deny_message(job_id: str, tool_name: str) -> str:
    allow = sorted(allowed_mcp_set(job_id))
    logical = mcp_logical_name(tool_name) or tool_name
    allow_s = ", ".join(allow) if allow else "(none)"
    return (
        f"Error: Tool '{tool_name}' ({logical}) is not allowed for cron job '{job_id}'. "
        f"Allowed MCP tools: {allow_s}. "
        "Do not retry with another MCP tool. Summarize using only allowed tools or state the duty blocked."
    )


def builtin_deny_message(job_id: str, tool_name: str) -> str:
    return (
        f"Error: Builtin tool '{tool_name}' is denied for cron job '{job_id}'. "
        "Do not read free-form files. Do NOT ask the human for a path. "
        "Use only this turn's allowed MCP tool output, or post a one-line OPS ERROR."
    )


def _session_key() -> str | None:
    try:
        from nanobot.agent.tools.context import current_request_session_key

        return current_request_session_key()
    except Exception:
        return None


def _path_from_params(params: Any) -> str | None:
    if not isinstance(params, dict):
        return None
    for key in ("path", "file_path", "target", "source", "destination"):
        val = params.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return None


def is_placeholder_path(path: str | None) -> bool:
    if not path:
        return False
    p = path.strip().strip("\"'")
    if not p:
        return False
    if p.lower() in _PLACEHOLDER_PATH_EXACT or p in _PLACEHOLDER_PATH_EXACT:
        return True
    if _PLACEHOLDER_PATH_RE.match(p):
        return True
    # Generic "path/to/..." textbook form
    if re.search(r"(?i)path/to/", p):
        return True
    return False


def placeholder_path_message(tool_name: str, path: str) -> str:
    return (
        f"Error: Refusing placeholder path '{path}' for tool '{tool_name}'. "
        "This is not a real workspace path. Do NOT retry with path/to/file.txt. "
        "Do NOT ask the human for a file path. "
        "If MCP tool output is already in this turn, format the duty from that payload only; "
        "otherwise post a one-line OPS ERROR that the duty failed."
    )


def looks_like_path_ask(text: str | None) -> bool:
    if not text or not str(text).strip():
        return False
    return bool(_PATH_ASK_RE.search(str(text)))


def call_signature(name: str, params: Any) -> str:
    try:
        if isinstance(params, dict):
            args = json.dumps(params, sort_keys=True, default=str, ensure_ascii=False)
        else:
            args = json.dumps(params, default=str, ensure_ascii=False)
    except Exception:
        args = repr(params)
    return f"{name}|{args}"


def is_error_result(result: Any) -> bool:
    if result is None:
        return False
    if not isinstance(result, str):
        return False
    s = result.lstrip()
    return s.startswith("Error") or s.startswith("Error:")


def circuit_break_message(job_id: str, name: str, count: int) -> str:
    return (
        f"Error: CIRCUIT_BREAK for cron job '{job_id}': identical failed tool call "
        f"'{name}' repeated {count} times this turn. STOP retrying. "
        "Do NOT ask the human for a file path or free-form recovery. "
        "If allowed MCP output is already available this turn, format the duty from it. "
        "Otherwise post exactly one short OPS ERROR line that the duty failed."
    )


def path_ask_block_message(job_id: str) -> str:
    return (
        f"Error: Cron job '{job_id}' must not ask the human for file paths. "
        "Do not post recovery questions. Format from this turn's MCP payload or "
        "post a one-line OPS ERROR."
    )


def missing_mcp_ops_error(job_id: str, missing: set[str]) -> str:
    tools = ", ".join(sorted(missing))
    return (
        f"OPS ERROR: cron `{job_id}` finished without required MCP tool(s): {tools}. "
        "No market claim invented. Retry next schedule or check MCP/logs."
    )


def path_ask_ops_error(job_id: str) -> str:
    return (
        f"OPS ERROR: cron `{job_id}` attempted a human path-ask after tool failure. "
        "Suppressed. No free-form recovery on scheduled turns."
    )


def enforce_cron_final_content(content: str | None, *, session_key: str | None = None) -> str | None:
    """Rewrite final assistant text for cron duty violations."""
    sk = session_key if session_key is not None else _session_key()
    job_id = cron_job_id_from_session_key(sk)
    if not job_id:
        return content

    if looks_like_path_ask(content):
        logger.warning(
            "cron_duty path-ask suppressed job=%s session=%s",
            job_id,
            sk,
        )
        return path_ask_ops_error(job_id)

    required = required_mcp_set(job_id)
    if required:
        ok = _get_ok_mcp()
        missing = required - ok
        if missing:
            logger.warning(
                "cron_duty missing required MCP job=%s missing=%s ok=%s",
                job_id,
                sorted(missing),
                sorted(ok),
            )
            return missing_mcp_ops_error(job_id, missing)

    return content


def install(ToolRegistry: type) -> None:
    """Monkey-patch ToolRegistry + progress-hook finalize for cron duty guards."""
    if getattr(ToolRegistry, "_sawtooth_cron_allowlist_installed", False):
        return

    original_prepare = ToolRegistry.prepare_call
    original_get_definitions = ToolRegistry.get_definitions
    original_execute = ToolRegistry.execute

    def prepare_call(self, name: str, params: Any):  # type: ignore[no-untyped-def]
        session_key = _session_key()
        job_id = cron_job_id_from_session_key(session_key)
        tool_name = str(name)

        if job_id:
            # Circuit-break before re-running identical failures
            sig = call_signature(tool_name, params)
            counts = _get_fail_counts()
            limit = identical_fail_limit(job_id)
            if counts.get(sig, 0) >= limit:
                logger.warning(
                    "cron_circuit_break pre-deny job=%s tool=%s count=%s",
                    job_id,
                    tool_name,
                    counts.get(sig),
                )
                return None, params, circuit_break_message(job_id, tool_name, counts[sig])

            # Hard-deny listed builtins (e.g. read_file on market snapshot)
            if is_builtin_denied(job_id, tool_name):
                logger.warning(
                    "cron_builtin_deny job=%s tool=%s session=%s",
                    job_id,
                    tool_name,
                    session_key,
                )
                return None, params, builtin_deny_message(job_id, tool_name)

            # Placeholder path block (all FS-ish tools on cron)
            if tool_name in _FS_TOOLS or tool_name in builtin_deny_set(job_id):
                path = _path_from_params(params)
                if is_placeholder_path(path):
                    logger.warning(
                        "cron_placeholder_path job=%s tool=%s path=%s",
                        job_id,
                        tool_name,
                        path,
                    )
                    return None, params, placeholder_path_message(tool_name, path or "")

            # Message tool: no path-asks; require MCP first when configured
            if tool_name == "message":
                content = ""
                if isinstance(params, dict):
                    content = str(params.get("content") or "")
                if looks_like_path_ask(content):
                    logger.warning("cron_message path-ask blocked job=%s", job_id)
                    return None, params, path_ask_block_message(job_id)
                required = required_mcp_set(job_id)
                if required:
                    ok = _get_ok_mcp()
                    missing = required - ok
                    if missing:
                        msg = (
                            f"Error: Cron job '{job_id}' cannot send a message until required "
                            f"MCP tool(s) succeed this turn: {', '.join(sorted(missing))}. "
                            "Call the required tool with a fresh invocation, then format from "
                            "its payload. Never invent stable/no-movers without it."
                        )
                        logger.warning(
                            "cron_message blocked missing MCP job=%s missing=%s",
                            job_id,
                            sorted(missing),
                        )
                        return None, params, msg

            # MCP allowlist + force_args
            if mcp_logical_name(tool_name) is not None:
                if not is_mcp_allowed(job_id, tool_name):
                    logger.warning(
                        "cron_tool_allowlist deny job=%s tool=%s session=%s",
                        job_id,
                        tool_name,
                        session_key,
                    )
                    return None, params, deny_message(job_id, tool_name)

                logical = mcp_logical_name(tool_name)
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
        session_key = _session_key()
        job_id = cron_job_id_from_session_key(session_key)
        if not job_id:
            return definitions

        allow = allowed_mcp_set(job_id)
        deny = builtin_deny_set(job_id)
        filtered: list[dict[str, Any]] = []
        for schema in definitions:
            name = ToolRegistry._schema_name(schema)
            logical = mcp_logical_name(name)
            if logical is None:
                if name not in deny:
                    filtered.append(schema)
            elif logical in allow:
                filtered.append(schema)
        return filtered

    async def execute(self, name: str, params: Any) -> Any:  # type: ignore[no-untyped-def]
        session_key = _session_key()
        job_id = cron_job_id_from_session_key(session_key)
        tool_name = str(name)
        sig = call_signature(tool_name, params)

        if job_id:
            counts = _get_fail_counts()
            limit = identical_fail_limit(job_id)
            if counts.get(sig, 0) >= limit:
                logger.warning(
                    "cron_circuit_break execute job=%s tool=%s count=%s",
                    job_id,
                    tool_name,
                    counts.get(sig),
                )
                return circuit_break_message(job_id, tool_name, counts[sig])

        result = await original_execute(self, name, params)

        if job_id:
            if is_error_result(result):
                counts = _get_fail_counts()
                counts[sig] = counts.get(sig, 0) + 1
                limit = identical_fail_limit(job_id)
                if counts[sig] >= limit:
                    logger.warning(
                        "cron_circuit_break trip job=%s tool=%s count=%s",
                        job_id,
                        tool_name,
                        counts[sig],
                    )
                    # No "try a different approach" — hard stop.
                    return circuit_break_message(job_id, tool_name, counts[sig])
            else:
                logical = mcp_logical_name(tool_name)
                if logical:
                    _get_ok_mcp().add(logical)

        return result

    ToolRegistry.prepare_call = prepare_call  # type: ignore[method-assign]
    ToolRegistry.get_definitions = get_definitions  # type: ignore[method-assign]
    ToolRegistry.execute = execute  # type: ignore[method-assign]
    ToolRegistry._sawtooth_cron_allowlist_installed = True  # type: ignore[attr-defined]
    logger.info("Sawtooth cron duty guards installed on ToolRegistry")

    _install_progress_hook_guards()


def _install_progress_hook_guards() -> None:
    """Patch AgentProgressHook for turn reset + final-content duty rewrite."""
    try:
        from nanobot.agent.progress_hook import AgentProgressHook
    except Exception as exc:  # noqa: BLE001
        logger.warning("cron duty: AgentProgressHook not available yet: %s", exc)
        return

    if getattr(AgentProgressHook, "_sawtooth_cron_duty_installed", False):
        return

    original_finalize = AgentProgressHook.finalize_content
    original_before_run = AgentProgressHook.before_run

    def finalize_content(self, context: Any, content: str | None) -> str | None:  # type: ignore[no-untyped-def]
        cleaned = original_finalize(self, context, content)
        session_key = getattr(self, "_session_key", None) or _session_key()
        return enforce_cron_final_content(cleaned, session_key=session_key)

    async def before_run(self, context: Any) -> None:  # type: ignore[no-untyped-def]
        reset_turn_state()
        await original_before_run(self, context)

    AgentProgressHook.finalize_content = finalize_content  # type: ignore[method-assign]
    AgentProgressHook.before_run = before_run  # type: ignore[method-assign]
    AgentProgressHook._sawtooth_cron_duty_installed = True  # type: ignore[attr-defined]
    logger.info("Sawtooth cron duty guards installed on AgentProgressHook")
