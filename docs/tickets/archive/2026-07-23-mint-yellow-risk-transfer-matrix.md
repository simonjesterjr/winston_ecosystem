# Ticket: Mint/Yellow risk-transfer matrix (R1 ladder + capacity)

**Status:** Done — matrix scored 2026-09-04  
**Priority:** P2  
**Date:** 2026-07-23  
**Domain:** One-Way Dynamic Risk, capacity, PortfolioBacktestRun  
**Monoliths:** winston_unit_test  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md); script `winston_unit_test/lib/scripts/mint_yellow_risk_transfer.rb`

## Problem

Blue-era doctrine (PBR 48/62/80) transfers **one_way_dynamic R1 ladder** and capacity (max_positions 10/11/12, max_markets 4) after entry win. Script `mint_yellow_risk_transfer.rb` was written but not fully executed post runner fix. Need evidence whether Mint/Yellow behave like Blue under accelerating risk vs static vet winners.

## Desired outcome

- Run the script after vet winners exist (or pin Elephant / Breakout50NoHistory winners).  
- Produce `/portfolio_configs/mint-yellow-risk-transfer-results.json` summary table.  
- Recommend one recipe per portfolio for smoke (static vs R1, caps).

## Acceptance

- [x] Matrix completed for both portfolios  
- [x] Results JSON written  
- [x] One recommended fingerprint per portfolio documented in session note or ticket update

## 2026-09-04 run

Script `lib/scripts/mint_yellow_risk_transfer.rb` now **stamps `next_bar_open`**. Unstamped PBRs default to rejected hybrid price-level fill (`LabFillCadence::DEFAULT`). Vet winners remain opt#47/#48 Breakout50NoHistory + VolatilityExit.

Cells per book: static-m12-k4-swap; R1 capacity grid (m10/11/12 × k4/nil, swap on/off); R3 conservative; winner-exits under R1. Sequential after Mango/Rust rescue. Results → `/portfolio_configs/mint-yellow-risk-transfer-results.json`.

---

## Close-out (2026-09-04)

Blue R1 **does not transfer** onto exclusive books the way it rescued Blue.

| Portfolio | Recommendation | Fingerprint |
|-----------|----------------|-------------|
| **Mint** | **None from this matrix.** All 8 cells failed return and drawdown (best static PBR 542 −53% / 83% DD). Keep live Turtle S2 paper **#797**. | — |
| **Yellow** | **PBR 550** static m12 k4 swap: +424.7% / 38.8% DD / Sharpe 0.90 / 139 trades, **trade_ready**. R1 cells are worse than static. Do **not** activate (Turtle S1 **#798** is Active; OWDC-none **#1400** already inactive). | WUT TS **#101** `64a02b74…` |

Analysis: [`business_analysis/2026-09-04-mango-rust-mint-yellow-lab.md`](../../business_analysis/2026-09-04-mango-rust-mint-yellow-lab.md).  
