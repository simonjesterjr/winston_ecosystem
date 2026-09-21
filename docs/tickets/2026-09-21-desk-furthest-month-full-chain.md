# Ticket: Desk Plan B still ATM-3 of one month, not the listed call surface

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-21  
**Mode:** contractor  
**Graph nodes:** broker_gateway (`Adapters::Ibkr::LeapCandidates#pick_month`, `#pick_strikes`, `ATM_LIMIT`); winston_v2 (`CallFulfillmentSelector`, Justification)  
**Implementer:** Winston Dev  
**Human gates:** Mode C paper; quotes from CPGW only; no Black–Scholes; agent never Desk-Sends  
**DoD:** Operator can see (Justification or a chain panel) more than the three at-the-money (ATM) strikes of the furthest month, **or** a documented decision that ATM-3 of furthest month is enough.  
**Origin:** Wrap [`../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md`](../session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md) §14 item 3  
**Related:** ADR-018 2026-09-21 furthest-expiry lock; BG LeapCandidates; packaging [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](2026-09-19-standard-call-fulfillment-packaging-rung.md)

## Problem

2026-09-21 lock: pick the **furthest listed month** in the rung window. The Interactive Brokers (IBKR) walker still returns **ATM_LIMIT = 3** strikes of **that one month**. Full SEF / BITQ surfaces (40+ listed calls) were dumped in chat for out-of-band comparison; Justification does not list rejected Options Clearing Corporation (OCC) rows.

Consequences:

- A better strike in the furthest month (e.g. SEF Feb 28C vs 30C) never enters the selector if it is outside ATM-3.  
- Nearer months are correctly excluded by law; that is not this ticket.  
- Operator cannot see *why* Plan B picked 30 vs 29 without a rails runner.

## Scope (pick in implementation, not here)

- Widen `pick_strikes` / `ATM_LIMIT` for the furthest month, **or**  
- Dual-fetch a few extra strikes around spot, **or**  
- Stamp `selection_trace` onto Justification (rejected reasons already exist on the selector).

Do not invent greeks or quotes. Empty snapshot stays untradeable.

## Non-goals

- Returning every expiry (that would fight furthest-month law)  
- Desk-Send / `place_order`  
- Changing 8%/200 defaults (Mode C paper UAT knobs are a separate ops question)

## Acceptance

- [ ] Decision recorded: ATM-3 of furthest month is enough, **or** walker/selector returns a wider strike set for that month  
- [ ] If wider: spec that a non-ATM-3 in-band row in the furthest month can win  
- [ ] If keep ATM-3: Justification shows selection_trace so HITL sees the three rows
