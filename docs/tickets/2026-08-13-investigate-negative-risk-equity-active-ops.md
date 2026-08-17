# Ticket: Investigate negative risk_equity on Active OPs

**Status:** Superseded — classified 2026-08-17  
**Priority:** P2  
**Date:** 2026-08-13  
**Monolith:** winston_v2  
**See:** session `2026-08-13-0850-turtle-walnut-risk-equity-wrap.md`; `Operations::RiskEquity`  
**Superseded by:** [`2026-08-17-wv2-equity-wut-parity-flow-dar-shell.md`](2026-08-17-wv2-equity-wut-parity-flow-dar-shell.md) · issue [`../issues/2026-08-17-wv2-short-flow-breaks-wut-equity.md`](../issues/2026-08-17-wv2-short-flow-breaks-wut-equity.md)

**Classification:** not stale marks / lot identity. Short stock journals are booked as cash **debits** (`signed_flow` ignores direction). Equity = cash + long MV − short MV then double-counts shorts. Implementation moved to the 2026-08-17 ticket.

## Problem

Live RiskEquity smoke (2026-08-12) showed **negative risk_equity** on some Active Operational Portfolios (e.g. Mint / Blue / Orange forks) while free cash was also stressed. That confuses dual-metric DAR and may indicate mark/journal/lot identity bugs — not dual-metric plumbing itself.

Examples from smoke (as_of report day):

| OP | free_cash | risk_equity |
|----|-----------|-------------|
| Orange · 7ea76741 | ~318 | **~−971** |
| Blue · f4dd31eb | ~149 | **~−4070** |
| Mint · 0478e0ea | ~−2440 | **~−14807** |

## Scope

1. For each affected OP: list open lots, marks used, journal flow sums, CashEvents.  
2. Classify: short MV, stale marks, wrong direction, double-count, or expected.  
3. Fix bugs if found; else document operator hygiene (close/archive dead paper).  
4. Spec if a concrete bug is isolated.

## Acceptance

- [ ] Classification table per affected Active OP  
- [ ] Bugs fixed or archive recommendation  
- [ ] No false over-deployed from free_cash/risk_equity disagree bugs (free_cash alignment already fixed)  

## Non-goals

- Changing OVER_DEPLOYED_RATIO  
- Full journal ledger redesign  
