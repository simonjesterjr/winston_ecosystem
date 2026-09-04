# Trade-Ready Viability Gates

**Type:** Domain rule  
**Glossary:** `CONTEXT.md` — **Viability Gates**, **Trade-Ready Portfolio**, **Observation Portfolio**  
**Status:** Agreed in grill session 2026-07-07. Thresholds remain placeholders. Doctrine/gates review closed as operator dead end 2026-09-04 (`docs/tickets/archive/2026-07-09-first-pass-doctrine-gates-review.md`) — do not retune.

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

## Closed (not open work)

- **2026-09-04:** first-pass doctrine / gates review will not retune thresholds or `FIRST_PASS_BASE_CONFIG`. Gates remain labels for `export_kind`.
- Blue membership post-mortem closed: keep the 11-name book; OWD + capacity rescued economics (see archived `2026-07-07-revisit-portfolio-blue-membership-strategy.md`).

## Related

- Ticket: `docs/tickets/2026-07-07-portfolio-trading-strategy-evaluation-framework.md`
- Session: `docs/session-reports/2026-07-06-2020-portfolio-overlap-pipeline.md`