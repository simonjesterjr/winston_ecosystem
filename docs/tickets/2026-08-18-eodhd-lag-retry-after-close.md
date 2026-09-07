# Ticket: EODHD lag retry when 15:30 MT pull misses today’s print

**Status:** Done  
**Priority:** P0  
**Date:** 2026-08-18  
**Updated:** 2026-09-07  
**Related:** [`2026-08-18-after-close-eod-session-contract.md`](2026-08-18-after-close-eod-session-contract.md); ADR-012; issue [`docs/issues/2026-08-22-friday-dar-hold-was-not-scored.md`](../issues/2026-08-22-friday-dar-hold-was-not-scored.md)

## Problem

data_manager (DM) now requests through the completed New York session at 15:30 Mountain (17:30 Eastern). If End of Day Historical Data (EODHD) has not published that print yet, parquet stays on the prior session. Winston v2 (Wv2) exact-bar readiness will then skip Operational Portfolios as `missing_data` instead of a false hold — honest, but the evening DAR still has no today.

**Triggered** Friday 2026-08-21: 15:30 Mountain missed the print; 16:30 DAR published hold; Saturday 08:00 weekend sync wrote Friday bars. See issue 2026-08-22.

## Acceptance (when triggered)

- [x] Reproduce: Friday 2026-08-21 after-close, EODHD last date &lt; completed session
- [x] Retry / second pull before 17:00 Mountain (DAR waits on a Scored Session)
- [x] Spec locks “session date requested but print absent → retry, not mark ready”
- [x] No return to `Date.current - 1` as the after-close `to`
- [x] Catch-up Daily Analysis mints tasks when bars arrive; no false-hold DAR; no required replacement DAR (Friday 2026-08-21 → 13 Saturday-desk tasks, fill 2026-08-24, Telegram off)

## Live evidence

| Date | What happened |
|------|----------------|
| Fri 2026-08-21 | Pre-ADR: 16:31 MT `daily_complete` hold; 7 OPs `missing_data` |
| Fri 2026-08-28 | Unattended scored DAR 16:31 MT (`session_status=scored`, 16 next steps) — print was present |
| Fri 2026-09-04 | Unattended scored DAR 16:30 MT (`session_status=scored`) — print was present |
| Mon 2026-09-07 (Labor Day) | First live **Not Scored**: DA 16:30–17:03 MT wrote `daily_not_scored` (70 symbols, latest parquet **2026-09-04**). No hold DAR. Old retry job then **rewrote 106 symbols through 17:05 MT** (7-year pull after the deadline). |

## 2026-09-07 fix

`SessionCoverageRetryJob` now **probes EODHD for the session print** before any parquet rewrite, **stops at 17:00 MT before work**, and re-enqueues only while stale. `request_consumer_sync` is async (`ConsumerSyncJob`) and skips rewrite when history exists but the print is absent. Winston v2 `SessionDataGate` pokes data_manager once, then polls ingest.

Holiday calendar remains ADR-012 v1 (weekday with no print → Not Scored). See [`2026-09-07-completed-ny-session-us-holiday-calendar.md`](2026-09-07-completed-ny-session-us-holiday-calendar.md).

## Related

- Observe next Friday: [`2026-08-22-observe-friday-scored-session-dar.md`](2026-08-22-observe-friday-scored-session-dar.md)
- Observe (prior): [`archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md`](archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md)
- Radar cousin: [`2026-07-13-stale-parquet-prior-close-active-symbols.md`](2026-07-13-stale-parquet-prior-close-active-symbols.md)
