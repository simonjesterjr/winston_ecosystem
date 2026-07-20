# Ticket: Speed up full validation PortfolioBacktestRun after vet_trend

**Status:** Proposed
**Priority:** unset

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md). After optimization grid completed, Orange **winner validation** full PBR (#41) took **~40 minutes** (1288 trading days, 15 markets) while screening/final combos in optimization_mode were much faster. White validation was shorter but still non-trivial.

## Problem

`PortfolioTrendVetter#vet!` runs a full persisted `PortfolioBacktestRunner` for the winner. Day-by-day `results_json` updates and verbose logging make validation the long tail after the 17-combo grid.

## Scope

1. Profile what dominates: SQL logging, `results_json` rewrite per day, signal eval, swap/ER path.
2. Options to consider:
   - Throttle `results_json` persistence (every N days / end only)
   - Disable day_by_day payload for validation runs
   - Lower log verbosity for rake vet path
   - Reuse optimization_mode runner metrics when already full-range
3. Preserve export correctness and UI show page usefulness for the winning run.

## Acceptance

- Orange-scale validation wall-clock measurably improved (target: well under ~15 min on same hardware) **or** documented why not
- Specs or smoke that winner export still produces correct metrics + `export_kind`

## Related

- Code: `portfolio_trend_vetter.rb`, `portfolio_backtest_runner.rb`
- Accelerate ticket: `2026-07-07-accelerate-portfolio-vet-optimization.md`
- Session: `docs/session-reports/2026-07-09-1308-orange-white-vet-trend.md`
