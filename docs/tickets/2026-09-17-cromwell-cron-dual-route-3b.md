# Ticket: Dual-route Cromwell cron to 3b (sessionKey model routing)

**Status:** Proposed  
**Date:** 2026-09-17  
**Priority:** P3  
**Origin:** Wrap follow-up; staff roster Decision 9; L1 non-goal. Session `docs/session-reports/2026-09-17-1700-cromwell-llm-desk-and-daily-state.md`

## Problem

Live pin is `cromwell-qwen3:8b` for **all** nanobot turns (`agents.defaults.model`). Staff roster wanted `cron:*` → `cromwell-qwen2.5:3b` and interactive → 8b so hourlies do not hold the 8b lock. GPU makes 8b cheap, but `NANOBOT_MAX_CONCURRENT_REQUESTS=1` is still one slot — `dream` (~59s / 2h) and EOD still serialize against Telegram DMs.

Nanobot `config.json` has **no** per-`sessionKey` model field today. Routing is a real patch (same class as `cron_tool_allowlist.py`), not a one-liner.

## Scope

1. Patch nanobot (or config if a newer nanobot-ai supports it) so `sessionKey` `cron:*` uses 3b and default uses 8b.
2. Keep `think: false`; do not raise `OLLAMA_NUM_PARALLEL` in the same PR.
3. Update `ecosystem/ai/MODEL_PIN.md` + allowlist tests.
4. Thin existing hourlies remain preferred even after routing (template snapshot > 3b essay).

## Non-goals

- Five concurrent workers
- Changing live interactive pin away from 8b
- File-only Saturday staff cron (separate unbound-session patch)

## Related

- Staff roster: [`../../plans/cromwell-staff-roster.md`](../../plans/cromwell-staff-roster.md) §E / Decision 9
- Thin cron: [`2026-07-15-cromwell-thin-cron-and-priority.md`](2026-07-15-cromwell-thin-cron-and-priority.md)
- Promotion policy: [`2026-07-16-cromwell-core-model-promotion-policy.md`](2026-07-16-cromwell-core-model-promotion-policy.md)
- L1 (does not include this): [`2026-09-17-cromwell-daily-state-verifier.md`](2026-09-17-cromwell-daily-state-verifier.md)
- Pin: [`../../ai/MODEL_PIN.md`](../../ai/MODEL_PIN.md)
