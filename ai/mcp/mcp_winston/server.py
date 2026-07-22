"""
MCP server for Winston (Wv2 core use cases + conveniences).

This is the "MCP component" that lets nanobot (our cromwell bot on Telegram)
or any other MCP client securely drive the 6 primary Wv2 operations plus
supporting discovery/report tools.

Design goals for immediate slice (see ecosystem/plans/winston-mcp-immediate.md):
- Thin delegator only. All real work lives in the monoliths (Wv2 internal
  controllers, DmParquetIngester, CromwellNotifier, WUT export/strategy_config).
- Talk only over the podman compose network using the existing /internal/*
  HTTP surfaces (no direct DB access, no rake exec, no broad fs).
- Support both stdio (easy local testing: python -m mcp_winston) and
  HTTP/SSE (preferred when nanobot runs in the same compose network).
- Exact tool surface defined in ecosystem/interfaces/winston-mcp-tools.md.

The compose "winston_mcp" service runs the HTTP mode.
"""

from __future__ import annotations

import os
import time
from typing import Any

import httpx

from mcp_winston.audit import (
    append_audit,
    attach_meta,
    begin_invocation,
    correlation_headers,
    monolith_label,
    strip_observability_args,
    summarize_hops,
    webhook_inbox_dir,
)
from mcp_winston.errors import build_error_payload
from mcp_winston.progress import attach_long_running_meta, log_progress
from mcp_winston.rate_limit import check_rate_limit
from mcp_winston.tools_schema import LONG_RUNNING_TOOLS, with_observability

# mcp package provides the protocol. We use a simple Server + stdio + a small
# ASGI app for the HTTP/SSE transport when run under uvicorn.
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    # Fallback message if the package isn't installed in the env.
    raise RuntimeError("Install with: pip install mcp httpx  (or use the Containerfile)")

# Base URLs inside the podman compose network (overridable for local testing).
WV2_BASE = os.getenv("WINSTON_V2_URL", "http://winston_v2:3000")
WUT_BASE = os.getenv("WINSTON_UNIT_TEST_URL", "http://winston_unit_test:3000")
DM_BASE = os.getenv("DATA_MANAGER_URL", "http://data_manager:3000")

server = Server("winston-mcp")


async def _post(
    base: str,
    path: str,
    json: dict | None = None,
    timeout: float = 30.0,
    *,
    ctx: Any = None,
    audit_hops: list[tuple[str, str, int]] | None = None,
) -> Any:
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"
    headers = correlation_headers(ctx) if ctx else {}
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=json, headers=headers)
        if audit_hops is not None:
            audit_hops.append((monolith_label(base), f"/{path.lstrip('/')}", resp.status_code))
        resp.raise_for_status()
        return resp.json()


async def _get(
    base: str,
    path: str,
    params: dict | None = None,
    timeout: float = 30.0,
    *,
    ctx: Any = None,
    audit_hops: list[tuple[str, str, int]] | None = None,
) -> Any:
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"
    headers = correlation_headers(ctx) if ctx else {}
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get(url, params=params, headers=headers)
        if audit_hops is not None:
            audit_hops.append((monolith_label(base), f"/{path.lstrip('/')}", resp.status_code))
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# Tool definitions (must stay in sync with ecosystem/interfaces/winston-mcp-tools.md)
# ---------------------------------------------------------------------------

