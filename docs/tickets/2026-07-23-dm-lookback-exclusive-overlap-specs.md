# Ticket: Specs for DM lookback/date-range and exclusive MAX_OVERLAP=0

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-23  
**Domain:** PortfolioBacktestRunner, PortfolioOverlapPolicy, regression  
**Monoliths:** winston_unit_test  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md)

## Problem

Session fixes are production-critical but unspec’d:

1. `PortfolioBacktestRunner#find_overlapping_date_range` / `#get_lookback_activities` for **DM-only markets** (empty activities).  
2. `PortfolioOverlapPolicy` / builder **max_overlap_fraction = 0** and rake `EXCLUDE_TAKEN`.  
3. `OneWayDynamicRiskValidator.pyramid_risks_from_run` TS fallback + factory ladder seed.

Without specs, dual-path (activities vs parquet) will regress again.

## Desired outcome

- Unit/integration specs covering: empty activities + DmCoverage present → non-nil overlap + non-empty lookback.  
- Builder/policy: exclusive 0 shared markets rejects peer twin.  
- Export: one_way_dynamic without ladder fails; with TS provenance succeeds.

## Acceptance

- [ ] Specs green in compose WUT  
- [ ] Covers at least lookback empty-activities regression  
