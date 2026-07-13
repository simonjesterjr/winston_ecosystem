# Ticket: Fix Cromwell dream routing for MEMORY.md and skill status paths

**Status:** Proposed  
**Context:** Same morning as issue `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md` (secondary failure mode, not the Telegram symptom). Session `docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`.

## Problem

The `dream` consolidation job at ~09:12 MDT (15:12 UTC) attempted:

- `read_file("MEMORY.md")` — fails; truth is `memory/MEMORY.md`
- `read_file("skills/winston-ecosystem-status/ECOSYSTEM_STATUS.md")` — file does not exist (skill dir has `SKILL.md` only)

Dream prompt table already documents `memory/MEMORY.md`, but the model still used bare `MEMORY.md`. Consolidation then asked about “ecosystem operational status” instead of completing memory maintenance.

## Acceptance criteria

- [ ] Dream/consolidation reliably reads `memory/MEMORY.md` (or nanobot resolves the canonical path without agent guesswork)
- [ ] Dream does not invent skill status files that are not part of the skill contract
- [ ] One natural or forced dream cycle completes without false “file not found” for MEMORY
- [ ] Document any prompt/template change under `ecosystem/ai/` if applicable

## Related

- Issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md) (§ secondary dream failures)
- Runtime evidence: `ai/data/cromwell-bot/workspace/sessions/dream_20260713-151240.jsonl`
- Session: [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
