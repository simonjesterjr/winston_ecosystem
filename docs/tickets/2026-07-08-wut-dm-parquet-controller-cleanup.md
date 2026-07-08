# Ticket: WUT DM parquet: clean up remaining Activity queries in controllers

**Status:** Proposed

**Date:** 2026-07-08

**Context:** Part of the full WUT DM source-of-truth refactor. Daily ops, runners, and some creation paths are converted. Several controllers still perform `market.activities`, `Activity.where`, and joins for readiness checks, exports, logging, and data preparation.

See:
- Session report: `ecosystem/docs/session-reports/2026-07-08-1130-wut-dm-parquet-audit-refactor.md`
- Parent plan and ticket: `ecosystem/plans/wut-dm-parquet-source-of-truth.md`, `2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md`

## Problem
- `backtest_runs_controller.rb`, `portfolio_backtest_runs_controller.rb`, `data_sets_controller.rb` (remaining actions), `portfolios_controller.rb`, `option_chains_controller.rb`, `portfolio_builder_controller.rb` (partially addressed) still hit activities directly.
- Some checks like `market.activities.exists?` or counts block or misreport DM markets.
- Logging and prep code assumes activities for DM runs.

## Goal
- Replace DM-path activity access with `DmParquetLoader` + coverage checks or result reader.
- Keep legacy paths intact.
- Make data readiness, exports, and UI data prep DM-aware.

## Acceptance Criteria
- [ ] Audit and update all controller sites identified in the session audit.
- [ ] DM markets report readiness/coverage via DmCoverage + loader, not activities.count.
- [ ] No duplication or materialization triggered from controller paths for DM symbols.
- [ ] Tests or manual checks pass for both DM and legacy markets.
- [ ] Cross-link any new helpers back to the loader.

**Related:** DataSets UI is already mostly registry; focus on remaining actions and backtest result controllers.
