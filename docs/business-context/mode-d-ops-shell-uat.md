# Mode D — Ops Shell workflow (user acceptance)

**Type:** Domain / desk law, user-acceptance record  
**Applies to:** Winston v2 portfolio **#1585** (`Portfolio Copper · mode-d-from-wut-794`), paper account DUT070450  
**Date:** 2026-09-25  
**Session:** [`../session-reports/2026-09-25-1407-mode-d-uat-ops-shell.md`](../session-reports/2026-09-25-1407-mode-d-uat-ops-shell.md)  
**Resume:** [`../tickets/2026-09-25-mode-d-uat-resume.md`](../tickets/2026-09-25-mode-d-uat-resume.md)

Mode D is `fulfillment_packaging_policy.fulfillment_mode=mode_d` with `leap_fulfillment=none`. It is not a Plan A / Plan B / Plan C rung and not a column.

## Locked for this user-acceptance walk

The operator set these aside or required them during the walk. They are not a silent change to Trading Strategy law for other books.

1. The walk uses the real Ops Shell desk (`/operations/workflow` and `/operations/desk`). A separate page that only writes Winston rows is not the test.
2. The first order is a stock buy of more than 100 shares. Confirm sends it. The button label is **Confirm**.
3. When that stock print books, Winston parks the Good Till Canceled (GTC) exit stop by itself, using the same working-stop distance as the other paper books. It does not also send a pyramid buy.
4. The same print offers a covered call for `floor(shares/100)` contracts. The offer is opt-out until Confirm. Passing it leaves the stock bare. The chain is read on that step only, from the stock price, not from the option premium sitting in the price field.
5. Open interest and the 8% bid/ask spread are not gates on this walk. A missing bid or ask still refuses the contract. Mode C Plan B defaults (200 contracts, 8% spread) stay on long calls.
6. Risk sizing, the first-lot cash slice, and the book's $30,000 cash cap are relaxed for these user-acceptance orders only. The paper account's own cash and buying power still decide whether Interactive Brokers (IBKR) will take the order.
7. A new pyramid buy, and a covered-call confirm, are not a second send of a stop that is already parked.
8. A stop that already has a broker order id is not a pending Ops Shell action. The covered-call card is headed **Mode D Option Workflow**, not HITL.
9. Buy the call back, then sell the stock. A stock sale while the short call is open is refused.
10. A filled call does not clear the naked-stop flag and does not replace the stop. Book the call credit at the print, not at the limit that was on the draft.

## What the account was when the session stopped

- DUT070450. Call bought back: order **946212656**, 1 XLE Oct 16 66 call at **0.60**.
- Stock still long **240** XLE. Flatten order **946212659**, GTC limit sell 240 at **61.00**, was PreSubmitted because the exchange was closed.
- Winston lots 936 (120 at 61.81) and 937 (120 at 62.10) stay open until that sell fills. No pending desk task. Free cash in the book about **$15,099.80**.

## Not locked — needs the operator

- Whether the 8% spread gate returns after this walk.
- Whether production Mode D auto-sends the GTC stop on the fill, or goes back to slate Approve then send.
- One stop for the whole symbol (resize when a pyramid fills) versus one stop per lot.
- A watcher that drops `working` when IBKR cancels a stop Winston still holds. The call fill is not, by itself, proof that IBKR cancelled the stop.
- `outside_rth` on the broker ticket. A market sell while the exchange is closed was rejected. A GTC limit is what rested.
