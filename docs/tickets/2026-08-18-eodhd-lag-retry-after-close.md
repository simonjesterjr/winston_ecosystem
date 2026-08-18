# Ticket: EODHD lag retry when 15:30 MT pull misses today’s print

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-18  
**Related:** [`2026-08-18-after-close-eod-session-contract.md`](2026-08-18-after-close-eod-session-contract.md); session [`docs/session-reports/2026-08-18-1000-after-close-eod-session-contract.md`](../session-reports/2026-08-18-1000-after-close-eod-session-contract.md)

## Problem

data_manager (DM) now requests through the completed New York session at 15:30 Mountain (17:30 Eastern). If End of Day Historical Data (EODHD) has not published that print yet, parquet stays on the prior session. Winston v2 (Wv2) exact-bar readiness will then skip Operational Portfolios as `missing_data` instead of a false hold — honest, but the evening DAR still has no today.

Do **not** implement until tonight’s observe ticket shows a miss. File work here only if 15:30 Mountain still lacks today’s bar after the window fix.

## Acceptance (when triggered)

- [ ] Reproduce: after-close cron, EODHD last date &lt; completed session
- [ ] Retry / second pull before 16:30 Mountain DAR (or delay DAR until coverage matches)
- [ ] Spec locks “session date requested but print absent → retry, not mark ready”
- [ ] No return to `Date.current - 1` as the after-close `to`

## Related

- Observe first: [`2026-08-18-observe-tuesday-unattended-eod-cycle.md`](2026-08-18-observe-tuesday-unattended-eod-cycle.md)
- Radar cousin: [`2026-07-13-stale-parquet-prior-close-active-symbols.md`](2026-07-13-stale-parquet-prior-close-active-symbols.md)
