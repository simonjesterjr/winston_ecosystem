# Ticket: WUT DM parquet: implement full bar re-pull + rendering in all backtest result views and charts

**Status:** Proposed
**Priority:** unset

**Date:** 2026-07-08

**Context:** Continuation of the WUT DM source-of-truth refactor (see `ecosystem/plans/wut-dm-parquet-source-of-truth.md`). Core runners, daily ops, creation sites, and expected-return are on DM Bar loader + (market_id, date) composites with result parquets carrying identity. Result views and charts still rely heavily on `Activity.where` and `activity` associations for candlesticks, equity curves, positions tables, MTM, passed signals, etc.

See:
- Session report: `ecosystem/docs/session-reports/2026-07-08-1130-wut-dm-parquet-audit-refactor.md`
- Parent ticket: `ecosystem/docs/tickets/2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md`
- BacktestResultsReader (market_key support) and DmParquetLoader

## Problem
- Result rendering (backtest_runs/ and portfolio_backtest_runs/ views) performs direct Activity queries and includes for chart data, exit prices, day-by-day, etc.
- Old result parquets lack full identity; new ones do via market_id + trade_date.
- Without re-pull, DM-only runs will show incomplete or broken visuals.
- Violates "rich bar data is re-pulled from the DM loader at render time".

## Goal
- All result views and charts use `BacktestResultsReader` (or equivalent) + stored market_key / (market_id, bar_date) to fetch Bars via `DmParquetLoader` (or range loads).
- Treat captured result data (P&L, journals, risk) as sufficient; re-pull only for OHLCV + indicators when needed.
- Support holes by triggering DM fill if necessary.
- Legacy (non-DM) paths continue to work via activities.

## Acceptance Criteria
- [ ] Update _candlestick_chart.html.erb, _equity_chart.html.erb, _day_by_day.html.erb, _positions_table.html.erb, _passed_signals.html.erb (and portfolio equivalents) to prefer DM re-pull.
- [ ] Add helper (e.g. in services or view helpers) `load_bars_for_result_rows` or similar using reader + DmParquetLoader.
- [ ] Charts and tables render rich data (OHLCV, ATR, indicators) for DM backtests using re-pulled Bars.
- [ ] No new Activity rows created during view rendering for DM runs.
- [ ] Old result parquets gracefully degrade (use captured data + note missing bars).
- [ ] Manual verification: DM backtest run → result show → charts show correct data from loader, activity count unchanged.
- [ ] Update any controller actions that prepare data for these views.

**Related:** Wv2 daily analysis rendering patterns for reference.
