# Ticket: Update wut-to-wv2-handoff.md to document richer TradingStrategy export shape

**Status:** Proposed

**Date:** 2026-07-07

**Context:** Session [`2026-07-07-1752-rich-trading-strategy-export-alignment.md`](../session-reports/2026-07-07-1752-rich-trading-strategy-export-alignment.md)

We completed the alignment of the `portfolios:vet_trend` export (and Wv2 importer) on the rich first-class `TradingStrategy` structure (nested `trading_strategy` with `risk_management` / `entrance_strategy` / `risk` / `exit_strategies` + flat compat keys).

The handoff document still describes the legacy flat "Configured Portfolio" shape as primary.

## Scope

1. Update `ecosystem/docs/business-context/wut-to-wv2-handoff.md` to present the richer nested shape as the preferred/modern form for vetted portfolio exports from WUT.
2. Note that the legacy flat form remains supported by the importer during transition.
3. Update examples and "What Wv2 creates on import" table as needed.
4. Cross-link to the restructure session report and related tickets.

## Acceptance

- Handoff doc accurately reflects the rich `trading_strategy` export now produced by `PortfolioTrendVetter`.
- Legacy flat path noted but not primary.
- Cross-links present.

## Related

- Session report: `docs/session-reports/2026-07-07-1752-rich-trading-strategy-export-alignment.md`
- Ticket for tasks.json update: `docs/tickets/2026-07-07-update-portfolio-overlap-tasks-red-vet-complete.md`
- Code: `winston_unit_test/app/services/portfolio_trend_vetter.rb`, `winston_v2/lib/tasks/wv2.rake`
- Example: `portfolio_configs/portfolio-red.json`