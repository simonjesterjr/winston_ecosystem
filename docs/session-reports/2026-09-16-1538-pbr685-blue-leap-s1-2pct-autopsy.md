# Session Report — PBR #685 Blue LEAP S1 2% autopsy

**Date:** 2026-09-16  
**Time:** ~15:30–15:40 MDT (Forensics evidence → Scribe trail)  
**Project:** Sawtooth / Winston ecosystem  
**Cell:** `blue_rst_turtle_r02_leap30k_ts75` · PBR **#685** · Portfolio Blue · TS75 · RST · leap_fulfillment=all · risk **2%** · $30k · heat turtle  
**Parent:** #668 `blue_rst_turtle_r01_leap30k`  
**Roles:** Forensics (evidence) → Scribe (trail)  
**Banner:** report only — no pack promotion · no stamps

---

## 1. Goal & Outcome

**Stated goal:** Autopsy Blue LEAP S1 at 2% heat (#685); file AI-DLC trail; surface ranking vs Blue 1% (#684) / Red 1% (#692) and the journal gap red flag.

**Outcome:** Analysis on sawtooth; this wrap filed. Desk law pointer: universal exit+stops ([`exit-and-protective-stop-desk-law.md`](../business-context/exit-and-protective-stop-desk-law.md)); sticky 20D_BO S2-only. Journal gap **explained** (short-LEAP entry always debit); **trust** `final_cash`/OA. Do not treat delta as fake equity.

**One-line summary:** Real LEAP Blue S1 2% compounder (cash ~8759%, OA ~8834%, edge_r 7.80, PF 4.89) — solvent but worse risk-adjusted than #684 / #692; journal delta ≈ **$433.7k** is short-LEAP journal bug (165 shorts), not fake cash.

---

## 2. Work Completed

- Confirmed analysis: [`docs/analysis/2026-09-16-pbr685-blue-leap-s1-2pct.md`](../analysis/2026-09-16-pbr685-blue-leap-s1-2pct.md)
- Wrote this wrap; left analysis + wrap uncommitted
- Linked related CoS workstream ticket (new Blue paper from #685 fingerprint) — see Links

---

## 3. Metrics (quoted from analysis only)

| Metric | #685 Blue 2% | #684 Blue 1% | #692 Red 1% |
|--------|-------------:|-------------:|------------:|
| edge_r | **7.7981** | 8.9251 | 9.4183 |
| PF | **4.8854** | 24.1995 | 27.6637 |
| cash return % | **8759.3** | 2906.5 | 3473.7 |
| OA return % | **8833.6** | 2943.6 | 3493.5 |
| OA max_dd % | **21.40** | 3.03 | 4.20 |
| cash_vs_journal_delta | **433656** | 9180 | 8033 |

Fidelity: 731 closes, 731 leap / 0 share; exit mix 10d 371 / stop 360 (dual doctrine).

---

## 4. Decisions

1. Prefer **OA/cash** ranking (same hygiene as #692 stream).
2. **Trust** `final_cash` / OA / cash_events for promote/ranking; journal delta is **not** evidence the curve is fake.
3. Stop doctrine same as #692 (not sticky 20D_BO) — universal exit+stops law.
4. **No ADR** for this autopsy.
5. File WUT ticket: direction-aware LEAP entry journals (+ short PnL sign in `remove_positions`).

---

## 5. Open / Next

1. ~~Investigate journal delta~~ — **root cause filed** in analysis § Journal gap root cause (Forensics follow-up).
2. Ranking judgment: 2% vs 1% is not a free lunch (OA DD 3%→21%, PF 24→4.9).
3. CoS workstream: new Wv2 paper Blue from #685 fingerprint (IBKR-eval, no IBKR fulfill) — ticket below.
4. Implement / babysit WUT ticket: direction-aware `add_leap_position` journals (+ short close PnL sign).

### Journal gap root cause (quoted from analysis)

- Formula: `cash_vs_journal_delta = final_free_cash − (initial + sum journal flow)`.
- #685: **165/731** closed lots missing credit journals — **100% short**; `sum(pnl − journal_flow)` on those lots = **$433,656.14** (= delta).
- Siblings: #684 **$9,180** (7 short); #692 **$8,033** (5); #683 Orange 2% **~$1.09M** (283).
- Defect: `PositionManager#add_leap_position` always `@total_equity -= flow` + `debit_credit: :debit`. Share path is direction-aware; `PortfolioPositionManager#update_cash_on_entry` correctly credits short LEAP cash — so **live cash is right**, journal ledger is wrong for short LEAPs.
- Secondary: close journal attaches to `positions_to_close.first.id` only; LEAP `remove_positions` PnL uses `(exit−entry)×contracts×100` for both directions (shorts should be entry−exit).

---

## 6. Links

- Analysis: [`../analysis/2026-09-16-pbr685-blue-leap-s1-2pct.md`](../analysis/2026-09-16-pbr685-blue-leap-s1-2pct.md)
- Related #692 wrap: [`2026-09-16-1447-pbr692-working-stop-autopsy.md`](2026-09-16-1447-pbr692-working-stop-autopsy.md)
- Desk law: [`../business-context/exit-and-protective-stop-desk-law.md`](../business-context/exit-and-protective-stop-desk-law.md)
- New ticket (paper Blue): [`../tickets/2026-09-16-wv2-paper-leap-eval-blue-from-685.md`](../tickets/2026-09-16-wv2-paper-leap-eval-blue-from-685.md)
- WUT bug ticket: `winston_unit_test/docs/tickets/2026-09-16-leap-short-entry-journal-direction.md`

---

## 7. Commits / git

- None this turn — leave uncommitted; no push until John/CoS authorize.

---

## 8. Addendum — journal-gap root cause (2026-09-16 ~15:45 MDT)

Forensics amended analysis with § Journal gap root cause. Wrap open/next + decisions updated above. Ticket opened in WUT for the fix. Still no commit/push.
