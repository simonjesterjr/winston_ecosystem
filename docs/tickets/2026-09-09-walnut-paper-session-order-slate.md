# Ticket: Portfolio Walnut paper Session Order Slate (stop-market)

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-09-09  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Human gates:** Slate Approve then remaining ready legs Desk Send automatically (one Order Intent at a time); operator never HTTP-baskets; paper DUT only  
**DoD:** After EODHD, Walnut rebuild cancels DAY entries on DUT; Approve Desk-Sends remaining STPs automatically; GTC protective stays/replaces; DUT print Accept-Fills  
**Origin:** Grill 2026-09-09 (operator answers 1–6) — ADR-013 §7, `CONTEXT.md` **Slate Approve** / **Session Order Slate** / **Working Stop** / **Accept-Fill**  
**Related:** `2026-08-20-resting-session-stop-orders.md` (methodology cycle; still blocked on cancel/replace); `2026-09-06-ibkr-cpgw-unattended-session.md` (tickle ≠ login); `2026-09-01-adr-009-resting-slate-addendum.md`; first STP round [`docs/session-reports/2026-09-09-1444-walnut-paper-stp-slate.md`](../session-reports/2026-09-09-1444-walnut-paper-stp-slate.md); Accept-Fill [`2026-09-09-walnut-stp-accept-fill-day-entry.md`](2026-09-09-walnut-stp-accept-fill-day-entry.md); close reconcile [`2026-09-09-walnut-day-stp-close-reconcile.md`](2026-09-09-walnut-day-stp-close-reconcile.md); tick [`2026-09-09-ibkr-stp-tick-size.md`](2026-09-09-ibkr-stp-tick-size.md); **Direction 2 parked** [`2026-09-09-extra-modal-leap-unit-evaluation.md`](2026-09-09-extra-modal-leap-unit-evaluation.md) + analysis [`docs/analysis/2026-09-09-extra-modal-leap-unit-vs-shares.md`](../analysis/2026-09-09-extra-modal-leap-unit-vs-shares.md) (do not start until this grain is automated)

## Problem

Walnut is paper-bound to Interactive Brokers DUT. Confirm can Desk-Send **one DAY MKT** (DBC wiring proof). The TS is TurtleV1 S2 Breakout55/20 — that loop is a **Session Order Slate** of **stop-market** parks, not limits and not a nightly market-on-open.

**2026-09-09:** first Approve → per-leg Confirm STP round **parked on DUT** (fail-closed without order id; 0.01 tick; CPGW `compete: true` after SSO). Broker Gateway still **refuses native replace** (cancel of one DAY id shipped; GTC cancel needs `allow_protective`).

**2026-09-10:** slate #40 auto-sent; three DUT prints **Accept-Filled** (DD short 36 @ 127.10, DBC pyramid 281 @ 33.21, SCHZ short 914 @ 22.49). Fill-driven delta slate parks GTC at TradingStrategy N + DAY pyramid; poll is **15 minutes**; broker push/websocket is a P1 eval (`2026-09-10-bg-broker-push-websocket-eval.md`).

**2026-09-10 afternoon:** `ProtectiveGtcGuard` blocked GTC *replace* and DAY pyramids on a name that already had a live GTC, so fill-driven slates **#41–#45** reminted DBC while pyramids stayed draft. Guard now allows replace (matching DUT id) and pyramid/entry sends; FillDrivenRepark is idempotent while an open fill-driven slate already covers the legs. Slates **#42–#45** voided; **#41** auto-send parked DBC GTC 563 @ 32.32 (replaced `#1646204526`), plus DAY pyramids DBC / DD / SCHZ.

## Locked packaging (do not re-litigate here)

