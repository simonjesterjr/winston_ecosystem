# Portfolio Trading Strategy Evaluation — First Pass

**Status:** Agreed 2026-07-07 (grill session + first-pass backtest spec)  
**Implements:** P0 ticket `docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md`

## First-pass grid (Option A — small, fast)

| Dimension | Value |
|-----------|-------|
| Entries | 6 breakout classes (see `PortfolioTrendVetter::ENTRY_STRATEGY_CLASSES`) |
| Exits | 2 per entry: **opposite breakout** (same class, paired) + **VolatilityExitStrategy** |
| Combinations | 12 (6 × 2), full 5-year window, no screening subset |
| Starting capital | **$10,000** per backtest |
| Ranking | `practical_sharpe_ratio` (with viability gates on export — see trade-ready doc) |

## Fixed components (pass 1)

| Component | Setting | Rationale |
|-----------|---------|-----------|
| Stops | ATR-based (`atr_multiplier: 2`) | Standard trend risk unit |
| Stop trail | `move_to_last_entry` | Stops move to last pyramid entry |
| Risk | 2% static per trade | `risk_evaluation_strategy: static` |
| Pyramid | On each 1× ATR move | `pyramid_atr_multiplier: 1.0` |
| Max pyramid / market | 5 positions | `max_positions_per_symbol: 5` |
| Max open positions | 12 portfolio-wide | `max_positions_per_portfolio: 12` |
| Max open markets | 4 concurrent | `max_markets_per_portfolio: 4` |
| 13th signal | Swap if better ER | Close least-risk open position when incoming signal beats weakest by expected return |
| Ignore first signal | true | Avoid cold-start entries |
| Always in market | false | Observation / trend follower default |

## Code entry points

- `PortfolioTrendVetter::FIRST_PASS_BASE_CONFIG` — canonical defaults
- `portfolios:vet_trend` rake — runs 6×2 grid
- `PortfolioBacktest::PositionSwapEvaluator` — 13th-signal / capacity swap
- Viability gates: `docs/business-context/trade-ready-viability-gates.md`

## Export paths

- **Trade-Ready Portfolio** — passes viability gates
- **Observation Portfolio** — sub-breakeven winner; Wv2 paper/regime only

## Open (later passes)

- Confirmational entries, combined exits, screening subset tuning
- Ranking fallback when `practical_sharpe_ratio` is null
- Regime filters, membership vs strategy post-mortem template