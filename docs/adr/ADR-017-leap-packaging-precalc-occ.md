# ADR-017: LEAP packaging — precalc OCC at Signal/slate (Model B)

**Status:** Proposed (awaiting operator accept) — **recommendation: accept** as desk lock aligned with 2026-09-14/15 LEAP proxy law and analysis Model B  
**Date:** 2026-09-15  
**Deciders:** Operator (pending) + Architecture / Grok Bot Chief of Staff (draft)  
**Builds on:** ADR-009 (Human-Gated desk; dual spines), ADR-013 (paper DUT `order_write`; Order Intent types; §7 Guardrail extra-modal = HITL)  
**Domain law:** [`docs/business-context/leap-extra-modal-proxy.md`](../business-context/leap-extra-modal-proxy.md); sticky 20D_BO [`turtle-s2-pyramid-and-working-stop.md`](../business-context/turtle-s2-pyramid-and-working-stop.md)  
**Authoritative plan:** [`plans/wv2-bg-ibkr-leap-fulfillment.md`](../../plans/wv2-bg-ibkr-leap-fulfillment.md)  
**Detailed inventory:** [`docs/analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md`](../analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md)  
**Parent:** [`plans/spending-capacity-and-leap-fulfillment.md`](../../plans/spending-capacity-and-leap-fulfillment.md)  
**Glossary:** `CONTEXT.md` — Extra-Modal Fulfillment, Fulfillment Packaging Policy, Desk Send, Order Intent, Fulfillment Link, Working Stop, Protective Stop Guardrail

## Context

Walnut / Trend Following signals size and evaluate Working Stops on the **underlying** Market. Operators want the **same unit** fulfilled with a listed LEAP (geometry **B**: the Desk-Sent command **is** the LEAP). Broker Gateway’s IBKR `resolve_conid` is **stock-biased** unless `intent["conid"]` is explicit. Client Portal Gateway can place MKT/LMT on an OPT conid when given that conid.

Two contract-timing models were inventoried (analysis 2026-09-15):

- **Model A — Live resolve at Confirm/Send:** secdef dance on the critical Send path; strike matches fill-time last; Confirm can be blind unless preview is mandatory.  
- **Model B — Precalc at Signal / slate:** candidate OCC (and optional conid) stamped on handoff / `fulfillment_details`; Send verifies conid and warns/refuses on stale strike class; Approve sees the instrument.

ADR-009 requires Desk Approve to see what will be sent. ADR-013 requires fail-closed paper write and HITL for extra-modal protective path (not silent option STP).

## Decision

We choose **Model B** for v1 paper LEAP packaging:

1. **Precalc OCC at Signal / slate time** (or Confirm packaging step that stamps the same fields): strike, expiry, right, contracts, optional `ibkr_conid`, `instrument_label` / OCC, `packaging_resolved_at`, `underlying_last_at_resolve`. Journal / Book Market remains the **underlying**.  
2. **Desk Send verifies** conid (refresh if missing) and **does not silently re-ATM**. If underlying last has moved past the packaged strike class (e.g. >½ strike increment), **refuse or force HITL re-pick**.  
3. **Order Intent for OPT** carries explicit `conid` + `asset_class=option` (or `sec_type=OPT`); BG must never fall through to NYSE/NASDAQ stock search for that intent.  
4. **Entry:** MKT or LMT on the OPT conid; **no** protective option STP for v1. Stop-out: underlying Working Stop / sticky 20D_BO → **HITL** sell-to-close of the packaged LEAP.  
5. **Model A** remains a **fallback only** when CPGW was down at slate mint and `conid` is blank — resolve once at Confirm packaging, then stamp details (converges to B). Silent resolve-inside-`place_order` with no stamped packaging fields is **forbidden**.

## Alternatives considered

| Alt | Why not for v1 |
|-----|----------------|
| **Model A as silent resolve at Send** | Blind Approve (violates ADR-009 HITL preview); secdef latency on MKT urgency; stock-biased resolve risk |
| **Model A with mandatory Confirm preview** | Functionally B-at-Confirm; still pays secdef on every Send unless stamped |
| **Geometry A** (stock STP “fills as LEAP”) | Rejected in 2026-09-09 analysis; not this ADR’s scope |
| **Silent option protective STP** | Forbidden by ADR-013 §7 Guardrail / leap-extra-modal-proxy HITL |

## Consequences

### Positive

- Approve sees exact OCC / conid / cash outlay before Send.  
- Send path stays thin and fail-closed.  
- Aligns WQ-like intent shape (`client_order_key` + explicit instrument) with OPT.  
- Slate rebuild culture can refresh candidate LEAPs with DAY parks.

### Negative / residual

- Packaged strike may stale overnight — mitigated by Send recheck + HITL re-pick (not silent re-ATM).  
- Requires Wv2 packaging fields + BG OPT intent schema (tickets 2026-09-15-*).  
- Expect **ADR-013 addendum** when OPT Order Intent + stop HITL are fully operator-locked in code.

### Risks mitigated

- Blind option Send.  
- Stock conid resolved for a LEAP ticker.  
- Silent re-ATM changing the approved instrument.

## Smoke (when implemented)

- Handoff / slate shows `fulfillment_type=leap` + OCC + optional conid; Book Market = underlying.  
- BG place with `asset_class=option` and missing `conid` → refuse.  
- Paper DUT: one operator Desk-Sent OPT MKT/LMT → working → Accept-Fill at option print.  
- Agent Desk-Send of options still impossible / refused.

## Related

- Plan: `plans/wv2-bg-ibkr-leap-fulfillment.md`  
- Tickets: `2026-09-15-wv2-leap-packaging-fields.md`, `2026-09-15-bg-ibkr-opt-order-intent-prove.md`, `2026-09-09-extra-modal-leap-unit-evaluation.md`  
- Session: `docs/session-reports/2026-09-14-2330-leap-proxy-law-and-wv2-bg-plan.md`
