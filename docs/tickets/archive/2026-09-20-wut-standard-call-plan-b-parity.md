# Ticket: WUT lab parity for standard_call / ADR-018 Plan B (optional)

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-20  
**Mode:** contractor  
**Graph nodes:** winston_unit_test (`PortfolioBacktestRunner` leap packaging); winston_v2 selector is **not** copied blindly  
**Human gates:** Do **not** start unless the operator asks for lab parity  
**DoD:** If accepted: a Winston Unit Test (WUT) Portfolio Backtest Run (PBR) can prefer `standard_call` and Plan-B to shares when the call floor is 0, with the same vocabulary as ADR-018. Today WUT refuses LEAP when contracts floor to 0.  
**Origin:** Wrap [`../session-reports/2026-09-20-1140-standard-call-packaging-rung.md`](../session-reports/2026-09-20-1140-standard-call-packaging-rung.md); ADR-018 “parity is a separate decision”  
**Related:** [`2026-09-19-standard-call-fulfillment-packaging-rung.md`](2026-09-19-standard-call-fulfillment-packaging-rung.md) (Wv2 first; WUT out of scope); WUT [`../../../winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md`](../../../winston_unit_test/docs/tickets/2026-09-14-wut-leap-packaged-pbr-faithful-sim.md)

## Problem

Wv2 Mode C Plan B stocks when LEAP/standard_call is untradeable. WUT LEAP PBRs historically **skip** (refuse) when `floor(shares/100)=0`. Do not assume the lab already Plan-B’s.

## Scope (only if operator opts in)

1. Decide: lab skip vs Plan B shares vs standard_call sim.  
2. If Plan B: Justification-shaped results_json; no Black–Scholes for live packaging truth (lab BS remains lab-only if used).

## Non-goals

- Silently changing historical PBR fingerprints  
- Copying Wv2 desk code into WUT

## Acceptance

- [ ] Operator lock on skip vs Plan B  
- [ ] One PBR fixture matching that lock
