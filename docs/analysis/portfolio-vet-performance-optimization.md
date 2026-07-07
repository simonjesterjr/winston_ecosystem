# Portfolio Vet Performance — Analysis

**Type:** Technical reference  
**Date:** 2026-07-07  
**Context:** Portfolio Red `portfolios:vet_trend` (optimization #8) — first combo ~30+ min at `0/12`; wall-clock estimate 4–6 hours for 12 combos.

## Problem

`portfolios:vet_trend` is the production lab path for trend portfolio strategy selection, but it uses the **slowest** execution mode available in WUT. Operators cannot distinguish “stuck” from “slow” because `completed_combinations` only increments when an entire combo finishes.

## Date range (not a fixed “5 years”)

`PortfolioSignalOptimizationContext#compute_date_range` uses the **overlapping** range across portfolio markets (max start, min end). There is no hardcoded 5-year constant.

**Portfolio Red (2026-07-07):** 2020-10-13 → 2026-07-01 = **2,088 trading days** (~5.7 calendar years), constrained by PHYMF / MSOS membership.

## Why `vet_trend` is slow

### 1. Full persisted backtest per combo

`PortfolioTrendVetter` sets `date_subset_pct: 100`, which routes every combo through `run_full_backtest_combo`:

- Creates a real `PortfolioBacktestRun`
- Runs `PortfolioBacktestRunner` **without** `optimization_mode`
- Writes journals, positions, status updates, parquet
- Archives chart data via `PortfolioSignalOptimizationChartArchiver`
- Purges and destroys the run

The UI default path (`date_subset_pct: 25`) uses `optimization_mode` for screening — skips journals, parquet, ER jobs, broadcasts, etc.

### 2. Sequential combo execution

Combos run one-at-a-time inside `PortfolioSignalOptimizer#run_phase`. No combo-level parallelism.

### 3. Development throttle

In `development`, non-`optimization_mode` runs sleep **0.05s per day**:

```ruby
# portfolio_backtest_runner.rb
if Rails.env.development? && !optimization_mode?
  Async::Task.current.sleep(0.05) rescue sleep(0.05)
end
```

For Red: 2,088 × 0.05s ≈ **104s artificial delay per combo** (~21 min across 12 combos).

### 4. Async does not parallelize today

| Path | Async? | Parallel combos? |
|------|--------|------------------|
| UI (`PortfolioSignalOptimizationsController`) | `PortfolioSignalOptimizationJob.perform_later` | No — sequential in one job |
| `portfolios:vet_trend` | Synchronous in rake | No |

Moving vet to Sidekiq frees the terminal but does **not** reduce wall-clock unless combos are parallelized.

## Reference timings

| Run | Combos | Duration | Per combo |
|-----|--------|----------|-----------|
| Red opt #3 (old 6×1) | 6 | ~85 min | ~14 min |
| Blue opt #7 | 6 | ~88 min | ~15 min |
| Red opt #8 (12×2, full persisted) | 12 | est. 4–6 hr | ~20–30 min observed on combo 1 |

## Optimization options (ranked)

### A. Screening pipeline (largest win, low ranking risk)

Already implemented in `PortfolioSignalOptimizer`:

1. **Phase 1:** All combos on last **25%** of days (`screening_date_range`), `optimization_mode`, early-abort at 50% drawdown
2. **Phase 2:** **Top N** survivors on full overlap window, still `optimization_mode`
3. **Winner:** One full persisted backtest + export (already done by `PortfolioTrendVetter` after optimization)

**Estimate:** ~3–5× faster than 12 full persisted combos. Small risk: a combo that only wins on older regimes may be screened out.

### B. `optimization_mode` for 100% grid (large win, low risk)

At `date_subset_pct: 100`, use `run_combo` (transient) for all grid combos; only the **winner** gets `run_full_backtest_combo`. Integration spec (`portfolio_signal_optimizer_spec.rb`) expects full-range optimization without persisting intermediate runs.

**Estimate:** ~2–4× per combo (no journals/parquet/status + no dev sleep).

### C. Gate or remove dev sleep (easy win)

Skip throttle when `optimization_mode` or `ENV['SKIP_BACKTEST_THROTTLE']` for batch/vet runs.

### D. Combo-level parallel Sidekiq jobs (medium effort, high win)

Fan out one job per combo; coordinator ranks and triggers winner backtest. With ~5 Sidekiq threads, grid phase could approach **~3×** on multi-core.

Requires: idempotent result rows, failure handling, coordinator job.

### E. Shorter date window (e.g. 3 years)

Not configurable in `vet_trend` today. Would need `VET_START_DATE`, `VET_YEARS`, or similar on context.

| | ~3 years (~756 days) | Full overlap (~2,088 days) |
|--|---------------------|---------------------------|
| Speed | ~2.7× fewer days | Baseline |
| Strategy mechanics | Sufficient for 55-day breakouts | ✅ |
| Regime coverage | Misses more cycles | Stronger |
| Viability / trade-ready | Weaker sample | Preferred for export gates |

**Recommendation:** Short window OK for **screening / relative ranking** if all combos share it. For **trade-ready export**, re-validate winner on full overlap (or document the tradeoff in viability gates).

## Recommended two-phase doctrine

1. **Screen fast:** 25% recent window (or 3-year floor) + `optimization_mode` → pick winner
2. **Validate slow:** Full overlap on winner only → viability gates + export

Aligns with `docs/business-context/trade-ready-viability-gates.md` (gates on same range as optimization — interpret as “winner validation range”).

## Code touchpoints

- `winston_unit_test/app/services/portfolio_trend_vetter.rb` — hardcoded `date_subset_pct: 100`
- `winston_unit_test/lib/tasks/portfolio_trend_vet.rake` — no env overrides yet (ticket #5 backlog)
- `winston_unit_test/app/services/portfolio_signal_optimizer.rb` — `run_full_backtest_combo` vs `run_combo`
- `winston_unit_test/app/services/portfolio_signal_optimization_context.rb` — date range computation
- `winston_unit_test/app/jobs/portfolio_signal_optimization_job.rb` — async entry (UI only)
- `winston_unit_test/app/services/portfolio_backtest_runner.rb` — `optimization_mode`, dev sleep

## Related

- Ticket: `docs/tickets/2026-07-07-accelerate-portfolio-vet-optimization.md`
- P0 framework: `docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md`
- First-pass doctrine: `docs/analysis/portfolio-trading-strategy-evaluation.md`
- Red vet: `docs/tickets/2026-07-07-vet-portfolio-red-trend.md`