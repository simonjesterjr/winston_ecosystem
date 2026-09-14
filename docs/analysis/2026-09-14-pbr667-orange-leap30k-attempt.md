# PBR #667 — Orange RST LEAP $30k attempt

**Banner:** report only — no pack promotion.  
**Date:** 2026-09-14  
**cell_key:** `orange_rst_turtle_r01_leap30k`  
**Experiment:** `strategy77_rst_parity_v1`  
**Do not confuse with #666** (hybrid share, failed LEAP intent).

## Stamp (accepted)
- Orange × TS#77 × $30k × `resting_stop_touch` × turtle heat × risk 1%
- `leap_fulfillment=all`, `leap_atr_offset=0`, `leap_expiration_days=730`
- Parent window from #650: 2021-05-10 → 2026-09-11
- `results_parsed` carries leap knobs + turtle heat hash

## Execute
- Status: **failed** (`NoMethodError: undefined method 'date' for nil`)
- Before crash, logs showed **LEAP CALL entries with premiums** (GLTR / XLF / FPA) and RST parks — partial acceptance of LEAP tape.
- Likely crash: `LeapExitService` uses `position.activity.date` while LEAP positions often have nil `activity` and use `bar_date` / `entry_date`.

## Acceptance (not yet)
| Check | #667 |
|-------|------|
| Option premiums on tape | Started (then failed) |
| LEAP log lines | Yes (partial day) |
| RST fills | Yes (parks + LEAP fills) |
| Turtle heat stamped | Yes |
| No raw 20d under-max closes | Not evaluated (run died early) |

## Next
LeapExitService now uses `position.entry_date` (`bar_date || activity&.date`) and skips holding-days when that date is missing. Re-execute #667 (or a new cell if the failed row cannot be reset to pending).
