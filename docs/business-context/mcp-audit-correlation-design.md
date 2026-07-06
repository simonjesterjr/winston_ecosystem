# MCP Audit + Correlation ID — Design Decisions (Grill Session 2026-07-02)

**Type:** Domain + implementation design (precedes task 8 Phase 3 slice)
**Plan:** `plans/winston-mcp-next-steps.md` task 8
**ADR:** `docs/adr/ADR-004-ecosystem-audit-log.md`
**Status:** Accepted via `/grill-with-docs`
**Tickets (fast follow):** `docs/tickets/2026-07-02-wv2-integration-audit-correlation.md`, `docs/tickets/2026-07-02-dm-integration-audit-mirror.md`, `docs/tickets/2026-07-02-cromwell-audit-trail-skill.md`

## Summary

Establish a central **Ecosystem Audit Log** at `ecosystem/logs/audit/` for integration observability. MCP generates **Correlation ID** per tool invocation; optional **Parent Correlation ID** chains multi-tool Cromwell turns. Phase 3 ships MCP JSONL + webhook relocation; Wv2/DM mirrors follow in separate tickets.

## Correlation model

| Decision | Choice |
|----------|--------|
| ID scope | **Hybrid** — one `correlation_id` per MCP invocation; optional `parent_correlation_id` links sibling calls in one Cromwell turn |
| Who generates `correlation_id` | **MCP server** — UUID4 at start of every `call_tool`; callers never supply it |
| Who supplies `parent_correlation_id` | **Caller** — optional tool argument and/or `X-Parent-Correlation-Id` header on HTTP/SSE path |
| Chaining convention | First tool in turn → `parent_correlation_id: null`. Nanobot passes prior `_meta.correlation_id` as parent on subsequent tools |
| Monolith payloads | MCP **strips** `parent_correlation_id` before forwarding to `/internal/*` (observability metadata only) |

## Central audit hub

| Decision | Choice |
|----------|--------|
| Root path | `ecosystem/logs/audit/` |
| What belongs here | **Integration Log** entries only (MCP, webhooks, coordination API access) |
| What stays local | Monolith **application** logs (Rails, Sidekiq, in-process exceptions) with normal log rolling |
| Error representation | Single tree — integration failures use `status: "error"` on JSONL lines; not a separate `logs/error/` tree for MCP |
| Git | Log file contents gitignored; structure documented in deployment |

### Partition layout

```
ecosystem/logs/audit/
├── mcp/       # winston_mcp tool invocations (Phase 3)
├── webhook/   # Cromwell webhook receipts (Phase 3 — relocated from webhook_inbox)
├── wv2/       # Wv2 integration events (fast follow)
└── dm/        # DM Cromwell sync events mirror (fast follow)
```

## MCP audit record (Phase 3)

**File:** `mcp/mcp_audit_YYYYMMDD.jsonl`  
**Env:** `CROMWELL_MCP_AUDIT_DIR` (default under audit mount)

```json
{
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "parent_correlation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "tool": "wv2_perform_daily_analysis",
  "started_at": "2026-07-02T16:30:00.123Z",
  "duration_ms": 4200,
  "status": "ok",
  "monolith": "winston_v2",
  "endpoint": "/internal/portfolios/evaluate",
  "http_status": 200,
  "error_code": null,
  "error_summary": null
}
```

- One line appended per `call_tool` completion (success or integration error).
- No full request/response bodies (daily analysis payloads are too large).
- Container stdout `print()` timing lines may remain; JSONL is the durable audit trail.

## HTTP header propagation

MCP sends on every `httpx` call to Wv2, WUT, DM:

```
X-Correlation-Id: <uuid>
X-Parent-Correlation-Id: <uuid>   # omitted when null
```

| Phase | Behavior |
|-------|----------|
| **Phase 3** | MCP sends headers + logs IDs in `mcp/` JSONL; monoliths may ignore |
| **Fast follow (Wv2)** | Read headers → `wv2/integration_*.jsonl` + embed in `daily_complete` notification (schema v1.1) |
| **Fast follow (DM)** | Mirror events to `dm/events_*.jsonl` with `correlation_id` when present |

Document header contract in `interfaces/winston-mcp-tools.md` (`_meta` + propagation section).

## MCP tool response `_meta`

Every tool response includes:

```json
"_meta": {
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "parent_correlation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

## Webhook relocation (Phase 3)

| Before | After |
|--------|-------|
| `ai/data/cromwell-bot/workspace/webhook_inbox` | `ecosystem/logs/audit/webhook/` |
| `CROMWELL_WEBHOOK_INBOX=/inbox` | Point at audit webhook partition |

Filename pattern preserved: `{stamp}_{type}.json`.

## Cromwell notification (fast follow — v1.1 additive)

Add to `daily_complete` payload when evaluate was triggered with correlation headers:

```json
{
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "parent_correlation_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

## Telegram surfacing

| Surface | Rule |
|---------|------|
| MCP `_meta` / notification JSON | Full UUIDs always |
| Routine daily briefing | No UUID noise |
| Error or explicit debug request | Optional footer: `ref: 550e8400` (first 8 chars of `correlation_id`) |

Cromwell skill `winston-audit-trail` (fast follow) documents grep/tail by full ID.

## Phase 3 implementation checklist

- [x] Create `ecosystem/logs/audit/{mcp,webhook}/` + gitignore for `*.jsonl` / webhook JSON
- [x] MCP audit writer in `call_tool` (`mcp_winston/audit.py`)
- [x] Correlation ID generation + `parent_correlation_id` ingress
- [x] Header propagation on all monolith HTTP calls
- [x] Relocate compose webhook mount to `audit/webhook/`
- [x] Read-only audit mount on Cromwell workspace
- [x] Update `interfaces/winston-mcp-tools.md` (v0.2)
- [x] Smoke: `bin/test-mcp-audit-smoke`

## Task 8 remainder (completed 2026-07-02)

- `errors.py` — structured errors + `retry_guidance`
- `rate_limit.py` — expensive tool sliding window
- `progress.py` — `event: progress` audit lines + `_meta.long_running`
- `tools_schema.py` — `parent_correlation_id` on all tool schemas
- `bin/test-mcp-maturity`, interfaces v0.3

## Out of scope (deferred per plan)

- Wv2/DM integration JSONL writers (fast follow tickets)
- Config-driven managed portfolios, signed external auth
- Centralizing monolith application errors
- Log retention / rotation policy for audit hub (future ops note)