# Ticket: Ad-hoc paper fill (journal without DAR draft)

**Status:** Proposed (Paper Telegram Phase 4 / Phase 3 follow-on)  
**Date:** 2026-07-14  
**Source:** Paper Telegram roadmap Phase 4; session `2026-07-14-1112-paper-telegram-phase0-1.md`

## Problem

“I bought 54 shares of TSMC at 323.44 for portfolio Magenta” is not supported. Confirm path only executes **existing draft** journals from daily analysis.

## Scope

1. Internal create path: draft-then-confirm or executed journal with explicit portfolio, market, date, direction, units, price.  
2. Reuse `JournalPositionExecutor` / capital flow rules.  
3. MCP tool + Cromwell skill (confirm-before-write).  
4. Engages OP (first journal locks shape per ADR-006).  

## Non-goals

- LEAP/options real mechanics (separate, deferred)  
- Broker automation  

## Acceptance

- [ ] Ad-hoc long stock fill updates position + capital_base  
- [ ] Same accounting as DAR confirm path  
- [ ] MCP + audit correlation_id  

## Related

- Phase 1 proved draft-confirm path on Blue PBR62  
- `JournalConfirmationService`  
