# Ticket: Broker confirmation intake (email / API) for desk fulfillment

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-21  
**Series:** `adr-009-desk-fulfillment` (follow-on; not #1–#6 core)  
**Domain:** ADR-009 Fulfillment, Booked Capital Spine, Desk Workflow  
**Glossary:** Desk Action, Desk Handoff, Desk Workflow, Signal Spine, Booked Capital Spine, Fulfillment, Journal, Working Stop  
**Monoliths:** primarily **Wv2** (+ optional Cromwell/agent surface); broker/email plumbing TBD

## Problem

Today the desk loop is:

1. DAR / Desk Handoff proposes a task.  
2. Human opens **Desk Workflow** (or classic desk), fills the form, and **confirms** in Winston.  
3. Human separately executes at the broker (e.g. Schwab).  

Winston’s **Booked Capital Spine** is whatever the human types (or prefill allows). There is **no** inbound channel that proves “Schwab filled ABC @ xxx for yyy shares” and attaches that evidence to the journal/lot. That gap matters for **real** OPs: process miss vs actual fill, stop-out reconciliation, audit, and dual-spine honesty.

We want to **figure out** how Winston can **read trade confirmations** (email first; broker API second or alternative) so confirm can be prefilled, matched, or verified against broker truth—not so Winston becomes an OMS.

## Desired flow (target sketch)

```
DAR next task
  → human opens Desk Workflow / fills form (signal intent)
  → human executes at Schwab (or other broker)
  → broker sends email confirmation and/or API fill event
       (symbol, side, qty, price, time, account, order id, …)
  → Winston ingests confirmation
  → match to open Desk Handoff / draft Journal / Position
  → prefill or verify booked fill; surface mismatch for human confirm
```

Human-gated boundary (ADR-009) stays: **Winston does not auto-open Positions from email alone** without an explicit policy decision. Default product intent: **evidence + prefill + match → human still confirms** (or a later explicit auto-book decision).

## Discovery scope (this ticket)

Spike / design work before implementation:

1. **Channels**  
   - Email: IMAP/Gmail API/forwarding mailbox dedicated to confirmations; parse Schwab (and later others).  
   - API: Schwab (or broker) trade/order history webhook or poll—availability, auth, ToS.  
   - Prefer dual-path design: same **normalized fill event** whether source is email or API.

2. **Normalized confirmation schema**  
   - Minimum fields: broker, account id/ref, symbol, side, qty, fill price(s), fill time, order/confirmation id, raw payload ref.  
   - Partial fills, multi-leg, options/LEAPs, cancellations, corrections.

3. **Matching rules**  
   - Match confirmation → open Desk Handoff / draft journal / OP / position (fingerprint, symbol, side, size band, signal/fill window).  
   - Ambiguous / multi-match / no-match behavior (queue for human, never silent wrong book).  
   - Unsignaled exits (stop-out, discretionary) still allowed with reason + lot link (existing ADR-009).

4. **Product boundary**  
   - Confirm: prefill Desk Workflow from matched confirmation vs verify after human entry vs both.  
   - Never treat broker email as Signal Spine; only **Fulfillment / Booked Capital** evidence.  
   - Privacy, credentials, and where secrets live (host vs container vs agent).

5. **Non-goals for discovery**  
   - Full OMS / resting order management.  
   - Autotrader or DA auto-fill.  
   - Multi-broker production support on day one (Schwab as first exemplar is fine).  
   - Replacing human desk confirm without a separate ADR decision.

## Implementation (later; not required to close discovery)

Only after discovery + acceptance of approach:

- Ingest pipeline + durable store for raw + normalized confirmations.  
- Matcher + Desk Workflow / confirm-path integration.  
- DAR / attention for unmatched or mismatched confirmations.  
- Optional Cromwell skill: “attach confirmation” / “review unmatched fills.”  
- Specs + ops runbook (mailbox setup, rotate credentials).

## Acceptance (discovery ticket)

- [ ] Written recommendation: email vs API vs both for v1 (with constraints)  
- [ ] Draft normalized confirmation event shape (fields + examples from real Schwab emails if available)  
- [ ] Matching algorithm sketch + failure modes (ambiguous / orphan / late)  
- [ ] Explicit decision: human confirm still required vs optional auto-book (ADR-009 impact)  
- [ ] Security note: mailbox/API secrets, PII, retention  
- [ ] Follow-on implementation ticket(s) filed or this ticket re-scoped with build acceptance  

## Related

- **Analysis (grill tee):** [`docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`](../analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md) — fulfillment ownership model + broker intake design; run `/grill-with-docs` against that doc before implementing  
- ADR-009 — Human-gated desk and fulfillment boundary  
- `docs/business-context/human-gated-desk-and-fulfillment.md` — dual spines, Desk Workflow  
- ADR-006 — OP lifecycle / real capital series  
- Series tickets #1–#6 (`docs/tickets/2026-07-20-*` desk fulfillment)  
- `docs/tickets/2026-07-15-journal-ledger-order-vs-fill-deferred.md` — order vs fill deferred  
- `docs/tickets/2026-07-09-capital-activation-mcp-telegram.md` — real capital path  
- Stop-Out Reconciliation (shipped) — external fill truth adjacent problem  

## Notes / open questions

- Is the human expected to confirm **in Winston first** then trade, or **trade first** then Winston books from confirmation? Both modes may need support; product default should be explicit.  
- Schwab email formats change; parser brittleness argues for API if available.  
- Options packaging (signal stock size vs LEAP contracts) already dual-spine—confirmations must not collapse spines.  
