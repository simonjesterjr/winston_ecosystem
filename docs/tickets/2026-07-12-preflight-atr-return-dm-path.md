# Ticket: Preflight ATR DM-path return (fixed) — regression note

**Status:** Done (code in WUT this session)  

**Date:** 2026-07-12  

## Problem

`PortfolioSignalOptimizationPreflight#atr_error_for` took the DM parquet branch but did not `return` the ATR-zero error string, falling through to legacy `"no price activities found"` even when parquet existed (CORN/WTI/XLI). Blocked `vet_trend` on new cohorts.

## Fix

- Explicit `return` on DM ATR failure path  
- Prefer `atr_17` from Bar extra when `Bar#atr` is zero  
- Re-acquired CORN/WTI/XLI via DM so atr columns populated  

## Acceptance

- [x] Green/Pink/Blank/Rust vet_trend ran past preflight  
- [ ] Optional unit spec for DM-path ATR zero message (nice-to-have)  

## Files

- `winston_unit_test/app/services/portfolio_signal_optimization_preflight.rb`  
