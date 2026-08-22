# Ticket: Work Friday 2026-08-21 catch-up desk tasks (13 pending)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-22  
**Related:** issue [`docs/issues/2026-08-22-friday-dar-hold-was-not-scored.md`](../issues/2026-08-22-friday-dar-hold-was-not-scored.md); session [`docs/session-reports/2026-08-22-1429-friday-dar-scored-session-gate.md`](../session-reports/2026-08-22-1429-friday-dar-scored-session-gate.md)

## Problem

Friday’s close was scored on Saturday via mint-only catch-up (Telegram off; Friday DAR not replaced). Thirteen human-gated paper tasks are **pending** on the ops shell (`as_of` 2026-08-22). Fill Date is **Monday 2026-08-24**.

This is operator desk work, not an engineering change.

## Desk list

All `report_date=2026-08-21`, `fill_date=2026-08-24`, status pending:

| Task | Journal | OP | Type | Market |
|------|---------|----|------|--------|
| 790 | 1061 | Orange · 7ea76741 | exit | BITQ |
| 791 | 1062 | Orange · 7ea76741 | exit | COPR |
| 792 | 1063 | Orange · 7ea76741 | enter | MSOS |
| 789 | 1060 | Rust · dd7e7c7a | pyramid | AAAU |
| 793 | 1064 | Blue · f4dd31eb | pyramid | TSLA |
| 794 | 1065 | Mint · 0478e0ea | pyramid | USO |
| 795 | 1066 | Mango · 45c09e30 | pyramid | BIB |
| 796 | 1067 | Mango · 45c09e30 | pyramid | PPLT |
| 797 | 1068 | Mint · 85730621 | pyramid | XOP |
| 798 | 1069 | Yellow · 7aa73357 | enter | AEP |
| 799 | 1070 | Yellow · 7aa73357 | pyramid | REMX |
| 800 | 1071 | Yellow · 7aa73357 | pyramid | IAU |
| 801 | 1072 | Yellow · 7aa73357 | pyramid | SGOL |

Mango BIB/PPLT and Mint S2 XOP are the same pyramids declined earlier this week. Yellow BNO entry from the dry scan did not mint.

## Acceptance

- [ ] Each row Confirm or Pass in ops shell / desk workflow before Monday open
- [ ] No new Friday DAR / no Telegram rebroadcast unless the operator asks
- [ ] Pending count 0 after the desk is worked
