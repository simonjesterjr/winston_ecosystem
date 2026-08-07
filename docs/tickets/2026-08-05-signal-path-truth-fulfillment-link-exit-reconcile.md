# Ticket: Signal-path operational truth + fulfillment link + exit capital reconcile

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-05  
**Series:** `trade-fulfillment-engine`  
**Domain:** ADR-009 Fulfillment, Extra-Modal Fulfillment, Booked Capital, Signal Spine, Desk Workflow  
**Glossary:** Signal Spine, Fulfillment, Fulfillment Packaging, Extra-Modal Fulfillment, Journal, Position, CashEvent, Working Stop, Operational Portfolio  
**Monoliths:** primarily **Wv2**; ecosystem docs (CONTEXT / business-context / plan after grill)  
**Origin:** Phase 1 Q&A D10 — operator decision 2026-08-05  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md)

## Problem

Winston Daily Analysis (DA) sizes and tracks risk on the **signal Market** (e.g. long **210 IBM** using methodology / EODHD data). Operators often **fulfill** that signal with different packaging (e.g. **2 January 2029 LEAPs**, ITM+OTM) or different fill prices.

Today’s dual-spine language tends toward “booked capital immediately follows packaging economics” (premium × multiplier, etc.). Operator product intent for real desk work is different:

1. **While the position is live**, Winston v2 (Wv2) should track the **signal path as operational truth**: entrance signal → fulfillment (as Winston understands the lot) → stop placement → pyramiding → exit — sized and journaled **as if** the signal share story were true (e.g. 210 IBM forever for sizing/risk path).  
2. **Fulfillments** (broker packages, LEAPs, actual prints) are **linked** to that signal for tracking (“fulfillment A is for signal S”) **without** forcing Wv2 DA/risk to recompute everything in option/premium space mid-life. Signalling stays on the **underlying market**.  
3. **At position exit** (or an explicit reconcile gate), reconcile **Wv2 signal-path truth ↔ actual fulfillments** and apply a **capital adjustment** `±$D` so household cash honesty lands **after** the trade lifecycle, not continuously mid-trade.

Without this model documented and built, we will either:

- corrupt methodology-comparable risk sizing with packaging noise every day, or  
- lose the economic truth of real LEAP/proxy fills until someone fixes capital by hand with no audit.

## Desired product model (Phase 1 lock — grill to ratify)

```
Signal S (e.g. long 210 IBM, risk %, stops in signal units)
    │
    ├─► Wv2 operational path (truth for DA / capacity / pyramid / Working Stop story)
    │     entrance → “fulfilled” signal lot → stops → pyramids → exit
    │     sized AS IF signal units (210 shares story)
    │
    └─► Fulfillment link(s) A, B, … (broker evidence / packaging)
          “fulfillment A is for signal S”
          may imply provisional capital delta note ±$D (not necessarily applied yet)
                │
                ▼
         On position exit (or explicit reconcile)
                │
                ▼
         Reconcile Wv2 path ↔ fulfillments → CashEvent adjustment ±$D
         Audit: signal identity, fulfillment ids, delta, who approved
```

### Speech / workflow shape

> Fulfillment A is for signal S, indicating a capital adjustment of ±$D.

Operator (or later L1 match) attaches A→S; system records the **indicated** delta; **application** of delta to `capital_base` is gated (prefer **on exit** / explicit reconcile — grill to confirm mid-life optional apply).

### What does **not** change

- DA continues on **signal Market** / Books.  
- Signaled Entry Rule still requires signal provenance for opens/pyramids.  
- Extra-modal packaging still allowed and must be **linkable**.  
- Broker confirmation intake (L1) still feeds evidence; it does not rewrite Signal Spine.

### What **does** change vs naïve “book LEAP cash immediately”

| Concern | While open | At exit / reconcile |
|---------|------------|---------------------|
| Risk sizing / capital_base for new signals | Follow **signal-path** lot economics (share story) | After adjustment, capital_base reflects **reconciled** cash |
| Packaging (LEAPs, proxies) | Linked; not full re-model of DA | Part of reconcile inputs |
| Fill price vs signal prefill | Can live on fulfillment record; Winston lot may keep signal story until reconcile | Delta into ±$D |
| Methodology comparability | Preserved | Preserved + honest cash catch-up |

