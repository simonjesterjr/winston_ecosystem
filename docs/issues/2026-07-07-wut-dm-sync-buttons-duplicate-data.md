**Status:** Open

# Issue: WUT "Load Full Data from DM" and "Sync" buttons duplicate data from DM into local WUT storage and activities table

**Date:** 2026-07-07

**Observed at:** http://localhost:3000/wut/data_sets

## Summary

The UI buttons labeled "Load full data from DM" (when no local activities) and "Sync" (otherwise) on the Data Sets page, plus "Update All Data", appear to be "syncing from DM" but in fact cause WUT to copy the full time-series data (OHLCV + indicators) from DM's parquet into:

- WUT-local parquet files (`data/price_data/*.parquet`, `data/calculated/*.parquet`)
- The `activities` table (full rows)
- `market_indicator_values` (ATRs)

This directly contradicts the established architecture: **DM is the manager and source of truth for market data**; parquets are made available to other systems (WUT, Wv2) via shared volume; consumers must not duplicate the heavy time-series data. PG in consumers holds only metadata (DmCoverage as pointer).

## Root Cause (verified in code)

- View logic: `winston_unit_test/app/views/data_sets/_market_row.html.erb:38`
  ```erb
  <% needs_full_data = stats[:activity_count].to_i == 0 %>
  ...
  <%= needs_full_data ? "Load full data from DM" : "Sync" %>
  ```
  Both call the same `sync_from_dm_data_set_path` → `DataSetsController#sync_from_dm` → queues `DataSetDmSyncJob`.

- Runner: `app/services/data_set_dm_sync_runner.rb`
  ```ruby
  result = DataSetDmImporter.import!(@symbol, download: false)
  ```

- Importer: `app/services/data_set_dm_importer.rb:59`
  ```ruby
  DmParquetIngester.ingest(symbol)
  ParquetData::Pipeline.new(rows: price_rows).save_price(symbol).save_calculated(symbol)
  ...
  ParquetData::BacktestActivitiesLoader.sync_to_activities!(market)
  ```

- `sync_to_activities!` (lib/parquet_data/backtest_activities_loader.rb) does `Activity.find_or_initialize_by(...)` + save + MIV rows for every bar.

- Same path used by "Download", add_from_dm, update_all_data, market_catalog, universe_downloader, correlation builder, rakes, etc.

- `DmParquetIngester` has the correct comment ("We do NOT replicate...") but is only used for metadata. The "sync" UX path bypasses it for full copy.

- Data sets freshness and stats sometimes show DM coverage when activities==0 ("DM Synced"), but the action still hydrates the copy.

## Why This Matters

Per `ecosystem/principles/02_data_storage_and_reconciliation.md` and `CONTEXT.md`:
- "The parquet files in the shared volume are the source of truth"
- "No heavy OHLCV or indicator time-series rows in PG tables"
- Wv2 correctly implements this (no Activity table, direct ParquetLookbackLoader + ParquetBar from /dm_data, missing_data skips).
- WUT is the "mature reference" but has this transitional duplication bridge that is now being treated as permanent by the UI.

The buttons mislead the user into thinking data stays in DM.

## Related Artifacts

- Plan: `ecosystem/plans/wut-dm-parquet-source-of-truth.md`
- Tickets:
  - `ecosystem/docs/tickets/2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md`
  - `ecosystem/docs/tickets/2026-07-07-wut-dm-data-sets-ui-dm-truth-no-load-sync-buttons.md`
  - `ecosystem/docs/tickets/2026-07-07-wut-activities-compatibility-shim-dm-stubs.md`
- Adversary review performed on the plan (verdict: BROKEN on shim details; corrections noted in plan).
- Wv2 reference implementation: `winston_v2/app/services/parquet_lookback_loader.rb`, `parquet_bar.rb`, `dm_parquet_ingester.rb`, `operations/portfolio_readiness.rb`
- Key WUT files: `data_set_dm_importer.rb`, `backtest_activities_loader.rb`, `data_sets_controller.rb`, `dm_parquet_ingester.rb` (metadata path only)

## Next Steps

See the plan for the full remediation (make DM parquet primary, provide compatibility for `market.activities` expressions via loaders + sparse stubs or refactor, overhaul data_sets UI to be DM-metadata only, remove hydration from sync paths, add missing_data-style readiness).

This issue should be closed when the duplication paths for DM data are removed and the UI reflects the principles.

**Cross-linked to the plan and tickets above.**