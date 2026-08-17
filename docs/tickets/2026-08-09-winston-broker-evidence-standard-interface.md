# Ticket: Winston Broker Evidence Standard — interface doc

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-09  
**Completed:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Winston Broker Evidence Standard, Broker Gateway, Confirmation Intake, Trade Notification  
**Glossary:** Winston Broker Evidence Standard, Broker Gateway, Trade Notification  
**Monoliths:** ecosystem `interfaces/`; consumers **broker_gateway**, **winston_v2**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Grill B Q4  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Grill B locked a DM-shaped **Winston Broker Evidence Standard** (append-only JSONL events, idempotency keys, optional rebuildable snapshots, PG registry/cursors in BG). Without a versioned contract, BG and Wv2 implementers would diverge on event shape, cursor semantics, and orphan rules.

## Outcome

**Accepted** `interfaces/winston-broker-evidence-standard.md` v0.1 for L1:

- Location layout locked (`data/evidence/{binding_id}/events.jsonl`)
- Consumer-owned durable cursor (Wv2 stores `next_cursor`; BG issues opaque seq)
- MG1 routes normative: `POST/GET …/bindings/{binding_id}/refresh|events`
- Paper → `dummy_sim` locked; Manual stays Wv2 zero-IO escape hatch
- Envelope, idempotency, orphans, non-goals, CapabilityProfile L1

## Acceptance

- [x] `interfaces/winston-broker-evidence-standard.md` exists and is versioned (`0.1` Accepted)
- [x] Event + idempotency + orphan rules documented with at least one concrete JSON example
- [x] Cursor / consumer-read model summarized (§9.3 locked)
- [x] Explicit: consumers do not write the store; balances never capital_base
- [x] Linked from plan, epic, BG evidence store ticket, and related tickets
- [x] Compatible with fixture harness ticket for shared contract fixtures (envelope shape ready)

## Related

- Epic: [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
- BG store: [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md)  
- API: [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md)  
- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
- Interface: [`../../interfaces/winston-broker-evidence-standard.md`](../../interfaces/winston-broker-evidence-standard.md)  
