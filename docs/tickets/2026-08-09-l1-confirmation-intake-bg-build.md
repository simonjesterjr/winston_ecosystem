# Ticket: L1 Confirmation Intake + Broker Gateway — build epic

**Status:** In progress  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Confirmation Intake, Broker Gateway, Winston Broker Evidence Standard, Human-Gated, Desk Confirm, Trade Notification  
**Glossary:** Broker Gateway, Confirmation Intake, Trade Notification, Desk Confirm, Desk Send, Single Fulfillment Identity, Human-Gated  
**Monoliths:** **`broker_gateway`** (new); **winston_v2** (Confirmation Intake); ecosystem interfaces/docs  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) Phase 5–7; Grill B Q1–Q7  
**Origin:** Grill B handoff — build path item 1 (implementation authorized)

## Authorization

**L1 Confirmation Intake / Broker Gateway implementation is authorized** by Grill A + Grill B domain locks. This epic indexes the implement tickets; it does not re-open design.

### Domain locks (do not re-open)

| Lock | Meaning |
|------|---------|
| **L1 capabilities only** | `auth` + `txn_read` + `order_read` — **no** `order_write`, **no** Desk Send, **no** `place_order` until **ADR-010** |
| **Human-Gated book** | Evidence may prefill / mismatch; booking requires **Desk Confirm** or **Corrective Amend** — never silent book from notifications |
| **Ownership** | **Broker Gateway** owns transport + **Winston Broker Evidence Standard** (JSONL append-only); **Wv2** owns match / prefill / book |
| **Channel** | API poll primary; **no email as source of truth** |
| **Language** | Ruby/Rails for BG and Wv2 |

## Child tickets (implementation)

### Ecosystem contracts

| Ticket | Role |
|--------|------|
| [`2026-08-09-winston-broker-evidence-standard-interface.md`](2026-08-09-winston-broker-evidence-standard-interface.md) | Land `interfaces/winston-broker-evidence-standard.md` |

### Broker Gateway (Rails)

| Ticket | Role |
|--------|------|
| [`2026-08-09-broker-gateway-rails-scaffold.md`](2026-08-09-broker-gateway-rails-scaffold.md) | Scaffold monolith, compose, health |
| [`2026-08-09-bg-adapter-registry-and-capability-profile.md`](2026-08-09-bg-adapter-registry-and-capability-profile.md) | Registry keys + CapabilityProfile + binding (Q8 TBD) |
| [`2026-08-09-bg-dummy-sim-adapter.md`](2026-08-09-bg-dummy-sim-adapter.md) | Dummy/sim adapter for paper path + contract tests |
| [`2026-08-09-bg-schwab-read-adapter-l1.md`](2026-08-09-bg-schwab-read-adapter-l1.md) | Schwab auth + order_read + txn_read (fixtures → live) |
| [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md) | Append-only JSONL + PG registry/cursors |
| [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md) | Refresh/poll commands + GET events since cursor |

### Wv2 Confirmation Intake

| Ticket | Role |
|--------|------|
| [`2026-08-09-wv2-bg-client-and-event-cursor.md`](2026-08-09-wv2-bg-client-and-event-cursor.md) | BG client + cursor store + pull loop |
| [`2026-08-09-wv2-trade-notification-store-and-normalize.md`](2026-08-09-wv2-trade-notification-store-and-normalize.md) | Durable TradeNotification face |
| [`2026-08-09-wv2-match-prefill-confirmation-intake.md`](2026-08-09-wv2-match-prefill-confirmation-intake.md) | Match + prefill; never auto-book |
| [`2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md`](2026-08-09-wv2-desk-workflow-hitl-evidence-ui.md) | Desk UI: evidence, mismatch, Confirm/Amend |
| [`2026-08-09-wv2-confirmation-intake-integration-specs.md`](2026-08-09-wv2-confirmation-intake-integration-specs.md) | Integration tests vs BG dummy / fixtures |

### Cross-cutting

| Ticket | Role |
|--------|------|
| [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md) | Shared evidence fixtures + Wv2↔BG contract tests |

## Related (not children; do not block first L1 ship alone)

| Ticket | Relation |
|--------|----------|
| [`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md) | Sandbox reality for live Schwab read |
| [`2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md`](2026-08-05-signal-path-truth-fulfillment-link-exit-reconcile.md) | D10 capital — related; not L1 blocking for first ship |
| [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md) | Discovery — **superseded** by this L1 implement set |

## Non-goals (epic)

- L2 position/balance reconcile as capital SoT  
- L3 Desk Send / `order_write` / ADR-010  
- Email as primary confirmation channel  
- Shared PG between BG and Wv2  
- Manual adapter moved into BG (Manual stays zero-IO escape hatch in Wv2; paper default is `dummy_sim` via BG)

## Acceptance (epic)

- [ ] All child tickets filed and linked from INDEX  
- [ ] Discovery ticket re-scoped to point here  
- [ ] Plan §15 notes L1 tickets filed + implementation authorized  
- [ ] Child tickets complete when L1 path works end-to-end: BG poll/evidence → Wv2 TradeNotification → match/prefill → human Desk Confirm (no auto-book, no place_order)  
- [ ] Ruby/Rails for BG and Wv2 surfaces  

## Suggested build order

1. Evidence Standard interface (contract) + contract fixtures  
2. BG Rails scaffold  
3. Evidence store + internal API  
4. Adapter registry + dummy/sim adapter  
5. Wv2 client + TradeNotification store  
6. Match/prefill + desk UI  
7. Schwab read adapter (fixtures first; live after sandbox spike)  
8. Integration specs  

## Open questions

| ID | Question | Notes |
|----|----------|-------|
| **LOCKED-paper→dummy_sim** | Paper default binding? | **Locked 2026-08-09:** paper OPs default to BG **`dummy_sim`** (synthetic evidence → full Confirmation Intake). **`manual`** remains zero-IO escape hatch in Wv2 only. Never live credentials / `order_write` for paper. |
| **Q8** | OP ↔ broker account binding model | Deferred post-build; document TBD in registry ticket |
| **Q9** | Match ownership detail | Largely implied (Wv2); deferred post-build |

## Related docs

- Session: [`docs/session-reports/2026-08-09-1408-trade-fulfillment-grill-b.md`](../session-reports/2026-08-09-1408-trade-fulfillment-grill-b.md)  
- `CONTEXT.md` — Confirmation Intake, Broker Gateway, Winston Broker Evidence Standard  
- ADR-009 / human-gated business-context  
