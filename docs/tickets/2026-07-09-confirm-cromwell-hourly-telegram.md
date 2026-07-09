# Ticket: Confirm natural Cromwell hourly Telegram after CPU tuning

**Status:** Proposed  
**Context:** Session `docs/session-reports/2026-07-09-1410-cromwell-cpu-tuning-and-watchdog.md` mitigated LLM timeouts (`cromwell-qwen2.5:3b`, 8k ctx, keep-alive 24h, `NANOBOT_MAX_CONCURRENT_REQUESTS=1`). Natural hourlies not yet confirmed green.

## Acceptance criteria

- [ ] At least one `market-snapshot-hourly` (or open) on Sawtooth Main posts **non-error** content  
- [ ] Cron run artifact under `ai/data/cromwell-bot/workspace/cron/runs/` has useful response (not `timed out after 300s`)  
- [ ] Close or update `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md` when confirmed  

## Related

- `docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`  
- `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`  
