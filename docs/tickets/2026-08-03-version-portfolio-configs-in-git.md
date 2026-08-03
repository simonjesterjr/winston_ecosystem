# Ticket: Version primary portfolio_configs JSON in git

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-03  
**Scope:** ecosystem / workspace exchange  
**Session:** [`../session-reports/2026-08-03-1520-portfolio-preferred-color.md`](../session-reports/2026-08-03-1520-portfolio-preferred-color.md)  
**Related:** [`../business-context/wut-to-wv2-handoff.md`](../business-context/wut-to-wv2-handoff.md)

## Goal

Decide and implement durable versioning for primary handoff JSON under `portfolio_configs/` (e.g. `portfolio-green.json`), which today is a compose bind-mount exchange volume **outside** any majestic-monolith git repo.

## Why it came up

Session that added preferred `"color"` to primary configs updated files on disk only. There is no `portfolio_configs/.git` and no root monorepo git — changes are not reviewable or restorable via PR.

## Options (pick one)

1. **Track under `ecosystem/`** — e.g. `ecosystem/portfolio_configs/` or `ecosystem/fixtures/portfolio_configs/` as SoT; compose mount or copy script into runtime volume  
2. **Dedicated small git repo** at `portfolio_configs/`  
3. **Leave untracked** — document as operator-local exchange only; regenerate via WUT export rake  

## Acceptance

- [ ] Written decision (short note in handoff README or ticket outcome)
- [ ] If tracked: primary color-cohort JSONs (not every sidecar/pbr log) in chosen repo; ignore `*-vet.log` / `*-build.log` / huge sidecars as appropriate
- [ ] Compose / operator path still lands files where WUT/Wv2 expect `/portfolio_configs`

## Out of scope

- Auto-commit on every export
- Tracking all historical PBR exports
