# Ticket: WUT DM parquet: refactor remaining services for direct DM loader usage

**Status:** Proposed
**Priority:** unset

**Date:** 2026-07-08

**Context:** After daily ops and core runners, several supporting services still use `market.activities`, Activity queries, or MIVs.

See session report `2026-07-08-1130-wut-dm-parquet-audit-refactor.md` and the source-of-truth plan.

## Problem
Services such as:
- market_correlation_calculator
- leap_purchase_service
- option_chain_generator
- indicator_calculator
- data_set_reconciler (some paths)
- pyramid_indicator_correlator
- dataset_loader (legacy)
- simple_backtest_runner
- market_catalog
- market_data_update_planner

...still assume activity-backed data.

## Goal
Convert DM paths to use DmParquetLoader (full_history / load_for_range / bar_for) + composite keys. Isolate legacy non-DM.

## Acceptance Criteria
- [ ] Audit and update each listed service (and any discovered).
- [ ] DM paths produce correct results without touching activities table or local parquets.
- [ ] No breakage for Yahoo/CSV legacy markets.
- [ ] Update callers and any stats/freshness logic.

**Related:** Main refactor plan and zero-delta verification.
