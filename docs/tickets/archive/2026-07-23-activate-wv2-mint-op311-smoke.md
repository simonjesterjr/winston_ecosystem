# Ticket: Activate Wv2 Portfolio Mint OP#311 for smoke DAR

**Status:** Done  
**Priority:** P2  
**Date:** 2026-07-23  
**Closed:** 2026-07-24  
**Domain:** Operational Portfolio, Active, Paper Trading, DAR smoke  
**Monoliths:** winston_v2  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md); Telegram hang path: [`../2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md`](../2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md); multi-cohort: [`2026-07-23-multi-cohort-evaluate-yellow-mint-active.md`](2026-07-23-multi-cohort-evaluate-yellow-mint-active.md)

## Problem

Mint + Elephant5+20 was imported as **OP#311** (`Portfolio Mint · 3749c990`) paper/inactive after PBR 121. It is not yet in the Active smoke set, so DAR / evaluate will not exercise this exclusive cohort.

## Desired outcome

- Operator decides whether to activate #311 (mutex vs other Active OPs).  
- If yes: `wv2:portfolios:activate[311]` (or MCP activate), then one evaluate smoke.  
- Document Active set after change.

## Progress (2026-07-23 ~16:46 UTC)

- **Activated** via internal API after Telegram `activate 311` hung on empty LLM (no MCP call).  
- Result: `active=true`, `execution_mode=paper`, no mutex conflicts (seed Portfolio Mint).  
- Telegram path did **not** complete; see fastpath P1 ticket.

## Smoke evidence (2026-07-24 ~15:50 UTC)

Multi-cohort evaluate with #311 + #330 Active:

```bash
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
```

- #311 status **`evaluated`** in `wv2_20260724` Cromwell notification + DAR.  
- PCS Mint **91.2** (daily_job snapshot).  
- 0 skips / missing_data for Mint.  
- Full write-up: archived multi-cohort ticket.

## Acceptance

- [x] Activate decision recorded (activate or skip) — **activated**  
- [x] If activated: evaluate smoke for latest EOD date with #311 ready — **2026-07-24 multi-cohort**  
- [x] Active mutex policy respected (force only if intentional)  

## Commands

```bash
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:activate[311]
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
```
