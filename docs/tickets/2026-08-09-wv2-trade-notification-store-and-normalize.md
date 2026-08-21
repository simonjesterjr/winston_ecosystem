# Ticket: Wv2 — TradeNotification durable store + normalize

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Trade Notification, Confirmation Intake  
**Glossary:** Trade Notification, Confirmation Intake, Booked Capital Spine, Signal Spine  
**Monoliths:** **winston_v2**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Phase 5; atomic `normalize_notification` / `store_notification`  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Evidence events from BG must become durable, queryable **Trade Notifications** in Wv2 — the in-process face used for match/prefill. Without a store and normalizer, desk UI and match cannot attach broker truth to a Single Fulfillment Identity.

## Scope

1. Schema/model for **TradeNotification** (or equivalent name aligned with CONTEXT).  
2. **Normalize** BG evidence event → TradeNotification fields: broker, account_ref, symbol, side, qty, price(s), time, external order/txn ids, status, raw/evidence refs, binding_id.  
3. **Idempotent store** on external ids / evidence event id.  
4. Statuses suitable for pipeline: e.g. received → matched / ambiguous / orphan / mismatch (match ticket may own transitions).  
5. Explicit: notifications are **not** Signal Spine; **not** capital_base.  
6. Specs: normalize fixture events; dedupe re-pull.

## Non-goals

- Auto-book Position from notification  
- Match algorithm completeness (next ticket may own match status writes)  
- Exit Capital Reconcile math (D10 ticket)  
- Email parse pipeline as primary  

## Domain locks

- Human-Gated: store ≠ book  
- No place_order  
- Ruby/Rails  
- API/evidence-derived only for v1 SoT path  

## Acceptance

- [x] Durable TradeNotification rows from BG events  
- [x] Idempotent on re-ingest  
- [x] Fields sufficient for match + desk prefill  
- [x] Specs with shared L1 fixtures  
- [x] No Journal executed / Position open side effects  

Shipped 2026-08-19: `TradeNotification` + `ConfirmationIntake::NormalizeNotification` / `StoreNotification`. Fixtures: `ecosystem/interfaces/fixtures/broker-evidence/`.  

## Related

- Client: [`2026-08-09-wv2-bg-client-and-event-cursor.md`](2026-08-09-wv2-bg-client-and-event-cursor.md)  
- Match: [`2026-08-09-wv2-match-prefill-confirmation-intake.md`](2026-08-09-wv2-match-prefill-confirmation-intake.md)  
- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
- Interface: [`2026-08-09-winston-broker-evidence-standard-interface.md`](2026-08-09-winston-broker-evidence-standard-interface.md)  
