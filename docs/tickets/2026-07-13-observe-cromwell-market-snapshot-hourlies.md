# Ticket: Observe Cromwell market-snapshot hourlies for real MCP + clean Telegram

**Status:** Proposed  
**Priority:** P1
**Context:** Issue `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`. Sessions `docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`, `docs/session-reports/2026-07-13-1307-intraday-market-radar.md`. Overlaps acceptance on `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`.

## Cluster (Cromwell hourly Telegram)

| # | Artifact | Role |
|---|----------|------|
| 1 | [`2026-07-09-confirm-cromwell-hourly-telegram.md`](2026-07-09-confirm-cromwell-hourly-telegram.md) | Delivery after CPU tuning |
| 2 | [`2026-07-13-cromwell-scrub-placeholder-path-memory.md`](2026-07-13-cromwell-scrub-placeholder-path-memory.md) | Memory scrub |
| 3 | **This ticket** | Live MCP + clean Telegram proof |
| 4 | [`2026-07-21-cromwell-hourly-telegram-attention-discipline.md`](2026-07-21-cromwell-hourly-telegram-attention-discipline.md) | Quiet = one line |

## Problem

After the 09:00 MDT 2026-07-13 failure, 10:00 and 11:00 MT hourlies posted “no movers / stable” **without** logging a `wv2_market_snapshot` tool call. Need a short observation pass to establish current baseline (still broken vs intermittent).

**Update 2026-07-13 (later session):** `wv2_market_snapshot` now returns **live internet quotes + ATR movers** (not EOD parquet dump). Observation should also check that Telegram posts prefer `movers` (prev → now, ATR, status) and do not invent prices when the tool succeeds.

**Update 2026-07-21:** Principal saw a ~10:21 local hourly: tool-shaped payload (`2026-07-21 16:17:15 UTC`) but **verbose all-quiet dump** + menu + placeholders (AAPL ATR `[calculated value]`). That is a **content** fail under principle §12 — track against attention-discipline issue/ticket.

**Observation log 2026-07-21 (pre-seed attention prompts — full NYSE window):**

| Local MT | Job | MCP `wv2_market_snapshot` | Telegram quality |
|----------|-----|---------------------------|------------------|
| 07:38 | open | yes (logs) | Verbose Key Metrics dump |
| 08:08 | hourly | yes | Quiet symbol list (AAAU…) |
| 09:26 | hourly | yes | Quiet multi-symbol dump |
| 10:21 | hourly | yes | Quiet dump + menu + placeholders (principal sample) |
| 11:20 | hourly | yes | Verbose “Key Observations” |
| 12:11 | hourly | yes | Empty set + still multi-bullet summary (not one line) |
| 13:06 | hourly | yes | Empty set + speculation list |
| 14:08 | hourly | yes | AAAU `testing` buried in multi-symbol list (should be short radar) |

**Cadence reliability (2026-07-21): green** — open + all 8–14 MT hourlies completed (`status: ok` in `cron/runs/`). Principal “last at 10:21” was the attention-worst sample; later slots still posted.

**2026-07-21 16:20 MT ops:** `bin/seed-cromwell-workspace --force-cron` + `compose --profile ai restart nanobot_cromwell`. Workspace skill + cron messages now include hard `All markets quiet.` path.

**Post-seed observation 2026-07-22 (soft prompt FAIL for attention):**

| Local MT | Job | MCP | Prompt has quiet hard rules | Telegram quality |
|----------|-----|-----|-----------------------------|------------------|
| 07:42 | open | yes (`{}`) | yes | `message` tool posted multi-symbol dump (logs); run `response` field **empty** |
| 08:07 | hourly | yes | yes | Verbose “Notable Movers” including **quiet** AAL + **Would you like** menu |
| 09:13 | hourly | yes | yes | Multi-symbol dump (not one-liner when quiet-ish) |
| 10:08 | hourly | yes | yes | Still multi-paragraph radar waffle |
| 11:07 | hourly | yes | yes | Quiet symbols listed + menu + invented path to tool-results file |

**Conclusion:** Cadence/MCP still green. Soft skill+cron text is **not** sufficient for attention discipline. Escalate to **runtime** work on attention-discipline ticket. Overnight watcher raced `status=queued` — do not trust its heuristic.

## Acceptance criteria

- [ ] Capture at least **two** natural `market-snapshot-hourly` runs during NYSE session (or one forced + one natural)
- [ ] For each: note whether `mcp_winston_wv2_market_snapshot` (or equivalent) was invoked in `nanobot_cromwell` logs
- [ ] For each: note Telegram text quality (placeholder / invented stable / real brief from tool / **attention-correct quiet one-liner**)
- [ ] For each: if tool returns `movers`, post lists symbol + prev close + current + ATR; if empty movers → **one line** (`All markets quiet.` or equivalent) — not a quiet symbol table
- [ ] No numbered menus on scheduled snapshot posts
- [ ] Record findings on this ticket (or close as Done with summary linking issue)
- [ ] If still failing, point residual work at hardening / attention-discipline tickets rather than re-investigating from scratch

## How to check

```bash
podman logs --since "…" nanobot_cromwell 2>&1 | grep -E "market-snapshot-hourly|wv2_market_snapshot|path/to/file|Response to telegram"
```

Session: `ai/data/cromwell-bot/workspace/sessions/telegram_-1003884714483.jsonl`

## Related

- Issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md)
- Hardening (Done offline 2026-07-20 — deploy image + seed, then observe here): [`docs/tickets/2026-07-13-cromwell-cron-hallucination-hardening.md`](2026-07-13-cromwell-cron-hallucination-hardening.md)
- Prior: [`docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md)
- Session: [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
