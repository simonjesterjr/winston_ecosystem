"""Ecosystem audit log + correlation IDs for winston_mcp (ADR-004)."""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OBSERVABILITY_KEYS = frozenset({"parent_correlation_id"})


class CorrelationContext:
    __slots__ = ("correlation_id", "parent_correlation_id", "started_at")

    def __init__(
        self,
        correlation_id: str,
        parent_correlation_id: str | None,
        started_at: str,
    ) -> None:
        self.correlation_id = correlation_id
        self.parent_correlation_id = parent_correlation_id
        self.started_at = started_at


def audit_mcp_dir() -> Path:
    root = os.getenv(
        "ECOSYSTEM_AUDIT_DIR",
        os.getenv("CROMWELL_MCP_AUDIT_DIR", "/audit/mcp"),
    )
    path = Path(root)
    path.mkdir(parents=True, exist_ok=True)
    return path


def webhook_inbox_dir() -> Path:
    path = Path(os.getenv("CROMWELL_WEBHOOK_INBOX", "/audit/webhook"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def begin_invocation(arguments: dict[str, Any] | None) -> CorrelationContext:
    args = arguments or {}
    parent = args.get("parent_correlation_id")
    if parent is not None:
        parent = str(parent).strip() or None
    started = (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )
    return CorrelationContext(str(uuid.uuid4()), parent, started)


def strip_observability_args(arguments: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in arguments.items() if k not in OBSERVABILITY_KEYS}


def correlation_headers(ctx: CorrelationContext) -> dict[str, str]:
    headers = {"X-Correlation-Id": ctx.correlation_id}
    if ctx.parent_correlation_id:
        headers["X-Parent-Correlation-Id"] = ctx.parent_correlation_id
    return headers


def monolith_label(base: str) -> str:
    lowered = base.lower()
    if "winston_v2" in lowered:
        return "winston_v2"
    if "winston_unit_test" in lowered:
        return "winston_unit_test"
    if "data_manager" in lowered:
        return "data_manager"
    return "unknown"


def summarize_hops(hops: list[tuple[str, str, int]]) -> tuple[str | None, str | None, int | None]:
    if not hops:
        return None, None, None
    if len(hops) == 1:
        mono, endpoint, status = hops[0]
        return mono, endpoint, status
    endpoint = " -> ".join(f"{mono}{path}" for mono, path, _ in hops)
    return "multi", endpoint, hops[-1][2]


def attach_meta(data: Any, ctx: CorrelationContext) -> Any:
    if not isinstance(data, dict):
        return data
    meta = data.setdefault("_meta", {})
    if isinstance(meta, dict):
        meta["correlation_id"] = ctx.correlation_id
        if ctx.parent_correlation_id:
            meta["parent_correlation_id"] = ctx.parent_correlation_id
    return data


def append_audit(
    ctx: CorrelationContext,
    *,
    tool: str,
    duration_ms: int,
    status: str,
    monolith: str | None = None,
    endpoint: str | None = None,
    http_status: int | None = None,
    error_code: str | None = None,
    error_summary: str | None = None,
) -> None:
    record = {
        "correlation_id": ctx.correlation_id,
        "parent_correlation_id": ctx.parent_correlation_id,
        "tool": tool,
        "started_at": ctx.started_at,
        "duration_ms": duration_ms,
        "status": status,
        "monolith": monolith,
        "endpoint": endpoint,
        "http_status": http_status,
        "error_code": error_code,
        "error_summary": error_summary[:500] if error_summary else None,
    }
    day = ctx.started_at[:10].replace("-", "")
    path = audit_mcp_dir() / f"mcp_audit_{day}.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, default=str) + "\n")