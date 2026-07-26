# Strategy Bakeoff V1 — PBR map (pending)

**Ticket:** `2026-07-25-strategy-bakeoff-v1-phase1`  
**Experiment:** `strategy_bakeoff_v1`  
**Fill:** `next_bar_open` · **Capital:** $10k · **Chassis:** OWD ladder A · pyr ATR 1.0 · 5/12  

Machine JSON: `ecosystem/docs/analysis/2026-07-25-strategy-bakeoff-v1-matrix.json`

## TradingStrategies

| Key | TS id | Name |
|-----|-------|------|
| S1 | **45** | BakeoffV1 S1 Elephant |
| S2 | **46** | BakeoffV1 S2 Donchian20+EMA55 |
| S3 | **47** | BakeoffV1 S3 SlowBO50NH |
| S4 | **48** | BakeoffV1 S4 FastBO5 |
| S5 | **49** | BakeoffV1 S5 StructureExit |

## PBR grid (all pending at setup)

| Portfolio | Tier | S1 | S2 | S3 | S4 | S5 |
|-----------|------|----|----|----|----|-----|
| Blue | core | 198 | 199 | 200 | 201 | 202 |
| Orange | core | 203 | 204 | 205 | 206 | 207 |
| Red | core | 208 | 209 | 210 | 211 | 212 |
| Green | core | 213 | 214 | 215 | 216 | 217 |
| Mango | core | 218 | 219 | 220 | 221 | 222 |
| Rust | core | 223 | 224 | 225 | 226 | 227 |
| White | stress | 228 | 229 | 230 | 231 | 232 |
| Pink | stress | 233 | 234 | 235 | 236 | 237 |
| Gray | stress | 238 | 239 | 240 | 241 | 242 |
| Mint | exclusive | 243 | 244 | 245 | 246 | 247 |
| Yellow | exclusive | 248 | 249 | 250 | 251 | 252 |

UI: `http://localhost:3000/wut/portfolio_backtest_runs/<id>` → Execute

## Scorecard

```bash
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_bakeoff_v1_scorecard.rb
bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_bakeoff_v1_scorecard.rb WRITE=1
```
