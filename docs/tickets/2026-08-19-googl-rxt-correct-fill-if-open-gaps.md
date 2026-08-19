# Ticket: Correct-fill Rust GOOGL / RXT if 2026-08-19 open gaps

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-08-19  
**Related:** session [`docs/session-reports/2026-08-18-1823-rust-11-desk-confirms.md`](../session-reports/2026-08-18-1823-rust-11-desk-confirms.md); TSM remap session [`docs/session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md`](../session-reports/2026-08-19-1304-tsmc-to-tsm-storage-remap.md)

## Problem

Paper Operational Portfolio Rust `#11` drafts 937 (GOOGL short 9) and 938 (RXT pyramid 179) were confirmed **2026-08-18 evening at signal close** (340.19 / 3.51) as an operator override. Architecture Decision Record (ADR) 009 prefers Fill Date = next session **open** (2026-08-19). Lots **#565** / **#566** are the Single Fulfillment Identity — do not second-book.

## Scope

Operator desk after Wednesday’s bar exists (parquet latest ≥ 2026-08-19):

1. Load GOOGL and RXT session **open** for 2026-08-19.
2. If the open is materially different from 340.19 / 3.51, **correct-fill** the same lots (amend), with a note that the original book was a close proxy.
3. If the gap is noise, leave them and note “accepted close proxy” on this ticket.

## Acceptance

- [ ] 2026-08-19 GOOGL open vs 340.19 recorded
- [ ] 2026-08-19 RXT open vs 3.51 recorded
- [ ] Amend same lots **or** explicit accept of close proxy
- [ ] No second GOOGL/RXT enter against those signals

## Non-goals

- Changing EOD cadence / infer_price
- Telegram redelivery
