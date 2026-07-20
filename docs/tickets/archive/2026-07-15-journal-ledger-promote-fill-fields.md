# Ticket: Promote journal fill fields out of JSON

**Status:** Done (2026-07-20)  
**Priority:** P1
**Date:** 2026-07-15  
**Series:** `journal-to-ledger` **#1** (foundation)  
**Analysis:** [`docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`](../analysis/2026-07-15-winston-journal-vs-trading-ledger.md)

## Problem

Fill economics live split across entities:

- **Position:** `units`, `execution_price` after open  
- **Journal:** suggested/realized cash in `flow`; confirm stores `execution_price`, `units`, `confirmed_at` inside **`fulfillment_details` JSON** only  

That blocks clean ledger export, inquiry APIs, and Telegram answers like “what did we fill?” without digging Position + JSON. Industry trading ledgers treat qty/price/time as first-class columns.

## Scope (Wv2)

1. Migration: add first-class columns on `journals`, e.g.  
   - `execution_price` (decimal)  
   - `units` (integer)  
   - `executed_at` (datetime, nullable until executed)  
   Optional later: `fees` / `commission` (nullable; not required for this ticket).  
2. `JournalConfirmationService` + any presenters write/read these columns; keep writing `fulfillment_details` for one release if useful for back-compat.  
3. Backfill best-effort from existing `fulfillment_details` + linked positions where safe.  
4. Update `InternalJournalPresenter`, daily report `serialize_journal`, MCP responses, ops shell journal view.  
5. Specs: confirm path populates columns; get_journal returns them.

## Non-goals

- Ad-hoc book without draft (series #2)  
- Stop override (series #3)  
- Fees mandatory  
- WUT schema (series #6)

## Acceptance

- [x] Confirmed journal has non-null `execution_price`, `units`, `executed_at` for stock fills  
- [x] `wv2_get_journal` / internal show expose first-class fields  
- [x] Existing draft→confirm smoke (paper OP) still green; capital_base unchanged vs prior behavior  
- [x] Analysis series table still points here as #1 foundation  

## Implementation notes (2026-07-20)

- Migration: `winston_v2/db/migrate/20260720120000_add_journal_fill_columns.rb`
  - Columns: `execution_price` (decimal 12,4), `units` (integer), `executed_at` (datetime, indexed)
  - Backfill: `fulfillment_details` → position fallback → `updated_at` for `executed_at`
- Write path: `Operations::JournalConfirmationService#persist_journal!` sets first-class columns and continues writing JSON (`execution_price` / `units` / `confirmed_at`) for one-release back-compat
- Surfaces: `InternalJournalPresenter` (MCP `wv2_get_journal`), confirm response serialize, daily report `serialize_journal`, ops shell panels + `journal` command
- Specs: `spec/services/operations/journal_confirmation_service_spec.rb`, `spec/services/internal_journal_presenter_spec.rb` (+ draft/ad-hoc/related suites green)

## Depends on / unblocks

| Relation | Ticket |
|----------|--------|
| Unblocks | #2 ad-hoc fill, #3 stop, #4 export (cleaner schema) |
| Parallel OK | #5 route cleanup, #6 WUT |

## Related code

- `winston_v2/app/models/journal.rb`  
- `winston_v2/app/services/operations/journal_confirmation_service.rb`  
- `winston_v2/app/services/internal_journal_presenter.rb`  
- `winston_v2/db/schema.rb` `journals`  

## Discovery

Search: `journal-to-ledger`, or open the analysis and follow ticket #1.  
