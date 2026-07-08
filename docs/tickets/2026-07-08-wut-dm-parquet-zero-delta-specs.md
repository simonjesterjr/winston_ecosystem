# Ticket: WUT DM parquet: add/update specs for zero activity delta invariant

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Core DM loader + daily ops + ER paths now avoid creating Activity rows or local parquets. Specs and verification are incomplete.

See: `ecosystem/docs/session-reports/2026-07-08-1130-wut-dm-parquet-audit-refactor.md` and parent plan.

## Problem
- No automated assertions that "DM backtest/optimization/daily ops/ER calculation produces delta=0 Activity rows and no local price/calculated parquets".
- Manual runner checks exist but are not in the test suite.
- Risk of regression as more paths are added.

## Goal
Add RSpec / test helpers that:
- Run a small DM backtest or signal optimization on a covered market.
- Assert activity count unchanged.
- Assert no new local parquet files created under data/price_data or data/calculated for DM symbols.
- Cover result rendering re-pull paths where possible.

## Acceptance Criteria
- [ ] New or updated specs in spec/ exercising DM paths via DmParquetLoader.
- [ ] Helper or shared example for "DM source of truth no-duplication".
- [ ] Run as part of normal test suite (or dedicated DM smoke).
- [ ] Verification command documented and passing (e.g. via bin/ or rake).
- [ ] Covers backtest, portfolio optimization, daily ops (if ActiveAccount DM path), and expected return.

**Related:** Existing `bin/verify-daily-analysis-parity` and smoke scripts.
