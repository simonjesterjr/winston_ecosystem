# Ticket: Broker Gateway — adapter registry + CapabilityProfile

**Status:** Done  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Broker Gateway, CapabilityProfile, Confirmation Intake  
**Glossary:** Broker Gateway, CapabilityProfile, Desk Confirm, Desk Send  
**Monoliths:** **broker_gateway**; schema notes may touch **winston_v2** later for binding ref  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) §6.2, Grill B Q2–Q3  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Adapters are selected by **registry key** + described by **CapabilityProfile**, not hard-coded Schwab shapes. BG needs a registry of adapter keys, profiles, and a **binding** model (account/credentials pointer) so poll jobs and Wv2 know what a binding can do. Grill B **Q8** (OP↔account binding detail) is **deferred** — implementers need temporary assumptions documented as TBD.

## Scope

1. **Registry keys** (string keys, not forever-enum): e.g. `manual` (Wv2-side only), `dummy_sim`, `schwab_trader_api`, future `ibkr_…`.  
2. **CapabilityProfile** fields for L1 ship: at least `auth`, `order_read`, `txn_read`; flags for `order_write` (must be **false** for L1 bindings), optional `position_read` / `balance_read` / `activity_stream` / `sandbox` as documented stubs.  
3. **Binding model (minimal):** account_ref, adapter_key, secrets pointer, env (`sandbox|live`), enabled capabilities override if needed.  
4. **Document Q8 TBD:**  
   - Temporary assumption for L1: binding is **account-level** in BG; Wv2 associates OP → binding_id **opaquely** (single binding per real OP is enough for first ship).  
   - Multi-OP same account / match ambiguity → **deferred** (do not invent silent auto-split).  
5. Orchestrators/adapters **query capabilities** before any future write; L1 code paths refuse `order_write`.  
6. Minimal ops visibility: list registry keys + binding health (auth status stub OK).

## Non-goals

- Final OP↔broker multi-account product law (Q8)  
- L3 Desk Send enablement  
- IBKR discovery completeness  
- Moving Manual adapter into BG (Manual stays zero-IO in Wv2)

## Domain locks

- L1 = `auth` + `txn_read` + `order_read` only  
- No place_order until ADR-010  
- Ruby/Rails  

## Acceptance

- [x] Registry keys loadable without schema migration per new vendor (prefer config/registry table over hard enum) — `Adapters::Registry` MAP + PROFILES  
- [x] CapabilityProfile exposed for dummy_sim and schwab_trader_api (L1 read set; `order_write: false`) — `GET /api/v1/adapters`  
- [x] Binding record holds adapter_key + account_ref + secrets pointer + env  
- [x] Q8 deferred section written in code comments or ops doc / ticket notes — `AdapterBinding` model header  
- [x] Attempted write capability use fails closed with clear error — `Adapters::CapabilityGate`  
- [x] Specs cover capability gate  

**Closed 2026-08-10** — registry formalized; BG compose services up on :3003.

## Related

- Dummy adapter: [`2026-08-09-bg-dummy-sim-adapter.md`](2026-08-09-bg-dummy-sim-adapter.md)  
- Schwab read: [`2026-08-09-bg-schwab-read-adapter-l1.md`](2026-08-09-bg-schwab-read-adapter-l1.md)  
- Epic: [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
