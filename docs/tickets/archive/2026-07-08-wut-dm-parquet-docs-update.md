# Ticket: WUT DM parquet: update documentation for DM as source of truth

**Status:** Completed

**Date:** 2026-07-08

**Context:** After substantial code changes, WUT docs still describe the old activities + local parquet model in places.

See session report 2026-07-08-1130-wut-dm-parquet-audit-refactor.md.

## Delivery Summary (2026-07-08)

Delivered by docs work in audit-refactor + remaining + manager consolidation:
- `winston_unit_test/docs/parquet_data.md`: new "Backtest data source (DM source of truth)" section + "DataSet and parquet" registry note. Details DmParquetLoader, Bar, result identity + re-pull, no sync/dupe for DM, cross-refs to plan + reader.
- `winston_unit_test/docs/data_reconciliation.md`: updated intro: "**DM is the single source of truth** (shared Winston EOD Standard parquet + DmCoverage metadata). WUT consumers read via DmParquetLoader (no duplication). ... Data sets should not be duplicated..."
- architecture.md (operations flow) and TESTING* largely untouched (no conflicting DM language; architecture.md focuses on ops not data source); legacy diagram remains as ops view.
- AGENTS.md (WUT): no direct data loading prose requiring change at time of audit (ref ecosystem first).
- Cross-refs added in code comments + tickets to `ecosystem/interfaces/winston-eod-parquet-standard.md` and plan.

**Verified post-restart 2026-07-08:** Docs now state DM loader primary for DM symbols; registry view; legacy isolated. Changes reflected in actual files (grep confirmed DM source language present). See linked docs in WUT.

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
- [x] Review and rewrite relevant sections in the listed docs. (parquet_data.md + data_reconciliation.md rewritten with DM primary + loader + registry + re-pull; links to plan)
- [ ] Add or update architecture diagrams / flow if present. (no change needed in ops-focused architecture.md; diagrams in business-context/adr cover)
- [x] Cross-reference `ecosystem/interfaces/winston-eod-parquet-standard.md` and the main plan. (in updated docs + code comments)
- [x] AGENTS.md and README notes updated if they mention data loading. (no direct updates required; ecosystem/AGENTS and CONTEXT take precedence per rules; WUT docs now align)

**Remaining follow-ups:** If ops architecture mermaid should evolve for DM data flow, open separate; current state reflects delivered changes. Verified post-restart 2026-07-08.

**Related:** Parent plan and CONTEXT.md glossary.
