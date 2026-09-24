# Shares-only TS75 modified-heat bakeoff — stamp note

- **Ticket:** [`../tickets/2026-09-24-shares-ts75-modified-heat-bakeoff.md`](../tickets/2026-09-24-shares-ts75-modified-heat-bakeoff.md)
- **Script:** [`2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb`](2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb)
- **Experiment:** `shares_ts75_mod_heat_bakeoff_20260924`
- **Cells:** 8 (Blue/Indigo/Teal/Copper × r01/r02) — TS75 only, shares-only, caps 3/10
- **Heat:** ALWAYS full hash + `heat_mode=turtle` — knobs **3 / 6 / 10 / 10** (market / close / loose / direction); `unit_risk_fraction` = risk
- **LEAP:** omit `leap_fulfillment` (IBKR Level 1)
- **Baseline control:** heat-absent shares bakeoff PBRs **772–787** (TS75 won Edge_R)
- **Do not stamp from CoS chat** — PBR Ops dry-run then live. Live stamp overwrites this note with the PBR table.

## Dry-run (Ops)

```bash
cd /home/johnkoisch/Documents/com/sawtooth
DRY_RUN=1 ./bin/compose exec -T -e DRY_RUN=1 winston_unit_test bin/rails runner \
  /ecosystem/docs/analysis/2026-09-24-stamp-shares-ts75-modified-heat-bakeoff.rb
```
