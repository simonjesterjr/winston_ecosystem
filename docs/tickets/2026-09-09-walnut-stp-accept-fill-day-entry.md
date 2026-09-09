# Ticket: Prove Accept-Fill at DUT print for a Walnut DAY STP entry

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-09  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Human gates:** operator Confirm already sent; do not Desk-Send from an agent; paper DUT only  
**DoD:** One Walnut DAY stop-market (STP) entry (or pyramid) Accept-Fills at the Interactive Brokers (IBKR) paper DUT print — journal executed at fill price/size, not last close, not Confirm click  
**Origin:** [`docs/session-reports/2026-09-09-1444-walnut-paper-stp-slate.md`](../session-reports/2026-09-09-1444-walnut-paper-stp-slate.md) §14 item 2  
**Related:** [`2026-09-09-walnut-paper-session-order-slate.md`](2026-09-09-walnut-paper-session-order-slate.md); ADR-013; CONTEXT **Accept-Fill**

## Problem

2026-09-09 parked a first round of Walnut Session Order Slate STPs on DUT (including DBC protective Good-Til-Cancelled). DAY entries/pyramids were sent as working journals. **Accept-Fill at the print** was not proven this session — the desk still has not booked a DAY STP from DUT fill evidence.

Without that proof, Walnut Confirm-Send of STP is only “parked,” not “the print is source of truth.”

## Scope

1. Pick one already-sent DAY STP (prefer a name that actually prints; not a probe).  
2. When DUT fills: Confirmation Intake / `WqFillBind` Accept-Fills the matching journal (price and size from the print).  
3. Record: client_order_key, broker_order_id, fill, journal status, cash/lot.  
4. Protective GTC fill (if a stop prints) is a sibling proof — same Accept-Fill law.

## Non-goals

- Booking last close at Confirm  
- Basket Accept-Fill  
- Cancel/replace (separate; still refused)

## Acceptance

- [ ] One DAY STP entry or pyramid journal goes `working` → `executed` from DUT fill evidence  
- [ ] Booked price/size match the print, not parquet last close  
- [ ] Session note or this ticket updated with ids  
