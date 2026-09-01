# Ticket: Production-ready Winston Quiver (WQ) — epic

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-30  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway, ecosystem  
**Edges:** `plans/production-ready-wq.md`, `interfaces/winston-broker-evidence-standard.md`, ADR-006, ADR-009 §11  
**Human gates:** `/quiver_tracking` Approve / blow-away (Phase 1); developer.schwab.com (Phase 2); Capital Activation of a new real WQ series (Phase 3); Desk Send on live capital (Phase 4)  
**DoD:** Phases 1–3 verified; Phase 4 only after a new fulfillment-write ADR (not ADR-010)  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md)  
**Monoliths:** winston_v2 (Wv2), broker_gateway (BG), ecosystem  

## Problem

WQ paper desk exists (paste → Monday Rebalance Plan → Plan Approve → dummy_sim). Aim is a production-ready WQ that can, later, send **one** Schwab order at a time and confirm the fill. Code is ahead of human verification; the Schwab adapter is a stub; Plan Approve auto-books and must not become a live basket send.

## Scope

Index and sequence the four phases. Do not implement Phase 4 in this ticket.

| Phase | Ticket | Now |
|-------|--------|-----|
| 1 Paper cadence | [`2026-08-30-wq-phase1-paper-cadence-verify.md`](2026-08-30-wq-phase1-paper-cadence-verify.md) | **In progress** |
| 2 Schwab read + sandbox spike | [`2026-08-30-wq-phase2-schwab-read-and-sandbox.md`](2026-08-30-wq-phase2-schwab-read-and-sandbox.md) | Proposed (later today) |
| 3 WQ evidence bind | [`2026-08-30-wq-phase3-wq-schwab-evidence-bind.md`](2026-08-30-wq-phase3-wq-schwab-evidence-bind.md) | Proposed |
| 4 One-at-a-time Send | [`2026-08-30-wq-phase4-one-at-a-time-send.md`](2026-08-30-wq-phase4-one-at-a-time-send.md) | Proposed — blocked |

## Non-goals

- L4 autotrader
- Turtle-from-PDF / family-of-OPs (scrapped)
- paperMoney as API sandbox
- Write on dummy_sim or paper #1372

## Acceptance

- [ ] Phase 1 closed on compose (two dummy_sim cycles + flatten once)
- [ ] Phase 2: spike verdict written; Schwab read adapter fixtures green; `order_write` still false
- [ ] Phase 3: one hand-placed Schwab fill → evidence → Desk Confirm on a **new real** WQ series
- [ ] Phase 4 not started without write ADR + operator authorization
