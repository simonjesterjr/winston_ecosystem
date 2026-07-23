# Ticket: Multi-cohort evaluate smoke with Yellow #330 + Mint #311 Active

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-23  
**Domain:** Daily Analysis, paper Active band, smoke  
**Monoliths:** winston_v2  
**See:** [session report](../session-reports/2026-07-23-1158-yellow-122-wv2-activate.md); Mint activate: [`2026-07-23-activate-wv2-mint-op311-smoke.md`](2026-07-23-activate-wv2-mint-op311-smoke.md)

## Problem

Yellow OP **#330** (`Portfolio Yellow · 92776cfd`) and Mint OP **#311** (`Portfolio Mint · 3749c990`) are both **Active paper** after exclusive-cohort handoffs. Multi-cohort Daily Analysis / evaluate has not been re-run as a deliberate smoke since both joined the Active band.

## Desired outcome

1. Run evaluate for the current Active set (or explicit date) without auto-activating extras.  
2. Confirm both #311 and #330 appear in notification / DAR portfolio list.  
3. Note any `missing_data` / skip reasons for Yellow or Mint markets.  
4. Short session note or checklist tick on success.

## Acceptance

- [ ] `wv2:portfolios:evaluate` (or internal evaluate) completes for Active band including #311 + #330  
- [ ] Operator-visible summary: which OPs evaluated, errors if any  
- [ ] No unexpected activation of demos/smoke OPs  

## Non-goals

- Real capital activation  
- Changing Active mutex policy  
- Fixing MCP transfer path  

## Ops sketch

```bash
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
# inspect cromwell notification / DAR as usual
```