**Honest label:** mid-life capital is **intentionally signal-proxied** (“dishonest” vs broker cash until reconcile). That is a product choice, not a bug — document it so operators know when capital is provisional vs reconciled.

## Scope

### A — Domain / docs (grill-gated)

1. Ratify or revise this model vs current CONTEXT **Booked Capital Spine** wording (may need dual terms: **Signal-path operational lot** vs **Fulfillment economics** vs **Reconciled capital**).  
2. Update plan decision log D10; business-context / ADR-009 extension or ADR-010 section.  
3. Reason codes for indicated vs applied capital adjustment.

### B — Data model (design → implement)

1. **Fulfillment link** entity or journal/fulfillment_details shape:  
   `signal_journal_id` / task / position_id, fulfillment id, packaging, broker refs, **indicated_capital_delta**, status (`linked` | `reconciled` | `void`).  
2. Lifecycle events on signal path remain Journals/Positions **in signal units**.  
3. **Reconcile on exit** service: compute ±$D from linked fulfillments vs Winston path; propose CashEvent `adjustment`; human confirm (v1).  
4. Optional: mid-life “indicated delta” visible on desk without applying.

### C — Workflows / UX / MCP

1. Desk / MCP: “attach fulfillment to signal” with indicated ±$D.  
2. Exit path: “reconcile fulfillments” step before/after close.  
3. DAR attention: open lots with large unreconciled indicated delta; exits missing reconcile.  
4. L1 confirmation match attaches as fulfillment link (not silent capital rewrite).

### D — Non-goals (this ticket)

- Full options Greek risk engine inside DA.  
- Continuous mark-to-market of LEAPs as capital_base every bar (unless later explicit).  
- L3 place_order.  
- Treating broker account balance dump as capital SoT.

## Acceptance

### Discovery / design

- [ ] Grill ratifies signal-path truth + link + exit reconcile (or documents alternative)  
- [ ] CONTEXT / business-context terms updated if law changes  
- [ ] Plan `trade-fulfillment-engine.md` D10 decision log updated  
- [ ] Schema sketch for fulfillment link + indicated vs applied delta  
- [ ] Worked example: 210 IBM signal → 2 LEAPs → exit → ±$D CashEvent  

### Implementation (after design acceptance)

- [ ] Persist fulfillment↔signal link with indicated capital delta  
- [ ] Exit (or explicit) reconcile produces proposed/applied CashEvent with audit  
- [ ] Specs: mid-life capital_base ignores packaging; post-reconcile reflects ±$D  
- [ ] Desk/MCP speech path for attach + reconcile  
- [ ] No DA symbol retarget to LEAP underlyings  

## Depends on / related

| Relation | Artifact |
|----------|----------|
| Plan | [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) §7 capital, Phase 1 D10 |
| L1 intake | [`2026-07-21-broker-confirmation-email-api-intake.md`](2026-07-21-broker-confirmation-email-api-intake.md) |
| Grill | [`2026-07-22-grill-fulfillment-schwab-extra-modal.md`](2026-07-22-grill-fulfillment-schwab-extra-modal.md) — include this model |
| Extra-modal law | CONTEXT Extra-Modal Fulfillment / Fulfillment Packaging — **may need amendment** |
| LEAP book path today | MCP related-instrument confirm (partial; cash×100 today may **conflict** — reconcile with this ticket) |
| CashEvent | `wv2_add_cash_event` / `CashEventService` — adjustment type for applied ±$D |
| Single fulfillment / amend | archive `2026-07-22-single-fulfillment-invariant-and-post-confirm-amend` |

## Notes / open questions (for grill)

1. Is reconcile **only** on full exit, or also on partial pyramid closes / rolls?  
2. May operator **apply** indicated ±$D mid-life with force?  
3. How does today’s LEAP `fulfillment_type` cash×multiplier path coexist until this ships (deprecate vs dual-mode)?  
4. Paper OPs: same model or paper always pure signal economics with no fulfillments?

## Implementation notes

- Prefer **indicated** vs **applied** delta states so L1 can attach evidence early.  
- Reconcile should be Human-Gated v1 (propose → confirm).  
- Keep Signal Spine immutable; adjustments are CashEvents + audit, not rewrite of historical signal size story.
