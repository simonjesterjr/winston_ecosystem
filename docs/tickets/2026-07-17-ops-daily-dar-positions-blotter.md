# Ticket: DAR last-page open positions blotter (all Active)

**Status:** Done (2026-07-17)  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Operators want a single DAR appendix: **all open positions across Active OPs**, with day movement, stop, and signal/task if any. Today open positions are partial/per-chapter only.

## Scope

1. Payload builder: cross-portfolio open blotter (real band first, then paper).  
2. Columns: OP, band, symbol, units, entry, stop, MTM/day move if available, linked draft/pending signal or task id.  
3. PDF + MD last section “Open book”.  
4. Specs for ordering and empty state.

## Acceptance

- [x] Next DAR PDF/MD ends with full Active open blotter  
- [x] Multi-Active bands labeled  

## Delivered

| Piece | Where |
|-------|--------|
| Open book builder | `winston_v2/app/services/daily_report_open_book.rb` |
| Payload `open_book` + day_move on positions | `daily_report_payload_builder.rb` |
| PDF last page “OPEN BOOK” | `daily_activity_report_pdf_renderer.rb` |
| MD last section “Open book” | `daily_activity_report_markdown_renderer.rb` |
| Specs | open_book + payload attention + MD/PDF renderers (8 ex) |

Day move = mark vs prior parquet close when available. Task id linked when next_steps/pending/actions match symbol on that OP.

## Related

- Attention bands DAR (Done)  
- Epic: `2026-07-17-ops-daily-demo-epic.md`  
