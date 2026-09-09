# Ticket: Specs for DM lookback/date-range and exclusive MAX_OVERLAP=0

**Status:** Done  
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

- [x] Specs green in compose WUT  
- [x] Covers at least lookback empty-activities regression  

## Close-out (2026-09-09)

Still applicable: production code from the 2026-07-23 session remained in WUT; the three regression locks were missing. No production-code change — specs only.

| Gap | Spec |
|-----|------|
| Empty activities + DmCoverage → overlap + lookback | `spec/services/portfolio_backtest_runner_dm_lookback_spec.rb` |
| Exclusive `max_overlap_fraction = 0` rejects a peer-book twin | `portfolio_overlap_policy_spec.rb`, `portfolio_correlation_builder_spec.rb` |
| OWD without ladder fails; TS provenance / factory seed succeeds | `one_way_dynamic_risk_validator_spec.rb`, `portfolio_backtest_run_factory_spec.rb`, `portfolio_config_exporter_spec.rb` |

`EXCLUDE_TAKEN` remains a rake candidate-pool pre-filter. The durable invariant is exclusive `max_overlap_fraction = 0` on policy + builder, which is what the specs lock.

Compose WUT: 47 examples, 0 failures.
