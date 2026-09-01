# Ticket: After WQ setup — reset IBKR paper DUT and bind paper Mint

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-01  
**Mode:** contractor  
**Graph nodes:** winston_v2, broker_gateway  
**Human gates:** WQ paper setup done first; CPGW paper SSO; **Slate Automation** is an explicit OP+fingerprint flag, not implied by this bind  
**DoD:** DUT is a clean paper book bound to a paper Trend Following OP (probably Mint); WQ is not on this binding  
**Blocked on:** WQ paper hygiene ([`2026-09-01-wq-cost-basis-corrective-amend-dut.md`](2026-09-01-wq-cost-basis-corrective-amend-dut.md) and Phase 1 cadence)  
**Non-goal of:** [`2026-09-01-wq-ibkr-paper-evidence-bind.md`](2026-09-01-wq-ibkr-paper-evidence-bind.md) (explicitly not Mint)  
**Origin:** Grill 2026-09-01 Q9 — [`docs/session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md`](../session-reports/2026-09-01-1601-ibkr-paper-and-slate-grill.md)

## Problem

DUT070450 was used to rehearse WQ sizes. Operator intent: after WQ initial setup, **reset** Interactive Brokers paper and bind it to a paper Trend Following Operational Portfolio (probably Mint) for mechanical **Session Order Slate** *learning*. Discovery: policy Send is glossary-only until `order_write`; Accept-Fill is stops-only and not scheduled to widen.

## Scope

1. Flatten / reset DUT paper positions and cash to a known starting NLV.  
2. Unbind WQ #1372 from this CPGW session (WQ stays dummy_sim or a later Schwab evidence bind).  
3. Bind the chosen paper Mint OP + fingerprint; Capital Authority = Broker Account Capital.  
4. Confirm ≠ Send; `order_write` still false unless a write ADR exists.  
5. DAR for that OP can show Turtle priorities as **review** copy.

## Non-goals

- Turning Slate Automation on just because the bind exists  
- Whole-slate accept-fill  
- Live capital  
- Parking stop-market orders (L3)  

## Acceptance

- [ ] DUT flat (or documented seed)  
- [ ] WQ #1372 not on `bnd_*` DUT binding  
- [ ] Paper Mint (or named successor) bound; Risk Capital follows polled NLV  
- [ ] No policy Send until Slate Automation is explicitly flagged
