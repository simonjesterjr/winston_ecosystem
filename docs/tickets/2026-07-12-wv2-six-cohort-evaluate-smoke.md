# Ticket: Smoke daily analysis for six Active color cohorts

**Status:** Proposed  

**Date:** 2026-07-12  

## Context

Wv2 Active set (post Phase 6 import):

- Portfolio Red, Blue, Green, Pink, Blank, Rust (all Active)  
- Orange deactivated; White not activated  

PCS daily path and DAR correlation section depend on WUT snapshots + WutClient.

## Scope

1. Ensure DM parquet for all Books symbols of the six (sync if missing)  
2. `bin/rails wv2:portfolios:evaluate` (or DailyAnalysisJob) for today  
3. Confirm notification JSON has `correlation_scores.series` for Active OPs  
4. Confirm DAR markdown/PDF include CORRELATION SCORES section (or graceful WUT-down note)  
5. Note any `missing_data` / `unsupported_strategy` skips  

## Acceptance

- [ ] Evaluate completes without crash  
- [ ] Six portfolios appear in evaluate result or explicit skip reasons  
- [ ] `correlation_scores` present when WUT reachable  
- [ ] Brief note in session report or ticket checklist  

## Related

- ADR-007, Phase 5 DAR enrichment  
- WUT `GET /internal/correlation_scores`  
