# Ticket: After cash close — reconcile Walnut DAY STPs vs DUT

**Status:** In progress — DUT-first overnight rebuild expires DAY already gone from DUT (2026-09-10)  
**Priority:** P1  
**Date:** 2026-09-09  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Human gates:** paper DUT only; do not invent cancels; operator blotter is SoT until BG cancel ships  
**DoD:** After the regular cash session, DUT working orders and Walnut working journals are compared; unfilled DAY entries/pyramids are honest (gone on DUT and not left working in Wv2 without evidence); protective GTC still live if the lot is open  
**Origin:** [`docs/session-reports/2026-09-09-1444-walnut-paper-stp-slate.md`](../session-reports/2026-09-09-1444-walnut-paper-stp-slate.md) §14 item 3  
**Related:** [`2026-09-09-walnut-paper-session-order-slate.md`](2026-09-09-walnut-paper-session-order-slate.md) (cancel still refused); [`2026-09-09-walnut-stp-accept-fill-day-entry.md`](2026-09-09-walnut-stp-accept-fill-day-entry.md)

## Problem

DAY STPs die at the cash close if unfilled. Walnut journals stay `working` until something expires or Accept-Fills them. Broker Gateway still **refuses cancel**, so a nightly rebuild cannot honestly pull unfilled DAY tickets off DUT. After 2026-09-09’s first park, the close must be observed, not assumed.

## Scope

1. After 16:00 ET: list DUT working orders (CPGW `GET /iserver/account/orders`) vs Walnut #1428 working journals (slate #12 legs).  
2. Classify each DAY leg: filled / cancelled-by-tif / still working (unexpected).  
3. Protective GTC (DBC SELL 282 @ 31.53 or successor): still on DUT iff the lot is open.  
4. If DUT dropped DAY and Wv2 still says working: HITL / expire path — do not silent-book.  
5. Expire-unfilled-DAY automation waits on **cancel** (parent slate ticket). This ticket is the **observation + desk honesty** slice.

## Non-goals

- Implementing BG cancel/replace (parent ticket)  
- Rebuilding the slate in a way that voids parked GTC  

## Acceptance

- [ ] Table in this ticket or a session report: symbol / side / tif / DUT status / journal status  
- [ ] Unfilled DAY not left as fake working without a named HITL  
- [ ] Open DBC (or successor) lot is not naked  