@server.list_tools()
async def list_tools() -> list[Tool]:
    tools = [
        Tool(
            name="wv2_list_portfolios",
            description="List Wv2 portfolios.",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="wv2_market_snapshot",
            description=(
                "Intraday attention radar for symbols in active portfolios: live internet price "
                "vs prior EOD close and atr_17 (DM parquet). Returns previous_close, current_price, "
                "atr_17, move, atr_multiple, status (quiet|testing|breach_up|breach_down), and movers. "
                "Symbols without a live quote are omitted. Focusing tool only — not daily analysis."
            ),
            inputSchema={
                "type": "object",
                "properties": {"all_portfolios": {"type": "boolean", "description": "Include inactive portfolios"}},
            },
        ),
        Tool(
            name="wv2_transfer_portfolio_from_wut",
            description=(
                "Transfer portfolio config from WUT into Wv2. "
                "Pass exactly one of run_id or ts_id (integer). "
                "Omit unused optional keys — do not pass null. "
                "On success the JSON includes reply_text and summary — "
                "paste reply_text as the entire user-facing reply "
                "(must show action + #id; no market lists or menus)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    # null allowed: small LLMs often fill unused optionals with null.
                    "run_id": {
                        "type": ["integer", "null"],
                        "description": "WUT PortfolioBacktestRun id (preferred for full portfolio+markets)",
                    },
                    "ts_id": {
                        "type": ["integer", "null"],
                        "description": "WUT TradingStrategy id (strategy export path)",
                    },
                },
            },
        ),
        Tool(
            name="wv2_create_portfolio",
            description="Create Wv2 portfolio (name, initial_capital, markets).",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "initial_capital": {"type": "number"},
                    "markets": {"type": "array", "items": {"type": "string"}},
                    "trading_strategy_name": {"type": "string"}
                },
                "required": ["name", "initial_capital", "markets"],
            },
        ),
        Tool(
            name="wv2_add_market",
            description="Add symbol to portfolio.",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string", "description": "Portfolio id or name"},
                    "symbol": {"type": "string"},
                },
                "required": ["portfolio_id_or_name", "symbol"],
            },
        ),
        Tool(
            name="wv2_sync_data",
            description="Sync data for portfolio or symbols.",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string", "description": "Portfolio id or name"},
                    "symbols": {"type": "array", "items": {"type": "string"}},
                },
            },
        ),
        Tool(
            name="wv2_perform_daily_analysis",
            description=(
                "Run daily analysis synchronously for active portfolios (production EOD path). "
                "Omit date to use the production report date (today after 4:30 PM MT, else prior day). "
                "Historical dates are REJECTED unless allow_historical=true (explicit test pass only). "
                "Historical runs do not auto-post Telegram unless deliver_telegram=true. "
                "Never call from morning/market-snapshot cron. "
                "Returns evaluated/skipped portfolios, signals, actions, summary, and Cromwell report."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string", "description": "Portfolio id or name"},
                    "date": {
                        "type": "string",
                        "description": (
                            "YYYY-MM-DD production EOD date only by default. "
                            "Historical requires allow_historical=true."
                        ),
                    },
                    "allow_historical": {
                        "type": "boolean",
                        "description": (
                            "Explicit test pass only. Required for any non-production report date. "
                            "Default false. Never set from cron."
                        ),
                    },
                    "deliver_telegram": {
                        "type": "boolean",
                        "description": (
                            "With allow_historical=true, also post PDF to Sawtooth Main. "
                            "Default false — historical DARs must not hit production Telegram."
                        ),
                    },
                },
            },
        ),
        Tool(
            name="wv2_get_daily_activity_report",
            description=(
                "Get daily activity report for a date. Returns JSON plus pdf_path and telegram_media_path. "
                "Without fetch_only, may run analysis if the report file is missing — that path "
                "follows the same production-date policy (historical needs allow_historical). "
                "Scheduled EOD delivery must use fetch_only true (report built by Wv2 Sidekiq at 4:30 PM MT)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "YYYY-MM-DD"},
                    "portfolio_id_or_name": {"type": "string", "description": "Portfolio id or name"},
                    "fetch_only": {"type": "boolean", "description": "Do not trigger analysis if report missing"},
                    "allow_historical": {
                        "type": "boolean",
                        "description": "Only for on-demand generate of a non-production date (test pass).",
                    },
                    "deliver_telegram": {
                        "type": "boolean",
                        "description": "With allow_historical, opt in to Sawtooth Main PDF post (default false).",
                    },
                },
            },
        ),
        Tool(
            name="wv2_confirm_journal",
            description=(
                "Confirm and execute a draft journal (opens/closes positions, updates capital flow). "
                "Idempotent when journal is already executed. "
                "To change units/price/notes/stop without executing, use wv2_edit_journal first."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "journal_id": {"type": "integer"},
                    "execution_price": {"type": "number"},
                    "units": {"type": "integer"},
                    "notes": {"type": "string"},
                    "fulfillment_type": {
                        "type": "string",
                        "description": "stock | leap | option | proxy | option_strategy",
                    },
                    "fulfillment_details": {
                        "type": "object",
                        "description": (
                            "Related instrument packaging: strike, expiry, option_type, "
                            "contract_multiplier, signal_journal_id, signal_task_id, instrument_symbol"
                        ),
                    },
                },
                "required": ["journal_id"],
            },
        ),
        Tool(
            name="wv2_edit_journal",
            description=(
                "Amend a draft journal before confirm: units, price, notes, stop_price, "
                "trade_date, fulfillment_type / related-instrument fields. "
                "Refuses executed/cancelled/passed (immutable). Does NOT open/close positions. "
                "For executed fills use wv2_amend_journal (correct fill, same lot). "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "journal_id": {"type": "integer"},
                    "units": {"type": ["integer", "number", "null"]},
                    "price": {
                        "type": ["number", "null"],
                        "description": "Suggested / sticky fill price for later confirm",
                    },
                    "execution_price": {
                        "type": ["number", "null"],
                        "description": "Alias for price",
                    },
                    "notes": {"type": ["string", "null"]},
                    "stop_price": {"type": ["number", "null"]},
                    "trade_date": {"type": ["string", "null"], "description": "YYYY-MM-DD"},
                    "direction": {"type": ["string", "null"]},
                    "fulfillment_type": {
                        "type": ["string", "null"],
                        "description": "stock | leap | option | proxy | option_strategy",
                    },
                    "fulfillment_details": {"type": ["object", "null"]},
                    "expiry": {"type": ["string", "null"]},
                    "strike": {"type": ["number", "null"]},
                    "option_type": {"type": ["string", "null"]},
                    "contract_multiplier": {"type": ["integer", "number", "null"]},
                    "instrument_symbol": {"type": ["string", "null"]},
                    "replace_notes": {
                        "type": ["boolean", "null"],
                        "description": "If true, replace notes instead of appending",
                    },
                },
                "required": ["journal_id"],
            },
        ),
        Tool(
            name="wv2_amend_journal",
            description=(
                "Correct an executed enter/pyramid fill in place (same Position lot). "
                "Use when broker fill differs from booked price/units (e.g. 253.66 → 255.02). "
                "Does NOT open a second position. For drafts use wv2_edit_journal + confirm. "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "journal_id": {"type": "integer"},
                    "units": {"type": ["integer", "number", "null"]},
                    "price": {
                        "type": ["number", "null"],
                        "description": "Corrected fill price",
                    },
                    "execution_price": {
                        "type": ["number", "null"],
                        "description": "Alias for price",
                    },
                    "notes": {"type": ["string", "null"]},
                    "stop_price": {"type": ["number", "null"]},
                },
                "required": ["journal_id"],
            },
        ),
        Tool(
            name="wv2_book_trade",
            description=(
                "Ad-hoc paper fill: book a buy/sell without a Daily Analysis draft. "
                "Requires human-authorized portfolio, symbol (on Books = signal underlying), "
                "units, and price. "
                "Related instruments: fulfillment_type=leap|option|proxy with strike+expiry "
                "(options). units=contracts for leap/option; price=premium; "
                "cash impact = units×price×multiplier (default 100). "
                "Refuses second book against an existing draft/executed signal "
                "(use confirm or wv2_amend_journal); force+notes for deliberate second lot. "
                "Never invent fills. On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {
                        "type": "string",
                        "description": "Operational Portfolio id or name",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Signal underlying Market symbol (must be on Books)",
                    },
                    "units": {
                        "type": ["integer", "number"],
                        "description": "Shares (stock/proxy) or contracts (leap/option)",
                    },
                    "price": {
                        "type": "number",
                        "description": "Fill price (stock) or option premium per share",
                    },
                    "direction": {
                        "type": ["string", "null"],
                        "description": "long (default) or short",
                    },
                    "trade_date": {
                        "type": ["string", "null"],
                        "description": "YYYY-MM-DD (default today)",
                    },
                    "notes": {"type": ["string", "null"]},
                    "stop_price": {
                        "type": ["number", "null"],
                        "description": "Optional human stop; ATR default for stock only",
                    },
                    "fulfillment_type": {
                        "type": ["string", "null"],
                        "description": "stock (default) | leap | option | proxy | option_strategy",
                    },
                    "fulfillment_details": {
                        "type": ["object", "null"],
                        "description": "Optional packaging bag (merged with top-level related fields)",
                    },
                    "expiry": {
                        "type": ["string", "null"],
                        "description": "YYYY-MM-DD option expiry (required for leap/option)",
                    },
                    "strike": {
                        "type": ["number", "null"],
                        "description": "Strike price (required for leap/option)",
                    },
                    "option_type": {
                        "type": ["string", "null"],
                        "description": "call (default) or put",
                    },
                    "contract_multiplier": {
                        "type": ["integer", "number", "null"],
                        "description": "Default 100 for leap/option; 1 for stock/proxy",
                    },
                    "instrument_symbol": {
                        "type": ["string", "null"],
                        "description": "Proxy filled symbol when different from signal underlying",
                    },
                    "signal_journal_id": {
                        "type": ["integer", "number", "null"],
                        "description": "Link to motivating signal/draft journal id",
                    },
                    "signal_task_id": {
                        "type": ["integer", "number", "null"],
                        "description": "Link to motivating operations task id",
                    },
                },
                "required": ["portfolio_id_or_name", "symbol", "units", "price"],
            },
        ),
        Tool(
            name="wv2_exit_trade",
            description=(
                "Ad-hoc exit: close an open position without a Daily Analysis draft. "
                "Requires human-authorized portfolio, price, and either symbol or position_id. "
                "Full exit of the matched open position. Never invent exits. "
                "For broker/external stops use reason=external_stop "
                "(speech: 'SYMBOL stopped out — book exit, no Winston signal'). "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {
                        "type": "string",
                        "description": "Operational Portfolio id or name",
                    },
                    "price": {"type": "number", "description": "Exit fill price (required)"},
                    "symbol": {
                        "type": ["string", "null"],
                        "description": "Market symbol of open position (if position_id omitted)",
                    },
                    "position_id": {
                        "type": ["integer", "number", "null"],
                        "description": "Open position id (preferred when known)",
                    },
                    "trade_date": {
                        "type": ["string", "null"],
                        "description": "YYYY-MM-DD (default today)",
                    },
                    "notes": {"type": ["string", "null"]},
                    "reason": {
                        "type": ["string", "null"],
                        "description": (
                            "Exit reason packaging: external_stop | discretionary | ad_hoc | other. "
                            "Aliases: stopped_out, broker_stop, disc, desk. Default ad_hoc. "
                            "Stored as fulfillment_details.exit_reason (winston_signal=false)."
                        ),
                    },
                    "units": {
                        "type": ["integer", "number", "null"],
                        "description": "Reserved; full exit for now",
                    },
                },
                "required": ["portfolio_id_or_name", "price"],
            },
        ),
        Tool(
            name="wv2_exit_all_trades",
            description=(
                "Bulk ad-hoc exit: close ALL open lots for a symbol on an Operational Portfolio. "
                "One journal per lot at the same price. Use for multi-lot/pyramid flatten. "
                "Requires human-authorized portfolio, symbol, and price. Never invent exits. "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {
                        "type": "string",
                        "description": "Operational Portfolio id or name",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Market symbol — all open lots for this market",
                    },
                    "price": {"type": "number", "description": "Exit fill price for every lot"},
                    "trade_date": {
                        "type": ["string", "null"],
                        "description": "YYYY-MM-DD (default today)",
                    },
                    "notes": {"type": ["string", "null"]},
                    "reason": {
                        "type": ["string", "null"],
                        "description": (
                            "Exit reason: external_stop | discretionary | ad_hoc | other "
                            "(same packaging as wv2_exit_trade)"
                        ),
                    },
                },
                "required": ["portfolio_id_or_name", "symbol", "price"],
            },
        ),
        Tool(
            name="wv2_update_stops",
            description=(
                "Bulk stop move: set the same stop on ALL open lots for a symbol on an OP. "
                "Use for pyramid books / trail-all. Never invent stop prices. "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {
                        "type": "string",
                        "description": "Operational Portfolio id or name",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "Market symbol — all open lots for this market",
                    },
                    "stop_price": {
                        "type": "number",
                        "description": "New stop price applied to every open lot",
                    },
                    "notes": {"type": ["string", "null"]},
                },
                "required": ["portfolio_id_or_name", "symbol", "stop_price"],
            },
        ),
        Tool(
            name="wv2_add_cash_event",
            description=(
                "Add capital to an Operational Portfolio via CashEvent (inflow or adjustment). "
                "Use for speech like 'add $5600 cash to Portfolio White'. "
                "Does not open/close positions. Never invent amounts. "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {
                        "type": "string",
                        "description": "Operational Portfolio id or name",
                    },
                    "amount": {
                        "type": "number",
                        "description": "Cash amount (positive for inflow; adjustment may be negative)",
                    },
                    "event_type": {
                        "type": ["string", "null"],
                        "description": "inflow (default) or adjustment",
                    },
                    "event_date": {
                        "type": ["string", "null"],
                        "description": "YYYY-MM-DD (default today)",
                    },
                    "notes": {"type": ["string", "null"], "description": "Audit notes"},
                },
                "required": ["portfolio_id_or_name", "amount"],
            },
        ),
        Tool(
            name="wv2_close_portfolio",
            description=(
                "Close an Operational Portfolio series (ADR-006). Ends signal evaluation; "
                "keeps journals/history. Paper soft-close allowed with open residue. "
                "Real requires flat (no open positions / draft journals) unless force=true. "
                "Not the same as exiting a single position (use wv2_exit_trade). "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {
                        "type": "string",
                        "description": "Operational Portfolio id or name",
                    },
                    "force": {
                        "type": ["boolean", "null"],
                        "description": "Allow real soft-close with open residue (default false)",
                    },
                    "notes": {"type": ["string", "null"], "description": "Audit notes"},
                },
                "required": ["portfolio_id_or_name"],
            },
        ),
        Tool(
            name="wv2_successor_portfolio",
            description=(
                "Shape rebalance via successor (ADR-006): close source OP A, open A′ with new "
                "Books and/or TradingStrategy. Journals stay on A. A′ gets a new initial CashEvent. "
                "Use when engaged OP needs add-market / recipe change. "
                "On success paste reply_text as the entire user reply."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {
                        "type": "string",
                        "description": "Source Operational Portfolio id or name",
                    },
                    "symbols": {
                        "type": ["array", "string", "null"],
                        "items": {"type": "string"},
                        "description": "New Books symbols (default: copy source Books)",
                    },
                    "trading_strategy_id": {
                        "type": ["integer", "number", "null"],
                        "description": "TradingStrategy id for A′ (default: source TS)",
                    },
                    "initial_capital": {
                        "type": ["number", "null"],
                        "description": "Initial CashEvent on A′ (default: source capital_base)",
                    },
                    "fingerprint": {"type": ["string", "null"]},
                    "seed_name": {"type": ["string", "null"]},
                    "name": {"type": ["string", "null"], "description": "Override display name"},
                    "execution_mode": {
                        "type": ["string", "null"],
                        "description": "paper (default from source) or real",
                    },
                    "activate": {
                        "type": ["boolean", "null"],
                        "description": "Activate A′ after create (default false)",
                    },
                    "force": {
                        "type": ["boolean", "null"],
                        "description": "Force close residue and/or Active mutex",
                    },
                    "force_close": {
                        "type": ["boolean", "null"],
                        "description": "Force close of A with residue (real)",
                    },
                    "notes": {"type": ["string", "null"]},
                },
                "required": ["portfolio_id_or_name"],
            },
        ),
        Tool(
            name="wv2_mark_task_done",
            description=(
                "Complete an operations task; by default confirms the linked draft journal first."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "notes": {"type": "string"},
                    "confirm_journal": {"type": "boolean", "description": "Default true"},
                    "execution_price": {"type": "number"},
                    "units": {"type": "integer"},
                    "fulfillment_type": {"type": "string"},
                    "fulfillment_details": {"type": "object"},
                },
                "required": ["task_id"],
            },
        ),
        Tool(
            name="wv2_list_pending_actions",
            description="List actionable pending operations tasks (enter/exit/pyramid).",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string"},
                    "as_of": {"type": "string", "description": "YYYY-MM-DD"},
                },
            },
        ),
        Tool(
            name="wv2_get_journal",
            description=(
                "Fetch one Wv2 journal by id (draft, executed, passed). "
                "Drafts include proposed_units / proposed_price / proposed_stop / editable."
            ),
            inputSchema={
                "type": "object",
                "properties": {"journal_id": {"type": "integer"}},
                "required": ["journal_id"],
            },
        ),
        Tool(
            name="wv2_get_portfolio_status",
            description=(
                "Portfolio snapshot: capital_base, cash events, open positions, recent journals."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string"},
                    "journal_limit": {"type": "integer", "description": "Recent journals (default 10)"},
                },
                "required": ["portfolio_id_or_name"],
            },
        ),
        Tool(
            name="wv2_list_trading_strategies",
            description="List reusable Wv2 TradingStrategy definitions for transfer/apply flows.",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="wv2_compare_equity",
            description=(
                "Compare equity curves for 1–6 Operational Portfolios (e.g. Blue vs Mango). "
                "Returns metrics + a single-page PDF chart with telegram_media_path for "
                "Telegram media attach (same volume as daily activity PDFs). "
                "Labels use OP display names and short fingerprints. "
                "On success paste reply_text and attach media=[telegram_media_path]."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolios": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Portfolio ids or names (e.g. [\"Blue\", \"Mango\"])",
                    },
                    "portfolio_ids_or_names": {
                        "type": ["array", "string", "null"],
                        "description": "Alias for portfolios (array or comma-separated string)",
                    },
                    "as_of": {
                        "type": ["string", "null"],
                        "description": "YYYY-MM-DD report end date (default today)",
                    },
                    "normalize": {
                        "type": ["boolean", "null"],
                        "description": "If true, rebase each series to 100 at start",
                    },
                    "title": {"type": ["string", "null"]},
                },
            },
        ),
        Tool(
            name="dm_request_full_sync",
            description=(
                "Trigger DM ecosystem sync for all consumer symbols (WUT + Wv2). "
                "Default async=true (enqueue job); poll dm_get_cromwell_events."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "async": {"type": "boolean", "description": "Enqueue Sidekiq job (default true)"},
                    "notify_cromwell": {"type": "boolean", "description": "Emit Cromwell events (default true)"},
                },
            },
        ),
        Tool(
            name="wv2_get_daily_activity_report_pdf",
            description=(
                "Get paths to the daily activity PDF for Telegram delivery. "
                "Use telegram_media_path with the message tool media=[] after fetching the report."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "YYYY-MM-DD"},
                },
            },
        ),
        Tool(
            name="dm_get_cromwell_events",
            description=(
                "Get Data Manager Cromwell sync events (download started, per-symbol updates). "
                "Post event.message strings to Sawtooth Main during the 3:30 PM MT sync window."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "since": {"type": "string", "description": "ISO8601 — return events after this time"},
                    "limit": {"type": "integer", "description": "Max events (default 50)"},
                },
            },
        ),
        # WUT lab portfolio control plane (add market, sync, daily ops — not Wv2 live)
        Tool(
            name="wut_list_portfolios",
            description="List WUT lab portfolios with markets and active account status.",
            inputSchema={"type": "object"},
        ),
        Tool(
            name="wut_list_portfolio_runs",
            description="List recent backtest runs for a WUT portfolio.",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string", "description": "Portfolio id or name"},
                },
                "required": ["portfolio_id_or_name"],
            },
        ),
        Tool(
            name="wut_add_market",
            description=(
                "Add symbol to a WUT lab portfolio (Book + backtest market config + DM sync). "
                "Resolves aliases (e.g. GOLD → CLETF)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string"},
                    "symbol": {"type": "string"},
                    "sync": {"type": "boolean", "description": "Queue DataSetDmSyncJob (default true)"},
                },
                "required": ["portfolio_id_or_name", "symbol"],
            },
        ),
        Tool(
            name="wut_sync_portfolio_data",
            description="Queue DM sync for portfolio markets (or explicit symbols).",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string"},
                    "symbols": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["portfolio_id_or_name"],
            },
        ),
        Tool(
            name="wut_run_daily_operations",
            description=(
                "Run WUT daily operations for a portfolio's ActiveAccount "
                "(signals, tasks, DailyOperationsReport). Requires ActiveAccount in WUT Operations."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string"},
                    "date": {"type": "string", "description": "YYYY-MM-DD (default today)"},
                },
                "required": ["portfolio_id_or_name"],
            },
        ),
        Tool(
            name="wut_get_daily_operations_report",
            description="Fetch WUT DailyOperationsReport JSON for a portfolio/date.",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id_or_name": {"type": "string"},
                    "date": {"type": "string", "description": "YYYY-MM-DD (default today)"},
                },
                "required": ["portfolio_id_or_name"],
            },
        ),
        # Convenience
        Tool(
            name="wv2_activate_portfolio",
            description=(
                "Activate portfolio (sets active=true). ADR-006 mutex: refuses if another Active OP "
                "shares seed_name or identical Books unless force=true (short dual-active experiment)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "id_or_name": {"type": "string", "description": "Portfolio id or name"},
                    "force": {
                        "type": "boolean",
                        "description": "Allow dual Active same seed_name or identical Books set",
                        "default": False,
                    },
                },
                "required": ["id_or_name"],
            },
        ),
        Tool(
            name="wv2_deactivate_portfolio",
            description="Deactivate portfolio (sets active=false). Does not close positions or rewrite journals.",
            inputSchema={
                "type": "object",
                "properties": {"id_or_name": {"type": "string", "description": "Portfolio id or name"}},
                "required": ["id_or_name"],
            },
        ),
    ]
    return [
        Tool(
            name=t.name,
            description=t.description,
            inputSchema=with_observability(t.inputSchema or {"type": "object"}),
        )
        for t in tools
    ]


