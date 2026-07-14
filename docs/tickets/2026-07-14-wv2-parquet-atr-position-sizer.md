# Ticket: Fix parquet ATR / PositionSizer zero units

**Status:** Proposed  
**Date:** 2026-07-14  
**Source:** `docs/session-reports/2026-07-14-1112-paper-telegram-phase0-1.md`

## Problem

On first Blue PBR62 paper confirm, `Operations::PositionSizer` returned **0 units** for AMZN/GOOGL because loaded `atr` ≈ price (e.g. GOOGL close ~359, atr ~363). TSMC atr looked sane (~21). Explicit `units: 5` was required to complete the confirm loop.

## Scope

1. Trace `ParquetLookbackLoader` / bar ATR column source (`atr_17` vs wrong column).  
2. Compare DM Winston EOD parquet for affected symbols vs loader mapping.  
3. Spec: sensible ATR band vs price for liquid equities; sizer returns positive units for normal capital/risk.  
4. Do not block paper ops (confirm already supports explicit units).

## Acceptance

- [ ] Root cause documented (loader vs data)  
- [ ] Auto sizing produces non-zero units for AMZN-like bars on recent dates  
- [ ] Spec or smoke covering sizer + bar load  

## Related

- `winston_v2/app/services/operations/position_sizer.rb`  
- `JournalConfirmationService`  
- Session: `2026-07-14-1112-paper-telegram-phase0-1.md`  
