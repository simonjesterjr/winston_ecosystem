# ADR-004: Ecosystem Audit Log for Integration Observability

**Status:** Accepted
**Date:** 2026-07-02
**Deciders:** Architecture (via `/grill-with-docs` session)
**Builds on:** ADR-001
**Source design:** `docs/business-context/mcp-audit-correlation-design.md`
**Domain context:** `CONTEXT.md` — Ecosystem Audit Log, Integration Log, Correlation ID

## Context

The MCP access layer (`winston_mcp`) and Cromwell coordination paths (webhooks, internal APIs) needed durable, operator- and agent-readable observability. Principals use the ecosystem as a whole; tracing a Telegram-driven daily flow across MCP → Wv2 → Cromwell notification required joinable records.

Alternatives evaluated:

- **Approach A: Per-service container stdout only** — ephemeral, hard for Cromwell/agents to query, no cross-service join key
- **Approach B: Centralize all monolith application logs** — duplicates Rails/Sidekiq noise; wrong abstraction for coordination debugging
- **Approach C: Ecosystem Audit Log hub** — `ecosystem/logs/audit/` for integration events only; monoliths keep local app logs with rolling
- **Approach D: PostgreSQL audit table in Wv2** — couples audit to one monolith MCP delegates to; harder for DM/MCP to write without new coupling

## Decision

We chose **Approach C: Ecosystem Audit Log hub** at `ecosystem/logs/audit/`.

- **Scope:** **Integration Log** entries only — MCP tool invocations, webhook receipts, and (fast follow) Wv2 notifier delivery and DM Cromwell sync events at coordination boundaries.
- **Format:** Append-only JSONL per producer partition (`mcp/`, `webhook/`, `wv2/`, `dm/`).
- **Exclusion:** Monolith application runtime logs (Rails, Sidekiq, strategy exceptions) remain local per monolith with normal log rolling. Central `status: "error"` means the **integration action** failed, not an in-app exception.
- **Correlation:** Hybrid model — MCP generates `correlation_id` per invocation; callers may pass `parent_correlation_id` to chain tools in one Cromwell turn. Propagation via `X-Correlation-Id` / `X-Parent-Correlation-Id` HTTP headers (see business-context design).
- **Compose:** Participating services mount `./ecosystem/logs/audit` (or subpaths); Cromwell workspace gets read-only access for agent skills.
- **Git:** Log contents gitignored; directory structure and contracts live in ecosystem docs and interfaces.

Phase 3 implements MCP JSONL + webhook relocation; Wv2/DM mirrors are fast-follow tickets (2026-07-02).

## Rationale

### Why not stdout-only?

MCP and webhook events are the audit surface ADR-001 names for Cromwell. Container logs rotate away and lack a stable join key across services.

### Why not centralize application logs?

Application errors belong to the monolith that owns the domain logic. Dumping Wv2 `SignalEvaluation` stack traces centrally blurs integration vs application concerns and duplicates existing Rails logging.

### Why not a PG audit table?

MCP and DM would need new write paths into Wv2's database — violates narrow coordination and majestic monolith boundaries. File-based JSONL matches existing Cromwell notification and DM event patterns.

### Why host path under `ecosystem/`?

Operators and agents work from the sawtooth workspace root. A first-class path under `ecosystem/logs/audit/` signals cross-monolith scope and aligns with ecosystem as general contractor.

## Consequences

### Positive

- One grep-friendly trail for Cromwell and principals diagnosing integration failures
- `correlation_id` joins MCP audit lines → (fast follow) Wv2 notifications → webhook files
- Agents can tail audit JSONL without shell access to monolith PG or Rails logs
- Monolith log rolling and ops stay unchanged for application runtime

### Negative

- Host disk growth under `ecosystem/logs/audit/` — requires retention discipline (not specified in Phase 3)
- Compose mount wiring across multiple services — more compose surface than stdout-only
- Producers must agree on partition layout and JSONL field conventions

### Risks mitigated

- Lost traceability on Telegram-driven flows → correlation IDs + durable JSONL
- Confusing audit with app logs → explicit Integration Log boundary in CONTEXT.md and this ADR
- Tight coupling via shared DB → file-based hub keeps monoliths independent