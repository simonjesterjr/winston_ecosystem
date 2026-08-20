# Ticket: Ecosystem health Telegram hints should match the failed probe

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-20  
**Monoliths:** data_manager (DM)  
**See:** [`docs/session-reports/2026-08-19-1505-dm-pending-migration-telegram.md`](../session-reports/2026-08-19-1505-dm-pending-migration-telegram.md)

## Problem

Hourly `EcosystemHealthCheckJob` posts Telegram only when a probe fails. The FAIL lines are accurate (`FAIL data_manager: unexpected status 500` + URL). The footer is not:

```text
Recovery hints:
  ./bin/compose ps
  ./bin/compose --profile ai up -d
  ./bin/compose --profile ai logs -f nanobot_cromwell ollama
```

Those three lines are hardcoded in `EcosystemHealthCheckService#format_message` (`data_manager/app/services/ecosystem_health_check_service.rb`). On 2026-08-19 the only failure was DM HTTP 500 from a pending migration. The footer pointed at Cromwell / Ollama, which were green.

Related prior note: [`docs/session-reports/2026-07-28-1544-winston-mcp-mcp-sdk-pin.md`](../session-reports/2026-07-28-1544-winston-mcp-mcp-sdk-pin.md) asked to include `winston_mcp` logs/rebuild in the same footer.

## Scope

1. Keep `./bin/compose ps` as a generic first hint.
2. Add probe-specific follow-ups from `result.failed` (e.g. DM → `compose logs data_manager` + `db:migrate`; MCP → rebuild/logs `winston_mcp`; nanobot/Ollama → `--profile ai` as today).
3. Spec: degraded message for a DM-only failure must not tell the operator to restart nanobot/Ollama.

## Acceptance

- [ ] Unit spec covers footer text for a DM-only failure vs an AI-layer failure
- [ ] Telegram degraded body still lists each failed probe name + URL
- [ ] Hourly remains silent when all probes pass

## Non-goals

- Changing probe URLs or accepted status codes
- Replacing the watchdog with Cromwell narrative status
