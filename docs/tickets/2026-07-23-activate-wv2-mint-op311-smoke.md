# Ticket: Activate Wv2 Portfolio Mint OP#311 for smoke DAR

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-23  
**Domain:** Operational Portfolio, Active, Paper Trading, DAR smoke  
**Monoliths:** winston_v2  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md)

## Problem

Mint + Elephant5+20 was imported as **OP#311** (`Portfolio Mint · 3749c990`) paper/inactive after PBR 121. It is not yet in the Active smoke set, so DAR / evaluate will not exercise this exclusive cohort.

## Desired outcome

- Operator decides whether to activate #311 (mutex vs other Active OPs).  
- If yes: `wv2:portfolios:activate[311]` (or MCP activate), then one evaluate smoke.  
- Document Active set after change.

## Acceptance

- [ ] Activate decision recorded (activate or skip)  
- [ ] If activated: evaluate smoke for latest EOD date with #311 ready  
- [ ] Active mutex policy respected (force only if intentional)  

## Commands

```bash
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:activate[311]
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
```
