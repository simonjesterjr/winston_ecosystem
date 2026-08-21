# Ticket: Automate Quiver Strategies PDF grab / scrape (future)

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-08-21  
**Monoliths:** DM-adjacent worker (preferred); not Wv2  
**Blocked on:** tracking desk PDF ingest green  
**See:** plan [`quiver-pdf-bot-and-scrape.md`](../../plans/quiver-pdf-bot-and-scrape.md)

## Problem

v1 ingest is HITL PDF download. Later we may log in to Quiver Quantitative and fetch the same PDF/table so the operator does not.

## Scope (when unblocked)

- Secret store for **site** credentials (not `QUIVER_API_KEY`, not Wv2 env)
- Weekly job after Quiver rebalance; POST bytes into existing Wv2 ingest
- Fail closed → HITL task; never fall back to filing reconstruction as if it were the published book
- ToS / brittleness review in the plan before code

## Acceptance

- [ ] Tracking ingest contract reused
- [ ] Failure is HITL, not a fake book
- [ ] No Quiver site password in Wv2 or Telegram logs

## Non-goals

- v1 tracking desk
- Replacing DM Alt Filings
