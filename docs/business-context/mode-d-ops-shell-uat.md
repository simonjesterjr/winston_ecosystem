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

## Operator locks after the walk (2026-09-25)

1. The 8% spread gate does not return for Mode D. The open-interest floor stays off Mode D. Mode C’s 200-contract and 8% screens were not an operator decision. They need a design session before anyone treats them as law. Do not change those Mode C screens until that session.
2. Day orders (the stock entry and the pyramid adds) go back to the nightly Session Order Slate: Approve, then send. A lot with no working protective stop is never acceptable. The covered-call sale stays a human confirm. Not every long is written.
3. Pyramid stops stay `move_to_last_entry` on Trading Strategy #341. Earlier lots take the stop of the most recently added lot. The user-acceptance cadence made that look like a one-off resize. It is the strategy’s existing rule, two Average True Range units under the latest fill, Good Till Canceled.
4. Winston has to match Interactive Brokers. A working journal whose broker order is cancelled or filled must leave `working`. The shell then shows the lot naked if no stop remains, so the operator knows to act at the broker. A filled call does not prove the stop was cancelled and does not clear naked.

`outside_rth` on a market ticket was rejected for this XLE order while the exchange was closed. The resting order was a GTC limit. That flag is not a general overnight switch.
