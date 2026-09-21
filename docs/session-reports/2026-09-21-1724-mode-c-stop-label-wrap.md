# Session Report — Mode C Working Stop, ATM-3 trace, Instrument Label

**Date:** 2026-09-21
**Time:** ~15:00–17:24 MDT
**Duration:** ~2h 25m
**Project:** Sawtooth / Winston ecosystem (cross-monolith)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` `main`; `broker_gateway` `main`; `ecosystem` `main`. Workspace root is **not** a git repo.
**Model:** Grok 4.6
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Tackle three follow-ups from wrap `2026-09-21-1457-mode-c-furthest-call-desk-uat.md`: (1) P0 Working Stop booked from option premium, (2) P2 ATM-3 vs listed surface, (3) P2 OCC vs ticker (existing ticket, not duplicated). P0 first.

**Outcome:** Delivered. P0 enter-path coded and spec-locked; journals **1943** / **1946** Working Stops restored on paper. P2 ATM-3 kept with Justification `selection_trace`. P2 instrument label designed (grill Q1–Q4) and implemented. Agent never Desk-Sent options.

**One-line summary:** Option Plan B Confirm now keeps Working Stop 2N under the underlying; desk speech is `SEF 2027-02-19 C 30`; conid stays Send identity; ATM-3 of furthest month stays, with HITL trace.

---

## 2. Work Completed

- Issue `docs/issues/2026-09-21-option-enter-working-stop-from-premium.md` marked ready then in-progress; P0 ticket In progress → Done this wrap.
- Three stacked writers of premium-space stops: StopSuggestion used option mid; fill-stop JS `stopFromFill(Price)`; `JournalConfirmationService#lot_working_stop_price` used fill = premium.
- Fix: option-like GET suggests 2N under underlying bar/signal close; JS locks Stop when fulfillment is leap / standard_call / option; confirm persists underlying stop (rejects premium-space submits).
- Operator go: journal **1943** pos 887 stop 0.78 → **29.95**; journal **1946** pos 889 stop 2.33 → **24.85**. No cash, no flatten, no Desk-Send.
- P2 ATM-3: keep walker; stamp `selection_trace` on Justification (OCC, mode, reject reasons).
- Grill Q1–Q4: **Instrument Label** `{UNDERLYING} {YYYY-MM-DD} {C|P} {strike}`; **Contract Identity** = conid; **OCC Symbol** only if IBKR sent `localSymbol` (no invented OSI); separate `fulfillment_details` keys. Glossary + leap-proxy domain note.
- Broker Gateway `LeapCandidates` emits `instrument_label`; does not copy CPGW `symbol`/ticker/`desc2` into OCC.

---

## 3. Code Delivered

### Files changed (this wrap’s intended commit set)

**winston_v2** (`main`) — this session plus leftover Mode C paper dirty left uncommitted after 1457 wrap (`OptionMark`, exit-at-stop, flatten tasks). Those files are entangled with `journal_confirmation_service.rb` (`OptionMark.for_position`).

| File | Change | Notes |
|------|--------|-------|
| `app/services/operations/stop_suggestion.rb` | modified | option-like still suggests underlying ATR; `lock_stop_to_underlying` |
| `app/services/operations/desk_context.rb` | modified | `apply_fill_adjusted_stop` skips option-like |
| `app/controllers/operations/desk_workflows_controller.rb` | modified | suggestion_context underlying ref; fill-stop type; `instrument_label` field |
| `app/controllers/operations/desk_actions_controller.rb` | modified | pass `fulfillment_type` into fill-stop |
| `app/views/operations/shared/_fill_stop_adjust_script.html.erb` | modified | `stopLockedToUnderlying` |
| `app/views/operations/shared/_stop_suggestion.html.erb` | modified | `lockStopToUnderlying` JSON |
| `app/services/operations/journal_confirmation_service.rb` | modified | `option_enter_working_stop`; also prior exit-at-stop OptionMark |
| `app/services/operations/related_instrument_fulfillment.rb` | modified | speech label `UNDERLYING YYYY-MM-DD C strike` |
| `app/services/operations/fulfillment_packaging_selector.rb` | modified | stamp `instrument_label`; OCC only if not stock root |
| `app/views/operations/desk_workflows/_justification.html.erb` | modified | selection_trace; Instrument Label |
| `app/views/operations/desk_workflows/show.html.erb` | modified | Instrument Label next to contracts |
| `app/services/operations/option_mark.rb` | added | leftover 1457 / exit-at-stop P0 |
| `app/services/operations/call_lifecycle_tasks.rb` | added | leftover flatten desk |
| `app/services/operations/{ad_hoc_exit,exit_at_stop,stop_out_reconciliation,task_generator}.rb` | modified | leftover Mode C exit/flatten |
| specs listed in git status for the above | modified/added | P0 GET/confirm lock; Instrument Label; leftover exit-at-stop |

