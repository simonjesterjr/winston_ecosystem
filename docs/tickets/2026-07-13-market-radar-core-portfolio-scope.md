# Ticket: Limit intraday market radar to core Active portfolios

**Status:** Proposed  
**Context:** Session `docs/session-reports/2026-07-13-1307-intraday-market-radar.md`. Live `wv2_market_snapshot` now returns ~47 symbols from all Active Books; many small-ATR ETFs produce dense “breach” lists that dilute attention.

## Problem

The market radar is a focusing tool for core users with active portfolios. Scoping to **all** Active Books floods movers (commodity/bond/levered ETFs with tiny ATR). Team Telegram posts risk becoming noise rather than weather radar.

## Acceptance criteria

- [ ] Decide product rule: all Active vs named subset vs Active + `execution_mode` / portfolio tag
- [ ] Implement filter in `MarketSnapshotService` (or portfolio flag) if subset chosen
- [ ] Cromwell skill/cron still work without arg changes (or document optional filter args)
- [ ] Smoke: mover list is short enough for one Telegram paragraph on a normal day

## Related

- Session: [`docs/session-reports/2026-07-13-1307-intraday-market-radar.md`](../session-reports/2026-07-13-1307-intraday-market-radar.md)
- Code: `winston_v2/app/services/market_snapshot_service.rb`
- Skill: `ecosystem/ai/skills/winston-market-snapshot/SKILL.md`
