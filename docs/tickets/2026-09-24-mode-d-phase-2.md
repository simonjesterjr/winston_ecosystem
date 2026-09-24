# Ticket: Mode D phase 2 — desk walk, bot visibility, paper send, assignment replace

**Status:** Proposed
**Priority:** P1
**Date:** 2026-09-24
**Lane:** A
**Implementer:** Grok CLI
**DoD:** The four child tickets below are done in this order, on one Mode D book, with no order sent before the desk walk has been clicked through.
**Origin:** [session report](../session-reports/2026-09-24-1227-mode-d-phase-0-1.md)
**Children:**

1. [Desk walk](2026-09-24-mode-d-phase-2-desk-walk.md)
2. [Portfolio list emits fulfillment mode](2026-09-24-mode-d-phase-2-portfolio-list-mode.md)
3. [Assignment replace on the same desk](2026-09-24-mode-d-phase-2-assignment-replace.md)
4. [One paper send after the book is named](2026-09-24-mode-d-phase-2-paper-send.md)

## Goal

Finish Mode D as one phase. Phases 0 and 1 already land the mode flag, the stock packaging, the unbound test-desk service, and the Daily Analysis covered-call tasks. Phase 2 makes that visible and operable: a person can click the walk, Grok Bot can see which books are Mode D, the desk can replace shares after assignment without selling a new call, and only then does one covered call go to Interactive Brokers (IBKR) paper.

## Order

Do not start the paper send until the desk walk and the portfolio-list field are in. Assignment replace is part of this phase, exercised on the unbound desk with an assumed snapshot, not deferred to a later program.

## Non-goals

- Changing Plan A / Plan B / Plan C or `LeapCandidates` furthest-month selection
- Putting Mode D on an existing Mode C book (Blue, Mango, Orange, Indigo, and the rest)
- Agent Desk Send
- A new `leap_fulfillment` value

## System One harness

**State:** child ticket results; portfolio id; `fulfillment_mode`; whether any `place_order` ran.

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| still_phase_2 | Noul | Did this work ship a paper send or an assignment path before the clickable desk walk existed? | noul ≥ 0.85 → FAIL |
| bot_can_see | Noul | Does `GET /internal/portfolios` omit `fulfillment_mode` after this phase is marked done? | noul ≥ 0.85 → FAIL |

**Runner:** `jev ask` on the phase wrap state.
**On fail:** do not mark the parent Done.
