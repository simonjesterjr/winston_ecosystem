---
name: winston-equity-compare
description: Compare Operational Portfolio equity curves (e.g. Blue vs Mango) and deliver a chart PDF over Telegram.
---

# Winston Equity Compare

## Triggers

- "compare equity Blue vs Mango"
- "show equity of Blue and Orange"
- "equity chart Red Blue Green"
- "how are Blue and Mango doing side by side"

## MCP Tool

| Tool | When |
|------|------|
| `wv2_compare_equity` | Multi-OP equity series + chart PDF |
| `wv2_list_portfolios` | Resolve ambiguous names if needed |
| `message` | Attach chart via `media=[telegram_media_path]` |

## Required inputs (never invent)

1. **At least one portfolio** id or name (two+ for a real compare)
2. Optional: `as_of` date, `normalize=true` (rebase each series to 100)

## Playbook

1. Resolve portfolio names if ambiguous (`wv2_list_portfolios`).
2. Call **`wv2_compare_equity`** with `portfolios: ["Blue", "Mango"]`.
3. On success:
   - Paste **`reply_text`** (metrics summary) as the user message.
   - Attach chart: `message` with `media=[telegram_media_path]` (or nanobot auto-attach when `_meta.delivery` is present).
4. Do **not** paste raw filesystem paths as hyperlinks.
5. Stop. No activate/sync/daily-analysis menus.

## Examples

```
wv2_compare_equity { portfolios: ["Blue", "Mango"] }
```

```
wv2_compare_equity {
  portfolios: ["12", "Orange"],
  as_of: "2026-07-16",
  normalize: true
}
```

Shell: `equity_compare Blue Mango` · `equity Blue Mango normalize=true`

## Reply contract

```
Equity compare: Blue vs Mango
as_of 2026-07-17
Blue · ab12cd34 #12: ret=3.2% dd=1.1% end=$10320
Mango · ef56gh78 #18: ret=-0.5% dd=2.4% end=$11940
chart attached via media path
```

Labels = OP display name + short fingerprint when present.

## Errors

| Code | Action |
|------|--------|
| `not_found` | Clarify portfolio name/id |
| `invalid_input` | Need 1–6 portfolios |
| `compare_failed` | Report message; do not invent a chart |

## Never Do

- Invent equity numbers or charts
- Claim live interactive charting (PDF snapshot only)
- Auto-chain daily analysis after compare
- Paste host paths as user-visible links
