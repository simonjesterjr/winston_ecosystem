# Ticket: Wv2 paper Red — IBKR-eval LEAP, paper-only fulfill (from WUT #692)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-16  
**Depends on:** Blue Mode C cutover (`2026-09-16-wv2-paper-leap-eval-blue-from-685`) verified first  
**Origin:** John → CoS 2026-09-16 — finish Blue, then migrate Red

## Problem

After Blue Mode C paper-LEAP is live, stand up a new **Red** paper book from WUT PBR **#692** at **$30k**, same Mode C rules (IBKR eval only; Wv2 paper fulfill; `broker_binding_id` nil). This **replaces** existing Wv2 Red portfolio(s) (currently only inactive `Portfolio Red` **#5**, color `#dc2626`).

## Fingerprint (lab)

- Cell: `red_rst_turtle_r01_leap30k_ts75`
- PBR **#692** · **TS75** · TurtleV1 **S1** Breakout20/10 · RST · `leap_fulfillment=all` · **risk 1%** · **$30k** · heat turtle
- Stop doctrine: pyramid `move_to_last_entry` 2N + S1 10d channel (not sticky 20D_BO)

## Mode C locks (same as Blue)

1. IBKR real chain ATM LEAP eval only — no IBKR fulfill / no OPT Desk-Send  
2. `broker_binding_id` **nil**; desk read via `LEAP_READ_BINDING_ID`  
3. No Black-Scholes; staleness OK at HITL Approve  
4. Entry HITL; Working Stop pierce → auto paper STC  
5. Spend: `premium×100×contracts` vs paper cash  
6. Adapter: `dummy_sim`

## Acceptance

- [ ] Existing Wv2 Red OP(s) closed/deactivated (evidence: ids)  
- [ ] New Red $30k active, #692/TS75 fingerprint, LEAP-all, paper-only, bind nil  
- [ ] Smoke: LEAP resolve via desk read binding without portfolio bind  
- [ ] INDEX + session note updated; Blue ticket linked as predecessor

## Related

- Blue: [`2026-09-16-wv2-paper-leap-eval-blue-from-685.md`](2026-09-16-wv2-paper-leap-eval-blue-from-685.md)  
- Analysis: [`../analysis/2026-09-16-pbr692-sticky-2n-working-stop.md`](../analysis/2026-09-16-pbr692-sticky-2n-working-stop.md)  
- Plan Mode C: [`../../plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md)
