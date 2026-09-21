# Session Report — Mode C furthest-call desk UAT (SEF / BITQ)

**Date:** 2026-09-21
**Time:** ~morning UAT through wrap 14:57 MDT
**Duration:** ~session (continuation of Mode C paper LEAP / standard_call desk)
**Project:** Sawtooth / Winston ecosystem (cross-monolith)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` `main` (dirty); `broker_gateway` `main` (dirty); `ecosystem` `main` (ahead 1, dirty). Workspace root is **not** a git repo.
**Model:** Grok 4.6
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Relax open-interest / spread screens for journal **1943** (Mango / SEF) so Desk shows Plan B; dump the full SEF chain; then lock **furthest listed expiry** as Winston call law (cash cut, not risk haircut); then get BITQ **1946** onto the same ladder. Agent never Desk-Sends options.

**Outcome:** Delivered for desk packaging + UAT confirms. Working Stop on the two option fills is **wrong** (premium geometry). Wrap commits pending operator follow-up promotion.

**One-line summary:** Plan B is now the furthest listed call below the LEAP floor at `floor(shares/100)` contracts; SEF 1943 and BITQ 1946 confirmed as paper standard calls; 8%/200 was hiding those names until Mode C paper books got UAT knobs.

---

## 2. Work Completed

- Confirmed Client Portal Gateway (CPGW) brokerage session HTTP 200; walked **SEF** (Nov + Feb) and **BITQ** (Oct, Nov, Jan, Apr) listed call surfaces.
- Relaxed Mango #1577 `min_open_interest=0`, `max_spread_pct=5.0` so SEF Nov 29C could pass; later applied the same knobs to **all** `dummy_sim` + `leap_fulfillment=all` paper books (not a second one-off).
- Operator lock: furthest expiry in the rung window; `risk_mult` 1.0 on both call rungs; `max_dte` 120 removed (window is `[21, leap_min_dte)`).
- Desk form: Units/banner/price for option Plan B are **contracts and premium**, not leftover share units (491 contracts / $30.54 bug). Justification label **Signal size** (not Risk units); right-to-buy copy.
- Overlay GET re-resolves Plan C drafts; packaging stamp keys replaced so leftover `fulfillment_plan_c=stock` cannot pin Plan C after a live call appears.
- Confirm flash for journal #X is dropped on a different workflow GET; ops shell now renders flash.
- Operator confirmed: **1943** SEF 4× Feb 19 2027 30C @ 1.375 (−$550); **1944** BFIX 2373 sh stock (no chain); **1946** BITQ 2× Apr 16 2027 28C @ 4.75 (−$950). **1941** SMH 17 sh stock already executed (`zero_contracts`).
- ADR-018 addendum 2026-09-21; CONTEXT Plan B / Justification glossary.

---

## 3. Code Delivered

### Files changed (this wrap’s intended commit set)

**winston_v2** (`main`, uncommitted)

| File | Change | Notes |
|------|--------|-------|
| `app/controllers/operations/desk_workflows_controller.rb` | modified | contract/premium prefill; overlay stamp replace; drop foreign confirm flash; always re-resolve dummy_sim drafts |
| `app/services/operations/desk_action_handoff.rb` | modified | option-like units/premium beat share handoff |
| `app/services/operations/fulfillment_packaging_policy.rb` | modified | `max_dte` nil→364; `risk_mult` 1.0 |
| `app/services/operations/call_fulfillment_selector.rb` | modified | furthest DTE first on leap + standard pick |
| `app/views/operations/desk_workflows/show.html.erb` | modified | Plan B N contracts; units hint; turbo-temporary flash |
| `app/views/operations/desk_workflows/_justification.html.erb` | modified | Signal size; right-to-buy; floor(shares/100) |
| `app/views/operations/home/index.html.erb` | modified | ops shell flash |
| `spec/requests/desk_workflow_plan_c_overlay_spec.rb` | added | Plan B prefill; Plan C re-resolve; foreign flash |
| `spec/services/operations/call_fulfillment_selector_spec.rb` | modified | Dec 18 IBM furthest eligible |
| `spec/services/operations/fulfillment_packaging_selector_spec.rb` | modified | 2 contracts; furthest OCC |
| `spec/integration/mode_c_leap_untradeable_fallback_spec.rb` | modified | Signal size; Plan C banner on empty chain |

**broker_gateway** (`main`, uncommitted)

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/ibkr/leap_candidates.rb` | modified | `pick_month` furthest in [min,max]; fixture furthest expiry |
| `spec/services/adapters/ibkr/leap_candidates_spec.rb` | modified | SEF NOV26 vs FEB27; JAN29 vs DEC28 |

