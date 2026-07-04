# Winston / Cromwell Schedule (single source of truth)

This directory is the **authoritative catalog** of recurring tasks across the Sawtooth ecosystem. Runtime copies are derived from here; they are not edited by hand in production workspaces.

## How the pieces work together

| Layer | Where it runs | Role |
|-------|---------------|------|
| **Sidekiq** (DM, Wv2, WUT) | Rails workers in compose | Deterministic backend: EODHD fetch, parquet, analysis, report files |
| **Cromwell cron** (nanobot) | `workspace/cron/jobs.json` | Telegram delivery and narrative only — reads artifacts, does not re-run analysis |
| **Skills** | `ecosystem/ai/skills/` | Playbooks linked from manifest by `skills:` — **no duplicate cron times** |
| **HEARTBEAT.md** | Cromwell workspace | Pointer to this directory; heartbeat gateway stays **disabled** |

### Cron vs gateway heartbeat

**Cromwell cron owns all periodic Telegram posts** (DM relay, EOD report, market snapshots). The nanobot gateway heartbeat (`gateway.heartbeat.enabled`) stays **false** — do not re-enable it for Sawtooth Main broadcasts. `HEARTBEAT.md` is a pointer to this directory only; it must not duplicate cron job definitions. When adding a new recurring Telegram task, edit `manifest.yaml` + `cromwell-cron.json`, then `bin/seed-cromwell-workspace --force-cron`.

```text
M-F (America/Denver):
  3:30 PM  DM Sidekiq     → EODHD sync for all WUT+Wv2 portfolio symbols (+ Cromwell event log)
  3:35/3:45 PM Cromwell cron → relay DM events via dm_get_cromwell_events
  4:30 PM  Wv2 Sidekiq    → DailyAnalysisJob → JSON + PDF on disk
  4:35 PM  Cromwell cron  → fetch_only report + Telegram (+ PDF)

NYSE session (7:30 AM–2:00 PM MT ≈ 9:30 AM–4:00 PM Eastern):
  7:30 AM  Cromwell cron  → market snapshot (open)
  8–14:00  Cromwell cron  → hourly market snapshot (hourly on the hour)

Saturday 8:00 AM MT:
  DM Sidekiq → weekend parquet refresh (same symbol union as dm:sync)

WUT 6:00 AM (optional):
  DailyOperationsJob → Winston Operations UI only (not Cromwell/Telegram)
```

## Files in this directory

| File | Purpose |
|------|---------|
| [`manifest.yaml`](manifest.yaml) | Human-readable task catalog: id, owner, cron, tz, dependencies, skills, MCP tools |
| [`cromwell-cron.json`](cromwell-cron.json) | Template for nanobot `workspace/cron/jobs.json` |
| [`sidekiq.yaml`](sidekiq.yaml) | Mirror of monolith `config/sidekiq_schedule.yml` entries — keep in sync when changing crons |

## Deploying Cromwell cron

```bash
bin/seed-cromwell-workspace              # merge cron template (preserves lastRun state)
bin/seed-cromwell-workspace --force-cron # overwrite job definitions from template
./bin/compose --profile ai restart nanobot_cromwell
```

## Deploying Sidekiq schedules

Sidekiq cron is loaded from each monolith's `config/sidekiq_schedule.yml` when the **Sidekiq worker** starts. After editing `sidekiq.yaml` here, apply the same entries to the monolith YAML and restart the worker:

```bash
./bin/compose up -d data_manager_sidekiq winston_v2_sidekiq winston_unit_test_sidekiq
./bin/compose restart data_manager_sidekiq winston_v2_sidekiq
```

## Time zones

All cron expressions use **`America/Denver` (Mountain Time)**. NYSE cash session maps to **7:30 AM–2:00 PM MT** (9:30 AM–4:00 PM Eastern). Denver observes DST, so this offset stays correct year-round.

## EOD handoff rule

Cromwell EOD cron must use `fetch_only: true` on `wv2_get_daily_activity_report`. Wv2 Sidekiq at 4:30 PM MT must have already written `storage/cromwell_notifications/wv2_YYYYMMDD.json`. If the file is missing, Cromwell reports `report_not_ready` — it does **not** trigger a second analysis run.

## Testing procedure

