# Session Report — MACD 12/26/9 + Walnut Session Order Slate

**Date:** 2026-09-10
**Time:** ~08:00–11:21 MDT (implementation); HMM analysis 2026-09-09
**Duration:** ~analysis + ~3h ops/code
**Project:** sawtooth Winston ecosystem — `data_manager`, `winston_unit_test`, `winston_v2`, `ecosystem/`
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on each touched repo (from `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

Earlier partial report (MACD only, never committed): `docs/session-reports/2026-09-10-0851-macd-1269-parquet-inspect.md`

---

## 1. Goal & Outcome

**Stated goal:** (1) Ship MACD 12/26/9 as the concrete leftover from the Hidden Markov Model (HMM) analysis. (2) Diagnose Walnut Session Order Slate remints and missing DAY pyramids. (3) Shade slate rows by Winston vs DUT alignment. (4) Verify a later Approve package for DBC.

**Outcome:** Delivered. HMM overlay not built. Slate #46 is a **real** third-lot delta (not a remint); operator still needs to Approve it.

**One-line summary:** MACD is a Winston EOD v0.2 derivative and inspect pane; Walnut fill-driven GTC replace + DAY pyramids now send; slate rows are color-coded; DBC 841-lot replace is waiting on Approve of slate #46.

---

## 2. Work Completed

- HMM treated as dead end except MACD.
- DM always bakes `macd_line` / `macd_signal` / `macd_histogram`; fixed date-keyed Hash write bug; `data:restandardize[SYMBOL]`; GOOGL re-baked.
- WUT + Wv2 `Macd1269Strategy`; inspect MACD pane under ATR.
- `ProtectiveGtcGuard` was blocking GTC **replace** and DAY pyramids on a name with a live GTC → remint storm slates #41–#45. Guard now allows replace (matching DUT id) and pyramid/entry sends.
- Fill-driven repark: do not remint identical coverage; **do** mint when GTC size/stop changed (third lot).
- Voided remint slates #42–#45; re-sent remaining #41 legs (DBC GTC 563 @ 32.32 replacing old 282; DAY pyramids DBC/DD/SCHZ).
- DBC DAY pyramid **filled** 278 @ 33.45 (16:45 UTC) → book 841 long. Slate **#46** draft is the correct replace (841 @ 32.56 + DAY 276 @ 33.67).
- Slate table row shades: aligned GTC / DAY until print / filled / in motion / pending / urgent / cancelled / replace queued.

---

## 3. Code Delivered

### Files changed (this session only — do not stage the rest of the dirty trees)

#### data_manager

| File | Change |
|------|--------|
| `app/services/parquet_standardizer.rb` | modified — always-on MACD, array-aligned compute |
| `app/services/parquet_restandardize_service.rb` | added |
| `lib/tasks/data.rake` | `data:restandardize[SYMBOL]` |
| `spec/services/parquet_standardizer_spec.rb` | added |
| `spec/services/parquet_restandardize_service_spec.rb` | added |
| `AGENTS.md`, `README.md`, `data/README.md` | tiny list updates |

#### winston_unit_test

| File | Change |
|------|--------|
| `app/strategies/entry_exit/macd_1269_strategy.rb` | added |
| `app/strategies/strategy_registry.rb` | `FILE_PATHS` |
| `app/services/strategy_lookback.rb` | period 34 |
| `lib/tasks/seed_strategies.rake` | catalog row |
| `spec/strategies/macd_1269_strategy_spec.rb` | added |
| `spec/services/strategy_lookback_spec.rb` | modified |

**Not this session:** WUT ponytail tickets / INDEX.

#### winston_v2

| File | Change |
|------|--------|
| `app/strategies/entry_exit/macd_1269_strategy.rb` | added |
| `app/strategies/strategy_registry.rb`, `app/services/strategy_lookback.rb` | MACD |
| `app/services/operations/signal_inspect_*` + `show.html.erb` | MACD pane |
| `spec/strategies/macd_1269_strategy_spec.rb`, overlay/payload specs | added/modified |
| `app/services/operations/protective_gtc_guard.rb` | replace + pyramid allow |
| `app/services/operations/journal_confirmation_service.rb` | pass `journal:` to guard |
| `app/services/operations/session_order_slate/fill_driven_repark.rb` | coverage includes units/stop |
| `app/services/operations/session_order_slate/leg_truth.rb` | added — row shades |
| `app/controllers/operations/slates_controller.rb` | overlay + replace-queued |
| `app/views/operations/slates/_legs_table.html.erb` | shaded rows + legend |
| `app/assets/stylesheets/ops_shell.css` | row colors |
| guard / repark / leg_truth / slate request specs | added/modified |

**Not this session:** Quiver Tracking, desk workflows, schema, `working_stop_signal`, eod cadence, etc. (dirty from other work).

#### ecosystem

| File | Change |
|------|--------|
| `interfaces/winston-eod-parquet-standard.md` | v0.2 MACD required |
| `docs/adr/ADR-003-dm-owns-derivatives.md` | MACD bullet |
| `CONTEXT.md` | Winston EOD Standard glossary |
| `docs/tickets/2026-09-09-walnut-paper-session-order-slate.md` | 2026-09-10 afternoon note |
| `docs/session-reports/2026-09-10-0851-macd-1269-parquet-inspect.md` | earlier partial |
| `docs/session-reports/2026-09-10-1121-macd-and-walnut-slate.md` | this report |

### Commits

- _Pending wrap Step 2 (follow-up promotion)._

### Branch / PR state at sign-off

- Branch: `main` on DM / WUT / Wv2 / ecosystem — dirty with this session **plus unrelated work**
- Pushed: not yet
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Bake MACD, not HMM
- **Choice:** parquet + TS primitive + inspect pane. No hidden-state column.
- **Why:** theoretically next TF rule after EMA; HMM needs residual-signal first.
- **Promote to ADR?** No — ADR-003 one-liner.

### Decision 2: Guard allows GTC replace and DAY pyramid
- **Choice:** live GTC still blocks dummy-sim Confirm; slate auto-send of `pyramid_stop` / `entry_stop` / matching `replaces_broker_order_id` is allowed; cancel old GTC after new parks.
- **Why:** otherwise fill-driven replace can never land and pyramids never send.
- **Promote to ADR?** No — methodology already said replace-then-cancel.

### Decision 3: Slate #46 is a real third-lot delta
- **Choice:** do **not** void #46. Operator Approves. Old 563 @ 32.32 GTC is stale vs 841 @ 32.56.
- **Why:** DAY pyramid `#443701277` filled 278 @ 33.45.
- **Promote to ADR?** No.

---

## 5. Insights Surfaced

- `ProtectiveGtcGuard` was written for dummy-sim double-book; it sat on the same Confirm path as Desk Send.
- Fill-driven remint of **identical** 563 @ 32.32 ≠ a later mint when lots/stop change (841 @ 32.56). Coverage key must include units + stop.
- Overlay applied **current** ProtectiveStatus onto **old** executing rows, so a still-live prior GTC looked “stale vs DUT” while the replace sat on a newer draft. Shade **replace queued** when another open slate already cites that DUT id.
- Inspect MACD pane can compute from 90 closes if parquet is old; table column needs baked `macd_*`.

---

## 6. Issues & Tickets

### Resolved this session
- MACD never written to parquet (index vs date-keyed Hash).
- Walnut remint #41–#45; missing DAY pyramids (guard).
- Slate row status was a tag only; now alignment shades.

### Deferred
- Restandardize remaining DM parquet (only GOOGL done). See: [`docs/tickets/2026-09-10-dm-restandardize-macd-corpus.md`](../tickets/2026-09-10-dm-restandardize-macd-corpus.md)
- One-axis MACD confirm vs EMA-20 — blocked on `2026-09-04-tf-p1-residual-signal-and-oos.md`. See: [`docs/tickets/2026-09-10-macd-confirm-one-axis.md`](../tickets/2026-09-10-macd-confirm-one-axis.md)
- HMM overlay — after measurement layer.
- Operator: **Approve Walnut slate #46** (841 GTC + DAY 33.67) if not already done.
- Overnight: DAY teardown of unfilled entries; close stale `executing` slates #40/#41 hygiene.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| DM MACD + restandardize | compose rspec | ✅ |
| WUT Macd1269 | compose rspec | ✅ |
| Wv2 inspect MACD | compose rspec + live GOOGL payload | ✅ |
| Guard / repark / auto-send | compose rspec | ✅ |
| Slate LegTruth + request | compose rspec 20 examples | ✅ |
| #41 remaining legs parked | rails AutoSend; DUT oids | ✅ 563 GTC + 3 DAY pyramids |
| DBC 3rd lot | J1636 executed 33.45 | ✅ real fill |
| #46 | live DB | ✅ draft replace 841 @ 32.56 — **not Approved** |
| Slate row shades live HTML | curl Walnut slate | ✅ classes present |
| Plotly / Approve click-through | none | ⚠️ |

**Live:**  
Inspect GOOGL: `/wv2/operations/signal_inspect?as_of=2026-09-09&portfolio_id=11&symbol=GOOGL&window=90`  
Walnut slate: `/wv2/operations/slate?portfolio_id=1428`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** compose; `winston_v2_sidekiq` restarted after guard fix
- **Migrations:** None
- **Data:** GOOGL parquet MACD columns; Walnut paper DUT orders as above

---

## 9. Risks & Technical Debt

- Wv2/WUT/ecosystem trees still hold **unrelated** dirty files — wrap must stage precise paths.
- Two/three copies of MACD math (DM, WUT calculator, Wv2 strategy/overlay).
- `executing` slates #40/#41 stay open after send; desk shows several historical packs. Hygiene later.
- If operator Approves #46 while Client Portal is cold, new GTC stays in-motion and old GTC stays live (not naked).

---

## 10. Open Questions

- **Did the operator Approve slate #46?** — operator; blocks DBC GTC 841 alignment.
- **Restandardize whole parquet now?** — operator; inspect pane still works via compute.

---

## 11. Handoff & Resume Notes

- **Where I left off:** #46 draft waiting for Approve; old DBC GTC `#443701276` 563 @ 32.32 still on DUT; shade “replace queued” on that row after reload.
- **Next concrete step:** Operator Approves #46 (do not Rebuild). Reload; confirm new GTC oid and old `#443701276` cancelled.
- **Files to read first:**
  1. `winston_v2/app/services/operations/protective_gtc_guard.rb`
  2. `winston_v2/app/services/operations/session_order_slate/leg_truth.rb`
  3. `ecosystem/docs/tickets/2026-09-09-walnut-paper-session-order-slate.md`

---

## 12. Stakeholder Communications

- _None._ Desk: Approve #46 to move DBC GTC to 841 @ 32.56. MACD is selectable, not a live default.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report; four subagents on MACD (CoS + DM + WUT + Wv2)
- **What worked well:** frozen MACD contract in parallel prompts; live rails runner for AutoSend
- **Friction:** host rspec cannot reach compose Postgres; CSS is digested but `/wv2/assets/...` picked up ops_shell changes
- **Subagents:** MACD implementers; slate work was parent-only

---

## 14. Follow-up Actions

- [ ] Approve Walnut slate #46 (841 GTC @ 32.56 + DAY pyramid 276 @ 33.67) — owner: operator — due: this session / next look
- [ ] Restandardize remaining DM parquet for MACD columns — owner: DM — due: convenient — ticket [`2026-09-10-dm-restandardize-macd-corpus.md`](../tickets/2026-09-10-dm-restandardize-macd-corpus.md)
- [ ] One-axis MACD confirm vs EMA-20 after P1 residual-signal — owner: lab — due: later — ticket [`2026-09-10-macd-confirm-one-axis.md`](../tickets/2026-09-10-macd-confirm-one-axis.md)
- [ ] HMM overlay not until measurement layer — owner: lab — due: later
- [ ] Optional: close or hide completed `executing` fill-driven packs so the desk is one current slate — owner: Wv2 — due: later

---

## 15. Appendix (optional)

DBC lots after 16:45 UTC: 282 @ 32.84 + 281 @ 33.21 + 278 @ 33.45 = 841. Working stop 33.45 − 2N ≈ 32.56. Parked DUT `#443701276` is 563 @ 32.32 until #46 sends.
