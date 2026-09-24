# Session Report — Capital Fit beside Turtle sizing

**Date:** 2026-09-24
**Time:** 2026-09-23 – 08:54 MDT (session crossed midnight; start hour not recorded)
**Duration:** multi-hour
**Project:** sawtooth — Winston v2, Winston Unit Test, ecosystem
**Working directory:** /home/johnkoisch/Documents/com/sawtooth
**Branch:** `main` on winston_v2, winston_unit_test, and ecosystem (each its own git repo; all tracking `origin/main`)
**Model:** Grok 4.7
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Confirm the Teal USDU 2,872-share paper trade is a tiny Average True Range (ATR) stop, not a broken multiply, and put limits beside Turtle sizing so one fill cannot spend the book and later lots can still diversify.

**Outcome:** Delivered

**One-line summary:** Capital Fit caps the cash a new enter may spend. The first lot on an empty book is at most 1/portfolio-cap of today's cash and equity. A stop so tight that the capped shares cannot fund 0.20% of equity is passed. Winston Unit Test uses the same curve with short-capacity leverage, not 3× borrowing for longs.

---

## 2. Work Completed

- Confirmed Teal journal 2029: `floor(2% × $28,727.88 / $0.20) = 2,872` shares at $26.65, debit $76,538.80, free cash to about −$47,649. Indigo 2,809 shares is the same pattern. Heat counted each add as one unit.
- Operator amendments: the equal slice is for the first open lot only; the 3rd and the 11th must not stay on remaining-slots division; a later trade may consume remaining buying power. Small ATR gets a max share function. Winston Unit Test (WUT) gets a Portfolio Backtest Run (PBR) peer, not a shared singleton. `max_leverage` 3× is short capacity, not long borrowing.
- Shipped `Operations::CapitalFit` on Winston v2 (Wv2): draft task generator, confirm guard, pass reason `capital_fit`, Justification line.
- Shipped `PortfolioBacktest::CapitalFit` on WUT: entry estimator, single-market sizer when it sizes itself, long buying power uses tradeable cash.
- Updated the capital-consumption ticket to Done, the 22 September autopsy addendum, and the Capital Fit glossary sentence in `CONTEXT.md`.
- Did not flatten the open Teal or Indigo USDU lots. "Books healthy" stays held.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/app/services/operations/capital_fit.rb` | added | Diversity divisor, small-ATR max, notional cash |
| `winston_v2/app/services/operations/task_generator.rb` | modified | Fit after packaging; pass deletes the draft |
| `winston_v2/app/services/operations/journal_confirmation_service.rb` | modified | Cash hard stop; slice resize; force+note cannot overdraft |
| `winston_v2/app/services/operations/pass_signal_service.rb` | modified | Reason `capital_fit` |
| `winston_v2/app/models/passed_signal.rb` | modified | Description |
| `winston_v2/app/services/operations/mid_month_scoreboard_builder.rb` | modified | Algorithmic pass kind |
| `winston_v2/app/controllers/operations/desk_workflows_controller.rb` | modified | `force` stamped into confirm details |
| `winston_v2/app/views/operations/desk_workflows/_justification.html.erb` | modified | Capital fit line |
| `winston_v2/spec/services/operations/capital_fit_spec.rb` | added | Teal numbers and seat curve |
| `winston_v2/spec/services/operations/journal_confirmation_service_spec.rb` | modified | Refusal and slice book; seed date fixed |
| `winston_v2/spec/services/operations/task_generator_journal_flow_spec.rb` | modified | Flow signs kept; notionals are fitted |
| `winston_unit_test/app/services/portfolio_backtest/capital_fit.rb` | added | Peer; short room argument |
| `winston_unit_test/app/services/portfolio_backtest/entry_requirement_calculator.rb` | modified | Fit before cash check; calls capped on premium |
| `winston_unit_test/app/services/portfolio_backtest/entry_pass_reason.rb` | modified | `capital_fit` |
| `winston_unit_test/app/services/portfolio_backtest_runner.rb` | modified | Record the pass; book the checked share count |
| `winston_unit_test/app/services/position_manager.rb` | modified | Single-market fit; longs spend tradeable cash |
| `winston_unit_test/app/models/passed_signal.rb` | modified | Description |
| `winston_unit_test/spec/services/portfolio/capital_fit_spec.rb` | added | Curve, short room, restricted short proceeds |
| `winston_unit_test/spec/services/portfolio/entry_requirement_calculator_spec.rb` | modified | Slice and pass cases |
| `winston_unit_test/spec/services/position_manager_fill_relative_stop_spec.rb` | modified | Expected shares follow the pyramid cap |
| `winston_unit_test/spec/services/position_manager_park_pyramid_spec.rb` | modified | Stub includes `current_leverage` |
| `ecosystem/CONTEXT.md` | modified | Capital Fit glossary |
| `ecosystem/docs/analysis/2026-09-22-wv2-dar-paper-trade-autopsy.md` | modified | 2026-09-23 addendum |
| `ecosystem/docs/tickets/2026-09-22-min-atr-capital-consumption-guard.md` | modified | Status Done, locked rule |
| `ecosystem/docs/tickets/INDEX.md` | modified | Ticket row Done |

Not staged: `winston_v2/.grok/skills/ponytail-apply/`, `winston_unit_test/graphify-out/`, and the large unrelated ecosystem dirty tree.

### Commits

- `winston_v2` `b70de10` — Cap new enters with Capital Fit beside Turtle sizing.
- `winston_unit_test` `8e8d07f` — Fit backtest entries to cash and a fading diversity reserve.
- `ecosystem` — this report, the two follow-up tickets, the locked capital-consumption ticket, the autopsy addendum, and the Capital Fit glossary sentence (commit at wrap).

### Branch / PR state at sign-off

- Branch: `main` on all three repos
- Pushed: wrap push follows this commit
- PR: not opened. Work landed on `main` directly.

---

## 4. Decisions Made

### Decision 1: Capital Fit sits beside the Turtle sizer
- **Choice:** `signal_share_units` stays the Turtle integer. Capital Fit only reduces the booked size or passes.
- **Why:** The 2,872 share count was correct Turtle math. The hole was cash.
- **Alternatives considered:** Rewriting the sizer; a raw minimum ATR in dollars; refusing whenever the clip keeps under 25% of the Turtle unit.
- **Reversibility:** easy
- **Promote to ADR?** no — glossary sentence is enough; the gate is reversible

### Decision 2: Diversity reserve fades
- **Choice:** First lot divisor = portfolio cap (12 → 1/12). Each open lot retires `market_cap` seats (4). Third lot divisor is 4. Eleventh lot divisor is 1 and may consume remaining buying power.
- **Why:** Operator: the equal-slice rule is right for the first position and wrong for the third and the eleventh. A trade may consume the book once diversity has started.
- **Alternatives considered:** Divide by remaining slots for every add; only rule-1 cash solvency.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Small-ATR max, then a floor
- **Choice:** `min(turtle shares, floor(budget / price))`. If that clip cannot fund 0.20% of equity at the stop, pass (`min_slot_risk`). The floor applies only when the budget clip is what shrank the Turtle count.
- **Why:** An 89-share USDU lot risks about $18. Ordinary names with a few-percent stop stay as a real small position.
- **Alternatives considered:** Always book the dust clip; pass when expressed risk is under 25% of the Turtle unit (that would skip ordinary Plan C stocks on an empty 12-slot book).
- **Reversibility:** easy (constant `MIN_SLOT_RISK_FRACTION = 0.002`)
- **Promote to ADR?** no

### Decision 4: Two peers, not a singleton
- **Choice:** `Operations::CapitalFit` and `PortfolioBacktest::CapitalFit` duplicate the divisor and the max-share function. Buying power is the caller's job.
- **Why:** Operator: PBRs and Wv2 paper/real books are different. A 3× lab multiple is short capacity. Wv2 longs cannot debit free cash below zero. Short-sale proceeds are not tradeable cash.
- **Alternatives considered:** One shared Ruby object; enforcing stored `max_leverage` 3× as gross long room (that would still have allowed Teal).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 5: Do not flatten the live lots
- **Choice:** Forward gate only.
- **Why:** Already-executed journals are operator books. Negative free cash then blocks new longs by rule 1.
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Identity: `notional / equity = risk% / (stop distance / price)`. USDU's 0.75% stop at 2% risk wants 2.66× equity for one unit. A ~5% stop still wants about 40% of equity. The first-lot 1/12 cap binds on ordinary stock, not only USDU.
- Wv2 `PositionSizer` clamped only at 10,000 shares. `insufficient_cash` existed as a pass reason and was not applied on Daily Analysis or confirm.
- WUT portfolio path cash-checked the full Turtle notional and skipped the name. The single-market `PositionManager` allowed cash to go negative up to `(max_leverage − 1) × equity`. Teal/Indigo were cut over with `max_leverage: 3.0`, so 2.66× would still have fit under a gross 3× ceiling.
- The rows extract stop of 26.38 does not reproduce 2,872. The booked count matches the $0.20 stop in the autopsy.

---

## 6. Issues & Tickets

### Resolved this session
- `ecosystem/docs/tickets/2026-09-22-min-atr-capital-consumption-guard.md` — locked and implemented. Status Done.

### Deferred
- Open Teal (1584) and Indigo (1583) USDU lots still overdraft free cash. The gate does not flatten them. Needs an operator flatten or cash decision.
- Broker Special Memorandum Account / buying power remains `ecosystem/plans/spending-capacity-and-leap-fulfillment.md` and ticket `2026-09-04-tf-p3-live-sizing-and-capital-authority.md`. Capital Fit does not close that ticket.
- Desk Justification Capital fit line was not clicked in a browser.
- New PBR paths will size smaller than stored historical runs. Old result JSON was not rewritten.
- Single-market long buying-power change (no borrow) is covered by the code path; the fill-relative spec stubs `check_leverage_constraint`, so that branch has no direct example.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Wv2 Capital Fit math | rspec `capital_fit_spec` | ✅ |
| Wv2 confirm refusal, force cannot overdraft, slice book | rspec `journal_confirmation_service_spec` | ✅ |
| Wv2 draft flow signs after fit | rspec `task_generator_journal_flow_spec` plus heat, cadence, stop-out generators | ✅ |
| Wv2 Turtle sizer unchanged | rspec `position_sizer_spec` | ✅ |
| WUT Capital Fit, estimator, fill-relative stops, pass reasons, pyramid naming | rspec listed below | ✅ |
| Desk Justification in a browser | not driven | ⚠️ |
| Live Teal/Indigo books after the gate | not re-run Daily Analysis | ⚠️ |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/services/operations/capital_fit_spec.rb \
  spec/services/operations/position_sizer_spec.rb \
  spec/services/operations/journal_confirmation_service_spec.rb \
  spec/services/operations/task_generator_journal_flow_spec.rb \
  spec/services/operations/task_generator_heat_spec.rb \
  spec/services/operations/task_generator_eod_cadence_spec.rb \
  spec/services/operations/task_generator_stop_out_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wut_postgres winston_unit_test \
  bundle exec rspec spec/services/portfolio/capital_fit_spec.rb \
  spec/services/portfolio/entry_requirement_calculator_spec.rb \
  spec/services/portfolio/entry_pass_reason_spec.rb \
  spec/services/position_manager_fill_relative_stop_spec.rb \
  spec/services/position_manager_park_pyramid_spec.rb \
  spec/services/position_manager_leap_journal_spec.rb
```

