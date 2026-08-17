# Ticket: Broker Gateway — internal API (refresh + events since cursor)

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-09  
**Completed:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Broker Gateway, Confirmation Intake  
**Glossary:** Broker Gateway, Winston Broker Evidence Standard, Trade Notification  
**Monoliths:** **broker_gateway** (API); **winston_v2** consumes  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) architecture diagram; Grill B Q4  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Wv2 must pull evidence the DM-shaped way: **API commands to do work**, **GET events since cursor**.

## Outcome

MG1 routes live:

| Method | Path | Behavior |
|--------|------|----------|
| `POST` | `/api/v1/bindings/{binding_id}/refresh` | Sync poll via `Evidence::RefreshService` + adapter registry |
| `GET` | `/api/v1/bindings/{binding_id}/events?since_cursor=&limit=` | Ordered envelopes + `next_cursor` + `has_more` |
| `GET` | `/api/v1/bindings` / `…/{binding_id}` | Registry list/show |

- **Cursor ownership:** Wv2 stores last `next_cursor`; BG stream is stateless w.r.t. consumer (opaque decimal seq)
- **Auth:** optional `BG_INTERNAL_TOKEN` + `X-BG-Token` (open when unset)
- **Fail closed:** unknown binding 404; auth_failed / capability errors surface; no invent fills
- Flat scaffold stubs removed
- Request specs green (refresh, pull, empty, pagination, token auth)

## Acceptance

- [x] `POST` refresh for binding runs poll (sync L1)
- [x] `GET` events since cursor returns ordered events
- [x] Cursor advances only on consumer side (Wv2 owns durable cursor; documented)
- [x] Request specs green
- [x] Documented contract in interface §9 + BG AGENTS.md
- [x] No write-order routes

## Related

- Evidence store: [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md)  
- Wv2 client: [`2026-08-09-wv2-bg-client-and-event-cursor.md`](2026-08-09-wv2-bg-client-and-event-cursor.md)  
- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
