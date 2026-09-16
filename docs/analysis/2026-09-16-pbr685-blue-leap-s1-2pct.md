# PBR #685 — Blue LEAP S1 2% autopsy

**Banner:** report only — no pack promotion · no stamps.  
**Date:** 2026-09-16 (America/Denver)  
**Cell:** `blue_rst_turtle_r02_leap30k_ts75` · PBR **#685** · Portfolio Blue · TS75 · RST · leap_fulfillment=all · risk **2%** · $30k · heat turtle  
**Parent:** #668 `blue_rst_turtle_r01_leap30k`  
**Desk law:** [`exit-and-protective-stop-desk-law.md`](../business-context/exit-and-protective-stop-desk-law.md) — exit strategy + protective stops (TS75 obeys). Sticky 20D_BO is S2-only.

---

## VERDICT

**Real LEAP cash compounder at 2% heat — solvent, high return, worse risk-adjusted than Blue 1% (#684) or Red 1% (#692).** Prefer OA/cash for ranking. Signal-path `edge_r=7.80` (not the old ~920 fiction). **Red flag:** `cash_vs_journal_delta ≈ $433.7k` — much larger than siblings (~$8–9k); investigate before promote.

---

## Knobs

| Field | Value |
|-------|--------|
| cell_key | `blue_rst_turtle_r02_leap30k_ts75` |
| experiment | `strategy75_leap_risk_ab_v1` |
| book | Portfolio Blue (portfolio_id 7) |
| TS | 75 TurtleV1 S1 Breakout20/10 |
| fill_cadence | resting_stop_touch |
| leap_fulfillment | all |
| stop_strategy | move_to_last_entry |
| atr / pyramid | 2.0 / 0.5 (TS) |
| risk / heat unit | 0.02 |
| capital | 30000 |
| window | 2020-08-05 → 2026-09-14 |

## Metrics (quoted)

| Metric | #685 Blue 2% | #684 Blue 1% | #692 Red 1% |
|--------|-------------:|-------------:|------------:|
| edge_r | **7.7981** | 8.9251 | 9.4183 |
| edge_n | 731 | 406 | 422 |
| PF | **4.8854** | 24.1995 | 27.6637 |
| win_rate | 0.5499 | 0.564 | 0.4905 |
| avg_win_r / avg_loss_r | 17.68 / 4.28 | 16.52 / 0.90 | 19.94 / 0.71 |
| legacy return % | 8931.4 | 2992.5 | 3513.3 |
| legacy max_dd % | 44.53 | 34.44 | 25.96 |
| cash return % (final_cash/30k−1) | **8759.3** | 2906.5 | 3473.7 |
| OA return % | **8833.6** | 2943.6 | 3493.5 |
| OA max_dd % | **21.40** | 3.03 | 4.20 |
| final_equity / final_cash | 2.709M / 2.658M | 928k / 902k | 1.084M / 1.072M |
| open MV (equity−cash) | 51624 (4 opens) | 25812 (4) | 11868 (5) |
| cash_vs_journal_delta | **433656** | 9180 | 8033 |

## Fidelity / exits

- Closes **731**; **731 leap / 0 share** — LEAP fidelity PASS
- Exit mix: **10d 371** / **stop 360** (dual doctrine: channel + WS pierce)
- Positions 735 all `is_option`; stop moved 455/735 (`move_to_last_entry` on adds)
- sum realized_pnl 2,635,343; cap+pnl ≈ final_cash path

## What John should care about next

1. **Ranking:** vs #684, 2% buys ~3× cash return but OA DD 3%→21% and PF 24→4.9 — not a free lunch.
2. **Journal gap $434k** on #685 — do not promote on scoreboard alone until reconciled.
3. Same stop doctrine as #692 (not sticky 20D_BO).

---

## Journal gap root cause (2026-09-16 follow-up)

**Same red flag as `cash_vs_journal_delta ≈ $433,656.18`.**

### Formula
`portfolio_backtest_runner.rb` `calculate_final_results`:
- `journal_reconstructed_cash = initial_capital + Journal.where(run_id).where.not(debit_credit: nil).sum(:flow)`
- `cash_vs_journal_delta = final_free_cash − journal_reconstructed_cash`

### What happened on #685
| Check | Result |
|-------|--------|
| Missing credit journals (cred=0 on closed lots) | **165 / 731** |
| Direction of those lots | **100% short** |
| Exit mix among them | 87×10d + 78×stop |
| `sum(pnl − journal_flow)` on those lots | **$433,656.14** (= delta exactly) |
| Live `final_cash` vs `initial + close_pnl − open basis` | coherent (~$7.5k open premium still tied) |

Siblings (same bug, smaller short counts):
- #684: 7 short missing-credit → delta **$9,180**
- #692: 5 short → delta **$8,033**
- #683 Orange 2%: 283 short → delta **~$1.09M**

### Code defect
`PositionManager#add_leap_position` (~997–1037) **always** treats LEAP entry as a purchase:
- `@total_equity -= flow`
- `Journal.create!(flow: -flow, debit_credit: :debit, …)`

Share path (~233–246) correctly does long=debit / short=credit.

`PortfolioPositionManager#update_cash_on_entry` **does** credit cash on short entry (`@portfolio_cash += position_cost`). So **scoreboard `final_cash` / cash_events are trustworthy**; the journal ledger is not for short LEAPs.

On short close, `remove_positions` correctly journals a **debit** (buy-to-cover). With entry also a debit, both legs are negative → journal_cash too low by **~2× short entry premium** per closed short (matches lot 309331: entry deb −2547 + close deb −8826; flipping entry to +2547 credit adds +5094 to journal sum = that lot’s mismatch).

### Secondary note
`remove_positions` attaches the close journal to `positions_to_close.first.id` only — multi-lot flatten attribution quirk (not the #685 delta driver).

### Also check (separate)
LEAP `remove_positions` PnL uses `(exit − entry) × contracts × 100` for **both** directions; shorts should be `(entry − exit)`. Cash path via PPM may still be OK; journal/PnL identity for shorts deserves a ticket.

### Verdict for promote / ranking
- **Trust OA/cash / `final_cash`** for #685.
- **Do not** treat `cash_vs_journal_delta` as evidence the equity curve is fake — it is a **short-LEAP journal bug** amplified by 2% heat (more shorts).
- Fix: make `add_leap_position` journal + `@total_equity` direction-aware like the share entry path; backfill optional.
