"""Progress hints for long-running MCP tools (task 8)."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp_winston.tools_schema import LONG_RUNNING_SECONDS, LONG_RUNNING_TOOLS


def log_progress(correlation_id: str, tool: str, message: str) -> None:
    record = {
        "event": "progress",
        "correlation_id": correlation_id,
        "tool": tool,
        "message": message,
        "at": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    }
    day = record["at"][:10].replace("-", "")
    root = os.getenv("ECOSYSTEM_AUDIT_DIR", os.getenv("CROMWELL_MCP_AUDIT_DIR", "/audit/mcp"))
    path = Path(root) / f"mcp_audit_{day}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    print(f"[winston_mcp] progress {tool}: {message} corr={correlation_id[:8]}", flush=True)


def attach_long_running_meta(data: Any, tool: str) -> Any:
    if tool not in LONG_RUNNING_TOOLS or not isinstance(data, dict):
        return data
    if data.get("status") == "error":
        return data
    meta = data.setdefault("_meta", {})
    if isinstance(meta, dict):
        meta["long_running"] = True
        meta["estimated_duration_seconds"] = LONG_RUNNING_SECONDS.get(tool, 120)
        meta["progress_note"] = (
            "Tool may take up to estimated_duration_seconds; tail ecosystem/logs/audit/mcp/ "
            "for event=progress lines keyed by correlation_id."
        )
    return data