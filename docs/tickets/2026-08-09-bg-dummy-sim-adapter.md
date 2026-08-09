# Ticket: Broker Gateway — dummy/sim adapter (paper path + contracts)

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Broker Gateway, Trade Notification, Confirmation Intake  
**Glossary:** Broker Gateway, CapabilityProfile, Trade Notification, Paper Trading  
**Monoliths:** **broker_gateway**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) §9 contracts; Grill B Q7 fixtures-first  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

L1 needs a **read path without live broker** so Wv2 can exercise BG HTTP (refresh, cursor, events) and match/prefill in CI and paper desk. Manual adapter is **zero-IO inside Wv2** by domain lock — that path alone does **not** exercise the BG boundary. A **dummy/sim adapter** in BG synthesizes order/txn evidence for contract tests and paper-path rehearsal.

## Recommended design

| Concern | Recommendation |
|---------|----------------|
| **Purpose** | Synthesize `order_read` / `txn_read` evidence → Winston Broker Evidence Standard events |
| **Capabilities** | `auth` (no-op success), `order_read`, `txn_read`; **`order_write: false`** |
| **Triggers** | Refresh/poll API or Sidekiq job on `dummy_sim` binding |
| **Data** | Fixture sets and/or deterministic generators (symbol, side, qty, price, external ids) |
| **Orphans** | Can emit events with no Winston journal id (orphan path tests) |
| **Paper OPs** | Prefer binding paper rehearsal OPs to dummy_sim **through BG** so client/cursor always run |

### LOCKED — operator confirmation 2026-08-09

| Status | Decision |
|--------|----------|
| **LOCKED** | Paper OPs **default** to BG **`dummy_sim`** so Confirmation Intake is always exercised. **`manual`** remains zero-IO escape hatch inside Wv2 only. Never live credentials / `order_write` for paper. |

See CONTEXT fulfillment adapter keys + work graph §2.

## Scope

1. Register adapter key `dummy_sim` with L1 read CapabilityProfile.  
2. On refresh: produce append-only evidence events consistent with Winston Broker Evidence Standard.  
3. Support seeded scenarios: exact fill, partial (if schema allows), cancel/reject stub, orphan fill.  
4. No external network IO.  
5. Specs: refresh → events visible via BG GET-events API; idempotent re-refresh.

## Non-goals

- Simulating full OMS / resting stops product  
- `place_order` simulation that implies L3 readiness  
- Replacing Manual zero-IO policy in Wv2  
- Live Schwab calls  

## Domain locks

- No `order_write` / Desk Send  
- Human still Desk Confirms in Wv2  
- Ruby/Rails  
- API poll primary (dummy fulfills poll contract without vendor)

## Acceptance

- [ ] `dummy_sim` binding refresh writes evidence events  
- [ ] Events satisfy Evidence Standard + shared fixtures where applicable  
- [ ] Re-poll is idempotent (no duplicate logical events)  
- [ ] Wv2 can pull events via internal API (integration with client ticket)  
- [x] Docs note paper→`dummy_sim` default (locked 2026-08-09)  
- [ ] No network calls; no secrets required  

## Related

- Registry: [`2026-08-09-bg-adapter-registry-and-capability-profile.md`](2026-08-09-bg-adapter-registry-and-capability-profile.md)  
- Evidence store: [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md)  
- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
- Wv2 client: [`2026-08-09-wv2-bg-client-and-event-cursor.md`](2026-08-09-wv2-bg-client-and-event-cursor.md)  
