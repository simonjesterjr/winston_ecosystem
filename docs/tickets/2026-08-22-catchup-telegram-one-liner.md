# Ticket: Optional catch-up Telegram one-liner (desk-only is the default)

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-22  
**Related:** ADR-012; session [`docs/session-reports/2026-08-22-1429-friday-dar-scored-session-gate.md`](../session-reports/2026-08-22-1429-friday-dar-scored-session-gate.md)

## Problem

When Daily Analysis catch-up mints tasks after a **Not Scored** evening (bars arrived late), ADR-012 does **not** send a second Daily Activity Report (DAR) PDF. The operator only sees work on the current desk. That avoids a fake second “daily.” It also means Sawtooth Main stays quiet while pending appears.

## Locked default

Desk-only. No replacement DAR. No second PDF.

## Optional (only if operator reopens)

- [ ] One-line Telegram: `Catch-up: N next actions for YYYY-MM-DD on the desk (fill DATE). Not a new DAR.`
- [ ] Never attach the old hold PDF or a rewritten DAR
- [ ] Spec: mint_only does not call `TelegramReportDelivery` unless this flag is on

Do **not** implement until the operator asks to reopen.
