# Ticket: Broker confirmation intake (email / API) for desk fulfillment

**Status:** Superseded by L1 implement tickets (discovery closed via Grill A/B)  
**Priority:** P2  
**Date:** 2026-07-21  
**Series:** `adr-009-desk-fulfillment` → superseded by `trade-fulfillment-engine` L1  
**Domain:** ADR-009 Fulfillment, Booked Capital Spine, Desk Workflow  
**Glossary:** Desk Action, Desk Handoff, Desk Workflow, Signal Spine, Booked Capital Spine, Fulfillment, Journal, Working Stop, Confirmation Intake, Broker Gateway, Trade Notification  
**Monoliths:** primarily **Wv2** + **broker_gateway** (implementation); discovery was design-only  
**Superseded by:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md) and child implement tickets (2026-08-09-*)

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
  → broker API poll (primary) produces evidence events
       (symbol, side, qty, price, time, account, order id, …)
  → Broker Gateway stores Winston Broker Evidence Standard (JSONL)
  → Wv2 Confirmation Intake normalizes Trade Notifications
  → match to open Desk Handoff / draft Journal / Position
  → prefill or verify booked fill; surface mismatch for human confirm
```

Human-gated boundary (ADR-009) stays: **Winston does not auto-open Positions from evidence alone** without an explicit policy decision. Default product intent: **evidence + prefill + match → human still confirms**.

## Discovery scope (this ticket) — COMPLETE

Spike / design work before implementation (done via analysis + Grill A + Grill B):

1. **Channels** — API poll primary; streamer L2+; **no email as SoT** (Grill A Q3).  
2. **Normalized confirmation schema** — Trade Notification / Winston Broker Evidence Standard.  
3. **Matching rules** — explicit link → underlying-aware soft match → human pick → orphan; never symbol-equality alone.  
4. **Product boundary** — human Confirm required v1; BG transport + evidence; Wv2 match/prefill/book.  
5. **Non-goals for discovery** — OMS, autotrader, L3 write without ADR-010 — locked.

## Implementation (authorized 2026-08-09)

**Do not implement under this discovery ticket.** Follow the L1 epic and children:

| Area | Ticket |
|------|--------|
| **Epic** | [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md) |
| Evidence interface | [`2026-08-09-winston-broker-evidence-standard-interface.md`](2026-08-09-winston-broker-evidence-standard-interface.md) |
| BG scaffold | [`2026-08-09-broker-gateway-rails-scaffold.md`](2026-08-09-broker-gateway-rails-scaffold.md) |
| Registry / CapabilityProfile | [`2026-08-09-bg-adapter-registry-and-capability-profile.md`](2026-08-09-bg-adapter-registry-and-capability-profile.md) |
| Dummy/sim adapter | [`2026-08-09-bg-dummy-sim-adapter.md`](2026-08-09-bg-dummy-sim-adapter.md) |
| Schwab L1 read | [`2026-08-09-bg-schwab-read-adapter-l1.md`](2026-08-09-bg-schwab-read-adapter-l1.md) |
| Evidence store | [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md) |
| BG internal API | [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md) |
| Wv2 client + cursor | [`2026-08-09-wv2-bg-client-and-event-cursor.md`](2026-08-09-wv2-bg-client-and-event-cursor.md) |
| TradeNotification store | [`2026-08-09-wv2-trade-notification-store-and-normalize.md`](2026-08-09-wv2-trade-notification-store-and-normalize.md) |
| Match + prefill | [`2026-08-09-wv2-match-prefill-confirmation-intake.md`](2026-08-09-wv2-match-prefill-confirmation-intake.md) |
| Desk HITL UI | [`2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md`](2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md) |
| Integration specs | [`2026-08-09-wv2-confirmation-intake-integration-specs.md`](2026-08-09-wv2-confirmation-intake-integration-specs.md) |
| Contract fixtures | [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md) |
| Schwab sandbox spike | [`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md) |

## Acceptance (discovery ticket)

Discovery acceptance satisfied via Grill A (2026-08-06) + Grill B Q1–Q7 (2026-08-07–09). **Not archived** so history and links remain in the active index until L1 epic ships or ops prefer archive hygiene later.

- [x] Written recommendation: email vs API vs both for v1 (with constraints) — **API poll primary; no email SoT** (Grill A Q3)  
- [x] Draft normalized confirmation event shape — **Trade Notification** + **Winston Broker Evidence Standard** (CONTEXT + Grill B Q4); full interface file is implement ticket  
- [x] Matching algorithm sketch + failure modes (ambiguous / orphan / late) — Grill A extra-modal + plan atomics; Q9 detail deferred post-build  
- [x] Explicit decision: human confirm still required vs optional auto-book — **required v1** (Grill A Q2)  
- [x] Security note: mailbox/API secrets, PII, retention — OAuth/host secrets in BG; redact accounts; analysis docs  
- [x] Follow-on implementation ticket(s) filed — **2026-08-09 L1 epic + children**  
- [x] **(Expanded)** Automation ladder examined (L0–L4): L1 only near-term; L3 = ADR-010; no implement of write path  

### Locked answers (Grill A/B)

| Item | Locked recommendation |
|------|------------------------|
| Channel v1 | **API poll primary**; streamer L2+; **no email as SoT**; missing conf → DAR/Telegram warn + human attach/link |
| Event shape | **Trade Notification** face; durable **Winston Broker Evidence Standard** (JSONL) in **Broker Gateway** |
| Matching | explicit link → underlying-aware soft match → human pick → orphan; **never symbol-equality alone** |
| Human confirm | **Required v1** (real); no silent book-from-notification |
| Ownership | BG = transport + evidence; Wv2 = match/prefill/book |
| L1 capabilities | `auth` + `txn_read` + `order_read` only |
| Security | OAuth + re-auth ops; secrets in BG not Wv2; redact accounts in Telegram |
| Automation | **L1 only** near-term; L3+ = ADR-010 |

## Related

- **Master plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md)  
- **L1 epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
- **Grill A:** [`2026-07-22-grill-fulfillment-schwab-extra-modal.md`](2026-07-22-grill-fulfillment-schwab-extra-modal.md) — Done  
- **Grill B session:** [`docs/session-reports/2026-08-09-1408-trade-fulfillment-grill-b.md`](../session-reports/2026-08-09-1408-trade-fulfillment-grill-b.md)  
- **Analysis:** [`docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`](../analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md)  
- **Schwab discovery:** [`docs/analysis/2026-07-22-schwab-integration-discovery.md`](../analysis/2026-07-22-schwab-integration-discovery.md)  
- ADR-009 — Human-gated desk and fulfillment boundary  
- `docs/business-context/human-gated-desk-and-fulfillment.md`  

## Notes / open questions (carry to implement)

- Binding model Q8 and match detail Q9 deferred post-build — see L1 epic.  
- Paper → dummy BG vs Manual zero-IO only — **OPEN** on dummy/sim ticket.  
- Schwab sandbox availability — spike ticket.  
