# Ticket: Harden Cromwell cron against post-truncation hallucination

**Status:** Proposed  
**Context:** Issue `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`. Session `docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`. Related open quality work: `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`.

## Problem

On 2026-07-13, `market-snapshot-hourly` called `wv2_market_snapshot` successfully, hit output truncation, then looped **8×** on `read_file({"path": "path/to/file.txt"})` and posted a human-facing ask for the path to Sawtooth Main. Job still marked completed.

Same day, later hourlies posted “stable market” with **no** MCP tool call.

Cron duty is not enforced: completion does not require the mandated tool, and identical failed tool calls are not circuit-broken.

## Acceptance criteria

- [ ] Circuit-break (or hard-stop) after N identical failed tool calls (same name + args) within one turn/job
- [ ] Cron turns that require MCP (e.g. market snapshot) either invoke the tool with a fresh call or **hard-fail** with a short ops error — never invent “stable / no movers”
- [ ] Cron/system turns must **not** ask the human for file paths or other free-form recovery
- [ ] Natural or forced `market-snapshot-hourly` posts non-placeholder content after a real `wv2_market_snapshot` call
- [ ] Cross-link result from parent issue when Done

## Implementation notes (non-binding)

Possible layers: nanobot agent loop guards; tighter cron prompts/skills; structured snapshot formatter that does not re-read free-form files; model upgrade if still required after guards.

## Related

- Issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md)
- Ticket: [`docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md)
- Ticket: [`docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`](2026-07-09-cromwell-cpu-only-llm-tuning.md)
- Session: [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
