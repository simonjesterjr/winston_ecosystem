# Ticket: Cromwell market-snapshot-open — empty run `response` vs Telegram `message`

**Status:** Proposed  
**Priority:** P2  
**Context:** Session `docs/session-reports/2026-07-22-1144-cromwell-hourly-attention-principle.md`. Cluster observe/confirm hourlies.

## Problem

On **2026-07-22 ~07:30–07:42 MT**, `market-snapshot-open` completed with:

- Cron run artifact `ai/data/cromwell-bot/workspace/cron/runs/market-snapshot-open_1784727000002_ff60b48a.json`: `status: ok`, **`response` empty**
- `podman logs nanobot_cromwell`: successful `mcp_winston_wv2_market_snapshot({})` then **`message` tool** posted a multi-symbol dump to Telegram

Observers that only read `response` (including the overnight watcher) treat the duty as empty or “attention-ok,” while Sawtooth Main may still have received content. Artifact hygiene and confirmation ACs are unreliable.

## Acceptance criteria

- [ ] Document when nanobot writes final text to `response` vs only via `message` tool on cron turns
- [ ] Either: (a) always mirror delivered Telegram text into run `response`, or (b) teach observe scripts to also parse session JSONL / `message` tool calls
- [ ] Re-check one natural `market-snapshot-open` run: artifact reflects what Telegram got
- [ ] Cross-link from observe ticket once verified

## Related

- Observe: [`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md)
- Confirm: [`2026-07-09-confirm-cromwell-hourly-telegram.md`](2026-07-09-confirm-cromwell-hourly-telegram.md)
- Session: [`docs/session-reports/2026-07-22-1144-cromwell-hourly-attention-principle.md`](../session-reports/2026-07-22-1144-cromwell-hourly-attention-principle.md)
