# Session Report — S4 fill science, capital panel, recipe transfer, stop UI

**Date:** 2026-07-26  
**Time:** ~afternoon through 22:24 MDT  
**Duration:** multi-block  
**Project:** sawtooth Winston ecosystem  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `winston_unit_test/main`, `ecosystem/main` (Wv2 data only; no code commit)  
**Model:** Grok 4.5  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Continue from strategy bake-off Phase 2 freezes — ladder mildness, capital scale, hybrid fill implementation + matrix, price-level pyramid experiment, S4 recipe transfer Mint/Yellow/Blue, ops UI clarity on stops / max_markets.

**Outcome:** Delivered. Phase 2 tactics complete; fill variants rejected; S4 pack on Wv2 paper; trade-timeline stop UI clarified.

**One-line summary:** Under next-bar-open, S4 frozen pack (pyr ATR 1.0 · max/symbol 4 · max port 12 · ladder A · $10k) is locked; hybrid same-day-close and price-level pyramid fills both path-destructive; three paper OPs imported inactive; Trade Timeline now emphasizes final/shared stop.

---

## 2. Work Completed

- Phase 2 step 3b OWD ladder mildness (A/B/C): **path-identical** → freeze **keep ladder A**.
- Capital $20k vs $10k panel: **$20k hurts** medians → freeze **keep $10k**.
- Hybrid fill code (`hybrid_entry_next_pyramid_same_day`) + 6-book matrix: **reject hybrid** as pack default.
- Price-level pyramid code (`hybrid_entry_next_pyramid_price_level`) + Blue/Mango/Yellow: **reject**.
- S4 recipe transfer: export PBR 305/323/324 → Wv2 OPs **#381 Blue, #382 Mint, #383 Yellow** (paper, observation, inactive landing; operator later activated Mint #382).
- Ticket: max_markets book-count patch (**not applied** per operator).
- Trade Timeline / positions UI: Final/shared stop primary; initial stop muted; legend.

---

## 3. Code Delivered

