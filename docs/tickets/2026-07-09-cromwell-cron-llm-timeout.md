# Ticket: Harden Cromwell cron LLM path (timeouts on scheduled Telegram)

**Status:** Proposed
**Context:** Session `docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md` fixed unbound cron skips; smoke still hit `LLM request timed out` (2m) on `cromwell-qwen3.5:4b` CPU during a bound `market-snapshot-open` run.

## Problem

Session-bound cron jobs now enter the agent loop, but a full tool-bearing turn against the 4b model on CPU can exceed nanobot’s LLM timeout. Ollama logged `POST /v1/chat/completions` → 500 after 2m0s. If this continues, Telegram posts can still fail even though the scheduler is healthy.

## Acceptance criteria

- [ ] Observe at least one natural cron (hourly / DM relay / EOD) end-to-end on Sawtooth Main
- [ ] If timeouts recur: either (a) switch cron-facing model to a proven tool-calling size (e.g. 8b) or (b) raise LLM timeout for gateway/cron turns
- [ ] Document chosen model + timeout in `ai/configs/nanobot-cromwell.example.json` and schedule README if changed
- [ ] Confirm MCP tools still invoked successfully on a timed-out-prone path (snapshot or EOD fetch_only)

## Out of scope

- Reopening session-binding / SSRF whitelist work (done 2026-07-09)
- Replacing nanobot with another gateway

## Related

- `docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md`
- `ecosystem/ai/schedule/README.md` (§ Nanobot 0.2.x session binding)
- Runtime: `ai/data/cromwell-bot/config.json` model `cromwell-qwen3.5:4b`
