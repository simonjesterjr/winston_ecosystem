# Ticket: WUT — Remove belongs_to :activity for DM data; refactor creation + usage sites + result rows to composite (market_id, date) + DM Bar loader

**Status:** Proposed (see main plan)
**Priority:** P2

**Date:** 2026-07-07

**Context:** See authoritative plan `ecosystem/plans/wut-dm-parquet-source-of-truth.md` and main ticket. All legacy non-DM records are defunct. No shims or transitional stubs. Direct refactor to composite keys + Bar from DM loader. DM owns indicators.

## Problem

`belongs_to :activity` (NOT NULL activity_id on positions, trading_signals, backtest_indicator_values, etc.) and `Activity` queries are used throughout creation (Position.manage_position, signal gen, BIVs) and usage (runners, views doing Activity.where for charts on results, expected return calcs, Market#risk, Activity#atr via MIV). Result parquets currently lack per-row market identity. This violates DM source of truth and prevents clean removal of duplication.

## Goal

Every creation and usage site for DM-sourced data uses composite `(market_id, date)` (or equivalent non-persisted key) + Bar object from the DM loader. Result rows are always identifiable by `(market_id, date)`. No Activity rows created for DM data. Result parquets minimal + identity; rich data re-pulled. "Just use DM to pull the data again."

## Acceptance Criteria

- [ ] Result rows: BACKTEST schema + writer/reader ensure `(market_id, date)` identifiability per row (chosen representation: column(s), concat, or reversible hash). Exposed for re-pull.
- [ ] Creation sites refactored: Position, TradingSignal, PassedSignal, BacktestIndicatorValue, MarketIndicatorValue, Journal etc. no longer take or store activity_id for DM data. Use `(market_id, date)` + Bar (or transient equivalent).
- [ ] Usage sites refactored: Remove/replace all Activity.where(market_id, date), .activity, Activity#atr, Market#risk via activity, direct queries in backtest result views, expected_return calculators, charts, pyramid correlator, etc. Use stored keys + DM loader re-pull (or Bar at runtime).
- [ ] Runners produce only minimal output: journals/positions with identity keys (no activity materialization).
- [ ] Result views: Use result parquet data + DM loader for any additional bar data or to address holes (missing dates or indicators). Re-pull is the model.
- [ ] Models: belongs_to :activity remains only for truly legacy (defunct) non-DM paths. Plan for eventual schema cleanup (nullable or removal of activity_id on DM paths).
- [ ] No Activity rows: Post-DM flow for a symbol, zero new rows in activities or MIVs for that market from the DM path.
- [ ] Legacy isolated: Existing backtest runs and non-DM symbols continue to function; new work does not create activity dependencies for DM symbols.
- [ ] Tests: Cover loader-based creation, result identity roundtrip, re-pull in views, hole scenario.

## Related

- Main ticket + `ecosystem/plans/wut-dm-parquet-source-of-truth.md` (detailed call sites for .id, activities in Position creation, journal, strategies, views doing Activity.where for charts)
- Wv2 ParquetBar (id=nil) pattern for inspiration
- Models: activity.rb, market.rb, position.rb, journal.rb, market_indicator_value.rb
- Runners and operations services

**Only after plan + adversary verification.**
