# Ticket: Optional Mint S2 re-score after UNG / WEAT / AMCR stitch

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-07  
**Mode:** normal  
**Graph nodes:** winston_unit_test  
**Human gates:** do **not** overwrite Portfolio Backtest Runs (PBRs) 532/533 or 536/537; do not stamp resting-touch as pack default  
**DoD:** New exclusive pair on current parquet; scores recorded; Turtle Mint S2 paper OPs unchanged  
**Origin:** [`docs/session-reports/2026-09-07-1957-corporate-action-hold-refuse.md`](../session-reports/2026-09-07-1957-corporate-action-hold-refuse.md)  
**Parent:** [`2026-08-22-corporate-action-stop-safeguards.md`](2026-08-22-corporate-action-stop-safeguards.md); [`2026-08-20-wut-resting-stop-touch-fill-cadence.md`](2026-08-20-wut-resting-stop-touch-fill-cadence.md)

## Problem

Mint S2 v2 pair (PBR **536** next-open +94% / 58% drawdown vs **537** resting +242% / 56%) ran on 2026-08-22 while United States Natural Gas Fund (UNG) 2024-01-24, Teucrium Wheat (WEAT) 2025-11-25, and Amcor (AMCR) 2026-01-15 were still split-like suspects. Those three are **clean** on disk as of 2026-09-07. The corporate-action guard did not fire on 537 — parquet stitch was load-bearing.

A new pair would be honest vs current files. It is **not** required to close the Winston v2 Confirm HOLD gate.

## Scope

1. `bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/resting_stop_touch_v2_mint_setup.rb` (or equivalent new experiment key).  
2. New PBR ids only.  
3. Record scores next to 536/537. Do not promote resting-touch.

## Non-goals

- Overwriting 532/533/536/537  
- Stamping Active Mint `#797` / FastBO5 `#384` to `resting_stop_touch`  
- Universe parquet APPLY  

## Acceptance

- [ ] New next-open + resting pair exist with distinct PBR ids  
- [ ] 532/533/536/537 untouched  
- [ ] Operator freeze (keep / drop resting as opt-in) recorded on this ticket  
