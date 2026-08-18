# Ticket: Persist DM download_runs / download_tasks for after-close sync

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-18  
**Related:** session [`docs/session-reports/2026-08-18-1000-after-close-eod-session-contract.md`](../session-reports/2026-08-18-1000-after-close-eod-session-contract.md)

## Problem

Monday 2026-08-17 15:30 Mountain data_manager (DM) sync rewrote parquet (file mtimes 21:30 UTC) but `download_runs` and `download_tasks` in `data_manager_development` were **empty**. There is no durable run row for “what date window, which symbols, success/fail.”

`DownloadRun` / `DownloadTask` models and tables exist (`pending/running/completed/failed/partial`). `DailyDataOrchestratorJob` → `EcosystemDataSyncService` notifies Cromwell via JSONL but does not insert PG runs. `triggers#daily_downloads` is still a skeleton.

## Acceptance

- [ ] Each scheduled / orchestrated acquire writes a `DownloadRun` with `to` session date, symbol count, status
- [ ] Per-symbol `DownloadTask` (or equivalent) records latest bar date and errors
- [ ] Operator can answer “what did 15:30 MT pull?” from PG without reading container logs
- [ ] Existing Cromwell JSONL notifications keep working

## Related

- Issue: [`docs/issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md`](../issues/2026-08-18-dm-yesterday-window-misses-after-close-session.md)
- Code: `data_manager/app/models/download_run.rb`, `app/jobs/daily_data_orchestrator_job.rb`, `app/controllers/api/v1/triggers_controller.rb`
