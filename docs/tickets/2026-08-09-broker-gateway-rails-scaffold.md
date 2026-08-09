# Ticket: Broker Gateway — Rails monolith scaffold

**Status:** Ready  
**Priority:** P1  
**Date:** 2026-08-09  
**Series:** `trade-fulfillment-engine`  
**Domain:** Broker Gateway, Majestic Monolith  
**Glossary:** Broker Gateway, Majestic Monolith  
**Monoliths:** **`broker_gateway`** (new repo / directory under workspace when built)  
**Plan:** [`plans/trade-fulfillment-engine.md`](../../plans/trade-fulfillment-engine.md) H22 / Grill B Q3  
**Epic:** [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)

## Problem

Phase 1 H22 + Grill B Q3 locked a new majestic monolith **`broker_gateway`**. It does not exist yet. L1 transport, evidence store, and secrets isolation cannot land without a Rails app, AGENTS.md, Containerfile, compose service, and health surface.

## Scope

1. Scaffold **Ruby on Rails** app named **`broker_gateway`** (API-first; minimal ops UI later is OK as stub routes).  
2. **`AGENTS.md`** for the monolith (role: transport + Winston Broker Evidence Standard; **not** journals/capital/Desk Confirm).  
3. **Containerfile** + integration into workspace **`bin/compose`** / root compose as service **`broker_gateway`**.  
4. **Host port:** suggest **3003** (DM 3001, WUT 3000, Wv2 3002).  
5. **Postgres:** dedicated DB (or shared-Postgres multi-DB pattern like DM) — **not** shared tables with Wv2.  
6. **Sidekiq** stub (queues ready for poll/refresh jobs).  
7. **Health** endpoint (compose/smoke can hit it).  
8. Secrets layout: env / volume pattern isolating broker OAuth from Wv2 process.  
9. Update workspace monorepo map / AGENTS.md table when scaffold lands (workspace root + ecosystem notes as needed).

## Non-goals

- Schwab OAuth product code  
- Evidence JSONL writer (follow-on ticket)  
- Full ops UI polish  
- `place_order` / any `order_write`  
- Implementing Confirmation Intake match in BG  

## Domain locks

- L1 only: scaffold must not expose write-order APIs  
- Human Confirm stays in Wv2  
- Ruby/Rails primary language  
- Manual fulfillment remains zero-IO inside Wv2 (no requirement that Manual live in BG)

## Acceptance

- [ ] Rails app boots in compose  
- [ ] Service reachable on host **3003** (or documented alternate if conflict)  
- [ ] Health endpoint green under compose smoke  
- [ ] Sidekiq process stub starts  
- [ ] Postgres dedicated (or multi-DB) with migrations path  
- [ ] `AGENTS.md` states ownership boundaries (transport + evidence; no desk/capital)  
- [ ] Containerfile + compose wiring checked in  
- [ ] No `order_write` / place_order routes  

## Related

- Epic: [`2026-08-09-l1-confirmation-intake-bg-build.md`](2026-08-09-l1-confirmation-intake-bg-build.md)  
- Evidence store: [`2026-08-09-bg-evidence-store-jsonl-and-cursors.md`](2026-08-09-bg-evidence-store-jsonl-and-cursors.md)  
- Internal API: [`2026-08-09-bg-internal-api-refresh-events.md`](2026-08-09-bg-internal-api-refresh-events.md)  
