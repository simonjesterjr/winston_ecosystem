# Lab close-out — Mango/Rust rescue and Mint/Yellow risk-transfer

**Date:** 2026-09-04  
**Fill:** `next_bar_open` (stamped; unstamped lab default is rejected hybrid price-level)  
**Gates (unchanged):** return ≥ 0%, max drawdown ≤ 50%, trades ≥ 20  
**Tickets:** `2026-07-12-re-vet-mango-rust-trade-ready`, `2026-07-23-mint-yellow-risk-transfer-matrix`

## 1. Mango / Rust — keep observation

First-pass winners (Breakout5 + VolatilityExit) missed the drawdown gate. Blue-style One-Way Dynamic (OWD) R1 + `max_markets=4` and Yellow-style One-Way Dynamic Close (OWDC) were tried on honest next-bar-open fills. Neither book passed.

| Cell | PBR | Return | Max DD | Sharpe | Trades | Kind |
|------|-----|--------|--------|--------|--------|------|
| Mango OWD R1 m12 k4 | 538 | −27.3% | 91.5% | 0.54 | 272 | observation |
| Mango OWDC R1 m12 k4 | 539 | +205.4% | **54.6%** | 0.63 | 60 | observation (DD) |
| Rust OWD R1 m12 k4 | 540 | −34.5% | 93.4% | 0.26 | 131 | observation |
| Rust OWDC R1 m12 k4 | 541 | +257.0% | **65.5%** | 0.75 | 72 | observation (DD) |

**Root cause:** membership + short breakout still blow the 50% drawdown cap once fill is next-bar-open. OWDC lifts return vs OWD but does not get under the cap (Mango misses by 4.6 points, Rust by 15.5). Earlier Mango OWD PBRs 391–394 that *looked* trade-ready used **rejected** `hybrid_entry_next_pyramid_price_level` — not promotable.

**Decision:** keep existing observation Operational Portfolios (OPs) — Mango **#385**, Rust **#11**. No new export. No successor import.

JSON: `portfolio_configs/mango-rust-rescue-results.json`.

## 2. Mint / Yellow — Blue R1 does not transfer

Vet winners: opt#47/#48 Breakout50NoHistory + VolatilityExit. Capacity / R1 ladder copied from Blue PBR 48/62 doctrine.

### Mint (exclusive, 10 books) — no cell

Every next-bar-open cell lost money and failed drawdown. Best of a bad set is still observation.

| Cell | PBR | Return | Max DD | Sharpe |
|------|-----|--------|--------|--------|
| static m12 k4 swap | 542 | −53.2% | 82.7% | −0.15 |
| R1 m12 k4 | 545/547/549 | −66.0% | 81.9% | −0.20 |
| R1 m10 k4 | 543 | −74.4% | 89.8% | −0.30 |
| R1 m11 k4 | 544 | −91.4% | 99.3% | −0.19 |
| R3 m12 k4 | 548 | −78.5% | 91.3% | −0.38 |
| R1 m10 k=nil | 546 | −129.0% | 118.6% | −0.30 |

**Recommend:** do **not** paper the Mint vet-winner + R1. Live paper Mint Turtle S2 **#797** (1% static Breakout55/20) stays the Mint observation.

### Yellow (exclusive, 17 books) — static beats R1

| Cell | PBR | Return | Max DD | Sharpe | Trades | Kind |
|------|-----|--------|--------|--------|--------|------|
| **static m12 k4 swap** | **550** | **+424.7%** | **38.8%** | **0.90** | 139 | **trade_ready** |
| R1 m10 k=nil | 554 | +269.1% | 47.9% | 0.76 | 334 | trade_ready |
| R1 m11 k4 | 552 | +121.1% | 40.6% | 0.49 | 229 | trade_ready |
| R1 m12 k4 (± swap / winner-exits) | 553/555/557 | +115.9% | 40.6% | 0.48 | 245 | trade_ready |
| R1 m10 k4 | 551 | +114.3% | 40.6% | 0.48 | 232 | trade_ready |
| R3 m12 k4 | 556 | +89.6% | **76.7%** | 0.43 | 188 | observation |

Blue accelerating R1 **hurts** Yellow vs static on this chassis. Uncapped markets (k=nil) is the best R1 cell and still trails static.

**Recommend fingerprint from this matrix:** PBR **550** → WUT TradingStrategy **#101** `64a02b74…` (static, Breakout50NoHistory + VolExit, m12 k4, swap on, `export_kind=trade_ready`). **Do not activate.** Live Yellow paper is Turtle S1 **#798**. Inactive trade-ready Yellow OWDC-none **#1400** (PBR 353) already covers the close-out recipe. A third Active Yellow would need FORCE.

JSON: `portfolio_configs/mint-yellow-risk-transfer-results.json`.

## 3. What this is not

- Not a first-pass `vet_trend` re-grid (doctrine closed as dead end).
- Not a reason to rebuild Mango/Rust/Blue membership.
- Not a reason to make OWD the live Trend Following default.
