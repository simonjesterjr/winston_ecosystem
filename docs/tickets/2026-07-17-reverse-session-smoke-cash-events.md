# Ticket: Reverse session smoke cash on Orange / Rust

**Status:** Proposed  
**Date:** 2026-07-17  
**Source:** Session `docs/session-reports/2026-07-16-2210-public-url-cash-dar-error-guidance.md`  
**Priority:** Low (ops hygiene)

## Problem

Live verification of `wv2_add_cash_event` left real inflows on Active paper OPs:

| OP | CashEvent | Amount | capital_base after |
|----|-----------|--------|--------------------|
| #6 Portfolio Orange · 6622b2eb | #100 | +$100 | 10100 |
| #11 Portfolio Rust · dd7e7c7a | #101 | +$50 | 10050 |

These were intentional smokes, not operator capital policy.

## Scope

1. Optional reverse via `adjustment` −100 (Orange) and −50 (Rust), or leave if operator prefers the top-up.  
2. Prefer MCP/internal: `wv2_add_cash_event` with `event_type=adjustment` and notes citing this ticket.  
3. Do **not** delete CashEvent history rows if reverse is chosen — record offsetting adjustments.

## Acceptance

- [ ] Operator decision: reverse or keep  
- [ ] If reverse: capital_base back to pre-smoke (10000 each, modulo other activity)  
- [ ] Notes auditable (`source=…` + ticket ref)

## Related

- Cash path: `docs/tickets/2026-07-14-wv2-cash-inflow-mcp.md` (Done)  
- Session: [`docs/session-reports/2026-07-16-2210-public-url-cash-dar-error-guidance.md`](../session-reports/2026-07-16-2210-public-url-cash-dar-error-guidance.md)
