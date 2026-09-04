# Ticket: Yellow OWDC + scale=none as paper candidate (from matrix)

**Status:** Done — captured, exported, imported inactive paper 2026-09-04  
**Priority:** P2  
**Date:** 2026-07-31  
**Monolith:** WUT lab → Wv2 paper path  
**Session:** `docs/session-reports/2026-07-31-1556-risk-scale-matrix-findings.md`

---

## Problem

Among scale=none cells on Yellow 17-book pack:

| Base | PBR | Ret | Max DD | Sharpe |
|------|-----|-----|--------|--------|
| OWDC | **353** | **+176%** | **39%** | **0.64** |
| OWD | 345 | +143% | 49% | 0.56 |
| static | 349 | −0.8% | 41% | 0.12 |

OWDC-none is the standout **base** recipe from the matrix. Not auto-promoted to capital.

## Desired outcome

1. Capture/promote TradingStrategy from PBR 353 (or re-export clean fingerprint).  
2. Run viability / paper hygiene per existing ops (observation vs trade_ready).  
3. Do **not** attach Kelly/Martingale scale for first paper band.  

## Acceptance

- [x] TS captured with base OWDC + scale none  
- [x] Paper OP path decided (import / activate paper)  
- [x] Link PBR 353 in provenance

---

## Close-out (2026-09-04)

| Artifact | Id |
|----------|----|
| WUT PBR | **353** Yellow, OWDC, scale=none, fill `hybrid_entry_next_pyramid_same_day` |
| Gates | **trade_ready** — return +176.1%, max DD 39.0%, 193 trades |
| WUT TradingStrategy | **#100** fingerprint `33d2063c…` `one_way_dynamic_close` |
| Export | `portfolio_configs/portfolio-yellow-owdc-none-pbr353.json` |
| Wv2 OP | **#1400** `Portfolio Yellow · 33d2063c` paper, **inactive**, `export_kind=trade_ready` |
| Wv2 TS | **#318** |

**Paper path:** land inactive. Do **not** activate. Active Yellow is Turtle S1 **#798**. Dual-Active same seed needs FORCE; operator did not ask to displace Turtle.

Importer applied paper caps: `max_markets` 4 (lab was 17), `max_leverage` 1.0 (lab 3.0). No Kelly/Martingale scale.

Provenance: `wut_backtest_run_id=353`, `wut_trading_strategy_id=100`.  

## Related

- Close-trigger / OWDC prior science  
- Matrix findings session report  
