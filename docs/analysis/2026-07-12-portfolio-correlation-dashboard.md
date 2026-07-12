# Portfolio Correlation Dashboard (WUT Portfolios tab)

**Date:** 2026-07-12  
**Status:** Design recommendation (Phase 6 follow-on)  
**Plan:** `plans/portfolio-correlation-methodology-and-score.md`

## Why yes

Heatmaps today live on **Portfolio Builder** (session draft) and **Correlation Calculator** (ad-hoc). Color cohorts need a **portfolio-centric** surface:

- Open **Portfolio Green** → see Books correlation health without re-selecting symbols  
- Compare **PCS rankings** across all color portfolios  
- Watch **PCS time series** (rebalance flag hygiene) without opening DAR JSON  

That matches ADR-007 (WUT SoT) and Phase 3 transparency without a second formula.

## Recommendation

Add a **Correlation** sub-nav under WUT **Portfolios** (not a separate top-level app):

| Route | Purpose |
|-------|---------|
| `GET /portfolios/correlation` | **Dashboard** — ranking table + multi-PCS chart |
| `GET /portfolios/:id/correlation` | **Portfolio detail** — heatmap, matrix, high pairs, quality flags, PCS history |

Keep Portfolio Builder for *assembly*; dashboard for *monitoring* existing books.

## Dashboard layout (index)

1. **Ranking table** (sortable)  
   Portfolio · Seed · n · PCS · Max\|r\| · Mean\|r\| · High pairs · As-of · Rating  
   Pull latest `portfolio_correlation_snapshots` (+ registry seed).

2. **Multi-series PCS chart** (last 30–90 days)  
   Reuse Chart.js / Plotly pattern from PBR equity; one series per color portfolio.

3. **Flags strip**  
   Any max\|r\| > 0.70 or PCS drop ≥10 pts → amber cards with link to portfolio detail.

4. **Methodology footnote**  
   `corr_v2`, build cap 0.55, weak 0.70, max\|r\|-first PCS.

## Portfolio detail

- Existing shared partial: `shared/correlation_transparency_strip`  
- Heatmap + matrix (dual threshold colors from Phase 3)  
- Optional: **Rebuild correlation** button → `capture` snapshot for this portfolio’s Books (no membership change)  
- Link out: Builder (if reshaping), PBR runs, export JSON `correlation_snapshot`

## Data sources (already exist)

| Need | Source |
|------|--------|
| Latest PCS | `PortfolioCorrelationSnapshot` |
| History | same table (`as_of_date`) |
| Live matrix | `MarketCorrelationCalculator` on Books |
| Registry seed / peers | `PortfolioRegistry` |

No Wv2 dependency for this dashboard (WUT-only lab).

## Implementation sketch (1–2 sessions)

1. Controller `Portfolios::CorrelationController` (or actions on `PortfoliosController`)  
2. Index + show views; Chart.js for PCS series  
3. Nav link on Portfolios index + show  
4. Specs: snapshot ranking query, empty portfolio edge  
5. Optional Sidekiq “refresh all visible” = call existing daily scorer  

## Explicit non-goals (v1)

- Live streaming tick correlations  
- Auto-rebalance from the UI  
- Replacing Portfolio Builder greedy flow  

## Decision

**Ship this.** It is the right home for “graphical visualization” after corr_v2 membership is locked — operator-facing, portfolio-scoped, and reuses the Phase 3–5 stack.
