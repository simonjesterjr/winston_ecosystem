# Pyramid price-level (resting stop) panel — S4 frozen pack

**Experiment:** `hybrid_fill_price_level_v1`  
**Ticket:** `2026-07-26-hybrid-fill-price-level-pyramid`  
**Status:** **3/3 completed** (scored 2026-07-26)  
**TS:** #48 FastBO5  

## Call (freeze)

| Decision | Value |
|----------|--------|
| Adopt price-level pyramids for S4 pack? | **No** |
| Keep pure `next_bar_open` pyramids? | **Yes** |
| Broker “park stop at next ATR level” priority from this panel? | **No** |

**Same family of outcome as same-day-close hybrid:** path-destructive vs pure next_bar on Blue/Mango/Yellow. Median Δret **−200**, Δdd **+20**, Δcagr **−20**, pyramid fills **down** (not more scale-ins).

---

## Doctrine tested

| Arm | Entry | Pyramid |
|-----|-------|---------|
| next_bar (baseline) | T+1 open | T+1 open after close clears level |
| **price_level** | T+1 open | Resting stop at last_entry±N×ATR; OHLC touch fill |

Integrity: ATR from last-lot bar; only sessions after last lot.

## Chassis

Frozen S4 pack: ladder A / 2% · pyr ATR **1.0** · max_sym **4** · max_port **12** · $10k

## Results (side-by-side)

| Portfolio | Price-level ret / DD / CAGR / trades / pyr | Next_bar ret / DD / CAGR / trades / pyr | Δret | Δdd | Δcagr | Δpyr |
|-----------|--------------------------------------------|------------------------------------------|------|-----|-------|------|
| Blue **331** vs **305** | **−96 / 98 / −41 / 153 / 0** | **+204 / 53 / +21 / 203 / 3** | **−300** | **+44** | **−62** | −3 |
| Mango **332** vs **311** | +111 / 48 / +13 / 207 / 1 | +182 / 38 / +19 / 161 / 4 | **−71** | +10 | −6 | −3 |
| Yellow **333** vs **324** | **−34 / 77 / −6 / 305 / 0** | +166 / 57 / +15 / 319 / 2 | **−200** | +20 | −20 | −2 |

### Paired medians (n=3)

| Metric | Price-level − next_bar |
|--------|-------------------------|
| Med Δ return% | **−199.9** |
| Med Δ max DD% | **+20.1** |
| Med Δ CAGR% | **−20.2** |
| Med Δ pyramid fills | **−3** |

## Interpretation

1. Resting price-stops did **not** increase pyramid engagement (0–1 fills vs 2–4 on next_bar).  
2. Paths still diverged sharply — Blue and Yellow destroyed; Mango retained positive return but far behind next_bar.  
3. Combined with same-day-close hybrid rejection: **neither faster pyramid fill model beats pure next_bar_open on this pack.**  
4. Scale-in timing under next-bar-open + portfolio heat remains a **path-selection** problem, not “fill closer to the stop = free alpha.”

**Working pack fill (unchanged):** pure `next_bar_open` for entry and pyramid.

## Score command

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/hybrid_fill_price_level_scorecard.rb
```
