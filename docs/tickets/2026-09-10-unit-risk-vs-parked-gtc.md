# Ticket: Remaining unit risk vs parked GTC when the row stop differs

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-10  
**Monolith:** winston_v2  
**Mode:** contractor  
**Graph nodes:** winston_v2  
**See:** session [`winston_v2/docs/session-reports/2026-09-10-1532-walnut-unit-risk-inspect-layout.md`](../../../winston_v2/docs/session-reports/2026-09-10-1532-walnut-unit-risk-inspect-layout.md)

---

## Problem

Open-lot **Unit risk** is dollars from the mark to the **stop in that row** (`updated_stop` || `original_stop`). On Walnut #1428 that is honest for DBC (shared trailed 32.56). It is misleading for DD and SCHZ:

| Name | Row stop | Mark | Unit risk shown | Parked GTC |
|------|----------|------|-----------------|------------|
| DD short | 127.75 | 127.92 | **$0** (through the row stop) | BUY 36 @ **133.88** |
| SCHZ short | 22.56 | 22.61 | **$0** | BUY 914 @ **22.76** |

The operator can read $0 as “no dollars left to the protective” while a Good-Til-Cancelled (GTC) 2N is still parked farther out.

## Scope

- When a parked GTC working stop exists for the lot (Session Order Slate protective / DUT oid), remaining unit risk should use **that** stop, or show both (row vs GTC) without a second mystery number.
- Keep $0 + red when the **protective** is through the mark (true naked / should-have-filled).
- Tooltip still shows original-at-entry.

## Acceptance

- [ ] Walnut DD/SCHZ remaining is ~1% original vs GTC 133.88 / 22.76, not $0, while those GTCs are parked
- [ ] DBC (row stop = GTC 32.56) unchanged (~$81)
- [ ] Spec: fixture with row stop through mark and a farther parked GTC
- [ ] Caption still says “working stop”; if GTC wins, the row Stop column should not silently disagree (either match or annotate)

## Out of scope

- Changing DUT orders or PositionSizer
- Enforcing `max_leverage` (P3 Capital Authority ticket)

## Origin

Wrap follow-up item 1 from session `2026-09-10-1532-walnut-unit-risk-inspect-layout.md`.
