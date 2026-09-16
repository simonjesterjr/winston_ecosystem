# Session Report — WUT LEAP Edge fix, OA scoreboard, Setup column

**Date:** 2026-09-16  
**Time:** continued from 2026-09-15 Edge work through ~14:00 MDT  
**Project:** sawtooth Winston (`winston_unit_test` primary; `ecosystem` tracking)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Operator:** johnkoisch  
**Agents:** Chief of Staff (Grok Bot), Forensics, PBR Ops, Cursor cloud agents  

---

## 1. Goal & Outcome

**Stated goal:** Fix broken LEAP stored Edge (R); make PBR scoreboard honest for LEAP cells; show TS/setup at a glance on the index.

**Outcome:** Delivered for Edge + OA primary metrics + Setup column. Follow-up UX (accordion / Edge column restore) in flight.

**One-line summary:** Signal-path 1R Edge is on WUT `main` and S1 `#682`–`#697` were refreshed; OA/cash returns persist and lead the scoreboard; Setup column shows `TS# · fulfillment · risk% · heat` with details disclosure.

---

## 2. Work Completed

### Edge (R) — signal-path 1R
- WUT PR #37 merged (`8ea7635`): canonical Winston Edge expectancy + option 1R = `|order_price − stop| × contracts × 100`.
- Rebuild blocked on 258G `development.log` without `.dockerignore`; ignore added; image rebuilt; redis AOF repaired.
- Recalculated `#682`–`#697` `edge_r` into ~1–10R order (was hundreds–thousands). Example: `#692` 886.9 → **9.42**.
- Ticket: [`docs/tickets/2026-09-15-wut-leap-edge-signal-path-1r.md`](../tickets/2026-09-15-wut-leap-edge-signal-path-1r.md) → Done (archived).

### Equity return validation (#682)
- Legacy `total_return` ~**4299%** on `$30k` → `$1.32M` final equity.
- Ending free cash ~`$1.30M` → **~4244% cash return**. Share-notional mark only ~+$17k / ~55 pts at endpoint.
- **Verdict:** predominantly real simulated LEAP premium-cash compounding, not Edge-style fiction. Still not comparable to share books (leverage). Legacy mid-run DD remains misleading.

### Option-aware scoreboard (PR #39)
- Merged: columns `option_aware_total_return`, `option_aware_max_drawdown*`, `cash_total_return`.
- Index/show lead with OA → cash → legacy; sort uses COALESCE.
- Backfilled `#682`–`#697` on sawtooth (`f8d8dca` + migrate).
- Sample OA return / OA DD / cash:
  - `#682` 4263% / 18.6% / 4244%
  - `#692` 3494% / **4.2%** / 3474% (legacy DD was 26%)
  - `#693` 8109% / 5.4% / 8087%
- Duplicate PRs #38/#40 closed; #39 narrative corrected (not “OA ~42%”).

### Setup column (PR #41)
- Merged (`5d12197`): compact Setup cell + `<details>` for chassis / Working Stop / LEAP knobs / stamp.
- Pulled to sawtooth. Follow-up requested: accordion (one open), risk/scale into panel, remove Risk/Scale column, restore **Edge (R)** column — cloud agent in flight.

### Desk bots
- **PBR Ops** — stamp / queue / babysit / scoreboard.
- **Forensics** (Winston section) — PBR/TS/risk autopsies. First task: `#692`.

### #692 forensic (Forensics)
- Real LEAP cash compounder; 100% option closes; Edge 9.42; OA DD ~4.2%.
- **Working Stop on this cell is classic 2N + move_to_last_entry — NOT sticky 20D_BO.**
- TS75 / Red / LEAP all / 1% / turtle / RST / `$30k` / parent `#672`.
- Do not promote as desk-law sticky stops.

### Brokerage (advisory)
- Stay on **IBKR** for LEAP automation (existing Wv2→BG→IBKR path). Tradier/tastytrade are secondary options-API alternatives only.

---

## 3. Code Delivered (WUT)

| PR | SHA / note | Topic |
|----|------------|--------|
| #37 | `8ea7635` | LEAP Edge signal-path 1R |
| #39 | `f8d8dca` | OA/cash metrics + scoreboard primary |
| #41 | `5d12197` | Setup column on PBR index |
| (follow-up) | in flight | Accordion + Edge(R) column restore |

Also: `.dockerignore` on sawtooth tree (large `log/` was blocking image builds).

---

## 4. Decisions (no new ADR)

- **No ADR** for OA scoreboard: presentation/ranking hygiene, not irreversible packaging law.
- LEAP cells: **rank/lead on OA (or cash) return + OA DD**; keep legacy equity visible; do not treat share-notional DD as promote truth.
- Sticky **20D_BO** remains desk Working Stop law; TS75 S1 panel cells that still run classic 2N are a different chassis — label accordingly before promote.
- IBKR remains primary LEAP brokerage for automation.

---

## 5. Open / Next

1. Land Setup follow-up PR (accordion, risk/scale in panel, Edge(R) column).
2. Fix remaining EdgeCalculator scratch-`n` spec (expected 3 got 4).
3. Before promote: restamp sticky-20D_BO LEAP cells if comparing to desk law (do not promote `#692` as sticky).
4. Optional: refresh S2 LEAP refs Edge the same way.
5. Continue Wv2↔BG↔IBKR LEAP fulfillment (separate stream; option permissions).

---

## 6. Links

- Analysis: [`docs/analysis/2026-09-15-ts75-leap-edge-accounting-audit.md`](../analysis/2026-09-15-ts75-leap-edge-accounting-audit.md)
- Edge ticket (archive): `docs/tickets/archive/2026-09-15-wut-leap-edge-signal-path-1r.md`
- Interface: `interfaces/winston-edge-v1.md`
- WUT PRs: #37, #39, #41
