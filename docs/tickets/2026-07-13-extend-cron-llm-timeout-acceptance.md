# Ticket: Extend Jul 9 cron LLM timeout ticket with post-truncation acceptance

**Status:** Proposed  
**Priority:** unset
**Context:** Issue `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md` and new hardening ticket `docs/tickets/2026-07-13-cromwell-cron-hallucination-hardening.md`. Parent open ticket: `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`.

## Problem

`2026-07-09-cromwell-cron-llm-timeout` acceptance still focuses on timeouts / non-error content. The 2026-07-13 incident shows a **different** failure mode: truncation recovery → placeholder tool loops → fake completion without MCP on later ticks. Quality criteria for “natural cron OK” should explicitly cover both.

This ticket is **bookkeeping / criteria alignment**, not the implementation work (that lives in the hardening ticket).

## Acceptance criteria

- [ ] Update `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md` Related + acceptance to cite the 2026-07-13 issue and require:
  - no placeholder-path / “provide the correct file path” posts on cron
  - required MCP tool present on market-snapshot turns (or documented hard-fail)
- [ ] Cross-link hardening ticket and observe-hourlies ticket so owners do not duplicate investigation
- [ ] Leave status of Jul 9 ticket accurate (In progress until criteria met)

## Related

- Parent: [`docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md)
- Hardening: [`docs/tickets/2026-07-13-cromwell-cron-hallucination-hardening.md`](2026-07-13-cromwell-cron-hallucination-hardening.md)
- Observe: [`docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md)
- Issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md)
- Session: [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
