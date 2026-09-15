# Strategy77 LEAP $30k — 7-book validation panel

**Banner:** report only — no pack promotion.
**Date:** 2026-09-14 (completed into 2026-09-15 PT)
**Experiment:** `strategy77_rst_parity_v1`
**Panel:** 668–674 (+ yellow replacement **#680**); Orange **#667** reference only.

## Doctrine
- LEAP premium Edge is **not** share-R-comparable.
- Rank **within this LEAP panel only**; Orange #667 is a **footnote reference**, not a rank peer.
- Prefer `edge_r`, `n`, PF, `total_return`, `max_dd`, and LEAP trade fidelity (`is_option` closes).

## Knobs (locked)
- TS#77 TurtleV1 S2 · `$30k` · turtle heat · risk `0.01`
- `resting_stop_touch` · `leap_fulfillment=all` · `leap_atr_offset=0` · `leap_expiration_days=730`
- Experiment: `strategy77_rst_parity_v1`

## Status table

| id | book | cell_key | status | edge_r | n | return | max_dd | PF | leap fidelity |
|----|------|----------|--------|--------|---|--------|--------|----|--------------|
| 667 †ref | orange | `orange_rst_turtle_r01_leap30k` | completed | **117.35** | 283 | +363.6% | 89.0% | 4.22 | PASS 283/283; stop=278 exp=5 20d=0 |
| 668 | blue | `blue_rst_turtle_r01_leap30k` | completed | **137.58** | 207 | +318.4% | 81.9% | 4.15 | PASS 207/207; stop=206 exp=1 20d=0 |
| 669 | mango | `mango_rst_turtle_r01_leap30k` | completed | **-33.58** | 132 | -101.1% | 167.7% | 0.44 | PASS 132/132; stop=132 exp=0 20d=0 |
| 670 | mint | `mint_rst_turtle_r01_leap30k` | completed | **-118.82** | 93 | -112.0% | 152.1% | 0.33 | PASS 93/93; stop=89 exp=4 20d=0 |
| 680 *(repl #671)* | yellow | `yellow_rst_turtle_r01_leap30k` | completed | **-43.03** | 110 | -103.9% | 150.7% | 0.22 | PASS 110/110; stop=110 exp=0 20d=0 |
| 672 | red | `red_rst_turtle_r01_leap30k` | completed | **59.43** | 215 | +133.7% | 81.8% | 2.33 | PASS 215/215; stop=215 exp=0 20d=0 |
| 673 | green | `green_rst_turtle_r01_leap30k` | completed | **-70.07** | 58 | -116.7% | 157.0% | 0.04 | PASS 58/58; stop=58 exp=0 20d=0 |
| 674 | rust | `rust_rst_turtle_r01_leap30k` | completed | **80.04** | 351 | +425.9% | 147.7% | 1.49 | PASS 351/351; stop=349 exp=2 20d=0 |

† Orange #667 reference (not ranked). Yellow original #671 and restamp #677 were **deleted mid-run** (Home stop-all destroy); #680 is the completed replacement.

## Ranking by edge_r (LEAP panel only)

| rank | id | book | edge_r | n | PF | return | max_dd |
|------|----|------|--------|---|----|--------|--------|
| 1 | 668 | blue | 137.58 | 207 | 4.15 | +318.4% | 81.9% |
| 2 | 674 | rust | 80.04 | 351 | 1.49 | +425.9% | 147.7% |
| 3 | 672 | red | 59.43 | 215 | 2.33 | +133.7% | 81.8% |
| 4 | 669 | mango | -33.58 | 132 | 0.44 | -101.1% | 167.7% |
| 5 | 680 | yellow | -43.03 | 110 | 0.22 | -103.9% | 150.7% |
| 6 | 673 | green | -70.07 | 58 | 0.04 | -116.7% | 157.0% |
| 7 | 670 | mint | -118.82 | 93 | 0.33 | -112.0% | 152.1% |

**Orange #667 reference:** edge_r=117.35, n=283, PF=4.22, return=+363.6%, max_dd=89.0%.

## Ranking by total_return (with DD callouts)

| rank | id | book | return | max_dd | edge_r | n | DD callout |
|------|----|------|--------|--------|--------|---|------------|
| 1 | 674 | rust | +425.9% | 147.7% | 80.04 | 351 | SEVERE (>140%) |
| 2 | 668 | blue | +318.4% | 81.9% | 137.58 | 207 | HIGH (≥80%) |
| 3 | 672 | red | +133.7% | 81.8% | 59.43 | 215 | HIGH (≥80%) |
| 4 | 669 | mango | -101.1% | 167.7% | -33.58 | 132 | SEVERE (>140%) |
| 5 | 680 | yellow | -103.9% | 150.7% | -43.03 | 110 | SEVERE (>140%) |
| 6 | 670 | mint | -112.0% | 152.1% | -118.82 | 93 | SEVERE (>140%) |
| 7 | 673 | green | -116.7% | 157.0% | -70.07 | 58 | SEVERE (>140%) |

## Glance findings
1. **Blue #668 tops LEAP edge_r (137.6)** and beats Orange reference edge (117.4) with still-high DD (~82%) but better than Orange DD (~89%). Return +318% trails Orange +364% and Rust +426%.
2. **Rust #674 tops return (+426%)** with broadest n (351) but **severe DD 148%** and only middling PF (1.49) — cosmetic return, not packable under LEAP accounting.
3. **Four books destroyed capital** (mango/mint/yellow/green): negative edge, PF≪1, DD 150–168%. Mint is worst on edge (−118.8); Green worst on PF (0.04) with only n=58.
4. **Red #672** is the only other positive book: edge 59.4, return +134%, DD ~82%, PF 2.33 — solid third on edge, third on return.
5. LEAP fidelity: all completed cells show `is_option` / premium / extra_modal on essentially all closes; 20-Day Breakout exits remain 0 (S2 under-max suppression).

## Ops incidents (documented, no pack promotion)
- PBR #671 (yellow) deleted while running (~53%) — likely Home#stop_all_running destroy
- PBR #677 (yellow restamp) deleted while running (~42%) — same stop-all hazard
- PBR #680 (yellow) completed via sync PortfolioBacktestRunner after Sidekiq starvation (DmRegistrySyncJob + OA runs 678/679)
- winston_unit_test_sidekiq container restart orphaned 671/673/674 mid-first-pass; 673/674 re-executed successfully

## Artifacts
- `ecosystem/docs/analysis/2026-09-14-strategy77-leap30k-7book-panel.md`
- `ecosystem/docs/analysis/2026-09-14-strategy77-leap30k-7book-panel.json`
- Orange reference: `ecosystem/docs/analysis/2026-09-14-pbr667-orange-leap30k-attempt.md`

