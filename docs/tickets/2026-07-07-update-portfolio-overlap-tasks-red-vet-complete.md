# Ticket: Update portfolio-overlap-rebuild.md.tasks.json after rich TradingStrategy export alignment

**Status:** Proposed

**Date:** 2026-07-07

**Context:** [`2026-07-07-1752-rich-trading-strategy-export-alignment.md`](../session-reports/2026-07-07-1752-rich-trading-strategy-export-alignment.md)

We completed the major restructure of the `portfolios:vet_trend` export path (PortfolioTrendVetter + Wv2 importer) to use the rich first-class `TradingStrategy` nested structure instead of the legacy flat shape.

## Problem

The tasks.json still shows:
- Task #2 "Vet Portfolio Red (portfolios:vet_trend)" as `pending` (blockedBy [5])
- Task #5 framework note still lists "export_kind + viability gates in vet_trend, ... re-vet Red/Blue" as remaining

The export structure alignment is now done (the core of the vet + framework work for this phase).

## Scope

1. Mark task #2 as `done` (or `completed`).
2. Update task #5 note: remove "re-vet Red/Blue" from remaining, note that export structure is now using rich nested `trading_strategy` (with `risk_management`, `entrance_strategy`, `risk`, etc.).
3. Add cross-links to the session report and the new ticket for the restructure work.
4. Optionally bump framework progress % in the note.

## Acceptance

- tasks.json accurately reflects that Red vet is complete and the export alignment (part of framework) is delivered.
- Cross-links present in report §14 and this ticket.

## Related

- Plan: `plans/portfolio-overlap-rebuild.md`
- Session report: `docs/session-reports/2026-07-07-1752-rich-trading-strategy-export-alignment.md`
- Main work: `winston_unit_test/app/services/portfolio_trend_vetter.rb`, `winston_v2/lib/tasks/wv2.rake`, `portfolio_configs/portfolio-red.json` (example)