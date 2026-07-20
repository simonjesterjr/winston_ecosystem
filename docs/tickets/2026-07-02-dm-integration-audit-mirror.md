# Ticket: DM integration audit mirror to ecosystem hub (fast follow)

**Status:** Proposed
**Priority:** P2
**Blocked by:** Task 8 Phase 3 — `ecosystem/logs/audit/` hub + compose mounts (`plans/winston-mcp-next-steps.md` task 8)
**Plan:** `plans/winston-mcp-next-steps.md` task 8 (fast follow after Phase 3 slice)
**Glossary:** `CONTEXT.md` — Ecosystem Audit Log, Integration Log
**ADR:** `docs/adr/ADR-004-ecosystem-audit-log.md`
**Design:** `docs/business-context/mcp-audit-correlation-design.md`

## Scope

Mirror DM Cromwell coordination events into the central **Ecosystem Audit Log** at `ecosystem/logs/audit/dm/`, aligned with existing `dm_events_YYYYMMDD.jsonl` semantics.

## Acceptance criteria

- [ ] DM writes (or mirrors) integration events to `ecosystem/logs/audit/dm/events_YYYYMMDD.jsonl` via compose volume mount
- [ ] Event types preserved: `sync_started`, `consumer_sync_started`, `symbol_updated`, `sync_complete` (see `interfaces/cromwell-notification-v1.md` DM section)
- [ ] When MCP calls DM internals with `X-Correlation-Id`, DM integration lines include `correlation_id` where applicable
- [ ] Monolith application errors stay in DM local logs; only coordination/integration events land in central audit tree
- [ ] `dm_get_cromwell_events` MCP tool remains functional; central path is additive for operator/agent tailing

## Out of scope

- Replacing DM's on-disk `data/cromwell_notifications/` source of truth (mirror/copy, not sole store)
- Wv2 notifier correlation echo (separate ticket)

## Related

- `docs/tickets/2026-07-02-wv2-integration-audit-correlation.md`
- `docs/tickets/2026-07-02-cromwell-audit-trail-skill.md`
- `interfaces/cromwell-notification-v1.md` — DM event log shape