**broker_gateway** (`main`) — **this session only** (leave unrelated `place_order` / cancel-order dirty)

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/ibkr/leap_candidates.rb` | modified | `instrument_label`; `occ_symbol` from `localSymbol` only |
| `spec/services/adapters/ibkr/leap_candidates_spec.rb` | modified | BITQ root symbol + empty localSymbol |

**ecosystem** (`main`) — **this session only**

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | Instrument Label, Contract Identity, OCC Symbol; grill flags |
| `docs/business-context/leap-extra-modal-proxy.md` | modified | speech vs conid vs OCC |
| `docs/issues/2026-09-21-option-enter-working-stop-from-premium.md` | modified | ready → in-progress; 1943/1946 corrected |
| `docs/tickets/2026-09-21-option-enter-working-stop-underlying.md` | modified | P0 ACs |
| `docs/tickets/2026-09-21-desk-furthest-month-full-chain.md` | modified | ATM-3 decision; archive this wrap |
| `docs/tickets/2026-09-19-leap-instrument-label-occ-vs-ticker.md` | modified | Q1–Q4 lock; archive this wrap |
| `docs/tickets/INDEX.md` | modified | status rows |
| `docs/session-reports/2026-09-21-1724-mode-c-stop-label-wrap.md` | added | this report |

Not staged: ecosystem Cromwell/analysis/INDEX leftovers; BG `place_order` / cancel-order; `.grok/skills/ponytail-apply/`; `graphify-out/`.

### Commits

- `winston_v2` `d302fdc` — feat(desk): option Working Stop on underlying; Instrument Label
- `broker_gateway` `4d5b412` — feat(ibkr): Instrument Label when CPGW symbol is the stock root
- `ecosystem` `dac281f` — docs: Mode C Working Stop, Instrument Label, ATM-3 trace wrap

### Branch / PR state at sign-off

- Branch: `main` on each monolith — this slice pushed
- Pushed: yes
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Working Stop stays on the underlying for option enter
- **Choice:** Skip fill-stop rewrite for option-like; confirm uses signal close / bar, not premium.
- **Why:** ADR-018 Signal Spine; booked SEF/BITQ stops were through-the-market.
- **Alternatives considered:** Keep skip-ATR (nil stop) for options — rejected (false 0.01 / naked lot).
- **Reversibility:** easy
- **Promote to ADR?** no — ADR-018 already says this

### Decision 2: ATM-3 of furthest month is enough
- **Choice:** Do not widen `ATM_LIMIT`; show `selection_trace` on Justification.
- **Why:** More CPGW `secdef/info` for strikes quality screens may still drop.
- **Alternatives considered:** Widen ATM_LIMIT / dual-fetch extra strikes.
- **Reversibility:** easy (follow-up if HITL sees a missed furthest-month strike)
- **Promote to ADR?** no

### Decision 3: Instrument Label grammar (grill Q1–Q4)
- **Choice:** Speech `UNDERLYING YYYY-MM-DD C|P strike`; identity = conid; do not invent OSI; separate keys.
- **Why:** CPGW `symbol` is the stock root; OSI padding is ugly; empty `localSymbol` is common.
- **Alternatives considered:** OCC OSI, IBKR `localSymbol`/`desc2`, constructed OSI, one blob field.
- **Reversibility:** easy (string field)
- **Promote to ADR?** no — glossary + leap-proxy note

---

## 5. Insights Surfaced

- GET HTML could already show a premium-space stop **before JS**: StopSuggestion referenced option mid (1.50 → ATR-guarded 1.44). JS was not the only writer.
- Confirm ignored submitted `stop_price` on enter and recomputed from fill (`Levels.working_stop(fill: premium)`).
- `RelatedInstrumentFulfillment.instrument_label` previously prefixed `LEAP`/`CALL`; speech lock dropped that prefix (`fulfillment_type` carries the rung).
- winston_v2 still has **no** `graphify-out/graph.json`. Wrap did not full-rebuild.

---

## 6. Issues & Tickets

### Resolved this session
- P0 issue `2026-09-21-option-enter-working-stop-from-premium` — code + live 1943/1946 stops. Resolve YAML when commit SHA lands.
- P0 ticket `2026-09-21-option-enter-working-stop-underlying` — Done; archive this wrap.
- P2 ticket `2026-09-21-desk-furthest-month-full-chain` — Done; archive this wrap.
- P2 ticket `2026-09-19-leap-instrument-label-occ-vs-ticker` — design + code; Done; archive this wrap.

### Deferred
- Widen `ATM_LIMIT` only if HITL sees a furthest-month strike outside ATM-3 that should have won — already noted on the ATM-3 ticket, not a new file.
- P0 `2026-09-20-mode-c-leap-exit-at-stop-option-mark` — leftover dirty code is included in the wv2 wrap commit so `OptionMark` is not missing; ticket status not closed here without a dedicated verify pass.
- Unrelated ecosystem / BG dirty trees — left unstaged (operator pref: in-repo hygiene, not tickets).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| P0 GET/confirm Working Stop | compose rspec overlay + confirmation + fill-stop + stock desk workflow | ✅ 63 then 74 examples, 0 failures |
| Live stock desk GET | curl journal 1938 | ✅ `lockStopToUnderlying: false`; new JS present |
| Live 1943/1946 | rails runner before/after | ✅ 0.78→29.95; 2.33→24.85 |
| P2 Justification trace | overlay + untradeable fallback request specs | ✅ |
| Instrument Label BG | `leap_candidates_spec` | ✅ 10 examples, 0 failures |
| Instrument Label Wv2 | packaging + overlay + related fill | ✅ 61 examples, 0 failures |
| Option Plan B desk GET in browser | no pending option draft except protected 1915 | ⚠️ request spec HTML only |
| Exit-at-stop leftover | not re-swept this session | ⚠️ shipped with wrap for coherence |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/requests/desk_workflow_plan_c_overlay_spec.rb \
  spec/services/operations/desk_context_fill_stop_spec.rb \
  spec/services/operations/stop_suggestion_spec.rb \
  spec/services/operations/journal_confirmation_service_spec.rb \
  spec/requests/operations_desk_workflow_spec.rb \
  spec/services/operations/related_instrument_fulfillment_spec.rb \
  spec/services/operations/fulfillment_packaging_selector_spec.rb \
  spec/integration/mode_c_leap_untradeable_fallback_spec.rb \
  spec/services/operations/related_instrument_fill_spec.rb

./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=bg_postgres broker_gateway \
  bundle exec rspec spec/services/adapters/ibkr/leap_candidates_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** existing compose (winston_v2 :3002, broker_gateway :3003)
- **Migrations:** None
- **Paper lots:** 1943/1946 stop columns only

---

## 9. Risks & Technical Debt

- wv2 wrap commit mixes this session with leftover 1457 Mode C exit-at-stop / flatten (`OptionMark`). Next session should smoke that P0 path.
- Duplicate `speech_label` in BG `LeapCandidates` and Wv2 `RelatedInstrumentFulfillment` (majestic-monolith copy, ~15 lines).
- `winston_v2/graphify-out/graph.json` missing.

---

## 10. Open Questions

- **None blocking.** Widen ATM-3 only after live HITL sees a missed furthest-month strike.

---

## 11. Handoff & Resume Notes

- **Where I left off:** P0/P2 coded; 1943/1946 stops corrected; wrap committing.
- **Next concrete step:** After push, smoke a Plan B desk GET (Instrument Label + Stop ~2N under stock) on a dummy_sim draft. Optionally verify exit-at-stop option mark (`2026-09-20-mode-c-leap-exit-at-stop-option-mark`).
- **Files to read first:** this report; ADR-018; `stop_suggestion.rb`; `journal_confirmation_service.rb` `option_enter_working_stop`; `LeapCandidates#build_candidate`.

