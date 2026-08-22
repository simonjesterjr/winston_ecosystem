---
status: Diagnosed
date_opened: 2026-08-22
environment: local compose Winston Unit Test (WUT) lab
baseline: Portfolio Backtest Run (PBR) 532 — Mint S2 `next_bar_open`
candidate: PBR 533 — Mint S2 `resting_stop_touch`
scope: Mint Turtle S2 2019-11-01…2026-08-10; same books, same Trading Strategy (TS) #77, $10k static 1%
adversarial_review: self-skeptical, 2026-08-22, holds with caveats, high confidence on trigger, medium on counterfactual 2021 path
---

# Mint S2 resting-touch ruin — reverse-split gaps, not same-bar stops

## Summary

Mint’s resting run (PBR **533**, −100% / 101% maximum drawdown) vs next-open (PBR **532**, +395% / 44% DD) is **not** a same-bar stop bug and **not** unique short-margin accounting. Both arms went cash-negative on 2019-12-31 with ~$10k equity still intact. Resting has **zero** same-bar exits. The book died in Feb–Apr 2020 because data_manager (DM) parquet for USO and XOP still contains **unadjusted reverse-split jumps**, and resting v1 covers shorts at the **gap-through open**. Four USO lots covered at $18.01 on 2020-04-29 (1-for-8 reverse split) and three XOP lots covered at $31.10 on 2020-03-30 (1-for-4 reverse split) account for **≈ $9.2k of the $9.0k 2020 P&L**. Next-open filled the same stop-hits at the **working stop** (~$3.23 and ~$18.08), so it survived. Yellow S1 has neither symbol; its +85 return / +10 DD is the cleaner cadence comparison.

Primary classification: **Capture or data artifact** (unadjusted reverse splits) **interacting with** resting’s intentional gap-through-at-open stop fill.

## Comparison contract

- Governing requirement: ticket `2026-08-20-wut-resting-stop-touch-fill-cadence` — fill-relative stop; gap-through protective stop fills at **open**; mid-bar fill does not stop the same bar. ADR-009 remains next-open for ops. Winston EOD parquet (ADR-002) does **not** currently specify split adjustment.
- Shared input: Portfolio Mint, TS #77 Breakout55/20, Turtle chassis, overlapping window of parent PBR 432.
- Baseline: `fill_cadence=next_bar_open` — stop-out uses `execute_exit` at the working stop when high/low tags it (`portfolio_backtest_runner.rb` stop branch without `exit_price_override`).
- Candidate: `fill_cadence=resting_stop_touch` — if open is already through the stop, `exit_price_override: activity.open` (`portfolio_backtest_runner.rb` ~1818–1831).

## Target comparison

| Field | Baseline 532 | Candidate 533 | Contract/notes |
|-------|--------------|---------------|----------------|
| Terminal return / DD / trades | +394.7% / 44.4% / 747 | −100.2% / 100.6% / 97 | Equity ruin, not a close call |
| Same-bar exits / same-bar stops | **0 / 0** | **0 / 0** | Same-bar freeze held; hypothesis falsified |
| Avg hold (days) | 29.4 | 32.9 | Similar |
| Stop-out rate | 83.5% | 70.1% | Resting not “stopped more often” |
| Long vs short lot mix | 395 / 352 | 36 / 61 | Resting died short-heavy in 2020 |
| Approx closed P&L long / short | +50.6k / −11.6k | +0.15k / −10.3k | Resting never got the 2021 long explosion |
| Cash on 2019-12-31 | **−$4,707** | **−$3,477** | Shared; equity still ~$10.4k / ~$10.1k |
| Equity 2020-06 | $11,382 | $3,169 | Divergence is H1 2020 |
| Equity 2021-06 | $39,187 | $523 | Baseline recovered; candidate already dead |
| First equity < $5k | never | 2020-04-29 | Same day as USO reverse-split cover |

## Dependency or contention scope

| Peer | Order | Baseline | Candidate | Classification |
|------|------:|----------|-----------|----------------|
| VNQ short Dec 2019 cover | 2019-12-31 | Stop ~$92; cash −$4.7k | Stop ~$92; cash −$3.5k | Same (short-cover cash drain) |
| Short-entry cash credit | 2019-12 | Shorts add `units×entry` to cash | Same rule | Same (ledger, not ruin) |
| XOP 1-for-4 reverse split | 2020-03-30 | Stop-fill ~$18.08 on open $31.10 | Cover at **open $31.10** | Different value — data jump × candidate rule |
| USO 1-for-8 reverse split | 2020-04-29 | Stop-fill ~$3.23 on open $18.01 | Cover at **open $18.01** | Different value — data jump × candidate rule |
| OIH ~1-for-20 reverse split | 2020-04-15 | — | Shorts already flat Apr 9; longs start $91.47 | Candidate-only luck (not held through jump) |
| 2021 long trend | 2021 | +$34.2k on 73 lots | +$0; 9 lots, $523 equity | Contention-driven — no capital left |
| Yellow S1 books | n/a | No USO/XOP/OIH | No USO/XOP/OIH | Cross-scope: cleaner cadence cell |

## Invariant and conservation checks

