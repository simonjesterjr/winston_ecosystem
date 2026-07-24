# Ticket: Lab PBR fill cadence — signal day X → fill at X+1 open

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-24  
**Completed:** 2026-07-24  
**Monolith:** winston_unit_test (lab); ops doctrine ADR-009  

## Problem

WUT lab PBRs filled at **same-day open** of the signal bar (`PositionManager#market_price` → `activity.open`), while ops doctrine is **Signal Date T → Fill Date T+1 open**.

Also: `TradingSignal` had `attr_accessor :bar_date, :market_id` that **shadowed AR columns**, so signal dates never persisted to the DB.

## Solution

1. **Default lab mode `next_bar_open`** (`LabFillCadence`):
   - Signal day T: evaluate entry/exit/pyramid; **queue** fill for next session  
   - Fill day T+1: execute at **open**, journal/position `bar_date` = fill date  
   - `TradingSignal.bar_date` = **signal date T**  
2. **Legacy escape:** `LAB_FILL_CADENCE=same_bar_open` or `results_json["fill_cadence"]="same_bar_open"`  
3. **Stops:** still fill same day at stop price (intrabar exception)  
4. **Signal-driven exits:** queue for next open (same as entries)  
5. Fixed `TradingSignal` attr_accessor shadow so Signal Date persists  

## Code

| Piece | Path |
|-------|------|
| Cadence helper | `app/services/lab_fill_cadence.rb` |
| Pending queue + fill | `app/services/portfolio_backtest_runner.rb` |
| Fill bar pricing | `app/services/position_manager.rb` (`fill_activity:`) |
| Estimate fill price | `app/services/portfolio_backtest/entry_requirement_calculator.rb` |
| Signal date fix | `app/models/trading_signal.rb` |
| Specs | `spec/services/lab_fill_cadence_spec.rb`, `portfolio_backtest_next_open_fill_spec.rb` |

## Verification (smoke PBR 153)

Short window clone of parent 62 (2020-08-01 … 2020-10-31), `fill_cadence=next_bar_open`:

| Check | Result |
|-------|--------|
| Positions with signal_date null | **0 / 43** |
| Fill date **after** signal date | **43 / 43** |
| Fill date == signal date | **0 / 43** |
| Example | signal **2020-08-05** → fill **2020-08-06** @ open |

Historical close-trigger PBRs (142–150) remain **same-day open** (pre-fix); do not re-interpret without re-run.

## Acceptance

- [x] Documented lab mode: `fill_at: same_bar_open | next_bar_open` (default **next**)  
- [x] Specs: next bar helper + enqueue  
- [x] Smoke rebaseline short-window PBR **153** (parent 62 recipe)  
- [x] BA note: historical campaign used same-day open  

## Related

- ADR-009  
- BA: `business_analysis/2026-07-24-close-trigger-signal-strength.md`  
- Archive: `tickets/archive/2026-07-24-close-trigger-signal-strength-one-way-dynamic.md`  
