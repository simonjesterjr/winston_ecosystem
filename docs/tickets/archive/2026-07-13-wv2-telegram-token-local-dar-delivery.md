# Ticket: Restore Telegram token for local DAR PDF delivery

**Status:** Done (2026-07-14 Phase 1)  

**Date:** 2026-07-13  

## Problem

`telegram_delivery` skipped with `missing_telegram_token` even when `ecosystem/deployment/watchdog.env` held the bot token.

## Root cause

`compose.yml` used Compose-spec map form:

```yaml
env_file:
  - path: ./ecosystem/deployment/watchdog.env
    required: false
```

**podman-compose** did not inject those vars into `winston_v2` / `winston_v2_sidekiq` (`TOKEN_LEN=0`).

## Fix

Use plain path form (same as DM `eodhd.env`):

```yaml
env_file:
  - ecosystem/deployment/watchdog.env
```

Recreate `winston_v2` + `winston_v2_sidekiq`. Verify:

- `ECOSYSTEM_WATCHDOG_TELEGRAM_TOKEN` non-empty  
- `WV2_TELEGRAM_CHAT_ID=-1003884714483`  

## Smoke (2026-07-14)

After re-eval 2026-07-11 for Blue PBR62:

```json
"telegram_delivery": {
  "delivered": true,
  "status": 200,
  "telegram_message_id": 329,
  "channel": "sawtooth_main",
  "chat_id": "-1003884714483"
}
```

## Acceptance

- [x] Env contract: token from `watchdog.env` via plain `env_file`; chat id via `WV2_TELEGRAM_CHAT_ID`  
- [x] Live smoke: Telegram PDF delivered to Sawtooth Main  
- [x] No secrets committed  

## Related

- `TelegramReportDelivery`  
- Six-cohort smoke / paper Phase 1  