- **Same-bar stops:** 0/97 candidate, 0/747 baseline. Independently counted from `position.bar_date == last journal.trade_date`.
- **2020 candidate P&L ≈ −$9,000.** USO four Apr lots at $18.01 cover ≈ **−$6,131**. XOP three Feb lots at $31.10 cover ≈ **−$3,097**. Sum **−$9,228**. Remainder of 2020 after removing those two events ≈ **+$229**. Baseline 2020 P&L ≈ **−$202**.
- **Parquet (same files both arms):**
  - USO 2020-04-28 close **2.13** → 2020-04-29 open **18.01** (ratio ~8.5; USCF 1-for-8 reverse split after close 28 Apr, first trade 29 Apr).
  - XOP 2020-03-27 close **8.03** → 2020-03-30 open **31.10** (ratio ~3.9; State Street 1-for-4 reverse split effective 30 Mar).
  - OIH 2020-04-14 close **4.82** → 2020-04-15 open **91.47** (energy-service reverse split; shorts were already closed).
- **Counterfactual (stop-fill like baseline on the same jumps):** USO lots would lose ~1 ATR instead of ~$1.5k each; XOP stacked shorts would be ~scratch instead of −$3k. Candidate would not have been at $3k equity on 29 Apr. **2021 path after that is not proven** (different heat/cash), so we do not claim Mint would have matched +395%.

## Executable trace

### Baseline (532)

`process_portfolio_day_next_open` → `update_stops_and_check_hits`: short hit if `activity.high >= stop`; `execute_exit` without override → `PositionManager#remove_positions` uses `updated_stop \|\| original_stop` (`position_manager.rb` ~310–315). Apr 29 USO high 18.22 ≥ last-lot stop 3.226 (`move_to_last_entry` shared stop) → cover at **3.23**.

### Candidate (533)

Same stop check, plus resting branch: if `activity.open >= stop` (short), `exit_price_override: activity.open` (`portfolio_backtest_runner.rb` ~1818–1831). Apr 29 USO open 18.01 ≥ 3.73 → cover at **18.01**. Mar 30 XOP open 31.10 ≥ 18.13 → cover at **31.10**. Same-bar skip (`same_bar_level_fill?`) never fired on this run.

Short cash: `add_position` credits `units×fill` on short entry; cover debits `units×exit`. That is why Dec 31 cash is negative on **both** arms after covering VNQ while longs are still deployed. Equity was still ~$10k. Terminal cash −$23 on 533 is leftover after equity hit zero in Mar 2022, not the 2019 cash print.

## Classification

**Capture or data artifact** (primary).

Winston EOD parquet for USO/XOP/OIH is not reverse-split-adjusted across the COVID corporate actions. Resting’s gap-through-at-open is the *correct live stop-market* on a continuous tape; on an 8× overnight jump it is a forced cover at the post-split print. Next-open’s “fill at stop” is optimistic vs a real gap and accidentally *survives* the artifact.

Why not the other labels:

| Label | Why not |
|-------|---------|
| Candidate defect (same-bar stop) | Zero same-bar exits |
| Candidate defect (gap-through at open) | Matches frozen v1 doctrine; would be right on adjusted bars |
| Baseline defect | Baseline stop-at-level is the old lab convention, not a new bug |
| Intentional contract change (alone) | The 8×/4× prints are not overnight trading; they are splits |
| Short-margin accounting as unique cause | Shared Dec 31 cash dip; equity still $10k |
| Undetermined | Trigger lots, bars, and ratios are identified |

## Recommendation

1. **Keep the freeze.** Do not promote `resting_stop_touch`. Yellow is still mixed (+85 ret, +10 DD).
2. **Do not revert gap-through-at-open** as a v2 “fix.” That would make lab stops *less* like live resting orders.
3. **v2 landed 2026-08-22** (issue `2026-08-22-unadjusted-reverse-split-jumps`, ticket `2026-08-22-corporate-action-stop-safeguards`):
   - DM back-adjusted USO (×8), XOP (×4), OIH (×20). Overnight ratios now 1.057 / 0.968 / 0.949 (not split-like). Backups `bars.parquet.pre_split_adjust`.
   - WUT resting: tradable gap still covers at open; split-like covers at working stop.
   - Wv2 Stop-Out Reconciliation: `split_like_gap` + `CORPORATE_ACTION_HOLD`.
   - BG `order_write` hold is ticketed; L3 not shipped.
4. **Re-score Mint:** pending PBRs **536** (next-open) and **537** (resting) under `resting_stop_touch_v2`. Do not overwrite 532/533.

## Adversarial verification

- Mode: self-skeptical
- Verdict: **holds with caveats**
- Re-derived: 0 same-bar exits; both arms cash-negative 2019-12-31; USO 18.01/2.13 ≈ 8.5 vs 1-for-8 split; XOP 31.10/8.03 ≈ 3.9 vs 1-for-4; USO+XOP covers ≈ −$9.2k vs 2020 P&L −$9.0k.
- Corrections: first draft called it “cash-ruin”; the lethal object is **equity** after split covers. Cash print in Dec 2019 is a short-cover ledger effect on both arms.
- Remaining uncertainty: whether an adjusted-bar Mint re-run would still lag next-open in 2021 (path dependence). Not needed for the freeze.

## Cross-references

- Scorecard: `docs/analysis/2026-08-21-resting-stop-touch-v1-scorecard.md`
- Ticket: `docs/tickets/2026-08-20-wut-resting-stop-touch-fill-cadence.md`
- ADR-002 parquet (no split-adjust clause today)
- Code: `winston_unit_test/app/services/portfolio_backtest_runner.rb` resting stop gap-through; `position_manager.rb` stop-level exit
- PBRs: 532/533 (v1 pair), 536/537 (v2 re-score pending), 432 (parent hybrid-price)
