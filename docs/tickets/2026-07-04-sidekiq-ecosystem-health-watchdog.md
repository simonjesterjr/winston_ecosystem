# Ticket: Sidekiq ecosystem health watchdog (Telegram alerts)

**Status:** Proposed
**Context:** `nanobot_cromwell` was not running during 2026-07-04 ops; Cromwell cron (including the 6 AM morning briefing) cannot fire when the gateway is down, and the briefing itself cannot authoritatively report container or DB health today.

## Problem

Periodic Telegram posts depend entirely on `nanobot_cromwell` + `winston_mcp` + LLM inference. When the Cromwell gateway is stopped or never started (`--profile ai` not brought up), there is **no independent signal** that core infrastructure is unhealthy.

The 6 AM `cromwell_ecosystem_status_daily` job uses MCP reachability probes only (Wv2, WUT, DM). It cannot see:

- `nanobot_cromwell`, `winston_mcp`, `ollama` container state
- `redis`, `postgres` / `wut_postgres` / `wv2_postgres` health
- Sidekiq worker liveness (`data_manager_sidekiq`, `winston_v2_sidekiq`, `winston_unit_test_sidekiq`)
- Backup completion (not implemented — see `operational-data-backup-dr` plan)

Operators discover outages only when expected messages fail to arrive.

## Proposed solution

Add a **deterministic Sidekiq cron job** (recommended owner: **Data Manager**) that runs independently of Cromwell:

| Aspect | Proposal |
|--------|----------|
| Job | `EcosystemHealthCheckJob` (or rake invoked by Sidekiq-Cron) |
| Schedule | **6:05 AM MT** daily (5 min after Cromwell narrative briefing) + optional **hourly degraded-only** ping |
| Checks | HTTP health on DM, Wv2, WUT, `winston_mcp` `/health`; compose-network DNS reachability; optional podman status via documented host script or socket mount (decision in implementation) |
| Alert path | Direct **Telegram Bot API** post (token from `ecosystem/deployment/` env — not committed); separate from Cromwell `message` tool |
| On failure | Immediate alert: which service failed, last successful check, suggested `./bin/compose` recovery command |
| On success | **Silent** on hourly; optional one-line "all green" on daily run, or defer to Cromwell briefing only |

## Acceptance criteria

- [ ] Sidekiq cron entry in `ecosystem/ai/schedule/sidekiq.yaml` + DM `config/sidekiq_schedule.yml`
- [ ] Job runs when `nanobot_cromwell` is **down** and delivers Telegram alert within one schedule tick
- [ ] Job detects Wv2/DM unreachable (simulate stop) and alerts with service name
- [ ] Telegram token loaded from env; no secrets in git
- [ ] Runbook section in `ecosystem/deployment/README.md` (troubleshooting + watchdog)
- [ ] Morning briefing skill updated to reference watchdog for authoritative infrastructure section once live

## Related follow-ups (same or child tickets)

| Item | Why |
|------|-----|
| `dm_get_cromwell_events` optional `date` param | 6 AM briefing needs **yesterday's** `symbol_updated` count for "Winston updated N markets from EODHD" — today's log-only API is insufficient |
| Backup status line | Wire in when `operational-data-backup-dr` Phase 2 lands (`bin/backup-sawtooth` manifest) |
| `ecosystem_health` MCP tool (optional) | Thin aggregator calling same probes for Cromwell narrative layer — not required if Sidekiq owns infra truth |

## Out of scope

- Re-enabling nanobot gateway heartbeat (contradicts cron migration — `docs/tickets/2026-07-04-cromwell-cron-heartbeat-closeout.md`)
- External SaaS monitoring (Uptime Kuma, etc.) — optional operator add-on, not this ticket

## Related

- `ecosystem/ai/skills/winston-ecosystem-status/SKILL.md` — morning briefing (narrative layer)
- `ecosystem/ai/schedule/manifest.yaml` — `cromwell_ecosystem_status_daily`
- `ecosystem/plans/winston-mcp-next-steps.md` — task 17
- `ecosystem/plans/operational-data-backup-dr.md` — backup status future
- `ecosystem/docs/tickets/2026-07-04-cromwell-cron-heartbeat-closeout.md` — cron owns periodic posts