Last green runs: Wv2 confirm+fit+flow 33 examples; WUT capital fit + estimator + pass reasons + fill-relative 26 examples on the first combined run; park pyramid 8 examples after the leverage stub fix. Leap journal specs were in a run that failed only on a missing `OpenStruct` require when those files loaded alone; they passed once `ostruct` was loaded by a sibling spec. Not re-run as a named green file after that.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none added
- **Services:** existing compose used only to exec rspec (`winston_v2`, `wv2_postgres`, `winston_unit_test`, `wut_postgres`)
- **Migrations:** none
- **Data:** no live journal amended

---

## 9. Risks & Technical Debt

- Two copies of the divisor and max-share function can drift. Operator asked that they not be one singleton.
- New backtests will not match old share counts on tight-stop names. Stored PBR results are unchanged until someone re-runs them.
- Confirm sizes cash as of `Date.current`. A test that rewinds `Date.current` to before the seed deposit sees an empty book. The confirmation spec seeds cash on 2020-01-01 for that reason.
- While Teal and Indigo free cash stay negative, rule 1 blocks every new long on those books.
- `max_leverage` column on the live books is still 3.0 and is still unread by Wv2. WUT no longer treats it as long borrowing.

---

## 10. Open Questions

- **What to do with the open USDU lots?** — needs answer from: operator; blocks: those two books taking another long.
- **When to say the paper books are healthy?** — needs answer from: operator after the lots are dealt with and a Daily Analysis no longer drafts 2,872 shares.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Code and specs are green on the commands above. Nothing committed. Graphify refresh finished (see §13). Follow-up promotion is waiting on the operator before commit.
- **Next concrete step:** Operator chooses flatten vs leave on Teal 1584 and Indigo 1583 USDU, then a Daily Analysis smoke on a fresh signal.
- **Files to read first:**
  1. `winston_v2/app/services/operations/capital_fit.rb`
  2. `winston_unit_test/app/services/portfolio_backtest/capital_fit.rb`
  3. `ecosystem/docs/tickets/2026-09-22-min-atr-capital-consumption-guard.md`
  4. `ecosystem/docs/analysis/2026-09-22-wv2-dar-paper-trade-autopsy.md` (addendum)

