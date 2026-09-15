# LEAP extra-modal proxy — underlying signal ↔ option packaging

**Type:** Domain / trading rules (Fulfillment Packaging)  
**Applies to:** Trend Following Operational Portfolios (OPs) and Winston Unit Test (WUT) lab recipes that fulfill equity **signals** with Long-term Equity Anticipation Security (LEAP) / option **packaging** as a proxy for the underlying. First lab chassis: Resting Stop Touch (RST) + Turtle S2 sticky 20D_BO.  
**Status:** Desk lock for Wv2 planning 2026-09-14/15 (promotes lab law from WUT LEAP-packaged PBR work).  
**Glossary:** `CONTEXT.md` — Extra-Modal Fulfillment, Fulfillment Packaging Policy, Signal-Path Operational Lot, Risk Modality, Fulfillment Link, Exit Capital Reconcile, Working Stop, Protective Stop Guardrail, Signal Spine, Booked Capital Spine  
**Related:** [`human-gated-desk-and-fulfillment.md`](human-gated-desk-and-fulfillment.md); [`turtle-s2-pyramid-and-working-stop.md`](turtle-s2-pyramid-and-working-stop.md); [`wut-s2-working-stop-lab.md`](wut-s2-working-stop-lab.md); ADR-009; ADR-017 (Proposed); plans `spending-capacity-and-leap-fulfillment.md`, `wv2-bg-ibkr-leap-fulfillment.md`; tickets `2026-09-09-extra-modal-leap-unit-evaluation.md`, `2026-09-15-wv2-leap-packaging-fields.md`, `2026-09-15-bg-ibkr-opt-order-intent-prove.md`, WUT `2026-09-14-wut-leap-packaged-pbr-faithful-sim.md`

## Purpose

State the **non-negotiable split** between:

1. **Methodology / Trading Strategy (TS)** — what the Book signals on the **underlying Market** (entry, pyramid, **exit recipe**, Working Stop geometry, heat).  
2. **Fulfillment Packaging** — how the desk (or lab) **books cash** when the fill is a LEAP/option (or other extra-modal instrument) instead of shares.

This doc is the Wv2 handoff surface for “LEAP as proxy for the underlying.” It does **not** invent a second TS. If the TS has no exit strategy, there is no LEAP-proxy exit law to inherit — fix the fingerprint first.

## One-sentence law

**DA and the Working Stop stay on the underlying signal Market; cash, marks, and broker legs follow packaging; Exit Capital Reconcile makes household cash honest when packaging differed.**

## Assumptions (explicit)

| Assumption | Meaning |
|------------|---------|
| TS owns exits | Exit signal strategies (e.g. Breakout20Day / sticky 20D_BO path under S2) live on the **TS fingerprint**, not on the option OCC symbol. |
| Extra-modal is packaging | Confirm may change **Fulfillment Packaging** (shares → LEAP) while still referencing the same signal / direction / Book Market. |
| Dual spines | **Signal Spine** keeps share-unit methodology story; **Booked Capital Spine** keeps contracts × premium × multiplier. |
| Human-gated default | Live option Desk Send / CPGW quotes are a **later** fulfillment path; lab may use synthetic Black-Scholes premiums without claiming listed bid/ask truth. |

## Signal Market vs fill symbol

| Layer | Symbol / Market | Owns |
|-------|-----------------|------|
| Book / DA / PCS / heat | **Underlying** (signal Market on the Book) | Entries, pyramids, exits, Working Stop evaluation, unit occupancy |
| Broker / journal packaging | **OCC / LEAP** (or other related) | Cash outlay, premium marks, what is sold on stop-out HITL |
| Link | Fulfillment Link on the Journal | Joins signal ↔ packaged fill; never retargets the Book to the fill symbol |

**Do not** re-point Books, Daily Analysis, or correlation to the LEAP symbol. **Do not** treat the LEAP as a different methodology signal.

## What the TS still does (unchanged by LEAP packaging)

These remain **underlying** geometry from the TS / sticky 20D_BO law:

- Entry and pyramid **levels** (Donchian / ATR steps) on the underlying.  
- **Unit Heat** occupancy: one heat unit per lot (LEAP does not buy more heat room).  
- **Working Stop** phases (under-max 2N only; after max, sticky 20D_BO when 20d has passed last-entry 2N; pierce = flatten-all). See [`turtle-s2-pyramid-and-working-stop.md`](turtle-s2-pyramid-and-working-stop.md).  
- **Exit strategies on the TS** — including 20-day / channel recipes — are evaluated as the fingerprint says on the **underlying**. Packaging does not add a silent second Donchian on the option.

## What packaging changes

| Concern | Share fulfillment | LEAP / option packaging |
|---------|-------------------|-------------------------|
| Cash contest / affordability | Share notional (units × price) | **Contracts × premium × 100** (US equity option multiplier) |
| Booked entry identity | Shares @ underlying | `is_option` / premium / contracts; `extra_modal` on cash events |
| Pyramid reference price | Underlying fill | Still **underlying** fill for 1N add distance — not premium |
| Working Stop price | Underlying 2N / 20d | Same **underlying** stop level |
| Stop-out realization | Sell/cover shares at stop/gap rules | **Sell the packaged option** (HITL live; lab marks option). Broker stop on the option is **not** assumed unless packaging policy says so. |
| Protective Stop Guardrail | GTC stop-market on underlying (IBKR stock/ETF) | Stop **evaluated** on underlying; trigger → desk task to exit related fill ([`human-gated-desk-and-fulfillment.md`](human-gated-desk-and-fulfillment.md)) |

