"""Shared JSON Schema fragments for MCP tools (task 8)."""

from __future__ import annotations

from typing import Any

OBSERVABILITY_PROPERTIES: dict[str, Any] = {
    "parent_correlation_id": {
        # LLMs often emit null for unused optionals; nanobot validates against this schema.
        "type": ["string", "null"],
        "description": (
            "Optional UUID from a prior tool _meta.correlation_id to chain Cromwell turns. "
            "Omit the key (preferred) or pass null when unused."
        ),
    },
}

LONG_RUNNING_TOOLS: frozenset[str] = frozenset({
    "wv2_perform_daily_analysis",
    "wv2_get_daily_activity_report",
    "wv2_sync_data",
    "wut_run_daily_operations",
    "wut_sync_portfolio_data",
    "wv2_transfer_portfolio_from_wut",
    "dm_request_full_sync",
})

LONG_RUNNING_SECONDS: dict[str, int] = {
    "wv2_perform_daily_analysis": 180,
    "wv2_get_daily_activity_report": 180,
    "wv2_sync_data": 60,
    "wut_run_daily_operations": 180,
    "wut_sync_portfolio_data": 60,
    "wv2_transfer_portfolio_from_wut": 45,
    "dm_request_full_sync": 600,
}


def with_observability(schema: dict[str, Any]) -> dict[str, Any]:
    props = dict(schema.get("properties") or {})
    props.update(OBSERVABILITY_PROPERTIES)
    out = dict(schema)
    out["properties"] = props
    return out