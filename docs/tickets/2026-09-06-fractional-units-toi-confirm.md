# Ticket: Fractional units dropped by `to_i` on confirm / sizer

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-09-06  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**Edges:** WQ fractional lots (BRK-B, MSFT, NVDA); `JournalConfirmationService#resolved_units`  
**Human gates:** none once a failing spec exists  
**DoD:** confirm of a tracking/copy lot with units below 1 books the decimal size; regression spec; `plan_approve` / live snapshot no longer show 0 for sub-share names  
**Series:** `production-ready-wq`  
**Plan:** [`plans/production-ready-wq.md`](../../plans/production-ready-wq.md)  
**Origin:** [`docs/session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md`](../session-reports/2026-09-06-1907-adr-013-wq-confirm-send.md)

## Problem

WQ lots are fractional (IBKR size step 0.0001). `JournalConfirmationService#resolved_units` still uses `@units.to_i` / `details["units"].to_i` on the non-copy path. Copy/tracking confirm has a `first_positive_copy_units` branch, but `plan_approve_spec` confirm/blow-away/flatten failed with open lots empty, and `PortfolioLiveSnapshot` previously used `units.to_i` (MSFT/NVDA showed 0). Snapshot was patched to `to_d`/`to_f`; confirm `to_i` was **not** fully retired.

A DUT Accept-Fill that passes fractional `units:` into confirmation can still collapse to 0 on some branches.

## Scope

1. Failing spec: confirm `drop_book` / `add_book` / reweight with units `0.41` and `2.8632`.  
2. Replace remaining `to_i` size reads on tracking/WQ and any IBKR-paper fill bind with decimal coerce.  
3. Re-run `plan_approve_spec` cells that expected open lots.

## Non-goals

- Changing TF integer sizing for Mint Daily Analysis (ATR integer lots stay integer unless a separate ticket).  
- DUT send.

## Acceptance

- [ ] Spec: fractional confirm does not book 0  
- [ ] `resolved_units` / `fill_units` keep four-decimal IBKR sizes  
- [ ] `plan_approve` flatten/confirm cells green or classified  
