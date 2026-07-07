# Ticket: data_sets UI — DM as source of truth; pure registry view using DataCoverage; remove all "Load Full Data", "Sync", hydration actions and language; columns reflect DM metadata

**Status:** Proposed (see main ticket)

**Date:** 2026-07-07

**Context:** The /wut/data_sets page (and related in portfolio builder) currently mixes local activity stats with DM coverage. Buttons labeled "Load full data from DM" (when activity_count==0) vs "Sync" are the same code path (DataSetDmSyncJob → DataSetDmImporter → full materialization + local copies). This contradicts "all data managed in DM".

See main ticket (`ecosystem/plans/wut-dm-parquet-source-of-truth.md`) and plan for details. Related: registry metadata ticket.

## Problem

Users see and click buttons that appear to "load into WUT" (and do, duplicatively). Table shows "Activities" count that may be 0 even when DM has the data (or shows DM dates with (DM) tag only in some places). Freshness, "Update All Data", export etc. not DM-centric.

## Goal

data_sets (index, rows, show, discovery) is a pure registry view of what DM has made available (via DataCoverage). No UI language or actions that suggest or perform bulk data copy into WUT. All data truth from DM.

## Acceptance Criteria

- [ ] No hydration buttons or language at all ("Load full...", "Sync", "Update All Data" that materializes). Actions limited to "Request DM refresh" (trigger + metadata ingest) or view.
- [ ] All columns, counts, ranges, freshness, indicators from DataCoverage (converge naming). "(DM)" and indicators_present prominent.
- [ ] Discovery and forms are request-only (no implied local load).
- [ ] Show page and related use coverage metadata; never materializes activities for DM markets.
- [ ] Consistent with main plan: pure DM registry; no suggestion of data living in WUT.

## Related

- Main WUT DM source-of-truth ticket
- 2026-07-06-dm-wut-registry... followups (UI polish items overlap)
- winston_unit_test/app/views/data_sets/* , data_sets_controller.rb , DataSetFreshness, merge_dm_display_stats

**Implementation only after main plan verified.**
