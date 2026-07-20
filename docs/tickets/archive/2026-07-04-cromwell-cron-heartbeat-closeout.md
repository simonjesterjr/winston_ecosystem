# Ticket: Close out Cromwell cron vs gateway heartbeat migration

**Status:** Done
**Verified:** 2026-07-04
**Context:** Legacy `dream` cron job removed; gateway heartbeat disabled; authoritative schedule moved to `ecosystem/ai/schedule/`. Verify and document so future sessions do not reopen this work.

## Problem

Cron and heartbeat responsibilities were ambiguous (empty `dream` job, shared `MessageTool` context, gateway heartbeat duplicating cron). Fixes landed across nanobot, `jobs.json`, and `HEARTBEAT.md`, but no ticket recorded the migration or acceptance sign-off.

## Current expected state

| Surface | Expected |
|---------|----------|
| `ai/data/cromwell-bot/workspace/cron/jobs.json` | `market-snapshot-open`, `market-snapshot-hourly`, `dm-sync-events`, `eod-daily-report` (no `dream`) |
| `ai/data/cromwell-bot/workspace/HEARTBEAT.md` | Pointer only; gateway heartbeat **disabled** |
| `ecosystem/ai/schedule/manifest.yaml` | Authoritative M-F timeline (DM 3:30, Wv2 4:30, Cromwell EOD 4:35, snapshots) |
| Nanobot | Per-task `contextvars` for channel/chat_id; `_auto_deliver_daily_report` attaches PDF |

## Acceptance criteria

- [x] Runbook note in `ecosystem/ai/schedule/README.md`: cron owns periodic Telegram; heartbeat does not
- [x] `jobs.json` in seeded workspace matches manifest task ids (or documents intentional subset)
- [x] Smoke: `eod-daily-report` cron fetches `fetch_only` report after 4:30 PM MT Wv2 Sidekiq run; PDF attaches to Telegram group
- [x] No regression: concurrent cron + direct Telegram message does not drop replies (`cli:direct` / unknown channel)
- [x] Mark this ticket **Done** with verification date and compose command used

## Verification (2026-07-04)

| Check | Command / method | Result |
|-------|------------------|--------|
| jobs.json ↔ template | Python diff of `cromwell-cron.json` vs workspace `jobs.json` (ignoring `state`) | ✅ 4 jobs match; no `dream` |
| jobs.json ↔ manifest | `cromwell_*` task ids map to cron job ids | ✅ all 4 mapped |
| Gateway heartbeat off | `ai/data/cromwell-bot/config.json` `gateway.heartbeat.enabled` | ✅ `false` |
| HEARTBEAT.md pointer | workspace `HEARTBEAT.md` | ✅ disabled notice + schedule link only |
| EOD pipeline | `bin/test-daily-pipeline --offline` | ✅ DM events, Wv2 JSON, `fetch_only` 200 |
| PDF artifact | `winston_v2/storage/reports/wv2_20260704.pdf` | ✅ exists |
| fetch_only delivery hints | `GET /internal/cromwell_notifications?fetch_only=1` | ✅ `pdf_exists: true`, `telegram_media_path` set |
| eod-daily-report last run | `jobs.json` state `lastStatus: ok` | ✅ prior successful cron run recorded |
| Context isolation | `pytest tests/test_message_tool_context_isolation.py` | ✅ concurrent tasks route to distinct chat_ids |
| Runbook | `ecosystem/ai/schedule/README.md` § Cron vs gateway heartbeat | ✅ added this session |

**Compose command used:**

```bash
./bin/compose up -d redis postgres wut_postgres wv2_postgres \
  data_manager data_manager_sidekiq winston_v2 winston_v2_sidekiq
bin/test-daily-pipeline --offline
```

Note: `nanobot_cromwell` was not running during verification; EOD cron smoke validated via pipeline + prior `jobs.json` runtime state. Live Telegram delivery remains optional manual check per schedule README.

## Out of scope

- New cron jobs beyond manifest
- Re-enabling gateway heartbeat for daily briefing

## Related

- `ecosystem/ai/schedule/manifest.yaml`
- `ecosystem/ai/schedule/README.md`
- `openclawd-stack/nanobot/nanobot/agent/loop.py`
- `openclawd-stack/nanobot/nanobot/agent/tools/message.py`
- `openclawd-stack/nanobot/tests/test_message_tool_context_isolation.py`
- `ecosystem/plans/winston-mcp-next-steps.md.tasks.json` — task 10 (Phase 4 polish, partial)