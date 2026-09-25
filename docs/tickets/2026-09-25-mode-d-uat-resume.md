# Ticket: Resume Mode D user acceptance early next week

**Status:** Proposed
**Priority:** P1
**Date:** 2026-09-25
**Lane:** A
**Implementer:** Grok CLI
**DoD:** The XLE flatten has filled, Winston is flat, and the Mode D walk has been started again from a fresh 120-share XLE long on the real desk. Full Mode D integration stays blocked until that walk finishes.
**Origin:** [session report](../session-reports/2026-09-25-1407-mode-d-uat-ops-shell.md)
**Parent:** [Mode D phase 2](2026-09-24-mode-d-phase-2.md)
**Rules:** [Ops Shell UAT](../business-context/mode-d-ops-shell-uat.md) · [ADR-019](../adr/ADR-019-mode-d-ops-shell-workflow.md)

## Grok Bot reminder

Tell the bot:

> Resume Mode D user acceptance. Read `ecosystem/docs/tickets/2026-09-25-mode-d-uat-resume.md` and `ecosystem/docs/session-reports/2026-09-25-1407-mode-d-uat-ops-shell.md`. Do not start full Mode D integration. First check whether IBKR paper order 946212659 (GTC limit sell 240 XLE at 61.00) has filled. If it has, book the print and close Winston lots 936 and 937. If it has not and the market is open, replace it with a market sell. When the account and Winston are both flat, put a fresh 120-share XLE long on the desk and walk it: Confirm the stock, let the GTC stop park, offer the covered call, pyramid to 3 lots, then a short with no call.

## Where it stopped (2026-09-25)

Paper account DUT070450, binding `bnd_3d6a5020d839c315583277d2`, Winston portfolio **#1585**.

- Call bought back. Order **946212656**. 1 XLE Oct 16 66 call at **0.60**. No short call left.
- Stock not flat. **240** XLE still long. Order **946212659** is a GTC limit sell of 240 at **61.00**, PreSubmitted, because the exchange was closed. A market sell was rejected for that reason.
- Winston still open: position **936** (120 at 61.81) and **937** (120 at 62.10). Working journal for the resting sell carries broker order **946212659**. No pending desk task. Book free cash about **$15,099.80**.
- Both earlier GTC stops (120 at 59.25, order 440801976, and 240 at 59.54) show Cancelled on the IBKR blotter. Winston no longer marks 440801976 working.

## First actions next session

1. Client Portal Gateway up and logged in at `https://localhost:5000` with the paper username.
2. Check order **946212659**. Book the fill if it traded. If it is still resting and the market is open, sell the 240 shares at the market and book that print.
3. Confirm Winston lots 936 and 937 are closed and the broker snapshot has no XLE stock and no XLE call.
4. Mint one fresh desk draft: 120 XLE, market, day, `source=mode_d_uat`, task type enter. Give the operator the workflow link. Do not send it.
5. Operator Confirms. On the print: GTC stop parks, covered-call draft appears (1 contract, opt-out). Then lot 2 and lot 3 the same way. Then one short, no call.

## Do not

- Treat this walk as finished Mode D integration.
- Send the fresh entry yourself.
- Use Microsoft. One round lot does not fit this account.
- Put a covered call on the entry line.
- Leave a cancelled broker stop marked `working` in Winston.
