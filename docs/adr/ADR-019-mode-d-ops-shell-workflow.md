# ADR-019: Mode D Ops Shell workflow

**Status:** Proposed (production). The user-acceptance record in the business note is already in force for portfolio #1585.  
**Date:** 2026-09-25  
**Deciders:** Operator, this user-acceptance walk. Production items below are not accepted until the operator says so.  
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

## Proposed for production (not accepted)

- Auto-send of the GTC stop on every Mode D fill, versus the Walnut path (draft slate, Approve, then send).
- One symbol-level stop resized on each pyramid, versus one stop per lot.
- Re-introducing a spread or open-interest floor after the walk.
- Treating an IBKR cancel of a stop as a first-class journal transition (drop `working`, show naked, do not block the next confirm).

## Consequences

Phase 2 paper send and fingerprint adopt stay blocked on their own tickets. This walk has to finish before Mode D is treated as integrated. Resume: `docs/tickets/2026-09-25-mode-d-uat-resume.md`.
