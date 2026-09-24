# Ticket: Settle open Teal and Indigo USDU overdrafts

**Status:** Proposed
**Priority:** P1
**Date:** 2026-09-24
**Lane:** B (operator action; no sizing-code change)
**Implementer:** Operator
**DoD:** Teal portfolio 1584 and Indigo portfolio 1583 have free cash at or above zero, and neither book still carries the 22 September WisdomTree Bloomberg U.S. Dollar Bullish Fund (USDU) Plan C stock lot at the uncapped share count.
**Parent:** [`2026-09-22-min-atr-capital-consumption-guard.md`](2026-09-22-min-atr-capital-consumption-guard.md)
**Session:** [`../session-reports/2026-09-24-0854-capital-fit-usdu-guard.md`](../session-reports/2026-09-24-0854-capital-fit-usdu-guard.md)

## Goal

The Capital Fit gate is forward-only. These two paper lots were confirmed before it existed. Free cash on each book went negative. While it stays negative, a new long on that book is blocked. The operator flattens the lots or adds cash, on purpose, and checks the ledger.

## Context / specimens

| Book | Portfolio | Journal | Fill | Debit | Free cash after (autopsy) |
|------|-----------|---------|------|-------|---------------------------|
| Teal | 1584 | 2029 | 2,872 @ $26.65 | $76,538.80 | about −$47,648.80 |
| Indigo | 1583 | 2028 | 2,809 @ $26.65 | $74,859.85 | about −$38,576 |

Autopsy: [`../analysis/2026-09-22-wv2-dar-paper-trade-autopsy.md`](../analysis/2026-09-22-wv2-dar-paper-trade-autopsy.md).

Desk (Winston v2 on port 3002):

- Teal book: http://127.0.0.1:3002/operations/portfolios/1584
- Teal journals: http://127.0.0.1:3002/operations/portfolios/1584/journals
- Teal USDU journal: http://127.0.0.1:3002/operations/workflow?journal_id=2029
- Indigo book: http://127.0.0.1:3002/operations/portfolios/1583
- Indigo journals: http://127.0.0.1:3002/operations/portfolios/1583/journals
- Indigo USDU journal: http://127.0.0.1:3002/operations/workflow?journal_id=2028

## Work items

- [ ] Open each book and confirm the USDU lot is still open and free cash is still negative.
- [ ] Flatten the lot, or add cash, and write which choice on this ticket.
- [ ] After the ledger move, free cash on that book is ≥ 0.
- [ ] Do not describe the paper books as healthy until both books are checked.

## System One harness

**State:** Teal 1584 journal 2029 debit $76,538.80. Indigo 1583 journal 2028 debit $74,859.85. Capital Fit does not unconfirm executed journals.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| lots_still_open | Noul | The 22 September USDU stock lots are still the operator's problem, not a code bug | noul ≥ 0.7 |
| cash_non_negative | Noul | After the operator action, both books' free cash are ≥ 0 | noul ≥ 0.85 |

**Runner:** operator on the desk links above. No `jev ask` required for the flatten-vs-fund choice.
**On fail:** leave Proposed. Do not auto-flatten from an agent session.

## Non-goals

- Changing Capital Fit, Turtle unit math, or `max_leverage`.
- Rewriting historical Portfolio Backtest Run (PBR) results.
