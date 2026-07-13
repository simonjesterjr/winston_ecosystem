# Ticket: Enforce paper-first max_markets=4 and max_leverage=1× on export/import

**Status:** Proposed  
**Date:** 2026-07-13  

## Context

Operator policy (2026-07-13, paper-first partial decision):

| Policy | Value |
|--------|-------|
| Ops / paper `max_markets` | **Force 4** |
| Paper `max_leverage` | **Force 1×** |

Today this is **documentation-only** (business analysis §15 + paper-first ticket). Lab may still run uncapped / leverage 3 for science. Risk: paper imports land without the locked caps, so ops quietly diverges from policy.

Session: [`2026-07-13-1741-paper-first-cohort-partial.md`](../session-reports/2026-07-13-1741-paper-first-cohort-partial.md).

## Scope

1. Locate WUT trade-ready / portfolio export fields for capacity and leverage.  
2. Locate Wv2 import path for the same.  
3. Choose enforcement surface (prefer least surprise):
   - **A.** Export-time defaults + warnings when paper-intended exports omit caps  
   - **B.** Import-time validation / normalization for paper Execution Mode  
   - **C.** Both, with clear override/force for lab observation archives  
4. Document behavior in handoff business-context if contracts change.  
5. Do **not** block pure lab PBRs that intentionally use nil max_markets or leverage 3.

## Acceptance

- [ ] Paper-intended handoff path documents or applies `max_markets=4`  
- [ ] Paper-intended handoff path documents or applies `max_leverage=1` (or equivalent risk sizing)  
- [ ] Lab uncapped / 3× research still possible without fighting the gate  
- [ ] Spec or smoke covering reject/normalize behavior  
- [ ] Cross-link from paper-first ticket when Done  

## Related

- Policy: `2026-07-13-paper-first-cohort-decision.md`  
- BA §15: `business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`  
- Level 2 K-path (calibration): `2026-07-13-pbr-level2-remaining-experiments.md`  
- Handoff: `docs/business-context/wut-to-wv2-handoff.md`  
