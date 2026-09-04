# Tracker: Trend Following six-principles competency

**Status:** Proposed (program)  
**Priority:** P2 as a program — does not preempt P0 capital/data tickets already in flight  
**Date:** 2026-09-04  
**Kind:** Parallel work graph for architecture and plans. Not a defect bucket.

**Analysis (narrative, one page per principle):**  
`/home/johnkoisch/Documents/com/typewriter/librarian/koisch-jr/winston_foundations/20260904/`

**Ecosystem pointer:** [`docs/analysis/2026-09-04-tf-six-principles-competency.md`](../analysis/2026-09-04-tf-six-principles-competency.md)

---

## How to use this tracker

1. Read the librarian page for the principle.  
2. Open the **principle ticket** below — that ticket owns *new* architecture.  
3. Finish **existing tickets** it cites before inventing a second plan.  
4. Promote irreversible choices to ADRs; promote build slices to child tickets.  
5. Do not start Evolution Mode from this tracker.

## Program tickets (this session)

| Pri | Status | File | Owns |
|-----|--------|------|------|
| P2 | Proposed | [`2026-09-04-tf-foundations-competency-epic.md`](2026-09-04-tf-foundations-competency-epic.md) | Program charter |
| P1 | Proposed | [`2026-09-04-tf-p1-residual-signal-and-oos.md`](2026-09-04-tf-p1-residual-signal-and-oos.md) | Shannon: residual signal, walk-forward, deflated Sharpe |
| P2 | Proposed | [`2026-09-04-tf-p2-tails-ruin-and-uncertainty.md`](2026-09-04-tf-p2-tails-ruin-and-uncertainty.md) | Mandelbrot / Knight: ruin metrics, crisis corr, Sharpe demotion |
| P1 | Proposed | [`2026-09-04-tf-p3-live-sizing-and-capital-authority.md`](2026-09-04-tf-p3-live-sizing-and-capital-authority.md) | Kelly / Thorp: Risk Capital into the sizer |
| P2 | Proposed | [`2026-09-04-tf-p4-compounding-and-champion-freeze.md`](2026-09-04-tf-p4-compounding-and-champion-freeze.md) | Hamming: sit-vs-kill, CAGR, auto-paper twin |
| P1 | Proposed | [`2026-09-04-tf-p5-desk-discipline-completion.md`](2026-09-04-tf-p5-desk-discipline-completion.md) | Feynman: finish the desk (do not rewrite doctrine) |
| P2 | Proposed | [`2026-09-04-tf-p6-map-territory-and-model-death.md`](2026-09-04-tf-p6-map-territory-and-model-death.md) | Derman / Lo: shelf-life, extra-modal, cadence honesty |

## Already in flight (do not duplicate)

These predate this tracker and **are** competency work. Link, don’t clone.

| Layer | Existing ticket | Why it belongs |
|-------|-----------------|----------------|
| 6 / 2 | [`2026-08-22-corporate-action-stop-safeguards.md`](2026-08-22-corporate-action-stop-safeguards.md) **P0** | Reverse-split territory (Mint PBR 533 ruin) |
| 6 | [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md) **P0** | Scored Session vs Not Scored |
| 6 | [`2026-08-22-observe-friday-scored-session-dar.md`](2026-08-22-observe-friday-scored-session-dar.md) | Live Friday proof of ADR-012 |
| 3 / 5 | [`2026-09-01-wv2-unit-heat-slate-contest.md`](2026-09-01-wv2-unit-heat-slate-contest.md) | Heat is in Daily Analysis; Slate Contest is not |
| 6 | [`2026-09-01-adr-009-resting-slate-addendum.md`](2026-09-01-adr-009-resting-slate-addendum.md) | Do not mix next-open score with resting live |
| 6 | [`2026-09-01-fulfillment-packaging-policy-ops-ui.md`](2026-09-01-fulfillment-packaging-policy-ops-ui.md) | Extra-modal accounting |
| 5 | [`2026-07-20-dar-real-process-miss-attention.md`](2026-07-20-dar-real-process-miss-attention.md) | Process miss must outrank paper noise |
| 5 | [`2026-07-20-wv2-capacity-swap-desk-packages.md`](2026-07-20-wv2-capacity-swap-desk-packages.md) | Deterministic handoff, not expected-return menus |
| 4 | [`2026-07-26-bakeoff-scorecard-cagr-calmar.md`](2026-07-26-bakeoff-scorecard-cagr-calmar.md) | Compounding metrics |
| 3 | [`2026-07-30-kelly-martingale-sizing-portfolio-management.md`](2026-07-30-kelly-martingale-sizing-portfolio-management.md) | Kelly lab → eventual ops (not global default) |
| 3 | [`2026-08-09-kelly-mango-wk66-fingerprint-paper.md`](2026-08-09-kelly-mango-wk66-fingerprint-paper.md) | Kelly observation only |
| 4 / 6 | [`2026-07-19-loop-engineering-evolution-mode.md`](2026-07-19-loop-engineering-evolution-mode.md) | Evolution **after** closed-system verify |
| 1 | Confirm C03 walk-forward (named in BA, **no prior ticket**) | Owned now by P1 residual-signal ticket |
| 1 | [`archive/2026-07-09-first-pass-doctrine-gates-review.md`](archive/2026-07-09-first-pass-doctrine-gates-review.md) | Closed 2026-09-04 as operator dead end — **do not retune** first-pass gates; P1 adds out-of-sample measurement, not a doctrine rewrite |

## Suggested plan promotions (later, not this session)

When a principle ticket is accepted, promote to `ecosystem/plans/` only if the work is cross-monolith and design-heavy:

- `plans/tf-residual-signal-and-walk-forward.md` (from P1)  
- `plans/tf-capital-authority-sizer.md` (from P3)  
- `plans/tf-fingerprint-shelf-life.md` (from P6)  

Do not write those plans until the operator accepts this tracker.
