# Ticket: Mode D phase 2 — portfolio list tells Grok Bot the fulfillment mode

**Status:** Done
**Priority:** P1
**Date:** 2026-09-24
**Lane:** B
**Parent:** [Mode D phase 2](../2026-09-24-mode-d-phase-2.md)
**Implementer:** Grok CLI
**DoD:** `GET /internal/portfolios` includes `fulfillment_mode` for every portfolio. A Mode D book reads `mode_d`. A current Mode C book still reads `mode_c`. Grok Bot’s `wv2_list_portfolios` shows that field without a new tool.
**Origin:** [session report](../../session-reports/2026-09-24-1227-mode-d-phase-0-1.md)

## Goal

Mode D is stored as `fulfillment_packaging_policy["fulfillment_mode"]`. `Portfolio#fulfillment_mode` already derives `stock`, `mode_c`, or `mode_d`. The list used by Grok Bot does not return it. Today that payload is id, name, active, markets, and capital base (`InternalController#portfolios`).

This slice is part of Phase 2 so the bot can see the book the desk walk is using. It does not turn any existing paper book into Mode D.

## Work items

- [x] Add `fulfillment_mode` to the `/internal/portfolios` JSON
- [x] Spec: blank policy + `leap_fulfillment=all` → `mode_c`; blank + `none` → `stock`; explicit `mode_d` → `mode_d`
- [x] Do not add a database column

Landed 2026-09-24. Live `GET /internal/portfolios` includes the field on all 53 books. #1585 reads `mode_d`. #1581 reads `mode_c`. Walnut #1428 reads `stock`. No new column. `wv2_list_portfolios` already returns this payload unchanged.

## System One harness

**State:** one row each for stock, mode_c, and mode_d from the list payload.

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| mode_omitted | Noul | Is `fulfillment_mode` missing from any listed portfolio? | noul ≥ 0.85 → FAIL |
| mode_c_kept | Noul | Did a `leap_fulfillment=all` book get labeled `mode_d`? | noul ≥ 0.85 → FAIL |

**Runner:** request spec first; `jev ask` only if the payload shape is in dispute.
**On fail:** do not tell the operator the bot can see Mode D.

## Non-goals

- Daily Analysis Report packaging copy (separate from this list)
- Setting Mode D on Blue, Mango, Orange, or Indigo
