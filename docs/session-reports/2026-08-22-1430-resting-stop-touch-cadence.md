# Session Report — Resting stop-touch cadence + split safeguards

**Date:** 2026-08-22
**Time:** 2026-08-20 session start → 14:30 MDT
**Duration:** multi-day (~two calendar days of lab work)
**Project:** sawtooth Winston ecosystem
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on each monolith (started from `origin/main`)
**Model:** Grok 4.6
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Land Winston Unit Test (WUT) lab cadence `resting_stop_touch` from ticket `2026-08-20-wut-resting-stop-touch-fill-cadence`; score vs next-open; then diagnose Mint ruin and ship v2 data/guard safeguards.

**Outcome:** Delivered.

**One-line summary:** Resting Donchian stop-entry is an opt-in WUT fill mode; v1 Mint −100% was unadjusted reverse-split covers, not Turtle geometry; after parquet stitch + stop-guard, Mint resting **+242% / 56% DD** beats honest next-open **+94% / 58% DD**. Do not promote as pack default.

---

## 2. Work Completed

- New lab mode `resting_stop_touch`: signal-bar Donchian fill via `price_level_fill`; no T+1 entry queue; pyramids stay price-level; same-bar mid-touch freeze; gap-through protective stop at open (tradable).
- PBR UI “Set for next run” + helper badge; fingerprint cadence stamps (omit unstamped hybrid default; resting includes `corporate_action_stop_guard`).
- v1 scorecard: Mint S2 #533 vs #532, Yellow S1 #535 vs #534.
- Diagnosed Mint ruin: 0 same-bar exits; Dec 2019 cash-negative on **both** arms with ~$10k equity; USO 1-for-8 and XOP 1-for-4 unadjusted jumps × cover-at-open ≈ −$9.2k of −$9.0k 2020 P&L.
- v2: DM reverse-split back-adjust (USO×8, XOP×4, OIH×20); WUT split-like overnight covers at **working stop**; Wv2 `split_like_gap` / CORPORATE_ACTION_HOLD; P0 issue + ticket.
- v2 Mint re-score #536/#537 completed (operator-run). Resting survived and beat next-open on stitched bars.

---

## 3. Code Delivered

### Files changed

#### winston_unit_test

| File | Change | Notes |
|------|--------|-------|
| `app/services/lab_fill_cadence.rb` | modified | `RESTING_STOP_TOUCH` mode |
| `app/services/portfolio_backtest_runner.rb` | modified | signal-bar Donchian fill, same-bar freeze, gap-through stop, split-guard |
| `app/services/corporate_action_jump.rb` | added | overnight ratio ≥1.8 / ≤1/1.8 |
| `app/services/trading_strategy_fingerprint_capture.rb` | modified | cadence stamps + guard flag |
| `app/helpers/portfolio_backtest_runs_helper.rb` | modified | labels/badge |
| `app/controllers/portfolio_backtest_runs_controller.rb` | modified | MODES include resting |
| `app/views/portfolio_backtest_runs/show.html.erb` | modified | switch option |
| `spec/services/lab_fill_cadence_spec.rb` | modified | |
| `spec/services/portfolio_backtest_resting_stop_touch_spec.rb` | added | locked tapes + shorts + split-guard |
| `spec/services/corporate_action_jump_spec.rb` | added | |
| `spec/services/position_manager_fill_relative_stop_spec.rb` | modified | fill 110 → stop 102 |
| `spec/services/portfolio/entry_requirement_calculator_spec.rb` | modified | fill_price sizing |
| `spec/services/trading_strategy_fingerprint_capture_spec.rb` | modified | |
| `spec/helpers/portfolio_backtest_runs_helper_spec.rb` | modified | |
| `spec/requests/portfolio_backtest_runs_fill_cadence_spec.rb` | added | |
| `lib/scripts/resting_stop_touch_v1_setup.rb` | added | |
| `lib/scripts/resting_stop_touch_v1_scorecard.rb` | added | |
| `lib/scripts/resting_stop_touch_v2_mint_setup.rb` | added | |
| `docs/tickets/2026-08-20-wut-resting-stop-touch-fill-cadence.md` | added | pointer to ecosystem |