def _query_params(arguments: dict[str, Any]) -> dict[str, str]:
    """Flatten MCP tool args for httpx GET query strings (strings only, skip null)."""
    out: dict[str, str] = {}
    for key, val in (arguments or {}).items():
        if val is None:
            continue
        out[key] = str(val)
    return out


def _optional_int(val: Any) -> int | None:
    """Coerce optional int tool args; treat null/blank as missing; accept numeric strings."""
    if val is None:
        return None
    if isinstance(val, bool):
        return None
    if isinstance(val, int):
        return val
    s = str(val).strip()
    if not s or s.lower() in {"null", "none"}:
        return None
    try:
        return int(s)
    except (TypeError, ValueError):
        return None


def _portfolio_id_payload(args: dict[str, Any]) -> dict[str, Any]:
    """Map MCP id_or_name (or id/name) to Wv2 internal activate/deactivate body."""
    payload: dict[str, Any] = {}
    if args.get("id") is not None:
        payload["id"] = args["id"]
    elif args.get("name") is not None:
        payload["name"] = args["name"]
    else:
        idn = args.get("id_or_name")
        if idn is None:
            payload = dict(args)
        else:
            s = str(idn).strip()
            if s.isdigit():
                payload["id"] = int(s)
            else:
                payload["name"] = s
    if "force" in args and args.get("force") is not None:
        payload["force"] = bool(args["force"])
    return payload


