# Ticket: P5 — Desk discipline completion (do not rewrite doctrine)

**Status:** Proposed  
**Priority:** P1 — doctrine is load-bearing; hatches are still quiet  
**Date:** 2026-09-04  
**Monolith:** Wv2 desk / DAR / Daily Analysis  
**Principle:** Feynman / Livermore / Marks  
**Page:** `winston_foundations/20260904/05-the-discipline-problem.md`  
**Parent:** [`2026-09-04-tf-foundations-competency-epic.md`](2026-09-04-tf-foundations-competency-epic.md)

## Problem

Layer 5 is the principle Winston **already manages well**: Daily Analysis never fills (ADR-009), Signaled Entry Rule, Unsignaled Exit Allowance, Passed Signal taxonomy, attention bands, anti-overfit lab doctrine, ADR-012 honesty.

The remaining failure mode is Feynman through **designed hatches**: confirm may change units/price/packaging; force enter; soft-warn Capital Activation; Working Stop edits; stop-out warns rather than blocks. Process miss is the dominant Mid-month Scoreboard drag, and **DAR real-band process-miss attention is still Proposed**. Daily Analysis sorts adds by **−ATR**, not Turtle Slate Contest. Size delta vs Signal Spine has no dedicated audit.

This ticket does **not** invent a new discipline philosophy. It **finishes the desk**.

## Desired outcome

1. Finish [`2026-07-20-dar-real-process-miss-attention.md`](2026-07-20-dar-real-process-miss-attention.md) — Active-real process miss outranks paper noise.  
2. Finish [`2026-07-20-wv2-capacity-swap-desk-packages.md`](2026-07-20-wv2-capacity-swap-desk-packages.md) — one deterministic Desk Handoff, not expected-return menus.  
3. Finish Slate Contest half of [`2026-09-01-wv2-unit-heat-slate-contest.md`](2026-09-01-wv2-unit-heat-slate-contest.md) (heat refuse is already in Daily Analysis).  
4. **New:** warn/audit when booked units ≫ Signal Spine size (packaging can differ; silent 3× share count cannot).  
5. Two-phase vet + holdout as the **export path**, not docs-only (shared with P1; this ticket owns the Feynman framing).  
6. HITL vs auto-paper twin so operator drag is measurable (shared with P4 / loop-engineering V1–V2).

## Must preserve

- ADR-009 human-gated boundary (Daily Analysis never opens Positions)  
- Desk Pass requires a reason and never waives capacity  
- LLM is not the entry engine  
- Extra-modal packaging remains allowed; the audit is **size honesty**, not “shares only”  

## Out of scope

- Whole-slate accept-fill (later grill; existing P3 ticket)  
- Rewriting Passed Signal taxonomy  
- Autotrader  

## Acceptance

- [ ] The three existing P1/P2 desk tickets above are Done, merged, or explicitly re-prioritized with owner  
- [ ] Booked-vs-signal size delta surfaces on desk confirm and DAR when over a named threshold  
- [ ] No new “discipline framework” doc that restates ADR-009  

## Related existing work

- ADR-009, Principle 12  
- `docs/business-context/human-gated-desk-and-fulfillment.md`  
- MMS scorer / findings (process fidelity vs desk discipline)
