# Ticket: Promote Wv2 daily-ops smoke scripts out of tmp/

**Status:** Proposed  
**Date:** 2026-07-10  
**Context:** Session [`2026-07-09-1655-wv2-strategy-registry-daily-smoke`](../session-reports/2026-07-09-1655-wv2-strategy-registry-daily-smoke.md). Ephemeral helpers used for wrap smoke:

- `winston_v2/tmp/ops_smoke_daily.rb`
- `winston_v2/tmp/ops_check_red_parquet.rb`
- `winston_v2/tmp/ops_eval_with_red.rb`

## Problem

Operators and agents re-run the same smoke sequence (registry, readiness, parquet, evaluate, notification inspect). Scripts live under `tmp/` and are not committed — they will be lost on clean trees.

## Scope

1. Move or re-home as `winston_v2/bin/` rake tasks or documented runner scripts (prefer small rake under `wv2:` namespace).
2. Document one-liner in `portfolio_configs/README.md` or Wv2 AGENTS.md.
3. Do not hard-code only Portfolio Red if generalizing — support env `PORTFOLIO` / `REPORT_DATE`.

## Acceptance

- Smoke path runnable from a clean clone without recreating tmp files
- Commands documented in one discoverable place

## Related

- Session: `2026-07-09-1655-wv2-strategy-registry-daily-smoke.md`
- `portfolio_configs/README.md` evaluate flow
