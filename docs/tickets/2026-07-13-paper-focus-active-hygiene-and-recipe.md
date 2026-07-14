# Ticket: After paper cohort choice — Active hygiene + recipe check / Blue 62 import

**Status:** Done (2026-07-14 Phase 1)  
**Date:** 2026-07-13  
**Unblocked by:** `2026-07-13-paper-first-cohort-decision.md` (cohort = **Blue 62**)

## Context

Paper-first policies: max_markets=4, paper leverage 1×. Seed = Blue 62 exploration. Live static isomorphic Blue was **not** the focus recipe.

## Work completed (2026-07-14)

1. **WUT export** — fixed `wut:portfolios:export_config` (`pyramid_atr_multiplier` try; risk_pct fraction; max_markets/max_leverage fields). Exported PBR 62 → `portfolio_configs/portfolio-blue-pbr62.json`.  
2. **Paper policy patch on JSON** — name `Portfolio Blue · PBR62`, `export_kind=trade_ready`, **max_leverage=1** (lab had 3), max_markets=4, vetting block.  
3. **Wv2 import** — new OP **#12** + TS **#15** (did not overwrite static Blue #7).  
4. **Attention hygiene** — only #12 Active; demoted Red/Blue/Green/Pink/Blank/Rust.  
5. **Recipe check** — one_way_dynamic + move_to_last_entry + SwingBreakout5Day + VolExit — **MATCH**.

## Acceptance

- [x] Cohort choice recorded on paper-first ticket + BA §15  
- [x] Active set matches attention policy for Blue 62 focus (only #12)  
- [x] Focus OP TS matches PBR 62 lab recipe under max_markets=4 / leverage 1× policy  
- [x] Blue 62 path uses new import lineage (not rename of static Blue)

## Live result

| Item | Value |
|------|--------|
| Focus OP | `#12 Portfolio Blue · PBR62` |
| TS | `#15` source `portfolio-import:portfolio-blue-pbr62.json` |
| Config file | `portfolio_configs/portfolio-blue-pbr62.json` |
| Legacy Blue | `#7` inactive (static/isomorphic archive) |
| Active count | **1** |

## Related

- First journal: `2026-07-13-confirm-first-paper-journal-focus-cohort.md` (**also Done**)  
- Parent: `2026-07-13-paper-first-cohort-decision.md`  
