# Ticket: Promote S4 FastBO5 tactics pack — transfer Mint / Yellow / Blue

**Status:** Transferred to Wv2 paper (inactive) — activate when ready  
**Priority:** P1  
**Date:** 2026-07-26  
**Monoliths:** winston_unit_test (export); winston_v2 (import)  
**Related:** bake-off Phase 1–2 freezes; hybrid fill rejected; Mint PBR 121 Elephant **not** the recipe  

---

## Frozen pack (lab truth)

| Knob | Value |
|------|--------|
| Primary | Breakout5DayStrategy |
| Confirm | none |
| Exits | VolatilityExitStrategy |
| Fill (lab) | **`next_bar_open`** (entry + pyramid) |
| Risk | OWD ladder A long 2/3/4/6 · short 2/2/2/3/3 · base **2%** |
| Pyramid ATR | **1.0** |
| Max / symbol · max pyramid | **4** |
| Max portfolio lots | **12** |
| Capital | **$10,000** |
| Stop | `move_to_last_entry` |

**Not in recipe:** hybrid same-day close, price-level pyramid stops, $20k capital, 1% unit risk.

**Supersedes for promotion:** Mint PBR **121** Elephant same-bar (~49% CAGR / 24% DD).

---

## Lab sources → Wv2 OPs

| Seed | WUT PBR | Lab ret / max DD (approx) | Export JSON | Wv2 OP | Fingerprint short | Markets |
|------|---------|---------------------------|-------------|--------|-------------------|---------|
| Portfolio Blue | **305** | +204% / 53% | `portfolio-blue-s4-p2pack.json` | **#381** · `Portfolio Blue · f4dd31eb` | `f4dd31eb` | 11 |
| Portfolio Mint | **323** | +163% / 54% | `portfolio-mint-s4-p2pack.json` | **#382** · `Portfolio Mint · 91608a22` | `91608a22` | 10 |
| Portfolio Yellow | **324** | +166% / 57% | `portfolio-yellow-s4-p2pack.json` | **#383** · `Portfolio Yellow · 2a97a043` | `2a97a043` | 17 |

- **export_kind:** `observation` (honest; not viability-gate trade_ready)  
- **execution_mode:** `paper`  
- **active:** **false** (landed inactive)  
- **force_lab_uncapped:** true (full books, not paper 4-market cap)  
- Ladder verified on import for all three  

Note: WUT capture produced **three fingerprints** (date-window metadata in capture names differs by book). Methodology knobs match; treat as one recipe family, three provenance lines.

### Lab economics note (honest next_bar)

| Book | Story |
|------|--------|
| Blue | Strong path (~21% CAGR tier / ~53% max DD on ladder-A panel) |
| Mint | Solid exclusive (~15% CAGR / ~54% DD on clean max_sym 4 baseline 323) |
| Yellow | Positive but higher DD (~15% CAGR / ~57% DD); **17 names** — heat discipline matters |

---

## Active seed conflicts (do not dual-active without FORCE)

| Seed | Currently Active OP | New S4 pack OP |
|------|---------------------|----------------|
| Blue | **#240** · 9cf64e64 | **#381** inactive |
| Mint | **#311** · 3749c990 (prior Elephant-era) | **#382** inactive |
| Yellow | **#330** · 92776cfd | **#383** inactive |

### Activate S4 pack (operator)

```bash
# Example: switch Mint attention to S4 pack
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:deactivate[311]
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:activate[382]
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate   # if desired

# Or dual-active experiment:
FORCE=1 bin/compose exec -T winston_v2 bin/rails wv2:portfolios:activate[382]
```

Same pattern for Blue 381 (vs 240) and Yellow 383 (vs 330).

### Inspect

```bash
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:inspect_strategy[381]
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:inspect_strategy[382]
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:inspect_strategy[383]
```

---

## Desk / fill doctrine (handoff)

- Lab path used **next_bar_open** for both initial entries and pyramids.  
- Live desk may still confirm fills human-gated (ADR-009); do not assume automated same-day scale-ins.  
- Hybrid / price-level pyramid labs **rejected** for pack default (2026-07-26).

---

## Acceptance

- [x] Freeze table embedded in export (max_sym 4, max_port 12, pyr 1.0, ladder A, next_bar lab)  
- [x] Export/import verified for Blue, Mint, Yellow  
- [x] Paper OPs created **#381 / #382 / #383** (inactive; operator activates)  
- [x] Note: 121 Elephant superseded for promotion  
- [x] Bake-off master + INDEX updated  

## Follow-up

- Ops audit `max_markets=` blank after uncapped import → ticket **`2026-07-26-s4-op-max-markets-book-count.md`** (set max_markets = book size 11/10/17 for clearer audits; lot heat stays 12).

## Out of scope (still)

- Live capital activate  
- Auto-deactivate prior Active OPs (left for operator)  
- Correlation unit heat  
