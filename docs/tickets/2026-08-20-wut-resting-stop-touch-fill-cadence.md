# Ticket: WUT lab cadence — resting stop-touch entries

**Status:** Scored — do not promote pack default; v2 Mint re-score **survived** (537 +242 vs 536 +94)  
**Priority:** P1  
**Date:** 2026-08-20  
**Monolith:** winston_unit_test  
**Experiment:** `resting_stop_touch_v1`  
**Parent (ops/BG, still Blocked):** [`2026-08-20-resting-session-stop-orders.md`](2026-08-20-resting-session-stop-orders.md)  
**Related:** ADR-009 next-open default; `docs/adr/2026-07-25-lab-t1-fill-queue.md`; [`2026-07-26-hybrid-fill-price-level-pyramid.md`](2026-07-26-hybrid-fill-price-level-pyramid.md) (pyramid-only touch — **rejected** as S4 pack default)

**Authorization:** Lab geometry only. No Broker Gateway (BG) `order_write`. Do not stamp this cadence as pack default until scored.

---

## Why this can start now

The parent ticket is blocked on BG L3. This child is **not**. Winston Unit Test (WUT) already has `LabFillCadence.price_level_fill` (bar-touch → level; gap-through → open) and uses it for **pyramids** under `hybrid_entry_next_pyramid_price_level`. **Entries are still next-bar open** on every current mode that uses the T+1 queue.

Automating live resting buy-stops against a next-open backtest would be a silent strategy change. The lab must grow a matching entry cadence **and fingerprint it** before any live slate.

## What you would miss if you only “fill T+1 when the open is still above the old stop”

That is a **filter on the existing queue**, not Turtle stop-entry.

`Breakout20DayStrategy` / `Breakout55DayStrategy` already fire when **today’s high/low clears the prior window extreme** (`activity.high > max_high` of `StrategyLookback.recent_window`, current bar excluded). The pathology is the **delay**: signal on T’s touch, fill T+1 **open**.

Turtle / Donchian resting entry:

- Parked level = prior Donchian (e.g. 110).
- Session T high trades through 110 → fill **that session** at 110 (or at **open** if open already through).
- T+1 open 100 is then a **stop-out of a real position**, not a reason to skip an unfilled ticket.

| Tape | Next-open (today) | Resting touch (this ticket) |
|------|-------------------|-----------------------------|
| T high clears 110, T+1 open 100 | Buy 100, stop 92 (or skip overlay) | Buy **110 on T**, stop 110−2N; T+1 open 100 **exits** if through stop |
| T open 115 (gap through 110) | Buy 115 next day if still queued | Buy **115 on T**, stop 115−2N |
| T high 105, channel 110 | No signal | No fill |

Do **not** reuse `hybrid_entry_next_pyramid_price_level`. That mode keeps `entry_fill_cadence = next_bar_open`.

Do **not** use `same_bar_open`. That fills at T’s **open**, which is usually *below* the breakout.

## Frozen v1 doctrine

New top-level mode: **`resting_stop_touch`**

| Leg | Cadence |
|-----|---------|
| Initial entry | `price_level_touch` on the **signal bar** (no T+1 entry queue) |
| Pyramid | existing `price_level_touch` (`last_fill ± pyramid_atr_multiplier × N`, sessions **after** last lot) |
| Protective stop | existing working-stop vs bar low/high **after** the position is live |

Fill helper: `LabFillCadence.price_level_fill` (already specified).

**Entry level** for Donchian high/low breakouts: prior-window `max_high` / `min_low` (the boolean the strategy already uses). Runner must know the **number**, not only true/false — add a level on the signal or recompute the same window at fill.

**Stop:** fill-relative, `fill ± atr_multiplier × ATR` of the signal/fill bar (same PositionManager rule as today).

**Same-bar OHLC ambiguity** (high touches entry and low would pierce the new stop):

- Gap-through (**fill = open**): same-bar stop-out **allowed** (path is known).
- Mid-bar touch (**fill = level**): **no** protective stop-out on that same bar (same reason pyramids already skip the last-lot session). Next bar can stop.

**v1 strategy set:** high/low Donchian only (`Breakout20DayStrategy`, `Breakout55DayStrategy`, and the other `*.high > max_high` family). **Out of v1:** close-confirm recipes (`Breakout20DayCloseStrategy`, etc.) — close-confirm + resting stop-entry is a mixed rule; do not pretend they are the same.

**Capacity:** use existing heat / cash / symbol gates **at fill**. Pre-session ranked reservation is the parent ticket, not this one.

**Defaults:** do **not** change `LabFillCadence::DEFAULT` (hybrid price-level) or S4 / Turtle pack stamps. Opt-in via `results_json["fill_cadence"]` / `LAB_FILL_CADENCE` / PBR “Set for next run.”

**Fingerprint:** `fill_cadence`, `entry_fill_cadence`, and `pyramid_fill_cadence` are **methodology identity**. They are **not** in `TradingStrategyFingerprintCapture` payload today — add them (omit only if you must preserve legacy hashes when cadence is the old default; prefer include-always once this mode exists so next-open vs resting-touch cannot share a fingerprint).

## Scope

