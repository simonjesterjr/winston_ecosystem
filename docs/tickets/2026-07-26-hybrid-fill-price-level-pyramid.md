# Ticket: Pyramid price-level fills (resting stop at last_entry ± N×ATR)

**Status:** Scored — **reject**; keep pure next_bar pyramids  
**Priority:** P1  
**Date:** 2026-07-26  
**Monolith:** winston_unit_test  
**Experiment:** `hybrid_fill_price_level_v1`  
**Map:** `docs/analysis/2026-07-26-hybrid-fill-price-level-pbr-map.md`  

---

## Score summary (2026-07-26)

| Portfolio | Price-level | Next_bar | Δret | Δdd | Δpyr |
|-----------|-------------|----------|------|-----|------|
| Blue 331 vs 305 | −96 / 98 | +204 / 53 | **−300** | +44 | −3 |
| Mango 332 vs 311 | +111 / 48 | +182 / 38 | −71 | +10 | −3 |
| Yellow 333 vs 324 | −34 / 77 | +166 / 57 | **−200** | +20 | −2 |

**Med Δ:** ret **−200**, dd **+20**, cagr **−20**, pyr **−3**.

### Freeze

- Do **not** adopt price-level pyramid fills for S4 pack default.  
- Do **not** prioritize broker “park stop at next ATR” automation from this panel.  
- Keep pure **`next_bar_open`** for entry and pyramid.  
- Aligns with same-day-close hybrid rejection: faster pyramid fills ≠ better pack economics under heat + T+1 entry queue.

## Acceptance

- [x] Code + specs  
- [x] 3 PBRs completed vs baselines  
- [x] Written freeze: keep pure next_bar  

## Code retained

`hybrid_entry_next_pyramid_price_level` remains a lab switch for future experiments — not pack default.
