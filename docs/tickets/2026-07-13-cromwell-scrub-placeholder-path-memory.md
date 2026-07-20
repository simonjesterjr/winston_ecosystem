# Ticket: Scrub Cromwell permanent memory of `path/to/file.txt` hallucination

**Status:** Proposed  
**Priority:** P1
**Context:** Issue `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`. Session `docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`.

## Problem

Idle-session compact wrote a permanent memory fact about a non-existent placeholder path:

- Runtime: `ai/data/cromwell-bot/workspace/memory/history.jsonl` cursor **61**  
  (`Error: File not found: path/to/file.txt - Tried different approaches but file not found.`)
- Session summary metadata on `telegram:-1003884714483` also captured the same text

This can bias later dream/consolidation turns.

## Acceptance criteria

- [ ] Remove or correct the permanent entry (cursor 61 and any compact summaries that restate it)
- [ ] Confirm `history.jsonl` / MEMORY-related artifacts no longer treat `path/to/file.txt` as a real ops failure
- [ ] Optional: one clean dream/consolidation cycle after scrub without reintroducing the fact

## Related

- Issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md)
- Session: [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
