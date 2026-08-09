# Ticket: L1 contract fixtures + test harness (Wv2 ↔ BG)

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Winston Broker Evidence Standard, Confirmation Intake  
**Glossary:** Winston Broker Evidence Standard, Trade Notification, Broker Gateway  
**Monoliths:** ecosystem fixtures; **broker_gateway**; **winston_v2**  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) §9  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Grill B Q7 locked **contract + fixtures first**. Shared evidence event fixtures and boundary contract tests prevent BG and Wv2 from drifting on schema and cursor semantics.

## Scope

1. **Shared fixture set** (ecosystem path preferred, e.g. under `ecosystem/interfaces/` or `ecosystem/docs/fixtures/broker-evidence/`):  
   - sample evidence JSONL events (fill, status, orphan, multi-event window)  
   - optional Schwab-shaped raw payloads mapped to standard events  
2. **Contract tests at Wv2↔BG boundary:**  
   - BG: fixture ingest → GET events shape  
   - Wv2: client normalize against same fixtures  
3. Document fixture version alignment with Evidence Standard version.  
4. CI-friendly: no live broker.  
5. Link dummy_sim to load/publish the same fixtures where practical.

## Non-goals

- Live OAuth CI  
- Full golden master of every Schwab field forever  
- Email body fixtures as SoT  

## Domain locks

- L1 evidence only  
- No place_order fixtures required  
- Human Confirm out of band for pure contract tests  

## Acceptance

- [ ] Fixture directory/files landed and referenced from Evidence Standard interface  
- [ ] At least one BG-side and one Wv2-side consumer of fixtures in specs  
- [ ] Contract assert: required fields present; idempotency key stable  
- [ ] Documented run command  
- [ ] No live network required  

## Related

- Interface: [`2026-08-09-winston-broker-evidence-standard-interface.md`](2026-08-09-winston-broker-evidence-standard-interface.md)  
- Dummy: [`2026-08-09-bg-dummy-sim-adapter.md`](2026-08-09-bg-dummy-sim-adapter.md)  
- Wv2 integration: [`2026-08-09-wv2-confirmation-intake-integration-specs.md`](2026-08-09-wv2-confirmation-intake-integration-specs.md)  
- Schwab spike: [`2026-08-07-schwab-trader-api-sandbox-spike.md`](2026-08-07-schwab-trader-api-sandbox-spike.md)  
