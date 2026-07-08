# Ticket: WUT DM parquet: review and handle MarketIndicatorValue (MIV) paths for DM data

**Status:** Proposed

**Date:** 2026-07-08

**Context:** ATR and other indicators are now baked into DM parquet. MIVs were the old mechanism for storing per-activity indicator values.

See the audit in session report 2026-07-08-1130 and the source-of-truth plan.

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
- [ ] Inventory of MIV usage sites.
- [ ] DM paths no longer create MIVs.
- [ ] Code that needs ATR or other indicators uses the loader (or Bar.atr) for DM markets.
- [ ] Any related uniqueness/index or cleanup tasks identified.

**Related:** BacktestIndicatorValue handling (already skipped for DM in this work) and IndicatorCalculator.
