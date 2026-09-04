# Ticket: Re-vet Portfolio Mango and Rust for trade-ready gates

**Status:** Done — keep observation 2026-09-04  
**Priority:** P2

**Date:** 2026-07-12  

**Context:** Phase 6 cohort vet_trend (2026-07-12). Green and Pink passed viability gates; Mango and Rust failed **max drawdown ≤ 50%**.

## Results (validation winners)

| Portfolio | Strategy | Return | Max DD | Trades | export_kind |
|-----------|----------|--------|--------|--------|-------------|
| Mango | Breakout5Day + VolExit | +671% | **55.0%** | 814 | observation |
| Rust | Breakout5Day + VolExit | +685% | **77.4%** | 496 | observation |

## Problem

Observation-only paper is fine short-term, but Mango/Rust cannot open real capital by default without trade-ready provenance. High returns with extreme DD suggest membership and/or strategy grid need another pass.

## Scope

1. Diagnose DD drivers (membership concentration, short breakout + vol exit, capital/risk base config)  
2. Options: re-membership under corr_v2; expand strategy grid; ranking metric experiment; risk/capital params  
3. Re-run `portfolios:vet_trend` with EXPORT; aim `export_kind: trade_ready`  
4. Re-import Wv2 only if fingerprint/export changes (successor hygiene if engaged)

## Acceptance

- [x] Root-cause note in analysis or session report  
- [x] New export labeled trade_ready **or** documented decision to keep observation  
- [x] Wv2 OP updated without silent mutate of engaged series  

## Related

- Exports: `portfolio_configs/portfolio-mango.json`, `portfolio-rust.json`  
- Gates: `docs/business-context/trade-ready-viability-gates.md`  
- Blue membership revisit closed 2026-09-04 (keep book; OWD+capacity rescued)

## 2026-09-04 approach

Do **not** re-run first-pass `vet_trend` (static grid + DD 50% abort). Operator closed that doctrine as a dead end.

Existing Mango OWD PBRs 391–394 that pass gates used **rejected** `hybrid_entry_next_pyramid_price_level` fill — not promotable.

Running `lib/scripts/mango_rust_rescue.rb`: Breakout5 + VolExit, **next_bar_open**, scale=none:

| Cell | Risk | Caps |
|------|------|------|
| OWD-R1-m12-k4 | `one_way_dynamic` R1 | max_pos 12, max_markets 4 |
| OWDC-R1-m12-k4 | `one_way_dynamic_close` R1 | same |

Then score against unchanged gates (return ≥0, max DD ≤50%, trades ≥20). Wv2 import only if a cell is trade_ready **and** fingerprint differs from engaged #385 / #11.

---

## Close-out (2026-09-04)

**Keep observation.** No trade-ready export. Did not mutate engaged Wv2 OPs #385 (Mango) or #11 (Rust).

| Cell | PBR | Return | Max DD | Kind |
|------|-----|--------|--------|------|
| Mango OWD R1 | 538 | −27.3% | 91.5% | observation |
| Mango OWDC R1 | 539 | +205.4% | 54.6% | observation (DD) |
| Rust OWD R1 | 540 | −34.5% | 93.4% | observation |
| Rust OWDC R1 | 541 | +257.0% | 65.5% | observation (DD) |

Fill stamped `next_bar_open`. Analysis: [`business_analysis/2026-09-04-mango-rust-mint-yellow-lab.md`](../../business_analysis/2026-09-04-mango-rust-mint-yellow-lab.md). Results JSON: `portfolio_configs/mango-rust-rescue-results.json`.  
