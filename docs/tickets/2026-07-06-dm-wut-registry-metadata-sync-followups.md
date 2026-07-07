# Ticket: DM ↔ WUT registry metadata mirror follow-ups

**Status:** Proposed

**Date:** 2026-07-06

**Context:** Follow-up work after implementing bulk DM registry sync (WUT Data Sets / Markets + DmCoverage now able to reflect all of DM's suitable + acquired symbols via `/api/v1/markets`). 

The core feature (one-touch full metadata sync, Sidekiq job, deploy-time boot enqueue, quick drift checks on Data Sets + Portfolio Builder pages, UI button, rake, proactive internal endpoint stub) was delivered in the session that produced the DM registry synchronizer.

This ticket captures the remaining polish, hardening, and cross-monolith improvements so the "WUT reflects current DM data sets" experience is complete and production-ready. The original discrepancy (WUT showing ~285 while DM had more for portfolio selection/correlation) is addressed by the mirror, but these items remain.

See implementation in:
- `winston_unit_test/app/services/dm_registry_synchronizer.rb`
- `winston_unit_test/app/jobs/dm_registry_sync_job.rb`
- Updates to `data_manager_client.rb`, `data_sets_controller.rb`, `portfolio_builder_controller.rb`, routes, views, rakes, initializers, `bin/setup`, and `docs/MARKET_CATALOG.md`
- New internal endpoint `POST /internal/dm/registry_update`

## Problem

Several follow-up items were identified during design/implementation to make the feature robust:

- No tests yet for the new synchronizer and job.
- Quick status check hits DM on every relevant page load (potentially chatty).
- No delta / incremental sync (always full list).
- Catalog and DM registry are not yet unified (catalog is WUT "blessed" subset; DM acquired is the broader pool from screener + suitability).
- No DM-side automation yet to proactively notify WUT of registry changes.
- Data Sets UI does not yet distinguish "sourced from DM registry" vs "from catalog" or "locally added".
- Deployment / boot experience and observability can be improved.
- Potential for use in correlation / universe selection flows (broader candidate pool).

## Goal

Complete the DM → WUT metadata mirror so that:
- WUT Data Sets (and consumers like Portfolio Builder, correlation) always have visibility into everything DM has acquired.
- Sync is efficient, observable, tested, and automatically kept fresh.
- Symbol metadata flows one way (DM → WUT); core data stays in DM only.
- UX surfaces drift and makes "one touch" obvious.

## Acceptance criteria

- [ ] Add RSpec tests for `DmRegistrySynchronizer` (sync_acquired!, quick_status, error paths) and `DmRegistrySyncJob` (broadcasting, error handling). Pattern after `spec/services/data_set_dm_*_spec.rb` and `market_catalog_spec.rb`.
- [ ] Make `quick_status` (and any page-load DM summary calls) lightly cached (e.g. Rails.cache or Redis with short TTL like 30-60s, or per-request memoization) to avoid hammering DM on every Data Sets / builder load.
- [ ] Implement (or document) a delta-only variant: only sync symbols where DM `latest` > local `DmCoverage.latest_date` (or new symbols). Expose via rake flag or param.
- [ ] Unify / bridge catalog and DM registry:
  - Option to (re)generate `market_catalog.json` (or a superset) from DM's suitable+acquired list.
  - Consider adding a `dm_sourced` or `registry_source` attribute / scope on Market or DmCoverage.
- [ ] DM-side call site for proactive notification:
  - After successful acquisition (in `EcosystemDataSyncService`, `MarketMetadataRecorder`, or post-`DataAcquisitionService`), POST to WUT's `/internal/dm/registry_update` (or the existing data_ready path).
  - Add minimal support in DM if needed (new notifier or extension of Cromwell notifications).
- [ ] UI/UX polish in Data Sets:
  - Indicate source (DM registry vs catalog vs manual) in the list, tabs, or rows (e.g. badge or filter).
  - Improve the drift banner (link directly to "Sync now" that triggers the job without page reload if possible).
  - Wire the same quick status + banner into the correlation calculator page.
- [ ] Boot / deploy / observability:
  - Make boot enqueue smarter (e.g. only if no recent full sync or if delta > threshold). Use a timestamp in metadata or a lightweight log.
  - Add logging / metrics around sync duration and counts.
  - Update relevant AGENTS.md, READMEs, or ecosystem docs with the new sync command as part of "after DM bulk downloads".
- [ ] Integration with correlation / portfolio selection:
  - Update `PortfolioCorrelationBuilder`, `UniverseDownloader`, or rakes to prefer / default to DM registry candidates when available.
  - Ensure `markets:ensure_data` and builder still work cleanly with the larger set.
- [ ] Smoke / verification:
  - End-to-end: with DM having extra symbols, run sync, confirm WUT Data Sets count increases and new symbols appear with DmCoverage data (without needing full parquet ingest for the listing itself).
  - Test with `bin/compose` restart + boot enqueue.

## Related

- `ecosystem/docs/business-context/winston-market-suitability.md` (DM suitability + acquired status)
- `ecosystem/interfaces/winston-eod-parquet-standard.md` and principles (metadata vs core data separation)
- `winston_unit_test/docs/MARKET_CATALOG.md`
- Previous implementation session (DM registry sync feature)
- `ecosystem/docs/tickets/2026-07-02-dm-integration-audit-mirror.md` (related DM integration patterns)
- `data_manager/app/controllers/api/v1/markets_controller.rb` (source of truth endpoint + summary)
- `winston_unit_test/app/services/dm_parquet_ingester.rb` (existing metadata ingest, now complemented by API mirror)

## Out of scope (for this ticket)

- Full time-series replication into WUT (explicitly forbidden by architecture).
- Changes to DM's core acquisition or suitability logic.
- Wv2 equivalent mirror (future, similar pattern expected).

## Suggested next steps / commands

```bash
# After changes
bin/compose restart winston_unit_test winston_unit_test_sidekiq data_manager data_manager_sidekiq
bin/compose exec winston_unit_test bin/rails dm:sync_dm_registry
```

Use the new "Sync All from DM (metadata)" button on the Data Sets page.
