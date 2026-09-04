# Ticket: Export Yellow PBR 550 / TS #101 as inactive paper OP

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-04  
**Mode:** normal  
**Graph nodes:** winston_unit_test, winston_v2  
**Human gates:** do **not** activate; Turtle Yellow S1 **#798** stays Active  
**DoD:** JSON in `portfolio_configs/`; Wv2 OP inactive paper; fingerprint `64a02b74…`; `inspect_strategy` OK  
**Origin:** [`docs/session-reports/2026-09-04-1428-lab-dead-ends-and-research.md`](../session-reports/2026-09-04-1428-lab-dead-ends-and-research.md)  
**Related:** [`archive/2026-07-23-mint-yellow-risk-transfer-matrix.md`](archive/2026-07-23-mint-yellow-risk-transfer-matrix.md); [`business_analysis/2026-09-04-mango-rust-mint-yellow-lab.md`](../../business_analysis/2026-09-04-mango-rust-mint-yellow-lab.md)

## Problem

Mint/Yellow risk-transfer matrix winner is Winston Unit Test (WUT) Portfolio Backtest Run (PBR) **550** (Yellow, static, Breakout50NoHistory + VolatilityExit, next-bar-open, +425% / 39% max drawdown / Sharpe 0.90). Captured as WUT Trading Strategy (TS) **#101** fingerprint `64a02b74b3f48709951123b86685b33ae9bd567453e733cd4f82c6326db4449b`, `export_kind=trade_ready`.

The TS is **not** on the PBR row. It is **not** in `portfolio_configs/` and **not** in Winston v2 (Wv2). Operator asked what the TS is and whether it is exportable. Wrap landed before import.

## Scope

1. `wut:portfolios:export_config[550, /portfolio_configs/portfolio-yellow-static-pbr550.json]` with `SEED_NAME="Portfolio Yellow"` and a distinct display name.  
2. Confirm JSON: `export_kind=trade_ready`, `risk_evaluation_strategy=static`, `risk_scale_policy=none`, fingerprint `64a02b74…`, `wut_backtest_run_id=550`, `wut_trading_strategy_id=101`.  
3. `wv2:portfolios:import[…]` — ADR-006 lands **inactive paper**.  
4. `wv2:portfolios:inspect_strategy[<new id>]`.  
5. Do **not** activate. Active Yellow is Turtle S1 **#798**. Inactive OWDC-none **#1400** stays as the other Yellow recipe.

## Non-goals

- FORCE dual-Active Yellow  
- Desk confirm / real capital  
- Mint cells from the same matrix (all failed)

## Acceptance

- [ ] Export JSON on the bind mount  
- [ ] Wv2 OP exists, `active=false`, `execution_mode=paper`, `seed_name=Portfolio Yellow`  
- [ ] Fingerprint matches TS #101  
- [ ] `inspect_strategy` OK; Breakout50DayNoHistory + VolatilityExit resolve  
- [ ] #798 still the sole Active Yellow unless operator later FORCE
