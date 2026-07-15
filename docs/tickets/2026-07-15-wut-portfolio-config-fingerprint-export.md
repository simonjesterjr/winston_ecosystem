# Ticket: WUT portfolio_config export — fingerprint + seed lineage

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** Medium-high (B — real ADR-006 quality)  
**Source:** Session 2026-07-15 Telegram transfer; transfer returned `legacy_no_fingerprint`  
**Repos:** `winston_unit_test`

## Problem

`GET /internal/portfolio_config?run_id=` (MCP transfer path) still exports a **legacy bare** payload:

- name like `"Portfolio Blank (WUT run 57)"`
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

- [ ] `portfolio_config?run_id=N` JSON includes fingerprint when methodology is fingerprinted  
- [ ] Re-transfer via MCP yields `updated`/`forked`/`adopted` as appropriate, not only `legacy_*`  
- [ ] Public action regression covered or documented  

## Related

- PR4 fingerprint export: WUT export rakes / TS capture  
- Ticket: `2026-07-14-refresh-remaining-color-portfolio-json-fingerprints.md`  
- Wv2: `Operations::PortfolioConfigImporter`  
- Session fix: `winston_unit_test` `internal_controller.rb` `public` for portfolio_config  

## Non-goals

- Changing engaged refuse / auto-fork semantics on Wv2  