**ecosystem** (`main`, uncommitted this slice)

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | Plan B furthest expiry; Signal size beat |
| `docs/adr/ADR-018-mode-c-leap-plan-a-plan-b.md` | modified | 2026-09-21 addendum |
| `docs/session-reports/2026-09-21-1457-mode-c-furthest-call-desk-uat.md` | added | this report |

Other dirty trees on `winston_v2` / `broker_gateway` / `ecosystem` from **prior** Mode C waves (exit-at-stop, flatten tasks, OPT refuse, analysis probes) were **not** mixed into this wrap’s file list. They remain dirty on disk.

### Commits

- `winston_v2` `5b8bcdf` — feat(desk): furthest-call Plan B, contract prefill, live overlay
- `broker_gateway` `a0731fc` — feat(ibkr): pick furthest option month in the DTE window
- `ecosystem` `2bbaff3` — docs: furthest-call desk UAT wrap, ADR-018 lock, follow-up tickets

### Branch / PR state at sign-off

- Branch: each repo `main` (this slice committed; other dirty files left unstaged)
- Pushed: pending wrap push
- PR: not opened (push `main`)

---

## 4. Decisions Made

### Decision 1: Furthest listed expiry is Winston call law
- **Choice:** Plan A LEAP = furthest month ≥365 DTE; Plan B standard_call = furthest month in `[min_dte, leap_min_dte)`. No nearest-month walk. No 120-DTE cap.
- **Why:** Operator: reduce cash vs share signal, still participate in the trend, avoid theta. Options are not a risk substitute or augment.
- **Alternatives considered:** Keep 120-DTE “standard” window; target 730 then fallback; 0.6 haircut on short-dated calls.
- **Reversibility:** easy (policy knobs + `pick_month`).
- **Promote to ADR?** Done — ADR-018 addendum 2026-09-21.

### Decision 2: Contract count is `floor(signal_share_units / 100)` on both call rungs
- **Choice:** `risk_mult` 1.0 for standard_call (was 0.6).
- **Why:** Haircut fought furthest-tenor law. Cash cut is premium notional, not fewer contracts.
- **Alternatives considered:** Keep 0.6 for 60-DTE names.
- **Reversibility:** easy.
- **Promote to ADR?** Covered in the same addendum.

### Decision 3: 8%/200 quality screens relaxed on Mode C paper books for UAT
- **Choice:** `min_open_interest=0`, `max_spread_pct=5.0` on all dummy_sim + leap_fulfillment=all OPs. `STANDARD_DEFAULTS` in code still 200 / 0.08 for new books unless copied.
- **Why:** Thin ETF chains (SEF, BITQ) fail 8%/200 even when two-sided quotes exist.
- **Alternatives considered:** Change global STANDARD_DEFAULTS; Mango-only (rejected as one-off).
- **Reversibility:** easy (restore knobs on those OPs).
- **Promote to ADR?** no — UAT ops knob, not law.

---

## 5. Insights Surfaced

- Storing `max_spread_pct: nil` still merges to STANDARD_DEFAULTS **0.08** (`merge_knobs` skips nil).
- Desk GET overlay skipped when `fulfillment_type=stock` and Plan B/C already stamped — live chain/policy changes never reached 1946 until the skip was removed.
- Overlay `Hash#merge` kept leftover `fulfillment_plan_c=stock`, so `adopted_fulfillment_type` pinned Plan C even after a call resolved.
- Confirm flash lives in session; ops shell did not render it, so the next workflow GET showed “OK confirmed: journal #1944”.
- Fill-stop JS treats Price as underlying. After premium prefill, stop becomes `premium − 2N` (BITQ **$2.33**, SEF **$0.78**) instead of 2N under the stock.
- IBKR walker is still **ATM-3 of one month**. Full chain is operator-chat only.
- OCC / `localSymbol` still often the stock ticker (`SEF`, `BITQ`) — existing P2 ticket.

---

## 6. Issues & Tickets

### Resolved this session
- 1943 Plan B hidden by 8%/200 + nearest-month + overlay leftover leap — desk now furthest call.
- 1946 Plan C despite listed April calls — same screens + Plan C overlay skip.
- 491-contract banner / Units / $30.54 price on option Plan B.
- Foreign confirm flash on the next journal’s workflow page.

