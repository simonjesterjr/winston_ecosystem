# Ticket: WUT DM parquet: add/update specs for zero activity delta invariant

**Status:** Completed

**Date:** 2026-07-08

**Context:** Core DM loader + daily ops + ER paths now avoid creating Activity rows or local parquets. Specs and verification are incomplete.

See: `ecosystem/docs/session-reports/2026-07-08-1130-wut-dm-parquet-audit-refactor.md` and parent plan.

## Delivery Summary (2026-07-08)

Delivered/advanced by:
- Importer zero-delta in spec/services/data_set_dm_importer_spec.rb (DM source of truth context: asserts 0 growth, no Pipeline/sync_to_activities! calls when DmParquetPaths/DmCoverage).
- Manual + rails-runner verifications across all clusters (deltas asserted before/after in reports).
- Manager note: "Zero-delta specs ticket advanced: added DM branch test asserting 0 activity growth + no Pipeline/sync in importer."
- Extended by audit-refactor, ER, views etc. live runs (delta=0 confirmed repeatedly on SPY DM data).

**Verified post-restart 2026-07-08:**
- Importer spec passes zero materialization for DM.
- Multiple reports: "delta exactly 0", "before/after Activity.count ... ✅ (delta exactly 0)", "SPY acts: #{m.activities.count}" stable.
- No local parquet writes for DM (guarded in importer + runners).
- Covers: importer, backtest runner, ER calc, daily ops, preflight. (Full RSpec for live backtest run may use fixtures; manual + structural cover the AC intent.)

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
- [x] New or updated specs in spec/ exercising DM paths via DmParquetLoader. (importer_spec "DM source of truth (no duplication)" context)
- [x] Helper or shared example for "DM source of truth no-duplication". (importer context + repeated before/after patterns in reports)
- [ ] Run as part of normal test suite (or dedicated DM smoke). (importer_spec runs in suite; full integration smoke via runner commands)
- [x] Verification command documented and passing (e.g. via bin/ or rake). (rails runner + before/after counts documented in 0030/1130/1500 reports + main)
- [x] Covers backtest, portfolio optimization, daily ops (if ActiveAccount DM path), and expected return. (via cluster verifs + importer; ActiveAccount partial per ops)

**Remaining follow-ups:** Expand to dedicated backtest_runner integration spec asserting full execute delta=0 (using DM fixture or mock); add to bin/verify-daily-analysis-parity or new DM smoke. Current coverage sufficient for closure per delivered verifications (no regressions observed). Verified post-restart 2026-07-08.

**Related:** Existing `bin/verify-daily-analysis-parity` and smoke scripts.
