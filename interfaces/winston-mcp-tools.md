# Winston MCP Tool Contract (Initial — for Cromwell bot / nanobot access)

**Version**: v0.4 (2026-07-02, task 9 additional MCP tools)
**Owner**: Wv2 (with coordination via DM and WUT for transfer/sync)
**Transport**: Primarily stdio MCP (launched by nanobot per its documented mcpServers config). HTTP/SSE supported for testing/direct clients.
**Security model**: The MCP server (winston_mcp) runs inside the podman network. It only talks to the monoliths' internal endpoints over compose DNS. No direct DB or broad fs access. All calls are logged/auditable. Nanobot enforces channel allowFrom before tool use.

## Tool Inventory (Immediate Scope — The 6 Core Wv2 Use Cases + Essentials)
Tools are named with `wv2_` prefix for clarity (future DM/WUT/Cromwell tools will follow patterns). All tools are idempotent where possible and return structured JSON (success + data or error + details).

1. **wv2_transfer_portfolio_from_wut**
   - Purpose: Move a vetted configuration (run or first-class TradingStrategy) from the lab (WUT) into live (Wv2) via the canonical JSON exchange in /portfolio_configs.
   - Inputs: `{ "run_id": 42 }` or `{ "ts_id": 7 }` or `{ "config_name": "my-trend.json" }` (path under the shared volume is resolved automatically).
   - Behavior: Calls WUT export (or reads existing), ensures the JSON is present, triggers Wv2 import + TradingStrategy creation/link, returns the resulting portfolio.
   - Returns: `{ "status": "ok", "action": "legacy_updated|created|forked|adopted|…", "summary": "…", "reply_text": "Transfer OK — …\\nactive=…", "reply_hint": "PASTE reply_text…", "portfolio": { "id": 6, "name": "...", "fingerprint": "…", "markets": [...], "capital_base": 10000.0, "active": false, "execution_mode": "paper", … }, "warnings": [...] }`
   - Notes: Import lands inactive (paper default). Cromwell must **paste `reply_text`** (or lead with `summary` / `action` + `#id`); never a markets/capital briefing. Activate / sync / daily analysis only if the user asks (skill `winston-wut-to-wv2`). MCP adds `summary` + `reply_text` for weak local models (ticket A/C).

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

