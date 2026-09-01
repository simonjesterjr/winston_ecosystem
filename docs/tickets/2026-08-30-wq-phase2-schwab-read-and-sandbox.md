# Ticket: WQ Phase 2 — Schwab sandbox spike + L1 read adapter

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-30  
**Mode:** contractor  
**Graph nodes:** broker_gateway, ecosystem  
**Edges:** `interfaces/winston-broker-evidence-standard.md`; CapabilityProfile L1; landscape §7.3  
**Human gates:** operator login at developer.schwab.com; live credentials never committed; no write scopes  
**DoD:** sandbox verdict written; `schwab_trader_api` adapter class registered; fixtures → evidence; `order_write` false; live read gated  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) §6  
**Epic:** [`2026-08-30-production-ready-wq.md`](2026-08-30-production-ready-wq.md)  
**Monoliths:** broker_gateway (primary), ecosystem docs  
**Depends on:** Phase 1 may overlap **fixtures only**; live Schwab read waits on spike + Phase 1 not blocking fixtures  

## Problem

BG lists `schwab_trader_api` as a CapabilityProfile stub (`registered: false`). There is no adapter class, OAuth, or secrets pointer. Whether Individual Trader API has a usable sandbox is still a blog-level guess. WQ staging must not pretend thinkorswim paperMoney is the API.

## Scope

1. Close child [`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md): portal field list + verdict (`usable sandbox` | `synthetic-only` | `retail production-only` | `unknown / blocked`). Update `docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md` §7.3.
2. Close child [`2026-08-09-bg-schwab-read-adapter-l1.md`](2026-08-09-bg-schwab-read-adapter-l1.md):
   - Fixtures: Schwab-shaped order/txn JSON → Winston Broker Evidence Standard events
   - Adapter class: `auth` + `order_read` + `txn_read`; **`order_write: false`**
   - OAuth/session owned by BG; fail closed; re-auth ~7d as ops attention
   - Live read behind env / binding `env` after spike; default safe without credentials
   - Specs refuse place/cancel/replace
3. Binding `env`: `sandbox` only if the spike says sandbox is real; otherwise `live` + dedicated small account for **read**.
4. Recommended integration ladder written: fixtures → optional sandbox → live read-only.

## Non-goals

- `place_order` / Desk Send (Phase 4)
- Binding WQ #1372 to Schwab (Phase 3)
- Capital Activation
- Email parser as source of truth
- IBKR
- Setting `cap_order_write` on dummy_sim

## Acceptance

- [ ] Spike verdict in landscape §7.3 with date + portal evidence (screenshot or written field list) — **operator portal**
- [x] `Adapters::Registry.registered?("schwab_trader_api") == true`
- [x] Fixture refresh produces valid evidence events
- [x] CapabilityProfile L1 read only; CapabilityGate still refuses write
- [x] Live path documented; default is fixtures/dev without live credentials
- [x] Auth failure fails closed with operator-visible status
- [ ] Child spike + L1-read tickets marked Done when the above hold

## Resume (later today)

Operator: portal spike. Coding: fixtures + adapter class with write gated off. No live `place_order`.
