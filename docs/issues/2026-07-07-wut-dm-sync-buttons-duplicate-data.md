**Status:** Fixed (duplication paths eliminated; DM source of truth; see evidence)

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

This issue is now closed (see Manager note + Closure below; duplication paths removed + UI reflects principles; all ACs from related main ticket met).

**Cross-linked to:** the plan, main ticket (strong evidence), all 2026-07-08 sub-tickets (Completed), and 2026-07-08 session reports.

## Manager note + Closure (2026-07-08, post all clusters + restart)

**Strong evidence duplication paths eliminated (DM now source of truth for registry + consumption):**

- **UI/buttons:** Removed/replaced hydration. Now "Request DM refresh" only (acquire + DmRegistrySynchronizer metadata sync). See data_sets views (_market_row, index, show, _dm_discovery), controller (sync_from_dm, add_from_dm, update_all_data, create all call request_... only; no DataSetDmSyncJob / importer full). "Update All Data" now registry sync. (Delivered in 2026-07-08-1505-wut-dm-parquet-data-sets-ui.md; directly resolves this issue.)
- **Ingestion:** DataSetDmImporter: DM if/else: ONLY DmParquetIngester.ingest + comment "do NOT duplicate bars into local... or activities". No Pipeline.save_price/calculated, no sync_to_activities!. SyncRunner thin. (2026-07-08-1510 report)
- **Write guards everywhere:** backtest_activities_loader#sync_to_activities! returns early for DM (no Activity/MIV rows). data_downloader skips MIV/calc. All creation (BIV if id.nil?, PassedSignal, journals via bar_date) guarded.
- **Consumption/registry:** data_sets now reads from DmParquetLoader for show/export; stats/freshness from DmCoverage. All runners/ops/ER/views/models/controllers use loader + (market_id, date) or reader re-pull for DM. No .activities for DM.
- **Verification (deltas=0, no dup, re-pull):** 
  - Multiple live runs on real DM SPY parquet (1798+ bars): before/after Activity.count delta=0, MIV=0 on import/backtest/ER/ops/render paths (see 2026-07-08-1130 table, 0030 ER, 1500 views, 2330 core, 1510 services).
  - Spec: data_set_dm_importer_spec "DM source of truth (no duplication)" asserts 0 growth + not received Pipeline/sync.
  - Re-pull confirmed: views use reader market_key + DmParquetLoader; charts/tables show correct OHLCV/ATR from DM.
  - Local parquets untouched for DM; no new writes.
  - Post-restart 2026-07-08: invariants hold across all clusters (audit-refactor, views-repull, remaining, controller-cleanup, ER, data-sets-ui) + manager integration.
- Cross links: main ticket (2026-07-07-...) has full AC evidence + "Deltas: ACT=0, MIV=0"; sub-tickets e2e-smoke, miv-handling, model-cleanup, zero-delta-specs, docs-update all Completed with verifs; plan; 2026-07-08 session reports; Wv2 reference.

**UI now reflects principles:** Pure DM registry view (DataCoverage pointer). No misleading "load into WUT". DM is manager/source; WUT reads.

**Dupe paths for DM data removed:** Old bridge isolated to legacy non-DM. Issue root cause fully remediated.

**Recommend close:** Human re-smoke on running system (bin/compose up; visit /wut/data_sets; request refresh for SPY; run backtest; verify no activity growth + views render from DM) per "post human verification". All automated + report verifs passed.

**Related closed tickets:** See the 2026-07-08-* and main 2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md (strong evidence section).