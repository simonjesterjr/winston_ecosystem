# Session Report — Copper 794 Mode D paper book

**Date:** 2026-09-24
**Time:** ~12:50–13:20 MDT
**Duration:** ~30m
**Project:** sawtooth — ecosystem (record), winston_v2 (live paper book)
**Working directory:** /home/johnkoisch/Documents/com/sawtooth
**Branch:** main on ecosystem, winston_v2, and broker_gateway
**Model:** Grok 4.7
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Mint a new unbound Winston v2 (Wv2) paper Operational Portfolio from Winston Unit Test (WUT) Portfolio Backtest Run (PBR) #794 / Copper 413, as Mode D shares-only Turtle system 75 (TS75), without editing Mode C Copper #1581, without an Interactive Brokers (IBKR) bind, and without calling the heat knobs a win.

**Outcome:** Delivered.

**One-line summary:** Wv2 portfolio #1585 is an active dummy-sim Mode D Copper book at 1% risk and $30,000; Mode C Copper #1581 is unchanged.

---

## 2. Work Completed

- Mode D phases 0–1 were already on main (`winston_v2` `1582ecc`, `broker_gateway` `e4ef7fc`, ecosystem script in `27db407`). Specs re-run green: Wv2 14 examples, Broker Gateway 13 examples.
- Dry-run, then apply, of the cutover. New book **#1585** `Portfolio Copper · mode-d-from-wut-794`.
- Activation used `force: true` because the market set matches active Mode C Copper #1581. #1581 stayed active, Mode C, `leap_fulfillment=all`, risk 2%, `updated_at` `2026-09-21T20:37:39Z`.
- Probe-before-promote on PBR #794 passed. Prior dirty `probe-before-promote-last.*` files were copied aside and restored.
- `Operations::ModeD::TestDesk` walked #1585 inside a transaction and rolled back. The book still has 0 journals, 11 books, and no TST market.
- Jev scored the desk walk and the promote checkpoints above the 0.85 bar. Promote framing is `mode_d_shares_candidate` at confidence 1.
- Host smoke: the running Wv2 process (container SHA `1582ecc`) serves `/operations/portfolios/1585` as Mode D and `/operations/portfolios/1581` as LEAP-preferred. `GET /internal/portfolios` lists #1585 and still omits `fulfillment_mode`.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/analysis/2026-09-24-copper-794-mode-d-cutover.rb` | added | Mint script. Default is dry-run. `APPLY=1` writes. |
| `ecosystem/docs/analysis/2026-09-24-copper-794-mode-d-cutover.json` | added | Apply report |
| `ecosystem/docs/analysis/2026-09-24-copper-794-probe.json` | added | PBR 794 probe |
| `ecosystem/docs/analysis/2026-09-24-copper-794-probe.md` | added | Same probe, markdown |
| `ecosystem/docs/analysis/2026-09-24-copper-794-probe-jev.json` | added | Smell nouls |
| `ecosystem/docs/analysis/2026-09-24-copper-794-mode-d-uat-state.txt` | added | Desk walk transcript |
| `ecosystem/docs/analysis/2026-09-24-copper-794-mode-d-uat-jev.json` | added | Desk nouls |
| `ecosystem/docs/analysis/2026-09-24-copper-794-mode-d-harness-state.txt` | added | Promote checkpoint state |
| `ecosystem/docs/analysis/2026-09-24-copper-794-mode-d-harness-jev.json` | added | Promote answers |
| `ecosystem/docs/tickets/archive/2026-09-24-copper-794-mode-d-paper-bind.md` | moved | Done |
| `ecosystem/docs/tickets/INDEX.md` | modified | Active row removed |
| `ecosystem/plans/copper-794-mode-d-paper-bind.md` | modified | Status Done |
| `ecosystem/docs/tickets/2026-09-24-mode-d-phase-2.md` | modified | Names #1585 |
| `ecosystem/docs/tickets/2026-09-24-mode-d-phase-2-paper-send.md` | modified | Names #1585; send still blocked |
| This report | added | |

No Winston v2 or Broker Gateway source edit this session. The book is a database row.

### Commits

- Prerequisite already on main before this mint: `1582ecc` (Wv2), `e4ef7fc` (Broker Gateway), `27db407` (ecosystem phase 0–1 record).
- This session's ecosystem commit is recorded in the wrap reply.

### Branch / PR state at sign-off

- Branch: `main` — pushed with this wrap
- PR: not opened

---

## 4. Decisions Made

