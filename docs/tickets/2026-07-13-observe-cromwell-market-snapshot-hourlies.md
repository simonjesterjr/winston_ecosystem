# Ticket: Observe Cromwell market-snapshot hourlies for real MCP + clean Telegram

**Status:** Proposed  
**Context:** Issue `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`. Session `docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`. Overlaps acceptance on `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`.

## Problem

After the 09:00 MDT 2026-07-13 failure, 10:00 and 11:00 MT hourlies posted “no movers / stable” **without** logging a `wv2_market_snapshot` tool call. Need a short observation pass to establish current baseline (still broken vs intermittent).

## Acceptance criteria

- [ ] Capture at least **two** natural `market-snapshot-hourly` runs during NYSE session (or one forced + one natural)
- [ ] For each: note whether `mcp_winston_wv2_market_snapshot` (or equivalent) was invoked in `nanobot_cromwell` logs
- [ ] For each: note Telegram text quality (placeholder / invented stable / real brief from tool)
- [ ] Record findings on this ticket (or close as Done with summary linking issue)
- [ ] If still failing, point residual work at hardening ticket rather than re-investigating from scratch

## How to check

```bash
podman logs --since "…" nanobot_cromwell 2>&1 | grep -E "market-snapshot-hourly|wv2_market_snapshot|path/to/file|Response to telegram"
```

Session: `ai/data/cromwell-bot/workspace/sessions/telegram_-1003884714483.jsonl`

## Related

- Issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md)
- Hardening: [`docs/tickets/2026-07-13-cromwell-cron-hallucination-hardening.md`](2026-07-13-cromwell-cron-hallucination-hardening.md)
- Prior: [`docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md)
- Session: [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
