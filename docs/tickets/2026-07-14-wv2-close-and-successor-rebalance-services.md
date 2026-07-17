# Ticket: Wv2 Close + successor rebalance services

**Status:** Done  
**Date:** 2026-07-14  
**Completed:** 2026-07-17  
**Source:** Phase 3 ADR-006 minimum complete; schema columns landed, verbs deferred  
**Plan:** `plans/paper-telegram-phase3-adr006.md` (out of minimum)

## Problem

ADR-006 defines **Close** (paper soft-close vs real flat-required) and **shape Rebalance** (successor A′). Phase 3 PR 1 added `closed_at` and `successor_of_id` but no domain services, rake, internal API, or MCP tools. Operators cannot formally end an engaged series or open a successor without console surgery.

## Scope

1. `Operations::PortfolioCloseService` — paper soft-close; real flat-required (optional force soft-close with residue).  
2. `Operations::PortfolioSuccessorService` — close/end signals on A; open A′ with new Books/TS; link `successor_of_id`; journals stay on A.  
3. Wire rake + internal API + MCP + ops shell.  
4. Specs: paper soft-close, real refuse with open position, successor preserves journals on A.  
5. Daily analysis skips closed series (`open_for_signals?` / `open_series` + readiness `:closed`).  

## Acceptance

- [x] Engaged paper OP can soft-close; no new signals  
- [x] Real close blocked when open positions unless force  
- [x] Successor creates new OP linked to A; A closed or signal-ended  
- [x] Docs in `wv2-operational-portfolio-lifecycle.md` stay accurate  

## Delivered

| Surface | Path |
|---------|------|
| Close service | `winston_v2/app/services/operations/portfolio_close_service.rb` |
| Successor service | `winston_v2/app/services/operations/portfolio_successor_service.rb` |
| Internal API | `POST /internal/portfolios/close`, `POST /internal/portfolios/successor` |
| Rake | `wv2:portfolios:close[id]`, `wv2:portfolios:successor[id]` (+ ENV) |
| Ops shell | `close_portfolio`, `successor` |
| MCP | `wv2_close_portfolio`, `wv2_successor_portfolio` |
| DA skip | `PortfolioReadiness` `:closed`; runner uses `Portfolio.active.open_series` |
| Specs | `portfolio_close_service_spec.rb`, `portfolio_successor_service_spec.rb` |

## Related

- ADR-006; lifecycle business-context  
- Schema: `2026-07-09-wv2-op-lifecycle-schema.md` (Done)  
- Capital Activation: `2026-07-09-capital-activation-mcp-telegram.md` (still open)
