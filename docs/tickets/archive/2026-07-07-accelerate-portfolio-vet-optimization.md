# Ticket: Accelerate portfolio vet / signal optimization

**Status:** In progress — Phase 1–2 **done** (2026-07-07); runtime verification + Phase 3 pending

**Priority:** P1 — unblocks lab throughput (Red/Blue/Orange/White vets)

**Date:** 2026-07-07

**Last updated:** 2026-07-07

**Context:** Portfolio Red vet optimization #8 stopped manually (~47 min on combo 1/12). Acceleration work implemented same session; Red re-started as optimization **#23** with fast defaults. Analysis: [`docs/analysis/portfolio-vet-performance-optimization.md`](../analysis/portfolio-vet-performance-optimization.md).

## Problem

`portfolios:vet_trend` used the slowest optimizer path (100% date subset + full persisted backtest per combo + dev sleep). The faster screening / `optimization_mode` paths existed for the UI but were not wired into the rake vet flow.

## Goal

Reduce wall-clock for a 12-combo first-pass vet from **~4–6 hours** to **~1–2 hours** without weakening winner validation for Wv2 handoff.

## Implementation status

### Phase 1 — Quick wins ✅ (WUT, 2026-07-07)

| Item | Status | Notes |
|------|--------|-------|
| `vet_trend` env vars | **Done** | `DATE_SUBSET_PCT`, `SCREENING_TOP_N`, `EARLY_ABORT_DRAWDOWN_PCT`, `SKIP_BACKTEST_THROTTLE` (default `1`) |
| Grid uses `optimization_mode` at 100% | **Done** | `run_full_range_optimization!` → `run_combo`; winner still gets full persisted run in `PortfolioTrendVetter#vet!` |
| Progress heartbeat | **Done** | `combo_progress_pct`, `combo_processed_days`, `last_activity_at` every 100 days |

**Code:** `portfolio_signal_optimizer.rb`, `portfolio_trend_vetter.rb`, `portfolio_backtest_runner.rb`, `portfolio_trend_vet.rake`

### Phase 2 — Screening doctrine ✅ (2026-07-07)

| Item | Status | Notes |
|------|--------|-------|
| Default screening 25% / top 5 | **Done** | `PortfolioTrendVetter::DEFAULT_SCREENING_CONFIG` |
| Two-phase doctrine docs | **Done** | `docs/analysis/portfolio-trading-strategy-evaluation.md` |
| `VET_YEARS` / `VET_START_DATE` | **Done** | `PortfolioSignalOptimizationContext#apply_date_constraints` |
| `portfolio_configs/README.md` | **Done** | vet_trend env table + examples |

### Phase 3 — Parallel combos ⏸ deferred

- `PortfolioSignalOptimizationComboJob` + coordinator — not started

## Acceptance

- [ ] Red-scale vet (12 combos, 9 markets) completes in **< 2 hours** on compose dev hardware with Phase 1 defaults — **in flight:** optimization #23
- [x] Winner backtest still runs on **full overlap** date range (`PortfolioTrendVetter#vet!` unchanged)
- [x] `portfolios:vet_trend` documents env vars in rake desc + `portfolio_configs/README.md`
- [x] Specs cover: screening path, 100% optimization_mode path, context date floors
- [x] No change to export JSON shape (export gates remain separate ticket)

## Verification

```bash
# Fast path (defaults)
PORTFOLIO="Portfolio Red" EXPORT=/portfolio_configs/portfolio-red.json \
  bin/rails portfolios:vet_trend

# Full-range grid (still optimization_mode — not old persisted path)
DATE_SUBSET_PCT=100 PORTFOLIO="Portfolio Red" bin/rails portfolios:vet_trend

# Optional date floor experiments
VET_YEARS=3 PORTFOLIO="Portfolio Red" bin/rails portfolios:vet_trend
```

Monitor optimization #23: `completed_combinations` / `total_combinations` (expect 17 = 12 screening + 5 finals with defaults).

## Out of scope

- Wv2 import changes
- Viability gate thresholds
- Null-Sharpe ranking fallback (separate P0 item)
- Phase 3 parallel Sidekiq combos

## Related

- Analysis: `docs/analysis/portfolio-vet-performance-optimization.md`
- Framework P0: `docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md` (partial env-vars overlap — close when framework ticket updated)
- Red vet: `docs/tickets/2026-07-07-vet-portfolio-red-trend.md`
- Plan task #5: `plans/portfolio-overlap-rebuild.md.tasks.json`