# Ticket: WUT DM parquet: review and handle MarketIndicatorValue (MIV) paths for DM data

**Status:** Completed

**Date:** 2026-07-08

**Context:** ATR and other indicators are now baked into DM parquet. MIVs were the old mechanism for storing per-activity indicator values.

See the audit in session report 2026-07-08-1130 and the source-of-truth plan.

## Delivery Summary (2026-07-08)

Delivered by MIV worker (noted in main ticket consolidation update 2026-07-08) + integrated in 2026-07-08-1130-wut-dm-parquet-audit-refactor.md:
- Skips added/ensured in: data_downloader.rb (calculate_atr), lib/parquet_data/backtest_activities_loader.rb (sync_to_activities! early return), portfolio_signal_optimization_preflight.rb, indicator paths, preflight checks.
- BIV skip (related) in backtest_runner (if activity.id.nil?).
- Read paths: use Bar.atr / .extra (from DmParquetLoader) for DM; legacy MIV only in else.
- Inventory done via grep audit in 1130 report.

**Verified post-restart 2026-07-08:**
- DM paths: no MIV rows created (delta MIV=0 confirmed in main + 1130 verifs with SPY).
- ATR from loader: Bar.atr(period:17) returns baked atr_17; extra for others.
- Preflight/data_ready use DM loader (not MIV).
- Main ticket: "DM skip MIV creation in data_downloader/dataset_loader/backtest_activities_loader + preflight updated to DM loader; legacy isolated; delta=0 MIV confirmed."
- No uniqueness issues triggered (skips prevent insert for DM).

## Problem
- Some code paths still create or query MarketIndicatorValue rows (often tied to activities).
- In DM world this duplicates what is already in the parquet (atr_17 + many other columns).
- May cause confusion in stats, preflight checks, or legacy indicator code.

## Goal
- Audit all MIV creation and read sites.
- For DM symbols: skip MIV creation; read from loader Bar.extra or specific columns.
- Deprecate or isolate MIV usage for non-DM data.
- Update any preflight/ATR checks that rely on MIV.

## Acceptance Criteria
- [x] Inventory of MIV usage sites. (via 1130 audit + main consolidation)
- [x] DM paths no longer create MIVs. (early returns + guards)
- [x] Code that needs ATR or other indicators uses the loader (or Bar.atr) for DM markets. (Bar + extra)
- [x] Any related uniqueness/index or cleanup tasks identified. (none blocking; BIV uniqueness scope noted but skips prevent)

**Remaining follow-ups:** None for core; future indicator additions go to DM parquet standard + loader (per plan/ADR). Verified post-restart 2026-07-08.

**Related:** BacktestIndicatorValue handling (already skipped for DM in this work) and IndicatorCalculator.
