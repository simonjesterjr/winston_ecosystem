# Ticket: Archive Broker Gateway L1 Done tickets

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-17  
**Monolith:** ecosystem  
**Domain:** Docs hygiene  
**See:** [`2026-08-17-1315-leftover-dirty-trees.md`](../session-reports/2026-08-17-1315-leftover-dirty-trees.md) §4 Decision 3, §14; [`INDEX.md`](INDEX.md)

## Problem

`INDEX.md` says Done tickets move to `docs/tickets/archive/`. The 2026-08-09 Broker Gateway (BG) L1 store/API/interface tickets are **Done** (bodies closed when the Evidence Standard was accepted) but still sit in `docs/tickets/`. Operator left them in place during leftover cleanup.

## Scope

Move (at least) these three, then refresh INDEX:

- `2026-08-09-winston-broker-evidence-standard-interface.md`
- `2026-08-09-bg-evidence-store-jsonl-and-cursors.md`
- `2026-08-09-bg-internal-api-refresh-events.md`

Optional same pass: other INDEX rows already marked Done (equity parity, Turtle heat, importer 1%, dummy-sim, adapter registry) if the operator wants a hygiene sweep.

## Acceptance

- [ ] The three BG L1 files live under `docs/tickets/archive/`
- [ ] INDEX points at the archive paths (or drops the rows per local convention)
- [ ] No broken relative links from the L1 epic

## Related

- `ecosystem/interfaces/winston-broker-evidence-standard.md` (Accepted v0.1)
- Epic `2026-08-09-l1-confirmation-intake-bg-build.md`
