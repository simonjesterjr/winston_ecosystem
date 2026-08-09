# Ticket: Wv2 — Broker Gateway client + event cursor store

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Confirmation Intake, Broker Gateway  
**Glossary:** Confirmation Intake, Broker Gateway, Trade Notification  
**Monoliths:** **winston_v2**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Grill B Q3–Q4  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Confirmation Intake lives in Wv2 for match/prefill/book, but evidence is produced in BG. Wv2 needs a **HTTP client**, durable **per-binding (or per-OP) cursor**, and a **pull loop/job** to fetch new events.

## Scope

1. Config: BG base URL, internal auth secret, timeouts.  
2. Client methods: refresh binding, get events since cursor.  
3. Durable **cursor store** in Wv2 PG (consumer-owned cursor recommended).  
4. Sidekiq job / scheduled loop: poll or refresh-then-pull cadence (minutes-class; configurable).  
5. Idempotent handling of already-seen event ids when advancing cursor.  
6. Failure: fail closed + log/attention; do not invent fills.  
7. Specs with WebMock/VCR or local BG dummy.

## Non-goals

- Match/prefill logic (follow-on)  
- Writing evidence into BG  
- place_order  
- Email IMAP client  

## Domain locks

- Human still Desk Confirms (client only moves evidence)  
- L1 read path only  
- Ruby/Rails  
- Manual zero-IO path remains available without BG  

## Acceptance

- [ ] Client can refresh + pull against BG (dummy or WebMock)  
- [ ] Cursor persists and advances only after successful local accept of events  
- [ ] Job scheduled or rake-triggerable for ops  
- [ ] Specs cover empty stream, multi-event page, BG down  
- [ ] No book/Position mutation in this ticket  

## Related

- BG API: [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md)  
- TradeNotification store: [`2026-08-09-wv2-trade-notification-store-and-normalize.md`](2026-08-09-wv2-trade-notification-store-and-normalize.md)  
- Dummy: [`2026-08-09-bg-dummy-sim-adapter.md`](2026-08-09-bg-dummy-sim-adapter.md)  
