# Ticket: Human stop on confirm/book + stop update path

**Status:** Proposed  
**Priority:** P1
**Date:** 2026-07-15  
**Series:** `journal-to-ledger` **#3**  
**Analysis:** [`docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`](../analysis/2026-07-15-winston-journal-vs-trading-ledger.md)

## Problem

Litmus desk line from the analysis:

> “I just bought 45 shares of GGG … at $58.87 **and put a stop in at $55**.”

Today `JournalPositionExecutor` always sets `original_stop` / `updated_stop` from **ATR × portfolio multiplier**. Confirm/book APIs accept units and price but **not** stop. There is no MCP/service to adjust a stop after open. Stops only move via strategy classes during evaluation.

## Scope (Wv2)

1. **Confirm / book open:** accept optional `stop_price` (or `stop`) on  
   - `JournalConfirmationService` / internal confirm  
   - Ad-hoc book service (series #2)  
   When present, write `Position.original_stop` and `updated_stop`; when absent, keep ATR default.  
2. **Stop update (open position):** service e.g. `Operations::PositionStopUpdateService`  
   - Input: portfolio, position_id (or market), `stop_price`, notes  
   - Updates `updated_stop`; append note to `action_description` or notes trail  
   - Optional: journal row with action type / notes only (if we want ledger line for stop moves — prefer lightweight first: position update + audit note; full `stop_adjust` journal type can wait for series #7)  
3. MCP + internal endpoints; ops shell commands (`confirm … stop=55`, `stop <position_id> price=…`).  
4. Cromwell skill update: confirmation-loop + book skill document stop params; **never invent stops**.  
5. Specs: override on open; update open position; reject closed position.

## Non-goals

- Resting order book / cancel-replace OMS (series #7)  
- Broker-synced stop orders  
- Changing default ATR stop strategy for signals that omit human stop  

## Acceptance

- [ ] Confirm enter with `stop_price: 55` yields position stop 55 (not ATR-only)  
- [ ] Ad-hoc book (when #2 lands) accepts same stop param  
- [ ] MCP/internal path updates stop on open position without inventing fills  
- [ ] Telegram skill docs mention stop override only when human provides it  
- [ ] Paper smoke on focus OP documented  

## Depends on / unblocks

| Relation | Ticket |
|----------|--------|
| Prefer after | #1 fill fields, #2 ad-hoc book (can ship confirm-only stop first if #2 slips) |
| Unblocks | #4 export (stop column truth), #7 order-vs-fill design |

## Related code

- `winston_v2/app/services/operations/journal_position_executor.rb`  
- `winston_v2/app/services/operations/journal_confirmation_service.rb`  
- `winston_v2/app/strategies/stops/*`  
- `ecosystem/ai/skills/winston-confirmation-loop/SKILL.md`  

## Discovery

Search: `journal-to-ledger`, analysis § litmus use case, series ticket #3.  