def _report_missing(data: dict[str, Any]) -> bool:
    note = str(data.get("note") or "")
    return "No notification file yet" in note


def _analysis_blocked(data: dict[str, Any]) -> bool:
    err = data.get("error")
    return err in {
        "daily_analysis_not_available_yet",
        "historical_daily_analysis_requires_force",
    } or bool(data.get("available_after_mt"))


def _attach_delivery_hints(data: dict[str, Any]) -> dict[str, Any]:
    """Tell Cromwell to post inline summary + PDF via the message tool."""
    media = data.get("telegram_media_path")
    pdf_exists = data.get("pdf_exists", True)
    if media and pdf_exists:
        filename = media.rsplit("/", 1)[-1]
        data.setdefault("_meta", {})
        data["_meta"]["delivery"] = {
            "inline_summary": True,
            "attach_pdf": True,
            "telegram_media_path": media,
            "pdf_filename": filename,
            "instruction": (
                "Nanobot auto-attaches the PDF when possible. Otherwise use the message tool: "
                "content = concise inline summary (portfolios, pending actions, last journals); "
                f"media = ['{media}'] — this sends a viewable Telegram document, not a filename."
            ),
        }
    elif data.get("pdf_error"):
        data.setdefault("_meta", {})
        data["_meta"]["delivery"] = {
            "attach_pdf": False,
            "pdf_error": data["pdf_error"],
            "instruction": "PDF generation failed; deliver the inline summary only and mention the PDF is temporarily unavailable.",
        }
    return data


# Plain-English action labels for Telegram (ticket A reply contract).
_TRANSFER_ACTION_LABELS: dict[str, str] = {
    "created": "New Operational Portfolio created",
    "legacy_updated": "Updated existing OP (legacy bare-name path)",
    "forked": "New OP forked (different methodology / fingerprint)",
    "adopted": "Adopted fingerprint onto existing OP",
    "engaged_refuse": "Refused — OP is engaged (journals exist)",
    "closed_refuse": "Refused — OP is closed",
}


def _short_fingerprint(fp: Any) -> str | None:
    if not fp or not isinstance(fp, str):
        return None
    fp = fp.strip()
    if not fp:
        return None
    return fp[:8]


def _json_bool(value: Any) -> str:
    """Lowercase true/false for Telegram; avoid Python True/False."""
    if value is True or value is False:
        return "true" if value else "false"
    if value is None:
        return "unknown"
    return str(value).lower() if str(value).lower() in ("true", "false") else str(value)


def _warning_lines(data: dict[str, Any], *, limit: int = 2) -> list[str]:
    warnings = data.get("warnings")
    if not isinstance(warnings, list):
        return []
    lines: list[str] = []
    for w in warnings[:limit]:
        text = str(w).strip()
        if text:
            lines.append(f"Warning: {text}")
    return lines


