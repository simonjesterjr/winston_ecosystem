# Ticket: Broker Gateway — evidence store (JSONL) + PG registry/cursors

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-09  
**Completed:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Winston Broker Evidence Standard, Broker Gateway  
**Glossary:** Winston Broker Evidence Standard, Broker Gateway  
**Monoliths:** **broker_gateway**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Grill B Q4  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

BG must durably store broker order/fill lifecycle truth the same way DM stores market truth: **files as evidence SoT**, **PG as registry/cursors/status**.

## Outcome

Implemented in `broker_gateway`:

- `Evidence::Store` — append-only JSONL under `data/evidence/{public_id}/events.jsonl`
- Idempotency via PG `evidence_event_indexes` (unique binding + idempotency_key)
- Orphan events accepted (no Winston FK)
- `AdapterBinding.public_id` as API `binding_id`; `last_event_seq` head
- Optional raw payload write under `raw/{yyyy}/{mm}/`
- Specs: append, dedupe, orphan, cursor read/pagination

Snapshots deferred (optional; documented in interface + README).

## Acceptance

- [x] JSONL append path writes versioned events (`schema_version: "0.1"`)
- [x] Idempotent write proven in specs
- [x] Orphan events accepted without Winston foreign keys
- [x] PG holds registry + index/seq + cursor metadata
- [x] File layout documented for ops (`data/evidence/README.md`)
- [x] Conforms to `interfaces/winston-broker-evidence-standard.md` v0.1 Accepted
- [x] No shared tables with Wv2

## Related

- Interface: [`2026-08-09-winston-broker-evidence-standard-interface.md`](2026-08-09-winston-broker-evidence-standard-interface.md)  
- API: [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md)  
