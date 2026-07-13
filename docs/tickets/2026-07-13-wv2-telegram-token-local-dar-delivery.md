# Ticket: Restore Telegram token for local DAR PDF delivery

**Status:** Proposed  

**Date:** 2026-07-13  

**Context:** Six-cohort evaluate smoke (`docs/tickets/2026-07-12-wv2-six-cohort-evaluate-smoke.md`, session `docs/session-reports/2026-07-12-1828-six-cohort-evaluate-smoke.md`). Evaluate for 2026-07-12 wrote MD/PDF and delivered webhook to MCP, but Telegram was skipped.

## Problem

`telegram_delivery` on the daily-complete notification:

```json
{
  "delivered": false,
  "skipped": true,
  "reason": "missing_telegram_token",
  "channel": "sawtooth_main"
}
```

Local/compose ops do not get the DAR PDF on **Sawtooth Main** until the bot token is present (or delivery is intentionally disabled). Webhook + on-disk package still work.

## Scope

1. Confirm which env var(s) Wv2 expects for Telegram (`TELEGRAM_BOT_TOKEN` / `WV2_TELEGRAM_*` — check `TelegramReportDelivery` and compose `env_file`).  
2. Document where the token should live for this host (compose env, secrets, not git).  
3. Either restore token for smoke/ops delivery **or** document `WV2_TELEGRAM_DELIVER=0` as intentional local default.  
4. Re-run evaluate (or report-only path) and confirm `telegram_delivery.delivered: true` when desired.

## Out of scope

- Changing Sawtooth Main chat id policy  
- Cromwell Telegram agent reply UX (separate tickets)

## Acceptance

- [ ] Env contract documented (required vars + where they are set on this host)  
- [ ] Either: live smoke shows Telegram PDF delivery, **or** explicit opt-out documented as default  
- [ ] No secrets committed to git  

## Related

- Smoke: `docs/tickets/2026-07-12-wv2-six-cohort-evaluate-smoke.md`  
- Report delivery skill: `ecosystem/ai/skills/winston-report-delivery/SKILL.md`  
- Older Telegram tickets: `2026-07-09-confirm-cromwell-hourly-telegram.md`, `2026-07-09-telegram-agent-reply-visibility.md`  
