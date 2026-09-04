# Ticket: P4 — Compounding: champion freeze and sit-vs-kill

**Status:** Proposed  
**Priority:** P2 — lineage already holds; this is the missing operator protocol  
**Date:** 2026-09-04  
**Monolith:** cross (WUT scorecards, Wv2 MMS / lifecycle, Cromwell skills)  
**Principle:** Hamming / Munger / Buffett  
**Page:** `winston_foundations/20260904/04-the-compounding-problem.md`  
**Parent:** [`2026-09-04-tf-foundations-competency-epic.md`](2026-09-04-tf-foundations-competency-epic.md)

## Problem

ADR-006 already protects compounding **integrity** (Engaged freeze, successor, Capital Activation never consumes paper terminal equity). What is missing is compounding **protocol**:

- No written rule for “this fingerprint is in a 40% Trend Following drawdown; **sit**.”  
- Bake-off churn has a cultural brake (anti-joint-regrid) but not a productized champion freeze.  
- Mid-month Scoreboard (MMS) grades **process**, not Compound Annual Growth Rate (CAGR). CAGR/Calmar ticket still Proposed.  
- Process miss moves the paper equity path, so edge decay and “we didn’t confirm” are confusable.  
- Capital Activation **soft-warns** observation provenance — a human can start compounding the wrong series.  
- Loop-engineering: skills document ops, not lessons after a losing paper series.

## Desired outcome

1. **Champion freeze + kill rule** (doctrine, then light machinery): pre-register per fingerprint “sit through drawdown ≤ X” vs “close / successor when rolling 12-month expectancy CI includes 0” (CI depends on P1 harness). Successor only — never mutate Engaged.  
2. **CAGR and Calmar** on lab scorecards and MMS (finish existing ticket; this ticket owns the *protocol* that uses those numbers).  
3. **Closed auto-paper twin** vs human-gated path so process miss is not mistaken for edge decay — loop-engineering V1–V2, **before** Evolution Mode.  
4. Holdout / walk-forward **required** before real Capital Activation (harder than today’s soft warn). Depends on P1.  
5. Bounded per-campaign STATE after a losing paper series (what fired, what we passed, what we learned).

## Must preserve

- ADR-006 engagement lock and successor path  
- Paper as regime heuristic, not household P&L  
- MMS “do not promote on this sample” copy  
- Observation vs Trade-Ready as passport, not trophy  

## Out of scope

- Evolution Mode search loops (existing loop-engineering ticket; after V1–V2)  
- Quiver in-place membership vs successor (existing grill ticket)  

## Acceptance

- [ ] Written sit-vs-kill doctrine in business-context or an ADR addendum to ADR-006  
- [ ] CAGR/Calmar ticket Done or explicitly merged here  
- [ ] Capital Activation of non-trade-ready provenance is either hard-block or a recorded operator override (not a buried warn)  
- [ ] One paper-loss campaign has a STATE artifact (even if manual markdown) as the template  

## Related existing work

- ADR-006  
- `docs/tickets/2026-07-26-bakeoff-scorecard-cagr-calmar.md`  
- `docs/tickets/2026-07-19-loop-engineering-evolution-mode.md`  
- `business_analysis/2026-07-30-berlekamp-simons-winston-lessons.md` (cut losers vs wait)  
- `ecosystem/ai/skills/winston-mms/SKILL.md`
