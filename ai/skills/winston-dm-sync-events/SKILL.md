---
name: winston-dm-sync-events
description: Relay Data Manager sync events to Sawtooth Main during the 3:30 PM MT download window.
---

# Winston DM Sync Events

Schedule: `ecosystem/ai/schedule/manifest.yaml` — poll during DM sync (after 3:30 PM MT Mon–Fri).

## MCP Tool

- `dm_get_cromwell_events` — optional `since` (ISO8601), `limit`

## Playbook

1. Call `dm_get_cromwell_events` once per cron invocation.
2. For each event in `events`, post **`event.message`** to Sawtooth Main (`telegram` / `-1003884714483`).
3. Track delivered `event.id` values — do not repost the same id in later polls the same day.
4. One Telegram line per event; no menus, no Runtime Context echo.

## Event types (examples)

- `sync_started` — "Data Manager started DailyDataOrchestratorJob"
- `consumer_sync_started` — "Data Manager has started market downloads for WUT"
- `symbol_updated` — "Data Manager has updated IBM for 6/24/2026"
- `sync_complete` — summary line

## Never Do

- Invent download status not in the tool response
- Post DM events outside the sync/delivery window unless the principal asks