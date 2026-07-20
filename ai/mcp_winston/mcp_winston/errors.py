"""Structured MCP error payloads with tool-specific retry guidance (ticket C)."""

from __future__ import annotations

from typing import Any

# Generic HTTP guidance — no report/EOD boilerplate (that is tool-specific).
RETRY_BY_HTTP: dict[int, str] = {
    400: "Fix tool arguments; compare with ecosystem/interfaces/winston-mcp-tools.md.",
    404: "Verify ids/names exist (wv2_list_portfolios / wut_list_portfolios).",
    422: "Business rule blocked the call; read message/details and fix inputs.",
    429: "Rate limited — wait for retry_after_seconds then retry once.",
    500: "Monolith error — check monolith logs; retry after service is healthy.",
    502: "Upstream unreachable — ensure compose stack is up; retry in 30s.",
    503: "Service starting — retry in 30–60s.",
    504: "Timed out — for analysis/sync retry with narrower portfolio scope.",
}

RETRY_BY_CODE: dict[str, str] = {
    "http_error": "See http_status and retry_guidance; use correlation_id in ecosystem/logs/audit/mcp/.",
    "internal_error": "Transient MCP failure — retry once; if persistent, rebuild winston_mcp.",
    "unknown_tool": "Use a tool from list_tools / winston-mcp-tools.md.",
    "rate_limited": "Wait for retry_after_seconds before calling this expensive tool again.",
}

# Tool-family overrides. Report/EOD guidance only for report tools.
_REPORT_TOOLS = frozenset(
    {
        "wv2_get_daily_activity_report",
        "wv2_get_daily_activity_report_pdf",
        "wv2_perform_daily_analysis",
        "wut_get_daily_operations_report",
        "wut_run_daily_operations",
    }
)

_TOOL_HTTP_OVERRIDES: dict[str, dict[int, str]] = {
    "wv2_get_daily_activity_report": {
        422: (
            "Report not ready or analysis blocked. Scheduled EOD: use fetch_only=true after "
            "4:30 PM MT Sidekiq DailyAnalysisJob. Manual: omit fetch_only to run analysis, "
            "or call wv2_perform_daily_analysis."
        ),
    },
    "wv2_get_daily_activity_report_pdf": {
        422: "PDF/report not ready — fetch the daily activity report first or wait for 4:30 PM MT analysis.",
    },
    "wv2_perform_daily_analysis": {
        422: (
            "Analysis blocked (pre-cutoff schedule, historical date without allow_historical, "
            "or active mutex). Production EOD: omit date or use production_date after 4:30 PM MT. "
            "Historical test pass only: allow_historical=true (deliver_telegram still defaults false). "
            "Never call from morning/market-snapshot cron. Read message/error code."
        ),
    },
    "wut_add_market": {
        404: "Portfolio not found in WUT — check wut_list_portfolios for exact id/name.",
        422: "WUT refused add_market — read message (unknown portfolio, bad symbol, or sync issue).",
    },
    "wv2_add_market": {
        404: "Portfolio not found in Wv2 — check wv2_list_portfolios for exact id/name.",
        422: "Wv2 refused add_market — read message (portfolio/symbol validation).",
    },
    "wv2_add_cash_event": {
        404: "Portfolio not found — check wv2_list_portfolios.",
        422: "Cash event refused — amount non-zero; event_type inflow|adjustment; portfolio not closed.",
    },
    "wv2_book_trade": {
        422: "Book refused — portfolio, symbol on Books, positive units/price required; read message.",
    },
    "wv2_edit_journal": {
        404: "Journal not found — check wv2_list_pending_actions / wv2_get_journal.",
        422: (
            "Edit refused — only draft journals are editable (executed immutable); "
            "provide at least one field (units/price/notes/stop); read message/code."
        ),
    },
    "wv2_compare_equity": {
        404: "One or more portfolios not found — check wv2_list_portfolios for exact id/name.",
        422: "Compare refused — need 1–6 portfolios; read message/code.",
    },
    "wv2_exit_trade": {
        422: "Exit refused — need open position + price; read message/code.",
    },
    "wv2_exit_all_trades": {
        422: "Exit-all refused — need open lots for symbol + price; read message/code.",
    },
    "wv2_update_stops": {
        422: "Bulk stops refused — need open lots for symbol + positive stop_price; read message/code.",
    },
    "wv2_close_portfolio": {
        404: "Portfolio not found — check wv2_list_portfolios.",
        422: "Close refused — real OPs must be flat (or force=true); read message/code (not_flat).",
    },
    "wv2_successor_portfolio": {
        404: "Source portfolio or trading_strategy not found.",
        422: "Successor refused — close preconditions, empty symbols, or Active mutex; read message/code.",
    },
    "wv2_transfer_portfolio_from_wut": {
        422: "Transfer refused — check run_id/ts_id/config; engaged OPs refuse silent mutation.",
    },
    "wv2_activate_portfolio": {
        422: "Activate refused — Active mutex (same seed_name or identical Books); retry with force=true if intentional.",
    },
}


def retry_guidance(
    *,
    tool: str | None = None,
    http_status: int | None = None,
    code: str | None = None,
) -> str:
    tool_name = (tool or "").strip()
    if tool_name and http_status is not None:
        overrides = _TOOL_HTTP_OVERRIDES.get(tool_name) or {}
        if http_status in overrides:
            return overrides[http_status]
        # Non-report tools: never mention fetch_only / 4:30 PM on generic 422.
        if http_status == 422 and tool_name not in _REPORT_TOOLS:
            return (
                f"Business rule blocked {tool_name}; read message/details and fix inputs. "
                "Do not assume report/EOD fetch_only guidance."
            )
    if http_status and http_status in RETRY_BY_HTTP:
        return RETRY_BY_HTTP[http_status]
    if code and code in RETRY_BY_CODE:
        return RETRY_BY_CODE[code]
    return "Retry once; trace with correlation_id in ecosystem/logs/audit/mcp/."


def build_error_payload(
    tool: str,
    *,
    code: str,
    message: str | None = None,
    http_status: int | None = None,
    details: dict[str, Any] | None = None,
    retry_after_seconds: int | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "error",
        "code": code,
        "tool": tool,
        "message": message or code,
        "retry_guidance": retry_guidance(tool=tool, http_status=http_status, code=code),
    }
    if http_status is not None:
        payload["http_status"] = http_status
    if details:
        payload["details"] = details
    if retry_after_seconds is not None:
        payload["retry_after_seconds"] = retry_after_seconds
    return payload