#### data_manager

| File | Change | Notes |
|------|--------|-------|
| `app/services/corporate_action_jump.rb` | added | lockstep with WUT |
| `app/services/split_adjustment_service.rb` | added | scan/apply parquet |
| `app/services/parquet_standardizer.rb` | modified | stitch jumps before ATR |
| `app/services/eodhd_client.rb` | modified | scale OHLC by `adjusted_close` |
| `lib/tasks/split_adjust.rake` | added | `data:scan_split_jumps`, `data:back_adjust_splits` |
| `config/environments/development.rb` | modified | FileUpdateChecker (inotify exhaustion) |
| `spec/services/corporate_action_jump_spec.rb` | added | |

**Not this session (left dirty):** `session_coverage*` jobs/specs, `daily_data_orchestrator_job.rb`.

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/services/operations/stop_out_reconciliation.rb` | modified | `split_like_gap` + CORPORATE_ACTION_HOLD |
| `app/services/operations/ad_hoc_exit_service.rb` | modified | pass flag through |
| `app/services/operations/ops_shell_chat.rb` | modified | print HOLD |
| `spec/services/operations/stop_out_reconciliation_spec.rb` | modified | |

**Not this session:** DAR honesty/catchup/session-data-gate files.

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/tickets/2026-08-20-wut-resting-stop-touch-fill-cadence.md` | added | |
| `docs/tickets/2026-08-20-resting-session-stop-orders.md` | added | parent, still Blocked |
| `docs/tickets/2026-08-22-corporate-action-stop-safeguards.md` | added | P0 |
| `docs/issues/2026-08-22-unadjusted-reverse-split-jumps.md` | added | |
| `docs/analysis/2026-08-21-resting-stop-touch-v1-scorecard.md` | added | v1 + v2 addendum |
| `docs/analysis/2026-08-21-resting-stop-touch-v1-matrix.json` | added | |
| `docs/analysis/2026-08-22-mint-resting-stop-touch-ruin.md` | added | |
| `docs/adr/2026-07-25-lab-t1-fill-queue.md` | modified | resting addendum + score |
| `interfaces/winston-eod-parquet-standard.md` | modified | split-jump clause |
| `docs/tickets/INDEX.md` | modified | |
| `docs/session-reports/2026-08-22-1430-resting-stop-touch-cadence.md` | added | this file |

### Commits

- _Pending wrap commit._

### Branch / PR state at sign-off

- Branch: `main` on WUT, DM, Wv2, ecosystem — dirty until wrap commits
- Pushed: no (this wrap)
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Resting-touch is opt-in, not pack default
- **Choice:** New `LabFillCadence` mode; unstamped PBR default stays hybrid price-level; ADR-009 next-open unchanged.
- **Why:** Automating live resting stops against a next-open backtest would be a silent strategy change.
- **Alternatives considered:** Reuse hybrid_price (keeps T+1 entries); same_bar_open (fills at T open, usually below breakout).
- **Reversibility:** easy (switch)
- **Promote to ADR?** Partial — addendum on `2026-07-25-lab-t1-fill-queue.md`, not a new ADR.

### Decision 2: Do not revert cover-at-open
- **Choice:** Tradable gaps still fill at open (live stop-market). Split-like overnight ratios cover at working stop.
- **Why:** Cover-at-open is correct on a continuous tape; 8× prints were corporate actions.
- **Alternatives considered:** Always fill stops at stop level (hides real gaps); skip the bar.
- **Reversibility:** easy
- **Promote to ADR?** no — issue + parquet standard sentence.