def _attach_agent_summary(name: str, data: Any) -> Any:
    """Paste-ready summary/reply_text for weak local models.

    Ticket A/C: transfer success JSON is easy to bury under market inventories.
    Models must paste `reply_text` (or at least `summary`) — not rewrite.
    """
    if not isinstance(data, dict):
        return data
    if data.get("status") == "error":
        return data

    p = data.get("portfolio") if isinstance(data.get("portfolio"), dict) else {}
    pid = p.get("id")
    pname = p.get("name") or "unknown"
    active = p.get("active")
    action = data.get("action")
    mode = p.get("execution_mode") or "paper"
    short_fp = _short_fingerprint(p.get("fingerprint"))
    warn_lines = _warning_lines(data)

    if name == "wv2_transfer_portfolio_from_wut" and (action or pid is not None):
        action_key = str(action or "ok")
        label = _TRANSFER_ACTION_LABELS.get(action_key, action_key)
        # Line 1 always has action + #id (acceptance criteria).
        line1 = f"Transfer OK — {label}: #{pid} “{pname}”"
        if short_fp:
            line1 = f"{line1} · {short_fp}"
        line2 = f"active={_json_bool(active)}, execution_mode={mode}"
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2] if not warn_lines else body)
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "Must include action and #id on line 1. "
            "FORBIDDEN in user text: market lists, capital inventories, "
            "“has been updated…”, “Here’s the confirmation”, "
            "“Would you like…”, “This is the complete response”, "
            "“No further actions or tool calls” (hint is for you, not the user)."
        )
    elif name in ("wv2_activate_portfolio", "wv2_deactivate_portfolio") and (
        action or pid is not None
    ):
        is_activate = name == "wv2_activate_portfolio"
        verb_done = "Activated" if is_activate else "Deactivated"
        action_key = str(action or ("activated" if is_activate else "deactivated"))
        fp_bit = f" · {short_fp}" if short_fp else ""
        line1 = f"{verb_done} #{pid} “{pname}”{fp_bit} — action={action_key}"
        line2 = f"active={_json_bool(active)}"
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN in user text: extra tools, menus, “Would you like…”, "
            "“Here’s the confirmation”, “This is the complete response”, "
            "“No further actions or tool calls” (hint is for you, not the user)."
        )
    elif name == "wv2_compare_equity" and data.get("status") == "ok":
        title = data.get("title") or "Equity compare"
        as_of = data.get("as_of") or "?"
        media = data.get("telegram_media_path")
        lines = [str(title), f"as_of {as_of}"]
        metrics = data.get("metrics") if isinstance(data.get("metrics"), list) else []
        for m in metrics:
            if not isinstance(m, dict):
                continue
            lines.append(
                f"{m.get('label')} #{m.get('portfolio_id')}: "
                f"ret={m.get('return_pct')}% dd={m.get('max_drawdown_pct')}% "
                f"end=${m.get('end_equity')}"
            )
        if media:
            lines.append(f"chart attached via media path")
        data["summary"] = " | ".join(lines[:3])
        data["reply_text"] = "\n".join(lines)
        data.setdefault("_meta", {})
        data["_meta"]["delivery"] = {
            "attach_pdf": bool(media),
            "telegram_media_path": media,
            "instruction": (
                "Paste reply_text as the user message. "
                f"Attach chart: message tool media=['{media}'] "
                "(viewable Telegram document). Do not paste filesystem paths as text links."
            ),
        }
        data["reply_hint"] = (
            "User message = reply_text only. Attach telegram_media_path via media=[...]. "
            "FORBIDDEN: inventing series, menus, path-as-hyperlink text."
        )
    elif name == "wv2_amend_journal" and data.get("status") == "ok":
        j = data.get("journal") if isinstance(data.get("journal"), dict) else {}
        jid = j.get("id")
        market = j.get("market") or "?"
        units = j.get("units")
        px = j.get("execution_price")
        capital = data.get("capital_base")
        line1 = f"Correct-fill journal #{jid} {market} {units}@{px} capital=${capital}"
        data["summary"] = line1
        data["reply_text"] = line1
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript."
        )
    elif name == "wv2_edit_journal" and data.get("status") == "ok":
        j = data.get("journal") if isinstance(data.get("journal"), dict) else {}
        jid = j.get("id")
        market = j.get("market") or "?"
        units = j.get("proposed_units")
        px = j.get("proposed_price")
        stop = j.get("proposed_stop")
        flow = j.get("flow")
        line1 = (
            f"Draft edited journal #{jid} {market} — still draft "
            f"(units={units} price={px} stop={stop})"
        ).strip()
        line2_parts = [f"status={j.get('status') or 'draft'}", f"flow={flow}"]
        changes = data.get("changes") if isinstance(data.get("changes"), dict) else {}
        if changes:
            bits = [f"{k}:{v.get('from')}→{v.get('to')}" for k, v in changes.items() if isinstance(v, dict)]
            if bits:
                line2_parts.append("changes=" + " · ".join(bits[:6]))
        line2 = ", ".join(str(x) for x in line2_parts if x is not None)
        line3 = f"next: confirm journal #{jid} (or confirm with overrides)"
        body = [line1, line2, line3, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "Do not confirm unless human authorized. FORBIDDEN: inventing fills/menus."
        )
    elif name == "wv2_book_trade" and data.get("status") == "ok":
        j = data.get("journal") if isinstance(data.get("journal"), dict) else {}
        pos = data.get("position") if isinstance(data.get("position"), dict) else {}
        ff = data.get("fulfillment") if isinstance(data.get("fulfillment"), dict) else {}
        jid = j.get("id")
        market = j.get("market") or pos.get("market") or "?"
        instrument = (
            ff.get("instrument_label")
            or pos.get("instrument_label")
            or market
        )
        units = pos.get("units") or j.get("units")
        px = pos.get("execution_price")
        direction = pos.get("direction") or "long"
        stop = pos.get("original_stop") or pos.get("updated_stop")
        ftype = ff.get("type") or j.get("fulfillment_type") or "stock"
        mult = ff.get("contract_multiplier")
        cap = data.get("capital_base")
        if cap is None and isinstance(p, dict):
            cap = p.get("capital_base")
        pid_bit = f"#{pid} " if pid is not None else ""
        type_bit = f" type={ftype}" if str(ftype) != "stock" else ""
        line1 = (
            f"Booked {direction} {units} {instrument} @ {px}{type_bit} — "
            f"journal #{jid} OP {pid_bit}“{pname}”"
        ).strip()
        line2_parts = [f"capital_base={cap}", f"active={_json_bool(active)}"]
        if stop is not None:
            line2_parts.insert(0, f"stop={stop}")
        if mult is not None and int(mult or 0) > 1:
            line2_parts.insert(0, f"multiplier={mult}")
            flow = j.get("flow")
            if flow is not None:
                line2_parts.insert(1, f"cash_impact={flow}")
        sig_task = ff.get("signal_task_id")
        sig_j = ff.get("signal_journal_id")
        if sig_task or sig_j:
            bits = []
            if sig_task:
                bits.append(f"signal_task={sig_task}")
            if sig_j:
                bits.append(f"signal_journal={sig_j}")
            line2_parts.append(" ".join(bits))
        line2 = ", ".join(str(x) for x in line2_parts)
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN: inventing fills, menus, “Would you like…”, "
            "“complete response” / “no further tool calls” (hint is for you)."
        )
    elif name == "wv2_exit_trade" and data.get("status") == "ok":
        j = data.get("journal") if isinstance(data.get("journal"), dict) else {}
        pos = data.get("position") if isinstance(data.get("position"), dict) else {}
        jid = j.get("id")
        market = j.get("market") or pos.get("market") or "?"
        units = pos.get("units")
        px = pos.get("execution_price")
        pos_id = pos.get("id")
        cap = data.get("capital_base")
        if cap is None and isinstance(p, dict):
            cap = p.get("capital_base")
        reason = data.get("exit_reason") or "ad_hoc"
        pid_bit = f"#{pid} " if pid is not None else ""
        pos_bit = f" position #{pos_id}" if pos_id is not None else ""
        units_bit = f"{units} " if units is not None else ""
        if reason == "external_stop":
            line1 = (
                f"{market} stopped out — book exit, no Winston signal "
                f"({units_bit}@ {px}) — journal #{jid} OP {pid_bit}“{pname}”{pos_bit}"
            ).strip()
        else:
            line1 = (
                f"Exited {units_bit}{market} @ {px} — "
                f"journal #{jid} OP {pid_bit}“{pname}”{pos_bit}"
            ).strip()
        line2 = (
            f"reason={reason}, capital_base={cap}, "
            f"active={_json_bool(active)}, open=false"
        )
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN: inventing exits, menus, “Would you like…”, "
            "“complete response” / “no further tool calls” (hint is for you)."
        )
    elif name == "wv2_exit_all_trades" and data.get("status") == "ok":
        market = data.get("symbol") or "?"
        n = data.get("lots_exited")
        px = data.get("price")
        reason = data.get("exit_reason") or "ad_hoc"
        cap = data.get("capital_base")
        if cap is None and isinstance(p, dict):
            cap = p.get("capital_base")
        pid_bit = f"#{pid} " if pid is not None else ""
        line1 = (
            f"Exited all {n} lot(s) {market} @ {px} — "
            f"OP {pid_bit}“{pname}” reason={reason}"
        ).strip()
        line2 = f"capital_base={cap}, active={_json_bool(active)}, open=false for {market}"
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN: inventing exits or partial flatten claims."
        )
    elif name == "wv2_update_stops" and data.get("status") == "ok":
        market = data.get("symbol") or "?"
        n = data.get("lots_updated")
        stop = data.get("stop_price")
        pid_bit = f"#{pid} " if pid is not None else ""
        line1 = (
            f"Moved stops on {n} lot(s) {market} → {stop} — "
            f"OP {pid_bit}“{pname}”"
        ).strip()
        line2 = f"active={_json_bool(active)}"
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN: inventing stop prices."
        )
    elif name == "wv2_add_cash_event" and data.get("status") == "ok":
        ce = data.get("cash_event") if isinstance(data.get("cash_event"), dict) else {}
        et = ce.get("event_type") or "inflow"
        amt = ce.get("amount")
        ed = ce.get("event_date")
        ce_id = ce.get("id")
        cap = data.get("capital_base")
        cap_before = data.get("capital_base_before")
        pid_bit = f"#{pid} " if pid is not None else ""
        line1 = (
            f"Cash {et} ${amt} — event #{ce_id} OP {pid_bit}“{pname}”"
        ).strip()
        line2_parts = [f"capital_base={cap}"]
        if cap_before is not None:
            line2_parts.insert(0, f"before={cap_before}")
        if ed:
            line2_parts.append(f"date={ed}")
        line2 = ", ".join(str(x) for x in line2_parts)
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN: inventing amounts, menus, “Would you like…”, "
            "“complete response” / “no further tool calls” (hint is for you)."
        )
    elif name == "wv2_close_portfolio" and data.get("status") == "ok":
        p = data.get("portfolio") if isinstance(data.get("portfolio"), dict) else {}
        pid = p.get("id")
        pname = p.get("name") or "?"
        action = data.get("action") or "closed"
        closed_at = p.get("closed_at")
        open_res = data.get("open_position_count")
        draft_res = data.get("draft_journal_count")
        pid_bit = f"#{pid} " if pid is not None else ""
        line1 = f"Closed OP series {pid_bit}“{pname}” — {action}".strip()
        line2_parts = [f"closed_at={closed_at}", f"active={_json_bool(p.get('active'))}"]
        if open_res is not None:
            line2_parts.append(f"open_residue={open_res}")
        if draft_res is not None:
            line2_parts.append(f"draft_residue={draft_res}")
        line2 = ", ".join(str(x) for x in line2_parts)
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN: inventing closes, menus, “Would you like…”, "
            "“complete response” / “no further tool calls” (hint is for you)."
        )
    elif name == "wv2_successor_portfolio" and data.get("status") == "ok":
        src = data.get("source_portfolio") if isinstance(data.get("source_portfolio"), dict) else {}
        suc = data.get("successor_portfolio") if isinstance(data.get("successor_portfolio"), dict) else {}
        src_id = src.get("id")
        suc_id = suc.get("id")
        suc_name = suc.get("name") or "?"
        mkts = data.get("markets") or []
        if isinstance(mkts, list):
            mkts_s = ",".join(str(m) for m in mkts)
        else:
            mkts_s = str(mkts)
        cap = data.get("capital_base")
        line1 = (
            f"Successor OP #{suc_id} “{suc_name}” from closed #{src_id}"
        ).strip()
        line2 = (
            f"markets=[{mkts_s}], capital_base={cap}, "
            f"active={_json_bool(suc.get('active'))}, journals_on=#{src_id}"
        )
        body = [line1, line2, *warn_lines]
        data["summary"] = " | ".join(body[:2])
        data["reply_text"] = "\n".join(body)
        data["reply_hint"] = (
            "User message = reply_text only (verbatim). No preamble/postscript. "
            "FORBIDDEN: inventing successors, menus, “Would you like…”, "
            "“complete response” / “no further tool calls” (hint is for you)."
        )
    return data


