# Ticket: Mode D phase 2 — assignment replace on the desk walk

**Status:** Proposed
**Priority:** P1
**Date:** 2026-09-24
**Lane:** A
**Parent:** [Mode D phase 2](2026-09-24-mode-d-phase-2.md)
**Implementer:** Grok CLI
**DoD:** The same unbound desk walk can assume an assignment snapshot. If Trend Following (TF) has not exited, it mints a stock-only replace. If TF has exited, it does not. The call is not resold on the replace.
**Origin:** [session report](../session-reports/2026-09-24-1227-mode-d-phase-0-1.md)

## Goal

Assignment is part of Phase 2, not a later program. The unbound desk does not wait for a live Interactive Brokers (IBKR) exercise. The operator (or the spec) supplies a snapshot: shares gone, short call gone, fill at the strike.

Rules already locked:

- Book the fact only from that snapshot. Do not invent a fill.
- If the same session also has a TF exit or stop, do not rebuy.
- If the trend has not exited, keep the lot in the pyramid count with broker shares at zero and mint a human task to buy the shares back.
- That task is stock only. The five-session attach clock restarts on the replacement fill.
- While replace is required, do not pyramid and do not sell a call.

## Work items

- [ ] Snapshot input on `Operations::ModeD::TestDesk` (and the desk page from the walk ticket)
- [ ] Replace task is stock only
- [ ] Spec: trend still on → replace, no call; TF exit the same day → no replace
- [ ] Attach clock reset asserted on the replacement fill

## System One harness

**State:** snapshot (shares, call, strike), whether a TF exit was in the same session, the tasks minted.

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| replace_stock_only | Noul | Did the assignment replace include a call? | noul ≥ 0.85 → FAIL |
| no_replace_on_exit | Noul | Was a replace minted on a day the TF exit also fired? | noul ≥ 0.85 → FAIL |

**Runner:** spec first, then `jev ask` on the snapshot transcript.
**On fail:** do not mark Phase 2 done.

## Non-goals

- Auto-rebuy without a human task
- Treating assignment as a TF exit signal