### Decision 1: New book, not a conversion of #1581
- **Choice:** Insert portfolio #1585. Leave #1581's row alone.
- **Why:** Different risk (1% vs 2%), different instrument (shares vs LEAP), and the operator lock.
- **Alternatives considered:** Flip #1581's policy to `mode_d`. Rejected.
- **Reversibility:** easy (deactivate or close #1585). #1581 was not rewritten.
- **Promote to ADR?** no

### Decision 2: Activate beside #1581 with force
- **Choice:** `PortfolioActivationService.activate!(force: true)`. Conflict reason `identical_books` against #1581 only.
- **Why:** The plan says activate. The books are the same eleven symbols, so the mutex would block. Seed name is the full Mode D name, so there is no seed clash.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Do not write heat onto Trading Strategy #341
- **Choice:** Caps 3 and 10 on the portfolio. Runtime heat comes from `Operations::PortfolioHeat` inference (3 / 6 / 10 / 10 at 1%) because #341 has no heat hash and the Copper books already have a correlation snapshot.
- **Why:** #341 is shared by the Mode C books. Writing heat there would change Blue, Mango, Orange, Indigo, Teal, Slate, and Copper #1581.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 4: Roll back the test-desk bookings
- **Choice:** Walk `Operations::ModeD::TestDesk` on #1585, write the transcript, roll the transaction back.
- **Why:** The walk books TST shares and a covered call. Leaving them would engage the paper book before any real signal.
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- `GET /internal/portfolios` still returns only id, name, active, markets, and capital base. Grok Bot cannot see Mode D on #1585 from that list. The portfolio page can.
- Compose still reports Winston v2 as `starting` while the portfolio page returns HTTP 200. Do not treat `starting` as down.
- Inferred heat labels its source `pcs_copy` because the pair map came from the correlation snapshot. The numbers themselves are the cap inference (market 3, direction 10, close 6, loose 10), not a hash stored on the strategy.
- WUT stores risk as a fraction (`0.01`). Wv2 stores it as percent points (`1.0`). The sizer treats `1.0` as 1%.

---

## 6. Issues & Tickets

### Resolved this session
- `2026-09-24-copper-794-mode-d-paper-bind` — Done, moved to `docs/tickets/archive/`.

### Deferred
- Clickable desk walk — already `2026-09-24-mode-d-phase-2-desk-walk.md`.
- Portfolio list `fulfillment_mode` — already `2026-09-24-mode-d-phase-2-portfolio-list-mode.md`.
- One paper covered-call send — already `2026-09-24-mode-d-phase-2-paper-send.md`. Book id is now #1585. Fingerprint on strategy #341 is null. Binding is still unset. Send stays blocked.
- Assignment replace — already `2026-09-24-mode-d-phase-2-assignment-replace.md`.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Mode D specs | rspec on Wv2 test DB | ✅ 14 examples, 0 failures |
| Covered-call + LEAP specs | rspec on Broker Gateway test DB | ✅ 13 examples, 0 failures |
| PBR 794 probe | `probe_before_promote.sh 794` | ✅ overall pass; smell nouls 0.06 / 0.03 / 0.06 |
| Desk walk | TestDesk on #1585, then rollback | ✅ facts match; 0 journals left |
| Desk Jev | `mode_d_uat_jev.sh` | ✅ 0.87, 0.98, 0.98, 0.88, 0.96 |
| Promote Jev | five checkpoints | ✅ nouls 0.98, 0.99, 0.97, 0.96; choice `mode_d_shares_candidate` confidence 1 |
| Packaging | selector on #1585 | ✅ 237 long → 200 stock; 80 short → 80 stock |
| #1581 untouched | row snapshot | ✅ Mode C, risk 2.0, updated_at unchanged |
| Running Wv2 | curl portfolio pages | ✅ #1585 Mode D, #1581 LEAP-preferred |
| Daily Analysis job | not run | ⚠️ selector smoke only, so no Telegram and no task expiry |
| IBKR | not called | ✅ out of scope |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/services/operations/mode_d_test_desk_spec.rb \
  spec/services/operations/covered_call_overlay_tasks_spec.rb
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=bg_postgres broker_gateway \
  bundle exec rspec spec/services/adapters/ibkr/covered_call_candidates_spec.rb \
  spec/services/adapters/ibkr/leap_candidates_spec.rb
./bin/compose exec -T -e APPLY=1 winston_v2 bin/rails runner tmp/2026-09-24-copper-794-mode-d-cutover.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none added
- **Services:** existing compose stack. No restart. Winston v2 and Broker Gateway source is bind-mounted, so the running process already had phases 0–1 (`1582ecc` / `e4ef7fc`).
- **Migrations:** none
- **Data:** Wv2 development database gained portfolio #1585, 11 books, and one initial cash event of $30,000. No journals.

---

## 9. Risks & Technical Debt

- #1585 and #1581 are both active on the same markets. Daily Analysis can draft both. That was the point of a parallel book; it is also an attention split.
- Heat on #1585 is inferred, not a stored hash on the strategy. A later edit that puts a different heat hash on Trading Strategy #341 would override this book's caps-based knobs for every book on #341.
- `GET /internal/portfolios` still hides the mode.
- The test-desk proof is a transcript, not rows left on the book.

---

## 10. Open Questions

- **Which paper binding, if any, should #1585 use?** — needs answer from: operator; blocks: the phase 2 paper send.
- **Should both Copper books stay active through the next Daily Analysis?** — needs answer from: operator; blocks: nothing in this ticket. Deactivate only if the dual-active attention is unwanted.

---

## 11. Handoff & Resume Notes

- **Where I left off:** #1585 is active, unbound, empty of journals. Ticket archived.
- **Next concrete step:** Phase 2 clickable desk walk on #1585. Do not send an order. Do not edit #1581.
- **Files to read first:**
  1. `ecosystem/docs/tickets/2026-09-24-mode-d-phase-2.md`
  2. `ecosystem/docs/analysis/2026-09-24-copper-794-mode-d-cutover.json`
  3. `http://127.0.0.1:3002/operations/portfolios/1585`

**Resume hint for a new session:**

> Mode D paper book is Winston v2 #1585, dummy_sim, unbound, leap_fulfillment none, fulfillment_mode mode_d, TS #341, 1%, caps 3/10, $30k. Do not edit Mode C Copper #1581. Do not IBKR-bind until the operator names a binding. Portfolio list still omits fulfillment_mode.

---

## 12. Stakeholder Communications

- Operator: the new book is #1585. It is not the Mode C Copper book. Heat did not improve Edge (R). Nothing was sent to IBKR. Grok Bot's portfolio list still cannot see the mode; the portfolio page can.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, typesafe-ai (`jev ask`), session-report, wrap
- **Graphify Graph:** `graphify update ./ecosystem` rebuilt the code graph (no LLM): 12833 nodes, 14615 edges, 930 communities. Doc/paper semantic extraction was not run. Workspace merge of the five existing graphs (ecosystem, data_manager, winston_unit_test, broker_gateway, ai) wrote `graphify-out/graph.json` (18906 nodes, 23323 edges). `winston_v2/graphify-out/graph.json` is missing — omitted, no full rebuild. Graphs were not staged.
- **Ponytail flags:** No new heat column and no clone of Trading Strategy #341. The cutover reuses portfolio caps plus `Operations::PortfolioHeat` inference. Close 6 and loose 10 are the existing hardcoded inference, which happens to match the #794 knobs when caps are 3 and 10.
- **What worked well:** Fail-closed compare of the #1581 snapshot inside the same transaction as the insert.
- **Friction points:** `probe_before_promote.sh` always overwrites `probe-before-promote-last.*`. Those files were already dirty, so this run copied them aside and restored them.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [x] Clickable desk, portfolio-list field, assignment replace, and paper send — already filed under phase 2. Paper send now names #1585 and stays blocked.
- [ ] Operator decides whether #1585 and #1581 should both stay active into the next Daily Analysis — owner: operator

---

## 15. Appendix

### Jev System One — probe (PBR 794)

Questions (yes is a failure):

1. heat_label_lie — heat labeled turtle while the hash is missing or heat is off?
2. cap_breach — peak open above the portfolio cap?
3. zero_contracts — packaging prefers a call while the contract floor is 0?

Answers: 0.06, 0.03, 0.06.

### Jev System One — desk walk

State file: `docs/analysis/2026-09-24-copper-794-mode-d-uat-state.txt`

Answers: call_on_opt_in_only 0.87, not_on_entry 0.98, paired_unwind 0.98, three_lots_each 0.88, short_has_no_call 0.96.

### Jev System One — promote

State file: `docs/analysis/2026-09-24-copper-794-mode-d-harness-state.txt`

Answers: not_mode_c 0.98, mode_d_flag 0.99, dna_match 0.97, desk_uat 0.96, promote_framing `mode_d_shares_candidate` confidence 1.0.

### Host

```text
action: mint Mode D paper OP from PBR 794
ids: [1585]
sha: winston_v2 1582ecc; broker_gateway e4ef7fc
kept: 1581 updated_at 2026-09-21T20:37:39Z leap_fulfillment=all fulfillment_mode=mode_c risk=2.0
status: active dummy_sim unbound journals=0 capital_base=30000
errors: none
```
