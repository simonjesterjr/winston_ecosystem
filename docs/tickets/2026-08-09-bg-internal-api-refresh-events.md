# Ticket: Broker Gateway — internal API (refresh + events since cursor)

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Broker Gateway, Confirmation Intake  
**Glossary:** Broker Gateway, Winston Broker Evidence Standard, Trade Notification  
**Monoliths:** **broker_gateway** (API); **winston_v2** consumes  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) architecture diagram; Grill B Q4  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Wv2 must pull evidence the DM-shaped way: **API commands to do work**, **GET events since cursor**. Without a minimal internal HTTP surface, Confirmation Intake cannot run.

## Scope

1. **Refresh/poll command(s):** trigger adapter poll for a binding (sync response with job id or accepted status; async Sidekiq OK).  
2. **GET events since cursor:** return evidence events (or normalized envelopes) for a binding after a cursor token/offset.  
3. Auth between monoliths: internal network / shared secret / existing ecosystem pattern (mirror DM consumer style as appropriate).  
4. Error model: auth fail, unknown binding, adapter capability refuse — fail closed, no silent empty success when poll failed.  
5. Pagination / max batch size for events.  
6. OpenAPI or markdown route table in BG or ecosystem interface cross-link.  
7. Specs (request specs) for refresh + cursor pull + empty + error cases.

## Non-goals

- Push webhooks day one (optional “events available” notify later)  
- Desk Confirm / match APIs on BG  
- Public internet exposure  
- `place_order` endpoints  

## Domain locks

- L1 read only  
- Ruby/Rails  
- No email ingest API as primary  

## Acceptance

- [ ] `POST` (or equivalent) refresh for binding enqueues or runs poll  
- [ ] `GET` events since cursor returns ordered events  
- [ ] Cursor advances only on successful consumer ack **or** documented pull-side cursor ownership (pick one; document clearly — recommend **Wv2 stores cursor**, BG is stateless stream by offset/id)  
- [ ] Request specs green  
- [ ] Documented contract linked from Wv2 client ticket  
- [ ] No write-order routes  

## Related

- Evidence store: [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md)  
- Wv2 client: [`2026-08-09-wv2-bg-client-and-event-cursor.md`](2026-08-09-wv2-bg-client-and-event-cursor.md)  
- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
