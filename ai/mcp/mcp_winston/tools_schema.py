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
    "wv2_market_snapshot",
    "wv2_sync_data",
    "wut_run_daily_operations",
    "wut_sync_portfolio_data",
    "wv2_transfer_portfolio_from_wut",
    "dm_request_full_sync",
})

LONG_RUNNING_SECONDS: dict[str, int] = {
    "wv2_perform_daily_analysis": 180,
    "wv2_get_daily_activity_report": 180,
    "wv2_market_snapshot": 90,
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


# WUT lab eval (Wave 1–2). Mutating tools require this exact string; forward to WUT.
LAB_AUTHORIZATION_SCHEMA: dict[str, Any] = {
    "type": "string",
    "const": "lab_geometry_report_only",
    "description": (
        "Required agent guardrail. Must be the exact string lab_geometry_report_only. "
        "Lab geometry / report-only — no pack-default promotion, no Broker Gateway order_write."
    ),
}

# Canonical heat. String turtle → TURTLE_DEFAULTS. null / omit / legacy → lot caps only.
HEAT_CONFIG_SCHEMA: dict[str, Any] = {
    "description": (
        "Canonical heat. String turtle → TURTLE_DEFAULTS. null / omit / legacy → lot caps only. "
        "Object is an explicit L1–L4 hash. Do not send expectancy-style aliases."
    ),
    "oneOf": [
        {"type": "null"},
        {"type": "string", "enum": ["turtle", "legacy"]},
        {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "enum": ["turtle", "legacy", "off"]},
                "unit_risk_fraction": {"type": "number", "exclusiveMinimum": 0},
                "max_units_per_market": {"type": "integer", "minimum": 1},
                "max_units_closely_correlated_same_direction": {
                    "type": "integer",
                    "minimum": 1,
                },
                "max_units_loosely_correlated_same_direction": {
                    "type": "integer",
                    "minimum": 1,
                },
                "max_units_single_direction": {"type": "integer", "minimum": 1},
                "correlation": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "default": "pcs_pairwise"},
                        "close_threshold": {"type": "number"},
                        "loose_threshold": {"type": "number"},
                        "window": {"type": "string", "default": "methodology"},
                    },
                },
            },
        },
    ],
}