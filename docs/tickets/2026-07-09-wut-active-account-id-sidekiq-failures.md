# Ticket: WUT Sidekiq jobs failing on missing active_account_id columns

**Status:** Proposed
**Priority:** P2
**Context:** Observed while diagnosing Cromwell Telegram silence (`docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md`). **Not** the cause of missing Telegram posts; filed so the WUT schema drift does not stay as log noise only.

## Problem

`winston_unit_test_sidekiq` is retry-failing jobs with:

```text
PG::UndefinedColumn: ERROR: column journals.active_account_id does not exist
PG::UndefinedColumn: ERROR: column positions.active_account_id does not exist
```

Affected jobs seen in logs:

- `ActiveAccountsBackupJob`
- `DailyOperationsJob` → `Operations::DailyTasksService`

Likely schema/code drift (code expects `active_account_id` after a rename or migration that did not run on this DB).

## Acceptance criteria

- [ ] Confirm intended schema for journals/positions (portfolio vs active_account naming) against WUT migrations and models
- [ ] Either run missing migration(s) or update services/jobs to the current column names
- [ ] `DailyOperationsJob` and `ActiveAccountsBackupJob` succeed on Sidekiq without retries
- [ ] Note in WUT session-report or AGENTS if this was a one-off local DB lag

## Out of scope

- Cromwell Telegram / nanobot cron (fixed separately)
- Wv2 schema

## Related

- `docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md` §6 Deferred
- Monolith: `winston_unit_test/` (`DailyOperationsJob`, `ActiveAccountsBackupJob`)
