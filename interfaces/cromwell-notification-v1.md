# Cromwell Notification Schema v1

**Version**: 1.1 (2026-07-04) — additive `correlation_id` / `parent_correlation_id` when MCP triggers analysis  
**Owner**: Wv2 (`CromwellNotifier`) + DM (`DmCromwellNotifier` events)  
**Transport**: File stub (always) + optional HTTP POST webhook (`CROMWELL_WEBHOOK_URL`)

## Wv2 `daily_complete` payload

Written to `winston_v2/storage/cromwell_notifications/wv2_YYYYMMDD.json` and POSTed to Cromwell when webhook is configured.

```json
{
  "source": "winston_v2",
  "type": "daily_complete",
  "schema_version": "1.0",
  "date": "2026-06-17",
  "report_id": "wv2-20260617",
  "report_links": {
    "report_id": "wv2-20260617",
    "date": "2026-06-17",
    "notification_json": "storage/cromwell_notifications/wv2_20260617.json",
    "pdf": "storage/reports/wv2_20260617.pdf",
    "internal_report": "/internal/cromwell_notifications?date=2026-06-17",
    "internal_pdf": "/internal/cromwell_notifications?date=2026-06-17&pdf_only=1",
    "mcp_tool": "wv2_get_daily_activity_report"
  },
  "portfolios": [
    { "id": 3, "name": "Sample Trend", "strategy": "Breakout 20", "status": "evaluated" },
    { "id": 4, "name": "No Data PF", "status": "skipped", "reason": "missing_data", "symbols": ["MSFT"] }
  ],
  "skipped_portfolios": [
    { "portfolio_id": 4, "name": "No Data PF", "status": "skipped", "reason": "missing_data", "symbols": ["MSFT"] }
  ],
  "actions": [
    {
      "task_id": 12,
      "portfolio": "Sample Trend",
      "market": "AAPL",
      "task_type": "enter",
      "direction": "long",
      "reason": "LONG - Primary: 20-Day Breakout",
      "price": 198.5,
      "journal_id": 44
    }
  ],
  "pending_actions": [],
  "passed_signals": [],
  "expired_today": [],
  "recent_journals": [],
  "summary": {
    "portfolios": 2,
    "portfolios_skipped": 1,
    "actions_created": 1,
    "pending_tasks": 0
  },
  "pdf_path": "storage/reports/wv2_20260617.pdf",
  "telegram_media_path": "/root/.nanobot/workspace/wv2_reports/wv2_20260617.pdf",
  "pdf_exists": true,
  "generated_at": "2026-06-17T22:30:00Z",
  "webhook_delivery": { "delivered": true, "status": 200, "url": "http://winston_mcp:8088/webhook/cromwell" }
}
```

### v1.1 correlation fields (additive, MCP-triggered flows only)

When daily analysis is invoked via MCP with `X-Correlation-Id` headers, `daily_complete` payloads include:

```json
{
  "schema_version": "1.1",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "parent_correlation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

- `parent_correlation_id` omitted when null.
- Scheduled Sidekiq runs without MCP headers keep `schema_version: "1.0"` and omit correlation fields.
- Wv2 mirrors integration events to `ecosystem/logs/audit/wv2/integration_YYYYMMDD.jsonl` (see ADR-004).

### Skip reasons (`portfolios` / `skipped_portfolios`)

| reason | Meaning |
|--------|---------|
| `missing_data` | DM parquet or `atr_17` missing for one or more Book symbols |
| `no_strategy` | Portfolio has no linked `TradingStrategy` |
| `unsupported_strategy` | Strategy class not in `StrategyRegistry` |
| `already_evaluated` | Idempotent re-run for same (portfolio, report_date) |

## Stable report artifacts (Task 7)

Manifest: `storage/reports/wv2-YYYYMMDD.manifest.json`

```json
{
  "report_id": "wv2-20260617",
  "source": "winston_v2",
  "type": "daily_complete",
  "date": "2026-06-17",
  "artifacts": {
    "notification_json": ".../wv2_20260617.json",
    "pdf": ".../wv2_20260617.pdf",
    "manifest": ".../wv2-20260617.manifest.json"
  },
  "links": { "...": "same shape as report_links in notification" }
}
```

## Webhook delivery

| Env (Wv2) | Purpose |
|-----------|---------|
| `CROMWELL_WEBHOOK_URL` | POST target (compose ai profile: `http://winston_mcp:8088/webhook/cromwell`) |
| `CROMWELL_WEBHOOK_TOKEN` | Optional `Authorization: Bearer` shared secret |

Dev receiver (`winston_mcp` HTTP mode) writes payloads to `CROMWELL_WEBHOOK_INBOX` (compose: `ecosystem/logs/audit/webhook` mounted at `/audit/webhook`). Cromwell workspace reads the parent audit tree read-only at `workspace/ecosystem_audit/`.

## DM event log (separate shape)

DM uses append-only JSONL: `data/cromwell_notifications/dm_events_YYYYMMDD.jsonl` with `event` types `sync_started`, `consumer_sync_started`, `symbol_updated`, `sync_complete`. See `dm_get_cromwell_events` MCP tool.

## Confirmation loop (Phase 2)

Agents confirm trades via MCP:

- `wv2_confirm_journal` → `POST /internal/journals/confirm`
- `wv2_mark_task_done` → `POST /internal/tasks/complete`

Journal state machine: `draft` → `executed` (terminal). Task: `pending` → `completed`. Entry confirmation opens a `Position`; exit confirmation appends `CLOSED` to `action_description`.