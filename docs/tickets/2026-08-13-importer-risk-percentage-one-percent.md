# Ticket: Importer treats risk_percentage 1.0 as 100%

**Status:** Done — importer `>= 1` store convention 2026-08-13  
**Priority:** P1  
**Date:** 2026-08-13  
**Monolith:** winston_v2  
**Mode:** normal  
**Graph nodes:** winston_v2, ecosystem  
**See:** session [`2026-08-13-1528-turtle-paper-handoff.md`](../session-reports/2026-08-13-1528-turtle-paper-handoff.md); `Operations::PortfolioConfigImporter`; handoff `2026-08-13-handoff-mint-s2-yellow-s1-observation.md`

## Problem

WUT `PortfolioConfigExporter` writes lab fraction `0.01` as top-level **`risk_percentage: 1.0`** (percent units). Wv2 import then does:

```ruby
risk_pct = risk_pct_raw.to_f
risk_pct = risk_pct > 1 ? risk_pct : (risk_pct * 100)
```

`1.0` is not `> 1`, so it becomes **stored 100**. `PositionSizer.base_risk_fraction_for` then treats 100 as 100% of capital per lot.

Caught on Turtle handoff (Mint #797 / Yellow #798) before activate. Live OPs patched to stored `1.0`. Sizer now uses `>= 1.0` as percent (1.0 = 1%). JSON files use `0.01` as a re-import workaround. **Importer is still wrong.**

## Scope

1. Normalize import so 1% chassis stores `1.0` (same convention as existing OPs storing `2.0` for 2%).  
2. Spec: JSON `1.0`, `0.01`, and `2.0` all land as 1% / 1% / 2% after sizer.  
3. Do not invent a second store convention; keep percent-on-column + sizer `>= 1.0`.  
4. Re-import of the Turtle JSON files must not 100× again.

## Acceptance

- [x] Importer spec covers the 1.0 boundary  
- [x] JSON `1.0` and `0.01` both store `1.0`, sizer 1% (`0.01` is the Turtle file workaround)  
- [x] Existing 2.0 / 0.02 paths unchanged  

**Landed 2026-08-13:** `risk_pct > 1` → `risk_pct >= 1` in `Operations::PortfolioConfigImporter`. Specs in `portfolio_config_importer_spec.rb` (`risk_percentage store convention`). Live #797/#798 already patched last session — **do not re-import during organic DAR**. Compose restart not required for live OPs.

## Non-goals

- Changing lab exporter units (optional later)  
- Recalculating historical OPs other than documenting the trap  
