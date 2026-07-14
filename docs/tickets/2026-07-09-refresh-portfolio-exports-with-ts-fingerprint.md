# Ticket: Refresh portfolio JSON exports with TradingStrategy id/fingerprint

**Status:** Done (2026-07-14 Phase 3 PR 4)

**Date:** 2026-07-09

**Context:** Session [`2026-07-09-0833-trading-strategy-fingerprint-capture`](../session-reports/2026-07-09-0833-trading-strategy-fingerprint-capture.md). Capture sets fingerprint on new vet exports; historical files lagged. **ADR-006** makes fingerprint the lineage key.  
**Plan:** [`plans/paper-telegram-phase3-adr006.md`](../../plans/paper-telegram-phase3-adr006.md) PR 4.

## Problem

Silent bare-name import when fingerprint missing. Paper focus `portfolio-blue-pbr62.json` had no fingerprint.

## Scope

1. Re-export or patch `portfolio_configs/portfolio-*.json` with nested `wut_trading_strategy_id`, `fingerprint`.
2. Prefer re-run of export path from existing validation PBR.
3. Document export rake options.
4. Match handoff provenance shape.

## Acceptance

- [x] Export path stamps fingerprint + WUT TS id when capture/selection exists (auto-capture if completed)
- [x] blue-pbr62 + red refreshed with fingerprints
- [x] Wv2 import uses lineage (smoke: fork, not bare-name wipe of `#12`)

## Delivered

- WUT `wut:portfolios:export_config` — fingerprint resolution, `PAPER_CAPS=1`, `SEED_NAME` / `DISPLAY_NAME`
- Captured TS#23 for PBR 62 (`c7788d2e…`)
- Host files: `portfolio_configs/portfolio-blue-pbr62.json`, `portfolio-red.json` (not in monolith git — tracking ticket remains)

## Related

- Import lineage Done PR 2
- Paper caps: `2026-07-13-enforce-paper-max-markets-and-leverage.md`
