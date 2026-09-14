# PBR #666 — LEAP intent audit + Edge read (Orange $30k)

**Banner:** report only — no pack promotion.  
**Date:** 2026-09-14  
**Operator intent:** Orange × TS#77 × $30k, simulate LEAP fulfillment long/short.  
**Comparators:** #650 ($10k RST parity), #664 ($30k RST parity).

## 1) Faithfulness to LEAP intent — **not faithful**

| Check | Result |
|-------|--------|
| `is_option` / `option_premium` / `LEAP` in `results_json` | **0** hits |
| Log lines mentioning leap/option | **0** |
| PBR leap knobs (`leap_pyramid_level`, `leap_atr_offset`, `leap_expiration_days`) | **absent** on this run model / unset |
| Cash-event tape | Share-like `units × stock entry_price` (e.g. GLTR 121 @ 102.97) |
| Fill cadence | **`hybrid_entry_next_pyramid_price_level`** (entry `next_bar_open`, pyramid `price_level_touch`) — **not** `resting_stop_touch` |
| Turtle heat | **not stamped** on #666 (parity cells carry turtle heat) |
| S2 Working Stop B1–B4 | Not on this path — **129** closes are `20-Day Breakout exit` (incl. under-max behavior hybrid allows) |

WUT *can* book LEAPs via `LeapPurchaseService` when `leap_pyramid_level` + ATR offset + expiration are set on the run evaluator; this run never entered that branch.

**Verdict:** #666 is a **hybrid share** Orange $30k backtest, not a LEAP-fulfillment simulation. Do not treat n=536 as evidence that LEAPs create breadth.

## 2) What #666 *does* show (still useful)

| Metric | #666 (hybrid $30k) | #664 (RST parity $30k) | #650 (RST parity $10k) |
|--------|--------------------|------------------------|------------------------|
| edge_r | **+0.2304** | −0.4015 | **+0.4127** |
| n | **536** | 75 | 184 |
| PF | 1.31 | 0.39 | 1.66 |
| win_rate | 31.2% | — | — |
| avg_win_r / avg_loss_r | 2.53 / 0.81 | — | — |
| return / max DD | +96.5% / 33.1% | +108.7% / 37.5% | +86.4% / 32.0% |
| Exit mix | stop 407 / 20d channel 129 | stop-dominated (parity) | stop-dominated |

**Insight:** The jump in n vs #664 is explained by **fill + contest geometry** (hybrid next-open, no overnight arm list, channel exits still live), not by option packaging. Edge is “ok” (+0.23) with classic Turtle shape (low hit rate, fat winners) — but it reopens the slippage hole RST was built to close, and it is **not** ops-parity.

## 3) Recommendation

- Re-run LEAP intent only after leap knobs are actually set and tape shows `is_option` / premiums.  
- Do not promote #666 as LEAP proof or as parity chassis.  
- For breadth: keep testing capital/LEAP on **RST + arm list + B1–B4**, or accept hybrid as a separate (less honest) lab family.

## 4) Why setting the UI knobs was not enough (2026-09-14)

Even a re-click of `leap_pyramid_level` on the new-PBR form would not have been a faithful extra-modal sim:

| Hole | Where | Effect |
|------|--------|--------|
| Lab eval Stamper never copies leap knobs | `LabEval::Stamper` / `CreateRun` | RST UAT cells cannot be LEAP cells |
| `is_leap` only on pyramid path; pyramids start at level 2 | `PortfolioBacktestRunner` | `leap_pyramid_level=1` (first unit) never books an option |
| ATR offset `0` is Ruby-falsy | `LeapPurchaseService` | ATM strike returns nil |
| `add_leap_position` zeros the stop, ignores RST fill | `PositionManager` | No 2N Working Stop on the underlying |
| Cash contest uses `shares × last` | `EntryRequirementCalculator` + RST reserve + final `entry_price * units` | Premium outlay cannot create breadth |

**Faithful re-run recipe** (ticket `winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md`): Orange × TS#77 × $30k, `fill_cadence=resting_stop_touch`, turtle heat, `leap_fulfillment=all` (or `entry` per packaging policy), ATM offset 0, expiration ≥ 730 days. Do not reuse #666. Live CPGW 1×1 remains a separate ticket.
