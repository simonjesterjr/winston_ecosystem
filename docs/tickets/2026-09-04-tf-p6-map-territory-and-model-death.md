# Ticket: P6 — Map vs territory and model death

**Status:** Proposed  
**Priority:** P2 — dual-spine law exists; shelf-life and extra-modal math do not  
**Date:** 2026-09-04  
**Monolith:** cross (DM parquet truth, Wv2 spines, later Evolution)  
**Principle:** Derman / Bernstein / Lo Adaptive Markets  
**Page:** `winston_foundations/20260904/06-the-reality-problem.md`  
**Parent:** [`2026-09-04-tf-foundations-competency-epic.md`](2026-09-04-tf-foundations-competency-epic.md)

## Problem

Winston already encodes map ≠ territory: Signal Spine vs Booked Capital Spine, extra-modal as normal, ADR-012 Not Scored ≠ Hold, DM reconciliation, three independent passport axes (export_kind / Active / Execution Mode).

Leaks:

- Unadjusted reverse splits (Mint PBR 533 ruin) — **P0 already in flight**  
- Extra-modal law without Exit Capital Reconcile / Risk Modality applied math  
- Lab next-open vs live resting **Session Order Slate** (ADR-009 addendum Proposed)  
- No fingerprint **shelf-life**; Lo’s “adapt before the market kills the old one” is manual successor  
- Evolution Mode is Proposed; jumping there now is the industry failure mode (argue layer one)  
- Soft-warn Capital Activation lets the operator travel without the passport stamp  

## Desired outcome

1. **Do not duplicate P0.** Corporate-action parquet + stop safeguards + scored-session Friday proof remain first. This ticket **depends** on them.  
2. Finish packaging UI + **Exit Capital Reconcile** + **Risk Modality** so the booked spine is household-cash honest.  
3. ADR-009 addendum: next-open stays lab default until a fingerprint is **scored on resting-touch**. Do not run live slate against a next-open recipe.  
4. **Model death / shelf-life:** time-boxed certificate (fingerprint + window + export_kind + last PCS + last scored drawdown) → auto **observation** (deactivate or flag) when live path violates lab drawdown or PCS high-pair regime. **Still no silent Books mutation.**  
5. Evolution Mode only after loop-engineering V1–V2 closed-system verify.  
6. Knightian overlay from P2 is how Bernstein’s “show up tomorrow” is implemented.

## Must preserve

- Dual spines; extra-modal fulfillment as normal  
- ADR-006 successor (shelf-life flags; it does not auto-rebalance membership)  
- Deterministic StrategyRegistry; no LLM-authored entries  
- Turtle “don’t mix fill cadences”  

## Out of scope

- Whole-slate accept-fill  
- Measuring “our AUM changed the market” (small-capital TF; Edge Persistence on P1 is the in-band proxy)  
- Replacing EOD human-gated frequency with Medallion trial-count  

## Acceptance

- [ ] P0 split and ADR-012 Friday tickets not blocked by this one  
- [ ] Shelf-life doctrine drafted (business-context or ADR-006 addendum)  
- [ ] Packaging reconcile has an implementation ticket or is merged with `2026-09-01-fulfillment-packaging-policy-ops-ui.md`  
- [ ] ADR-009 addendum accepted or explicitly deferred with the mixing-cadence prohibition restated  
- [ ] Evolution Mode remains unscheduled until V1–V2  

## Related existing work

- P0 `2026-08-22-corporate-action-stop-safeguards.md`  
- P0 `2026-08-18-eodhd-lag-retry-after-close.md`  
- `2026-08-22-observe-friday-scored-session-dar.md`  
- `2026-09-01-adr-009-resting-slate-addendum.md`  
- `2026-09-01-fulfillment-packaging-policy-ops-ui.md`  
- `2026-07-19-loop-engineering-evolution-mode.md`  
- ADR-006, ADR-009, ADR-012  
- `plans/winston-plus-llm.md` (LLM augments; never replaces StrategyRegistry)  

## Promote to plan when

Shelf-life + cadence honesty accepted as cross-monolith → `ecosystem/plans/tf-fingerprint-shelf-life.md`.
