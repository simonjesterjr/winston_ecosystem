# Ticket: Document first-time Broker Gateway compose bring-up

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-12  
**Series:** `trade-fulfillment-engine`  
**Domain:** Broker Gateway, compose, ops  
**Monoliths:** **broker_gateway**; ecosystem deploy/hints  
**Origin:** Session report [`docs/session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md`](../session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md)

## Problem

Operators expected BG to appear in `c ps` like `data_manager`. Compose defines `bg_postgres`, `broker_gateway`, `broker_gateway_sidekiq`, but a long-running stack started **before** BG was added only had `bg_postgres` (or nothing). First-time / catch-up steps lived only in session notes and AGENTS snippets.

## Scope

1. Ecosystem hint or deploy note: first-time BG trio up + `db:prepare` + seed.  
2. Smoke curls: health, adapters, bindings, refresh, events.  
3. Note Redis DB **/3** isolation and host port **:3003**.  
4. Cross-link from `broker_gateway/AGENTS.md` (already has partial smoke — keep DRY).

## Non-goals

- Changing compose default profiles  
- Auto-migrate on container start (optional later)

## Acceptance

- [ ] Operator can bring BG from zero using only ecosystem/BG docs  
- [ ] Mentions that existing stacks need explicit `up -d` for BG services  
- [ ] Linked from L1 epic or AGENTS  

## Related

- Epic: [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
- Session: [`../session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md`](../session-reports/2026-08-12-1152-bg-registry-dummy-sim-compose.md)  