6a. **wv2_book_trade** (ad-hoc paper fill)
   - Purpose: Book a free-form fill on an Operational Portfolio **without** a Daily Analysis draft (Phase 4 / journal→ledger #2). Stock **or related instrument** (LEAP/option/proxy).
   - Inputs (stock): `{ "portfolio_id_or_name": "11", "symbol": "GGG", "units": 45, "price": 58.87, "direction": "long", "trade_date": "2026-07-16", "stop_price": 55.0, "notes": "desk paper fill" }`
   - Inputs (related): same + `fulfillment_type: "leap"|"option"|"proxy"`, `strike`, `expiry` (YYYY-MM-DD), optional `option_type` (`call`/`put`), `contract_multiplier` (default **100** for leap/option), `instrument_symbol` (proxy), `signal_task_id` / `signal_journal_id` (link to motivating DAR signal).
   - Behavior: Creates draft journal + enter/pyramid task, then reuses `JournalConfirmationService` / `JournalPositionExecutor`. **symbol** = signal **underlying** (must be on Books). Engages OP (ADR-006).
   - **Capital / flow:** stock|proxy → `±units×price`; leap|option → `±units×price×multiplier` (units=contracts, price=premium per share).
   - Position: option columns (`is_option`, strike, expiry, premium) + instrument label in `action_description`. No ATR default stop for option-like.
   - Returns: `{ "status": "ok", "action": "booked", "journal": {...}, "position": {...}, "fulfillment": { "type", "instrument_label", "contract_multiplier", ... }, "capital_base", "summary", "reply_text", "reply_hint" }`
   - Skill: `winston-ad-hoc-fill` — never invent units/price/strike/expiry; human authorization required.
   - Shell: `enter Blue IBM units=2 price=12.50 type=leap strike=150 expiry=2028-01-21 option_type=call`
   - Non-goals: full options pricing/Greeks, multi-leg legs as separate positions, broker automation, partial fills.

6b. **wv2_exit_trade** (ad-hoc exit)
   - Purpose: Close an open position **without** a Daily Analysis draft (human-gated desk / Telegram).
   - Inputs: `{ "portfolio_id_or_name": "12", "price": 250.0, "symbol": "AMZN" }` **or** `{ "portfolio_id_or_name": "12", "price": 250.0, "position_id": 1 }` — optional `trade_date`, `notes`, **`reason`**. Full lot exit (partial `units` reserved).
   - **`reason` packaging** (stored as `fulfillment_details.exit_reason`, `winston_signal: false`):
     - `external_stop` — broker/external stop hit; speech: “AMZN stopped out — book exit, no Winston signal.”
     - `discretionary` — human exit without Winston signal
     - `ad_hoc` (default) — generic desk exit
     - `other` — free-form other
     - Aliases: `stopped_out`, `broker_stop`, `stop_hit` → external_stop; `disc` → discretionary; `desk` → ad_hoc
   - Operator paths:
     - Ops shell: `exit Blue AMZN price=252 reason=external_stop`
     - Desk form: Exit reason select
     - Telegram/MCP: `reason` on `wv2_exit_trade`
   - Behavior: `POST /internal/journals/exit` → `AdHocExitService` creates draft exit journal + task, then reuses `JournalConfirmationService` close path (same capital credit as DAR exit confirm).
   - Returns: `{ "status": "ok", "action": "exited", "exit_reason": "external_stop", "journal": {...}, "position": {...}, "portfolio": {...}, "capital_base": ..., "summary", "reply_text", "reply_hint" }`
   - Skill: `winston-ad-hoc-fill` (exit section) — never invent price/symbol; human authorization required.
   - Errors: `not_found`, `closed_refuse`, `invalid_input`, `invalid_state` (already closed), `exit_failed`.
   - Non-goal: broker stop sync.

6b2. **wv2_exit_all_trades** (bulk flatten market)
   - Purpose: Close **all** open lots for a symbol on one OP (pyramid flatten). Per-lot journals, same price/reason for the batch. All-or-nothing.
   - Inputs: `{ "portfolio_id_or_name": "12", "symbol": "MSFT", "price": 420.0, "reason": "external_stop" }` — optional `trade_date`, `notes`.
   - Behavior: `POST /internal/journals/exit_all` → `BulkMarketExitService` → N× `AdHocExitService` (one journal per lot).
   - Returns: `{ "status": "ok", "action": "exited_all", "lots_exited": N, "lots": [...], "exit_reason", "capital_base", "reply_text", ... }`
   - Shell: `exit_all Blue MSFT price=420 reason=external_stop`
   - Errors: `not_found` (no open lots), `closed_refuse`, `invalid_input`, `exit_all_failed`.

6b3. **wv2_update_stops** (bulk move stops)
   - Purpose: Set the **same** stop on all open lots for a symbol on one OP (pyramid trail-all).
   - Inputs: `{ "portfolio_id_or_name": "12", "symbol": "MSFT", "stop_price": 395.0 }` — optional `notes`.
   - Behavior: `POST /internal/positions/stops_bulk` → `BulkStopUpdateService` → N× `PositionStopUpdateService`.
   - Returns: `{ "status": "ok", "action": "stops_updated", "lots_updated": N, "lots": [...], "stop_price", "reply_text", ... }`
   - Shell: `stops Blue MSFT price=395` (alias `move_stops`)
   - Errors: `not_found`, `closed_refuse`, `invalid_input`, `stops_update_failed`.
   - Single-lot still: shell `stop <position_id> price=S`.

6c. **wv2_add_cash_event** (capital inflow / adjustment)
   - Purpose: Record a **CashEvent** on an Operational Portfolio (speech: “add $5600 cash to Portfolio White”). Capital-only rebalance (ADR-006) — does **not** open/close positions or change Books/TS.
   - Inputs: `{ "portfolio_id_or_name": "11", "amount": 5600, "event_type": "inflow", "event_date": "2026-07-16", "notes": "weekly contribution" }`
   - Behavior: `POST /internal/cash_events` → `Operations::CashEventService`. Allowed `event_type`: `inflow` (default, amount > 0) or `adjustment` (may be negative). `initial`/`exit` not accepted on this path. Notes stamped with `source=mcp:wv2_add_cash_event`. Closed series refused.
   - Returns: `{ "status": "ok", "action": "cash_inflow|cash_adjustment", "cash_event": {...}, "portfolio": {...}, "capital_base_before", "capital_base", "summary", "reply_text", "reply_hint" }`
   - Errors: `not_found`, `closed_refuse`, `invalid_input`.

6d. **wv2_close_portfolio** (ADR-006 Close series)
   - Purpose: End signal evaluation on an Operational Portfolio series. History retained. **Not** a single-position exit (`wv2_exit_trade`).
   - Inputs: `{ "portfolio_id_or_name": "12", "force": false, "notes": "hygiene" }`
   - Behavior: `POST /internal/portfolios/close` → `Operations::PortfolioCloseService`. Paper soft-close (open residue OK). Real requires flat (no open positions / draft journals) unless `force=true`. Sets `closed_at`, `active=false`.
   - Returns: `{ "status": "ok", "action": "closed|already_closed", "portfolio": {...}, "open_position_count", "draft_journal_count", "summary", "reply_text", "reply_hint" }`
   - Errors: `not_found`, `not_flat`, `invalid_input`.

6e. **wv2_successor_portfolio** (ADR-006 shape rebalance)
   - Purpose: Close source A and open successor A′ with new Books and/or TradingStrategy. Journals stay on A. Use for engaged add-market / recipe change.
   - Inputs: `{ "portfolio_id_or_name": "6", "symbols": ["AMZN","MSFT","GLD"], "initial_capital": 12000, "trading_strategy_id": 3, "activate": false, "force": false, "notes": "..." }`
   - Behavior: `POST /internal/portfolios/successor` → `Operations::PortfolioSuccessorService`. Close A (same paper/real rules) + create A′ with `successor_of_id`, new `initial` CashEvent. Default inactive; `activate=true` respects Active mutex (`force` for dual-active).
   - Returns: `{ "status": "ok", "action": "successor_opened", "source_portfolio", "successor_portfolio", "markets", "capital_base", "close", "summary", "reply_text", "reply_hint" }`
   - Errors: `not_found`, `already_closed`, `not_flat`, `active_mutex`, `invalid_input`.

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

**Phase 2 — Confirmation loop** (bidirectional Cromwell ↔ Wv2):

13. **wv2_confirm_journal**
    - Purpose: Execute a draft journal — opens/closes positions, updates signed `flow`, marks linked task completed.
    - Inputs: `{ "journal_id": 44, "execution_price": 198.5, "units": 10, "notes": "filled via IB", "fulfillment_type": "stock|leap|option|proxy", "fulfillment_details": { "strike", "expiry", "option_type", "signal_task_id", ... } }`
    - Related-instrument confirm: set `fulfillment_type=leap` (etc.) + strike/expiry in details when honoring an equity signal with options; cash uses contract multiplier (default 100).
    - Sticky draft: if units/price/stop were set via `wv2_edit_journal`, bare confirm reuses them (no need to re-pass).
    - Source: `POST /internal/journals/confirm`
    - Returns: `{ "status": "ok", "journal": {...}, "task": {...}, "capital_base": 25100.0, "fulfillment": {...} }` (idempotent if already executed)

13b. **wv2_edit_journal** (draft amend — does **not** execute)
    - Purpose: Change draft units / price / notes / stop / trade_date / fulfillment packaging **before** confirm. Executed journals are immutable.
    - Inputs: `{ "journal_id": 44, "units": 5, "price": 251.03, "stop_price": 245.0, "notes": "size-down" }` — optional related-instrument fields (`fulfillment_type`, `strike`, `expiry`, …).
    - Behavior: `POST /internal/journals/edit` → `JournalDraftEditService`. Updates journal `fulfillment_details` + linked task metadata; recalculates provisional `flow`. No position open/close.
    - Returns: `{ "status": "ok", "action": "draft_edited", "journal": { proposed_units, proposed_price, proposed_stop, ... }, "changes": {...}, "reply_text", ... }`
    - Errors: `not_found`, `invalid_state` (not draft), `invalid_input` (no fields).
    - Shell: `edit_journal 44 units=5 price=251.03 stop=245 notes=size-down`
    - Desk: action **edit** on Ops desk form.

14. **wv2_mark_task_done**
    - Purpose: Complete an operations task; defaults to confirming the linked journal first.
    - Inputs: `{ "task_id": 12, "confirm_journal": true, "execution_price": 198.5, "units": 10, "notes": "..." }`
    - Source: `POST /internal/tasks/complete`

15. **wv2_list_pending_actions**
    - Purpose: List actionable pending tasks (within `ActionItemWindow`).
    - Inputs: `{ "portfolio_id_or_name": "...", "as_of": "YYYY-MM-DD" }`
    - Source: `GET /internal/pending_actions`

**Task 9 — Discovery + inquiry** (implemented):

16. **wv2_get_journal**
    - Inputs: `{ "journal_id": 44 }`
    - Source: `GET /internal/journals/:id`
    - Draft fields: `proposed_units`, `proposed_price`, `proposed_stop`, `editable`, `task_id`

16b. **wv2_compare_equity** (multi-OP equity chart for Telegram)
    - Purpose: Ad-hoc “Blue vs Mango” equity compare — metrics + single-page PDF chart.
    - Inputs: `{ "portfolios": ["Blue", "Mango"], "as_of": "2026-07-17", "normalize": false }`
    - Behavior: `POST /internal/portfolios/equity_compare` → `EquityCompareChartService` builds aligned `PortfolioEquitySeries`, draws via `ReportPdfChartDrawer` (legend labels = display name + short fingerprint), writes PDF under `storage/reports` with `telegram_media_path` under nanobot `wv2_reports` (same volume as DAR PDFs).
    - Returns: `{ "status": "ok", "title", "metrics": [...], "pdf_path", "telegram_media_path", "reply_text", "reply_hint", "_meta.delivery" }`
    - Delivery: paste `reply_text`; attach `media=[telegram_media_path]`.
    - Shell: `equity_compare Blue Mango` · `equity Blue Mango normalize=true`
    - Skill: `winston-equity-compare`
    - Non-goals: interactive live charts; PNG encoding (PDF document is the attachable media).

17. **wv2_get_portfolio_status**
    - Inputs: `{ "portfolio_id_or_name": "...", "journal_limit": 10 }`
    - Source: `GET /internal/portfolio_status`
    - Returns: portfolio summary, cash_events, positions, recent_journals

18. **wv2_list_trading_strategies**
    - Inputs: `{}`
    - Source: `GET /internal/trading_strategies`

19. **dm_request_full_sync**
    - Purpose: DM discovers symbols from WUT + Wv2 and acquires parquet for all.
    - Inputs: `{ "async": true, "notify_cromwell": true }` — default async enqueues `EcosystemSyncRequestJob`
    - Source: `POST /internal/ecosystem_sync` on DM
    - Sync path (`async: false`) may run many minutes; poll `dm_get_cromwell_events` when async.

**Other convenience tools**:
- `wv2_market_snapshot` — live internet price vs prior EOD close + atr_17 for active portfolio Books; movers by ATR status (focusing tool).
- `wv2_list_portfolios` — active + summary.
- `wv2_list_pending_actions` — see tool 15 above.
- `wv2_activate_portfolio` — `POST /internal/portfolios/activate` with `{ "id_or_name": "12" }` (or `id` / `name`). Optional `force: true` for dual-Active same `seed_name` or identical Books (ADR-006 mutex). Sets `active=true`. Without force, conflicts return 422 `active_mutex` with conflicting OP ids.
- `wv2_deactivate_portfolio` — `POST /internal/portfolios/deactivate` with `{ "id_or_name": "..." }`. Sets `active=false`; does **not** close positions or rewrite journals.

## Correlation IDs and audit (Phase 3 — ADR-004)

Every tool invocation:

- MCP generates `correlation_id` (UUID4). Callers may pass optional `parent_correlation_id` to chain tools in one Cromwell turn.
- MCP strips `parent_correlation_id` before forwarding args to monolith `/internal/*` endpoints.
- MCP sends headers on all monolith HTTP calls:
  - `X-Correlation-Id: <uuid>`
  - `X-Parent-Correlation-Id: <uuid>` (omitted when null)
- Every tool response includes `_meta`:

```json
"_meta": {
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "parent_correlation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

**Ecosystem Audit Log:** append-only JSONL at `ecosystem/logs/audit/mcp/mcp_audit_YYYYMMDD.jsonl` (one line per tool call). Cromwell webhook receipts land in `ecosystem/logs/audit/webhook/`. Monolith application logs stay local.

Design: `docs/business-context/mcp-audit-correlation-design.md`. Wv2/DM echo headers in notifications (fast follow).

## Error Shape (All Tools)

```json
{
  "status": "error",
  "code": "http_error|internal_error|unknown_tool|rate_limited|...",
  "tool": "wv2_perform_daily_analysis",
  "message": "Human-readable summary",
  "http_status": 422,
  "retry_guidance": "Actionable next step for the agent or principal",
  "retry_after_seconds": 45,
  "details": { "body_preview": "..." },
  "_meta": { "correlation_id": "...", "parent_correlation_id": "..." }
}
```

## Rate limiting (expensive tools)

Default limited tools: `wv2_perform_daily_analysis`, `wv2_get_daily_activity_report`, `wv2_sync_data`, `wut_run_daily_operations`. Env: `MCP_RATE_LIMIT_TOOLS`, `MCP_RATE_LIMIT_WINDOW_SEC` (default 120), `MCP_RATE_LIMIT_MAX` (default 4).

## Long-running tools / progress

Expensive tools set `_meta.long_running`, `estimated_duration_seconds`, and `progress_note`. Progress lines append to the same `mcp_audit_*.jsonl` with `"event": "progress"` and the same `correlation_id`.

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
