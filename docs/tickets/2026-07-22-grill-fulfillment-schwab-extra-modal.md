# Ticket: Grill-with-docs — fulfillment ownership, Schwab intake, extra-modal

**Status:** Done (Grill A completed 2026-08-06)  
**Priority:** P2  
**Date:** 2026-07-22  
**Series:** `adr-009-desk-fulfillment`  
**Domain:** ADR-009 Fulfillment, Extra-Modal Fulfillment, Booked Capital Spine, broker intake  
**Glossary:** Extra-Modal Fulfillment, Fulfillment Packaging, Signal Spine, Booked Capital Spine, Human-Gated, Desk Workflow, BrokerFillEvent (proposed)  
**Monoliths:** primarily **Wv2** design; docs in **ecosystem**  

## Problem

Discovery and landscape analysis for Schwab broker access and desk fulfillment are written, but **domain law is not locked**. A `/grill-with-docs` session was teed (including post-confirm amend Q1) and then paused for research. Without grill outcomes we risk implementing:

- symbol-equality broker matching (breaks **Extra-Modal Fulfillment**),  
- wrong post-confirm amend semantics (WMT double-book class bugs),  
- premature L3 place_order, or  
- leaving parent discovery acceptance open indefinitely.

## Desired outcome

Run `/grill-with-docs` against:

1. [`docs/analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md`](../analysis/2026-07-22-winston-fulfillment-ownership-and-broker-intake.md)  
2. [`docs/analysis/2026-07-22-schwab-integration-discovery.md`](../analysis/2026-07-22-schwab-integration-discovery.md)  
3. [`docs/analysis/2026-07-22-schwab-thinkorswim-access-landscape.md`](../analysis/2026-07-22-schwab-thinkorswim-access-landscape.md) (§2a extra-modal)  
4. Glossary terms already drafted in `CONTEXT.md` (Extra-Modal Fulfillment, packaging)  
5. Plan HITL / stack-rank sections: [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) §5 (human pass pyramid A for entry D)

**Lock or revise:**

| Topic | Draft recommendation (challenge in grill) |
|-------|-------------------------------------------|
| One fulfillment identity per signal leg | Yes — amend not rebook |
| Post-confirm edit | Corrective amend same lot for price/qty; close+reopen for true cancel/duplicate |
| Broker v1 channel | Schwab API poll primary; email fallback |
| Human confirm v1 | Always required for real |
| Extra-modal | Signal Market for DA; cash/returns on packaging; link mandatory; no symbol-equality match |
| Automation ceiling near term | L1–L2 only; L3+ needs separate ADR |
| Trade order default | Intent/draft in Winston first for signaled enters; reverse for unsignaled exits |

Update CONTEXT / business-context / ADRs only where grill crystallizes hard decisions. Then close or re-scope parent discovery ticket acceptance boxes.

## Non-goals

- Implementing broker ingest or place_order  
- Full Schwab OAuth spike (optional separate work)  
- Multi-broker abstraction completeness  

## Acceptance

- [x] Grill session completed (or explicitly deferred with reason) — **Grill A 2026-08-06**  
- [x] Written decision log for topics above — `plans/trade-fulfillment-engine.md` Phase 2 log + CONTEXT  
- [x] CONTEXT / BC updated if any draft term or rule changed  
- [x] Parent ticket [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md) acceptance items marked accepted/revised — **superseded 2026-08-09; discovery boxes closed via Grill A/B**  
- [x] Follow-on implementation tickets filed or linked (L1 only after discovery acceptance) — **[`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md) + children**  

### Grill A outcomes (summary)

| Topic | Locked |
|-------|--------|
| Single fulfillment + corrective amend | Domain law; shipped code |
| L1 human confirm | Always (no silent book) |
| Channel | API poll primary; streamer L2+; **no email SoT**; missing conf → warn + human link |
| Extra-modal match | No symbol-equality alone |
| Desk Pass | Third Passed Signal kind; required reason |
| Capital mid-life | Signal-path truth; link ±$D; exit reconcile |
| Trade order | Intent-first enters; trade-first stop-outs |
| Ceiling | L1 only near-term |
| Object model | Journal + Task v1 |  

## Related

- **Master plan (2026-08-05):** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) — this ticket is **Grill A** vehicle; plan also schedules Phase 1 Q&A + Grill B (port/capital/L3)  
- Session report: [`docs/session-reports/2026-07-22-1332-schwab-integration-landscape.md`](../session-reports/2026-07-22-1332-schwab-integration-landscape.md)  
- Parent discovery: [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md)  
- Sibling (process): single-fulfillment invariant / post-confirm amend (archived Done)  
- ADR-009 + `docs/business-context/human-gated-desk-and-fulfillment.md`  

## Notes

Suggested first grill question (already teed): post-confirm price fix → rewrite same lot vs append correction vs close+reopen.
