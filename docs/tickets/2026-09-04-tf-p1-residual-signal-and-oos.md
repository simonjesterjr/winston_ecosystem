# Ticket: P1 — Residual signal proof and true out-of-sample

**Status:** Proposed  
**Priority:** P1 — science layer under the existing lab factory; blocks honest Capital Activation  
**Date:** 2026-09-04  
**Monolith:** WUT first (harness + persist on Portfolio Backtest Run); gates then handoff  
**Principle:** Shannon / Simons — does this channel still have signal?  
**Page:** `winston_foundations/20260904/01-the-signal-problem.md`  
**Parent:** [`2026-09-04-tf-foundations-competency-epic.md`](2026-09-04-tf-foundations-competency-epic.md)

## Problem

Winston Unit Test (WUT) ranks Trend Following combinations with `practical_sharpe_ratio` on the same equity path used to pick the winner. Viability Gates (return ≥ 0, max drawdown ≤ 50%, ≥ 20 trades) are **placeholders**. Two-phase vet screens the last 25% of the **same** overlap, then re-scores the winner on **full history including that 25%**. Walk-forward is named as optional (confirm C03; One-Way Dynamic Close) and is **not a harness**. Bake-off v1 ran 55 cells; confirm matrix 20; no deflated Sharpe, no bootstrap, no scrambled-return Monte Carlo.

Repo “capacity” means heat slots, not Shannon channel capacity. No rolling Sharpe-by-decade on a **frozen** fingerprint.

## Desired outcome

A **measurement layer** under the factory we already have — not a new indicator zoo.

1. **Residual-signal pack** on a frozen fingerprint + frozen membership: bootstrap / scramble of daily or trade returns vs 0; persist on the Portfolio Backtest Run (PBR) / TradingStrategy Selection. Do **not** use as a ranking metric until pre-registered.  
2. **True walk-forward / embargo:** train `[t0, t1)`, validate `[t1, t2)`, roll. Screening last-25% must not count as out-of-sample. First two frozen recipes: confirm C03 (Blue EMA20 hard) and Turtle Mint System 2.  
3. **Deflated Sharpe or Bonferroni** on any grid ≥ N cells (bake-off and confirm matrices are the motivating evidence).  
4. **Edge Persistence** monitor: time-decay of the *same* fingerprint (full sample vs post-GFC vs last 3y). New term — do not overload “capacity.”  
5. **Additive** out-of-sample clause on export (fail when in-sample ≫ out-of-sample). Do **not** reopen first-pass doctrine / retune the 0% / 50% / 20-trade placeholders (closed as operator dead end 2026-09-04). Those remain ruin/activity labels.

## Must preserve

- Closed strategy zoo (no LLM-invented formulas)  
- One-axis experiments; no joint re-grid of entry × confirm × ladder × Kelly  
- Winston Quiver remains a different channel; its CAGR never enters `portfolios:vet_trend`  
- ADR-006 fingerprint freeze  

## Out of scope

- Live Kelly promotion  
- Evolution Mode  
- New entry classes  

## Acceptance

- [ ] Walk-forward harness exists as a WUT service/script (not a docs wish)  
- [ ] Mint S2 and confirm C03 have persisted out-of-sample packs  
- [ ] Bake-off-scale grids report a multiple-testing haircut  
- [ ] `TradeReadyViabilityGates` either stays explicitly “placeholder” or gains an OOS clause  
- [ ] CONTEXT glossary gains **Edge Persistence** (distinct from Unit Heat / Spending Capacity)  

## Related existing work (finish or cite, don’t clone)

- `docs/business-context/trade-ready-viability-gates.md`  
- `docs/tickets/archive/2026-07-09-first-pass-doctrine-gates-review.md` (closed 2026-09-04 — do not retune placeholder gates; this ticket adds an **out-of-sample clause**, it does not reopen first-pass doctrine)  
- `business_analysis/2026-07-18-confirmational-entry-experiment.md` (walk-forward named)  
- `docs/tickets/2026-07-25-strategy-bakeoff-v1-phase1.md`  
- ADR-008 rejected joint re-grid  

## Promote to plan when

Accepted and scoped as cross-monolith (WUT persist + Wv2 observation kill rules) → `ecosystem/plans/tf-residual-signal-and-walk-forward.md`.