### Decision 3: Back-adjust named reverse splits, do not universe-blind-apply
- **Choice:** APPLY USO/XOP/OIH only. Leave APLD penny 2× flips. Flag UNG/WEAT/AMCR as suspects.
- **Why:** 1.8 ratio fires on penny noise; official COVID reverse splits are known.
- **Reversibility:** backups `bars.parquet.pre_split_adjust`
- **Promote to ADR?** no

### Decision 4: v1 Mint −100% is not evidence against Turtle stop-entry
- **Choice:** After stitch, Mint resting +242 / 56 DD vs next-open +94 / 58 DD. Yellow already +85 ret / +10 DD. Still no OP stamp.
- **Why:** One exclusive pair plus Yellow is not a pack freeze; it is enough to retire the ruin narrative.
- **Reversibility:** scoring decision
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- WUT `uses_t1_entry_queue?` is the day-loop fork; resting rides the same-bar path with a Donchian fill override.
- Same-bar protective stops: **0/97** on ruined 533 and **0/747** on 532. Freeze worked.
- Short-margin cash went negative **2019-12-31 on both arms** with ~$10k equity (VNQ cover). Terminal −$23 on 533 is leftover after equity ruin, not the Dec cash print.
- EODHD `close` vs `adjusted_close`: DM was storing raw OHLC. Parquet standard already asked for adjusted prices.
- v1 next-open Mint **+395%** is contaminated (stop-at-level through 8× jumps). Honest next-open on stitched energy is **+94%**.
- Corporate-action **guard did not fire** on PBR 537 — parquet stitch was load-bearing.
- DM `EventedFileUpdateChecker` exhausts inotify against the parquet corpus; `rails runner` was unusable until switched to `FileUpdateChecker`.
- Compose `RAILS_ENV=development` makes `rspec` hit CSRF and the lab DB unless `RAILS_ENV=test TEST_DB_HOST=…`.

---

## 6. Issues & Tickets

### Resolved this session
- Geometry + locked tapes for `resting_stop_touch`.
- Mint ruin classification (capture/data artifact × cover-at-open).
- USO/XOP/OIH reverse-split stitch on disk.
- WUT split-guard + Wv2 HOLD flag.

### Deferred
- UNG 2024-01-24, WEAT 2025-11-25, AMCR 2026-01-15 suspected reverse splits — noted on P0 issue, not applied.
- Broader resting vs next-open bakeoff on **adjusted** parquet (more books than Mint/Yellow).
- BG L3 `order_write` hold (ticketed; no write path).
- Do not stamp Turtle paper OPs to resting-touch (decision, not a ticket).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| WUT fill cadence + resting tapes + split-guard | `RAILS_ENV=test TEST_DB_HOST=wut_postgres bundle exec rspec` focused | ✅ 46 examples (later batch), 0 failures |
| DM CorporateActionJump | compose `rspec spec/services/corporate_action_jump_spec.rb` | ✅ 3 examples |
| Wv2 StopOutReconciliation | compose `rspec spec/services/operations/stop_out_reconciliation_spec.rb` | ✅ 4 examples |
| USO/XOP/OIH stitch | live parquet after APPLY=1 | ✅ ratios 1.057 / 0.968 / 0.949 |
| v1 PBR 532–535 | operator-run completed | ✅ scored |
| v2 PBR 536–537 | operator-run completed | ✅ 537 +242 / 56 vs 536 +94 / 58 |

**Test command(s):**

