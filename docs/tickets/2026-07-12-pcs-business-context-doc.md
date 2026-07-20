# Ticket: Business-context doc for Portfolio Correlation Score

**Status:** Proposed  
**Priority:** unset

**Date:** 2026-07-12  

## Problem

PCS glossary + ADR-007 exist; operators still lack a short domain explainer (how score is used in lab vs ops, flag thresholds, what rebalance means).

## Scope

Write `ecosystem/docs/business-context/portfolio-correlation-score.md`:

- PCS definition (max\|r\| first)  
- Methodology version discipline  
- Lab vs ops (WUT SoT, Wv2 client)  
- Flag thresholds (0.70 max\|r\|, 10pt PCS drop) — flag only, no auto rebalance  
- Link ADR-007, litmus analysis, plan  

## Acceptance

- [ ] Doc filed under business-context  
- [ ] Cross-linked from plan and ADR-007  

## Related

- `CONTEXT.md` terms already added  
- ADR-007 accepted  
