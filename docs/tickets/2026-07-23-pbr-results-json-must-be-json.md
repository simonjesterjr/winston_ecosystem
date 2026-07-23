# Ticket: PBR `results_json` must be valid JSON (not Hash#inspect)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-23  
**Domain:** PortfolioBacktestRun, export handoff, data integrity  
**Monoliths:** winston_unit_test (primary); consumers: MCP transfer, Wv2 import  
**See:** [session report](../session-reports/2026-07-23-1158-yellow-122-wv2-activate.md); related [`2026-07-23-wut-puma-large-pbr-results-json.md`](2026-07-23-wut-puma-large-pbr-results-json.md), [`2026-07-23-mcp-transfer-activate-flow-smooth.md`](2026-07-23-mcp-transfer-activate-flow-smooth.md)

## Problem

At least one completed multi-market PBR (**run 122**, Portfolio Yellow + Elephant5+20) stored `results_json` as a **Ruby `Hash#inspect` string** (`"key"=>value`) instead of JSON (`"key":value`).

Effects:

1. `PortfolioBacktestRun#results_parsed` does `JSON.parse(...) rescue {}` → **empty hash**.  
2. `OneWayDynamicRiskValidator.pyramid_risks_from_run` cannot see the ladder → export/capture fails with “missing pyramid_risks”.  
3. MCP transfer appears to hang or fails; operator must repair DB + rake-export.  
4. Mint **run 121** (same recipe family) had **valid JSON** — writer path is inconsistent.

Evidence (2026-07-23):

- Run 122 first bytes: `"{\"current_date\"=>\"2026-07-22\", \"processed_days\"=>1798, ..."`  
- Run 121 first bytes: `"{\"current_date\":\"2026-07-22\",\"processed_days\":1687,..."`  
- Ops repair: `eval` of trusted row → seed ladder from TS#25 → `JSON.generate` → export succeeded.

## Desired outcome

1. **Find writer(s)** that persist progress/final `results_json` via `#to_s` / inspect instead of `JSON.generate` / proper serialization.  
2. **Always write valid JSON** (or use a jsonb column + Hash only).  
3. **Guard on write:** reject / auto-coerce non-JSON before save.  
4. **Optional ops rake:** scan recent PBRs for inspect-format rows; report or repair.  
5. **Regression:** unit/spec that round-trips methodology keys (`risk_evaluation_config`, `trading_strategy_id`) through save/reload + `results_parsed`.

## Acceptance

- [ ] Identified code path(s) that wrote inspect-format for run 122 class  
- [ ] New writes always parse with `JSON.parse` without rescue-to-empty  
- [ ] Spec covers corrupt-string detection or write guard  
- [ ] Document ops repair one-liner in ticket or operations note  
- [ ] Spot-check: no open completed PBRs with `=>` in `results_json` prefix (or list repaired)

## Non-goals

- Slimming equity_history size (sibling puma ticket)  
- Changing OneWayDynamicRiskValidator ladder policy  
