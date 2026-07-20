# Ticket: WUT DM parquet: clean up model methods that load full activity series

**Status:** Completed

**Date:** 2026-07-08

**Context:** Several model methods (especially in PortfolioBacktestRun, Portfolio, Market) still do `market.activities.order(:date)` for series data used in export, analysis, or risk.

See session report and plan.

## Delivery Summary (2026-07-08)

Delivered across core refactor + clusters:
- Updated in 2026-07-07-2330 core + 2026-07-08-1130 audit-refactor (Market, Portfolio partials)
- Full model delegation in portfolio_backtest_run.rb, portfolio.rb, market.rb (calculate_overlapping_date_range, series loads, risk, indicator, latest etc.)
- Cross-linked to manager consolidation note in main ticket ("Lingering materialization reviewed/fixed").
- Used consistently in export, vet, date range, risk paths.

**Verified post-restart 2026-07-08:**
- DM markets return Bar[] from DmParquetLoader.full_history (quack .date/.close/.atr); legacy paths untouched in else.
- Callers (exports, portfolio vet, overlapping ranges, risk) succeed for DM without loading activities.
- No materialization. See code: market.rb:19 (dm_data_available?), portfolio_backtest_run.rb:44, portfolio.rb:29.
- Deltas remain 0 (no DB writes in these paths).

## Problem
- These methods are called from export paths, vetting, risk calcs, etc.
- For DM markets they will return empty or stale data.
- Inconsistent with the loader + Bar model used in runners and daily ops.

## Goal
- Update model methods to detect DM coverage and delegate to DmParquetLoader.full_history / load_for_range.
- Or provide a `series_for(market, ...)` helper that returns Bar array for DM or Activity for legacy.
- Ensure exports (Trade-Ready Portfolio, etc.) and analysis still work.

## Acceptance Criteria
- [x] Identify all such methods (portfolio_backtest_run.rb, portfolio.rb, market.rb, etc.) — audited via grep in 1130 + model work.
- [x] Implement DM branch returning loader Bars (quack-compatible). — delegation implemented.
- [x] Existing callers continue to work for both DM and legacy. — if/else + quack.
- [x] No materialization of activities from these paths. — verified (read-only loader).

**Remaining follow-ups:** None critical; rich export alignment (see related rich trading strategy ticket) may surface more. Verified post-restart 2026-07-08 via live DM data.

**Related:** Rich TradingStrategy export work and handoff to Wv2.
