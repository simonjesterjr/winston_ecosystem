# ADR-019: Mode D Ops Shell workflow

**Status:** Accepted 2026-09-25 for the four production rules below. The walk on #1585 is still unfinished.  
**Date:** 2026-09-25  
**Deciders:** Operator, after the user-acceptance walk.  
**Builds on:** ADR-009, ADR-013  
**Domain context:** `docs/business-context/mode-d-ops-shell-uat.md`  
**Glossary:** `CONTEXT.md` — Mode D

## Context

Mode D phase 2 started as an unbound Winston-only desk walk, then a portfolio-list field, then assignment replace, then one paper send. The walk showed that writing journals is not the test. The test is the same Ops Shell desk the operator already uses: a stock order, a broker print, a protective stop, and a covered-call choice, on an account that can hold the shares.

## Decision (user acceptance only)

For Copper **#1585** until this walk is finished:

1. Desk confirm is the send. There is no second Winston-only page.
2. Stock entry first. Covered call after the print, opt-in, `floor(shares/100)` contracts, never on a short.
3. The GTC protective stop is parked when the stock print books. A filled call does not satisfy that stop.
4. Naked on the ops shell means no working stop at the broker. A parked stop is not a pending action. A covered-call task is labeled **Mode D Option Workflow**.
5. Mode C open-interest and 8% spread screens do not apply to this walk's covered-call read.

## Production rules (operator, 2026-09-25)

1. **No 8% spread gate on Mode D.** The open-interest floor stays off Mode D as well. Mode C and any other mode that inherited the 200-contract / 8% screens need a design session. Those screens were not an operator lock.
2. **Day orders return to the nightly Session Order Slate** (Approve, then send). A position with no working protective stop is never acceptable. Selling a covered call stays a human confirm, because not every long is written.
3. **Pyramid stops stay on the Trading Strategy.** Copper’s strategy is #341 TurtleV1 S1 Breakout20/10, `stop_strategy=move_to_last_entry`. When a lot is added, earlier lots in that name take the new lot’s stop. The user-acceptance hour made one broker ticket for the whole stack look like a special rule. It is the existing move-to-last-entry behavior.
4. **Winston matches the broker.** If Interactive Brokers cancels or fills a working order, the journal leaves `working`. A stop that is gone at the broker is a naked lot, and the shell must show that so the operator can act at the broker. A filled call is not evidence that the stop was cancelled, and it does not clear the naked flag.

## Consequences

Phase 2 paper send and fingerprint adopt stay blocked on their own tickets. This walk has to finish before Mode D is treated as integrated. Resume: `docs/tickets/2026-09-25-mode-d-uat-resume.md`.
