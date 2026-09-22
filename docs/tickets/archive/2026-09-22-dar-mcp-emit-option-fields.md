# Ticket: DAR / pending MCP must emit option packaging fields

**Status:** Done  
**Date:** 2026-09-22  
**Updated:** 2026-09-22 (shipped — option rows emit stored packaging; share rows quiet; Jev pass)  
**Priority:** P2  
**Lane:** B (serializer projection; short System One harness)  
**Implementer:** Grok CLI (shared watchable session; Winston Dev only if Operator reassigns)  
**Origin:** Lane B stop on [`../2026-09-17-leap-aware-dar-narrative.md`](../2026-09-17-leap-aware-dar-narrative.md). Inventory: [`../../analysis/2026-09-22-dar-mode-c-option-field-inventory.md`](../../analysis/2026-09-22-dar-mode-c-option-field-inventory.md). Harness: [`../../analysis/2026-09-22-dar-option-field-emit-harness.md`](../../analysis/2026-09-22-dar-option-field-emit-harness.md).  
**DoD:** A Mode C Daily Analysis Report (DAR) row for an option-like fill or open lot carries the packaging fields already stored on the journal or position. Share-only rows omit them. Edge (R) is not recomputed. Packaging math, confirm, and journal edits do not change.

## Problem

`wv2_get_daily_activity_report` for 2026-09-21 (`storage/cromwell_notifications/wv2_20260921.json`) is share-shaped. Mode C books (Blue, Mango, Indigo, Teal) hold listed calls and a put. The report prints `units` × underlying `mark` as `notional` and never names premium, expiry, strike, contract count, or cash outlay.

Example: Indigo position 889 / journal 1946 is 2 BITQ 2027-04-16 28 calls at premium 4.75, cash outlay 950. The DAR open row is units 2, entry 4.75, mark 28.19, notional 56.38.

`wv2_get_journal` already returns `fulfillment_type` and `fulfillment_details` (premium, expiry, strike, multiplier, cash_outlay, instrument_label, conid, signal_share_units). Position columns `is_option`, `option_type`, `strike_price`, `expiration_date`, `option_premium` are populated. The DAR and `wv2_list_pending_actions` serializers drop them.

Cromwell End of Day (EOD) narration stays blocked until this projection exists. Do not teach the narrator to invent those lines, and do not fan out `wv2_get_journal` as a substitute.

## Scope

Project stored fields onto the DAR and the pending-actions payload. Copy; do not recompute.

When the journal or position is option-like (`leap`, `standard_call`, `option`, `option_strategy`, or `is_option`):

| DAR / pending field | Source (already stored) |
|---------------------|-------------------------|
| `fulfillment_type` | journal |
| `contracts` | journal `units` or position `units` (labeled; do not rename share `units` on stock rows) |
| `premium` | `option_premium` / `fulfillment_details["premium"]` |
| `expiry` | `expiration_date` / `fulfillment_details["expiry"]` |
| `strike` | `strike_price` / `fulfillment_details["strike"]` |
| `option_type` | call or put |
| `contract_multiplier` | details, else 100 for US equity options |
| `cash_outlay` | details `cash_outlay`, else `contracts × premium × multiplier` only when those three are already stored — do not price a new quote |
| `signal_share_units` | details, when present |
| `instrument_label` | details, when present |
| `conid` | details, when present |

Apply on:

- `DailyReportPayloadBuilder` pending, actions, processed signals, recent journals, and `open_positions`
- `InternalController#serialize_pending_task` (`wv2_list_pending_actions`)

Share rows: omit the option keys. Leave `fulfillment_label` null alone (catalog glance, not a contract).

Open-position `notional` today is `mark * units`. For option rows, keep that number only if a separate key says it is underlying mark × contracts. Put real cash on `cash_outlay`. Do not silently replace `notional` in this ticket.

## Non-goals

- Cromwell skill text (`winston-report-delivery` / `winston-daily-loop`) — resume the parent ticket after a payload contains the fields
- Packaging ladder, confirm, Desk Send, Edge (R), Black-Scholes
- Building an OCC symbol when `localSymbol` was blank
- A third narrator skill

## Specimens

- DAR file: `winston_v2/storage/cromwell_notifications/wv2_20260921.json`
- Journal 1946 (Indigo BITQ call, cash 950), journal 1943 (Mango SEF call, cash 550)
- Positions 889 (BITQ), 887 (SEF), 869/871 (Mango RXT calls), 873 (Teal XLU put)
- Pending specimen on that DAR: task 1838 / journal 1985 (Indigo BITQ pyramid). Live pending list was empty on 2026-09-22.

