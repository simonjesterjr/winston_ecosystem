# Ticket: Work Monday 2026-08-17 catch-up desk tasks (12 pending)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-18  
**Related:** session [`docs/session-reports/2026-08-18-1000-after-close-eod-session-contract.md`](../session-reports/2026-08-18-1000-after-close-eod-session-contract.md)

## Problem

Monday’s close was scored after the session-contract fix. Twelve human-gated paper tasks are **pending** in the ops shell. Last night’s Telegram DAR still says 0 actions (msg 774). Catch-up DAR did **not** re-broadcast.

This is operator desk work, not an engineering change.

## Desk list

All `session_bar_date=2026-08-17`, status pending:

| Task | OP | Type | Market | Journal |
|------|-----|------|--------|---------|
| 677 | Rust `dd7e7c7a` | enter | DBE | 905 |
| 678 | Orange `7ea76741` | enter | SMH | 906 |
| 679 | Orange | pyramid | ZROZ | 907 |
| 680 | Orange | pyramid | VXX | 908 |
| 681 | Blue `f4dd31eb` | pyramid | TSLA | 909 |
| 682 | Blue | enter | PG | 910 |
| 683 | Blue | pyramid | XLE | 911 |
| 684 | Mint `0478e0ea` | enter | OIH | 912 |
| 685 | Mint | pyramid | VNQ | 913 |
| 686 | Mango `45c09e30` | enter | MSFT | 914 |
| 687 | Mango | pyramid | COMB | 915 |
| 688 | Yellow `7aa73357` | enter | REMX | 916 |

Turtle Mint `85730621` had no Monday setup.

## Acceptance

- [ ] Each row Confirm or Pass in ops shell / desk workflow
- [ ] No re-mint of Friday-only names (BFIX, SCHD, USDU, FPA, NVDA, WMT, XOP, RXT, SVXY)
- [ ] Optional: Telegram redelivery of Monday DAR only if the operator asks
