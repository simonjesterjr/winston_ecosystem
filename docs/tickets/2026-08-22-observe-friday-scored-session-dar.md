# Ticket: Observe next Friday unattended EOD — scored DAR, not hold

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-22  
**Due:** 2026-08-28  
**Related:** ADR-012; issue [`docs/issues/2026-08-22-friday-dar-hold-was-not-scored.md`](../issues/2026-08-22-friday-dar-hold-was-not-scored.md); ticket [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md); session [`docs/session-reports/2026-08-22-1429-friday-dar-scored-session-gate.md`](../session-reports/2026-08-22-1429-friday-dar-scored-session-gate.md)

## Problem

Friday 2026-08-21 Daily Analysis ran at 16:31 Mountain while parquet still lacked Friday bars. The Daily Activity Report (DAR) published **hold**. Saturday 08:00 weekend sync then wrote the session. The wait/retry path (ADR-012) is in tree but has not run on a live Friday.

## Observe (2026-08-28)

- [ ] 15:30 MT data_manager (DM) pull: `CompletedNySession` = Friday; if EODHD lags, `SessionCoverageRetryJob` retries until 17:00 MT
- [ ] 16:30 MT Winston v2 (Wv2) Daily Analysis **waits** if bars are missing (not skip-all + hold)
- [ ] DAR is a **Scored Session** (next steps or true hold) **or** explicit **Not Scored** — never missing_data presented as hold
- [ ] Telegram, if sent, matches that (no false quiet day)
- [ ] If bars arrive after 17:00, catch-up mint-only lands tasks on the current desk without replacing a scored DAR

## Not this ticket

Live retry **implementation** is [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md). This ticket is the Friday observe pass.
