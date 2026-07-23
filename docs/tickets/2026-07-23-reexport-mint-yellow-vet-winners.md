# Ticket: Re-export Mint/Yellow first-pass vet winners (opt #47/#48)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-23  
**Domain:** Portfolio Signal Optimization, Trade-Ready / Observation export  
**Monoliths:** winston_unit_test  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md)

## Problem

Overnight `vet_trend` completed for exclusive Mint (opt **#47**) and Yellow (opt **#48**). Winners: **Breakout50DayNoHistoryStrategy + VolatilityExitStrategy**. Validation export / handoff JSON was incomplete while the runner still failed on DM-only books (0 trades or missing export). Static first-pass winners are still useful as observation/trade_ready baselines beside Elephant.

## Desired outcome

- Re-run validation PBR (or full `portfolios:vet_trend` export) under fixed runner.  
- Write `portfolio_configs/portfolio-mint.json` and `portfolio-yellow.json` with correct metrics + fingerprint.  
- Record export_kind via TradeReadyViabilityGates.

## Acceptance

- [ ] Both exports exist with non-zero trade validation metrics (or documented observation fail reasons)  
- [ ] Fingerprint + markets match exclusive books  
- [ ] Optional: import observation OPs to Wv2 if gates fail  