### Deferred
- **P0 Working Stop on option enter** — filed issue [`../issues/2026-09-21-option-enter-working-stop-from-premium.md`](../issues/2026-09-21-option-enter-working-stop-from-premium.md) + ticket [`../tickets/2026-09-21-option-enter-working-stop-underlying.md`](../tickets/2026-09-21-option-enter-working-stop-underlying.md).
- Restore vs keep Mode C paper OI=0 / spread 5.0 — left in report only (`skip`).
- Full listed chain on the desk — ticket [`../tickets/2026-09-21-desk-furthest-month-full-chain.md`](../tickets/2026-09-21-desk-furthest-month-full-chain.md).
- OCC vs ticker label — existing [`../tickets/2026-09-19-leap-instrument-label-occ-vs-ticker.md`](../tickets/2026-09-19-leap-instrument-label-occ-vs-ticker.md) (linked 2026-09-21 SEF/BITQ rows; not duplicated).
- Lane 2 option Desk-Send / Session Order Slate — parked (ADR-017, spending capacity, first paper Send operator-only) (`skip`).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Wv2 packaging + overlay + flash specs | `compose exec winston_v2 … rspec spec/requests/desk_workflow_plan_c_overlay_spec.rb spec/integration/mode_c_leap_untradeable_fallback_spec.rb spec/services/operations/call_fulfillment_selector_spec.rb spec/services/operations/fulfillment_packaging_selector_spec.rb` | ✅ 20+31 examples green (overlay+fallback 20; selector files separate) |
| BG LeapCandidates furthest month | `compose exec broker_gateway … rspec spec/services/adapters/ibkr/leap_candidates_spec.rb` | ✅ 9 examples |
| Live 1943 overlay | CPGW walk + rails selector + curl form | ✅ 4× SEF 2027-02-19 30C @ 1.375; operator confirmed |
| Live 1946 overlay | CPGW walk + rails selector + curl form | ✅ 2× BITQ 2027-04-16 28C @ 4.75; operator confirmed |
| Working Stop on those fills | `Position#updated_stop` | ❌ 0.78 / 2.33 (premium − ATR), not 2N under underlying |
| Browser UAT | operator screenshots + hard-refresh | ✅ Plan B form; ⚠️ flash until code restart |

**Test command(s):**

