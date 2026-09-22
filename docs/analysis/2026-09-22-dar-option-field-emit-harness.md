# DAR option-field emit — harness (2026-09-22)

**Status:** Pass  
**Ticket:** [`../tickets/archive/2026-09-22-dar-mcp-emit-option-fields.md`](../tickets/archive/2026-09-22-dar-mcp-emit-option-fields.md)  
**Parent (resume narrator only):** [`../tickets/2026-09-17-leap-aware-dar-narrative.md`](../tickets/2026-09-17-leap-aware-dar-narrative.md)  
**Before inventory:** [`2026-09-22-dar-mode-c-option-field-inventory.md`](2026-09-22-dar-mode-c-option-field-inventory.md)

Winston v2 (Wv2) `DailyReportPayloadBuilder` and `InternalController#serialize_pending_task` copy stored option packaging. They do not reprice, replace notional, or add Edge (R).

## Before / after (Indigo BITQ, journal 1946)

Stored journal: `standard_call`, premium 4.75, expiry 2027-04-16, strike 28, multiplier 100, cash outlay 950, units 2.

| | Before file row | After builder slice and patched file |
|--|-----------------|--------------------------------------|
| units / entry / mark | 2 / 4.75 / 28.19 | unchanged |
| notional / mtm | 56.38 / 46.88 | unchanged |
| premium, expiry, contracts | absent | 4.75, 2027-04-16, 2 |
| cash_outlay | absent | 950 |
| notional_basis | absent | `underlying_mark_x_contracts` |
| fulfillment_type, strike, option_type | absent | `standard_call`, 28, call |

Orange SMH journal 1941, 17 shares at 580.81: before and after have units, entry, mark, notional, mtm only. No premium, expiry, contracts, or cash_outlay.

Same shape on the other Mode C open lots in the patched file (Mango SEF cash 550, Teal XLU put, Blue/Mango RXT calls). Share rows stayed quiet (31 of 38 open rows).

`notional` is still underlying mark × contract count. Cash sits on `cash_outlay`.

## Specs

`winston_v2/spec/services/daily_report_payload_builder_option_fields_spec.rb`

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/services/daily_report_payload_builder_option_fields_spec.rb
```

4 examples, 0 failures. Attention-band and open-book specs still pass.

## File regenerate

`storage/cromwell_notifications/wv2_20260921.json` is what `wv2_get_daily_activity_report` reads. It was patched in place from current journal and position columns. No Telegram send, no webhook, no Daily Analysis job (that job can expire tasks). Schema version stays 1.4. Notional values were checked equal to the pre-patch file.

Task 1838 is completed now. Its pending row on that file carries the journal’s current stored packaging (premium 4.75, cash outlay 950). The old shell phrase still says `price=5.35`.

Some RXT journals already store float dust in `cash_outlay` (8 × 2.3 × 100 stored as 1839.9999999999998). This projection copies that number. It does not repair the journal.

## System One (Jev 1.13.0)

State: before/after BITQ open row plus SMH 17 @ 580.81. Pass rule from the emit ticket.

| id | noul | rule | result |
|----|------|------|--------|
| emit_premium | 0.93 | ≥ 0.85 PASS | PASS |
| emit_expiry_contracts | 0.97 | ≥ 0.85 PASS | PASS |
| cash_labeled | 0.92 | ≥ 0.85 PASS | PASS |
| quiet_share | 0.09 | ≥ 0.85 FAIL | PASS (share row did not gain option keys) |
| no_edge | 0.05 | ≥ 0.85 FAIL | PASS (no Edge (R) added) |
