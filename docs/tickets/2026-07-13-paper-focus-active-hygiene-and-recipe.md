# Ticket: After paper cohort choice — Active hygiene + recipe check / Blue 62 import

**Status:** Proposed  
**Date:** 2026-07-13  
**Blocked by:** cohort choice on `2026-07-13-paper-first-cohort-decision.md`  

## Context

Session [`2026-07-13-1741-paper-first-cohort-partial.md`](../session-reports/2026-07-13-1741-paper-first-cohort-partial.md). Paper-first **policies** are locked (max_markets=4, paper leverage 1×); **seed** still deferred. Six color Actives remain in Wv2. Live **Portfolio Blue** is static + isomorphic — not PBR 62.

## Scope

After operator records first paper seed (Green 55 / Blue 62 / dual):

1. **Attention hygiene** — primary paper focus Active; demote non-focus color Actives unless force dual (ADR-006 mutex spirit).  
2. **Recipe check** — OP/TS matches lab PBR for chosen path; ops caps document `max_markets=4` and paper leverage **1×**.  
3. **If Blue 62** — do not engage current static isomorphic Blue as if it were 62; WUT export C0 recipe → Wv2 import/auto-fork → Active + paper.  
4. **If Green 55** — confirm Breakout55 / VolExit / static / move_to_last still matches; adjust only if drift.  
5. Cross-link completion back to paper-first ticket remaining checklist.

## Acceptance

- [ ] Cohort choice recorded on paper-first ticket + BA §15  
- [ ] Active set matches attention policy for chosen focus  
- [ ] Focus OP TS matches intended lab recipe under locked policies  
- [ ] Blue 62 path uses new import lineage if Blue chosen (not rename of static Blue)

## Related

- Parent decision: `2026-07-13-paper-first-cohort-decision.md`  
- BA: `business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md` §15  
- Lifecycle: ADR-006 / `docs/business-context/wv2-operational-portfolio-lifecycle.md`  
- First journal: `2026-07-13-confirm-first-paper-journal-focus-cohort.md`  
