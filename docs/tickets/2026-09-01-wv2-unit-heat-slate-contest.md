# Ticket: Port Unit Heat and Slate Contest into Winston v2 Daily Analysis

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** winston_v2, winston_unit_test  
**Edges:** Portfolio Correlation Score pairwise map; WUT `HeatCapacityGate`  
**DoD:** DA contests are Turtle-mechanical; no expected-return menu  
**Blocked on:** not required for WQ paper; needed before Slate Automation code  
**Origin:** Grill 2026-09-01 Q8 — [`docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md`](../session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md)

## Problem

Live contests are **Unit Heat** (Faith caps; pairwise map from Portfolio Correlation Score) then **Slate Contest** (buy-strength / sell-weakness, first-to-touch). Winston Unit Test already has `PortfolioBacktest::HeatCapacityGate` and a PositionSwapEvaluator. Enabling swap on Blue **hurt** return and drawdown. Wv2 Daily Analysis must not rank by expected return or present a DAR pick-list.

## Scope

1. Port Faith unit-heat refuse (per market, close-corr, loose-corr, direction) into Wv2 DA / TaskGenerator.  
2. Remaining ties: buy-strength / sell-weakness; first-to-touch is a session-time rule once parks exist.  
3. Emit one Desk Handoff or algorithmic Passed Signal.  
4. Expected-return cycles stay lab/audit — optional DAR display later, never the picker.

## Non-goals

- Live expected-return swap of an open winner  
- Nightly human rank menu  
- Parking orders (L3)  

## Acceptance

- [ ] At-capacity correlated overflow is algorithmic pass with heat reason  
- [ ] Spec: no ER menu; WUT HeatCapacityGate behavior cited  
- [ ] DAR can show Turtle priorities as review copy, not as a picker
