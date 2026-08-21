---
name: winston-mms
description: Fetch and (when asked) attach the Winston Mid-month Scoreboard PDF.
---

# Winston Mid-month Scoreboard

## Triggers

- "mid-month scoreboard", "MMS", "monthly scoreboard", "how did paper do this month"

## MCP Tool

| Tool | When |
|------|------|
| `wv2_get_mid_month_scoreboard` | Fetch latest or dated MMS |
| `message` | Attach PDF via `media=[telegram_media_path]` |

## Playbook

1. Call **`wv2_get_mid_month_scoreboard`** (omit date for latest; or pass the third-Wednesday `date`).
2. On `mms_not_ready`: say the report is generated 06:00 MT on the third Wednesday. Do **not** invent scores.
3. On success: paste `summary.headline` (or a 4-line extract). Attach the PDF. Stop.
4. Do not chain daily analysis, activate, or confirm.

## Never Do

- Invent Sharpe, return, or PCS
- Treat MMS as a capital-promotion stamp
- Post a research essay on Sawtooth Main beyond the headline + PDF
