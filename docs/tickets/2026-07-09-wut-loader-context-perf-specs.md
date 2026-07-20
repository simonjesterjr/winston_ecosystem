# Ticket: Specs for DM loader and optimization context perf fixes

**Status:** Proposed
**Priority:** P3

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md). Two production stalls were fixed without automated tests:

1. `DmParquetLoader#describe_columns` — memoized (was DESCRIBE per bar)
2. `PortfolioSignalOptimizationContext#build_activities_by_date` — load `full_history` once per market (was O(days × markets))

## Problem

Regressions would re-introduce multi-hour hangs on `portfolios:vet_trend` with no failing CI.

## Scope

1. Unit/spec: memoize behavior of `describe_columns` (single DESCRIBE / connection path per loader instance; safe empty fallback).
2. Unit/spec or service spec: `build_activities_by_date` calls `DmParquetLoader.full_history` at most once per market for a multi-day range (stub/spy).
3. Optional: micro-benchmark assertion only if stable in CI; prefer call-count stubs over wall-clock.

## Acceptance

- Specs green in WUT container
- Fail if full_history is invoked N×days for N markets in context build

## Related

- Code: `winston_unit_test/app/services/dm_parquet_loader.rb`
- Code: `winston_unit_test/app/services/portfolio_signal_optimization_context.rb`
- Session: `docs/session-reports/2026-07-09-1308-orange-white-vet-trend.md`
