# Ticket: Broker Gateway — Schwab L1 read adapter (`auth` + `order_read` + `txn_read`)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine` / `production-ready-wq` Phase 2  
**Parent:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) Phase 2 · [`2026-08-30-wq-phase2-schwab-read-and-sandbox.md`](2026-08-30-wq-phase2-schwab-read-and-sandbox.md)  
**Domain:** Broker Gateway, Confirmation Intake, Trade Notification  
**Glossary:** Broker Gateway, CapabilityProfile, Confirmation Intake  
**Monoliths:** **broker_gateway**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Phase 7; Grill B Q2/Q7  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

First real-broker L1 adapter is **Schwab Trader API** read path: authenticate, list/get orders, list transactions (TRADE and kin). Fixtures first; live read only after sandbox spike guidance and contract green. No write scopes.

## Scope

1. Adapter key `schwab_trader_api` with CapabilityProfile: `auth`, `order_read`, `txn_read`; **`order_write: false`**.  
2. **Fixtures first:** map canned Schwab-shaped order/txn JSON → Winston Broker Evidence Standard events (shared fixture harness).  
3. **Auth:** OAuth/session plumbing owned by BG; fail closed on auth failure; re-auth ops awareness (~7d refresh product note).  
4. **Live read (gated):** only after  
   - fixtures/contract green, and  
   - sandbox spike findings ([`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md)) inform env (`sandbox|live`) + safe practices.  
5. Poll/refresh job writes append-only evidence (idempotent).  
6. Redact account identifiers in logs; secrets never in Wv2.  
7. Specs: fixture normalization; refuse any place/cancel/replace methods (not implemented or hard-disabled).

## Non-goals

- `order_write` / Desk Send / place_order  
- Email confirmation parser as SoT  
- Streamer / webhook day one  
- `position_read` / `balance_read` as L1 requirements (L2 hints later)  
- IBKR adapter  

## Domain locks

- L1 capabilities only  
- Human Desk Confirm remains in Wv2  
- API poll primary  
- Ruby/Rails  

## Acceptance

- [x] Fixture-based refresh produces valid evidence events  
- [x] CapabilityProfile exposes L1 read only; write gated off  
- [x] Idempotent re-poll  
- [x] Live path documented behind env flag / binding env; default safe (fixtures/dev without live credentials)  
- [x] Auth failure fails closed with operator-visible status (fixture + live-unauthed specs)  
- [x] No place_order code path  
- [ ] Cross-link sandbox spike verdict when available  

## Depends on

| Relation | Item |
|----------|------|
| After | Scaffold, registry, evidence store, Evidence Standard interface |
| Related | [`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md) before confident live integration tests |
| Parallel OK | Dummy/sim for CI without Schwab |

## Related

- Epic: [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
- Discovery (superseded): [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md)  
