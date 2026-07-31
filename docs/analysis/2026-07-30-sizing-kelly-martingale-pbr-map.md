# PBR map — sizing_kelly_martingale_v1 (S / M / K)

**Date:** 2026-07-30  
**Experiment key:** `sizing_kelly_martingale_v1`  
**Ticket:** `docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md`  
**Portfolio:** Yellow (id 111)  
**DNA:** clone of lab control PBR 340 market configs (Swing BO5 + VolExit family / SimpleScaleBO5ExVolStatic shape)  
**Fill:** hybrid entry next_bar_open + pyramid price_level_touch  
**Base risk:** 2% · stop `move_to_last_entry` · max_sym 4 · max_port 12 · leverage 3  

---

## Cells

| Pack | PBR | `risk_evaluation_strategy` | Notes |
|------|-----|----------------------------|--------|
| **S** | **341** | `static` | Control under current code |
| **M** | **342** | `martingale` | Defaults: max mult 2.0, min 0.5, step 0.1 |
| **K** | **343** | `kelly` | Defaults: half-Kelly, min_trades 10, mult 0.5–2.0 |

Optional knobs live in `results_json.risk_evaluation_config` / TradingStrategy `full_config_json.risk_evaluation_config`. Empty config → strategy-class defaults (safe for existing PBRs).

Historical **PBR 340** (+97% / 50.9% DD) is the operator example path; it is **not** re-scored as the S cell. Re-run static under current runner is **341**. Absolute level vs 340 differs (open investigation: trade count 178 vs 230) — use **341/342/343** for fair side-by-side only.

---

## Scorecard (completed 2026-07-30)

| Pack | PBR | Total ret % | Max DD % | Sharpe | Trades | Final equity | Close win % | Max loss streak |
|------|-----|-------------|----------|--------|--------|--------------|-------------|-----------------|
| **S** static | 341 | **−0.8** | **40.9** | 0.12 | 178 | $9,916 | 7.8 | 49 |
| **M** martingale | 342 | **+75.7** | **98.8** | 0.84 | 168 | $17,568 | 7.7 | 43 |
| **K** kelly | 343 | **+44.5** | **39.6** | 0.33 | 181 | $14,454 | 9.5 | 49 |

Links:  
- http://localhost:3000/wut/portfolio_backtest_runs/341  
- http://localhost:3000/wut/portfolio_backtest_runs/342  
- http://localhost:3000/wut/portfolio_backtest_runs/343  

---

## Reading

1. **Martingale “works” on headline return and fails on survival.** ~99% max drawdown is a near-wipe path; not viable for capital or ops.  
2. **Kelly beats static on this panel** for return with similar/slightly better DD (~40%). Still low Sharpe; does not invent edge — only resizes.  
3. **Quiet periods / loss clusters remain** under all three (max consecutive losing closes still ~43–49). Sizing is not a signal generator.  
4. **Plumbing fix verified in spirit:** M and K diverge from S, so portfolio `trade_history` is live. Prior bug was `trade_history: []` on every entry.

---

## Implementation notes (WUT)

- `PortfolioBacktestRunner` maintains `@trade_history` and appends on each applied close.  
- `EntryRequirementCalculator` + `PositionManager.add_position` receive that history.  
- Entry risk ceiling uses `risk_eval.max_risk_fraction` so M/K/OWD are not clamped to base 2%.  
- TradingStrategy: `RISK_MANAGEMENT_STRATEGIES` includes `kelly`; export carries `risk_evaluation_strategy` + `risk_evaluation_config` for Wv2 later.

---

## Provisional recommendation

| Policy | Lab call |
|--------|----------|
| Martingale | **Reject** for real capital (ruin DD) |
| Kelly (defaults) | **Interesting** — better than static here; needs more panels + fill honesty before ops |
| Static | Control; Yellow BO5 static DNA weak on this re-run |

Follow-ups: re-run matrix on Blue OWD DNA; half-Kelly sensitivity; capture TradingStrategy fingerprints for K-winner if promoted.
