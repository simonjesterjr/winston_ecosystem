# Ticket: DAR Telegram force re-publish runbook

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-24  
**Domain:** Wv2 Daily Activity Report, Telegram Sawtooth Main, ops runbooks  
**Monoliths / runtime:** `winston_v2`, `ecosystem/docs/operations/`  
**See:**  
[`2026-07-24-1705-dar-telegram-redeploy.md`](../session-reports/2026-07-24-1705-dar-telegram-redeploy.md),  
[`2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md`](2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md),  
[`../operations/README.md`](../operations/README.md)

## Problem

When Cromwell hangs on interactive “publish the DAR” (empty LLM response), operators still need a **deterministic, documented** way to re-post the existing PDF to Sawtooth Main **without** re-running Daily Analysis or waiting on the bot.

Tonight (2026-07-24) this was done ad hoc via `rails runner` + `TelegramReportDelivery.deliver!` and succeeded (msg **496**). That recipe should live under `ecosystem/docs/operations/` so the next hang is a copy-paste, not a rediscovery session.

## Desired outcome

Add a short ops runbook (e.g. `ecosystem/docs/operations/dar-telegram-force-republish.md`) that covers:

1. **Preconditions** — report date; artifacts exist  
   - `storage/cromwell_notifications/wv2_YYYYMMDD.json`  
   - `storage/reports/wv2_YYYYMMDD.pdf`  
2. **Check prior delivery** — read `telegram_delivery` in the notification JSON (message id / delivered flag).  
3. **Force re-push** — preferred command (compose-safe):

```bash
bin/compose exec -T winston_v2 bundle exec rails runner '
date = Date.parse(ENV.fetch("DAR_DATE", Date.current.iso8601))
path = Rails.root.join("storage/cromwell_notifications/wv2_#{date.strftime("%Y%m%d")}.json")
raise "missing #{path}" unless File.exist?(path)
payload = JSON.parse(File.read(path))
result = TelegramReportDelivery.deliver!(payload, date: date)
puts result.inspect
if result[:delivered]
  payload["telegram_delivery"] = result
  payload["telegram_redelivered_at"] = Time.now.utc.iso8601
  File.write(path, JSON.pretty_generate(payload))
end
'
# optional: DAR_DATE=2026-07-24 bin/compose exec -T winston_v2 env DAR_DATE=2026-07-24 ...
```

4. **Env notes** — token fallbacks in `TelegramReportDelivery` (`WV2_TELEGRAM_BOT_TOKEN` / `ECOSYSTEM_WATCHDOG_TELEGRAM_TOKEN`); chat defaults to Sawtooth Main `-1003884714483`.  
5. **Do not** re-run `DailyAnalysisJob` solely to “send the PDF” if artifacts already exist.  
6. **Link** from Cromwell empty-response ticket “operator escape hatch” section and from `winston-report-delivery` skill if useful.

## Acceptance

- [ ] Runbook file under `ecosystem/docs/operations/` with the force re-push command  
- [ ] Linked from `docs/operations/README.md`  
- [ ] Cross-linked from empty-response fastpath ticket escape-hatch section  
- [ ] Dry-run verified once against a known `wv2_YYYYMMDD.pdf` (or noted as verified 2026-07-24)

## Non-goals

- Fixing Cromwell empty-response (owned by P1 fastpath ticket)  
- Changing production-date Telegram guards (`DailyReportSchedule`)  
- Committing `storage/cromwell_notifications/*.json` runtime state  

## Evidence

- 2026-07-24 redelivery: `delivered: true`, `telegram_message_id: 496`, chat `-1003884714483`  
- Session report: [`2026-07-24-1705-dar-telegram-redeploy.md`](../session-reports/2026-07-24-1705-dar-telegram-redeploy.md)  
