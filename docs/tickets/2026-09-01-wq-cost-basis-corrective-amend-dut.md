# Ticket: WQ cost-basis / Corrective Amend vs DUT fills

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Human gates:** operator said do **not** amend the original three WQ book prices  
**DoD:** remaining WQ lots either match DUT evidence or have an explicit skip reason  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md)  
**Related:** [`2026-09-01-wq-ibkr-paper-evidence-bind.md`](2026-09-01-wq-ibkr-paper-evidence-bind.md)  
**Origin:** [`docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md`](../session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md)

## Problem

Paper WQ OP #1372 was filled on Interactive Brokers DUT070450 to matching **sizes** (0.0001 increment). Split executions booked via Confirm. Original WQ **prices** were not amended. DUT NLV/cash still diverges from the WQ ledger (~$11,977 / $293 vs ~$11,997 / $160). Confirm-from-evidence / Corrective Amend of cost basis was deferred.

## Scope

1. Inventory WQ executed journals vs DUT evidence (price, qty, split `execution_id`s).  
2. Corrective Amend **only** where the operator authorizes — never the original three prices already locked.  
3. Do not CashEvent-mimic DUT net liquidation (Capital Authority is broker; Risk Capital is NLV; WQ paper ledger stays journals).  
4. Document remaining cash/equity gap as expected vs defect.

## Non-goals

- Desk Send / `place_order`  
- Binding Mint to this account  
- Amending the three locked prices  

## Acceptance

- [ ] Lot-by-lot table: journal vs DUT (qty match / price match / skip reason)  
- [ ] Any authorized Corrective Amends have audit trail  
- [ ] Operator sign-off that remaining gap is hygiene, not a book error
