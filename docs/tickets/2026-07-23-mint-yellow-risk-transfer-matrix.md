# Ticket: Mint/Yellow risk-transfer matrix (R1 ladder + capacity)

**Status:** Proposed  
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

- [ ] Matrix completed for both portfolios  
- [ ] Results JSON written  
- [ ] One recommended fingerprint per portfolio documented in session note or ticket update  
