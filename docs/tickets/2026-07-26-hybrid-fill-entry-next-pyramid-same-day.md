# Ticket: Hybrid fill cadence — next-bar entry, same-day pyramid

**Status:** Scored — **keep pure next_bar pyramids**; do **not** promote hybrid  
**Priority:** P1  
**Date:** 2026-07-26  
**Monoliths:** winston_unit_test (lab first); winston_v2 / desk later (broker API)  
**Experiment key:** `hybrid_fill_pyr_same_day_v1`  
**Map:** `docs/analysis/2026-07-26-hybrid-fill-pyr-same-day-pbr-map.md`  
**Related:** ADR `2026-07-25-lab-t1-fill-queue.md` (addendum hybrid); bakeoff `2026-07-25-strategy-bakeoff-v1-phase1`

---

## Problem

Operator doctrine under test: initial entries `next_bar_open`; pyramids same-day close after the book is live.  
Question: does that hybrid materially improve Compound Annual Growth Rate (CAGR) / Sharpe / survivability on the frozen S4 pack, enough to prioritize broker same-day scale-in automation?

---

## Implementation (shipped)

Per-PBR switch `fill_cadence=hybrid_entry_next_pyramid_same_day` (B1 pyramid close fill). Specs green. Code remains available for future labs.

---

## Lab matrix v1 — scored 2026-07-26

**Chassis:** S4 #48 · ladder A / 2% · pyr ATR 1.0 · max_sym 4 · max_port 12 · $10k  

| Portfolio | Hybrid | Next_bar | Δret | Δdd | Δcagr | Δpyr |
|-----------|--------|----------|------|-----|-------|------|
| Blue | 325 −64/70 | 305 +204/53 | **−268** | +16 | −37 | −3 |
| Orange | 326 +17/52 | 308 +37/32 | −20 | **+20** | −3 | −1 |
| Mango | 327 +55/59 | 311 +182/38 | **−127** | +21 | −11 | −3 |
| Green | 328 −87/94 | 314 −2/88 | −85 | +6 | −36 | −4 |
| Mint | 329 **+298/71** | 323 +163/54 | **+136** | +18 | +7 | +1 |
| Yellow | 330 +106/63 | 324 +166/57 | −61 | +6 | −4 | 0 |

**Paired medians:** Δret **−73**, Δdd **+17**, Δcagr **−8**, Δpyr **−2**, Δtrades **−62**.  
Winners Blue/Mango/Mint med Δret **−127**, Δcagr **−11**. Equity paths distinct 0/6 identical.

### Freeze

- **Do not** adopt hybrid as lab default for S4 pack.  
- **Do not** prioritize broker same-day pyramid automation from this evidence.  
- Keep **pure `next_bar_open`** for entry **and** pyramid.  
- No wave-2 S1/hybrid heat panel indicated.  
- Mint-only wealth win is **not** a promotion (DD worse; Blue/Mango destroyed).

---

## Acceptance

- [x] Hybrid cadence implemented and tested  
- [x] Matrix completed (6 hybrid + Mint/Yellow next_bar baselines)  
- [x] Written call: **no** on same-day pyramid automation priority  
- [x] Map + master ticket updated  

---

## Out of scope (closed for this ticket)

Intraday bars, broker API implementation, S1 arm, re-sweep pyramid knobs under hybrid.