## System One harness

**State:** journal 1946 `fulfillment_details` (premium 4.75, expiry 2027-04-16, strike 28, multiplier 100, cash_outlay 950, units 2, fulfillment_type `standard_call`) and the DAR open-position or processed-signal row for that lot after the serializer change. Plus one share row (Orange SMH journal 1941, 17 shares at 580.81) that must stay free of option keys.

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| emit_premium | Noul | Option row states premium 4.75 from the journal, not a new quote | noul ≥ 0.85 → PASS |
| emit_expiry_contracts | Noul | Option row states expiry 2027-04-16 and contract count 2 | noul ≥ 0.85 → PASS |
| cash_labeled | Noul | Cash outlay 950 is present and distinct from share notional / underlying mark × contracts | noul ≥ 0.85 → PASS |
| quiet_share | Noul | Share row (SMH 17 @ 580.81) gains premium, expiry, or contract keys | noul ≥ 0.85 → FAIL |
| no_edge | Noul | Payload recomputes or adds Edge (R) | noul ≥ 0.85 → FAIL |

**Runner:** serializer spec first; then `jev ask` on the before/after JSON excerpt.  
**On fail:** do not mark Done; do not unblock narrator polish.

## Work items

- [x] Spec: option journal/position projects the table; stock row does not
- [x] Patch `DailyReportPayloadBuilder` and `serialize_pending_task`
- [x] Regenerate or fixture-compare one Mode C DAR slice (do not require a live Telegram send) — `wv2_20260921.json` patched in place; no Telegram
- [x] Jev on the excerpt — pass; see harness analysis
- [x] Hand parent [`../2026-09-17-leap-aware-dar-narrative.md`](../2026-09-17-leap-aware-dar-narrative.md) back to In progress

## Result

Indigo BITQ open row (journal 1946): premium 4.75, expiry 2027-04-16, contracts 2, cash_outlay 950, notional still 56.38 with `notional_basis` `underlying_mark_x_contracts`. Orange SMH 17 @ 580.81 omits option keys. Edge (R) not added. Narrator skills not edited.

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth  (workspace root OK for ticket/analysis reads)
Code changes live under winston_v2/ — cd there for specs/compose as needed.

Lane B. Ticket: ecosystem/docs/tickets/2026-09-22-dar-mcp-emit-option-fields.md
Parent (blocked until this ships): ecosystem/docs/tickets/2026-09-17-leap-aware-dar-narrative.md
Inventory: ecosystem/docs/analysis/2026-09-22-dar-mode-c-option-field-inventory.md

Goal: Project stored option packaging fields onto wv2_get_daily_activity_report (DailyReportPayloadBuilder) and wv2_list_pending_actions (InternalController#serialize_pending_task). Copy from journal fulfillment_details / position option columns. Do not change packaging math, confirm, Edge (R), or Cromwell narrator skills.

Specimens: journal 1946 Indigo BITQ (2 calls, premium 4.75, expiry 2027-04-16, strike 28, cash_outlay 950); share control Orange SMH journal 1941 (17 @ 580.81). DAR fixture: winston_v2/storage/cromwell_notifications/wv2_20260921.json

Steps:
1. Read this ticket (System One harness + field table) and the inventory analysis.
2. Locate DailyReportPayloadBuilder and serialize_pending_task; confirm where units/mark/notional are built and where option keys are dropped.
3. Failing spec first: option-shaped journal/position projects premium, expiry, contracts (or labeled units), cash_outlay, fulfillment_type, strike, option_type as applicable; share row omits those keys; do not silently replace notional.
4. Minimal projection patch — copy stored values only. cash_outlay from details or contracts×premium×multiplier only when those three are already stored. Keep existing notional behavior unless a separate label key is added for underlying mark × contracts.
5. Run specs via ./bin/compose exec -T winston_v2 bundle exec rspec <paths>. Optionally regenerate or fixture-compare a Mode C DAR slice (no live Telegram required).
6. System One: jev ask on before/after JSON excerpt per ticket harness; attach results on ticket or docs/analysis/.
7. In-band wrap session report under ecosystem. Push winston_v2 main (and ecosystem docs if you updated tickets). No PR.
8. When a real or fixture Mode C DAR row shows premium + expiry + contracts + labeled cash_outlay: set parent 2026-09-17-leap-aware-dar-narrative back to In progress (do not implement narrator in this ticket).

DoD: option row emits stored packaging fields; share row stays quiet; no Edge recompute; harness checkpoints pass; parent unblocked for resume (status only).
```
