# Ticket: Re-seed Cromwell workspace snapshot skill

**Status:** Proposed
**Priority:** P3
**Date:** 2026-08-13
**Monoliths:** ecosystem (`ai/skills`), Cromwell runtime (`ai/data/cromwell-bot/workspace`)
**See:** [`docs/session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md`](../session-reports/2026-08-13-1248-hourly-snapshot-shuffle-movers.md)

## Problem

SOT skill `ecosystem/ai/skills/winston-market-snapshot/SKILL.md` now documents shuffle + 3-mover payload. The live nanobot copy was **hand-edited** at `ai/data/cromwell-bot/workspace/skills/winston-market-snapshot/SKILL.md` so the next hourly would not contradict the tool.

`bin/seed-cromwell-workspace` was **not** run. A later seed from an uncommitted or stale SOT, or a force-cron seed, could drift.

## Scope

1. After the ecosystem skill commit is on `main`: `bin/seed-cromwell-workspace` (force-cron only if cron prompt should refresh too).
2. Diff live skill vs `ecosystem/ai/skills/winston-market-snapshot/SKILL.md` — shuffle / 3-mover lines present.
3. Restart `nanobot_cromwell` only if seed does not pick up without it.

## Acceptance

- [ ] Live workspace skill matches ecosystem SOT on shuffle + 3-mover contract
- [ ] Note in this ticket which seed command ran

## Non-goals

- Changing cron job JSON beyond what seed already writes
- MCP image rebuild (separate ticket)
