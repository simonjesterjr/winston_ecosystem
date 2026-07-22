# ADR-007: Portfolio Correlation Score — WUT System of Record

**Status:** Accepted  
**Date:** 2026-07-11  
**Deciders:** Architecture (via `/grill-with-docs`)  
**Builds on:** ADR-001, ADR-006  
**Plan:** `plans/portfolio-correlation-methodology-and-score.md`  
**Glossary:** `CONTEXT.md` — Portfolio Correlation Score, Correlation Snapshot, Correlation Methodology Version, Daily Activity Report

## Context

Operator surfaces (WUT builder, PBR metadata, handoff JSON, Wv2 **Daily Activity Report**) need a transparent, comparable measure of portfolio membership diversification. Naive mean pairwise \|r\| can look “strong” while high-correlation twins exist (e.g. DBE/OILK). Computing divergent formulas in WUT vs Wv2 would poison the time series. Ops must not auto-mutate **Engaged** Books when the score degrades (ADR-006 **Rebalance**).

Alternatives considered:

- **A. Parallel formula in WUT and Wv2** — simple independence; drift risk  
- **B. Shared gem** — DRY; couples release cycles  
- **C. WUT SoT + Wv2 client** — single compute path; ops depends on lab availability for refresh  

## Decision

We choose **C: WUT is the system of record for Portfolio Correlation Score (PCS)**.

1. **PCS** is a versioned 0–100 score; **primary driver is max pairwise \|r\|** (and high-pair count); mean \|r\| is secondary.  
2. **Correlation Methodology Version** (e.g. `corr_v2`) freezes formula, windows, quality gates, and build max-pairwise cap. New recipe → new version; history is not rewritten.  
3. **WUT** computes and stores **Correlation Snapshots** (time series) for **registry color portfolios**. A scheduled job runs after DM data readiness.  
4. **Handoff JSON** may embed a baseline snapshot.  
5. **Wv2** does not recompute a parallel formula. A **WUT client** fetches latest/history when **Daily Activity Report** or other tasking needs PCS. Optional thin cache for resilience only.  
6. Identity match: primarily **seed_name** (lab portfolio name / export `name`); fingerprint disambiguates multiple OP forks.  
7. PCS degradation **flags** review in DAR / next_steps only — never silent Books mutation or auto-successor.  
8. **Daily Activity Report** overview includes PCS **numeric time series and chart** from first ship (chart may degrade to table-only if data missing).

## Consequences

- WUT internal API + snapshot table become part of the ops report path (availability and versioning matter).  
- Registry membership defines what gets daily scored (not Wv2 Active alone).  
- Orange/White membership issues are handled by **archiving** and building new cohorts (Green/Pink/Mango/Rust), not by dual-scoring divergent books without methodology upgrade.  
- Six common lab↔ops portfolios intended: Red, Blue, Green, Pink, Mango, Rust.

## Rejected

- Auto-rebalance on PCS breach (violates ADR-006 engagement lock).  
- Mean-only score as SoT (dilution failure mode).  
- Wv2-only daily recompute without WUT (divergent science).
