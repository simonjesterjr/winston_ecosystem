# Ticket: Harden Cromwell cron LLM path (timeouts on scheduled Telegram)

**Status:** In progress (mitigations landed 2026-07-09; await natural hourly)  
**Context:** Session `docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md` fixed unbound cron skips. Hardware diagnosis: pure CPU is correct. Mitigations: CPU-only model/ctx/keep-alive + Sidekiq watchdog.

## Problem

Tool-bearing cron turns on `cromwell-qwen3.5:4b` + 16k ctx exceeded Ollama ~2 m and nanobot 300 s → Telegram error posts.

## Mitigations applied (same day)

- Model → `cromwell-qwen2.5:3b` (`num_ctx` 8192, `num_predict` 512)
- `OLLAMA_KEEP_ALIVE=24h`, flash attention, parallel=1
- Ops note: avoid backtests at top-of-hour MT
- Independent health watchdog (DM Sidekiq) so LLM death is not silent

## Acceptance criteria

- [ ] Observe at least one natural cron (hourly / DM relay / EOD) end-to-end on Sawtooth Main with **non-error** content  
- [x] Document chosen model + `num_ctx` in example config / README  
- [ ] Confirm MCP tools still invoked successfully on live snapshot path (after next natural tick or manual Telegram prompt)

## Related

- **`docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`**  
- **`docs/tickets/2026-07-04-sidekiq-ecosystem-health-watchdog.md`**  
- Runtime model: `cromwell-qwen2.5:3b`  
