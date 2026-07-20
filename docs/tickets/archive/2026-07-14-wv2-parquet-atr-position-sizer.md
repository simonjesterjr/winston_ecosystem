# Ticket: Fix parquet ATR / PositionSizer zero units

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-14  
**Source:** `docs/session-reports/2026-07-14-1112-paper-telegram-phase0-1.md`  
**Completed:** 2026-07-20  

## Problem

On first Blue PBR62 paper confirm, `Operations::PositionSizer` returned **0 units** for AMZN/GOOGL because loaded `atr` ≈ price (e.g. GOOGL close ~359, atr ~363). TSMC atr looked sane (~21). Explicit `units: 5` was required to complete the confirm loop.

## Scope

1. Trace `ParquetLookbackLoader` / bar ATR column source (`atr_17` vs wrong column).  
2. Compare DM Winston EOD parquet for affected symbols vs loader mapping.  
3. Spec: sensible ATR band vs price for liquid equities; sizer returns positive units for normal capital/risk.  
4. Do not block paper ops (confirm already supports explicit units).

## Acceptance

- [x] Root cause documented (loader vs data)  
- [x] Auto sizing produces non-zero units for AMZN-like bars on recent dates  
- [x] Spec or smoke covering sizer + bar load  

## Root cause

**Loader bug (primary):** `ParquetLookbackLoader` ran `SELECT *` then mapped array indices with a fixed list `date, open, high, low, close, volume, atr_17`. Live Winston EOD parquet has ~26 columns with MAs before ATR (`…, volume, sma_5, ma_5, atr_15, atr_17, …`), so index 6 was **`sma_5` (~price)**, not `atr_17`. That matches AMZN/GOOGL (`atr` ≈ close). TSMC’s older 14-column file puts `atr_15` at index 6 (~21), so it looked “sane” by coincidence — **data was fine; mapping was wrong.**

**Sizer bug (secondary):** Even with true `atr_17`, `PositionSizer` used `risk_dollars / (atr * mult * price)`, which zeros units for ~$10k paper capital. WUT uses `risk_dollars / (atr * mult)` (`UnitRiskEvalService` / `PositionManager`). Fixed to match WUT.

## Outcome

- Loader: project `SELECT date, open, high, low, close, volume, atr_17` so row indices always match `SELECT_COLUMNS`.  
- Sizer: `units = floor(risk_dollars / (atr * atr_multiplier))`.  
- Live check (OP #12, as_of 2026-07-10): AMZN units=11, GOOGL units=8, TSMC units=4 with `atr/close` ~3–5%.  
- Specs: `parquet_lookback_loader_spec` (Winston EOD multi-column + sizer band) + `position_sizer_spec` — 10 examples, 0 failures.

## Related

- `winston_v2/app/services/operations/position_sizer.rb`  
- `winston_v2/app/services/parquet_lookback_loader.rb`  
- `JournalConfirmationService`  
- Session: `2026-07-14-1112-paper-telegram-phase0-1.md`  
