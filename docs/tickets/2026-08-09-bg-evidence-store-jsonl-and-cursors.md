# Ticket: Broker Gateway — evidence store (JSONL) + PG registry/cursors

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Winston Broker Evidence Standard, Broker Gateway  
**Glossary:** Winston Broker Evidence Standard, Broker Gateway  
**Monoliths:** **broker_gateway**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Grill B Q4  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

BG must durably store broker order/fill lifecycle truth the same way DM stores market truth: **files as evidence SoT**, **PG as registry/cursors/status**. Without append-only JSONL + idempotency + orphan support, Wv2 cannot safely pull Confirmation Intake evidence.

## Scope

1. **Append-only JSONL** store conforming to Winston Broker Evidence Standard.  
2. **Idempotency:** re-ingest / re-poll does not duplicate logical events (idempotency keys).  
3. **PG registry:** bindings, ingest runs/status, auth health, **consumer cursors** (or cursor metadata enough for GET-events).  
4. **Orphans first-class:** store events with no Winston journal / OP id.  
5. Optional **rebuildable snapshots** (non-authoritative vs log) — implement if cheap; document if deferred.  
6. Raw payload refs (object path / blob pointer) for audit.  
7. Volume/path layout for evidence files (container-friendly).  
8. Specs: append, dedupe, orphan insert, cursor advance semantics.

## Non-goals

- Shared PG with Wv2  
- Mutable status-only files without event log  
- Balances as capital_base  
- Email mailbox store  
- Match/prefill logic (Wv2)  

## Domain locks

- Consumers (Wv2) do not write the evidence store  
- L1 evidence only (no order_write side effects)  
- Ruby/Rails  

## Acceptance

- [ ] JSONL append path writes versioned events  
- [ ] Idempotent write proven in specs  
- [ ] Orphan events accepted without Winston foreign keys  
- [ ] PG holds registry + status + cursor metadata  
- [ ] File layout documented for ops  
- [ ] Conforms to `interfaces/winston-broker-evidence-standard.md` once landed  
- [ ] No shared tables with Wv2  

## Related

- Interface: [`2026-08-09-winston-broker-evidence-standard-interface.md`](2026-08-09-winston-broker-evidence-standard-interface.md)  
- API: [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md)  
- Scaffold: [`2026-08-09-broker-gateway-rails-scaffold.md`](2026-08-09-broker-gateway-rails-scaffold.md)  
