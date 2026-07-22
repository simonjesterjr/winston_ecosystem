# Ticket: Grill-with-docs — fulfillment ownership, Schwab intake, extra-modal

**Status:** Proposed  
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

- [ ] Grill session completed (or explicitly deferred with reason)  
- [ ] Written decision log for topics above (in analysis decision log and/or session report)  
- [ ] CONTEXT / BC updated if any draft term or rule changed  
- [ ] Parent ticket [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md) acceptance items marked accepted/revised  
- [ ] Follow-on implementation tickets filed or linked (L1 only after discovery acceptance)  

## Related

- Session report: [`docs/session-reports/2026-07-22-1332-schwab-integration-landscape.md`](../session-reports/2026-07-22-1332-schwab-integration-landscape.md)  
- Parent discovery: [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md)  
- Sibling (process): single-fulfillment invariant / post-confirm amend (see analysis cross-links)  
- ADR-009 + `docs/business-context/human-gated-desk-and-fulfillment.md`  

## Notes

Suggested first grill question (already teed): post-confirm price fix → rewrite same lot vs append correction vs close+reopen.