```bash
./bin/compose exec -T winston_v2 bash -lc 'RAILS_ENV=test TEST_DB_HOST=wv2_postgres bundle exec rspec spec/requests/desk_workflow_plan_c_overlay_spec.rb spec/integration/mode_c_leap_untradeable_fallback_spec.rb spec/services/operations/call_fulfillment_selector_spec.rb spec/services/operations/fulfillment_packaging_selector_spec.rb'
./bin/compose exec -T broker_gateway bash -lc 'RAILS_ENV=test bundle exec rspec spec/services/adapters/ibkr/leap_candidates_spec.rb'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added.
- **Services:** `winston_v2` and `broker_gateway` restarted; CPGW host Java pid 938121, auth/tickle HTTP 200; `LEAP_READ_BINDING_ID=bnd_3d6a5020d839c315583277d2`.
- **Migrations:** None this slice.
- **DB knobs:** all paper `dummy_sim` + `leap_fulfillment=all` OPs now `standard_call.min_open_interest=0`, `max_spread_pct=5.0`.

---

## 9. Risks & Technical Debt

- Booked SEF/BITQ Working Stops will look like immediate stop-outs if anything reads `updated_stop` as underlying GTC.
- UAT 8%/200 bypass is on every Mode C paper book, including Blue/Orange LEAP books.
- Overlay GET now hits CPGW on every dummy_sim enter draft load (including Plan C).
- `occ_symbol` often the root ticker — desk and Justification look unlabeled.

---

## 10. Open Questions

- **Correct 1943/1946 stops to 2N under underlying?** — operator; blocks honest paper stop-outs.
- **Keep OI=0 / spread 5.0 on Mode C paper after UAT?** — operator.
- **Should fill-stop JS ignore option Price and keep underlying ATR stop?** — yes by ADR-018 Working Stop law; not coded this wrap.

---

## 11. Handoff & Resume Notes

- **Where I left off:** 1946 confirmed; wrap report written; commits not yet made (follow-up promotion first).
- **Next concrete step:** Set BITQ #889 and SEF option lot Working Stops to 2N under the underlying (or Pass if the operator wants them left). Then commit this slice.
- **Files to read first:**
  1. `ecosystem/docs/adr/ADR-018-mode-c-leap-plan-a-plan-b.md` (2026-09-21 addendum)
  2. `winston_v2/app/controllers/operations/desk_workflows_controller.rb` (`overlay_packaging_on_draft!`, `form_fields` units/price)
  3. `broker_gateway/app/services/adapters/ibkr/leap_candidates.rb` (`pick_month`)
  4. `winston_v2/app/views/operations/desk_workflows/show.html.erb` (fill-stop JS vs option premium)

**Live books (do not Desk-Send):**

| Journal | Book | Fill |
|---------|------|------|
| 1941 | SMH / Orange #1576 | 17 sh stock @ 580.81, flow −9873.77 |
| 1943 | SEF / Mango #1577 | 4× Feb 19 2027 30C @ 1.375, flow −550, stop **0.78** |
| 1944 | BFIX / Rust #1578 | 2373 sh stock @ 24.70, flow +58613.1 (short) |
| 1946 | BITQ / Indigo #1583 | 2× Apr 16 2027 28C @ 4.75, flow −950, pos **#889**, stop **2.33**, capital_base 29050 |

Journal **1915** left untouched.

---

## 12. Stakeholder Communications

- Operator already ran the UAT confirms. No outward email.
- Next operator-facing item: the two option Working Stops.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report, graphify-ponytail, long-running-background-tasks, record (deferred to promotion).
- **Graphify Graph:** updated `broker_gateway/graphify-out` (749 nodes); updated `ecosystem/graphify-out` (14937 nodes); **winston_v2 `graphify-out/graph.json` missing** — did not silent full rebuild; workspace merge of 5 graphs (no Wv2) → `graphify-out/graph.json` 21126 nodes / 26012 edges. `graphify-out/` not staged.
- **Ponytail flags:** furthest-tenor now lives in **two** layers by design — `LeapCandidates#pick_month` (which month IBKR walks) and `CallFulfillmentSelector#pick_leap` / `#pick_standard` (which eligible row wins). Not a third helper. New `overlay_packaging_details` replaces merge-keep of Plan C stamps; do not reintroduce `Hash#merge` of packaging keys.
- **What worked well:** live CPGW month walk + rails selector stamp + curl form assertions before asking the operator to refresh.
- **Friction points:** `STANDARD_DEFAULTS` nil-merge; Plan C overlay skip; confirm flash vs ops shell; fill-stop JS vs option Price.
- **Subagent usage:** none this wrap.

---

## 14. Follow-up Actions

- [x] Correct Working Stops on SEF 1943 and BITQ 1946 (and stop the form from subtracting ATR from option premium) — **ticket** [`../tickets/2026-09-21-option-enter-working-stop-underlying.md`](../tickets/2026-09-21-option-enter-working-stop-underlying.md) + **issue** [`../issues/2026-09-21-option-enter-working-stop-from-premium.md`](../issues/2026-09-21-option-enter-working-stop-from-premium.md)
- [ ] Decide whether Mode C paper keeps OI=0 / spread 5.0 — owner: operator — due: after this UAT — **skipped filing**
- [x] Desk ATM-3 of furthest month — **ticket** [`../tickets/2026-09-21-desk-furthest-month-full-chain.md`](../tickets/2026-09-21-desk-furthest-month-full-chain.md)
- [x] OCC vs ticker label design session — **linked existing** [`../tickets/2026-09-19-leap-instrument-label-occ-vs-ticker.md`](../tickets/2026-09-19-leap-instrument-label-occ-vs-ticker.md)
- [ ] Lane 2 option Desk-Send / SOS — parked — **skipped filing**

---

## 15. Appendix (optional)

**SEF (spot ~30.26):** months NOV26, FEB27. Furthest Plan B: Feb 19 2027 30C bid 0.50 / ask 2.25 / mid 1.375 / delta 0.561 / OI 21 / conid `893744520`.

**BITQ (spot ~28.19):** months OCT26, NOV26, JAN27, APR27. Furthest Plan B: Apr 16 2027 28C mid 4.75 / delta 0.609 / OI blank / conid `912464575`. Spreads 39–70% — fail 8%, pass 500%.

**Desk URLs:**  
https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/workflow?journal_id=1943&portfolio_id=1577&task_id=1796  
https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/workflow?journal_id=1946&portfolio_id=1583&task_id=1799
