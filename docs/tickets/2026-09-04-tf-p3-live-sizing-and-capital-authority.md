# Ticket: P3 — Live sizing: Capital Authority into the sizer

**Status:** Proposed  
**Priority:** P1 — grill law from 2026-09-01 is not yet Ruby; blocks honest real-capital size  
**Date:** 2026-09-04  
**Monolith:** Wv2 PositionSizer / Daily Analysis; WUT already has N-unit + RiskScale  
**Principle:** Kelly / Thorp / Soros / Buffett  
**Page:** `winston_foundations/20260904/03-the-sizing-problem.md`  
**Parent:** [`2026-09-04-tf-foundations-competency-epic.md`](2026-09-04-tf-foundations-competency-epic.md)

## Problem

Live Trend Following books size a **fixed 1% of notional risk equity, at signal-bar ATR**, with a human as last sizer. That is a competent Turtle chassis. It is **not** Kelly/Thorp growth optimality.

Glossary already names **Capital Authority**, **Risk Capital**, **Broker Buying Power**, **Leverage Guardrail**, **Spending Capacity**, **Moment of Truth**. There are **no Ruby identifiers** for the first four as sizer inputs. `max_leverage` is stored; PositionSizer does not enforce it.

One-Way Dynamic (OWD) is not the live default (operator preference after drawdown). Daily Analysis also **does not pass `pyramid_position_number`**, so even an OWD Operational Portfolio drafts **level-1** size.

Kelly engine is ported to Winston v2; observation recipes (Mint S2, Yellow S1) are `risk_scale_policy: none`. Yellow matrix forbade a global Kelly default.

## Desired outcome

1. Persist **Capital Authority** on the Operational Portfolio; PositionSizer takes **Risk Capital** (notional ledger or broker net liquidation).  
2. **Leverage Guardrail + Spending Capacity** in Daily Analysis and confirm: gross long+short vs equity × cap (default 2×); broker buying power as hard ceiling; per-ticket human override cannot exceed broker reject.  
3. **Moment of Truth** sizing: recompute units from fill-instant N and remaining spending capacity — required before Slate Automation.  
4. **OWD wiring decision:** pass concurrent pyramid level into ProposedSize, **or** refuse OWD Operational Portfolios at import for live TF. Do not leave a silent level-1 draft.  
5. One percent/fraction store convention so `risk_percentage` 1.0 cannot mean 100% again.  
6. Kelly remains **host-specific paper observation** (Mango wk66 ticket), never a global default.

## Must preserve

- ADR-010: Kelly not global default; Martingale research/paper only; live multiplier not in fingerprint  
- Turtle static 1% as current live chassis until an evidence-gated successor  
- Signal-path share units for Daily Analysis; extra-modal packaging does not retarget Books  
- Unit Heat occupancy (do not replace with a second Kelly allocator in v1)  

## Out of scope

- Slate Contest ranking (existing ticket; cite it)  
- Exit Capital Reconcile / Risk Modality math (P6 + packaging UI ticket)  
- Porting One-Way Dynamic Close to Wv2 as a default  

## Acceptance

- [ ] PositionSizer tests: notional vs broker-authority Risk Capital produce different unit counts on a fixture  
- [ ] Guardrail refuse + buying-power ceiling covered by specs  
- [ ] Documented OWD import/DA decision (wire or refuse)  
- [ ] CONTEXT and ADR-010 consequences marked implemented or explicitly deferred with owner  
- [ ] No live book ships `risk_scale_policy: kelly` without the Mango observation ticket closing first  

## Related existing work

- ADR-008, ADR-010  
- `docs/tickets/2026-07-30-kelly-martingale-sizing-portfolio-management.md`  
- `docs/tickets/2026-07-31-kelly-scale-not-global-default.md` (doctrine Done)  
- `docs/tickets/2026-08-09-kelly-mango-wk66-fingerprint-paper.md`  
- `docs/tickets/2026-08-13-importer-risk-percentage-one-percent.md` (fixed; footgun remains)  
- `docs/tickets/2026-09-01-wv2-unit-heat-slate-contest.md`  
- Grill 2026-09-01 Q2 (Risk Capital / buying power / guardrail)  

## Promote to plan when

Accepted as cross-monolith (Wv2 sizer + Broker Gateway balances + DA) → `ecosystem/plans/tf-capital-authority-sizer.md`.
