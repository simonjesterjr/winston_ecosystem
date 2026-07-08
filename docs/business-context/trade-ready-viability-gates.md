# Trade-Ready Viability Gates

**Type:** Domain rule  
**Glossary:** `CONTEXT.md` — **Viability Gates**, **Trade-Ready Portfolio**, **Observation Portfolio**  
**Status:** Agreed in grill session 2026-07-07 (thresholds are placeholders pending backtesting revisit)

## Purpose

Separate **Portfolio Signal Optimization** (pick a winner) from **Trade-Ready Portfolio** export (economically sane enough to promote). Sub-breakeven winners export as **Observation Portfolio** for Wv2 paper/regime watching only.

## Gates (Trade-Ready)

All must pass on the same date range used for optimization (currently full 5-year window in `portfolios:vet_trend`):

| Gate | Rule | Placeholder |
|------|------|-------------|
| Return | Total return ≥ 0% | `total_return >= 0` |
| Drawdown | Max drawdown ≤ cap | ≤ 50% (tune) |
| Activity | Minimum trade count | ≥ 20 trades (tune) |

Failure on any gate → export path is **Observation Portfolio** only (if exported at all), not **Trade-Ready Portfolio**.

## Not gates (separate concerns)

- Wv2 import does not imply live broker capital — **Operational Portfolio** may be inactive or **Paper Trading** only.
- Membership overlap / seed exclusivity — portfolio assembly rules, not strategy viability.
- Winston market suitability — DM symbol rules, not backtest economics.

## Implementation (WUT)

- Service: `TradeReadyViabilityGates` (`winston_unit_test/app/services/trade_ready_viability_gates.rb`)
- Wired into `PortfolioTrendVetter#export_run!` and `portfolios:vet_trend` summary output
- Export JSON fields: top-level `export_kind`, nested `vetting.viability`

## Open work

- Backtesting revisit ticket: tune **TradingStrategy** components comprehensively before trusting gates.
- Blue membership post-mortem (observation economics catastrophic — strategy vs membership).

## Related

- Ticket: `docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md`
- Session: `docs/session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md`