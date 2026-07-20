# Ticket: Signal → related instrument fill (e.g. equity signal, LEAP fill)

**Status:** Done  
**Date:** 2026-07-17  
**Done:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  

## Problem

IBM may signal a 20-day breakout; operator buys 2028 LEAPs (or other related instrument) to honor the signal without the stock. Schema has `fulfillment_type` / `fulfillment_details` but product path is stock-centric.

## Scope

1. Confirm or book fill with `fulfillment_type=leap|option|proxy` + details (underlying, expiry, strike).  
2. Link to motivating signal/journal/task id when present.  
3. Position representation rules (units, stops) for non-stock — minimum viable.  
4. Non-goal: full options pricing engine.

## Acceptance

- [x] Journal can record LEAP fill tied to equity signal context  
- [x] capital_base / flow rules documented for that path  

## Implementation (2026-07-17)

### Capital / flow rules

| Type | units | price | multiplier | enter flow | exit flow |
|------|-------|-------|------------|------------|-----------|
| `stock` | shares | stock $ | 1 | −u×p | +u×p |
| `proxy` | shares (of proxy) | proxy $ | 1 | −u×p | +u×p |
| `leap` / `option` / `option_strategy` | **contracts** | **premium per share** | **100** (override with `multiplier=`) | −u×p×m | +u×p×m |

Journal **Market** = signal **underlying** (must be on Books). Filled instrument lives on Position option columns + `fulfillment_details`.

### Position representation (MVP)

- `Position.is_option`, `option_type`, `strike_price`, `expiration_date`, `option_premium` populated for leap/option  
- `action_description` includes instrument label (e.g. `OPEN long 2 LEAP IBM 2028-01-21 150 C @ 12.5`)  
- Stops: human `stop=` on premium allowed; **no ATR default** for option-like (stock/proxy keep ATR)  
- Exit inherits packaging + multiplier from entry journal / open position  

### Surfaces

| Surface | Path |
|---------|------|
| Domain | `Operations::RelatedInstrumentFulfillment` + AdHocPaperFill / JournalConfirmation / AdHocExit |
| Shell | `enter Blue IBM units=2 price=12.50 type=leap strike=150 expiry=2028-01-21 option_type=call [signal_task=N]` |
| Desk form | Fulfillment type select + strike/expiry/option fields + signal ids |
| Internal | `POST /internal/journals/book` + confirm accept related fields |
| MCP | `wv2_book_trade` / `wv2_confirm_journal` — `fulfillment_type`, strike, expiry, signal_* |

### Files (winston_v2)

- `app/services/operations/related_instrument_fulfillment.rb` **added**  
- `ad_hoc_paper_fill_service.rb`, `journal_confirmation_service.rb`, `journal_position_executor.rb`, `ad_hoc_exit_service.rb`  
- `ops_shell_chat.rb`, desk controller/view, `internal_controller.rb`  
- Specs: `related_instrument_fulfillment_spec.rb`, `related_instrument_fill_spec.rb`  

### Host MCP

- `ai/mcp_winston/mcp_winston/server.py` — book_trade related args + reply_text instrument label  

## Related

- Journal vs trading ledger analysis  
- Epic: `2026-07-17-ops-daily-demo-epic.md`  
