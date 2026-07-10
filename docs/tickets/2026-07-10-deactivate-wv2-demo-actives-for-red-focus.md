# Ticket: Deactivate Wv2 demo actives so paper focus is Portfolio Red

**Status:** Done  
**Date:** 2026-07-10  
**Context:** Session [`2026-07-09-1655-wv2-strategy-registry-daily-smoke`](../session-reports/2026-07-09-1655-wv2-strategy-registry-daily-smoke.md). After StrategyRegistry fix, daily analysis evaluates all **Active** portfolios. Live set was three: Trading Portfolio B, Sample Trend Portfolio, Portfolio Red.

## Problem

Domain **Active** means laser attention on Daily Analysis / human task surface. Seed/demo portfolios (B, Sample Trend) dilute Red paper observation and clutter Cromwell notifications with empty evaluations.

## Scope

1. Deactivate Portfolio B and Sample Trend (`wv2:portfolios:deactivate` or internal API).
2. Leave Portfolio Red **Active** for paper/observation.
3. Re-run evaluate or wait for EOD cron; confirm notification lists only Red (plus any intentional actives).
4. Optional: document operator command in `portfolio_configs/README.md`.

## Acceptance

- [x] Active count is Red-only (or explicit operator set)
- [x] Next daily report does not evaluate demo seed portfolios
- [x] Red remains active with capital/TS unchanged

## Resolution (2026-07-10)

```bash
./bin/compose exec -T winston_v2 bin/rails wv2:portfolios:deactivate["Trading Portfolio B"]
./bin/compose exec -T winston_v2 bin/rails 'wv2:portfolios:deactivate[Sample Trend]'
./bin/compose exec -T winston_v2 bin/rails wv2:portfolios:list   # active: 1 → #5 Portfolio Red
./bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
```

- **Active set:** only Portfolio Red `#5` (capital_base $10k, TS#8 Portfolio Red Strategy).
- **Evaluate 2026-07-10:** notification `portfolios[]` = Red only (`status: evaluated`); `skipped_portfolios: []`; summary `portfolios: 1`.
- Historical `passed_signals` still list expired demo-window rows (archive data, not today's evaluation set).
- Documented Active hygiene + deactivate commands in `portfolio_configs/README.md`.

## Related

- CONTEXT: **Active** portfolio doctrine
- Session: `2026-07-09-1655-wv2-strategy-registry-daily-smoke.md`
- Docs: `portfolio_configs/README.md` (Active attention hygiene)