def _finish_tool_response(
    name: str,
    data: Any,
    ctx: Any,
    audit_hops: list[tuple[str, str, int]],
    start: float,
    *,
    status: str = "ok",
    error_code: str | None = None,
    error_summary: str | None = None,
) -> list[TextContent]:
    import json

    duration_ms = int((time.time() - start) * 1000)
    monolith, endpoint, http_status = summarize_hops(audit_hops)
    append_audit(
        ctx,
        tool=name,
        duration_ms=duration_ms,
        status=status,
        monolith=monolith,
        endpoint=endpoint,
        http_status=http_status,
        error_code=error_code,
        error_summary=error_summary,
    )
    payload = _attach_agent_summary(name, data)
    payload = attach_long_running_meta(payload, name)
    payload = attach_meta(payload, ctx)
    print(f"[winston_mcp] {name} {status} in {duration_ms}ms corr={ctx.correlation_id}", flush=True)
    return [TextContent(type="text", text=json.dumps(payload, indent=2, default=str))]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Dispatch to the real monolith internals (Wv2 + WUT + DM).
    All tools return a TextContent payload containing pretty JSON.
    """
    ctx = begin_invocation(arguments)
    args = strip_observability_args(dict(arguments or {}))
    audit_hops: list[tuple[str, str, int]] = []
    hop_kw = {"ctx": ctx, "audit_hops": audit_hops}
    start = time.time()

    limited, retry_after = check_rate_limit(name)
    if limited:
        err = build_error_payload(
            name,
            code="rate_limited",
            message=f"Rate limit exceeded for {name}",
            retry_after_seconds=retry_after,
        )
        return _finish_tool_response(
            name, err, ctx, audit_hops, start,
            status="error", error_code="rate_limited",
            error_summary=err["message"],
        )

    if name in LONG_RUNNING_TOOLS:
        log_progress(ctx.correlation_id, name, "started")

    try:
        if name == "wv2_list_portfolios":
            data = await _get(WV2_BASE, "/internal/portfolios", **hop_kw)

        elif name == "wv2_market_snapshot":
            params = {}
            if args.get("all_portfolios"):
                params["all"] = "1"
            data = await _get(
                WV2_BASE, "/internal/market_snapshot",
                params=params if params else None,
                **hop_kw,
            )

        elif name == "wv2_activate_portfolio":
            data = await _post(
                WV2_BASE, "/internal/portfolios/activate",
                json=_portfolio_id_payload(args), **hop_kw,
            )

        elif name == "wv2_deactivate_portfolio":
            data = await _post(
                WV2_BASE, "/internal/portfolios/deactivate",
                json=_portfolio_id_payload(args), **hop_kw,
            )

        elif name == "wv2_perform_daily_analysis":
            payload = dict(args)
            if payload.pop("wait_for_report", None):
                payload["sync"] = True
            payload.setdefault("sync", True)
            if payload.get("portfolio_id_or_name") is not None:
                payload["id_or_name"] = payload.pop("portfolio_id_or_name")
            # Pass through allow_historical / deliver_telegram for Wv2 guards.
            if "allow_historical" in payload:
                payload["allow_historical"] = bool(payload.get("allow_historical"))
            if "deliver_telegram" in payload:
                payload["deliver_telegram"] = bool(payload.get("deliver_telegram"))
            data = await _post(
                WV2_BASE, "/internal/portfolios/evaluate", json=payload,
                timeout=180.0 if payload.get("sync") else 30.0,
                **hop_kw,
            )

        elif name == "wv2_get_daily_activity_report":
            params = _query_params(args)
            if args.get("fetch_only"):
                params["fetch_only"] = "1"
            fetch_only = bool(args.get("fetch_only"))
            try:
                data = await _get(WV2_BASE, "/internal/cromwell_notifications", params=params, **hop_kw)
            except httpx.HTTPStatusError as exc:
                if fetch_only and exc.response.status_code == 422:
                    data = exc.response.json()
                else:
                    raise
            if (
                _report_missing(data)
                and not _analysis_blocked(data)
                and not fetch_only
                and data.get("error") != "report_not_ready"
            ):
                run_args = {"sync": True}
                if args.get("date"):
                    run_args["date"] = args["date"]
                if args.get("portfolio_id_or_name") is not None:
                    run_args["id_or_name"] = args["portfolio_id_or_name"]
                if args.get("allow_historical"):
                    run_args["allow_historical"] = True
                if args.get("deliver_telegram"):
                    run_args["deliver_telegram"] = True
                try:
                    result = await _post(
                        WV2_BASE, "/internal/portfolios/evaluate", json=run_args, timeout=180.0,
                        **hop_kw,
                    )
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code == 422:
                        data = exc.response.json()
                    else:
                        raise
                else:
                    if result.get("status") == "blocked":
                        data = result
                    else:
                        data = result.get("report") or await _get(
                            WV2_BASE, "/internal/cromwell_notifications", params=params,
                            **hop_kw,
                        )
                        if result.get("status") == "completed":
                            data.setdefault("_meta", {})
                            data["_meta"].update({
                                "generated_on_demand": True,
                                "notification_path": result.get("notification_path"),
                            })
            data = _attach_delivery_hints(data)

        elif name == "wv2_confirm_journal":
            data = await _post(WV2_BASE, "/internal/journals/confirm", json=args, **hop_kw)

        elif name == "wv2_edit_journal":
            edit_payload: dict[str, Any] = {"journal_id": args.get("journal_id")}
            for key in (
                "units",
                "price",
                "execution_price",
                "notes",
                "stop_price",
                "trade_date",
                "direction",
                "fulfillment_type",
                "expiry",
                "strike",
                "option_type",
                "contract_multiplier",
                "instrument_symbol",
                "replace_notes",
            ):
                val = args.get(key)
                if val is not None and val != "":
                    edit_payload[key] = val
            details = args.get("fulfillment_details")
            if isinstance(details, dict) and details:
                edit_payload["fulfillment_details"] = details
            data = await _post(WV2_BASE, "/internal/journals/edit", json=edit_payload, **hop_kw)

        elif name == "wv2_amend_journal":
            amend_payload: dict[str, Any] = {
                "journal_id": args.get("journal_id"),
                "source": "mcp",
            }
            for key in ("units", "price", "execution_price", "notes", "stop_price"):
                val = args.get(key)
                if val is not None and val != "":
                    amend_payload[key] = val
            data = await _post(WV2_BASE, "/internal/journals/amend", json=amend_payload, **hop_kw)

        elif name == "wv2_book_trade":
            # Coerce numeric fields; drop nulls small models often send.
            units_raw = args.get("units")
            if isinstance(units_raw, float):
                units_val: Any = int(units_raw)
            else:
                units_val = _optional_int(units_raw)
                if units_val is None:
                    units_val = units_raw
            book_payload: dict[str, Any] = {
                "portfolio_id_or_name": args.get("portfolio_id_or_name"),
                "symbol": args.get("symbol"),
                "units": units_val,
                "price": args.get("price"),
            }
            for key in (
                "direction",
                "trade_date",
                "notes",
                "stop_price",
                "fulfillment_type",
                "expiry",
                "strike",
                "option_type",
                "contract_multiplier",
                "instrument_symbol",
                "signal_journal_id",
                "signal_task_id",
            ):
                val = args.get(key)
                if val is not None and val != "":
                    book_payload[key] = val
            details = args.get("fulfillment_details")
            if isinstance(details, dict) and details:
                book_payload["fulfillment_details"] = details
            data = await _post(WV2_BASE, "/internal/journals/book", json=book_payload, **hop_kw)

        elif name == "wv2_exit_trade":
            exit_payload: dict[str, Any] = {
                "portfolio_id_or_name": args.get("portfolio_id_or_name"),
                "price": args.get("price"),
            }
            pos_raw = args.get("position_id")
            if pos_raw is not None and pos_raw != "":
                if isinstance(pos_raw, float):
                    exit_payload["position_id"] = int(pos_raw)
                else:
                    pos_id = _optional_int(pos_raw)
                    exit_payload["position_id"] = pos_id if pos_id is not None else pos_raw
            for key in ("symbol", "trade_date", "notes", "units", "reason", "exit_reason"):
                val = args.get(key)
                if val is not None and val != "":
                    exit_payload[key] = val
            try:
                data = await _post(
                    WV2_BASE, "/internal/journals/exit", json=exit_payload, **hop_kw
                )
            except httpx.HTTPStatusError as exc:
                # Surface AdHocExitService error JSON (422) for agent-friendly codes.
                if exc.response.status_code == 422:
                    data = exc.response.json()
                else:
                    raise

        elif name == "wv2_exit_all_trades":
            exit_all_payload: dict[str, Any] = {
                "portfolio_id_or_name": args.get("portfolio_id_or_name"),
                "symbol": args.get("symbol"),
                "price": args.get("price"),
            }
            for key in ("trade_date", "notes", "reason", "exit_reason"):
                val = args.get(key)
                if val is not None and val != "":
                    exit_all_payload[key] = val
            try:
                data = await _post(
                    WV2_BASE, "/internal/journals/exit_all", json=exit_all_payload, **hop_kw
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 422:
                    data = exc.response.json()
                else:
                    raise

        elif name == "wv2_update_stops":
            stops_payload: dict[str, Any] = {
                "portfolio_id_or_name": args.get("portfolio_id_or_name"),
                "symbol": args.get("symbol"),
                "stop_price": args.get("stop_price") or args.get("price"),
            }
            notes_val = args.get("notes")
            if notes_val is not None and notes_val != "":
                stops_payload["notes"] = notes_val
            try:
                data = await _post(
                    WV2_BASE, "/internal/positions/stops_bulk", json=stops_payload, **hop_kw
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 422:
                    data = exc.response.json()
                else:
                    raise

        elif name == "wv2_add_cash_event":
            cash_payload: dict[str, Any] = {
                "portfolio_id_or_name": args.get("portfolio_id_or_name"),
                "amount": args.get("amount"),
                "source": "mcp:wv2_add_cash_event",
            }
            for key in ("event_type", "event_date", "notes"):
                val = args.get(key)
                if val is not None and val != "":
                    cash_payload[key] = val
            try:
                data = await _post(
                    WV2_BASE, "/internal/cash_events", json=cash_payload, **hop_kw
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 422:
                    data = exc.response.json()
                else:
                    raise

        elif name == "wv2_close_portfolio":
            close_payload: dict[str, Any] = {
                "portfolio_id_or_name": args.get("portfolio_id_or_name"),
                "source": "mcp:wv2_close_portfolio",
            }
            if args.get("force") is not None:
                close_payload["force"] = bool(args.get("force"))
            notes_val = args.get("notes")
            if notes_val is not None and notes_val != "":
                close_payload["notes"] = notes_val
            try:
                data = await _post(
                    WV2_BASE, "/internal/portfolios/close", json=close_payload, **hop_kw
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in (404, 422):
                    data = exc.response.json()
                else:
                    raise

        elif name == "wv2_successor_portfolio":
            succ_payload: dict[str, Any] = {
                "portfolio_id_or_name": args.get("portfolio_id_or_name"),
                "source": "mcp:wv2_successor_portfolio",
            }
            syms = args.get("symbols")
            if isinstance(syms, str) and syms.strip():
                succ_payload["symbols"] = [
                    s.strip() for s in syms.replace(",", " ").split() if s.strip()
                ]
            elif isinstance(syms, list) and syms:
                succ_payload["symbols"] = syms
            ts_raw = args.get("trading_strategy_id")
            if ts_raw is not None and ts_raw != "":
                if isinstance(ts_raw, float):
                    succ_payload["trading_strategy_id"] = int(ts_raw)
                else:
                    ts_id = _optional_int(ts_raw)
                    succ_payload["trading_strategy_id"] = ts_id if ts_id is not None else ts_raw
            for key in (
                "initial_capital",
                "fingerprint",
                "seed_name",
                "name",
                "execution_mode",
                "export_kind",
                "notes",
            ):
                val = args.get(key)
                if val is not None and val != "":
                    succ_payload[key] = val
            for bkey in ("activate", "force", "force_close"):
                if args.get(bkey) is not None:
                    succ_payload[bkey] = bool(args.get(bkey))
            try:
                data = await _post(
                    WV2_BASE, "/internal/portfolios/successor", json=succ_payload, **hop_kw
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in (404, 422):
                    data = exc.response.json()
                else:
                    raise

        elif name == "wv2_mark_task_done":
            data = await _post(WV2_BASE, "/internal/tasks/complete", json=args, **hop_kw)

        elif name == "wv2_list_pending_actions":
            params = _query_params(args)
            data = await _get(WV2_BASE, "/internal/pending_actions", params=params, **hop_kw)

        elif name == "wv2_get_journal":
            journal_id = args["journal_id"]
            data = await _get(WV2_BASE, f"/internal/journals/{journal_id}", **hop_kw)

        elif name == "wv2_compare_equity":
            portfolios = args.get("portfolios") or args.get("portfolio_ids_or_names") or []
            if isinstance(portfolios, str):
                portfolios = [p.strip() for p in portfolios.replace(",", " ").split() if p.strip()]
            compare_payload: dict[str, Any] = {"portfolios": list(portfolios)}
            for key in ("as_of", "normalize", "title"):
                val = args.get(key)
                if val is not None and val != "":
                    compare_payload[key] = val
            data = await _post(
                WV2_BASE, "/internal/portfolios/equity_compare", json=compare_payload, **hop_kw
            )
            if data.get("status") == "ok" and data.get("telegram_media_path"):
                data = _attach_delivery_hints(data)

        elif name == "wv2_get_portfolio_status":
            params = _query_params(args)
            data = await _get(WV2_BASE, "/internal/portfolio_status", params=params, **hop_kw)

        elif name == "wv2_list_trading_strategies":
            data = await _get(WV2_BASE, "/internal/trading_strategies", **hop_kw)

        elif name == "dm_request_full_sync":
            payload = {
                "async": args.get("async", True),
                "notify_cromwell": args.get("notify_cromwell", True),
            }
            timeout = 30.0 if payload["async"] else 600.0
            data = await _post(
                DM_BASE, "/internal/ecosystem_sync", json=payload, timeout=timeout, **hop_kw,
            )

        elif name == "wv2_get_daily_activity_report_pdf":
            params = {"pdf_only": "1"}
            if args.get("date"):
                params["date"] = args["date"]
            data = await _get(WV2_BASE, "/internal/cromwell_notifications", params=params, **hop_kw)
            data = _attach_delivery_hints(data)

        elif name == "dm_get_cromwell_events":
            params = _query_params(args)
            data = await _get(DM_BASE, "/internal/cromwell_notifications", params=params, **hop_kw)

        elif name == "wv2_sync_data":
            payload = {"symbols": args.get("symbols")}
            if pid := args.get("portfolio_id_or_name"):
                payload["id_or_name"] = pid
            data = await _post(WV2_BASE, "/internal/dm/data_ready", json=payload, **hop_kw)

        elif name == "wv2_create_portfolio":
            data = await _post(WV2_BASE, "/internal/portfolios", json=args, **hop_kw)

        elif name == "wv2_add_market":
            data = await _post(WV2_BASE, "/internal/portfolios/add_market", json=args, **hop_kw)

        elif name == "wv2_transfer_portfolio_from_wut":
            # Coerce string ids; drop nulls. Prefer run_id when both set (WUT endpoint order).
            wut_params: dict[str, Any] = {}
            rid = _optional_int(args.get("run_id"))
            tid = _optional_int(args.get("ts_id"))
            if rid is not None:
                wut_params["run_id"] = rid
            elif tid is not None:
                wut_params["ts_id"] = tid
            else:
                data = build_error_payload(
                    name,
                    code="invalid_input",
                    message="Provide run_id or ts_id (integer). Omit unused keys; do not pass null.",
                    details={"run_id": args.get("run_id"), "ts_id": args.get("ts_id")},
                )
                return _finish_tool_response(
                    name, data, ctx, audit_hops, start,
                    status="error", error_code="invalid_input",
                )
            cfg = await _get(WUT_BASE, "/internal/portfolio_config", params=wut_params, **hop_kw)
            if "error" in cfg:
                data = cfg
            else:
                data = await _post(WV2_BASE, "/internal/portfolios", json=cfg, **hop_kw)

        elif name == "wut_list_portfolios":
            data = await _get(WUT_BASE, "/internal/portfolios", **hop_kw)

        elif name == "wut_list_portfolio_runs":
            data = await _get(
                WUT_BASE, "/internal/portfolios/runs",
                params={"portfolio_id_or_name": args["portfolio_id_or_name"]},
                **hop_kw,
            )

        elif name == "wut_add_market":
            data = await _post(WUT_BASE, "/internal/portfolios/add_market", json=args, **hop_kw)

        elif name == "wut_sync_portfolio_data":
            data = await _post(WUT_BASE, "/internal/portfolios/sync_data", json=args, **hop_kw)

        elif name == "wut_run_daily_operations":
            data = await _post(
                WUT_BASE, "/internal/portfolios/run_daily_operations",
                json=args, timeout=180.0,
                **hop_kw,
            )

        elif name == "wut_get_daily_operations_report":
            params = _query_params(args)
            try:
                data = await _get(
                    WUT_BASE, "/internal/portfolios/daily_operations_report",
                    params=params, **hop_kw,
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in (202, 422):
                    data = exc.response.json()
                else:
                    raise

        else:
            data = build_error_payload(
                name,
                code="unknown_tool",
                message="Tool not registered on winston_mcp",
                details={"hint": "See ecosystem/interfaces/winston-mcp-tools.md"},
            )
            return _finish_tool_response(
                name, data, ctx, audit_hops, start,
                status="error", error_code="unknown_tool",
            )

        tool_status = "error" if isinstance(data, dict) and data.get("status") == "error" else "ok"
        error_code = (
            data.get("code") or data.get("error")
            if tool_status == "error" and isinstance(data, dict)
            else None
        )
        return _finish_tool_response(
            name, data, ctx, audit_hops, start,
            status=tool_status, error_code=error_code,
        )

    except httpx.HTTPStatusError as e:
        body_preview = e.response.text[:500]
        err = build_error_payload(
            name,
            code="http_error",
            message=f"Monolith returned HTTP {e.response.status_code}",
            http_status=e.response.status_code,
            details={"body_preview": body_preview},
        )
        return _finish_tool_response(
            name, err, ctx, audit_hops, start,
            status="error",
            error_code="http_error",
            error_summary=body_preview,
        )
    except Exception as e:
        err = build_error_payload(
            name,
            code="internal_error",
            message=str(e),
            details={"exception": type(e).__name__},
        )
        return _finish_tool_response(
            name, err, ctx, audit_hops, start,
            status="error",
            error_code="internal_error",
            error_summary=str(e),
        )


# ---------------------------------------------------------------------------
# Entrypoints
# ---------------------------------------------------------------------------

def main() -> None:
    """Stdio entrypoint (great for local testing: python -m mcp_winston)."""
    import asyncio
    async def _run():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())
    asyncio.run(_run())


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# HTTP/SSE Transport (for nanobot inside compose)
# ---------------------------------------------------------------------------
#
# Nanobot's MCP client (when using "url") expects an SSE endpoint.
# We expose:
#   GET  /sse          -> SSE stream (tools, calls, results)
#   POST /messages/    -> client posts tool call responses / messages
#
# The compose service (winston_mcp) runs this via:
#   uvicorn mcp_winston.server:asgi_app --host 0.0.0.0 --port 8088
#
# The example config points to: http://winston_mcp:8088/sse

try:
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import Response
    from starlette.routing import Mount, Route
except ImportError:
    SseServerTransport = None  # type: ignore
    Starlette = None  # type: ignore

if SseServerTransport is not None:
    sse = SseServerTransport("/messages/")

    async def handle_sse(scope, receive, send):
        # Raw ASGI3 signature.
        # We call it directly from the dispatcher to avoid Starlette's routing/view logic
        # that was causing the TypeError (mismatch between how the route was registered and the function signature).
        try:
            async with sse.connect_sse(scope, receive, send) as (read_stream, write_stream):
                await server.run(
                    read_stream,
                    write_stream,
                    server.create_initialization_options(),
                )
        except Exception as e:
            import logging
            logging.getLogger(__name__).exception("SSE handler crashed for winston MCP")
            # Do not re-raise; let the ASGI server continue serving other requests/connections.
            # A clean close of this SSE is better than killing the whole uvicorn process.

    async def read_body(receive):
        body = b""
        while True:
            message = await receive()
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break
            elif message["type"] == "http.disconnect":
                break
        return body

    def header_value(scope, name):
        target = name.lower().encode()
        for key, val in scope.get("headers", []):
            if key.lower() == target:
                return val.decode()
        return ""

    async def health(scope, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        })
        await send({"type": "http.response.body", "body": b"ok"})

    async def cromwell_webhook(scope, receive, send):
        import json as _json
        from pathlib import Path

        if scope.get("method") != "POST":
            await send({"type": "http.response.start", "status": 405, "headers": []})
            await send({"type": "http.response.body", "body": b"Method Not Allowed"})
            return

        token = os.getenv("CROMWELL_WEBHOOK_TOKEN")
        if token:
            auth = header_value(scope, "authorization")
            if auth != f"Bearer {token}":
                await send({"type": "http.response.start", "status": 401, "headers": []})
                await send({"type": "http.response.body", "body": b"Unauthorized"})
                return

        body = await read_body(receive)
        inbox = webhook_inbox_dir()
        stamp = time.strftime("%Y%m%dT%H%M%S")
        notif_type = "daily_complete"
        try:
            parsed = _json.loads(body.decode() or "{}")
            notif_type = parsed.get("type", notif_type)
        except _json.JSONDecodeError:
            parsed = {}
        out = inbox / f"{stamp}_{notif_type}.json"
        out.write_text(body.decode() or "{}", encoding="utf-8")
        payload = _json.dumps({"status": "ok", "path": str(out), "type": notif_type}).encode()
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"application/json"]],
        })
        await send({"type": "http.response.body", "body": payload})

    async def asgi_app(scope, receive, send):
        if scope.get("type") == "http":
            path = scope.get("path", "")
            if path == "/health":
                await health(scope, receive, send)
                return
            if path == "/webhook/cromwell":
                await cromwell_webhook(scope, receive, send)
                return
            if path == "/sse":
                await handle_sse(scope, receive, send)
                return
            if path.startswith("/messages/"):
                await sse.handle_post_message(scope, receive, send)
                return
            # 404 for unknown paths
            await send({
                "type": "http.response.start",
                "status": 404,
                "headers": [[b"content-type", b"text/plain"]],
            })
            await send({"type": "http.response.body", "body": b"Not Found"})
            return
        # Ignore non-http scopes

        # Extra safety: never let unhandled exceptions in the dispatcher kill the server process.
else:
    async def asgi_app(scope, receive, send):
        await send({
            "type": "http.response.start",
            "status": 500,
            "headers": [[b"content-type", b"text/plain"]],
        })
        await send({"type": "http.response.body", "body": b"Dependencies not available"})

# No longer using Starlette for the main app to avoid routing issues with the SSE handler.
# The SseServerTransport and server are still used for the protocol.

# Added async httpx + per-call timing + improved tool descriptions + stronger
# "no loop" guidance in the no-report stub (see call_tool + cromwell_notifications).
# These address the repeated wv2_get_daily_activity_report calls and perceived
# long latency on simple messages (root cause was LLM think time on small CPU
# model + eager persona + missing report file causing the agent to spin).

# Hardened SSE handler (no re-raise on per-connection errors) to prevent the
# entire uvicorn process from exiting (code 0) during long-lived client connections
# or transient issues. This was observed during testing when the MCP server
# disappeared mid-interaction.


# Convenience: allow `python -m mcp_winston.server` to still do stdio
# when someone runs the module directly without uvicorn.
