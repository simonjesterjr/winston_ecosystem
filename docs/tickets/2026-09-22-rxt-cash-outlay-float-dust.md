# Ticket: Repair stored option cash_outlay float dust

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-22  
**Lane:** B (stored-number cleanup; short System One harness)  
**Implementer:** Grok CLI  
**Origin:** Wrap of [`../session-reports/2026-09-22-1502-dar-option-field-projection.md`](../session-reports/2026-09-22-1502-dar-option-field-projection.md) §14. The DAR projection copies `fulfillment_details["cash_outlay"]` and does not round it.  
**DoD:** New option stamps store an exact decimal cash outlay. Existing rows whose dusty `cash_outlay` is within one cent of `abs(flow)` are rewritten to that exact amount. Rows that disagree by more than one cent are listed and left unchanged. Journal `flow` is not edited.

## Problem

`Operations::FulfillmentPackagingSelector#call_stamp` sets `cash_outlay` with binary float math: `premium * contracts * multiplier`. Premium 2.3 × 8 × 100 is stored as `1839.9999999999998`. The journal `flow` column is decimal and already holds the clean cash (`-1840.0`).

The Daily Analysis Report (DAR) now copies that stored number onto the payload, so a narrator can quote the dust.

## Specimens (Wv2 paper, 2026-09-22)

| Journal | Symbol | Units | Flow | Stored cash_outlay | Within 1¢ of abs(flow)? |
|---------|--------|-------|------|--------------------|-------------------------|
| 1914 | RXT | 8 | -1840.0 | 1839.9999999999998 | yes |
| 1916 | RXT | 4 | -920.0 | 919.9999999999999 | yes |
| 1940 | RXT | 7 | -1610.0 | 1609.9999999999998 | yes |
| 1942 | RXT | 4 | -920.0 | 919.9999999999999 | yes |
| 1981 | RXT | 4 | -920.0 | 919.9999999999999 | yes |
| 1977 | RXT | 9 | -2070.0 | 1839.9999999999998 | no — stale 8-lot dust on a 9-lot fill |

Journal 1977 must not be rounded to 1840.

## Scope

1. Stamp `cash_outlay` with decimal arithmetic (BigDecimal or integer cents), not Float.
2. One-time rewrite of stored `cash_outlay` only when it is within $0.01 of `abs(flow)`. Write the exact decimal, the same magnitude as `flow`.
3. Print journals that disagree by more than one cent. Do not change them in this ticket.

## Non-goals

- Editing `flow`, units, premium, or confirm
- Recomputing Edge (R)
- Changing `DarOptionFields` to round or reprice
- Narrator skills
- Interactive Brokers orders

## System One harness

**State:** the specimen table above, plus the same journals after the rewrite (cash_outlay, flow, units).

**Checkpoints:**

| id | type | instructions | pass rule |
|----|------|--------------|-----------|
| dust_cleared | Noul | Journals 1914, 1916, 1940, 1942, and 1981 still show a cash_outlay that is not an exact dollar amount | noul ≥ 0.85 → FAIL |
| flow_untouched | Noul | Any specimen journal flow changed | noul ≥ 0.85 → FAIL |
| stale_left | Noul | Journal 1977 cash_outlay was rewritten to 1840 or to 2070 | noul ≥ 0.85 → FAIL |

**Runner:** spec or rails read of the six journals first; then `jev ask` on the before/after table.  
**On fail:** do not mark Done.

## Work items

- [ ] Spec: 2.3 × 8 × 100 stamps 1840, not 1839.9999999999998
- [ ] Stamp path uses decimal math
- [ ] Rewrite only the within-1¢ rows; list 1977 and leave it
- [ ] Jev on the before/after table