---

## 12. Stakeholder Communications

- Operator: Working Stop on SEF/BITQ paper lots restored. Desk will show `SEF 2027-02-19 C 30` / `BITQ 2027-04-16 C 28` on next overlay GET.

---

## 13. Tools & Workflow Notes

- **Skills used:** lightweight-bug-fix, operator-prose, grill-with-docs, session-report, wrap, graphify-ponytail (map missing on wv2)
- **Graphify Graph:** updated `broker_gateway/graphify-out` (753 nodes); `ecosystem/graphify-out` (14987 nodes); workspace merge 5 graphs → 20986 nodes (`winston_v2/graphify-out/graph.json` **missing**, not full-rebuilt). `graphify-out/` not staged.
- **Ponytail flags:** duplicate Instrument Label formatter in BG vs Wv2; owner is Wv2 packaging speech, BG copy is transport payload. Do not harmonize this wrap.
- **What worked well:** failing request spec locked GET 1.44 (premium-space) before JS.
- **Friction points:** ritual “go” on 1943/1946 when the P0 ticket already listed correction as DoD; operator had to ask what we were waiting on.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [x] Restore 1943/1946 Working Stops — done this session
- [ ] Smoke Plan B desk GET for Instrument Label + underlying Stop — owner: next session — due: next desk pass
- [ ] Verify leftover exit-at-stop option-mark path (`2026-09-20-mode-c-leap-exit-at-stop-option-mark`) now that `OptionMark` lands — owner: next session — due: before relying on auto stop-out
- [ ] Widen ATM_LIMIT only if HITL sees a missed furthest-month strike — owner: operator — due: unset (already on archived ATM-3 ticket)

---

## 15. Appendix

Live correction:

```
1943 SEF pos 887  stop 0.78 → 29.95  (signal_close 30.54, ATR 0.2965)
1946 BITQ pos 889 stop 2.33 → 24.85  (signal_close 27.31, ATR 1.2287)
```
