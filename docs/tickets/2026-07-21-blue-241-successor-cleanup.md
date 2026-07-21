# Ticket: Decide fate of Blue successor OP #241

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-07-21  
**Domain:** ADR-006 lifecycle, ops hygiene  
**Glossary:** Operational Portfolio, Successor, Active, Closed

## Problem

After WUT run 80 transfer, Cromwell freelanced `wv2_successor_portfolio` and created **#241** “Portfolio Blue · 9cf64e64” ($20k, successor of closed **#7**). The true transfer product is **#240** (same display name, $10k, Active paper as of 2026-07-21 recovery). Two OPs share the same human label → Telegram/ops ambiguity.

## Scope

1. Operator decision: close #241, keep inactive archive, or switch Active to #241 ($20k series).  
2. If close: paper soft-close path; confirm journals stay on #7.  
3. Optional: rename one OP for disambiguation if both kept.

## Non-goals

- Changing fingerprint identity of PBR80 methodology  
- Re-importing WUT run 80  

## Acceptance

- [ ] Single preferred Blue PBR80 attention OP documented  
- [ ] #241 either Closed or clearly labeled inactive archive  
- [ ] Active band has at most one intentional Blue paper OP  

## Related

- Session: `docs/session-reports/2026-07-21-0927-wut80-transfer-activate-recovery.md`  
- Sibling: `2026-07-21-cromwell-activate-id-or-name.md` (root cause of failed activate)  
- Sibling: `2026-07-21-portfolio-id-or-name-fingerprint-resolution.md`  
- ADR-006 operational portfolio lineage  
