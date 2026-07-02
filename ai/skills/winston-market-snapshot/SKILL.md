---
name: winston-market-snapshot
description: Brief market status for symbols in active portfolios — broadcast to Sawtooth Main only.
---

# Winston Market Snapshot

Schedule: `ecosystem/ai/schedule/manifest.yaml` — `cromwell_market_snapshot_open` (7:30 AM MT) and `cromwell_market_snapshot_hourly` (8 AM–2 PM MT hourly).

## Triggers

- Cromwell cron during NYSE session (7:30 AM–2:00 PM **Mountain Time**, Mon–Fri)
- Principal asks for "market status" (brief answer; broadcast only if they ask to post to the group)

## MCP Tools

- `wv2_market_snapshot` — latest EOD close, volume, atr_17 from DM parquet
- Do **not** call `wv2_list_portfolios`, `wv2_perform_daily_analysis`, or `wv2_get_daily_activity_report` on scheduled broadcasts

## Data Source (important)

- **Not live intraday** until Phase D (EODHD delayed quotes). MCP v1 uses **latest EOD bar** from DM parquet.
- Say clearly: "as of last EOD close (date)" when live session ATR breach is unavailable.

## Playbook (scheduled broadcast)

1. Confirm current time is **7:30 AM–2:00 PM MT** on a trading day. Outside that window → **skip** (no message).
2. Call **`wv2_market_snapshot` only** — **every run** (no args, or `{}`). Never reuse prior session tool output.
3. Post **one** concise message to **Sawtooth Main** via `message` tool (`channel`: `telegram`, `chat_id`: `-1003884714483`).
4. **When `atr_breach` is present on symbols** (Phase D): list movers where move exceeds 1× ATR; omit quiet symbols.
5. **When no breaches / no live quotes yet**: one brief staid or lightly humorous line (rotate tone; no invented prices). Example: "Markets are comporting themselves with unusual decorum — last EOD closes unchanged in our parquet snapshot."

## Never Do

- Post periodic snapshots to the principal 1-1 chat (unless explicitly asked)
- Claim live/real-time prices without tool support
- Mention EOD daily analysis or 4:35 PM report in session snapshots
- Numbered next-steps menus