## Lab knobs (WUT) vs Wv2 policy (same meanings)

WUT stamps these on PBR `results_json` / market configs for faithful sims. Wv2 should treat them as **Fulfillment Packaging Policy** vocabulary, not as a second fingerprint:

| Knob | Meaning |
|------|---------|
| `leap_fulfillment=entry` | First unit packages as LEAP; later pyramids may be shares (policy choice). |
| `leap_fulfillment=all` | Every fill on the name packages as LEAP (lab breadth hypothesis). |
| `leap_atr_offset` | Strike offset in ATR units (0 = ATM; must not be treated as Ruby falsy). |
| `leap_expiration_days` | Target tenor (lab often 730). |
| Contract floor | Sizing floors at 1 contract (100 shares controlled); small 1% units on cheap names may skip. |

**Fingerprint honesty:** changing `leap_fulfillment` (or live packaging policy) is a **new recipe** relative to share bake-offs — do not silently rewrite historical share-path Edge as LEAP Edge.

## Risk modalities (read in parallel)

Same open lot may be viewed several ways (CONTEXT **Risk Modality**):

1. **Signal-path share units** — DA draft size / heat / methodology audit.  
2. **Cash-at-risk** — premium × contracts × multiplier.  
3. **Underlying per-share** — Working Stop distance in underlying price.  
4. **Option structure** — calls/puts, strike, expiry (desk / later OMS).

DA still drafts pyramid size from (1). Packaging chooses how that add is filled.

## Marks and Edge (lab vs live)

| Context | Mark / Edge rule |
|---------|------------------|
| WUT classic `equity_history` | Must **not** pretend open LEAPs are `underlying × units × 100` share MTM for path/DD ranking — that invents cliffs. Prefer **option-aware** (Black-Scholes) equity alongside classic. |
| WUT LEAP Edge / PF | **Not share-R-comparable.** Rank within LEAP packaging only. |
| Wv2 mid-life | Prefer **indicate** packaging gap; do not continuously rewrite `capital_base` to LEAP MTM unless product says so. |
| Wv2 exit | **Exit Capital Reconcile** applies CashEvent so household cash matches **actual fulfillment profit**, not the signal-path proxy (CONTEXT worked example: IBM shares vs 2 LEAP calls). |

## Exit path (TS exit + packaging)

```
TS exit / Working Stop pierce fires on UNDERLYING
        │
        ├─ Signal Spine: signaled exit / stop-out (methodology)
        │
        └─ Fulfillment:
              shares packaging  → sell/cover shares (slate / broker / dummy_sim)
              LEAP packaging    → HITL (or policy-automatic later) sell option legs
                                   lab: mark option (BS); live: broker print / CPGW when ready
        │
        └─ Exit Capital Reconcile (Wv2): CashEvent if packaged PnL ≠ signal-path PnL
```

**Sticky 20D_BO / under-max silence** are **TS Working Stop** rules. They do not move to the OCC symbol. Under RST S2 lab, under-max 20-day channel closes stay suppressed; pierce of the Working Stop flattens packaged lots via the option mark path.

## What this is not

- **Not** a LEAP-only Trading Strategy (no underlying Book).  
- **Not** permission to evaluate 20-day / Donchian on the option chart.  
- **Not** listed bid/ask truth when the lab uses Black-Scholes.  
- **Not** multi-leg OMS as first-class Positions (still deferred in ADR-009 non-goals).  
- **Not** pack promotion / mv2 capital activation by itself — packaging law only.  
- **Not** doctrine A (`max(2N, 20d)` always) — sticky 20D_BO remains Working Stop law.

## Wv2 implementation checklist (non-normative)

| Capability | Lab (WUT) | Wv2 target |
|------------|-----------|------------|
| Extra-modal Confirm + Fulfillment Link | Partial / journals | Required for LEAP proxy OPs |
| Working Stop on underlying + HITL option exit | Spec-locked in LEAP PBR path | Desk task + guardrail (exists in principle) |
| Cash contest on premium outlay | Built for LEAP PBR | Desk sizing / slate must not use share notional for packaged adds |
| Exit Capital Reconcile CashEvent | Not WUT’s job | Required for real/paper honesty at exit |
| Option-aware path/DD | `option_aware_equity_history` | DAR / Score Projection: do not rank LEAP OPs on share-MTM cliffs |
| CPGW / Desk Send options | Out of lab recipe | Separate ticket (`2026-09-09-extra-modal-leap-unit-evaluation.md`) |

## Related reading (evidence, not law)

- Session: `docs/session-reports/2026-09-14-1001-wut-leap-packaged-pbr.md`, `docs/session-reports/2026-09-14-2330-leap-proxy-law-and-wv2-bg-plan.md`  
- Analysis: `docs/analysis/2026-09-09-extra-modal-leap-unit-vs-shares.md`, `2026-09-14-pbr676-oa-vs-672-red-leap.md`, `2026-09-15-wv2-bg-ibkr-leap-fulfillment-plan.md` (inventory)  
- Plan / ADR: `plans/wv2-bg-ibkr-leap-fulfillment.md`; `docs/adr/ADR-017-leap-packaging-precalc-occ.md`  
- Lab ticket: `winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md`
