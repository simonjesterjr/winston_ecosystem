# Ticket: Confirm no handoff path still uses singular exit only

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-24  
**Domain:** WUT → Wv2 handoff, multi-exit OR semantics  
**Monoliths:** winston_unit_test  
**See:** [session report](../session-reports/2026-07-24-1050-elephant-pbr-multi-exit-export.md); sibling [`2026-07-24-audit-wv2-multi-exit-truncation.md`](2026-07-24-audit-wv2-multi-exit-truncation.md)

## Problem

Multi-exit is dual-stored on PBR market configs:

| Field | Role |
|-------|------|
| `exit_strategy_id` | Legacy singular FK (first exit only) |
| `strategy_config_json["exit_strategy_ids"]` | Full OR list |

Any exporter/API that maps only the FK drops secondary exits (commonly `VolatilityExitStrategy`). Fixed in this session for:

- `PortfolioConfigExporter#exit_names`
- `PortfolioTrendVetter#export_run!` exit collection
- `InternalController#strategy_config` (run path)

Other call sites may still read singular only (e.g. single-market BR fan-out, ad-hoc scripts, MCP helpers, views).

## Desired outcome

1. Grep/audit WUT for `exit_strategy&.strategy_class`, `exit_strategy_id` without `exit_strategy_ids` / `exit_strategy_id_list`.
2. Prefer `PortfolioBacktestMarketConfig#exit_strategy_id_list` / `#exit_strategy_classes` everywhere methodology is serialized.
3. Spec or invariant: if market config has multi-exit JSON, export/API never returns a shorter class list.
4. Note any intentional singular uses (UI display of “primary” exit) vs bugs.

## Acceptance

- [ ] Inventory of remaining singular-only readers with fix or waive.
- [ ] Handoff paths (export_config, internal portfolio_config, strategy_config, trend vetter export) all multi-exit green.
- [ ] Regression covered by existing exporter multi-exit example (extend if new path found).

## Notes

- Runtime backtest (`PortfolioBacktestRunner`) already multi-exit aware — do not regress that path.
- Fingerprint capture already used multi-exit correctly.
