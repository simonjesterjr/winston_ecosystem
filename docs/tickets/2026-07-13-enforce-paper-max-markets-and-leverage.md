# Ticket: Enforce paper-first max_markets=4 and max_leverage=1× on export/import

**Status:** Done (2026-07-14 Phase 3 PR 4)

**Date:** 2026-07-13  

**Plan:** [`plans/paper-telegram-phase3-adr006.md`](../../plans/paper-telegram-phase3-adr006.md) PR 4.

## Context

| Policy | Value |
|--------|-------|
| Ops / paper `max_markets` | **Force 4** |
| Paper `max_leverage` | **Force 1×** |

## Scope

1. Export-time optional force (`PAPER_CAPS=1`)  
2. Import-time normalize for paper path  
3. Lab override `force_lab_uncapped`  
4. Specs  

## Acceptance

- [x] Paper-intended export can apply 4 / 1× (`PAPER_CAPS=1`)  
- [x] Import normalizes to 4 / 1× by default  
- [x] Lab uncapped via `force_lab_uncapped: true`  
- [x] Specs in `portfolio_config_importer_spec`  
- [x] Handoff business-context documents behavior  

## Delivered

- `Operations::PortfolioConfigImporter#apply_paper_caps!`  
- WUT export `PAPER_CAPS=1`  
- blue-pbr62 exported with paper policy  

## Related

- Policy: `2026-07-13-paper-first-cohort-decision.md`  
- Handoff: `docs/business-context/wut-to-wv2-handoff.md`  
