# Ticket: Close-only parquet load for correlation builder

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). Correlation greedy builds still take ~15–25 min for large candidate sets despite DmCoverage date bounds + process-level close cache, because `full_history` materializes full Bar objects with all indicator columns.

## Problem

Portfolio Orange/White builds are ops-time expensive; most correlation work only needs date + close.

## Scope

1. Add `DmParquetLoader` path (or option) to load only `date, close` for correlation.
2. Use it from `MarketCorrelationCalculator#load_full_close_series`.
3. Keep cache; measure wall-clock on 40+ candidate build.

## Acceptance

- Large greedy build completes in substantially less time without changing membership math
- Specs still green for correlation calculator

## Related

- `market_correlation_calculator.rb`, `dm_parquet_loader.rb`
