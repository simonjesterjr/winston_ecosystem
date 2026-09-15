# Ticket: BG OPT Order Intent + IBKR paper 1×1 prove

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-15  
**Mode:** contractor  
**Graph nodes:** broker_gateway (primary); winston_v2 (client intent builder later); IBKR CPGW  
**Human gates:** **paper DUT only**; **no live** IBKR/Schwab write; **agent never Desk-Sends**; operator-only first OPT Send after grill + SC + tradable matrix; no pack promotion  
**DoD:** BG accepts an OPT Order Intent with **required** `conid` (no stock-biased resolve); read path can resolve/snapshot 1–3 ATM LEAP candidates; one **human-gated** paper LEAP LMT (then maybe MKT) Submit → working → print evidence on DUT  
**Origin:** Plan [`plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md) Phases 2–3; ADR-017 Proposed; analysis [`2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md`](../analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md)  
**Related:** domain law [`leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); Wv2 fields [`2026-09-15-wv2-leap-packaging-fields.md`](2026-09-15-wv2-leap-packaging-fields.md); read-only matrix [`2026-09-09-extra-modal-leap-unit-evaluation.md`](2026-09-09-extra-modal-leap-unit-evaluation.md); parent [`spending-capacity-and-leap-fulfillment.md`](../../plans/spending-capacity-and-leap-fulfillment.md); ADR-009; ADR-013; ADR-017

## Problem

`PlaceOrderService` pass-through + IBKR adapter `resolve_conid` prefers NYSE/NASDAQ **stock** unless `intent["conid"]` is present. LEAP Desk Send cannot be honest until OPT intents **require** conid, evidence records `asset_class`/conid, and paper prove shows one OPT print.

## Scope

1. Intent schema (backward compatible): `asset_class` / `sec_type`, required `conid` when option, optional OCC audit fields (`right`, `strike`, `expiry`), `quantity` = contracts, `order_type` MKT|LMT for v1 LEAP entry.  
2. Adapter: if option, **require** `conid`; never fall through to stock search.  
3. Read API: thin `secdef/search` → strikes → `secdef/info` → snapshot (1–3 conids); empty quote → `untradeable`.  
4. Evidence: `order.upserted` records conid + asset_class + underlying symbol.  
5. CapabilityGate: option write behind same paper + `cap_order_write` + kill; no Schwab OPT write.  
6. Fixture path for OPT place without network.  
7. **Prove:** operator Desk Sends one paper LEAP (prefer LMT if MD wide; MKT allowed) — journal working until Accept-Fill at option print; Book stays underlying. Verify DUT option permission, multiplier 100, tick, paper MD.

## Non-goals

- Silent option protective STP / STPLMT for open LEAP lots  
- Geometry A / stock STP filled as LEAP  
- Live write  
- Agent Desk-Send  
- Multi-leg OMS  
- Replacing CPGW as Walnut **stock** STP adapter  
- TWS + CPGW on same paper username

## Acceptance

- [ ] Specs: option intent without conid refuses; stock path unchanged  
- [ ] Read resolve returns tradable/untradeable with live/snapshot quote (not BS)  
- [ ] Fixture OPT place_order green offline  
- [ ] Grill + SC + 1×1 gates checked before any OPT write  
- [ ] One operator paper OPT order id + working→print evidence; agent did not Send  
- [ ] No live / no pack promotion

## Human gates (repeat)

| Gate | Rule |
|------|------|
| Environment | Paper DUT only |
| Live | Forbidden |
| Agent | Never Desk-Sends options |
| Grill | `/grill-with-docs` before first OPT Send |
| SC / matrix | Parent Part 1 SC Check + tradable 1×1 row |
