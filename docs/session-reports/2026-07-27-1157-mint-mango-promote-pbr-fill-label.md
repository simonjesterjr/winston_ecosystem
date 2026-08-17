# Session Report — Mint/Mango promote + PBR fill label

**Date:** 2026-07-27  
**Time:** ~09:55–11:57 MDT  
**Duration:** ~2h  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `winston_unit_test/main`, `ecosystem/main` (Wv2 runtime data only)  
**Model:** Grok 4.5  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Promote Portfolio Backtest Runs (PBRs) 335 / 336 / 337 into Winston v2 (Wv2) Operational Portfolios (OPs) for Mint, Mango, and Blue (deactivate existing same-seed actives); then add a visible fill/fulfillment label on the Winston Unit Test (WUT) PBR show page.

**Outcome:** Delivered with intentional skip of Blue/336.

**One-line summary:** Mint #384 (PBR 335) and Mango #385 (PBR 337) are paper-active in Wv2; Blue skipped while 336 re-ran; PBR show page now badges fill cadence (same-bar / next-bar / hybrid modes).

---

## 2. Work Completed

- Inspected WUT PBRs 335–337 (seeds, returns, fill cadence, Trading Strategy (TS) linkage).
- Exported configs to shared `portfolio_configs/`:
  - `portfolio-mint-pbr335.json` (fingerprint `0478e0ea`, WUT TS #55 captured)
  - `portfolio-mango-pbr337.json` (fingerprint `45c09e30`, WUT TS #56 captured)
  - `portfolio-blue-pbr336.json` (export incomplete — no fingerprint; PBR was re-running)
- Patched Mint/Mango JSON with `force_lab_uncapped: true`.
- Imported to Wv2: Mint **#384** (forked), Mango **#385** (forked).
- Deactivated prior actives: Mint **#382** (S4 pack `91608a22`), Mango **#157** (legacy WUT run 57).
- Activated **#384** and **#385**; strategy audits OK.
- Operator directed **skip Blue / PBR 336** (run status flipped to `running` mid-session).
- UI: fill/fulfillment badge on PBR show header + completed overview panel + helper + specs.

---

## 3. Code Delivered

### Files changed

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `app/helpers/portfolio_backtest_runs_helper.rb` | modified | `pbr_fill_cadence_info` / badge helpers |
| `app/views/portfolio_backtest_runs/show.html.erb` | modified | Header badge + completed metadata panel; running block uses helpers |
| `spec/helpers/portfolio_backtest_runs_helper_spec.rb` | added | 5 examples |

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/session-reports/2026-07-27-1157-mint-mango-promote-pbr-fill-label.md` | added | this report |

#### winston_v2

Runtime OP import only (**#384**, **#385**). No application code this session.  
Pre-existing dirty tree (`daily_report_payload_builder`, equity series) **out of scope** — not staged.

### Runtime data (not application commits)

| Item | Result |
|------|--------|
| Exports | `portfolio_configs/portfolio-{mint,mango,blue}-pbr33{5,6,7}.json` |
| Wv2 OP Mint | **#384** · `Portfolio Mint · 0478e0ea` · active · paper · observation · WUT PBR 335 |
| Wv2 OP Mango | **#385** · `Portfolio Mango · 45c09e30` · active · paper · trade_ready · WUT PBR 337 |
| Deactivated | Mint #382, Mango #157 |
| Blue | **#381** S4 pack remains active; PBR 336 **not** promoted |

### Commits

_Pending wrap commit._

### Branch / PR state at sign-off

- Direct `main` on WUT + ecosystem  
- PR: not opened (direct main)

**Monoliths touched:** `winston_unit_test` (code), `ecosystem` (report), `winston_v2` (data only).

---

## 4. Decisions Made

### Decision 1: Skip Blue PBR 336
- **Choice:** Do not import/activate Blue from 336 this session  
- **Why:** Operator request; PBR 336 was mid re-run (`running`, results cleared) so fingerprint capture failed  
- **Alternatives considered:** Wait for completion; promote anyway bare-name  
- **Reversibility:** easy  
- **Promote to ADR?** no  

### Decision 2: Seed-aligned mapping for 335/337
- **Choice:** 335 → Mint, 337 → Mango (portfolio seed on the PBR, not list order)  
- **Why:** Matches lab book membership and exclusive cohorts  
- **Promote to ADR?** no  

### Decision 3: Deactivate prior seed actives before activate
- **Choice:** Deactivate Mint #382 and Mango #157, then activate new OPs (no FORCE dual-active)  
- **Why:** ADR-006 Active mutex per seed_name  
- **Promote to ADR?** no  

### Decision 4: Surface fill cadence on completed PBR show
- **Choice:** Human label + color badge in header and overview (not only running/pending metadata)  
- **Why:** Operator could not visually tell hybrid vs next-bar vs same-bar on completed runs  
- **Promote to ADR?** no  

---

## 5. Insights Surfaced

- PBR 335 lab path used `hybrid_entry_next_pyramid_price_level` (price-level hybrid previously rejected as pack default) with strong +505% / ~72% max drawdown (DD) story — promotion is operator intent, not S4 pack freeze.
- PBR 337 is static Breakout5Day + VolatilityExit, `same_bar_open`, trade_ready, milder path (+136% / 33% DD).
- Fill cadence UI previously lived only under `running? || pending?` metadata — completed overview omitted it entirely.
- Export with `attempt_capture: true` requires **completed** PBR; running runs yield bare strategy JSON without fingerprint (Blue 336).

---

## 6. Issues & Tickets

### Resolved this session
- Mint/Mango attention switched to new fingerprints  
- PBR fill doctrine visibility on show page  

### Deferred
- Blue promote after PBR 336 completes (or choose alternate PBR) — operator-driven  
- Optional: fill badge on PBR **index** table  
- Optional: document 335 hybrid-price promote vs prior S4 next_bar pack freezes  
- Pre-existing unrelated dirty files on ecosystem tickets + Wv2 services — leave alone  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Wv2 import Mint/Mango | rake import + activate + inspect_strategy | ✅ OK |
| Active set | rails runner list | ✅ #384/#385 active; #382/#157 inactive |
| Fill helper | `rspec spec/helpers/portfolio_backtest_runs_helper_spec.rb` | ✅ 5 examples, 0 failures |
| Show page UI | code path only (no browser smoke this session) | ⚠️ pending operator reload |

**Test command(s):**  
`bin/compose exec -T winston_unit_test bundle exec rspec spec/helpers/portfolio_backtest_runs_helper_spec.rb`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** local compose WUT + Wv2  
- **Migrations:** None  

---

## 9. Risks & Technical Debt

- Mint #384 is `export_kind=observation` with hybrid price-level fill doctrine — not the frozen S4 next_bar pack.  
- Mango #385 is `trade_ready` static same-bar; doctrine differs from Mint.  
- Blue attention still on S4 pack #381; dual-seed attention set is intentionally mixed.  
- Unrelated dirty trees on ecosystem/wv2 must not be accidentally staged on wrap.

---

## 10. Open Questions

- **Promote Blue after 336 finishes?** — needs operator; blocks Blue seed refresh  
- **Should 335 hybrid-price be considered temporary paper only?** — product judgment  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Wrap — report written; commits pending  
- **Next concrete step:** After wrap: reload a completed PBR show page to confirm fill badge; optionally re-export/import Blue when 336 completes  
- **Files to read first:**
  1. This report  
  2. `winston_unit_test/app/helpers/portfolio_backtest_runs_helper.rb` (fill helpers)  
  3. `ecosystem/docs/tickets/2026-07-26-s4-recipe-transfer-mint-yellow-blue.md` (prior S4 OP ids)  

---

## 12. Stakeholder Communications

- _None required._ Paper observation swaps only.

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `session-report`, `wrap`  
- **What worked well:** Seed-aligned export/import + deactivate-then-activate for mutex  
- **Friction points:** PBR 336 re-entered `running` mid-investigation (stale metrics → empty); wait-poll cancelled by operator  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Promote Blue when ready (complete PBR 336 or pick another run) — owner: operator  
- [ ] Optional PBR index fill column/badge — owner: eng  
- [ ] Optional note/ticket if hybrid-price Mint supersedes S4 pack freezes for ops attention — owner: operator  

---

## 15. Appendix (optional)

### Active set after promote (snapshot)

| OP | Seed | FP short | Note |
|----|------|----------|------|
| #6, #308 | Orange | 6622b2eb / 7ea76741 | dual-active (pre-existing) |
| #11 | Rust | dd7e7c7a | |
| #381 | Blue | f4dd31eb | S4 pack (unchanged) |
| #383 | Yellow | 2a97a043 | S4 pack |
| **#384** | **Mint** | **0478e0ea** | **PBR 335** |
| **#385** | **Mango** | **45c09e30** | **PBR 337** |

### Lab snapshot (pre-promote)

| PBR | Seed | Fill | Ret / max DD (approx) |
|-----|------|------|------------------------|
| 335 | Mint | hybrid price-level | +505% / 72% |
| 336 | Blue | re-running; skip | was ~−79% / 86% when last completed |
| 337 | Mango | same_bar_open | +136% / 33% |
