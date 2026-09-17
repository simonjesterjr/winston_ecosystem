---
name: winston-daily-loop
description: Persist bounded daily STATE and stop/skip the Cromwell EOD loop when DAR or MCP is incomplete.
---

# Winston Daily Loop (STATE + stop/skip)

Cadence owner is existing `eod-daily-report` (16:35 MT M–F). This skill does **not** re-run Daily Analysis.

## Triggers

- Scheduled EOD (with `winston-report-delivery`)
- "daily state", "write STATE", "did the loop complete?"

## MCP

- Required on EOD: `wv2_get_daily_activity_report` with `fetch_only: true` and **omit `date`** (server picks production date). Never pass 2023 or any guessed year.
- Optional: `wv2_list_pending_actions`, `wv2_list_portfolios`, `wv2_get_journal`
- Never: `wv2_perform_daily_analysis`, `wv2_confirm_journal`

## Stop / skip (checkable)

| Condition | `loop_status` | `skip_reason` | Telegram |
|-----------|---------------|---------------|----------|
| Report tool error / empty | `skip` | `mcp_error` | one-line OPS ERROR |
| `fetch_only` and no DAR for date D | `skip` | `dar_missing` | one-line; do **not** invent a complete day |
| Weekend / job not scheduled | — | `not_trading_day` | n/a |
| Report ok, coverage/skip list in payload | `partial` | `coverage_stale` if payload says so | EOD summary + honest skip list |
| Report ok | `complete` | `none` | existing EOD summary |

The loop **must not** claim `complete` if DAR is missing.

## STATE file

Write **only** `state/STATE-YYYY-MM-DD.md` (date = report date D). Shape: `memory/templates/STATE.template.md`. Hard cap **80 lines**. Facts from this turn's MCP only — no invented fills, Edge, or Sharpe.

On cron, `write_file` is allowed **only** under `state/`. Do not write `memory/`, `cron/`, or `skills/`.

If yesterday's `state/STATE-*.md` exists, you may `read_file` it for deltas (pending cleared / still open). Optional.

## Verifier

When pending drafts exist, follow `winston-decision-verifier`. Append verdicts to STATE. Telegram: one line per pending journal, not an essay. **Never confirm.**

## Interactive

1. Resolve date D (after 16:30 MT → today, else yesterday).
2. `fetch_only` report.
3. Write STATE.
4. If pending, verifier.
5. Reply: `loop_status` + pending count + path `state/STATE-D.md`.
