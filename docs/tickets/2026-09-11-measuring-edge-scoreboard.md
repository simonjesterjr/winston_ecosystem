# Ticket: Measuring Edge scoreboard (Edge R + E-ratio)

**Status:** In progress
**Priority:** P2
**Date:** 2026-09-11
**Monolith:** cross (WUT lab persist, Wv2 ops evaluation)
**Interface:** `interfaces/winston-edge-v1.md`
**ADR:** `docs/adr/ADR-015-edge-measurement-ownership.md`
**Domain:** `docs/business-context/measuring-edge.md`
**Parent program:** [`2026-09-04-tf-foundations-INDEX.md`](2026-09-04-tf-foundations-INDEX.md) (related to P1 residual signal and P4 compounding — does **not** replace P1)

## Problem

Winston ranks and reports equity-curve theater (total return, practical Sharpe, Calmar). The Measuring Edge note says the actual TF question is: does each unit of risk produce a reliably positive expected R after fills? Entry quality (E-ratio) is a second, independent question.

## Phase 0 (docs) — done

- CONTEXT terms (Edge, 1R, Lot R, Profit Factor, E-ratio, MFE, MAE, Drawdown duration, Edge Snapshot)
- ADR-015, interface `winston-edge-v1.md`, fixtures, business-context explainer

## Phase 1 (`edge_v1` lot expectancy) — shipped 2026-09-11

- [x] Golden fixtures `essay-068r` and `scratch-and-missing-1r` pass in WUT and Wv2
- [x] PBR persist + sortable index column (historical rows `—` until re-run)
- [x] PBR show Edge strip beside Stack ARR / MER
- [x] Wv2 live snapshot + detail fold + Positions (by band) chip
- [x] DAR / MMS recipe tables; not MMS operating_score
- [x] WEV `edge` source (UNKNOWN on first paint)
- [ ] Operator browser clickthrough (ops shell + PBR index)

## Phase 2 (this slice) — E-ratio + path extras

- E10 / E20 / E50 / E70 from MFE/MAE over N session bars after fill ÷ ATR at entry
- Lab PBR: same-symbol random E20 / E50
- Ops: taken entries only (no random scramble)
- Drawdown duration + Sortino on the Edge Snapshot
- Surfaces: PBR Edge strip, Wv2 Edge fold, DAR/MMS compounding (E20/E50)
- Per-lot MFE/MAE on WUT full trade timeline when computed

## Out of scope

- Walk-forward / Monte Carlo / cost stress (TF P1)
- Filter-on vs filter-off paired PBR
- Viability Gates, bake-off primary key, Slate Contest ranking
- Commission model, WQ tracking Edge, open-lot E-ratio on the Positions card
- Journal table columns for MFE/MAE

## Phase 2 acceptance

- [x] Fixture `eratio-long-e10.json` passes in WUT and Wv2
- [x] Persist path writes `e_ratio` + `max_dd_duration_days` (parquet miss is non-fatal)
- [x] PBR Edge strip shows E20 / E50 vs random when present
- [x] Wv2 portfolio live Edge fold shows E20 / E50
- [x] DAR per-OP equity table and MMS compounding include E20 / E50
- [x] Random keys absent on ops snapshots (`e20_random` lab-only)
- [ ] Operator browser clickthrough of E20/E50 on live eval + PBR show

## Related

- Librarian: `typewriter/librarian/koisch-jr/winston_foundations/measuring edge/Measuring Edge.md`
- Do not clone: [`2026-09-04-tf-p1-residual-signal-and-oos.md`](2026-09-04-tf-p1-residual-signal-and-oos.md)
- MER (different formula): [`2026-08-04-stack-arr-mer-risk-scale-chart.md`](2026-08-04-stack-arr-mer-risk-scale-chart.md)

## Progress note (2026-09-16, Scribe)

WUT PBR index **Edge (R)** column shipped in PR **#42** (`7fac0e6`) with hotfixes **#43** (read DB `edge_r`/`edge_components`) and **#44** (Setup TS resolution). Session: `winston_unit_test/docs/session-reports/2026-09-16-2009-pbr-index-setup-accordion-edge-column.md`. Phase 1 browser clickthrough + Phase 2 E-ratio still open; ticket remains **In progress**.
