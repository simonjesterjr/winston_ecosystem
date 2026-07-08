---
Status: Completed
---

# Ticket: Audit outside-UI callers (rakes, jobs, scripts) for legacy activities / duplication paths

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
The main DM-parquet source-of-truth plan and manager closeout list this as deferred/non-blocking:

> outside-UI callers (rakes/jobs) fully audited (importer guards them)

While core web paths, runners, and the new reconcile are on the DM loader + thin importer, there may still be rake tasks, background jobs, test scripts, or one-off scripts that still call `Pipeline.save`, `sync_to_activities!`, direct `Activity` creation, or local price/calculated writes for DM symbols.

## Acceptance Criteria
- [x] Inventory all rakes under `lib/tasks/` and any scripts in `lib/scripts/`, `bin/`, etc. that touch market data.
- [x] Audit jobs in `app/jobs/`.
- [x] For each, confirm they either:
  - Go through the DM branch / thin importer, or
  - Are explicitly legacy-only (FRED, Yahoo CSV paths, etc.) and guarded
- [x] Add guards or notes where missing.
- [x] Update the main ticket and plan with findings (or close the item if clean).

## Links
- Session report §6 / §14
- Main ticket: `2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md`
- Plan closeout section
- Importer guards and BacktestActivitiesLoader early returns

**Owner:** Worker 5 (2026-07-08 audit)  
**Due:** before declaring "no duplication paths remain" in production / scheduled jobs

---

## Audit results (2026-07-08)

### Inventory — jobs (`app/jobs/`)

| Caller | Market-data path | Verdict |
|--------|------------------|---------|
| `DataSetDmSyncJob` | `DataSetDmSyncRunner` → thin `DataSetDmImporter` | **Safe** (DM metadata only) |
| `DmRegistrySyncJob` | `DmRegistrySynchronizer` metadata upsert | **Safe** |
| `DailyOperationsJob` | `Operations::DailyTasksService` → `Operations::DataSync` (DM skip + legacy Yahoo) | **Safe** (already branched) |
| `RefreshPortfolioDataJob` | `DataDownloader.download_and_save` | **Fixed** — DM early return → thin importer |
| `DailyPaperTradingJob` | → `RefreshPortfolioDataJob` | **Safe** via fix above |
| `BacktestJob` | `BacktestRunner` (DM loader branch) | **Safe** |
| `PortfolioSignalOptimizationJob` | optimizer + context DM guards | **Safe** |
| `CalculateExpectedReturnJob` | DM bar re-pull / legacy activity | **Safe** (read path) |
| `PostBacktestExpectedReturnJob` | processor (read path) | **Safe** |
| `BroadcastBacktestUpdateJob` | Turbo only | N/A |
| `ActiveAccountsBackupJob` | JSON export of accounts/journals | N/A (no OHLCV write) |

### Inventory — rakes (`lib/tasks/`)

| Caller | Path | Verdict |
|--------|------|---------|
| `dm:*` (`dm_consume.rake`) | thin importer / registry / inspect / FRED reimport | **Safe** (FRED intentional local normalize) |
| `markets:ensure_data` / catalog | `MarketCatalog` → `DataSetDmImporter` | **Safe** |
| `universe:download` | `UniverseDownloader` → `DataSetDmImporter` | **Safe** |
| `paper_trading:refresh_data` / `:daily` | `DataDownloader` / `DailyPaperTradingJob` | **Fixed** via downloader guard + notes |
| `parquet:import_csv/append/export/calculate` | local WUT price/calculated | **Guarded** (abort on DM symbol; import_csv warns) |
| `parquet:delete_*` / `confirm_test` | cleanup / compare | **OK** (read/delete) |
| `datasets:load_csv` | `DatasetLoader` | **Fixed** — skips activity writes for DM symbols |
| `datasets:stats/export_*` | read/export | **OK** (stats still counts legacy activities; no write) |
| `portfolios:build_correlation` | `PortfolioCorrelationBuilder` → importer | **Safe** |
| `portfolios:vet_trend` | backtest runners (DM branch) | **Safe** |
| `markets:sync_etf_labels` | metadata labels only | **Safe** |
| strategy/config/seed/backup/db rakes | no market OHLCV writes | N/A |

### Inventory — scripts / bin

| Caller | Path | Verdict |
|--------|------|---------|
| `lib/scripts/download_datasets.rb` | Yahoo bulk | **Legacy annotated**; DM routed by downloader |
| `lib/scripts/regenerate_all_data_sets.rb` | Yahoo + CSV regen | **Legacy annotated**; DM routed by downloader |
| `lib/scripts/fill_nvda_gap.rb` | Yahoo gap fill | **Guarded** — aborts if NVDA DM-managed |
| `lib/scripts/test_atr_entry_prioritization.rb` | synthetic test Activities | **OK** (isolated TEST symbols) |
| `lib/scripts/fetch_leaps.py` | options history | **Legacy intentional** (options not DM EOD core) |
| `bin/*` | rails/rake/setup only | N/A |

### Code changes made
1. **`DataDownloader.download_and_save`** — central chokepoint: if `DmParquetPaths` or `dm_coverage`, call `DataSetDmImporter.import!(download: true)` and **never** write activities/MIV. Added `dm_managed_symbol?`.
2. **`BacktestActivitiesLoader.ensure_calculated_for_backtest!`** — no-op for DM (no local calculated parquet).
3. **`lib/tasks/parquet.rake`** — LEGACY labels + `ParquetRakeGuards.abort_if_dm_symbol!` on write tasks; import_csv warns on DM symbols.
4. **`DatasetLoader.load_from_csv`** — drops activity payloads for DM symbols (markets/books still OK).
5. **Jobs/rakes/scripts notes** — `RefreshPortfolioDataJob`, `paper_trading.rake`, `dataset_setup.rake`, legacy scripts headers.
6. **`fill_nvda_gap.rb`** — hard abort when DM-managed.

### Residual risk (low)
- **`parquet:import_csv`** still *can* write local `data/price_data` for symbols present in a bulk CSV even if DM-managed (warn only; no auto-delete). Manual rake, not scheduled.
- **FRED path** in `DataSetDmImporter` still writes local normalized price/calculated (intentional Option C).
- **`Pipeline.save_price/save_calculated`** remain callable from legacy/FRED code; not globally blocked (by design for FRED).
- **Options/LEAPs** still use Yahoo/`Activity` (out of DM EOD core scope).
- **New symbols with neither coverage nor DM parquet yet** still take Yahoo path in `download_and_save` until first DM acquire succeeds (expected bootstrap).
- Historical activity rows already in PG are not purged (per plan: non-blocking).

### Claim: "no duplication paths remain" for **scheduled jobs**?
**Yes, for scheduled/production jobs** after this audit:
- Daily ops DM branch skips Yahoo materialization.
- Paper refresh / `RefreshPortfolioDataJob` / `DataDownloader` no longer write activities for DM symbols.
- DM sync/registry jobs are metadata-only.
- Backtest/optimization jobs use DM loader branches; `sync_to_activities!` early-returns for DM.

Manual legacy rakes/scripts remain available but are labeled + guarded; they are not part of the scheduled job surface.

### Plan note
Main plan deferred item *"outside-UI callers (rakes/jobs) fully audited"* → **done** (this ticket). Update recorded in plan closeout section.