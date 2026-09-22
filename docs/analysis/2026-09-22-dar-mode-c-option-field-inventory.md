# Mode C DAR option-field inventory (2026-09-22)

**Status:** Finding — share-shaped payload  
**Parent:** [`../tickets/2026-09-17-leap-aware-dar-narrative.md`](../tickets/2026-09-17-leap-aware-dar-narrative.md)  
**Sibling (emit):** [`../tickets/2026-09-22-dar-mcp-emit-option-fields.md`](../tickets/2026-09-22-dar-mcp-emit-option-fields.md)  
**Specimen:** `winston_v2/storage/cromwell_notifications/wv2_20260921.json` (`schema_version` 1.4, `date` 2026-09-21, `type` daily_complete). This file is what `wv2_get_daily_activity_report` returns.

Narration was **not** patched. The Daily Analysis Report (DAR) has no structured option fields for the narrator to quote.

## Structured keys

Walk of the JSON for names containing option, premium, expir, contract, strike, conid, leap, fulfill, occ, instrument, multiplier, dte, call, put:

| Key | Where | Value |
|-----|--------|--------|
| `fulfillment_label` | every `portfolio_chapters[]` | `null` |
| `multiplier` | `risk_scale` | `1.0` (risk scale, not the option multiplier) |
| `expired_today` / `actions_expired_today` | top / summary | action-window counts, not expiries |

Absent everywhere in the DAR: `fulfillment_type`, `premium`, `option_premium`, `expiry`, `expiration_date`, `strike`, `contracts`, `conid`, `instrument_label`, `occ_symbol`, `contract_multiplier`, `cash_outlay`, `cash_impact`, `signal_share_units`, `is_option`.

`open_positions[]` keys are share bars only: `symbol`, `direction`, `units`, `entry`, `stop`, `mark`, `mtm`, `notional`, OHLC, `atr`. `notional` is `mark * units`.

`pending_actions[]` / chapter pending keys: `task_id`, `portfolio`, `portfolio_id`, `market`, `task_type`, `report_date`, `journal_id`, `status`, `execution_mode`, `attention_band`, `form_path`, `telegram_phrase`, `shell_phrase`, `human_gated`.

`processed_signals[]` keys: `outcome`, `portfolio`, `market`, `signal_type`, `direction`, `units`, `price`, `trade_date`, `journal_id`, `notes`, `signal_date`. No cash field.

`recent_journals[]` on this file are twenty Walnut drafts (`flow` 0). Keys: `id`, `portfolio`, `market`, `trade_date`, `status`, `notes`, `flow`, `units`. No execution price, no fulfillment.

One prose exception, not a field: processed signal journal 1950 notes begin `flatten demo 2026-09-21: 1x MSFT 2026-10-02 497.5 call @ 9.95`. Journals 1943 and 1946 notes are desk-confirm boilerplate with no call, expiry, or premium words.

## Mode C rows the narrator would misread

Booked lots below are options in Winston v2 (Wv2). The DAR prints them as shares.

| Book | DAR row | DAR numbers | What the books actually are |
|------|---------|-------------|------------------------------|
| Indigo 1583 | open BITQ | units 2, entry 4.75, stop 2.33, mark 28.19, notional **56.38**, mtm 46.88 | Position 889: call, strike 28, expiry 2027-04-16, premium 4.75. Journal 1946 `flow` **-950** (2 × 4.75 × 100). |
| Mango 1577 | open SEF | units 4, entry 1.375, stop 0.78, mark 30.2965, notional **121.19** | Position 887: call, strike 30, expiry 2027-02-19, premium 1.375. Journal 1943 cash outlay **550**. |
| Mango 1577 | open RXT ×2 | units 4, entry 2.3, mark 4.04, notional **16.16** each | Positions 869 and 871: calls, strike 4, expiry 2029-01-19, premium 2.3. |
| Blue 1574 | open RXT | units 8 and 7, entry 2.3, mark 4.04, notionals 32.32 and 28.28 | Positions 868 and 870: same call, premium 2.3. |
| Teal 1584 | open XLU | units 4, entry 2.775, stop 42.35, mark 40.66, notional **162.64** | Position 873: **put**, strike 41, expiry 2028-12-15, premium 2.775. |
| Indigo 1583 | pending task 1838 / journal 1985 | phrase `units=2 price=5.35`; action `price` **28.41**; reason `last lot @ 4.75` | At report time a pyramid draft. No expiry, strike, or contract label on the row. |

`notional` 56.38 = 28.19 × 2. That is underlying mark times contract count. It is not premium × 100 × contracts.

`processed_signals` for 1946: `units` 2, `price` 4.75, notes with no option words. The premium is unlabeled, so a narrator can read it as two shares.

## Where the fields already exist

`GET /internal/journals/:id` (`wv2_get_journal`) returns `fulfillment_type` and `fulfillment_details`. Journal 1946 (Indigo BITQ, executed `standard_call`) includes:

- `instrument_label`, `conid` 912464575, `strike` 28, `expiry` 2027-04-16, `option_type` call
- `premium` / `option_premium` 4.75, `units` 2, `contract_multiplier` 100
- `cash_outlay` 950, `cash_impact` -950
- `signal_share_units`, `fulfillment_plan_a` leap, `fulfillment_plan_b` standard_call

Same shape on journal 1943 (Mango SEF, cash outlay 550). Position columns `is_option`, `option_type`, `strike_price`, `expiration_date`, `option_premium` are set on the open lots above and are dropped by `DailyReportPayloadBuilder#open_positions_for`.

`GET /internal/pending_actions` (`InternalController#serialize_pending_task`) emits task, market, price, direction, reason. No fulfillment projection. Indigo and Blue had zero pending rows on 2026-09-22, so the 2026-09-21 DAR pending list is the specimen.

Serializers that omit the fields:

- `winston_v2/app/services/daily_report_payload_builder.rb` — `serialize_pending`, `serialize_action`, `serialize_journal`, `open_positions_for`, `processed_signals`
- `winston_v2/app/controllers/internal_controller.rb` — `serialize_pending_task`

End-of-day cron may call `wv2_get_journal`, but the narrator ticket forbids inventing from outside the report and forbids a per-draft journal fan-out as a substitute for fields on the report.

## Harness

No narrator text was produced. Parent checkpoints that compare Telegram text to the payload were not sent to Jev. The stop is the key walk above.
