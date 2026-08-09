# Ticket: Winston Broker Evidence Standard — interface doc

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Winston Broker Evidence Standard, Broker Gateway, Confirmation Intake, Trade Notification  
**Glossary:** Winston Broker Evidence Standard, Broker Gateway, Trade Notification  
**Monoliths:** ecosystem `interfaces/`; consumers **broker_gateway**, **winston_v2**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Grill B Q4  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Grill B locked a DM-shaped **Winston Broker Evidence Standard** (append-only JSONL events, idempotency keys, optional rebuildable snapshots, PG registry/cursors in BG). There is no landed interface file yet. Without a versioned contract, BG and Wv2 implementers will diverge on event shape, cursor semantics, and orphan rules.

## Scope

1. Draft and land **`ecosystem/interfaces/winston-broker-evidence-standard.md`**.  
2. Cover at minimum:  
   - Version field / schema versioning  
   - Append-only **JSONL event** model (order lifecycle, fills, status, cancel/reject as applicable)  
   - **Idempotency keys** (dedupe on re-poll)  
   - Event identity fields: broker, account_ref, external order/txn ids, timestamps, symbol/side/qty/price, raw payload ref  
   - Orphans first-class (no Winston journal id required to store)  
   - Optional rebuildable snapshots (non-authoritative vs log)  
   - Consumer rules: Wv2 **reads** only; BG **writes** the evidence store  
   - Cursor / “events since” pull semantics (API-facing summary; detail may live in BG API ticket)  
3. Align names with CONTEXT: evidence events → in-process **Trade Notification** face in Wv2.  
4. Explicit non-goals in the interface: not capital_base SoT; not Signal Spine; not email body as canonical event.

**Note:** Draft body may already exist at [`interfaces/winston-broker-evidence-standard.md`](../../interfaces/winston-broker-evidence-standard.md) (v0.1) from a parallel agent — **this ticket owns acceptance** that the file is complete, linked, and matches domain locks (not merely that a stub exists).

## Non-goals

- Implementing BG storage or Wv2 pull code (child implement tickets)  
- `order_write` / place_order fields as required L1 surface  
- Email-as-SoT channel  
- Parquet-as-primary (optional analytics export later only)

## Domain locks

- L1 capabilities: `auth` + `order_read` + `txn_read` only — no write-order payload requirements for L1  
- Human still Desk Confirms (interface is evidence, not book instruction)  
- Ruby/Rails implementers consume this contract  

## Acceptance

- [ ] `interfaces/winston-broker-evidence-standard.md` exists and is versioned  
- [ ] Event + idempotency + orphan rules documented with at least one concrete JSON example  
- [ ] Cursor / consumer-read model summarized  
- [ ] Explicit: consumers do not write the store; balances never capital_base  
- [ ] Linked from plan, epic, BG evidence store ticket, and Wv2 TradeNotification ticket  
- [ ] Compatible with fixture harness ticket for shared contract fixtures  

## Related

- Epic: [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
- BG store: [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md)  
- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
- Schwab sandbox: [`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md) (related live-read shape)  
- Analog: `interfaces/winston-eod-parquet-standard.md` (DM pattern, different domain)  