1. `LabFillCadence`: add `RESTING_STOP_TOUCH = "resting_stop_touch"` to `MODES`; resolve entry+pyramid both `price_level_touch`; `uses_t1_entry_queue?` → false for this mode.
2. Runner: when this mode, **do not** enqueue initial entries for T+1 open. On signal bar, fill via `price_level_fill` at the Donchian level; skip if helper returns nil.
3. PBR UI + helper badges/labels for the new mode.
4. Fingerprint payload includes the three cadence stamps.
5. Specs for the locked tapes below (Portfolio Backtest Run (PBR) or `LabFillCadence` + runner).
6. After geometry is green: **small scorecard** vs `next_bar_open` on Turtle chassis (Mint S2 and/or Yellow S1, same window as `turtle_systems_v1`). Report only — **no pack promotion**.

## Locked tapes (acceptance)

Channel long = 110, 2× Average True Range (ATR) = 8.

- [x] T `open=100, high=111, low=99, close=108` → **fill 110**, stop **102**. Not T+1 open.
- [x] Same, then T+1 `open=100` → **stop-out at 100** (gap through 102), not a new entry at 100.
- [x] T `open=115, high=116` → **fill 115**, stop **107**.
- [x] T `open=100, high=105` → **no fill**.
- [x] Mid-bar fill 110 with T `low` through 102 → **still open at T close** (ambiguity freeze); may stop on a later bar.
- [x] Gap-through fill 115 with T `low` through 107 → **stopped same bar**.
- [x] Pyramid still fills on a **later** session when high/low touches `last_fill ± N×ATR`, at level or open if gapped (existing helper).
- [x] Fingerprint of a resting-touch run **≠** fingerprint of an otherwise identical next-open run.
- [x] Unstamped PBR default unchanged (`hybrid_entry_next_pyramid_price_level`).

## Non-goals

- BG / Desk Send / live order slate (parent).
- Skipping T+1 tickets because open is through a hypothetical 102.
- Changing ADR-009 ops default (that ADR is for Winston v2 (Wv2) EOD next-open until a later fill-story ADR).
- Promoting S4 or Turtle paper Operational Portfolios (OPs) to this cadence.
- Close-confirm breakouts, confirmational-entry parks, one-cancels-other both-side slates.
- Pre-session heat reservation of unfilled parks.

## Implementation notes

- `winston_unit_test/app/services/lab_fill_cadence.rb` — extend `MODES` / `resolve` / `uses_t1_entry_queue?`.
- `portfolio_backtest_runner.rb` — branch initial entry off the T+1 queue when this mode; pass fill price + fill bar = signal bar.
- `trading_strategy_fingerprint_capture.rb` — cadence keys on payload.
- `portfolio_backtest_runs_helper.rb` + fill-cadence UI — label “Resting stop-touch (entry+pyramid)”.
- Specs next to `spec/services/lab_fill_cadence_spec.rb` and `spec/services/portfolio_backtest_pyramid_price_level_spec.rb`.

## Depends on

Nothing in BG. Can land behind the existing fill-cadence switch.

## Landed 2026-08-20 (geometry)

Opt-in `LabFillCadence::RESTING_STOP_TOUCH`. Unstamped PBR default still `hybrid_entry_next_pyramid_price_level`. PBR “Set for next run” includes the new mode.

- Runner fills initial Donchian entries on the signal bar via `price_level_fill` (no T+1 queue). Close-confirm recipes pass `resting_stop_touch_out_of_v1`.
- Mid-bar fill: no protective stop that bar. Gap-through fill (= open): same-bar stop allowed. Later-bar gap through the working stop fills at **open**.
- Fingerprint: cadence stamps included when the resolved mode is **not** the unstamped default (legacy hybrid-price hashes stay stable; next-open ≠ resting-touch).
- Specs: `spec/services/lab_fill_cadence_spec.rb`, `spec/services/portfolio_backtest_resting_stop_touch_spec.rb`, helper + fingerprint coverage, PositionManager fill-price stop, PBR fill-cadence request spec.

**Scorecard (2026-08-21):** completed. Freeze — do **not** promote. Write-up: [`docs/analysis/2026-08-21-resting-stop-touch-v1-scorecard.md`](../../analysis/2026-08-21-resting-stop-touch-v1-scorecard.md).

| Book | Resting | Next-open | Δret | Δdd |
|------|---------|-----------|------|-----|
| Mint S2 #533 vs #532 | −100 / 101 DD / 97 trades | +395 / 44 DD / 747 | **−495** | +56 |
| Yellow S1 #535 vs #534 | +206 / 40 DD / 1174 | +121 / 30 DD / 1267 | +85 | +10 |

Median Δret **−205**, Δdd **+33**. Yellow made more with worse DD and negative free cash. Lab switch stays; ADR-009 and Turtle paper OPs unchanged.

**Mint −100% diagnosed 2026-08-22** ([analysis](../../analysis/2026-08-22-mint-resting-stop-touch-ruin.md)): not same-bar stops (0 on both arms); not unique short-margin cash (both cash-negative 2019-12-31 with ~$10k equity). Ruin is unadjusted reverse-split jumps (USO 1-for-8 2020-04-29, XOP 1-for-4 2020-03-30) covered at the **open** under resting v1. Those lots ≈ −$9.2k of −$9.0k 2020 P&L. Do not revert gap-through-at-open; fix parquet / add a split-guard before re-scoring Mint.
