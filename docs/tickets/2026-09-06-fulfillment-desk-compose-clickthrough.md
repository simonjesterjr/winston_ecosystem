# Ticket: Restart Wv2 and click through Fulfillment Desk v1

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Human gates:** none (read-only UI)  
**DoD:** Ops shell, Winston Quiver, Fulfillment Desk index/show, and one bound chip work on the local compose stack  
**Origin:** [`docs/session-reports/2026-09-06-2149-fulfillment-label-and-desk.md`](../session-reports/2026-09-06-2149-fulfillment-label-and-desk.md)  
**Depends:** code in `2026-09-06-wv2-fulfillment-label-and-desk.md` (implemented, not compose-restarted)

## Problem

Fulfillment Label + Desk v1 is specced in Winston v2 but was not compose-restarted or browser-checked. Routes and views need a process restart.

## Scope

1. Restart `winston_v2`.  
2. Ops shell: Active OPs and positions-by-band keep `paper`/`real`; bound OPs show the chip; dummy_sim has no extra chip; **All adapters** opens the index.  
3. Winston Quiver header + Tracking OP broker row use the chip, not raw `bnd_…`.  
4. Fulfillment Desk: index lists stored bindings + manual; IBKR page shows login/tickle rituals and per-OP Confirm vs Send.  
5. If the DUT session is dead, `needs login` on ops/WQ only — not as a DAR/Telegram attention ping.

## Non-goals

- Rebind  
- Editing labels in the UI (see binding-label ticket)

## Acceptance

- [ ] Compose restart  
- [ ] Click path: ops shell → chip → binding page → All adapters → WQ header chip  
- [ ] dummy_sim Active OP has no second chip  
