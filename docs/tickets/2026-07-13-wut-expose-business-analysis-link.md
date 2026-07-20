# Ticket: Expose ecosystem business analysis from WUT UI

**Status:** Proposed  
**Priority:** P3
**Date:** 2026-07-13  
**Monolith:** winston_unit_test (WUT)

## Context

Business-level evaluations (PBR rankings, paper-first candidates, experiment economics) live in **`ecosystem/business_analysis/`**. Operators currently only find them via git. Lab work happens in WUT; the library should be one click away.

Canonical first doc: `ecosystem/business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`  
Index: `ecosystem/business_analysis/README.md`

## Problem

No WUT navigation surface for business analysis → promotion decisions stay buried in repo paths.

## Scope

1. Add a **Business analysis** entry to WUT nav (home and/or portfolios / PBR index — pick the least noisy place; prefer global nav or home “lab docs” section).
2. Serve or link the markdown library:
   - **Preferred thin path:** static mount / read of `ecosystem/business_analysis/*.md` rendered as simple HTML (or raw MD download + index list), **or**
   - Link to a documented host path if ecosystem is already served (e.g. compose volume) — avoid duplicating content into WUT git.
3. Index page lists dated docs from the folder (filename + H1 title); detail page shows one doc.
4. Do **not** invent a second copy of the analysis in WUT DB.

## Acceptance

- [ ] Operator can open business analysis index from WUT without leaving the lab UI
- [ ] At least the 2026-07-13 PBR evaluation is reachable
- [ ] Filing guide in `ecosystem/docs/README.md` and `business_analysis/README.md` still authoritative
- [ ] No secrets / full repo tree exposed beyond `business_analysis/`

## Related

- Session: `docs/session-reports/2026-07-13-1713-pbr-business-analysis-wrap.md`
- Source content: `business_analysis/2026-07-13-pbr-return-dd-pcs-evaluation.md`
