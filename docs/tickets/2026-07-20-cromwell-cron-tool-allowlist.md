# Ticket: Cromwell cron tool allowlist (hard forbid off-duty MCP)

**Status:** Done  
**Context:** Issue [`docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md`](../issues/2026-07-20-historical-dar-morning-telegram-leak.md). Session [`docs/session-reports/2026-07-20-1031-historical-dar-telegram-guards.md`](../session-reports/2026-07-20-1031-historical-dar-telegram-guards.md). Related hardening: [`2026-07-13-cromwell-cron-hallucination-hardening.md`](2026-07-13-cromwell-cron-hallucination-hardening.md).

## Problem

Prompt-level **FORBIDDEN** on cron jobs is insufficient. On 2026-07-20, `market-snapshot-open` (7:30 AM MT) ignored its forbid list after output-limit continue and called `wv2_perform_daily_analysis` with a historical date (`2023-10-15`, `parent_correlation_id=abc123`). Wv2/MCP date+Telegram guards now block the worst channel outcome, but the agent can still attempt off-duty tools and post noise.

## Acceptance criteria

- [x] Per-cron (or per-session-key) **allowlist** of MCP tools; calls outside the list fail closed with a short ops log line (no free-form recovery to Telegram)
- [x] `market-snapshot-open` / `market-snapshot-hourly` allow only `wv2_market_snapshot` (plus any minimal heartbeat/status read if required)
- [x] `eod-daily-report` allow only report-fetch path (`wv2_get_daily_activity_report` with `fetch_only`) — not `wv2_perform_daily_analysis` unless explicit operator session
- [x] Document allowlist in `ecosystem/ai/schedule/README.md` (or equivalent) and seed path
- [x] Smoke: force or observe one open snapshot; confirm forbidden tool call is rejected before monolith evaluate

## Implementation (2026-07-20)

| Piece | Location |
|-------|----------|
| Allowlist config (SOT) | `ecosystem/ai/schedule/cron-tool-allowlist.json` |
| Seed into workspace | `bin/seed-cromwell-workspace` → `workspace/schedule/cron-tool-allowlist.json` |
| Runtime enforce | `ai/nanobot/patches/cron_tool_allowlist.py` + Containerfile hook on `ToolRegistry` |
| Docs | `ecosystem/ai/schedule/README.md` |

**Verified live:** `prepare_call('mcp_winston_wv2_perform_daily_analysis')` under `session_key=cron:market-snapshot-open` returns `not allowed`; nanobot health ok after image rebuild.
## Implementation notes (non-binding)

Prefer nanobot/runtime enforcement over skill text. If runtime cannot allowlist yet, document gap and fall back to stricter structured formatters + circuit-break from the 2026-07-13 hardening ticket.

## Related

- Issue: [`../issues/2026-07-20-historical-dar-morning-telegram-leak.md`](../issues/2026-07-20-historical-dar-morning-telegram-leak.md)
- Ticket: [`2026-07-13-cromwell-cron-hallucination-hardening.md`](2026-07-13-cromwell-cron-hallucination-hardening.md)
- Schedule: `ecosystem/ai/schedule/cromwell-cron.json`
- Session: [`../session-reports/2026-07-20-1031-historical-dar-telegram-guards.md`](../session-reports/2026-07-20-1031-historical-dar-telegram-guards.md)
