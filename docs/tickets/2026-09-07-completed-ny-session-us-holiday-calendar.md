# Ticket: CompletedNySession US holiday calendar

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-07  
**Mode:** normal  
**Graph nodes:** data_manager, winston_v2  
**Human gates:** none  
**DoD:** Labor Day / NYSE-closed weekdays request the prior session, not a print that will never exist  
**Origin:** Labor Day 2026-09-07 Not Scored wait — [`2026-08-18-eodhd-lag-retry-after-close.md`](2026-08-18-eodhd-lag-retry-after-close.md)

## Problem

ADR-012 v1 has no holiday calendar: a weekday with no print is still the `CompletedNySession` date. On Labor Day 2026-09-07, data_manager (DM) requested Monday bars, parquet latest stayed **2026-09-04**, Winston v2 (Wv2) Daily Analysis waited until 17:03 Mountain and wrote **Not Scored**. Honest, but the desk waited 30 minutes for a session that NYSE never opened.

The lag-retry probe now avoids rewriting 7-year parquet until End of Day Historical Data (EODHD) actually has the print. It does not stop the 16:30 wait on a known closed day.

## Scope

1. Named US equity holiday list (NYSE closed) on `CompletedNySession` — at least Labor Day, Thanksgiving, Christmas, New Year, MLK, Presidents', Good Friday, Juneteenth, Independence Day.  
2. On those weekdays after the nominal close, session date is the prior weekday (same as Saturday).  
3. Specs: Labor Day 2026-09-07 after 16:00 ET → 2026-09-04.  
4. ADR-012 addendum: holiday is a known non-session, not Not Scored.

## Non-goals

- Full exchange calendar / early-close days in v1 of this ticket  
- Changing Friday lag retry  
- Inventing a hold DAR on holidays  

## Acceptance

- [ ] `CompletedNySession.date` on Labor Day 2026-09-07 17:30 ET is Friday 2026-09-04  
- [ ] Daily Analysis that evening scores Friday or no-ops as “no new session,” not 30 minutes of Not Scored  
- [ ] ADR-012 / business-context holiday row updated  
