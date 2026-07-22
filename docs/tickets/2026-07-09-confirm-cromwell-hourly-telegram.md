# Ticket: Confirm natural Cromwell hourly Telegram after CPU tuning

**Status:** Proposed  
**Priority:** P1
**Context:** Session `docs/session-reports/2026-07-09-1410-cromwell-cpu-tuning-and-watchdog.md` mitigated LLM timeouts (`cromwell-qwen2.5:3b`, 8k ctx, keep-alive 24h, `NANOBOT_MAX_CONCURRENT_REQUESTS=1`). Natural hourlies not yet confirmed green.

## Cluster (Cromwell hourly Telegram)

| # | Ticket / issue | Role |
|---|----------------|------|
| 1 | **This ticket** | Confirm hourlies fire with non-error content |
| 2 | [`2026-07-13-cromwell-scrub-placeholder-path-memory.md`](2026-07-13-cromwell-scrub-placeholder-path-memory.md) | Memory scrub |
| 3 | [`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md) | Real MCP + clean Telegram |
| 4 | [`2026-07-21-cromwell-hourly-telegram-attention-discipline.md`](2026-07-21-cromwell-hourly-telegram-attention-discipline.md) | Quiet = one line (attention) |

## Observation (2026-07-21)

- **Cadence reliability green** for full window: open 07:38 + hourlies 08–14 MT all completed (`cron/runs/`, `status: ok`). MCP invoked each slot.
- Principal sample ~10:21 was worst **content** (verbose quiet + menu); later slots still posted (12:11 empty-set waffle, 14:08 had a `testing` symbol buried in a dump).
- Content quality is **not** AC for this ticket — owned by observe + attention-discipline.
- **Post-seed natural sample armed:** 2026-07-22 07:30 MT open / 08:00 hourly after `seed --force-cron` + nanobot restart (2026-07-21 ~16:20 MT).
- **2026-07-22 morning:** open + hourlies through ≥11 MT **fired** with MCP; reliability remains green. Content still attention-fail (not this ticket’s AC). Open run artifact had empty `response` while logs show `message` tool sent a dump — note for observe/ops hygiene.

## Acceptance criteria

- [ ] At least one `market-snapshot-hourly` (or open) on Sawtooth Main posts **non-error** content  
- [ ] Prefer **two+** natural slots same session (cadence, not a single lucky fire)  
- [ ] Cron run artifact under `ai/data/cromwell-bot/workspace/cron/runs/` has useful response (not `timed out after 300s`)  
- [ ] Close or update `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md` when confirmed  
- [ ] Content quality (quiet one-liner vs mover radar) still owned by observe + attention-discipline tickets — this ticket is **delivery/reliability**

## Related

- `docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`  
- `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`  
- Issue (attention): [`docs/issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md`](../issues/2026-07-21-cromwell-hourly-verbose-quiet-attention-waste.md)  
