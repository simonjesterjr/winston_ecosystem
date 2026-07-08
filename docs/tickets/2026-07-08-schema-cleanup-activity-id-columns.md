---
Status: Proposed
---

# Ticket: Eventual schema cleanup for activity_id columns (post DM SoT)

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
The plan closeout lists this as deferred:

> full schema cleanup for activity_id columns

After the DM cutover, `activity_id` is optional on Position, Journal, TradingSignal, BacktestIndicatorValue, PassedSignal, etc. `MarketIndicatorValue` was left stricter. Many tables still carry the column and indexes.

We do not want to drop historical data or break legacy non-DM paths immediately, but we should have a plan for:

- Making columns nullable where they aren't yet
- Dropping unused indexes
- Eventually removing the columns (or keeping them only for a "legacy" source flag)
- Updating any remaining non-null constraints, unique indexes, and model validations

## Acceptance Criteria
- [ ] Inventory all tables/columns/indexes that still reference `activity_id` (or `belongs_to :activity`).
- [ ] Decide on migration strategy (one big migration vs phased, with or without `source` column on results).
- [ ] Produce a migration + rollback plan (or multiple).
- [ ] Update models, factories, and specs accordingly.
- [ ] Document the cutover date / conditions under which legacy activity rows can be purged (if ever).

## Links
- Plan: `ecosystem/plans/wut-dm-parquet-source-of-truth.md` (open items)
- Main ticket and cluster tickets
- Current schema + the relax migration (20260707150000_relax_activity_fks...)

**Owner:** follow plan (non-blocking for now)  
**Due:** when we are ready to drop the last legacy activity paths or do a major schema cleanup release