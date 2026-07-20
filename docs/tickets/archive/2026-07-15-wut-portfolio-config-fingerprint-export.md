# Ticket: WUT portfolio_config export — fingerprint + seed lineage

**Status:** Done (code + live smoke); commit pending  
**Date:** 2026-07-15  
**Priority:** Medium-high (B — real ADR-006 quality)  
**Source:** Session 2026-07-15 Telegram transfer; transfer returned `legacy_no_fingerprint`  
**Repos:** `winston_unit_test`

## Problem

`GET /internal/portfolio_config?run_id=` (MCP transfer path) still exports a **legacy bare** payload:

- name like `"Portfolio Mango (WUT run 57)"`
- **no fingerprint**
- weak seed/display lineage vs file export + PR4 paper path

Wv2 importer therefore takes `legacy_*` / bare-name paths forever on live Telegram handoffs, even when the lab has a fingerprinted winning TradingStrategy (e.g. TS 16 for run 57).

Also this session: `portfolio_config` / `strategy_config` / `testing_strategies` were accidentally **private** (under `private` helpers) → `ActionNotFound` until fixed with `public` keyword. Regression risk if helpers reorder again.

## Scope (B)

1. Align `InternalController#portfolio_config` run export with rich file export / validation winner:
   - Include **fingerprint** from winning TS / run when available  
   - Stable **seed_name** (lab portfolio seed, not only display `"Name (WUT run N)"`)  
   - `export_kind`, markets, risk/strategy fields, caps where known  
2. `ts_id` path already uses `to_export_json` — verify fingerprint parity with run path.  
3. Specs: run_id export has fingerprint when TS fingerprinted; seed_name stable; re-import prefers fingerprint lineage.  
4. Guard: keep handoff actions **public** (comment + quick request/spec).  

## Acceptance

- [x] `portfolio_config?run_id=N` JSON includes fingerprint when methodology is fingerprinted  
- [x] Re-transfer via MCP yields `updated`/`forked`/`adopted` as appropriate, not only `legacy_*`  
- [x] Public action regression covered or documented  

## Implementation (2026-07-15)

| Artifact | Change |
|----------|--------|
| `app/services/portfolio_config_exporter.rb` | Shared ADR-006 builder (selection → capture fallback) |
| `InternalController#portfolio_config` | Uses exporter; public comment; ts_id gets seed_name/export_kind from selection |
| `lib/tasks/portfolio_configs.rake` | Thin wrapper over exporter |
| `spec/services/portfolio_config_exporter_spec.rb` | 3 examples green |

**Live smoke:** `GET …?run_id=57` → `fingerprint=f88e1ca0…`, `seed_name=Portfolio Mango`, `export_kind=observation`, `wut_trading_strategy_id=16`.  
**Wv2 re-import:** `action=adopted` on bare OP `#10` (`Portfolio Mango · f88e1ca0`), not `legacy_updated`. Legacy OP `#157` remains a separate series (expected).

## Related

- PR4 fingerprint export: WUT export rakes / TS capture  
- Ticket: `2026-07-14-refresh-remaining-color-portfolio-json-fingerprints.md`  
- Wv2: `Operations::PortfolioConfigImporter`  
- Session fix: `winston_unit_test` `internal_controller.rb` `public` for portfolio_config  
- Reply contract A: still needs Telegram smoke after concurrency Tier 0  

## Non-goals

- Changing engaged refuse / auto-fork semantics on Wv2  
- Migrating / destroying legacy OP `#157` (operator choice)  
