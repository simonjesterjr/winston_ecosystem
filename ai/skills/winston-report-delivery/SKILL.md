---
name: winston-report-delivery
description: Deliver the Wv2 daily activity report and PDF over Telegram with correct date logic and no tool loops.
always: true
---

# Winston Report Delivery

## Triggers

- "send me the report", "daily activity report", "what happened today"
- "get today's report", "the daily"

## MCP Tools

- `wv2_get_daily_activity_report` (primary — one call)
- `wv2_get_daily_activity_report_pdf` (fallback for PDF path)
- `message` (nanobot — attach PDF via `media=[]`)

## Date Logic (4:30 PM Mountain Time)

- Reports for date **D** can only be **generated** after **4:30 PM MT on D** (post NY close).
- **Scheduled EOD cron (4:35 PM MT):** use `fetch_only: true` — Wv2 Sidekiq already ran `DailyAnalysisJob` at 4:30 PM MT.
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
3. On success:
   - Format the JSON into readable Telegram markdown (signals, passed reasons, action items, capital).
   - If `telegram_media_path` is present, the gateway may auto-attach the PDF. You may also use `message` with `media=[telegram_media_path]`.
   - Do **not** tell the user to "check back later".
   - Include **actionable todos only** when the payload has real items (entrances, exits, pyramids, pending confirmations). No generic "would you like me to…" footer.
4. If `telegram_media_path` is missing:
   - Call `wv2_get_daily_activity_report_pdf` for the same date.
   - `message` with `media=[that path]`.
5. On error — report the error message once. Do not retry in a loop unless the user asks.

## Anti-Loop Rules

- **One** `wv2_get_daily_activity_report` call per user request.
- Do **not** call this tool on "hello", "status?", or "what tools do you have?"
- Use `wv2_list_portfolios` for lightweight status checks.

## Never Do

- Paste filenames or filesystem paths as text links
- Call the report tool repeatedly with tweaked dates
- Invent report content not returned by the tool