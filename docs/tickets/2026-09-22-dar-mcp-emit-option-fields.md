# Ticket: DAR / pending MCP must emit option packaging fields

**Status:** Proposed  
**Date:** 2026-09-22  
**Priority:** P2  
**Lane:** B (serializer projection; short System One harness)  
**Implementer:** Winston Dev or Grok CLI  
**Origin:** Lane B stop on [`2026-09-17-leap-aware-dar-narrative.md`](2026-09-17-leap-aware-dar-narrative.md). Inventory: [`../analysis/2026-09-22-dar-mode-c-option-field-inventory.md`](../analysis/2026-09-22-dar-mode-c-option-field-inventory.md).  
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

- [ ] Spec: option journal/position projects the table; stock row does not
- [ ] Patch `DailyReportPayloadBuilder` and `serialize_pending_task`
- [ ] Regenerate or fixture-compare one Mode C DAR slice (do not require a live Telegram send)
- [ ] Jev on the excerpt
- [ ] Hand parent [`2026-09-17-leap-aware-dar-narrative.md`](2026-09-17-leap-aware-dar-narrative.md) back to In progress

## CLI seed

```
cwd: /home/johnkoisch/Documents/com/sawtooth
Lane B. Ticket: ecosystem/docs/tickets/2026-09-22-dar-mcp-emit-option-fields.md

Goal: Project stored option fields onto wv2_get_daily_activity_report and wv2_list_pending_actions. Copy journal/position values. Do not change packaging math, confirm, Edge, or Cromwell skills.

Steps:
1. Read this ticket and ecosystem/docs/analysis/2026-09-22-dar-mode-c-option-field-inventory.md.
2. Failing spec on DailyReportPayloadBuilder / pending serializer using journal 1946 shape vs a share journal.
3. Minimal projection. Option rows gain the field table. Share rows omit those keys. Do not replace notional silently.
4. Run the spec in compose (winston_v2). Jev ask on before/after excerpt. Attach under the ticket.
5. In-band wrap. Push the monolith that changed. Set parent 2026-09-17-leap-aware-dar-narrative back to In progress when a real or fixture DAR shows the fields.

DoD: option row shows premium, expiry, contracts, and labeled cash from stored fields; share row stays quiet; no Edge recompute.
```
