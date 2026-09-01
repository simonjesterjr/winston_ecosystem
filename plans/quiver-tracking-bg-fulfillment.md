# Plan: Broker Gateway fills for Quiver Tracking (future)

**Status:** **Superseded 2026-08-30** by [`production-ready-wq.md`](production-ready-wq.md) Phases 3–4. Kept as historical intent.  
**Date:** 2026-08-21  
**Monoliths:** Broker Gateway (BG), Winston v2 (Wv2)  
**Depends on:** Tracking desk v1 (`quiver-tracking-desk.md`); L1 Confirmation Intake already in flight; fulfillment-write ADR (not current ADR-010) before any `order_write`  
**Ticket:** `docs/tickets/2026-08-21-quiver-tracking-bg-fulfillment.md` (status: Superseded)

## Why not now

Quiver Tracking is a **paper membership desk**: close the gap between a published PDF book and a paper Operational Portfolio (OP). Fills are Human-Gated paper confirms (same journal spine). Wiring Broker Gateway (BG) would mix:

- dummy_sim rehearsal (L1, already the paper default on TF OPs), or
- live `order_write` (L3, ADR-010, not shipped)

into a book that is **not** Daily Analysis and may reweight weekly.

Do that only after:

1. Tracking desk has stable PDF → gap tasks → confirm.
2. Operator wants the paper tracking lots to **practice** Confirmation Intake (`dummy_sim`) without TF signal rules, **or** a later real-money copy of the published book.

## What it would look like (when authorized)

- Tracking OP `fulfillment_adapter_key`: `manual` (v1) → optional `dummy_sim` for intake practice → never auto-`schwab_trader_api` without Capital Activation on a **new** real series (ADR-006).
- Gap task confirm still books the **signal-path** lot on the tracking OP (ticker + weight from PDF). Packaging (LEAPs, ETFs) stays Extra-Modal / Fulfillment Link — same as TF.
- **Desk Send** only if a write-capable adapter is bound and ADR-010 is accepted. Tracking reweights must not auto-send a 20-name basket without a package + HITL.
- BG does **not** fetch Quiver. BG remains broker evidence only.

## Non-goals even later

- DA minting tracking enters
- Silent book-from-PDF
- Using Quiver API as a broker

## Acceptance (future ticket)

- [ ] Written decision: dummy_sim practice vs real series
- [ ] Tracking confirms still Human-Gated
- [ ] No `order_write` without ADR-010
- [ ] Multi-leg weekly reweight is one desk package, not N unsolicited sends
