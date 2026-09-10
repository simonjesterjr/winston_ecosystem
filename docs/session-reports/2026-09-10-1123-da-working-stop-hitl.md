# Session Report — DA Working Stop HITL + GTC reconstruction

**Date:** 2026-09-10
**Time:** ~2026-09-09 afternoon–2026-09-10 11:23 MDT
**Duration:** ~multi-hour (calendar overnight)
**Project:** sawtooth (Winston v2 + ecosystem)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** Wv2 `fix/da-working-stop-hitl` (from `39f22a1` / `main`); ecosystem `docs/da-working-stop-hitl` (from `6a2a761`). `main` in both repos was **dirty with unrelated Walnut-slate / MACD / WQ work** — not mixed into these branches.
**Model:** Grok 4.6 (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Explain why Mint #797 AMCR desk form was 40 @ 43.13 instead of flatten-all at the 2N stop; reconstruct GTC first-penetration books; recast `ISSUE-20260909-da-20day-exit-under-max-lots`; implement paper HITL Daily Analysis (DA) so Working Stop is methodology (fulfillment is the only paper vs live split); re-check remaining open lots and Walnut.

**Outcome:** Partially delivered — capital reconstruction and engine/docs shipped on dedicated branches; 2026-09-10 parquet not in, so today’s OIH/REMX/VXX stop-outs are not yet HITL-tasked; DA-stop **not merged to `main`** (slate WIP collision).

**One-line summary:** Paper Human-in-the-Loop (HITL) must obey the same Trend Following (TF) 2N Good-Til-Canceled (GTC) Working Stop as live; DA was Donchian-only. Operator books reconstructed first pierces; engine now emits signaled `:stop_out`; Confirm flatten-all; Walnut dummy-sim blocked while a parked GTC is live.

---

## 2. Work Completed

- Diagnosed workflow `journal_id=1477` / `task_id=1407`: DA **20-day** one-lot 40u @ last close 43.13 vs shared 2N 45.75, first GTC pierce **2026-08-27**.
- Filed then **recast** `winston_v2/docs/issues/2026-09-09-da-20day-exit-under-max-lots.md` after operator correction: paper HITL = same Winston/TF/Donchian; only fulfillment differs. Unsignaled Exit Allowance ≠ “DA may skip 2N.”
- Booked Mint #797 **AMCR** flatten 119u @ 45.75 on 2026-08-27 (j#1482–1484); passed j#1477 `superseded`.
- Booked Mint #797 **WEAT** flatten 257u @ **26.81** (gap-open) on 2026-09-03 (j#1590–1592).
- Booked **30** further paper stacks at first GTC pierce (j#1593–#1634). Remain-pierce **0** on 2026-09-09 parquet.
- Ecosystem glossary recast (Working Stop, Unsignaled Exit Allowance, Turtle S2, Walnut ticket pointer).
- Implemented DA `WorkingStopSignal`, TaskGenerator/EodCadence same-session GTC cadence, Desk Confirm flatten-all, `ProtectiveGtcGuard`.
- Compose smoke 2026-09-09: dummy_sim remaining lots **above 2N** (no stop_out). 2026-09-10: no parquet session bars yet.
- Coordinated git via worktrees so Walnut-slate dirty `main` was not the integration target.

---

## 3. Code Delivered

### Files changed

**winston_v2 `fix/da-working-stop-hitl` (vs `39f22a1`):**

| File | Change | Notes |
|------|--------|-------|
| `app/services/operations/working_stop_signal.rb` | added | GTC fill, S2 20-day gate, flatten-all `:stop_out` |
| `app/services/operations/signal_evaluation.rb` | modified | Working Stop **before** `evaluate_exit` |
| `app/services/operations/task_generator.rb` | modified | stack units; persist flatten_all / GTC fields |
| `app/services/operations/eod_cadence.rb` | modified | `fill_mode: stop_out` same-session, not T+1 |
| `app/services/operations/journal_confirmation_service.rb` | modified | flatten sibling `lot_ids`; GTC guard |
| `app/services/operations/exit_at_stop_service.rb` | modified | skip already-flat lots; GTC guard |
| `app/services/operations/protective_gtc_guard.rb` | added | refuse dummy-sim while Walnut protective GTC working |
| `app/services/operations/portfolio_live_snapshot.rb` | modified | stack `lots_freed` |
| `app/controllers/operations/desk_workflows_controller.rb` | modified | stop_out prefill |
| `app/views/operations/desk_workflows/*` | modified | Confirm flatten-all copy |
| `app/views/operations/shared/_signal_spine.html.erb` | modified | Working Stop signal speech |
| `docs/issues/2026-09-09-da-20day-exit-under-max-lots.md` | added | recast issue |
| specs listed in commits | added/modified | 76 examples green on integration worktree |

**ecosystem `docs/da-working-stop-hitl`:**

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | Working Stop / Unsignaled / Stop-Out Reconciliation |
| `docs/business-context/turtle-s2-pyramid-and-working-stop.md` | modified | law for DA **and** slate |
| `docs/business-context/human-gated-desk-and-fulfillment.md` | modified | signaled stop-out |
| `docs/tickets/2026-09-09-walnut-paper-session-order-slate.md` | modified | DA follow-on → recast issue |

**Live capital (not git):** journals #1477 passed; #1482–1484 AMCR; #1590–1592 WEAT; #1593–1634 other GTC flattens. Positions closed as booked.

**Not in this session’s DA-stop commits:** Walnut slate auto-send, MACD 12/6/9, WQ desk fulfillment — those sit **uncommitted on `main`**.

### Commits

**winston_v2 `fix/da-working-stop-hitl`:**

- `f6ac8f0` — `fix(da-stop): evaluate Working Stop as signaled stop_out`
- `e5ee245` — `fix(da-stop): task stop_out as same-session flatten-all HITL draft`
- `52657d3` — `fix(da-stop): desk Confirm prefills flatten-all GTC stop_out`
- `4cd7754` — `fix(da-stop): refuse dummy-sim stop-out while Walnut GTC is live`
- `951a7d5` — `docs(da-stop): record HITL engine merge and 2026-09-10 smoke`

**ecosystem `docs/da-working-stop-hitl`:**

- `e250345` — `docs(stops): paper HITL evaluates Working Stop; fulfillment is the only split`

### Branch / PR state at sign-off

- Winston v2 `main` / `origin/main`: `8df584f` (engine in `2489897`; issue history `8df584f`)
- Ecosystem `main` / `origin/main`: `84f8986` (CONTEXT recast, ADR-009 addendum `5c322b6`, this report)
- Pushed: yes
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Paper HITL = same methodology; fulfillment is the only split
- **Choice:** DA must emit a **signaled** `:stop_out` (GTC fill, flatten-all). Confirm books dummy_sim; Walnut Accept-Fill books the DUT print.
- **Why:** Operator grill 2026-09-10. ADR-009 unsignaled path is residual, not “skip 2N on paper.”
- **Alternatives considered:** Keep stops unsignaled / red-button only (rejected).
- **Reversibility:** easy (branch not on `main`)
- **Promote to ADR?** yes — short ADR-009 addendum if glossary vs ADR body still disagree (CONTEXT already narrowed).

### Decision 2: Historical GTC reconstruction at first penetration
- **Choice:** touch → stop; gap → open; skip fill bar; `external_stop`; pass spurious 20-day as `superseded`.
- **Why:** Same WUT `price_level_fill` sell/buy-stop as a live GTC.
- **Alternatives considered:** WUT default **close**-through (would delay AMCR to 08-31); book at last close (rejected).
- **Reversibility:** costly (capital already booked)
- **Promote to ADR?** no — fill rule belongs in Working Stop / Turtle S2 docs (done).

### Decision 3: Do not merge DA-stop onto dirty `main`
- **Choice:** Integration branch + worktrees; compose ran via **checkout of DA-stop files onto dirty `main` index**.
- **Why:** Walnut slate / MACD / WQ already dirty on `main`.
- **Alternatives considered:** Stash slate (risky); one mixed commit (rejected).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 4: Walnut dummy-sim refuse while protective GTC is working
- **Choice:** `ProtectiveGtcGuard` on Confirm and Exit-at-stop unless `accept_fill`.
- **Why:** Second MKT or local book while DUT GTC is live would double-fill.
- **Alternatives considered:** Silence DA on slate-bound OPs (rejected — DAR should still tell the truth).
- **Reversibility:** easy
- **Promote to ADR?** no — fulfillment table in CONTEXT is enough until Accept-Fill is proven.

---

## 5. Insights Surfaced

- DA holding path never read `updated_stop`. Channel exits (20/10/5-day, vol) are **not** the 2N GTC. That is why WEAT was silent and AMCR got a 20-day one-lot T+1 draft.
- Turtle S2 20-day-under-max is a **recipe** bug in DA, not a reason to skip 2N.
- `SessionHandoff` de-dupes exits by symbol×session — one 40u task for a 119u stack.
- Form default `reason=external_stop` made a 20-day look like a broker stop.
- DA uses **current** open lots, not as-of lots: 2026-09-09 Walnut smoke saw 09-10 DBC pyramid (#785) and emitted a false 09-09 DBC stop_out (stop 33.06 vs 09-09 open 32.81). Point-in-time positions are a follow-up.
- 2026-09-10 parquet not landed at wrap; Yahoo in-session suggested OIH/REMX/VXX through 2N.

---

## 6. Issues & Tickets

### Resolved this session
- Operator GTC reconstruction of missed 2N stacks (capital). Issue **not** closed — engine shipped on a branch, not `main`.
- Recast `ISSUE-20260909-da-20day-exit-under-max-lots` (status `in-progress`).

### Deferred
- Catchup DA + HITL Confirm when **2026-09-10 parquet** arrives (OIH Mint #797/#384, REMX Yellow, VXX Orange).
- Merge `fix/da-working-stop-hitl` to `main` without eating slate/MACD/WQ WIP; inspect payload/show left on slate dirty files.
- Signal-inspect STOP-OUT label lives on the DA-stop branch; `main` inspect files are slate-dirty.
- Walnut Accept-Fill proof for GTC (`2026-09-09-walnut-stp-accept-fill-day-entry.md`).
- DA as-of position snapshot (replay must not include later lots).
- ADR-009 body still lists stop-out under Unsignaled; CONTEXT now narrower.
- Push/PR for both DA-stop branches.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| WorkingStopSignal + SignalEvaluation | worktree rspec | ✅ 22 examples |
| EodCadence + TaskGenerator stop_out | worktree rspec | ✅ |
| Desk workflow + flatten-all Confirm | worktree rspec | ✅ |
| ProtectiveGtcGuard | worktree rspec | ✅ |
| Combined suite on `fix/da-working-stop-hitl` | 76 examples, 0 failures | ✅ |
| Mint AMCR/WEAT + 30 stacks | rails `BulkMarketExitService` live | ✅ lots closed |
| DA 2026-09-09 remaining dummy_sim lots | compose `SignalEvaluation` | ✅ no stop_out (above 2N) |
| DA 2026-09-10 | parquet session bars | ❌ none yet |
| Walnut DBC 09-09 replay | polluted by 09-10 lots | ⚠️ do not Confirm-book |
| Browser desk Confirm | not exercised on a new DA draft | ⚠️ |

**Test command(s):**

```bash
cd /home/johnkoisch/Documents/com/sawtooth/.worktrees/wv2-da-hitl
RAILS_ENV=test TEST_DB_HOST=127.0.0.1 PGPORT=5434 bundle exec rspec \
  spec/services/operations/working_stop_signal_spec.rb \
  spec/services/operations/signal_evaluation_open_position_spec.rb \
  spec/services/operations/eod_cadence_spec.rb \
  spec/services/operations/task_generator_stop_out_spec.rb \
  spec/services/operations/protective_gtc_guard_spec.rb \
  spec/services/operations/journal_confirmation_service_spec.rb \
  spec/requests/operations_desk_workflow_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added.
- **Services:** existing compose; `winston_v2` restarted so bind-mount picked up checked-out DA-stop files.
- **Migrations:** test DB migrated `20260909180000_create_session_order_slates` from **slate** (shared test PG). Integration worktree has dirty `db/schema.rb` from that — **do not commit**.
- **Capital:** paper books mutated (AMCR, WEAT, 30 stacks). Not production.

---

## 9. Risks & Technical Debt

- Wv2 `main` index mixes DA-stop checkouts with slate/WQ/MACD dirty files. Easy to `git add` the wrong tree.
- Compose is running DA-stop code from the dirty working tree, not from a clean `main` commit.
- 2026-09-10 GTC hits (OIH/REMX/VXX) are **intraday Yahoo**, not parquet. EOD may differ.
- Walnut DBC stop moved to **33.06** after 09-10 pyramid; dummy-sim Confirm must stay blocked.
- CONTEXT vs ADR-009 wording drift until an addendum.
- DA not point-in-time: historical `report_date` evals see current lots.

---

## 10. Open Questions

- **Merge strategy for `fix/da-working-stop-hitl` vs dirty slate `main`?** — operator; blocks landing on origin/main.
- **Confirm 09-10 OIH/REMX/VXX on dummy_sim as soon as parquet lands, or wait for scheduled DAR?** — operator; blocks HITL proof.
- **ADR-009 addendum now or later?** — architecture; does not block engine.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Wrap complete. Engine + ADR-009 on origin `main`. 09-10 parquet still missing.
- **Next concrete step:** When DM parquet has 2026-09-10, run DA; Confirm dummy_sim stop-outs for OIH/REMX/VXX; **do not** dummy-sim Walnut DBC.
- **Files to read first:**
  1. `winston_v2/docs/issues/2026-09-09-da-20day-exit-under-max-lots.md`
  2. `app/services/operations/working_stop_signal.rb`
  3. `ecosystem/CONTEXT.md` Working Stop / Unsignaled (on docs branch)
  4. This report

---

## 12. Stakeholder Communications

- Operator already has the recast explanation. No external email required. Optional `/stakeholder` if sharing the paper-HITL = live-methodology decision.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, manage-issue-ticket (initial file), session-report, wrap.
- **What worked well:** Disjoint worktrees (engine / tasking / desk / docs) merged with **zero** conflicts; 76 specs green before compose checkout.
- **Friction points:** `spawn_subagent` `cwd` + `isolation=worktree` are mutually exclusive — created worktrees by hand. Compose bind-mounts **main**, not worktrees. Dirty `main` made landing unsafe.
- **Subagent usage:** docs, engine, tasking, desk (implement); remaining-lots + Walnut audit (explore). GC merged and added `ProtectiveGtcGuard`.

---

## 14. Follow-up Actions

- [x] ADR-009 addendum: computed Working Stop pierce is signaled — ecosystem `5c322b6` / wrap
- [x] Push/merge DA-stop onto `main` — Wv2 `2489897`+`8df584f`; ecosystem `84f8986`
- [x] Remove DA-stop worktrees
- [ ] Catchup DA + dummy_sim Confirm when 2026-09-10 parquet arrives (OIH #797/#384, REMX #798, VXX #308)
- [ ] Walnut GTC Accept-Fill proof (do not dummy-sim DBC) — existing ticket
- [ ] DA as-of open lots (ignore positions created after `report_date`)

---

## 15. Appendix

**GTC reconstruction (dummy_sim, first pierce):**

- Mint #797 AMCR 3×119u 2026-08-27 @ 45.75 (touch) j#1482–1484; j#1477 passed superseded
- Mint #797 WEAT 3×257u 2026-09-03 @ 26.81 (gap) j#1590–1592
- 30 stacks j#1593–1634 (Yellow IAU/SGOL/ANET; Orange AAPL/ZROZ/WMT/GLTR/NVDA; Rust DBA/DBE/BIS/AAAU/AFIF; Blue JNJ/AMZN/GLD/AAL/RXT/WMT; Mint#384 WEAT/APLD/ASTS/AMCR/UNG; Mango AAAU/BIB/ROKU/MSFT/WTI/SEF)

**2026-09-10 in-session (Yahoo, not parquet) likely GTC:** OIH 417.78 touch (Mint #797 and #384); REMX gap ~73.68; VXX short gap ~18.73.

**Worktrees:** removed after wrap. Leftover dirty files on both `main` working trees are WQ/slate/docs **not** from this session.
