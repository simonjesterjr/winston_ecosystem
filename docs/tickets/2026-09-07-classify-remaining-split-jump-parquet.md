# Ticket: Classify remaining split-like parquet jumps (do not universe-APPLY)

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-09-07  
**Mode:** normal  
**Graph nodes:** data_manager  
**Human gates:** no universe `APPLY=1` without a per-symbol review  
**DoD:** Each of the 271 remaining 1.8-detector hits is split / reverse-split / false-positive; Active books stay clean; penny 2× series not blind-stitched  
**Origin:** [`docs/session-reports/2026-09-07-1957-corporate-action-hold-refuse.md`](../session-reports/2026-09-07-1957-corporate-action-hold-refuse.md)  
**Parent:** [`2026-08-22-corporate-action-stop-safeguards.md`](2026-08-22-corporate-action-stop-safeguards.md); issue [`docs/issues/2026-08-22-unadjusted-reverse-split-jumps.md`](../issues/2026-08-22-unadjusted-reverse-split-jumps.md)

## Problem

`data:scan_split_jumps` on 2026-09-07: **271 of 2716** parquet files still trip `open/prev_close` ≥ 1.8 or ≤ 1/1.8. **None** of the 81 Active Operational Portfolio (OP) book names jump (including USO, XOP, OIH, UNG, WEAT, AMCR, APLD).

The detector is load-bearing for reverse-split stitch, but it also flags ordinary 2-for-1s, leveraged-ETF reverse splits (BOIL), mega-cap splits (AVGO, CMG), and penny 2× noise. Universe-APPLY was rejected on 2026-08-22 because Applied Digital (APLD) flipped 2× many times.

`ParquetStandardizer` now auto-stitches on acquire, so a full rewrite of a name will stitch it. That is not a classified backlog.

## Scope

1. Dump the 271 hits (symbol, date, ratio, inferred factor).  
2. Bucket: official split / reverse-split; leveraged/vol product reset; penny noise; unknown.  
3. APPLY only named official reverse-splits that still jump **and** sit on lab or future-demand books.  
4. Spec or note: do not `scan_all` → `apply!` the universe.

## Non-goals

- Blind `APPLY=1` on all 271  
- Broker Gateway write hold (parent P0, L3)  
- Changing the 1.8 ratio in this ticket  

## Acceptance

- [ ] Hit list filed (session appendix or this ticket)  
- [ ] Buckets assigned; penny 2× left unstitched  
- [ ] Any APPLY is per-symbol with `*.pre_split_adjust` backup  
- [ ] Re-scan: Active OP books still 0 jumps  
