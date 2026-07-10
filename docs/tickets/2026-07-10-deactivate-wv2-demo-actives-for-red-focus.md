# Ticket: Deactivate Wv2 demo actives so paper focus is Portfolio Red

**Status:** Proposed  
**Date:** 2026-07-10  
**Context:** Session [`2026-07-09-1655-wv2-strategy-registry-daily-smoke`](../session-reports/2026-07-09-1655-wv2-strategy-registry-daily-smoke.md). After StrategyRegistry fix, daily analysis evaluates all **Active** portfolios. Live set is three: Trading Portfolio B, Sample Trend Portfolio, Portfolio Red.

## Problem

Domain **Active** means laser attention on Daily Analysis / human task surface. Seed/demo portfolios (B, Sample Trend) dilute Red paper observation and clutter Cromwell notifications with empty evaluations.

## Scope

1. Deactivate Portfolio B and Sample Trend (`wv2:portfolios:deactivate` or internal API).
2. Leave Portfolio Red **Active** for paper/observation.
3. Re-run evaluate or wait for EOD cron; confirm notification lists only Red (plus any intentional actives).
4. Optional: document operator command in `portfolio_configs/README.md`.

## Acceptance

- Active count is Red-only (or explicit operator set)
- Next daily report does not evaluate demo seed portfolios
- Red remains active with capital/TS unchanged

## Related

- CONTEXT: **Active** portfolio doctrine
- Session: `2026-07-09-1655-wv2-strategy-registry-daily-smoke.md`
