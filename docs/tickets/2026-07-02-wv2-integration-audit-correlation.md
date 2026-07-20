# Ticket: Wv2 integration audit + correlation ID echo (fast follow)

**Status:** Proposed
**Priority:** P2
**Blocked by:** Task 8 Phase 3 — MCP JSONL audit + `X-Correlation-Id` header propagation (`plans/winston-mcp-next-steps.md` task 8)
**Plan:** `plans/winston-mcp-next-steps.md` task 8 (fast follow after Phase 3 slice)
**Glossary:** `CONTEXT.md` — Correlation ID, Parent Correlation ID, Ecosystem Audit Log, Integration Log
**ADR:** `docs/adr/ADR-004-ecosystem-audit-log.md`
**Design:** `docs/business-context/mcp-audit-correlation-design.md`

## Scope

After `winston_mcp` sends `X-Correlation-Id` / `X-Parent-Correlation-Id` on internal HTTP calls, Wv2 consumes those headers on coordination paths and writes **Integration Log** entries to the central hub.

## Acceptance criteria

- [ ] `InternalController` (or shared concern) reads `X-Correlation-Id` and optional `X-Parent-Correlation-Id` on `/internal/*` requests
- [ ] Integration events append to `ecosystem/logs/audit/wv2/integration_YYYYMMDD.jsonl` (compose volume mount from Wv2 service)
- [ ] `CromwellNotifier` / `daily_complete` payload includes `correlation_id` and optional `parent_correlation_id` when present (schema bump documented in `interfaces/cromwell-notification-v1.md` → v1.1, additive only)
- [ ] Integration log lines cover notifier webhook delivery outcome (`status: ok|error`); monolith app errors remain in Wv2 `log/` only
- [ ] Smoke: MCP `wv2_perform_daily_analysis` → grep `mcp/` and `wv2/` JSONL by same `correlation_id`; notification JSON contains matching ID

## Out of scope

- Rails request log duplication or centralizing Sidekiq/application exceptions
- DM integration mirror (separate ticket)
- Cromwell Telegram formatting (separate ticket / skills Part 2)

## Related

- `docs/tickets/2026-07-02-dm-integration-audit-mirror.md`
- `docs/tickets/2026-07-02-cromwell-audit-trail-skill.md`
- Grill session decisions (2026-07-02): hybrid correlation, header propagation, single audit tree
