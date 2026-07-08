---
Status: Proposed
---

# Ticket: Complete zero-delta specs for DM reconcile path

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
The main WUT DM-parquet ticket and plan closeout note that zero-delta specs were partially advanced (importer_spec has a DM branch asserting no activity growth). Full coverage for the new `ReconciliationService`, `data:reconcile` rake, and related paths is still needed.

## Acceptance Criteria
- [ ] Add/expand specs that assert:
  - After `reconcile_all` / `reconcile_symbol` on DM symbols: 0 new `activities` rows, 0 new `market_indicator_values`
  - `DataCoverage` is updated from actual parquet (min/max date, bar_count, indicators_present)
  - `SymbolRegistryEntry.dm_data_status` set to "acquired" (with `list_source` default)
  - No local price/calculated parquet writes for DM symbols
  - Error paths (bad parquet, missing columns) are handled without crashing the run
- [ ] Cover the rake tasks (`data:reconcile`, `data:reconcile_symbol`)
- [ ] Ensure specs run cleanly against the current 600+ parquet corpus (or a representative subset)
- [ ] Update the zero-delta-specs ticket and main plan ticket with progress

## Links
- Main ticket: `2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md`
- Session report: `ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md`
- ReconciliationService: `data_manager/app/services/reconciliation_service.rb`
- Existing importer zero-delta work: see 2026-07-08-wut-dm-parquet-zero-delta-specs.md

**Owner:** follow existing ticket  
**Due:** before declaring the DM SoT effort fully tested in CI