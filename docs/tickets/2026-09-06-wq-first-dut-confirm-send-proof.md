# Ticket: First paper DUT Confirm-Send proof (one exit)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Edges:** ADR-013; WqConfirmSend; WqFillBind; CPGW paper SSO  
**Human gates:** each Confirm (send MKT) click; paper CPGW session must be authenticated  
**DoD:** one approved exit (IBM or SPCX) → working journal → DUT fill evidence → Accept-Fill at the print; WQ lot closed at fill qty/price; dummy_sim path untouched  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md) §8  
**Origin:** [`docs/session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md`](../session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md)  
**Blocked on:** [`2026-09-06-wq-ghost-journal-1279-spcx.md`](2026-09-06-wq-ghost-journal-1279-spcx.md) if the first name is SPCX  
**Related:** [`2026-08-30-wq-phase4-one-at-a-time-send.md`](2026-08-30-wq-phase4-one-at-a-time-send.md)

## Problem

ADR-013 write is implemented and the DUT binding has `cap_order_write`. Specs and dummy_sim refuse were verified. **No live paper order** was sent. Overnight/queue behavior and Accept-Fill at a real print are still assumed from code + IBKR docs.

Monday-plan exits on the table (from the Quiver paste vs DUT book): IBM ~5.8377, SPCX ~6.2703. Exits before rebalances before enters.

## Scope

1. Client Portal Gateway paper SSO (`DUT070450`) healthy.  
2. Operator Confirm (send MKT) on **one** exit only.  
3. Watch: journal `working`, task in progress, no cash move until print.  
4. BG refresh / Confirmation Intake / `WqFillBind` books at the DUT print (split executions still one command).  
5. Stop. Do not basket the rest of the Monday package.

## Non-goals

- Sending the whole Monday package.  
- Live IBKR / Schwab.  
- Mint/TF Confirm-that-sends.

## Acceptance

- [ ] One exit Order Intent on DUT with `client_order_key` `wq-{plan_id}-{task_id}`  
- [ ] Journal was `working` between send and fill  
- [ ] Booked qty/price match the print, not last close  
- [ ] Remaining legs still unsent  
