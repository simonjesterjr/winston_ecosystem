# Ticket: Promote S4 FastBO5 tactics pack — transfer Mint / Yellow / Blue

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-26  
**Monoliths:** winston_unit_test (TS capture / export); winston_v2 (import / paper activate)  
**Related:** bake-off `2026-07-25-strategy-bakeoff-v1-phase1.md`; session `2026-07-26-1103-strategy-bakeoff-phase2.md`; prior Mint Elephant transfer OP#311 caution

---

## Problem

Lab Phase 1–2 freezes a **working next-bar-open recipe** for S4 FastBO5 (Trading Strategy (TS) #48):

| Knob | Freeze |
|------|--------|
| Primary | Breakout5DayStrategy |
| Confirm | none |
| Exits | VolatilityExit |
| Fill | `next_bar_open` |
| Risk | One-Way Dynamic (OWD) ladder A long 2/3/4/6 · short 2/2/2/3/3 · base 2% |
| Pyramid ATR mult | **1.0** |
| Max per symbol / pyramid | **4** |
| Max portfolio lots | **12** |

Honest bake-off economics (not exceptional low-risk, but best primary found):

| Portfolio | Approx bake-off story |
|-----------|----------------------|
| Blue | Strong S4 path (~19% CAGR tier, mid-50s max DD at full chassis) |
| Mint | ~19% CAGR / ~43% max DD (S4 exclusive) |
| Yellow | Weaker CAGR / higher DD; **17 names** — capacity discipline matters |

Legacy Mint PBR 121 Elephant same-bar (~49% CAGR / 24% DD) must **not** be the transfer recipe.

---

## Scope

1. **Confirm TS #48** (or capture a clean fingerprinted successor) embeds freezes: ladder, pyr ATR 1.0, max_sym 4, max_port 12, stop `move_to_last_entry`.  
2. **WUT:** validation/export path for Blue, Mint, Yellow with that TS (or three portfolio configs + same fingerprint).  
3. **Wv2:** import/transfer paper Operational Portfolios; do not overwrite live capital without operator confirm.  
4. **Document** handoff note: next_bar-open lab vs desk fill doctrine; hybrid pyramid same-day is **not** yet in recipe.  
5. **Yellow:** call out larger book — max_port 12 + max_sym 4 is the lab default; watch stress-book lessons.  
6. Optional: Elephant TS #45 as **paper B sleeve at ~1% unit risk** only — not primary.

## Acceptance

- [ ] Fingerprinted TS (or #48 updated) matches freeze table  
- [ ] Export/import path verified for at least one of Mint/Blue/Yellow  
- [ ] Paper OPs created or updated with operator approval  
- [ ] Written note that 121 Elephant is superseded for promotion  
- [ ] Bake-off master ticket status updated  

## Out of scope

- Live capital activate  
- Hybrid fill implementation (separate ticket)  
- Correlation unit heat  

---

## Risks

- Transferring ladder A / 2% into ops without desk fill parity may overstate live path.  
- Yellow may need earlier heat BA than Mint.
