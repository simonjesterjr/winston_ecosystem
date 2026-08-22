# Ticket: EODHD lag retry when 15:30 MT pull misses today’s print

**Status:** In progress  
**Priority:** P0  
**Date:** 2026-08-18  
**Updated:** 2026-08-22  
**Related:** [`2026-08-18-after-close-eod-session-contract.md`](2026-08-18-after-close-eod-session-contract.md); ADR-012; issue [`docs/issues/2026-08-22-friday-dar-hold-was-not-scored.md`](../issues/2026-08-22-friday-dar-hold-was-not-scored.md)

## Problem

data_manager (DM) now requests through the completed New York session at 15:30 Mountain (17:30 Eastern). If End of Day Historical Data (EODHD) has not published that print yet, parquet stays on the prior session. Winston v2 (Wv2) exact-bar readiness will then skip Operational Portfolios as `missing_data` instead of a false hold — honest, but the evening DAR still has no today.

**Triggered** Friday 2026-08-21: 15:30 Mountain missed the print; 16:30 DAR published hold; Saturday 08:00 weekend sync wrote Friday bars. See issue 2026-08-22.

## Acceptance (when triggered)

- [x] Reproduce: Friday 2026-08-21 after-close, EODHD last date &lt; completed session
- [ ] Retry / second pull before 17:00 Mountain (DAR waits on a Scored Session)
- [ ] Spec locks “session date requested but print absent → retry, not mark ready”
- [x] No return to `Date.current - 1` as the after-close `to`
- [x] Catch-up Daily Analysis mints tasks when bars arrive; no false-hold DAR; no required replacement DAR (Friday 2026-08-21 → 13 Saturday-desk tasks, fill 2026-08-24, Telegram off)

## Related

- Observe next Friday: [`2026-08-22-observe-friday-scored-session-dar.md`](2026-08-22-observe-friday-scored-session-dar.md)
- Observe (prior): [`archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md`](archive/2026-08-18-observe-tuesday-unattended-eod-cycle.md)
- Radar cousin: [`2026-07-13-stale-parquet-prior-close-active-symbols.md`](2026-07-13-stale-parquet-prior-close-active-symbols.md)
