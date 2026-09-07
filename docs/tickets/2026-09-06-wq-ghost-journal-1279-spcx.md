# Ticket: Reverse or leave WQ ghost journal #1279 (SPCX drop)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Edges:** ADR-013; JournalConfirmationService `drop_book`; paper DUT lots  
**Human gates:** operator chooses reverse vs leave before the next SPCX Confirm-Send  
**DoD:** blotter either has no executed-but-open SPCX drop, or an explicit skip/leave note; DUT 6.2703 SPCX is not double-exited  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md)  
**Origin:** [`docs/session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md`](../session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md)  
**Related:** [`2026-08-30-wq-phase4-one-at-a-time-send.md`](2026-08-30-wq-phase4-one-at-a-time-send.md)

## Problem

Operator confirmed an SPCX `drop_book` while Confirm was still book-only. `JournalConfirmationService` treated only `task_type == "exit"` as a flatten; TaskMinter / gap tasks mint `drop_book`. Journal **#1279** stamped **executed** with flow 0; the lot stayed OPEN; paper DUT still held ~6.2703 SPCX.

The code path is fixed (ADR-013: `drop_book` is an exit; IBKR-paper Confirm now Desk Sends). The **row** was not reversed this session.

A later SPCX Confirm-Send could flatten DUT while WQ already thinks the drop executed — or skip the DUT exit because the task looks done.

## Scope

1. Inventory journal #1279, linked task, open SPCX lot on OP #1372, and DUT position.  
2. Operator pick: **reverse** the ghost (pass/cancel journal, reopen pending drop) **or leave** and treat the Monday SPCX exit as the DUT send.  
3. Do not invent a DUT order to “catch up” the ghost.  
4. Do not CashEvent-mimic.

## Non-goals

- Re-implementing `drop_book` as exit (done).  
- Live Schwab.  
- Amending unrelated cost basis ([`2026-09-01-wq-cost-basis-corrective-amend-dut.md`](2026-09-01-wq-cost-basis-corrective-amend-dut.md)).

## Acceptance

- [ ] Operator decision recorded (reverse vs leave)  
- [ ] WQ blotter and DUT SPCX size cannot double-count the same flatten  
- [ ] If reversed: journal #1279 is not `executed` with an open lot  
