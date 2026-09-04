# Ticket: WUT PBR show page should link the captured TradingStrategy

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-04  
**Mode:** normal  
**Graph nodes:** winston_unit_test  
**Human gates:** none  
**DoD:** completed PBR show names the captured TS (id + short fingerprint) or states none  
**Origin:** [`docs/session-reports/2026-09-04-1428-lab-dead-ends-and-research.md`](../session-reports/2026-09-04-1428-lab-dead-ends-and-research.md)

## Problem

`trading_strategies:capture_validation_runs` writes a Trading Strategy (TS) and a TradingStrategySelection keyed by `portfolio_backtest_run_id`. The Portfolio Backtest Run (PBR) **show** page does not surface that link. Operator looking at PBR **550** could not find WUT TS **#101** (`64a02b74…`) and assumed no TS existed. The record lives on `/wut/trading_strategies`.

## Scope

1. On PBR show (and optionally index), if a selection or `TradingStrategy` points at the run, render: TS id, name, short fingerprint, `export_kind`, link to the TS page.  
2. If none: explicit “no captured TS — run `trading_strategies:capture_validation_runs PBR_IDS=<id>`”.  
3. Spec: captured run shows the link; uncaptured completed run shows the empty state.

## Non-goals

- Auto-capture on PBR complete  
- Changing fingerprint identity  
- Wv2 OP pages

## Acceptance

- [ ] PBR 550 show (or equivalent fixture) displays TS #101 / `64a02b74`  
- [ ] Request or view spec covers captured vs uncaptured  
- [ ] No capture as a side effect of rendering
