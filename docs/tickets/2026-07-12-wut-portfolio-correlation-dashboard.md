# Ticket: WUT Portfolios tab — Correlation dashboard

**Status:** Proposed  

**Date:** 2026-07-12  

**Plan:** [`plans/portfolio-correlation-methodology-and-score.md`](../../plans/portfolio-correlation-methodology-and-score.md)  
**Design:** [`analysis/2026-07-12-portfolio-correlation-dashboard.md`](../analysis/2026-07-12-portfolio-correlation-dashboard.md)  
**ADR:** [`ADR-007`](../adr/ADR-007-portfolio-correlation-score-sot.md)

## Problem

Color-cohort operators need portfolio-centric heatmaps, PCS rankings, and time series. Today that lives only on Portfolio Builder (session draft) and Correlation Calculator (ad-hoc), not on the Portfolios tab.

## Scope

1. `GET /portfolios/correlation` — ranking table + multi-PCS chart + flags strip  
2. `GET /portfolios/:id/correlation` — heatmap, matrix (0.55/0.70 colors), high pairs, quality flags, PCS history  
3. Nav links from Portfolios index/show  
4. Reuse `shared/correlation_transparency_strip`, `PortfolioCorrelationSnapshot`, existing matrix helpers  
5. Optional: refresh snapshot for one portfolio’s Books (no membership change)

## Out of scope (v1)

- Auto-rebalance  
- Tick-level correlation  
- Replacing Portfolio Builder greedy assembly  

## Acceptance

- [ ] Index ranks all registry color portfolios by latest PCS  
- [ ] Multi-series PCS chart for last 30–90 days  
- [ ] Portfolio detail shows dual-threshold heatmap for Books  
- [ ] Flags surface max\|r\| > 0.70 and PCS drop ≥ 10  
- [ ] Specs for ranking query / empty portfolio  

## Related

- Phase 3 visualizers (builder/calculator) already shipped  
- Phase 5 DAR PCS section in Wv2 is ops-facing; this is WUT lab-facing  
