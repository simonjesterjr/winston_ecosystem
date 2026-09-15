# Plan: Wv2 + BG + IBKR LEAP packaging (Model B)

**Status:** Draft for operator lock / multi-party coordination  
**Date:** 2026-09-14/15  
**Mode:** contractor pickup  
**Monoliths:** Winston v2 (Wv2), Broker Gateway (BG), Client Portal Gateway (CPGW) via IBKR adapter; WUT only as sizing skeleton  
**Authoritative for:** Implementation sequence of LEAP extra-modal fulfillment on paper DUT (geometry B + Model B precalc OCC)  
**Does not invent domain law:** Domain rules live in [`docs/business-context/leap-extra-modal-proxy.md`](../docs/business-context/leap-extra-modal-proxy.md); sticky 20D_BO in [`turtle-s2-pyramid-and-working-stop.md`](../docs/business-context/turtle-s2-pyramid-and-working-stop.md)  
**Detailed inventory:** [`docs/analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md`](../docs/analysis/2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md) (phases, code pointers, grill questions — do not re-derive)  
**Parent plan:** [`spending-capacity-and-leap-fulfillment.md`](spending-capacity-and-leap-fulfillment.md) (SC before LEAP send; prefer LEAP cash outlay)  
**Decision record:** [`docs/adr/ADR-017-leap-packaging-precalc-occ.md`](../docs/adr/ADR-017-leap-packaging-precalc-occ.md) (Proposed — Model B)  
**Related tickets:** [`2026-09-09-extra-modal-leap-unit-evaluation.md`](../docs/tickets/2026-09-09-extra-modal-leap-unit-evaluation.md) (P1 read-only 1×1); [`2026-09-15-wv2-leap-packaging-fields.md`](../docs/tickets/2026-09-15-wv2-leap-packaging-fields.md); [`2026-09-15-bg-ibkr-opt-order-intent-prove.md`](../docs/tickets/2026-09-15-bg-ibkr-opt-order-intent-prove.md)

---

## Parties (one trail)

| Party | Role on this plan |
|-------|-------------------|
| **Operator (John)** | Lock grill answers; Desk Send on paper DUT only; accept/reject ADR-017 |
| **Grok Bot (Chief of Staff)** | Lab stamps, session reports, cross-link hygiene, coordination stamps — **never** Desk-Sends options |
| **Grok CLI** | Monolith code (Wv2 / BG) against this plan + ADR after grill |

Do **not** fork a second LEAP design in session drafts. Promote here; link analysis + business-context.

---

## Explicit gates (non-negotiable)

- **`/grill-with-docs` before any option Desk Send** — lock cash flip, Model B, stop HITL, stale-strike refuse (not silent re-ATM).
- **Paper DUT only** — no live IBKR / Schwab `order_write`.
- **No pack promotion** / mv2 Capital Activation / paper→real in-place (ADR-006).
- **Agent never Desk-Sends** options (ADR-009 / ADR-013).
- **SC Check + tradable 1×1** before first paper LEAP send (parent plan Part 1 + ticket 2026-09-09).

---

## One-sentence outcome

Paper DUT can **Desk Send one LEAP** as the fulfillment command for an underlying Trend Following signal, with Working Stop / sticky 20D_BO still evaluated on the **underlying**, sell-to-close of the option as **HITL** on stop-out, and Accept-Fill at the **option print**.

---

## Law vs inventory vs this plan

| Artifact | Authority |
|----------|-----------|
| `leap-extra-modal-proxy.md` | **Domain law** — signal Market vs packaging; dual spines; HITL sell LEAP on stop |
| `turtle-s2-pyramid-and-working-stop.md` | Sticky 20D_BO Working Stop (not doctrine A) |
| ADR-009 / ADR-013 | Human-gated desk; paper DUT write; extra-modal Guardrail = HITL |
| ADR-017 (Proposed) | **Model B** — precalc OCC at Signal/slate; Send verifies conid; no silent re-ATM |
| Analysis `2026-09-15-…` | Detailed inventory, code pointers, Model A vs B table, open grill ≤6 |
| **This plan** | Authoritative phased implementation + party coordination |

---

## Phases (summary — detail in analysis)

Gates between phases: paper DUT only; kill switch / `cap_order_write`; no live write; no agent Desk-Send of options.

| Phase | Owner | Goal |
|-------|-------|------|
| **0 — Prerequisites** | Operator / existing tickets | SC Check on Walnut (premium cash); read-only CPGW 1×1 tradable; grill § answers; Exit Capital Reconcile path before capital-honest LEAP lot |
| **1 — Wv2 packaging fields** | Wv2 (Grok CLI) | Model B: stamp OCC / optional conid on handoff/slate; journal Market stays underlying; SC on premium × 100 × contracts — ticket `2026-09-15-wv2-leap-packaging-fields` |
| **2 — BG OPT Order Intent** | BG (+ Wv2 client) | Require `conid` when `asset_class=option`; never stock-biased resolve for OPT — ticket `2026-09-15-bg-ibkr-opt-order-intent-prove` |
| **3 — IBKR adapter OPT path** | BG `IbkrAdapter` | One paper LEAP MKT/LMT Submit → working → print (operator Desk Send) |
| **4 — Monitoring / reconcile** | Wv2 + BG poll | Accept-Fill on OPT print; Fulfillment Link; Exit Capital Reconcile; naked-LEAP attention |
| **5 — Stop-out HITL** | Wv2 desk | Underlying Working Stop pierce → HITL sell-to-close on packaged conid; no silent option STP |

Contractor slices S0–S5 and field tables: see analysis §§3–7.

---

## Recommendation locks (awaiting operator)

| Choice | Lock |
|--------|------|
| Fulfillment geometry | **B** — Desk-Sent command is the LEAP |
| Contract timing | **Model B** — precalc OCC at Signal/slate; Send verifies; no silent re-ATM |
| Entry order | MKT default or LMT if quote width demands; no option STP protective |
| Stop-out | Underlying Working Stop + sticky 20D_BO; **HITL** sell LEAP |
| IBKR LEAP MKT | Supported on CPGW with explicit OPT conid |

---

## Non-goals

- Multi-leg OMS / spreads as first-class Positions  
- Pack promotion / Capital Activation by this plan  
- Silent option STP or stock STP “filled as LEAP” (geometry A)  
- Treating WUT Black-Scholes as live cheap/expensive  
- TWS + CPGW `compete:true` on the same paper username  
- Live IBKR or Schwab write  
- Slate Automation of unsent entries  
- New Trading Strategy fingerprint solely for packaging (unless Unit Heat occupancy changes — then grill)  
- Wv2/BG **code** in the filing session that minted this plan — implementation starts after grill + tickets

---

## Next concrete steps

1. Operator: `/grill-with-docs` on ADR-017 + this plan (or accept Proposed → Accepted).  
2. Parallel: paper read-only 1×1 (`2026-09-09-extra-modal…`) **or** start Phase 1 ticket `2026-09-15-wv2-leap-packaging-fields`.  
3. Do not Desk-Send OPT until SC + matrix + grill locked.
