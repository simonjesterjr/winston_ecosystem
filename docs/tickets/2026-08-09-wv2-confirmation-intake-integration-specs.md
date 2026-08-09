# Ticket: Wv2 — Confirmation Intake integration specs

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Confirmation Intake, Broker Gateway  
**Glossary:** Confirmation Intake, Trade Notification, Desk Confirm, Human-Gated  
**Monoliths:** **winston_v2** (primary); optional local **broker_gateway** in compose  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) §9  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Unit specs per service are not enough for capital-adjacent L1. Need integration coverage of the Wv2↔BG boundary: pull → store → match → prefill → human Confirm still required.

## Scope

1. Integration suite using **WebMock/VCR** and/or **local BG dummy_sim**.  
2. Scenarios:  
   - Happy path: refresh → events → TradeNotification → match → prefill → Confirm books once  
   - Orphan event: no auto-link  
   - Ambiguous: no silent pick  
   - Re-pull idempotent  
   - BG down: fail closed, no invent  
3. Assert **no** Position open without Desk Confirm.  
4. Assert **no** place_order HTTP calls.  
5. Reuse shared contract fixtures from harness ticket.  
6. Document how to run the suite in AGENTS.md / ticket notes.

## Non-goals

- Live Schwab CI dependency  
- L3 write tests  
- Full browser e2e (request/system specs sufficient for v1)

## Domain locks

- Human Confirm required  
- L1 only  
- Ruby/Rails  

## Acceptance

- [ ] Integration specs green in CI or documented compose path  
- [ ] Happy path + orphan + ambiguous + idempotent re-pull covered  
- [ ] Explicit assert: no auto-book; no place_order  
- [ ] Uses shared fixtures  

## Related

- Fixtures: [`2026-08-09-l1-contract-fixtures-and-test-harness.md`](2026-08-09-l1-contract-fixtures-and-test-harness.md)  
- Dummy: [`2026-08-09-bg-dummy-sim-adapter.md`](2026-08-09-bg-dummy-sim-adapter.md)  
- Match: [`2026-08-09-wv2-match-prefill-confirmation-intake.md`](2026-08-09-wv2-match-prefill-confirmation-intake.md)  
