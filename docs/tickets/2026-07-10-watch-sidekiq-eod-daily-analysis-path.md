# Ticket: Watch Sidekiq EOD path (DM sync → Wv2 analysis → Cromwell)

**Status:** Proposed  
**Priority:** unset
**Date:** 2026-07-10  
**Context:** Session [`2026-07-09-1655-wv2-strategy-registry-daily-smoke`](../session-reports/2026-07-09-1655-wv2-strategy-registry-daily-smoke.md). Manual `DailyAnalysisJob.perform_now` works; scheduled multi-day paper cadence not verified this session. Compose often shows Sidekiq services as health **starting**.

## Problem

Paper daily reports depend on the scheduled path, not only manual evaluate:

- DM ~3:30 PM MT data orchestration  
- Wv2 `DailyAnalysisJob` ~4:30 PM MT  
- Cromwell EOD delivery ~4:35 PM MT (`fetch_only`)

If workers are unhealthy or jobs never fire, Red stays silent even when signals would exist.

## Scope

1. Confirm `data_manager_sidekiq`, `winston_v2_sidekiq` are processing (logs / Sidekiq web / job history).
2. Next trading day after 4:30 PM MT: check `storage/cromwell_notifications/wv2_YYYYMMDD.json` and PDF for Active portfolios.
3. If missing: root-cause schedule vs worker vs analysis gate (`DailyReportSchedule`).
4. Cross-check plan tasks 11/14 and health-watchdog ticket.

## Acceptance

- One unattended EOD cycle produces notification + PDF for Active set
- Document any schedule/env gaps found

## Related

- `plans/winston-mcp-next-steps.md.tasks.json` tasks 11, 14, 17
- `docs/tickets/2026-07-04-sidekiq-ecosystem-health-watchdog.md`
- `winston_v2/app/services/daily_report_schedule.rb`
- Session: `2026-07-09-1655-wv2-strategy-registry-daily-smoke.md`
