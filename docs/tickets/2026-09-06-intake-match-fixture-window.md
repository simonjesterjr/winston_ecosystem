# Ticket: Confirmation Intake match specs — freeze fixture window

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Edges:** `ConfirmationIntake::MatchNotification::WINDOW_DAYS` (7); fixtures dated 2026-08-19  
**Human gates:** none  
**DoD:** `spec/services/confirmation_intake/match_and_prefill_spec.rb` green on a date after the 7-day window without hitting live DUT  
**Series:** Confirmation Intake  
**Origin:** [`docs/session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md`](../session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md)

## Problem

Match fixtures (`trade-executed-exact.json` and kin) have `occurred_at: 2026-08-19`. Journals in the spec use `Date.current`. `WINDOW_DAYS = 7`. On 2026-09-06 the exact/ambiguous/soft/mismatch examples return **orphan**. Not caused by ADR-013 Accept-Fill. Date-fragile; will keep failing.

## Scope

1. Freeze `Date.current` (and occurred_at) in the spec **or** set journal `trade_date` / fixture occurred_at inside the window.  
2. Do not widen `WINDOW_DAYS` as a substitute for frozen time.

## Non-goals

- Changing match law.  
- Live broker.

## Acceptance

- [ ] Isolated `match_and_prefill_spec` green regardless of calendar date  
- [ ] Comment in spec: window is 7 calendar days around journal dates  
