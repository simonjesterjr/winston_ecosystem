# Ticket: Portfolio Walnut paper Session Order Slate (stop-market)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-09  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Human gates:** Slate Approve then per-leg Confirm = Desk Send; operator never auto-baskets; paper DUT only  
**DoD:** After EODHD, Walnut can Approve a night’s stop-market slate; each Confirm Desk-Sends one STP; DAY entries/pyramids rebuild; GTC protective stops replace; DUT print Accept-Fills  
**Origin:** Grill 2026-09-09 (operator answers 1–6) — ADR-013 §7, `CONTEXT.md` **Slate Approve** / **Session Order Slate** / **Working Stop** / **Accept-Fill**  
**Related:** `2026-08-20-resting-session-stop-orders.md` (methodology cycle; still blocked on cancel/replace); `2026-09-06-ibkr-cpgw-unattended-session.md` (tickle ≠ login); `2026-09-01-adr-009-resting-slate-addendum.md`; first STP round [`docs/session-reports/2026-09-09-1444-walnut-paper-stp-slate.md`](../session-reports/2026-09-09-1444-walnut-paper-stp-slate.md); Accept-Fill [`2026-09-09-walnut-stp-accept-fill-day-entry.md`](2026-09-09-walnut-stp-accept-fill-day-entry.md); close reconcile [`2026-09-09-walnut-day-stp-close-reconcile.md`](2026-09-09-walnut-day-stp-close-reconcile.md); tick [`2026-09-09-ibkr-stp-tick-size.md`](2026-09-09-ibkr-stp-tick-size.md)

## Problem

Walnut is paper-bound to Interactive Brokers DUT. Confirm can Desk-Send **one DAY MKT** (DBC wiring proof). The TS is TurtleV1 S2 Breakout55/20 — that loop is a **Session Order Slate** of **stop-market** parks, not limits and not a nightly market-on-open.

**2026-09-09:** first Approve → per-leg Confirm STP round **parked on DUT** (fail-closed without order id; 0.01 tick; CPGW `compete: true` after SSO). Broker Gateway still **refuses cancel and replace**, so nightly GTC move and honest DAY teardown cannot ship.

## Locked packaging (do not re-litigate here)

1. Stops are always stop-market (STP). Not LMT. Not STPLMT for v1.  
2. DAY rebuild for entries and pyramids; GTC + replace for protective Working Stops; never cancel-all of live protective stops.  
3. Working stop / 20-day — trading rules `docs/business-context/turtle-s2-pyramid-and-working-stop.md`. Knobs from the TS (Walnut: 0.5N step, 2N stop, 4 lots). While lots < max: 20-day **not evaluated**; GTC 2N at last fill; DAY add at last fill ± step. After max lot fills: all lots to last−2N (long); 20-day evaluated; replace 2N with 20-day when it has passed that level (20-day may move nightly; may print through last purchase).  
4. **Slate Approve** then per-leg Send (WQ-shaped). Not Slate Automation. Not basket send.  
5. Desk-Sent DUT commands **Accept-Fill** at the print (entries, pyramids, protective stops). IBKR is fulfillment SoT.  
6. Slate Contest for now: park competing names; Unit Heat + first-to-touch consume cash (revisit later).

## Scope

1. Broker Gateway: live **cancel** and **replace** on paper DUT (fail closed; same kill switch as `place_order`).  
2. Order Intent: STP + `tif` DAY|GTC; `auxPrice` = stop; role `entry_stop` | `pyramid_stop` | `protective_stop`.  
3. Wv2: build the night’s Walnut slate from parquet (55-day highs/lows, 0.5N pyramid rungs, 2N / 20-day working stop).  
4. Ops shell: **Slate Approve** then Confirm (send STP) per leg; working until print; Accept-Fill.  
5. After session: DAY entries/pyramids gone; replace GTC protective stops; do not naked the book.  
6. Client Portal session: document that tickle is required for Accept-Fill; do not pretend unattended SSO is done.

## Non-goals

- Slate Automation (policy-send, no click)  
- Live IBKR / Schwab write  
- Mint dummy_sim slate  
- Stop-limit / trail  
- Whole-slate one-click Accept-Fill  
- Broker Account Capital as durable sizer (CashEvent align stays temporary)  
- Fixing Daily Analysis 20-day exit tasks while still adding (call out as a follow-on; slate rule wins at the broker)

## Acceptance

- [ ] Paper DUT cancel + replace specs + live refuse when kill switch off  
- [x] Approve slate → Confirm sends STP (DAY entry / GTC protective) and DUT shows a broker order id — 2026-09-09 first round (Accept-Fill at print still open: `2026-09-09-walnut-stp-accept-fill-day-entry.md`)  
- [ ] Open lot: GTC protective STP at 2N; replace moves the stop; cancel-all is refused  
- [x] Protective GTC can park on an open DBC lot (stock). Naked-lot attention / extra-modal HITL still follow-on  
- [ ] Maxed name with 20-day past 2N: next replace parks the 20-day, not 2N  
- [ ] Unfilled DAY entry is gone after the close; protective GTC still live (`2026-09-09-walnut-day-stp-close-reconcile.md`)  
- [ ] Mint Confirm still books; WQ Confirm still market  

## First slice

**Done 2026-09-09:** STP + DAY/GTC on the adapter/desk, Walnut Confirm parks a real DUT ticket (not MKT). Remaining first-slice: **cancel + replace**.