Use these checks to validate the M-F pipeline **without waiting for cron clocks or Telegram**. Cromwell/Telegram delivery is optional manual verification at the end.

### Manual data pull (all active markets)

When cron has not fired, or you want yesterday's EOD immediately:

```bash
# Preferred — discovers WUT + Wv2 symbols and pulls from EODHD
./bin/compose exec -T data_manager bin/rails dm:sync

# Same path the 3:30 PM cron job uses
./bin/compose exec -T data_manager bin/rails runner \
  'DailyDataOrchestratorJob.perform_now'

# Then run Wv2 analysis (what 4:30 PM cron does)
./bin/compose exec -T winston_v2 bin/rails runner \
  'DailyAnalysisJob.perform_now'
```

Requires `EODHD_API_KEY` in `ecosystem/deployment/eodhd.env` and consumers reachable (`winston_unit_test`, `winston_v2` up).

### Prerequisites

Core stack running (rebuild Sidekiq images after Gemfile changes):

```bash
./bin/compose up -d --build --force-recreate \
  redis postgres wut_postgres wv2_postgres \
  data_manager data_manager_sidekiq \
  winston_unit_test winston_v2 winston_v2_sidekiq
```

Verify Sidekiq cron loaded without scheduler errors:

```bash
podman logs --tail 20 data_manager_sidekiq   # should NOT show connection_pool ArgumentError
./bin/compose exec -T data_manager bin/rails runner \
  'puts Sidekiq::Cron::Job.all.map { |j| "#{j.name} #{j.cron}" }'
```

For live EODHD sync: `EODHD_API_KEY` set in `ecosystem/deployment/eodhd.env` and DM container recreated after edits.

After changing DM code: `./bin/compose build data_manager && ./bin/compose up -d --no-deps data_manager data_manager_sidekiq`

### Automated integration test (recommended)

From the repo root:

```bash
# Fast path — stub DM Cromwell events, no EODHD network calls
bin/test-daily-pipeline --offline

# Full path — real dm:sync-style download for all WUT+Wv2 symbols
bin/test-daily-pipeline
```

**What `bin/test-daily-pipeline` verifies:**

| Step | Check |
|------|--------|
| DM | Cromwell event log has ≥3 events (`dm_events_YYYYMMDD.jsonl`) |
| Wv2 | `DailyAnalysisJob.perform_now` writes `winston_v2/storage/cromwell_notifications/wv2_YYYYMMDD.json` |
| Wv2 | `GET /internal/cromwell_notifications?fetch_only=1` returns **200** when the report exists |
| DM | `GET /internal/cromwell_notifications` returns **200** |

Exit code **0** = all checks passed; **1** = at least one failure.

### Manual inspection (optional)

**DM sync events** (after offline stub or live sync):

```bash
curl -s http://127.0.0.1:3001/internal/cromwell_notifications | jq '.events[].message'
# or inside container:
./bin/compose exec -T data_manager bin/rails runner \
  'DmCromwellNotifier.events_since(limit: 20).each { |e| puts e["message"] }'
```

**Wv2 report artifact:**

```bash
cat winston_v2/storage/cromwell_notifications/wv2_$(date +%Y%m%d).json | jq '.summary'
```

**Offline stub only** (no pipeline script):

```bash
./bin/compose exec -T data_manager bin/rails dm:test_notifications
```

### Cromwell / Telegram (optional, not required for pipeline test)

After seeding cron and rebuilding MCP + bot:

```bash
bin/seed-cromwell-workspace --force-cron
./bin/compose --profile ai build winston_mcp nanobot_cromwell
./bin/compose --profile ai up -d --no-deps winston_mcp nanobot_cromwell
```

Confirm MCP exposes `dm_get_cromwell_events` and that scheduled jobs in `workspace/cron/jobs.json` match [`cromwell-cron.json`](cromwell-cron.json). Telegram posts are validated by watching Sawtooth Main during the sync window (3:35/3:45 PM MT) and EOD (4:35 PM MT).

## Planned (not yet scheduled)

- Weekend correlation analysis jobs (WUT `MarketCorrelationCalculator`)
- Intraday ATR breach filtering for snapshots (requires EODHD delayed/live quotes — see `winston-market-snapshot` skill Phase D)