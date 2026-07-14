# Ticket: Confirm first paper journal on paper-focus cohort

**Status:** Done (2026-07-14 Phase 1)  
**Date:** 2026-07-13  
**Focus seed:** **Blue 62** → Wv2 OP `#12 Portfolio Blue · PBR62`

## Work completed

1. Focus OP Active with PBR 62 recipe (hygiene ticket).  
2. Historical eval **2026-07-10** produced AMZN long enter (`pending` → task #16 / journal #16).  
3. Confirmed via `Operations::JournalConfirmationService` (same path as MCP `wv2_confirm_journal`):
   - `execution_price`: 251.03  
   - `units`: **5** (explicit — auto PositionSizer returned 0; see notes)  
   - `fulfillment_type`: stock  
   - paper notes  
4. Capital: $10,000 → **$8,744.85** (flow −$1,255.15).  
5. Open position: **AMZN long 5 @ 251.03**.  
6. Next-day eval **2026-07-11**: position + capital retained; 0 new tasks.

## Acceptance

- [x] At least one journal confirmed as **paper** on the **Blue 62 focus** OP  
- [x] Linked task done/completed  
- [x] Subsequent analysis sees open position / updated capital  
- [x] Real capital still out of scope  

## Notes / follow-ups

1. **Initial CashEvent date** — import used `Date.current`, so historical `capital_base(as_of:)` was $0 until backdated to 2020-01-01. Import rake fixed to default `2020-01-01` (or `initial_capital_date`).  
2. **ATR sizing** — for several US names parquet `atr` ≈ price (GOOGL/AMZN/TSLA), so `PositionSizer` floors to 0 units. Paper confirm used explicit units. Investigate atr_17 column load separately (not blocking confirm path).  
3. Red-specific ticket `2026-07-10-confirm-first-red-paper-pending-action.md` can be closed as superseded (focus is Blue 62).

## Related

- Hygiene: `2026-07-13-paper-focus-active-hygiene-and-recipe.md`  
- Paper-first: `2026-07-13-paper-first-cohort-decision.md`  
- MCP: `wv2_confirm_journal`, `wv2_list_pending_actions`  
