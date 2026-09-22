---
name: winston-report-delivery
description: >
  Daily report narration. If the tool text contains "Full output saved to:",
  the next call is grep on that path for cash_outlay, notional_basis, premium,
  and expiry before any other tool or reply. Quote premium, expiry, contracts,
  and cash_outlay only when those keys are present. Keep notional on
  notional_basis (underlying_mark_x_contracts is underlying mark times contracts,
  not cash). Rows without those keys get no LEAP line. Never invent fields,
  never recompute Edge (R), never confirm or edit journals.
always: true
---

# Winston Report Delivery

## Ground the reply

If the report tool says `Full output saved to:`, that preview is not the report. The next tool call is `grep` on that path (see Playbook). A reply that states counts, portfolio names, prices, or journal ids not copied from this turn's tool output is a failed turn.

## Triggers

- "send me the report", "daily activity report", "what happened today"
- "get today's report", "the daily"

## MCP Tools

- `wv2_get_daily_activity_report` (primary — one call)
- `wv2_get_daily_activity_report_pdf` (fallback for PDF path)
- `message` (nanobot — attach PDF via `media=[]`)

## Date Logic (4:30 PM Mountain Time)

- Reports for date **D** can only be **generated** after **4:30 PM MT on D** (post NY close).
- **Scheduled EOD cron (4:35 PM MT):** use `fetch_only: true` — Wv2 Sidekiq already ran `DailyAnalysisJob` at 4:30 PM MT. Same turn: `winston-daily-loop` writes `state/STATE-D.md`.
- Before that cutoff on day D, a generic "send me the daily" request means **yesterday's** report.
- Example: 4:29 PM on June 17 → deliver June 16.
- **Never** offer to trigger analysis for a future date.

## Delivery channel

- **Always deliver the final PDF to Sawtooth Main** for scheduled EOD and historical/demo report packages — `message` with `channel=telegram`, `chat_id=-1003884714483` (or `media=[telegram_media_path]`).
- Wv2 also posts the PDF via Bot API `sendDocument` to Sawtooth Main when `TelegramReportDelivery` has credentials (`WV2_TELEGRAM_BOT_TOKEN` / watchdog token + chat id defaulting to `-1003884714483`). Check `telegram_delivery` on the notification JSON.
- **1-1 explicit request**: still reply in the current session **and** ensure Sawtooth Main received the PDF when the user asked for “the daily report” to the group.

## Playbook

1. Resolve the target date per the cutoff rules above.
2. Call `wv2_get_daily_activity_report` **once** with `{ "date": "YYYY-MM-DD" }` (and optional `portfolio_id_or_name`). Scheduled EOD: add `"fetch_only": true`.
3. If the result contains `Full output saved to:`, the next tool call is `grep` on that path. Do not call the PDF tool, `message`, or any other MCP tool first. Suggested pattern: `cash_outlay|notional_basis|premium|expiry`. Use a second `grep` for the symbol or book you are narrating. `read_file` with offset and limit only if grep is unavailable. One read does not cover the file.
4. On success, format from those hits (and any inline JSON that was not persisted):
   - Telegram markdown: signals, passed reasons, action items, capital, and option packaging below.
   - Do **not** tell the user to "check back later".
   - Actionable todos only when the payload has real items. No generic "would you like me to…" footer.
5. PDF attach comes after that narrative. Grep the saved file for `telegram_media_path` instead of calling `wv2_get_daily_activity_report_pdf` when the report JSON was persisted. Call the PDF tool only when the report result has no saved file and no `telegram_media_path`. Then `message` with `media=[that path]` for scheduled EOD or when the user asked to send.
6. On error — report the error message once. Do not retry in a loop unless the user asks.

## Anti-Loop Rules

- **One** `wv2_get_daily_activity_report` call per user request.
- Do **not** call this tool on "hello", "status?", or "what tools do you have?"
- Use `wv2_list_portfolios` for lightweight status checks.

## Option packaging (quote the payload)

Scan `open_positions`, `actions_today`, `pending_actions`, and journal rows in this turn's report. Do not call `wv2_get_journal` to backfill packaging the report omitted.

A row is option-like only when it includes `premium`, `expiry`, `contracts`, or `cash_outlay`. For each such row, quote the keys that are present:

- `fulfillment_type` and `instrument_label`
- `contracts`, `premium`, `expiry`, and `strike` / `option_type` when present
- `cash_outlay` as cash outlay
- `notional` on its own. When `notional_basis` is present, say that label (`underlying_mark_x_contracts` is underlying mark × contracts). Do not call `notional` the cash outlay.

Rows with none of those option keys stay share lines (units, price, direction). No Long-term Equity Anticipation Security (LEAP), premium, expiry, or contract wording. If the payload has no option-like rows, add no packaging section.

## Never Do

- Paste filenames or filesystem paths as text links
- Call the report tool repeatedly with tweaked dates
- Invent report content, fills, prices, or packaging fields the tool did not return
- Recompute or redefine Edge (R). Quote a payload figure only when the payload already has it
- Confirm or edit journals (`wv2_confirm_journal`, `wv2_edit_journal`) or run `wv2_perform_daily_analysis`
