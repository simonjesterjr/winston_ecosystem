# Ticket: Quarantine historical/demo DAR artifacts off the hot path

**Status:** Done  
**Context:** Issue [`docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md`](../issues/2026-07-20-historical-dar-morning-telegram-leak.md). Session [`docs/session-reports/2026-07-20-1031-historical-dar-telegram-guards.md`](../session-reports/2026-07-20-1031-historical-dar-telegram-guards.md).

## Problem

Demo/test Daily Activity Report artifacts remain under live paths, e.g.:

- `winston_v2/storage/cromwell_notifications/wv2_20231015.json`
- `winston_v2/storage/reports/wv2_20231015.{md,pdf}`
- related manifests / webhook copies

Cromwell has repeatedly re-discovered **2023-10-15** (and similar dates) as tool arguments. Production evaluate now rejects historical dates without `allow_historical`, but leaving demo packages next to real EODs still confuses humans and models.

## Acceptance criteria

- [x] Inventory non-production report dates under `storage/cromwell_notifications/` and `storage/reports/`
- [x] Move or archive demo/historical packages to a clearly named quarantine (e.g. `storage/reports/archive/demo/` or outside the agent-visible tree)
- [x] Document that test passes write under quarantine or require `allow_historical` **and** optional `deliver_telegram`
- [x] Confirm real EOD files (recent production dates) remain untouched
- [x] Optional: gitignore or backup policy note if quarantine is large/binary-heavy

## Implementation (2026-07-20)

Moved **demo/historical** packages only:

| Date | Destination |
|------|-------------|
| 2021-03-17 | `winston_v2/storage/archive/demo_dars/` |
| 2023-10-15 | same |
| 2025-06-14 | same |

Live EOD path (`storage/cromwell_notifications/wv2_202606*` / `wv2_202607*`) and recent reports left in place. Nanobot bind-mount of `storage/reports` no longer sees demo PDFs (`wv2_20231015.pdf` absent; `wv2_20260719.pdf` present). Webhook audit JSON under `ecosystem/logs/audit/webhook/` retained for forensics.
## Non-goals

- Deleting audit webhook history under `ecosystem/logs/audit/` (keep for forensics)
- Changing production EOD Sidekiq schedule

## Related

- Issue: [`../issues/2026-07-20-historical-dar-morning-telegram-leak.md`](../issues/2026-07-20-historical-dar-morning-telegram-leak.md)
- Guards: `winston_v2/app/services/daily_report_schedule.rb`
- Session: [`../session-reports/2026-07-20-1031-historical-dar-telegram-guards.md`](../session-reports/2026-07-20-1031-historical-dar-telegram-guards.md)
