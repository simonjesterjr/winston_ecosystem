# Ticket: Optional delete of predecessor TSMC parquet folder

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-19  
**Related:** session [`docs/session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md`](../session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md)

## Problem

After the TSMC → TSM storage remap, `/app/data/markets/TSMC/bars.parquet` was **kept** as a predecessor archive (same as RGI after RSPN). `ParquetLookbackLoader.data_ready?("TSMC")` is therefore still true if a caller passes that string. No Winston v2 Market is named TSMC, so Daily Analysis will not score it — leftover, not a live book.

## Scope

Optional cleanup after Wednesday’s unattended cycle is green on **TSM**:

1. Confirm no consumer Market / Book still has `trading_symbol=TSMC`.
2. Remove or park `data/markets/TSMC/` on the DM volume.
3. Reconcile so TSMC coverage is `no_parquet` / predecessor-only registry.
4. Spec or smoke: `data_ready?("TSMC")` false; `data_ready?("TSM")` still true.

## Acceptance

- [ ] No live TSMC Market in DM consumers (Wv2, WUT)
- [ ] TSMC parquet gone or explicitly archived off the consumer mount
- [ ] TSM path unchanged (latest session intact)
- [ ] `TickerRemap.canonical("TSMC")` still `TSM` (do not drop the alias)

## Non-goals

- Deleting DM registry row TSMC (keep `renamed_to TSM` like RGI)
- Remapping TWSE 2330
