---
Status: Proposed
---

# Ticket: Audit outside-UI callers (rakes, jobs, scripts) for legacy activities / duplication paths

**Related to:** ecosystem/docs/session-reports/2026-07-08-1430-dm-reconcile-container-cleanup.md

## Context
The main DM-parquet source-of-truth plan and manager closeout list this as deferred/non-blocking:

> outside-UI callers (rakes/jobs) fully audited (importer guards them)

While core web paths, runners, and the new reconcile are on the DM loader + thin importer, there may still be rake tasks, background jobs, test scripts, or one-off scripts that still call `Pipeline.save`, `sync_to_activities!`, direct `Activity` creation, or local price/calculated writes for DM symbols.

## Acceptance Criteria
- [ ] Inventory all rakes under `lib/tasks/` and any scripts in `lib/scripts/`, `bin/`, etc. that touch market data.
- [ ] Audit jobs in `app/jobs/`.
- [ ] For each, confirm they either:
  - Go through the DM branch / thin importer, or
  - Are explicitly legacy-only (FRED, Yahoo CSV paths, etc.) and guarded
- [ ] Add guards or notes where missing.
- [ ] Update the main ticket and plan with findings (or close the item if clean).

## Links
- Session report §6 / §14
- Main ticket: `2026-07-07-wut-dm-parquet-source-of-truth-no-duplication.md`
- Plan closeout section
- Importer guards and BacktestActivitiesLoader early returns

**Owner:** follow plan  
**Due:** before declaring "no duplication paths remain" in production / scheduled jobs