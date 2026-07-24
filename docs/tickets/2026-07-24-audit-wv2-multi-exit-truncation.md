# Ticket: Audit Wv2 TradingStrategies for truncated multi-exit

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-24  
**Domain:** WUT → Wv2 handoff, TradingStrategy methodology fidelity  
**Monoliths:** winston_v2 (data), winston_unit_test (export history)  
**See:** [session report](../session-reports/2026-07-24-1050-elephant-pbr-multi-exit-export.md); related export fix in WUT `PortfolioConfigExporter#exit_names`

## Problem

WUT multi-exit recipes store the full OR list in `strategy_config_json["exit_strategy_ids"]` but historically exported only the singular FK `exit_strategy_id` (first exit). Mint/Yellow Elephant and at least one other Wv2 TS (#112) landed without `VolatilityExitStrategy` even when names/descriptions implied dual exits.

Elephant OP#311/#330 and TS#112/#113/#126 were patched live on 2026-07-24. Other historical imports may still be truncated.

## Desired outcome

1. Script or one-shot rails runner lists every Wv2 `TradingStrategy` where:
   - `exit_strategy_names` length is 1, and  
   - name/description/fingerprint provenance suggests multiple exits (e.g. contains `+`, `Volatility`, `and`, multiple breakout mentions), or  
   - linked WUT TS (`wut_trading_strategy_id`) has more exits than Wv2.
2. Operator-reviewed repair list; patch or re-export/re-import as appropriate.
3. Optional: assert on import that if JSON description embeds exit classes, names array covers them (soft warning).

## Acceptance

- [ ] Audit run completed against live Wv2; results filed (count + ids).
- [ ] Truncated rows repaired or explicitly waived with reason.
- [ ] No Active paper/real OP still missing VolatilityExit when methodology requires it.

## Notes

- Do **not** silently rewrite engaged OP shape via import if journals exist — patch TS methodology fields when safe.
- Prefer re-export from fixed WUT exporter when fingerprint still matches.
