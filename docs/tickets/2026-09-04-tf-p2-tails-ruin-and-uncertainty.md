# Ticket: P2 — Tails, ruin functionals, and Knightian uncertainty

**Status:** Proposed  
**Priority:** P2 — science + ranking doctrine; P0 split work stays first  
**Date:** 2026-09-04  
**Monolith:** WUT (PBR metrics, ranker) + Wv2 (MMS, snapshot radar)  
**Principle:** Mandelbrot / Knight / Box  
**Page:** `winston_foundations/20260904/02-the-distribution-problem.md`  
**Parent:** [`2026-09-04-tf-foundations-competency-epic.md`](2026-09-04-tf-foundations-competency-epic.md)

## Problem

Winston sizes on Average True Range (ATR) units and refuses correlated occupancy (Unit Heat). That is anti-Gaussian **geometry**. The **science layer** is still second-moment: practical Sharpe as default ranker, Pearson Portfolio Correlation Score (PCS), conjugate-normal expected return, Black–Scholes marking, live snapshot **drops moves > 8 ATR** as bad quotes.

Heat counts lots, not dollar tail. Frozen Pearson is blind on the Tuesday pairwise r jumps toward 1. There is no named distinction between **risk** (ATR, heat) and **uncertainty** (missing bars, split-like print, unscored session, unknown pair). Fingerprints have lineage (Box-adjacent) without **shelf-life** (owned on P6).

Ruin has been **scored as experiments** (S4 $20k, Martingale 98.8% drawdown, Mint PBR 533) and not promoted into stored path functionals (min equity, time under water, worst streak).

## Desired outcome

1. **Ruin functionals** on every PBR and Mid-month Scoreboard: min equity, time under water, worst streak — not just max drawdown.  
2. **Demote Sharpe** as default `RANKING_METRIC`. Calmar / min-equity / max drawdown as primary **gates**; Sharpe display-only with a fat-tail disclaimer. Complements (does not replace) the CAGR/Calmar scorecard ticket.  
3. **Crisis-correlation overlay** (e.g. 2020-Q1 / 2022), versioned like `corr_v2`, **without** silent daily refit. L2/L3 heat may read it as a stress vintage.  
4. Live tail sensor that **does not drop 8N+** moves; distinguish quote garbage from genuine gaps / split-like ratios.  
5. **Knightian capital policy** (doctrine + skip behavior): uncertainty → do not size, do not Hold-as-quiet, do not Kelly. Partial pieces (ADR-012, `CORPORATE_ACTION_HOLD`) become one named policy.  
6. Optional later: gap-adjusted unit or crash cap **orthogonal** to L1–L4 occupancy.

## Must preserve

- ATR-17 as N (do not replace range units with σ)  
- Unit Heat occupancy (Faith table)  
- PCS as WUT system of record (ADR-007); no parallel Wv2 formula  
- No auto-successor on PCS breach (ADR-006)  

## Out of scope

- Implementing split-adjusted parquet (existing P0 `2026-08-22-corporate-action-stop-safeguards.md`)  
- Slate Contest (existing `2026-09-01-wv2-unit-heat-slate-contest.md`)  
- Fingerprint shelf-life (P6)  

## Acceptance

- [ ] PBR results persist at least min-equity + time-under-water  
- [ ] Documented ranker change (or an ADR that Sharpe remains display-primary with rationale)  
- [ ] Snapshot radar no longer silently omits >8 ATR as the only tail path  
- [ ] CONTEXT names **risk vs uncertainty** actions  
- [ ] Crisis-corr vintage design accepted (implementation may follow a plan)  

## Related existing work

- P0 `2026-08-22-corporate-action-stop-safeguards.md` / issue `2026-08-22-unadjusted-reverse-split-jumps.md`  
- `docs/tickets/2026-07-25-strategy-bakeoff-v1-phase1.md` (Sharpe trap)  
- `docs/tickets/2026-07-26-bakeoff-scorecard-cagr-calmar.md`  
- `docs/analysis/2026-08-22-mint-resting-stop-touch-ruin.md`  
- `docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md` (ruin DD named, not stored)
