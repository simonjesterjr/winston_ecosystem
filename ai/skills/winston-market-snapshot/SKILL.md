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

- `wv2_market_snapshot` — live internet price vs prior EOD close + atr_17 for Books on active portfolios
- Do **not** call `wv2_list_portfolios`, `wv2_perform_daily_analysis`, or `wv2_get_daily_activity_report` on scheduled broadcasts

## Data Source (important)

- **Current price / session OHLV**: live internet quote (not EODHD, not stored bars)
- **Previous close + atr_17**: latest EOD bar from DM parquet (boundary reference only)
- Symbols without a live quote are **omitted**
- This is a **focusing tool / weather radar** — not authoritative daily analysis or trade instructions

## Playbook (scheduled broadcast)

1. Confirm current time is **7:30 AM–2:00 PM MT** on a trading day. Outside that window → **skip** (no message).
2. Call **`wv2_market_snapshot` only** — **every run** (no args, or `{}`). Never reuse prior session tool output. Runtime **requires** a successful call this turn or posts OPS ERROR (never invent "stable / no movers").
3. Format **only** from this turn's tool JSON. After truncation: summarize what you already have — do **not** call `read_file`, do **not** invent paths like `path/to/file.txt`, do **not** ask the human for a path.
4. Post **one** concise message to **Sawtooth Main** via `message` tool (`channel`: `telegram`, `chat_id`: `-1003884714483`) **or** as the natural final reply.
5. **When `movers` is non-empty**: list each mover with symbol, previous close, current price, ATR, status (testing / breach_up / breach_down), and atr_multiple. Quiet symbols can be omitted.
6. **When all quiet or no symbols** (and the tool **did** return): one brief staid or lightly humorous line (rotate tone; no invented prices). Example: "Active books are well inside 1× ATR of prior close — nothing asking for attention yet."
7. **On tool failure / circuit-break**: one-line **OPS ERROR** only (duty failed). No recovery questions.

### Message shape (when movers exist)

Keep it short. Example:

```
Radar — active books testing / breaking ATR:
• MSFT  prev 383.34 → 392.95  ATR 12.16  (+0.79× testing)
• AMAT  prev 570.50 → 615.20  ATR 43.68  (+1.02× breach_up)
```

## Never Do

- Post periodic snapshots to the principal 1-1 chat (unless explicitly asked)
- Invent prices or claim EOD analysis when only the radar ran
- Claim "stable / no movers / quiet" **without** a successful `wv2_market_snapshot` this turn
- Call `read_file` / free-form filesystem recovery after truncation
- Ask the human for file paths or other free-form recovery on cron turns
- Mention EOD daily analysis or 4:35 PM report in session snapshots
- Numbered next-steps menus
