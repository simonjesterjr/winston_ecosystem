# Winston MCP Tool Contract (Initial — for Cromwell bot / nanobot access)

**Version**: v0.1 (2026-06-12, immediate plan)
**Owner**: Wv2 (with coordination via DM and WUT for transfer/sync)
**Transport**: Primarily stdio MCP (launched by nanobot per its documented mcpServers config). HTTP/SSE supported for testing/direct clients.
**Security model**: The MCP server (winston_mcp) runs inside the podman network. It only talks to the monoliths' internal endpoints over compose DNS. No direct DB or broad fs access. All calls are logged/auditable. Nanobot enforces channel allowFrom before tool use.

## Tool Inventory (Immediate Scope — The 6 Core Wv2 Use Cases + Essentials)
Tools are named with `wv2_` prefix for clarity (future DM/WUT/Cromwell tools will follow patterns). All tools are idempotent where possible and return structured JSON (success + data or error + details).

1. **wv2_transfer_portfolio_from_wut**
   - Purpose: Move a vetted configuration (run or first-class TradingStrategy) from the lab (WUT) into live (Wv2) via the canonical JSON exchange in /portfolio_configs.
   - Inputs: `{ "run_id": 42 }` or `{ "ts_id": 7 }` or `{ "config_name": "my-trend.json" }` (path under the shared volume is resolved automatically).
   - Behavior: Calls WUT export (or reads existing), ensures the JSON is present, triggers Wv2 import + TradingStrategy creation/link, returns the resulting portfolio.
   - Returns: `{ "status": "ok", "portfolio": { "id": 3, "name": "...", "markets": [...], "capital_base": 10200.0, "trading_strategy": "..." }, "config_path": "/portfolio_configs/..." }`
   - Notes: After transfer, caller should usually follow with activate + evaluate or the dedicated tools below.

2. **wv2_create_portfolio**
   - Purpose: Directly create a new live portfolio (alternative or complement to transfer/import).
   - Inputs: `{ "name": "Trading Portfolio C", "initial_capital": 15000, "markets": ["AAPL", "MSFT"], "trading_strategy_name": "My Breakout", "risk_percentage": 1.8, ... (other risk/strategy fields) }`
   - Behavior: Creates Portfolio + CashEvent (initial) + Books + links or creates TradingStrategy. Minimal markets are registered.
   - Returns: The created portfolio summary + capital_base.
   - Idempotency: Name-based upsert is acceptable for convenience.

3. **wv2_add_market**
   - Purpose: Add a symbol to an existing portfolio's book and ensure data will be available.
   - Inputs: `{ "portfolio_id_or_name": "3" or "Trading Portfolio A", "symbol": "NVDA" }`
   - Behavior: Ensure Market + Book record; call the sync path so DM can acquire.
   - Returns: Updated portfolio markets list + any sync request result.

