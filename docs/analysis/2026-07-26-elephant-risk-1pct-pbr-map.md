# Elephant risk 1% side-panel — PBR map

**Experiment:** `elephant_risk_1pct_v1`  
**Ticket:** `2026-07-25-strategy-bakeoff-v1-phase1`  
**Fill:** `next_bar_open` · capital $10k · same chassis as bakeoff except risk pack  

## Risk packs

| Pack | Ladder long | Ladder short | `risk_percentage` |
|------|-------------|--------------|-------------------|
| `half_ladder` | 1 → 1.5 → 2 → 3 → 3% | 1 → 1 → 1 → 1.5 → 1.5% | 1% |
| `flat_1pct` | 1% × 5 | 1% × 5 | 1% |

## Grid (16 pending)

### S1 Elephant (TS #45)

| Portfolio | half_ladder | flat_1pct | Bakeoff baseline (ladder A / 2%) |
|-----------|-------------|-----------|----------------------------------|
| Blue | **253** | **254** | 198 |
| Orange | **255** | **256** | 203 |
| Mango | **257** | **258** | 218 |
| Green | **259** | **260** | 213 |
| Rust | **261** | **262** | 223 |

### S4 FastBO5 control (TS #48)

| Portfolio | half_ladder | flat_1pct | Bakeoff baseline |
|-----------|-------------|-----------|------------------|
| Blue | **263** | **264** | 201 |
| Orange | **265** | **266** | 206 |
| Mango | **267** | **268** | 221 |

UI: `http://localhost:3000/wut/portfolio_backtest_runs/<id>` → Execute

## Score after runs

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/elephant_risk_1pct_scorecard.rb
```

Compares each cell to bakeoff_v1 same portfolio @ 2% ladder A.

## Questions to answer

1. Does S1 median Core path recover (ret↑, DD↓) vs bakeoff?
2. At **equal** 1% risk, does S4 still beat S1 on Blue/Orange/Mango?
3. Half-ladder vs flat 1% — shape still matter at low risk?
