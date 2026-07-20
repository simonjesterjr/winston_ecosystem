# Ticket: Vet Portfolio Orange trend strategies

**Status:** Done (2026-07-09)

**Date:** 2026-07-08

**Last updated:** 2026-07-09 — opt#33 / PBR 41; export observation

**Context:** Session [`2026-07-08-1744-portfolio-overlap-orange-white-eval-gates`](../session-reports/2026-07-08-1744-portfolio-overlap-orange-white-eval-gates.md). Orange membership built (GLTR, 15 markets). Evaluation gates + `export_kind` live in WUT.

**Result:** [`2026-07-09-1308-orange-white-vet-trend`](../session-reports/2026-07-09-1308-orange-white-vet-trend.md) — winner `Breakout5DayStrategy` + paired opposite; return +7.2%, max DD 96.5%, trades 1912; `portfolio-orange.json` `export_kind=observation`.

## Membership (15)

AAPL, BITQ, COPR, FPA, GLTR, IBM, MSOS, NVDA, RXT, SMH, VXX, WMT, XLF, XLK, ZROZ

## Scope

1. Run detached:  
   `env PORTFOLIO="Portfolio Orange" EXPORT=/portfolio_configs/portfolio-orange.json bin/rails portfolios:vet_trend`
2. Confirm optimization completes; winner PBR on full overlap.
3. Export includes `export_kind` + `vetting.viability` via `TradeReadyViabilityGates`.
4. Record winner metrics in plan or session note.

## Acceptance

- Vet log + `portfolio-orange.json` present
- `export_kind` is `trade_ready` or `observation` with gate failures listed
- Not imported to Wv2 as live capital unless `trade_ready`

## Related

- Plan task #6: `plans/portfolio-overlap-rebuild.md.tasks.json`
- Ticket: `2026-07-07-portfolio-trading-strategy-evaluation-framework.md`
