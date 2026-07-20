# Ticket: Order vs fill semantics (resting stops) — deferred

**Status:** Deferred
**Priority:** P3
**Date:** 2026-07-15  
**Series:** `journal-to-ledger` **#7** (optional later)  
**Analysis:** [`docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`](../analysis/2026-07-15-winston-journal-vs-trading-ledger.md)

## Problem

Industry trading ledgers and OMS stacks separate:

- **Orders** (working: limit, stop, cancel/replace)  
- **Fills** (executions that change cash/positions)  

Winston today collapses risk management into **Position.stop fields** updated by strategies (and, after series #3, by human set/update). There is no order lifecycle, no “resting stop order id,” and no journal line type for “placed stop without fill.”

That is fine for paper hygiene and ATR strategy stops. It is **not** fine if the desk needs:

- “I put a stop in at $55” as a distinct ledger event without re-opening  
- Multiple working orders per position  
- Cancel/replace without changing units  

## Scope (only when #3 is insufficient)

1. Design note: Order model vs journal `stop_adjust` rows vs position-only.  
2. If built: minimal `orders` table or journal action types (`stop_place`, `stop_cancel`, `stop_replace`) that do **not** change capital until fill.  
3. MCP/Telegram: place/cancel stop order; list open orders.  
4. Keep fills on existing journal confirm/book path.  
5. ADR or business-context update if irreversible.

## Non-goals (until this ticket is un-deferred)

- Broker routing  
- Full multi-leg OMS  
- Starting this before series #1–#3  

## Acceptance (when activated)

- [ ] Written design choice vs “position stop is enough”  
- [ ] If implementing: open order list + cancel without capital change  
- [ ] Fills still only via journal confirm/book  
- [ ] Analysis non-goals / scorecard updated  

## Depends on

| Relation | Ticket |
|----------|--------|
| Requires | #3 human stop path proven in production desk use |
| Prefer after | #1–#4 so ledger export can include order events if any |

## Discovery

Search: `journal-to-ledger`, analysis series ticket #7, status Deferred.  
Do **not** pick this up in the first journal→ledger session unless desk explicitly needs resting-order semantics beyond Position.updated_stop.  
