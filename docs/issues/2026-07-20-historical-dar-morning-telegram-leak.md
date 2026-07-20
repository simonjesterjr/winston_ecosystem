# Issue: Historical DAR posted to Sawtooth Main from morning cron

**Status:** Fixed in tree — Wv2/MCP date+Telegram guards; cron MCP allowlist live; demo DARs quarantined  
**Observed:** 2026-07-20 ~07:47 MDT (repeat of Jul 15 / Jul 16 pattern)  
**Channel:** Telegram Sawtooth Main (`chat_id=-1003884714483`)  
**Scope:** Cromwell agent quality + missing Wv2/MCP hard guards on historical Daily Analysis / Telegram delivery

## Symptom

At **7:47 AM MDT**, Sawtooth Main received:

1. **Caption** (Wv2 `TelegramReportDelivery`):

   > Winston Daily Activity Report — **2023-10-15** (paper)  
   > Portfolios: Portfolio Orange · 6622b2eb, Portfolio Rust · dd7e7c7a, Portfolio Blue · PBR62, Portfolio Mango (WUT run 57)  
   > Actions: 0 · Pending: 0 · Next steps: 0  
   > Human-gated: …  
   > Channel: Sawtooth Main

2. **Agent prose** (same cron session): “The `mcp_winston_wv2_perform_daily_analysis` tool was executed successfully on 2023-10-15…” with empty-signals menu.

This is **not** an EOD DAR. Legitimate EOD is Sidekiq `DailyAnalysisJob` at **4:30 PM MT** + Cromwell `eod-daily-report` at **4:35** with `fetch_only: true`.

## Root cause

**Agent loop quality after output truncation + no hard date/Telegram policy.**

Verified timeline (`cron_market-snapshot-open` session + audit):

| Time (MT) | Event |
|-----------|--------|
| 07:30 | Cron `market-snapshot-open` — prompt **FORBIDDEN:** `perform_daily_analysis`, `get_daily_activity_report` |
| ~07:30–07:50 | Agent **hallucinates** snapshot movers (no tool call), hits output limit |
| Continue turn | Agent calls `wv2_perform_daily_analysis` with `date=2023-10-15`, `parent_correlation_id=abc123`, `portfolio_id_or_name=Portfolio White` |
| 07:47 | Wv2 evaluate accepts past date → builds PDF/MD → **auto-Telegram** + webhook |
| 07:50 | Agent posts empty-results narrative to Sawtooth Main |

Evidence:

- Session: `ai/data/cromwell-bot/workspace/sessions/cron_market-snapshot-open.jsonl` (tool call `call_m7vevpa8`)
- MCP audit: `ecosystem/logs/audit/mcp/mcp_audit_20260720.jsonl` correlation `53803f16-…`
- Notification: `winston_v2/storage/cromwell_notifications/wv2_20231015.json` (`generated_at: 2026-07-20T13:47:20Z`, `telegram_delivery.delivered: true`)
- Webhook: `ecosystem/logs/audit/webhook/20260720T134720_daily_complete.json`

### Why the date was 2023-10-15

Not a live market as-of. Recycled **test/demo** date:

| When | Report date | parent_correlation_id |
|------|-------------|------------------------|
| 2026-07-15 ~13:11 MT | 2023-10-15 | `abc123` (first birth of artifacts) |
| 2026-07-16 ~07:45 / 08:24 MT | 2025-06-14 | `abc123` |
| **2026-07-20 ~07:47 MT** | **2023-10-15** | **`abc123`** |

`parent_correlation_id: "abc123"` is an LLM placeholder, not a real chain id.

### Stacked failure modes

1. **Primary (agent):** Morning snapshot cron model ignores FORBIDDEN and invents `perform_daily_analysis` after truncation continue.
2. **Wv2 schedule gap:** `DailyReportSchedule.analysis_allowed?` only blocks *future* / pre-cutoff **today**. **Any past date is allowed.**
3. **Telegram gap:** `CromwellNotifier#deliver_telegram!` posts every successful `daily_complete` to Sawtooth Main (unless `WV2_TELEGRAM_DELIVER=0`).
4. **MCP gap:** Accepts arbitrary `date` with no production-vs-historical flag.

## What is *not* broken

- Intended EOD path: Sidekiq `30 16 * * * America/Denver` + prior-day reports (e.g. `2026-07-19` at 16:30 MT) still look healthy
- Caption/PDF plumbing for real EODs
- Portfolio capital mutation from this incident (empty signals; paper evaluate only)

## Impact

| Area | Impact |
|------|--------|
| Channel trust | Fake historical DAR in production group chat |
| Misguidance | Principals may treat empty 2023 analysis as “no trades today” |
| Ops noise | Follow-up agent menu after forbidden tool |
| Repeat risk | Same pattern Jul 15, Jul 16, Jul 20 — will recur without hard guards |

## Policy (operator rule)

1. **DARs are end-of-day only** (after NY close; ecosystem uses **4:30 PM MT** analysis + **4:35** delivery).
2. **Never** emit a DAR for a past date to Sawtooth Main unless an **explicit test pass** opts in.
3. Morning jobs = status / market snapshot only — never analysis.

## Fix plan

| Layer | Guard |
|-------|--------|
| Wv2 `DailyReportSchedule` | `production_date?` = `default_report_date`; evaluate blocked for other dates unless `allow_historical=true` |
| Wv2 Telegram | Auto-deliver only when `production_date?` (or explicit historical telegram force) |
| MCP | Surface `allow_historical`; refuse/forward policy with clear 422 guidance |
| Cromwell (follow-up) | Tool allowlists per cron — ticket [`../tickets/2026-07-20-cromwell-cron-tool-allowlist.md`](../tickets/2026-07-20-cromwell-cron-tool-allowlist.md); soft FORBIDDEN is insufficient |
| Artifact hygiene | Quarantine demo DARs — ticket [`../tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md`](../tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md) |

## Related

- Issue: [`2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](2026-07-13-cromwell-cron-placeholder-path-hallucination.md) — same class: truncation continue → hallucinated tools/paths
- Skill soft rules: `ecosystem/ai/skills/winston-daily-ops`, cron `eod-daily-report` / `market-snapshot-open` in `ecosystem/ai/schedule/cromwell-cron.json`
- Schedule service: `winston_v2/app/services/daily_report_schedule.rb`
