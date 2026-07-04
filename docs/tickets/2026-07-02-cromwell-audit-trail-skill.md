# Ticket: Cromwell audit-trail skill (grep integration logs by correlation ID)

**Status:** Done
**Verified:** 2026-07-04 — skill seeded via `bin/seed-cromwell-workspace`
**Blocked by:** ~~Task 8 Phase 3~~ (completed 2026-07-02)
**Plan:** `plans/cromwell-ai-skills-part2.md` (observability); depends on `plans/winston-mcp-next-steps.md` task 8
**Glossary:** `CONTEXT.md` — Correlation ID, Parent Correlation ID, Ecosystem Audit Log
**ADR:** `docs/adr/ADR-004-ecosystem-audit-log.md`
**Design:** `docs/business-context/mcp-audit-correlation-design.md`

## Scope

Add a Cromwell runtime skill so the Telegram bot (and principals) can diagnose integration failures by tracing **Correlation ID** across the central audit hub.

## Acceptance criteria

- [x] Skill `winston-audit-trail` in `ecosystem/ai/skills/` with deploy via `bin/seed-cromwell-workspace`
- [x] Skill documents how to tail `ecosystem/logs/audit/mcp/*.jsonl` filtered by `correlation_id` or `parent_correlation_id`
- [x] On MCP tool `status: error`, Cromwell may include short Telegram footer `ref: <first 8 chars>` per grill convention; skill explains how to expand to full trace
- [x] After Wv2/DM fast-follow tickets land, skill covers `wv2/` and `dm/` partitions too (Wv2 live; DM documented as pending mirror)
- [x] `ecosystem/ai/personas/cromwell-tools.md` references the skill

## Out of scope

- Implementing MCP audit writer (Phase 3 task 8)
- Full RAG over audit logs (`winston-plus-llm` roadmap)
- Centralizing monolith application error logs

## Related

- `docs/tickets/2026-07-02-wv2-integration-audit-correlation.md`
- `docs/tickets/2026-07-02-dm-integration-audit-mirror.md`
- `plans/cromwell-ai-skills-part2.md` — use case #8 stale reminders adjacent; audit trail is new