1. Stops are always stop-market (STP). Not LMT. Not STPLMT for v1.  
2. DAY rebuild for entries and pyramids; GTC + replace for protective Working Stops; never cancel-all of live protective stops.  
3. Working stop / 20-day — trading rules `docs/business-context/turtle-s2-pyramid-and-working-stop.md`. Knobs from the TS (Walnut: 0.5N step, 2N stop, 4 lots). While lots < max: 20-day **not evaluated**; GTC 2N at last fill; DAY add at last fill ± step. After max lot fills: all lots to last−2N (long); 20-day evaluated; replace 2N with 20-day when it has passed that level (20-day may move nightly; may print through last purchase).  
4. **Slate Approve** then automatic Send of remaining ready legs (one Order Intent at a time, protective first). Not a basket HTTP. Not **Slate Automation** (no Approve click).  
5. Desk-Sent DUT commands **Accept-Fill** at the print (entries, pyramids, protective stops). IBKR is fulfillment SoT.  
6. Slate Contest for now: park competing names; Unit Heat + first-to-touch consume cash (revisit later).

## Scope

1. Broker Gateway: live **cancel** and **replace** on paper DUT (fail closed; same kill switch as `place_order`).  
2. Order Intent: STP + `tif` DAY|GTC; `auxPrice` = stop; role `entry_stop` | `pyramid_stop` | `protective_stop`.  
3. Wv2: build the night’s Walnut slate from parquet (55-day highs/lows, 0.5N pyramid rungs, 2N / 20-day working stop).  
4. Ops shell: **Slate Approve** then automatic Desk Send of remaining ready legs; working until print; Accept-Fill.  
5. After session: DAY entries/pyramids gone; replace GTC protective stops; do not naked the book.  
6. Client Portal session: document that tickle is required for Accept-Fill; do not pretend unattended SSO is done.

## Non-goals

- Slate Automation (policy-send with no Approve click)  
- Live IBKR / Schwab write  
- Mint dummy_sim slate  
- Stop-limit / trail  
- Whole-slate one-click Accept-Fill  
- Broker Account Capital as durable sizer (CashEvent align stays temporary)  
- Fixing Daily Analysis 20-day exit tasks while still adding — follow-on `ISSUE-20260909-da-20day-exit-under-max-lots` in winston_v2 (paper HITL evaluates Working Stop; do not dummy-sim Confirm on a live GTC)

## Acceptance

- [x] Paper DUT cancel specs + refuse cancel-all / GTC without allow_protective / kill switch off — 2026-09-09 evening (replace still refused)  
- [x] Approve slate → Confirm sends STP (DAY entry / GTC protective) and DUT shows a broker order id — 2026-09-09 first round (Accept-Fill at print still open: `2026-09-09-walnut-stp-accept-fill-day-entry.md`)  
- [ ] Open lot: GTC protective STP at 2N; replace moves the stop; cancel-all is refused  
- [x] Protective GTC can park on an open DBC lot (stock). Naked-lot attention / extra-modal HITL still follow-on  
- [ ] Maxed name with 20-day past 2N: next replace parks the 20-day, not 2N  
- [ ] Unfilled DAY entry is gone after the close; protective GTC still live (`2026-09-09-walnut-day-stp-close-reconcile.md`)  
- [ ] Mint Confirm still books; WQ Confirm still market  

## First slice

**Done 2026-09-09:** STP + DAY/GTC on the adapter/desk, Walnut Confirm parks a real DUT ticket (not MKT).  
**In this slice:** Broker Gateway **cancel** (never cancel-all; GTC refused unless allow_protective); rebuild **DAY teardown** + new slate from last parquet bar; **Slate Approve auto-sends** remaining ready legs. Remaining: live **replace** of GTC when the stop moves; Accept-Fill proof; close-of-day DAY honesty.

**Operator lock 2026-09-09:** Direction 1 is this ticket + Accept-Fill + close reconcile + fill-driven repark, until Walnut can run park → print → book → repark on its own. Extra-modal LEAP vs share-unit evaluation is **parked** (blocked ticket above) — do not open a Trader Workstation adapter or option `place_order` in this grain.
