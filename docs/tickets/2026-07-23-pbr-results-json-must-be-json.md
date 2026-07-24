# Ticket: PBR `results_json` must be valid JSON (not Hash#inspect)

**Status:** Done  
**Priority:** P1  
**Date:** 2026-07-23  
**Resolved:** 2026-07-24  
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

## Root cause (2026-07-24)

**Assigning a Ruby `Hash` to a `text` column** makes ActiveRecord type-cast via `Hash#to_s` / `#inspect` (`"key"=>value`), not `JSON.generate`.

Confirmed live:

```ruby
run.results_json = { "current_date" => "2026-07-22" }
# stored: {"current_date"=>"2026-07-22"}  # poison
run.results_json = { "current_date" => "2026-07-22" }.to_json
# stored: {"current_date":"2026-07-22"}   # valid
```

Known / likely writers:

1. **`lib/scripts/mint_yellow_risk_transfer.rb`** — `run.update!(results_json: rj)` with bare Hash (fixed).  
2. **Any `update` / `update_column` / `create` with a Hash** for `results_json` (now guarded at the attribute type).  
3. Historical poison still in DB until repaired (run **122** repaired 2026-07-23; run **41** Orange repaired 2026-07-24).

Progress path in `PortfolioBacktestRunner` already used `.to_json`; inconsistency came from other Hash-assign writers + silent `results_parsed` rescue.

## Desired outcome

1. **Find writer(s)** that persist progress/final `results_json` via `#to_s` / inspect instead of `JSON.generate` / proper serialization.  
2. **Always write valid JSON** (or use a jsonb column + Hash only).  
3. **Guard on write:** reject / auto-coerce non-JSON before save.  
4. **Optional ops rake:** scan recent PBRs for inspect-format rows; report or repair.  
5. **Regression:** unit/spec that round-trips methodology keys (`risk_evaluation_config`, `trading_strategy_id`) through save/reload + `results_parsed`.

## Fix delivered (WUT)

| Piece | Location |
|-------|----------|
| Attribute type coerces Hash/Array → `JSON.generate` on all writes including `update_column` | `app/models/portfolio_backtest_run.rb` (`ResultsJsonType`) |
| `dump_results_json`, poison detect, trusted `recover_results_json` | same model |
| Validation when `results_json` changes | `results_json_must_be_parseable_json` |
| `write_results!` / `merge_results!` helpers | same model |
| Mint/Yellow transfer script no longer bare-Hash assigns | `lib/scripts/mint_yellow_risk_transfer.rb` |
| Scan + repair rake | `lib/tasks/pbr_results_json.rake` |
| Regression specs | `spec/models/portfolio_backtest_run_results_json_spec.rb` |

### Ops one-liners

```bash
# Scan (exit 1 if any poison remains)
bin/compose exec -T winston_unit_test bin/rails wut:pbr:scan_results_json

# Dry-run repair all / one id
bin/compose exec -T winston_unit_test bin/rails wut:pbr:repair_results_json
bin/compose exec -T winston_unit_test bin/rails 'wut:pbr:repair_results_json[41]'

# Apply repair
bin/compose exec -T -e APPLY=1 winston_unit_test bin/rails 'wut:pbr:repair_results_json[41]'
```

Console repair (legacy, prefer rake):

```ruby
r = PortfolioBacktestRun.find(ID)
h = PortfolioBacktestRun.recover_results_json(r.results_json)
r.update_column(:results_json, PortfolioBacktestRun.dump_results_json(h))
```

## Acceptance

- [x] Identified code path(s) that wrote inspect-format for run 122 class — bare Hash → text column (`to_s`/`inspect`); mint script + any Hash assign  
- [x] New writes always parse with `JSON.parse` without rescue-to-empty — attribute type + validation  
- [x] Spec covers corrupt-string detection or write guard — `spec/models/portfolio_backtest_run_results_json_spec.rb` (7 examples)  
- [x] Document ops repair one-liner in ticket or operations note — rake + console above  
- [x] Spot-check: no open completed PBRs with `=>` in `results_json` prefix — scan clean after repairing PBR **#41** (122 already fixed earlier)

## Non-goals

- Slimming equity_history size (sibling puma ticket)  
- Changing OneWayDynamicRiskValidator ladder policy  
- Migrating column to native `jsonb` (possible follow-up; type guard is sufficient now)

## Verification (2026-07-24)

```text
bundle exec rspec spec/models/portfolio_backtest_run_results_json_spec.rb  # 7 examples, 0 failures
bundle exec rspec spec/services/portfolio_backtest_run_factory_spec.rb \
  spec/services/portfolio_config_exporter_spec.rb                         # 8 examples, 0 failures
bin/rails wut:pbr:scan_results_json                                      # OK: no non-JSON rows
```
