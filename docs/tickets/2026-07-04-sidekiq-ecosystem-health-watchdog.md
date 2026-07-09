# Ticket: Sidekiq ecosystem health watchdog (Telegram alerts)

**Status:** Done (2026-07-09 implement pass)  
**Context:** `nanobot_cromwell` was not running during 2026-07-04 ops; Cromwell cron cannot fire when the gateway is down. Implemented independent DM Sidekiq probes + Telegram Bot API.

## Problem

Periodic Telegram posts depend entirely on `nanobot_cromwell` + `winston_mcp` + LLM inference. When the Cromwell gateway is stopped, there is **no independent signal**.

## Implementation

| Piece | Location |
|-------|----------|
| Service | `data_manager/app/services/ecosystem_health_check_service.rb` |
| Job | `data_manager/app/jobs/ecosystem_health_check_job.rb` |
| Specs | `data_manager/spec/services/ecosystem_health_check_service_spec.rb` (5 examples) |
| Sidekiq cron | `data_manager/config/sidekiq_schedule.yml` — hourly `:10`, daily `6:05` MT |
| Catalog | `ecosystem/ai/schedule/{sidekiq.yaml,manifest.yaml}` |
| Secrets template | `ecosystem/deployment/watchdog-env-template.txt` → `watchdog.env` (gitignored) |
| Compose | `data_manager_sidekiq` env: probe URLs + `env_file: watchdog.env` |
| Nanobot bind | `gateway.host: 0.0.0.0` so `/health` is reachable on compose network |
| Runbook | `ecosystem/deployment/README.md` § Ecosystem health watchdog |

### Behaviour

- **Hourly:** Telegram only when any probe fails  
- **Daily 6:05 AM MT:** always post green/red  
- Probes: DM, WUT, Wv2, MCP `/health`, Ollama `/`, nanobot `/health`

### Smoke (2026-07-09)

```text
EcosystemHealthCheckJob.perform_now("daily")
=> {:ok=>true, :failed=>[], :notify=>{:ok=>true, :code=>200}}
```

## Acceptance criteria

- [x] Sidekiq cron entry in `ecosystem/ai/schedule/sidekiq.yaml` + DM `config/sidekiq_schedule.yml`
- [x] Job can run and alert when stack is up (daily smoke → Telegram 200)
- [x] Telegram token from env; no secrets in git (`watchdog.env` gitignored)
- [x] Runbook in `ecosystem/deployment/README.md`
- [ ] Morning briefing skill one-liner pointing at watchdog as authoritative infra (optional polish)
- [ ] Simulated “stop nanobot → hourly alert” not re-run in this session (code path covered by unit tests)

## Related follow-ups

| Item | Why |
|------|-----|
| `dm_get_cromwell_events` optional `date` param | 6 AM briefing yesterday’s symbol count |
| Backup status line | When `operational-data-backup-dr` lands |

## Out of scope

- Re-enabling nanobot gateway heartbeat  
- External SaaS monitoring  

## Related

- `ecosystem/ai/skills/winston-ecosystem-status/SKILL.md`  
- `docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`  
