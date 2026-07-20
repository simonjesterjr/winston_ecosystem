# Ticket: Edit draft journal before confirm

**Status:** Done  
**Date:** 2026-07-17  
**Done:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

Operators can view and confirm drafts but cannot amend draft units/price/notes/stop without console. Executed journals must remain immutable.

## Scope

1. Service: edit **draft only** fields (units, suggested price, notes, stop override in details).  
2. Internal API + ops shell `edit_journal <id> …`.  
3. Refuse executed/cancelled/passed.  
4. Specs.

## Acceptance

- [x] Draft amendable from Ops UI  
- [x] Executed journal edit refused  

## Implementation (2026-07-17)

### Domain

`Operations::JournalDraftEditService` — draft only. Updates:

| Field | Storage |
|-------|---------|
| units | `fulfillment_details.units` + linked task `metadata.units` |
| price | `fulfillment_details.price` / `suggested_price` + task `metadata.price` |
| stop | `fulfillment_details.stop_price` + task `metadata.stop_price` |
| notes | journal.notes (append by default; `replace_notes=true` replaces) |
| trade_date | journal.trade_date |
| type / LEAP fields | fulfillment_type + details (same packaging as related-instrument fill) |

Provisional `flow` recalculated so desk/presenters show intended cash impact. **Does not** open/close positions or change capital.

`JournalConfirmationService` now prefers sticky draft units/price/stop (details → task metadata → PositionSizer/ATR). Bare confirm after edit works without re-passing size.

### Surfaces

| Surface | Path |
|---------|------|
| Shell | `edit_journal 44 units=5 price=251.03 stop=245 notes=size-down` · aliases `edit` / `amend` |
| Desk form | Action **edit** + journal id (same fields as enter/confirm) |
| Internal | `POST /internal/journals/edit` |
| MCP | `wv2_edit_journal` |
| Presenter | `proposed_units` / `proposed_price` / `proposed_stop` / `editable` on get journal |

### Refuse

- `invalid_state` when status ≠ `draft` (executed immutable)  
- `not_found`, `invalid_input` (no fields / bad values)

### Specs

`spec/services/operations/journal_draft_edit_service_spec.rb` — amend, refuse executed, sticky confirm, shell.

## Related

- Journal confirmation path  
- Epic #5 related-instrument fill (type/strike/expiry also editable on draft)  
