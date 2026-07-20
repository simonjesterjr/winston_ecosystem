# Ticket: Operational portfolio journal ledger export (CSV → PDF)

**Status:** Proposed  
**Priority:** P2
**Date:** 2026-07-15  
**Series:** `journal-to-ledger` **#4**  
**Analysis:** [`docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`](../analysis/2026-07-15-winston-journal-vs-trading-ledger.md)

## Problem

WUT has mature **CSV `export_journal`** for backtest runs. Wv2 has a strong **Daily Activity Report PDF** (ops narrative: next steps, open positions, equity) but **no portfolio-scoped trading ledger export**. Operators cannot dump executed journals for audit, coach review, or desk archive. Word (.docx) is absent; start with CSV + optional PDF.

## Scope (Wv2 primary)

1. **CSV export** for one Operational Portfolio (id or name), optional `from` / `to` dates:  
   Align columns with WUT where sensible, e.g.  
   Date · Status · Market · Debit/Credit · Units · Execution price · Flow · Run capital · MTM · Position id · Direction · Stop(s) · Fulfillment · Notes · Executed at  
2. Service e.g. `Operations::JournalLedgerExporter` (or under `ReportArtifactBuilder` family).  
3. Surfaces:  
   - Internal `GET /internal/portfolios/:id_or_name/journal_export?format=csv` (or query param portfolio)  
   - MCP tool e.g. `wv2_export_journal` returning path or inline summary + file path under `storage/reports/`  
   - Ops shell: `export [id|name]`  
4. **PDF** (phase B of same ticket if small, else follow immediately): chronological table subset + capital summary; reuse Prawn patterns from DAR, **do not** replace DAR.  
5. **Word (.docx):** out of scope for this ticket unless trivial; file as follow-up note if still needed after PDF.

## Non-goals

- Replacing Daily Activity Report  
- Broker Flex / tax formats  
- Full WUT expected-return dump on live journals  

## Acceptance

- [ ] CSV for focus paper OP includes all executed journals in range with units/price/stop join  
- [ ] Export does not mutate positions/journals  
- [ ] MCP or internal path + audit correlation where applicable  
- [ ] Analysis export section can mark “ledger CSV” as done when shipped  
- [ ] Document path convention under `winston_v2/storage/reports/`  

## Depends on / unblocks

| Relation | Ticket |
|----------|--------|
| Prefer after | #1 fill fields (cleaner columns), #2–#3 so ad-hoc + stops appear in export |
| Can start CSV early | Join Position for units/price if #1 not done yet |

## Pattern to reuse

- WUT `BacktestRunsController#export_journal` / `PortfolioBacktestRunsController#export_journal`  
- Wv2 `DailyActivityReportPdfRenderer` (PDF layout only)  

## Discovery

Search: `journal-to-ledger`, analysis § Export, series ticket #4.  
