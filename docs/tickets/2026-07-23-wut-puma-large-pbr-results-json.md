# Ticket: WUT puma timeouts under large multi-market PBR results_json

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-23  
**Domain:** PortfolioBacktestRun, performance, MCP handoff reliability  
**Monoliths:** winston_unit_test (primary); winston_mcp consumer  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md); related [`2026-07-09-validation-pbr-day-by-day-perf.md`](2026-07-09-validation-pbr-day-by-day-perf.md)

## Problem

Large multi-market PBRs (e.g. Mint/Yellow Elephant, ~1700 days × equity_history) write **huge `results_json`** on progress ticks. Observed:

- WUT puma RSS ~2GB during session  
- Host `curl` to `/internal/portfolio_config` **timed out** (0 bytes) while `rails runner` export completed in ~0.5s  
- Contributes to perceived “MCP transfer hang” under load  

## Desired outcome

1. Slim progress writes (truncate equity/cash history mid-run; full history only on complete).  
2. Or lower progress persist frequency / use Sidekiq for export.  
3. Confirm `/internal/portfolio_config?run_id=` stays &lt; few seconds under concurrent PBRs.  
4. Document operational limit (markets × days) for interactive PBR.

## Acceptance

- [ ] Progress `results_json` size bounded (threshold documented)  
- [ ] Internal export HTTP smoke under concurrent PBR does not hang 15s+  
- [ ] No regression in final PBR metrics persistence  
