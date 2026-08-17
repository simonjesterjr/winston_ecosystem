# Ticket: WUT PositionSwapEvaluator spec sets Activity.atr as a column

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-17  
**Monolith:** winston_unit_test  
**Domain:** Lab specs, Activity / ATR  
**See:** [`2026-08-17-1315-leftover-dirty-trees.md`](../session-reports/2026-08-17-1315-leftover-dirty-trees.md) §5/§7/§14; [`2026-07-08-schema-cleanup-activity-id-columns.md`](2026-07-08-schema-cleanup-activity-id-columns.md) §G

## Problem

`spec/services/portfolio_backtest/position_swap_evaluator_spec.rb` does `Activity.create!(..., atr: 2.5)`. `Activity#atr` is a **method** (Market Indicator Value lookup), not a column. Two examples fail with `ActiveModel::UnknownAttributeError: unknown attribute 'atr' for Activity`.

Caught while verifying leftover Portfolio Backtest Run (PBR) specs. Pre-existing; not caused by the leftover land.

## Scope

1. Stop assigning `atr:` on `Activity.create!`.
2. Stub `Activity#atr` (or attach a Market Indicator Value) so the swap evaluator still has a number.
3. Do **not** re-open the full activity-id schema cleanup unless this ticket proves a production path is also broken.

## Acceptance

- [ ] `bundle exec rspec spec/services/portfolio_backtest/position_swap_evaluator_spec.rb` — 2 examples, 0 failures
- [ ] No `atr:` mass-assignment on Activity in this spec

## Related

- `winston_unit_test/app/models/activity.rb` (`def atr`)
- `winston_unit_test/spec/services/portfolio_backtest/position_swap_evaluator_spec.rb`
