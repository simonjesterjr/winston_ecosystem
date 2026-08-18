# Ticket: Verify ops-shell Pending grouping on a live multi-OP mint

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-08-18  
**Monolith:** winston_v2  
**Domain:** Ops shell (`/operations`), Pending panel  
**Related:** [`2026-08-12-ops-shell-next-steps-by-portfolio.md`](2026-08-12-ops-shell-next-steps-by-portfolio.md) (Done); session [`docs/session-reports/2026-08-18-1337-ops-shell-pending-by-portfolio.md`](../session-reports/2026-08-18-1337-ops-shell-pending-by-portfolio.md)

## Problem

Pending-by-portfolio shipped and passed compose specs, but live `/operations` had **0** pending after Monday’s catch-up. First paint and JSON refresh were not clicked through with ≥2 Operational Portfolios (OPs) that each have tasks.

## Scope

Operator observation after the next real mint (tonight’s unattended Daily Analysis Report (DAR) if it creates tasks, or a later session). Not a code change unless grouping is wrong.

## Acceptance

- [ ] ≥2 Active OPs have pending tasks at once
- [ ] Pending panel shows distinct `#id` + lineage headers (not one flat type list)
- [ ] REAL band (if any) is above PAPER
- [ ] Empty OPs omitted; Refresh does not flash a flat list
- [ ] If grouping is wrong, reopen the parent ticket or file an issue — do not remint to force a screenshot

## Non-goals

- Reminting Monday tasks
- Changing the 25-row pending cap
- Ops-shell chat `pending` (still flat; parent non-goal)

## Related

- Observe tonight first: [`2026-08-18-observe-tuesday-unattended-eod-cycle.md`](2026-08-18-observe-tuesday-unattended-eod-cycle.md)
