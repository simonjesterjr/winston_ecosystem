# Ticket: WUT DM parquet: update documentation for DM as source of truth

**Status:** Proposed

**Date:** 2026-07-08

**Context:** After substantial code changes, WUT docs still describe the old activities + local parquet model in places.

See session report 2026-07-08-1130-wut-dm-parquet-audit-refactor.md.

## Problem
- `docs/parquet_data.md`
- `docs/data_reconciliation.md`
- `docs/architecture.md`
- Possibly TESTING_DATASET_LOADER.md and others
...still talk about syncing to activities, market.activities as the data source, etc.

## Goal
Update docs to:
- State that DM parquet (Winston EOD Standard via DmParquetLoader) is the primary source for DM-acquired symbols.
- Document the loader API, Bar struct, composite key usage, and when legacy paths apply.
- Note that Data Sets page is now a pure registry view.
- Remove or mark as legacy the old sync_to_activities and activities materialization paths for DM data.

## Acceptance Criteria
- [ ] Review and rewrite relevant sections in the listed docs.
- [ ] Add or update architecture diagrams / flow if present.
- [ ] Cross-reference `ecosystem/interfaces/winston-eod-parquet-standard.md` and the main plan.
- [ ] AGENTS.md and README notes updated if they mention data loading.

**Related:** Parent plan and CONTEXT.md glossary.