```
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wut_postgres winston_unit_test bundle exec rspec spec/services/lab_fill_cadence_spec.rb spec/services/portfolio_backtest_resting_stop_touch_spec.rb spec/services/corporate_action_jump_spec.rb
./bin/compose exec -T data_manager bin/rails data:back_adjust_splits SYMBOLS=USO,XOP,OIH APPLY=1
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added.
- **Services:** existing compose (WUT :3000, DM :3001, Wv2 :3002).
- **Migrations:** None.
- **Data:** mutated `sawtooth_dm_data` parquet for USO, XOP, OIH; backups `*.pre_split_adjust` on the volume.

---

## 9. Risks & Technical Debt

- Duplicate `CorporateActionJump` in DM and WUT — must stay in lockstep (RATIO_HIGH 1.8).
- Split-adjust changes ATR on those symbols; all future PBRs on USO/XOP/OIH differ from pre-2026-08-22 history (including parent Turtle 432).
- 1.8 threshold still flags APLD penny 2× noise — do not universe-APPLY.
- Guard is untested in production path (never fired on 537).
- Wv2 HOLD is warning-only; desk can still confirm a bad fill.

---

## 10. Open Questions

- **Should UNG/WEAT/AMCR be back-adjusted?** — needs a look at official split notices; blocks complete parquet hygiene.
- **Does resting belong on more exclusive books?** — needs a v2 matrix; blocks any promotion discussion.
- **Live stop-market vs lab cover-at-open** — parent BG ticket still Blocked on L3.

---

## 11. Handoff & Resume Notes

- **Where I left off:** v2 Mint pair scored; P0 filed; wrap.
- **Next concrete step:** Decide whether to back-adjust UNG/WEAT/AMCR; optionally run a wider resting vs next-open panel on stitched parquet. Do **not** stamp OPs.
- **Files to read first:**
  1. `ecosystem/docs/analysis/2026-08-21-resting-stop-touch-v1-scorecard.md` (v2 table)
  2. `ecosystem/docs/analysis/2026-08-22-mint-resting-stop-touch-ruin.md`
  3. `ecosystem/docs/issues/2026-08-22-unadjusted-reverse-split-jumps.md`
  4. `winston_unit_test/app/services/lab_fill_cadence.rb`
  5. `winston_unit_test/app/services/portfolio_backtest_runner.rb` (stop branch + `previous_session_bar`)

---

## 12. Stakeholder Communications

- Operator already has the v2 reading in chat. No outward email required unless promoting resting to paper OPs (not recommended this session).

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, lightweight-bug-fix (not a defect — ticket TDD), investigate-system-variance, manage-issue-ticket, record, wrap, session-report.
- **What worked well:** locked-tape specs; journal+parquet reconstruction of USO/XOP covers; fair-pair discipline (536 vs 537, not 537 vs 532).
- **Friction points:** compose rspec defaults to development (CSRF + lab DB); DM inotify; `rails runner` vs volume writes only from DM.
- **Subagent usage:** none.

---

## 14. Follow-up Actions

- [ ] Review/apply UNG, WEAT, AMCR reverse-split suspects — owner: operator + DM — due: next data hygiene pass — See: `docs/issues/2026-08-22-unadjusted-reverse-split-jumps.md`
- [ ] Optional wider resting vs next-open bakeoff on **adjusted** parquet — owner: operator — due: unset
- [ ] BG L3 `order_write` hold for split-like stop-markets — owner: later L3 — See: `docs/tickets/2026-08-22-corporate-action-stop-safeguards.md`
- [ ] Do not stamp Turtle paper OPs to resting-touch — owner: operator — standing decision

---

## 15. Appendix

### PBR IDs

| ID | Exp | Arm | Result |
|----|-----|-----|--------|
| 532 | v1 | next-open Mint S2 | +395 / 44 DD (contaminated) |
| 533 | v1 | resting Mint S2 | −100 / ruin |
| 534 | v1 | next-open Yellow S1 | +121 / 30 DD |
| 535 | v1 | resting Yellow S1 | +206 / 40 DD |
| 536 | v2 | next-open Mint S2 | +94 / 58 DD |
| 537 | v2 | resting Mint S2 | +242 / 56 DD |

### Parquet after APPLY

- USO 2020-04-28 close 17.04 → 2020-04-29 open 18.01 (ratio 1.057)
- XOP 2020-03-27 close 32.12 → 2020-03-30 open 31.10 (ratio 0.968)
- OIH 2020-04-14 close 96.40 → 2020-04-15 open 91.47 (ratio 0.949)