### Files changed

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `app/services/lab_fill_cadence.rb` | modified | HYBRID + HYBRID_PRICE modes; price_level_fill |
| `app/services/portfolio_backtest_runner.rb` | modified | Hybrid day path; same_day_close + price_level pyramids |
| `app/services/position_manager.rb` | modified | `fill_price:` override |
| `app/controllers/portfolio_backtest_runs_controller.rb` | modified | fill cadence UI/API; stop_ratcheted; preserve sub-keys |
| `app/helpers/portfolio_backtest_runs_helper.rb` | modified | stop legend helpers |
| `app/views/portfolio_backtest_runs/show.html.erb` | modified | fill switch + stop columns |
| `app/views/portfolio_backtest_runs/trade_timeline.html.erb` | modified | stop column order + legend |
| `app/views/portfolio_backtest_runs/_positions_table.html.erb` | modified | final/shared vs initial stop |
| `app/views/portfolio_backtest_runs/_trade_timeline_stop_cells.html.erb` | added | shared stop cell partial |
| `spec/services/lab_fill_cadence_spec.rb` | modified | hybrid + price-level |
| `spec/services/portfolio_backtest_hybrid_fill_spec.rb` | added | |
| `spec/services/portfolio_backtest_pyramid_price_level_spec.rb` | added | |
| `lib/scripts/s4_phase2_ladder_{setup,scorecard}.rb` | added | |
| `lib/scripts/s4_capital_20k_{setup,scorecard}.rb` | added | |
| `lib/scripts/hybrid_fill_pyr_same_day_{setup,scorecard}.rb` | added | |
| `lib/scripts/hybrid_fill_price_level_{setup,scorecard}.rb` | added | |

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/adr/2026-07-25-lab-t1-fill-queue.md` | modified | hybrid + price-level addenda; rejections |
| `docs/tickets/2026-07-25-strategy-bakeoff-v1-phase1.md` | modified | Phase 2b/capital/hybrid/transfer status |
| `docs/tickets/2026-07-26-s4-phase2-ladder-mildness.md` | modified | scored keep A |
| `docs/tickets/2026-07-26-s4-capital-20k-survivability.md` | added | scored keep $10k |
| `docs/tickets/2026-07-26-hybrid-fill-entry-next-pyramid-same-day.md` | modified | code + reject |
| `docs/tickets/2026-07-26-hybrid-fill-price-level-pyramid.md` | added | reject |
| `docs/tickets/2026-07-26-s4-recipe-transfer-mint-yellow-blue.md` | modified | transfer complete |
| `docs/tickets/2026-07-26-s4-op-max-markets-book-count.md` | added | Proposed; not applied |
| `docs/tickets/INDEX.md` | modified | |
| `docs/analysis/2026-07-26-s4-phase2-ladder-pbr-map.md` | added | |
| `docs/analysis/2026-07-26-s4-capital-20k-pbr-map.md` | added | |
| `docs/analysis/2026-07-26-hybrid-fill-pyr-same-day-pbr-map.md` | added | |
| `docs/analysis/2026-07-26-hybrid-fill-price-level-pbr-map.md` | added | |
| `docs/session-reports/2026-07-26-2224-s4-fill-science-and-transfer.md` | added | this report |

#### winston_v2

Runtime import only (OPs #381–383). **No application code committed this session.** Dirty tree (`daily_report_payload_builder`, etc.) is **pre-existing / out of scope**.

### Runtime lab / ops data (not in git)

| Experiment | Result |
|------------|--------|
| `s4_phase2_ladder_v1` PBR 305–316 | A≡B≡C; keep A |
| `s4_capital_20k_v1` 317–322 | $20k hurts; keep $10k |
| `hybrid_fill_pyr_same_day_v1` 323–330 | reject hybrid |
| `hybrid_fill_price_level_v1` 331–333 | reject price-level |
| Exports | `portfolio_{blue,mint,yellow}-s4-p2pack.json` |
| Wv2 OPs | #381 Blue, #382 Mint, #383 Yellow (paper / observation) |

### Commits

- `8820fd3` (winston_unit_test) — feat(lab): hybrid/price-level fills, S4 panels, trade-timeline stop UX  
- `7159c85` (ecosystem) — docs: S4 fill science freezes, transfer OPs, stop-UI session report  

### Branch / PR state at sign-off

- Direct `main` on WUT + ecosystem  
- Pushed: yes (`8820fd3` WUT; `7159c85` + `51d7f6d` ecosystem)  
- PR: not opened (direct main)  

**Monoliths touched:** `winston_unit_test`, `ecosystem`; `winston_v2` data only.

---

## 4. Decisions Made

### Decision 1: Keep OWD ladder A
- **Choice:** No milder ladder B/C  
- **Why:** Path-identical at frozen heat; level-1 2% dominates  
- **Promote to ADR?** no  

### Decision 2: Keep lab capital $10k
- **Choice:** Reject $20k as survivability upgrade  
- **Why:** Median path worse; not scale-invariant under next-bar queue  
- **Promote to ADR?** no  

### Decision 3: Pure next_bar for entry and pyramid
- **Choice:** Reject hybrid same-day-close and price-level resting stops as pack default  
- **Why:** Path-destructive vs next_bar; few pyramids; Blue/Mango hurt  
- **Promote to ADR?** addendum on lab T+1 ADR only  

### Decision 4: Transfer S4 pack to Wv2 paper observation
- **Choice:** OPs #381–383 from PBR 305/323/324; force_lab_uncapped  
- **Why:** Science freezes complete enough for ops paper  
- **Promote to ADR?** no  

### Decision 5: max_markets patch deferred
- **Choice:** Ticket only; do not apply now  
- **Why:** Operator request  
- **Promote to ADR?** no  

---

## 5. Insights Surfaced

- Mid-ladder mildness and half vs flat 1% identity: **level-1 unit risk + breadth heat** dominate depth.
- Extra cash ($20k) and “faster” pyramid fills both rewrite **T+1 path selection**, often for the worse.
- Pyramid fill counts stay tiny (~0–4) under max_port 12; fill timing still cascades entry paths.
- Trade timeline “initial stop” is birth stop; shared exit uses final/updated stop (move_to_last_entry).
- `max_markets` null ≠ missing heat freeze — heat is `max_positions_per_portfolio=12`.

---

## 6. Issues & Tickets

### Resolved this session
- Ladder mildness scored  
- Capital 20k scored  
- Hybrid fill implemented + scored reject  
- Price-level implemented + scored reject  
- S4 transfer to Wv2  

### Deferred
- `2026-07-26-s4-op-max-markets-book-count.md` — patch OPs max_markets to book size (not applied)  
- Operator activate remaining S4 OPs / deactivate prior seed Actives (Blue #240, Yellow #330; Mint may already be on #382)  
- Optional export hygiene + ops audit UX for max_markets vs max_port  
- Correlation multi-level heat BA (prior ticket)  

### Already filed
- See INDEX rows for bake-off / hybrid / capital / transfer / max_markets  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Ladder / capital / hybrid / price-level scorecards | rails runner scorecards | ✅ completed panels |
| LabFillCadence + hybrid + price-level specs | rspec (24 examples) | ✅ 0 failures |
| Wv2 import | rake import + inspect_strategy | ✅ ladder OK on #381–383 |
| Trade timeline UI | code + timeline smoke | ✅ stop_ratcheted flags work |
| max_markets patch | — | ⏭️ deferred |

**Test command(s):**  
`bin/compose exec -T winston_unit_test bundle exec rspec spec/services/lab_fill_cadence_spec.rb spec/services/portfolio_backtest_hybrid_fill_spec.rb spec/services/portfolio_backtest_pyramid_price_level_spec.rb`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** local compose WUT + Wv2  
- **Migrations:** None  

---

## 9. Risks & Technical Debt

- Three capture fingerprints for one recipe family (date windows in TS names) — methodology knobs match.  
- Dirty unrelated files on ecosystem/wv2 trees — wrap must not stage them.  
- Observation export_kind — Capital Activation soft-warns, not trade_ready.  

---

## 10. Open Questions

- **Activate Blue #381 / Yellow #383 and deactivate prior Actives?** — operator  
- **Apply max_markets book-count patch?** — ticket open, operator said not now  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Trade Timeline stop UI shipped; wrap  
- **Next concrete step:** Operator re-eval stops in UI; optionally activate remaining S4 OPs; later max_markets ticket  
- **Files to read first:**  
  1. `ecosystem/docs/tickets/2026-07-26-s4-recipe-transfer-mint-yellow-blue.md`  
  2. `ecosystem/docs/analysis/2026-07-26-hybrid-fill-pyr-same-day-pbr-map.md`  
  3. `ecosystem/docs/tickets/2026-07-26-s4-op-max-markets-book-count.md`  

**S4 working pack:** next_bar_open · OWD ladder A / 2% · pyr ATR **1.0** · max_sym **4** · max_port **12** · capital **$10k** · Breakout5 + VolatilityExit  

**Wv2 OPs:** Blue #381 · Mint #382 · Yellow #383  

---

## 12. Stakeholder Communications

- _None required._ Operator-facing freezes recorded in tickets/maps.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, session-report, wrap  
- **What worked well:** setup → operator Execute → scorecard loop  
- **Friction points:** multi-repo git; fill experiments need careful baseline max_sym matching  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Apply max_markets = book size on OPs #381–383 — ticket `2026-07-26-s4-op-max-markets-book-count.md`  
- [ ] Activate Blue #381 / Yellow #383 (deactivate #240 / #330 if desired) — operator  
- [ ] Optional: export path sets max_markets to markets.size when uncapped  
- [ ] Optional: ops Strategy audit prints max_port_lots vs max_markets  
- [ ] Correlation heat BA — prior ticket  

---

## 15. Appendix (optional)

### Fill science scorecard (abbrev)

| Panel | Med Δ vs next_bar | Call |
|-------|-------------------|------|
| Hybrid same-day close | Δret −73, Δdd +17 | Reject |
| Price-level stop | Δret −200, Δdd +20 | Reject |
| Capital $20k | Δret −98, Δdd +7 | Keep $10k |
| Ladder B/C | Δ = 0 | Keep A |