---

## 12. Stakeholder Communications

- Hold any "books healthy" or "workflow smooth means the books are fine" wording. Cash arithmetic on the 22 September journals can be described as matching the booked units. Teal and Indigo can still show negative free cash from one USDU lot until an operator acts.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator prose (during the build), session-report, wrap, graphify-ponytail (wrap step 2)
- **Graphify Graph:** updated `ecosystem/graphify-out` (12,687 nodes) and `winston_unit_test/graphify-out` (4,578 nodes). `winston_v2/graphify-out/graph.json` is missing — no full rebuild. Merged workspace graph from ecosystem, data_manager, winston_unit_test, broker_gateway, and ai (winston_v2 omitted) → `graphify-out/graph.json` (18,744 nodes). Not staged.
- **Ponytail flags:** WUT graph shows `PortfolioBacktest::CapitalFit` called from `EntryRequirementCalculator#fit_to_capital` and `PositionManager#single_market_capital_fit` — two call sites, one lab owner. The same `assess` / `diversity_divisor` / `spending_base` math is copied in `Operations::CapitalFit` on Winston v2, which this graph cannot see. Operator asked that they stay peers, not one singleton. No harmonize during wrap. God nodes unchanged (PortfolioBacktestRunner still the hub).
- **What worked well:** The autopsy formula reproduced 2,872 before any code. Operator amendments changed the divisor from "remaining slots forever" to a fading reserve without a new column.
- **Friction points:** Confirmation specs rewind `Date.current` or use large explicit share counts. The gate had to use today's cash and a cap of 1 in the column-identity examples so those tests still check fill columns rather than the slice.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Operator: flatten or fund Teal portfolio 1584 and Indigo portfolio 1583 USDU lots — ticket: [`../tickets/2026-09-24-teal-indigo-usdu-overdraft.md`](../tickets/2026-09-24-teal-indigo-usdu-overdraft.md)
- [ ] Click the desk Justification Capital fit line on a fitted draft — ticket: [`../tickets/2026-09-24-desk-capital-fit-justification-check.md`](../tickets/2026-09-24-desk-capital-fit-justification-check.md)
- [x] Broker buying power / Special Memorandum Account stays on the spending-capacity plan — already filed: `2026-09-04-tf-p3-live-sizing-and-capital-authority.md`. Not re-filed.
- [ ] Optional WUT lab spec (not an Interactive Brokers user-acceptance test): one `PositionManager` example that a 3× book cannot borrow for a long. Not filed. Owner: next session if wanted.

---

## 15. Appendix (optional)

Teal empty-book numbers used in specs: free cash $28,890, risk equity $28,727.88, price $26.65, stop $0.20, caps 4 and 12. First-lot budget is equity/12. Fit shares at that stop fail the 0.20% floor and pass. A $3 stop on the same price clips and books.

Diversity divisor (`book_cap` 12, `market_cap` 4): filled 0 → 12, filled 1 → 8, filled 2 → 4, filled 10 → 1.
