# Ticket: S4 pack OPs — set max_markets_per_portfolio to book size

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-26  
**Monolith:** winston_v2 (ops patch); optional WUT export follow-up  
**Related:** transfer `2026-07-26-s4-recipe-transfer-mint-yellow-blue.md`; ops panel Strategy audit shows `max_markets=` blank  

---

## Problem

After S4 FastBO5 Phase 2 pack transfer, Winston v2 (Wv2) Operational Portfolios (OPs) land with:

| Field | Value | Role |
|-------|--------|------|
| `max_positions_per_portfolio` | **12** | Concurrent **lot heat** (lab freeze) — correct |
| `max_positions_per_symbol` | **4** | Per-name / pyramid depth — correct |
| **`max_markets_per_portfolio`** | **`null`** | Membership cap — blank on ops audit |

Ops panel shows `max_markets=` empty. Operators reasonably confuse that with the freeze of **12** (which is **lots**, not markets). Null is intentional under `force_lab_uncapped` (full exclusive books), but a numeric value equal to **current book size** is clearer for audits and does not change membership or heat.

## Scope

Patch the three transferred S4 pack OPs so `max_markets_per_portfolio` equals the **book market count** at transfer:

| OP | Seed | Markets (Books) | Set `max_markets_per_portfolio` |
|----|------|-----------------|--------------------------------|
| **#381** | Portfolio Blue · f4dd31eb | **11** | **11** |
| **#382** | Portfolio Mint · 91608a22 | **10** | **10** |
| **#383** | Portfolio Yellow · 2a97a043 | **17** | **17** |

Verify after patch: ops Strategy audit shows numeric `max_markets`; lot heat remains 12; books unchanged.

### Optional follow-ups (same ticket or split)

1. **Export hygiene:** WUT `PortfolioConfigExporter` / S4 export JSON set `max_markets_per_portfolio` to `markets.size` when `force_lab_uncapped` (so future imports don’t re-blank).  
2. **Ops audit UX:** print both lines, e.g. `max_port_lots=12 · max_sym=4 · max_markets=10 (book)` so heat vs membership are not conflated.

## Not in scope

- Changing `max_positions_per_portfolio` (stays **12**)  
- Paper-capping to 4 markets (`PAPER_CAPS`)  
- Forcing `max_markets=12` for all three (would **truncate Yellow** from 17 → 12)

## Acceptance

- [ ] OP #381 / #382 / #383 have `max_markets_per_portfolio` = 11 / 10 / 17  
- [ ] Book membership counts unchanged  
- [ ] `max_positions_per_portfolio` still 12; `max_positions_per_symbol` still 4  
- [ ] Ops audit (or `inspect_strategy`) shows non-null max markets  
- [ ] Optional: export path no longer leaves max_markets blank for uncapped S4 packs  

## Implementation sketch

```ruby
# Wv2 rails runner
{
  381 => 11, # or Portfolio.find(id).markets.count
  382 => 10,
  383 => 17
}.each do |id, n|
  p = Portfolio.find(id)
  n = p.markets.count  # preferred: live book size
  p.update!(max_markets_per_portfolio: n)
end
```

Prefer **live `markets.count`** over hardcoding if Books may have drifted.

## Notes

- **Heat freeze = 12 lots** (`max_positions_per_portfolio`), not max markets.  
- Setting max markets to book size is a **display / membership ceiling** equal to current membership — no symbols added or removed.
