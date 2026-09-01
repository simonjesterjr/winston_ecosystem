# Ticket: Schwab Trader API sandbox / integration-test spike

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-07  
**Series:** `trade-fulfillment-engine` / `production-ready-wq` Phase 2  
**Monoliths:** `broker_gateway` (future); ecosystem docs  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Grill B Q7  
**Parent:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) Phase 2 · [`2026-08-30-wq-phase2-schwab-read-and-sandbox.md`](2026-08-30-wq-phase2-schwab-read-and-sandbox.md)  
**Related:** landscape §7.3 paperMoney/sandbox; discovery 2026-07-22  

## Problem

Grill B locks L1 test strategy as **contract + fixtures first**, then live **read** after green. We still need a factual answer: **does Charles Schwab expose a usable sandbox (or paper-linked API) for Trader API — Individual** that Broker Gateway can use for real integration tests?

Community + prior landscape (2026-07-22) suggest:

- **paperMoney** = thinkorswim **UI** mode, **not** the developer API target.  
- **Sandbox** may exist as a synthetic/developer env and/or be limited to commercial apps; retail often sees **Production-only** app environment.  
- Support quotes (2025–2026): no sandbox for Trader API / “in development” / test with non-marketable orders off-hours for place_order.

This must be **re-verified** on the live developer portal with our intended app, not assumed from blogs.

## Scope

1. Log into [developer.schwab.com](https://developer.schwab.com) as individual developer.  
2. Document for **Accounts and Trading** (and Market Data if used):  
   - App environments offered (Production / Sandbox / other)  
   - Whether sandbox is selectable for new apps  
   - Base URLs for sandbox vs production (if any)  
   - Whether sandbox returns synthetic accounts/orders/transactions or is non-functional for retail  
3. Confirm (with support ticket if needed): API **read** of orders/transactions against live account vs sandbox only.  
4. Confirm paperMoney cannot be used as API paper account (yes/no + evidence).  
5. Write findings into:  
   - `docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md` §7.3 (update date)  
   - short note in `plans/trade-fulfillment-engine.md` §9.1  
6. CapabilityProfile implication: `sandbox: true|false` for `schwab_trader_api` binding.

## Non-goals

- Implement Broker Gateway or OAuth product code.  
- Place live marketable orders.  
- Choose IBKR as first write adapter (separate decision / Grill C).

## Acceptance

- [ ] Portal screenshot or written field list: environments available for Individual Trader API app  
- [ ] Explicit verdict: **usable sandbox for our L1 read path** | **synthetic-only** | **retail production-only** | **unknown / blocked**  
- [ ] Recommended integration-test ladder for BG (fixtures → optional sandbox → live read-only binding)  
- [ ] Landscape §7.3 updated with spike date + sources  
- [ ] If production-only: document safe live-read practices (dedicated small account, fail closed, no write scopes until ADR-010)

## Discovery notes (pre-spike, 2026-08-07 — not authoritative)

| Source | Claim |
|--------|--------|
| Landscape 2026-07-22 §7.3 | paperMoney ≠ API; sandbox limited / not full paper twin |
| Reddit / support paste (2025) | No sandbox for Trader API; in development; test place_order off-hours / non-marketable; sandbox UI checkbox not active for retail |
| Secondary articles (2026) | Mixed: some say synthetic sandbox URL exists; some say commercial-only; all agree no paperMoney via API |

**Do not treat secondary articles as SoT — portal + support email is SoT.**

## Depends on

| Relation | Item |
|----------|------|
| After | Grill B Q7 (sandbox strategy A) |
| Before | Live Schwab OAuth in Broker Gateway against real capital account for L1 |
| Related | L1 implement tickets after Grill B close |
