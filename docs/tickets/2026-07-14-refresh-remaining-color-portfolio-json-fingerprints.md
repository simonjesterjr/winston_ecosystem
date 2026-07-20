# Ticket: Refresh remaining color portfolio_configs with fingerprints

**Status:** Proposed  
**Priority:** unset
**Date:** 2026-07-14  
**Source:** Phase 3 PR 4 partially completed blue-pbr62 + red; other cohort JSONs incomplete  
**Plan:** `plans/paper-telegram-phase3-adr006.md` PR 4 follow-on

## Problem

PR 4 refreshed **blue-pbr62** and **red** with fingerprints. Other color handoff files still missing or uneven (e.g. static `portfolio-blue.json`, some sidecars). Bare-name import remains a footgun for any file without fingerprint.

Inventory at PR 4 close (approx): green/orange/pink/mango (was blank)/rust/white already had nested fingerprints; blue static and some others did not.

## Scope

1. Inventory all `portfolio_configs/portfolio-*.json` for `fingerprint` / `wut_trading_strategy_id`.  
2. Re-export via `wut:portfolios:export_config` (capture if needed) for any validation PBR still lacking fingerprint.  
3. Prefer bare `seed_name` + fingerprint; keep human notes in `description`.  
4. Do **not** re-import over engaged OPs without lineage smoke.  
5. Cross-link host tracking ticket if files stay outside git.  

## Acceptance

- [ ] Primary color cohort JSONs used for ops handoff all carry fingerprint when a lab TS exists  
- [ ] Document any intentional legacy files  
- [ ] Optional: one-shot rake/script listing missing fingerprints  

## Related

- `2026-07-09-refresh-portfolio-exports-with-ts-fingerprint.md` (Done for blue-pbr62/red path)  
- `2026-07-14-workspace-compose-portfolio-configs-tracking.md`  
- WUT export: `PAPER_CAPS=1` optional  
