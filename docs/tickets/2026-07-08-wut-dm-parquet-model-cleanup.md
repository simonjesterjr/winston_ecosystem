# Ticket: WUT DM parquet: clean up model methods that load full activity series

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Several model methods (especially in PortfolioBacktestRun, Portfolio, Market) still do `market.activities.order(:date)` for series data used in export, analysis, or risk.

See session report and plan.

## Problem
- These methods are called from export paths, vetting, risk calcs, etc.
- For DM markets they will return empty or stale data.
- Inconsistent with the loader + Bar model used in runners and daily ops.

## Goal
- Update model methods to detect DM coverage and delegate to DmParquetLoader.full_history / load_for_range.
- Or provide a `series_for(market, ...)` helper that returns Bar array for DM or Activity for legacy.
- Ensure exports (Trade-Ready Portfolio, etc.) and analysis still work.

## Acceptance Criteria
- [ ] Identify all such methods (portfolio_backtest_run.rb, portfolio.rb, market.rb, etc.).
- [ ] Implement DM branch returning loader Bars (quack-compatible).
- [ ] Existing callers continue to work for both DM and legacy.
- [ ] No materialization of activities from these paths.

**Related:** Rich TradingStrategy export work and handoff to Wv2.
