# ADR-013: Fulfillment write — IBKR paper WQ first, Order Intent types stay open

**Status:** Accepted  
**Date:** 2026-09-06  
**Deciders:** Operator (grill 2026-09-06) + Architecture  
**Builds on:** ADR-006 (lineage / paper vs real), ADR-009 (Human-Gated desk; WQ Plan Approve addendum)  
**Does not replace:** ADR-010 (Risk Scale Meta-Layer — unrelated number collision)  
**Source design:** `plans/production-ready-wq.md` §8; grill 2026-09-06  
**Glossary:** `CONTEXT.md` — Desk Confirm, Desk Send, Order Intent, Working WQ Leg, Accept-Fill, Plan Approve, Fulfillment Packaging Policy, Session Order Slate  
**Tickets:** `docs/tickets/2026-08-30-wq-phase4-one-at-a-time-send.md`

## Context

Older tickets said “no `order_write` until ADR-010.” ADR-010 is Risk Scale. The fulfillment-write law was never numbered. Meanwhile:

- Winston Quiver (WQ) paper Operational Portfolio #1372 is bound to Interactive Brokers (IBKR) paper DUT through Broker Gateway (`interactive_broker_trader_api`). Confirm on a Monday-plan `drop_book` task stamped a journal executed without closing the lot and without talking to DUT — because Confirm was **book only** and `drop_book` was not treated as `exit`.
- The operator’s intent: WQ is the desk for this book; Confirm on that desk **implies DUT action**.
- Alternatives considered for a closed cash session:
  - **A. Hide Confirm until the next cash session** — parks the desk on Sunday; the operator still wants to Approve and work the package.
  - **B. Confirm books WQ now (last close) and DUT catch-up later** — last-close vs Monday print is how the books drift.
  - **C. Confirm Desk Sends a market order; journal stays working; matched fill Accept-Fills at the print** — honest weekend; DUT is fulfillment SoT for that command.
  - **D. Per-leg limit vs market HITL from day one** — extra packaging UI; WQ is a simple book.

Paper Mint / Trend Following on the **same** IBKR adapter will later need **limit** and **stop-market** Order Intents (Session Order Slate: entry, pyramid, protective Working Stop from EOD levels during the cash session). A WQ-only market adapter would box that in.

Phase 4 of `production-ready-wq.md` assumed Schwab live as first write and “paper #1372 never `order_write`.” Operator lock 2026-09-01 already made IBKR paper DUT the WQ rehearsal broker. This ADR records that first write is **paper DUT**, not live Schwab.

## Decision

We choose **C** for WQ paper, with **Order Intent types reserved** for Mint/TF.

### 1. This is the fulfillment-write ADR

`order_write` is governed here, **not** by ADR-010. CapabilityGate, tickets, and comments that still say “ADR-010 before `place_order`” mean **this** document.

### 2. First write binding

- **Allowed:** `order_write: true` only on the Interactive Brokers **paper** binding (`env=sandbox`, DUT) used by the **WQ Shadow Portfolio**.
- **Forbidden until a later decision:** dummy_sim write, live IBKR (`env=live`), Charles Schwab `order_write`, Mint/TF Confirm-that-sends, Daily Analysis `place_order`, basket/`place_order` of the whole Monday package.
- Kill switch: binding `cap_order_write` false, or an explicit env/ops kill, must refuse `place_order` (fail closed). Auth-failed / needs_reauth refuses write.

### 3. WQ Confirm on that binding is Desk Send of one market Order Intent

On the IBKR-paper-bound WQ Shadow Portfolio, after **Plan Approve**:

1. Remaining ready legs run **one at a time**: **exits, then rebalances, then enters**. Refuse an enter (and a rebalance that **adds** risk) while an exit is still a **Working WQ Leg** or unconfirmed.
2. The tracking-task **Confirm** click **Desk Sends** a **regular-hours market** Order Intent for that one command (G20-style idempotent `client_order_key`, e.g. `wq-{plan_id}-{leg_id}`).
3. The journal stays **working** — not executed, cash not moved, lot not closed/opened — including when the cash session is closed and the broker queues the order for the next regular session.
4. Broker Gateway poll/refresh records evidence. A **matched** fill **Accept-Fills** that same Single Fulfillment Identity at the **print** (actual qty/price, including split executions as one command). Unmatched / reject / cancel → attention; do not invent a book.
5. Last-close / plan fill_price is a **size hint**, not the booked fill.

dummy_sim Confirm still **books** the lot (no DUT). Mint / Trend Following Confirm stays **book only**.

### 4. Market-only is WQ policy, not the IBKR adapter

WQ paper **Fulfillment Packaging Policy** is regular-hours market. The `interactive_broker_trader_api` class and this write path **must** still accept and transport **limit** and **stop-market** Order Intents so a later paper Mint bind can **Desk Send** a Session Order Slate (stops, exits, pyramids) without a second adapter. Do not implement `place_order` as market-only in the adapter.

### 5. Confirm ≠ Send remains the default

Trend Following, live capital, and any OP that is not the IBKR-paper WQ Shadow Portfolio keep ADR-009: Confirm books; Send places; Send does not open a Position by itself. This carve-out is named, scoped, and reversible by turning `order_write` off on the DUT binding.

### 6. Implementation (2026-09-06)

Paper DUT `place_order` is behind `BG_IBKR_ORDER_WRITE` + binding `cap_order_write`. Winston Quiver Confirm on that bind Desk Sends one regular-hours MKT; the journal stays **working** until matched fill evidence Accept-Fills at the print. `drop_book` is an exit. dummy_sim Confirm still books. Live IBKR, Schwab, basket send, and Daily Analysis `place_order` stay off. The IBKR adapter still fixtures LMT / STP / STPLMT.

## Rationale

- DUT is already the fulfillment home for this paper OP (**Broker Account Capital**). Booking WQ without a DUT order is a ghost desk.
- Booking last-close on Sunday and filling Monday is the drift we just spent a week unwinding.
- Hiding Confirm until Monday fights how the operator actually works the Monday package.
- Limits on WQ now would stall a simple book; omitting them from the **adapter** would stall Mint.

## Consequences

### Positive

- Numbered write law; ADR-010 collision ends
- WQ paper can become a real DUT rehearsal without a 13-name basket
- Mint/TF stop-market/limit remain first-class on the same adapter
- Weekend Confirm is honest (working, not booked)

### Negative

- Confirm means two different things by OP/adapter — must stay explicit on the WQ desk copy
- Paper DUT `place_order` is live broker IO (paper capital, not household) — session, tickle, and kill switch are operational, not optional
- IBKR overnight/queue behavior for regular-hours market must be verified on DUT, not assumed from docs
- Accept-Fill of WQ prints is a carve-out from TF discovery (stops only)

### Risks mitigated

- Ghost `drop_book` executed journals with flow 0 → working until print, then close at fill
- WQ last-close vs DUT print drift → Accept-Fill at print
- Market-only IBKR adapter boxing Mint → Order Intent types on the class
- “ADR-010 blocks write” confusion → this document
- Basket Send / DA place_order / live Schwab implied by paper DUT write → explicit forbids

## Related

- ADR-009 §11 — Plan Approve still locks; dummy_sim Confirm still books; IBKR-paper WQ Confirm-Send is this ADR  
- `plans/production-ready-wq.md` §8 — first write is IBKR paper DUT, not live Schwab  
- `interfaces/winston-broker-evidence-standard.md`  
- Grill 2026-09-06 in `CONTEXT.md` (Plan Approve, Working WQ Leg, Order Intent, Confirm vs Send carve-out)  