4. **wv2_sync_data**
   - Purpose: Ensure Wv2 (and DM) have fresh Winston EOD Standard parquet for the symbols a portfolio (or explicit list) cares about.
   - Inputs: `{ "portfolio_id_or_name": "...", "symbols": ["AAPL"] }` (either or both).
   - Behavior: Uses DmParquetIngester.request_dm_data (which hits DM's request_consumer_sync) + ingest. Fire-and-notify pattern; caller can poll status or wait for data_ready side effects.
   - Returns: `{ "requested": true, "symbols": [...], "response": ... }` or error.

5. **wv2_perform_daily_analysis**
   - Purpose: Run the daily flow for one or all active portfolios (the heart of live ops).
   - Inputs: `{ "portfolio_id_or_name": "Trading Portfolio A" (optional; all active if omitted), "date": "2026-06-12" (optional) }`
   - Behavior: Runs synchronously (`sync: true`). Ensures data, ingests coverage, runs `DailyAnalysisJob` (SignalEvaluation + ReportBuilder + TaskGenerator), creates journals + operations_tasks + passed_signals, emits Cromwell notification.
   - Returns:
     ```json
     {
       "status": "completed",
       "date": "2026-06-12",
       "evaluated": [{
         "portfolio_id": 3, "portfolio_name": "...", "capital_base": 25000.0,
         "signals": [{ "type": "entry", "direction": "long", "market_symbol": "AAPL", "reason": "...", "price": 198.5 }],
         "warnings": [], "tasks_created": [{ "task_id": 1, "task_type": "enter", "direction": "long", "reason": "...", "price": 198.5 }]
       }],
       "skipped": [{ "portfolio_id": 2, "name": "...", "status": "skipped", "reason": "missing_data|no_strategy|unsupported_strategy", "symbols": ["MSFT"] }],
       "actions": [{ "task_id": 1, "portfolio": "...", "market": "AAPL", "task_type": "enter", "direction": "long", "reason": "...", "price": 198.5 }],
       "summary": { "portfolios": 2, "portfolios_skipped": 1, "actions_created": 1, "pending_tasks": 3 },
       "pending_actions": [...], "passed_signals": [...], "recent_journals": [...],
       "notification_path": "storage/cromwell_notifications/wv2_20260612.json",
       "report": { "source": "winston_v2", "type": "daily_complete", "portfolios": [...], "skipped_portfolios": [...], ... }
     }
     ```

6. **wv2_get_daily_activity_report**
   - Purpose: Retrieve the structured daily activity report / Cromwell notification payload (actions, journals, summaries) for a given date. This fulfills the "send link to daily activity report" use case.
   - Inputs: `{ "date": "2026-06-12", "portfolio_id_or_name": "..." (optional), "fetch_only": true (optional) }`
   - Notes: Scheduled Cromwell EOD (4:35 PM MT) must pass `fetch_only: true` — Wv2 Sidekiq runs `DailyAnalysisJob` at 4:30 PM MT. With `fetch_only`, a missing file returns `422` + `report_not_ready` (no on-demand analysis). Without `fetch_only`, missing file may trigger synchronous analysis (manual / 1-1 requests).
   - Behavior: Reads the CromwellNotifier JSON written by `DailyAnalysisJob`. On-demand path may call evaluate synchronously first; MCP merges `_meta.generated_on_demand` when that happens.
   - Returns: Full Cromwell payload (`portfolios` with per-portfolio `status`/`reason`, `skipped_portfolios`, `actions`, `pending_actions`, `passed_signals`, `recent_journals`, `summary`, `pdf_path`, `telegram_media_path`) plus MCP `_meta.delivery` hints for Telegram.
   - The agent (nanobot/Cromwell) is expected to format and "send" this over the Telegram channel.

**WUT lab portfolio tools** (control plane for backtest/operations portfolios — not Wv2 live):

7. **wut_list_portfolios**
   - Purpose: Discover WUT lab portfolios, markets, and whether an ActiveAccount exists.
   - Inputs: `{}`
   - Source: `GET /internal/portfolios` on WUT.

8. **wut_list_portfolio_runs**
   - Purpose: List recent backtest runs for transfer/discovery.
   - Inputs: `{ "portfolio_id_or_name": "..." }`
   - Source: `GET /internal/portfolios/runs` on WUT.

9. **wut_add_market**
   - Purpose: Add symbol to WUT portfolio (Book + backtest market config + optional DM sync).
   - Inputs: `{ "portfolio_id_or_name": "...", "symbol": "CLETF", "sync": true }`
   - Notes: Resolves aliases (`GOLD` → `CLETF`). Source: `POST /internal/portfolios/add_market`.

10. **wut_sync_portfolio_data**
    - Purpose: Queue DM sync for portfolio markets or explicit symbols.
    - Inputs: `{ "portfolio_id_or_name": "...", "symbols": ["AAPL"] }` (symbols optional).
    - Source: `POST /internal/portfolios/sync_data`.

11. **wut_run_daily_operations**
    - Purpose: Run WUT Operations daily flow for a portfolio's ActiveAccount.
    - Inputs: `{ "portfolio_id_or_name": "...", "date": "YYYY-MM-DD" }`
    - Requires ActiveAccount in WUT Operations UI. Source: `POST /internal/portfolios/run_daily_operations`.

12. **wut_get_daily_operations_report**
    - Purpose: Read DailyOperationsReport without re-running analysis.
    - Inputs: `{ "portfolio_id_or_name": "...", "date": "YYYY-MM-DD" }`
    - Source: `GET /internal/portfolios/daily_operations_report`.

**Data Manager (DM) tools:**
- `dm_get_cromwell_events` — sync activity log (`sync_started`, `consumer_sync_started`, `symbol_updated`, `sync_complete`). Cromwell posts `event.message` to Telegram during the 3:30 PM MT window. Source: `GET /internal/cromwell_notifications` on DM.

**Convenience / discovery tools** (also immediate):
- `wv2_market_snapshot` — latest EOD close/volume/atr_17 for symbols in active portfolios (DM parquet; not live intraday; no internet quotes).
- `wv2_list_portfolios` — returns active + summary (id, name, markets, capital_base, linked strategy).
- `wv2_list_pending_actions` — operations_tasks that are still pending.
- `wv2_get_portfolio_status` (id/name) — cash events summary, current positions, recent journals.
- `wv2_list_trading_strategies` — the reusable methodology definitions (for transfer/apply flows).
- `wv2_activate_portfolio` / `deactivate_portfolio` — mirror the existing internal + rake surface.

## Error Shape (All Tools)
```json
{ "status": "error", "code": "not_found|sync_failed|analysis_failed|invalid_input|...", "message": "...", "details": { ... } }
```

## Contract Evolution
- This lives in `ecosystem/interfaces/`. Bump version on material change.
- The MCP server implementation (in the winston_mcp component) is the reference.
- Nanobot config examples and the Cromwell persona prompt (in ecosystem/ai/) must stay aligned with these tool names and shapes.
- Future tools (DM sync, Cromwell confirmation, LLM explain) will be added in the same style and documented here before implementation.

## Security & Trust Notes
- Only narrow, auditable operations.
- No tool should ever allow arbitrary code execution, broad file writes, or direct position mutation outside the journal/confirmation flow.
- All state changes that affect capital or positions still flow through the existing Wv2 models, CashEvents, and the executed journal path (LLM or human can only influence drafts and notes until confirmation).
- The immediate implementation must be reviewable in one sitting (small Python MCP server + the existing Wv2 internal surface).

See plans/winston-mcp-immediate.md for the build slice and verification. The next-steps plan adds confirmation tools and richer report artifacts.

(End of initial MCP tool contract)
