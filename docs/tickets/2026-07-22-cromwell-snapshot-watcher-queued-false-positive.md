# Ticket: Fix market-snapshot overnight watcher — race on `queued` / empty response

**Status:** Proposed  
**Priority:** P3  
**Context:** Session `docs/session-reports/2026-07-22-1144-cromwell-hourly-attention-principle.md`. Script (gitignored): `ecosystem/logs/watch-market-snapshot-next.py`.

## Problem

Durable watcher armed 2026-07-21 for next natural open/hourly:

1. Captured run files as soon as they appeared with `status: queued` and **empty `response`**
2. Scored `attention_ok_heuristic=True` because short/empty text looked “quiet”
3. Exited at 08:00 MT before hourlies finished writing real Telegram text

False green misleads observe/attention ACs. Session background tasks also hit a **10h max runtime** before open (use nohup/host process, not session-bound bash).

## Acceptance criteria

- [ ] Wait until `status == ok` (or terminal fail) **and** either non-empty `response` or confirmed `message` delivery path (see empty-response ticket)
- [ ] Do not score attention until text is final; empty ≠ all-quiet success
- [ ] Optional: poll up to N minutes after fire time; log path + preview + true attention flags
- [ ] Prefer durable host path under `ecosystem/logs/` (gitignored) with clear README note, or promote a small ops script under `ecosystem/docs/operations/` if reused

## Related

- Empty response hygiene: [`2026-07-22-cromwell-snapshot-open-empty-response-artifact.md`](2026-07-22-cromwell-snapshot-open-empty-response-artifact.md)
- Observe: [`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md)
- Session: [`docs/session-reports/2026-07-22-1144-cromwell-hourly-attention-principle.md`](../session-reports/2026-07-22-1144-cromwell-hourly-attention-principle.md)
