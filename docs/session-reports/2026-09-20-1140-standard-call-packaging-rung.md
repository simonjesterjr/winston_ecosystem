# Session Report — Standard long-call packaging rung (ADR-018)

**Date:** 2026-09-20
**Time:** 2026-09-19 session → wrap 11:40 MDT
**Duration:** multi-hour (overnight into 20th)
**Project:** Sawtooth / Winston ecosystem (cross-monolith)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `ecosystem` `main`; `winston_v2` `main`; `broker_gateway` `main`. Workspace root is **not** a git repo.
**Model:** Grok 4.6
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Add a **standard (non-LEAP) long call** as a third Fulfillment Packaging path in Winston v2 (Wv2), without touching Trend Following (TF) / Trading Strategy (TS) signal engines. First deliverable: design note, selector + frozen-chain fixtures, desk stamp + Justification, tests green. Broker Gateway (BG) OPT Desk-Send only if Confirm already stamps `conid`.

**Outcome:** Delivered (first deliverable). Live OPT Desk-Send and Winston Unit Test (WUT) lab parity left parked.

**One-line summary:** Operational Portfolios can prefer LEAP, a listed standard call, or stock on one Plan A/B ladder; Mode C default remains `[leap, stock]`; `standard_call` is opt-in policy.

---

## 2. Work Completed

- Read ADR-018 / 017 / 013, LEAP proxy law, Mode C Plan A/B, Wv2 `LeapCandidateResolver` + desk workflow (workspace Graphify Graph was stale for these classes — files used).
- Filed ADR-018 addendum (`standard_call` as packaging rung; does not reopen ADR-017).
- Wrote design note (the Grok Bot conversation handle).
- Implemented `FulfillmentPackagingPolicy`, `CallFulfillmentSelector`, `FulfillmentPackagingSelector`, `CallLifecycle`.
- Wired desk Confirm stamp + Justification copy; `RelatedInstrumentFulfillment` type `standard_call`.
- BG: refuse `asset_class=option` without `conid` (no stock-biased resolve).
- Tests green except one pre-existing Mode C paper **exit** spec (`exit_at_stop` stamp).

---

## 3. Code Delivered

### Files changed

**ecosystem** (this session only)

| File | Change | Notes |
|------|--------|-------|
| `docs/analysis/2026-09-19-standard-call-packaging-rung.md` | added | **Single doc for Grok Bot** |
| `docs/tickets/2026-09-19-standard-call-fulfillment-packaging-rung.md` | added | First deliverable checked |
| `docs/tickets/INDEX.md` | modified | One row insert |
| `docs/adr/ADR-018-mode-c-leap-plan-a-plan-b.md` | added/amended | Whole ADR was untracked; addendum 2026-09-19 |
| `docs/business-context/mode-c-leap-plan-a-plan-b.md` | added/amended | Plan B row mentions `standard_call` |
| `docs/business-context/leap-extra-modal-proxy.md` | modified | Standard-call sentence |
| `CONTEXT.md` | modified | Plan A / Plan B / Justification glossary only |
| `docs/session-reports/2026-09-20-1140-standard-call-packaging-rung.md` | added | This report |

**winston_v2**

| File | Change | Notes |
|------|--------|-------|
| `app/services/operations/fulfillment_packaging_policy.rb` | added | Derives `[leap, stock]` from `leap_fulfillment=all` |
| `app/services/operations/call_fulfillment_selector.rb` | added | Call rungs only |
| `app/services/operations/fulfillment_packaging_selector.rb` | added | Plan A/B ladder |
| `app/services/operations/call_lifecycle.rb` | added | flatten / roll / no auto-exercise |
| `app/services/operations/leap_candidate_resolver.rb` | modified | `chain_for` without long-dated-only filter |
| `app/controllers/operations/desk_workflows_controller.rb` | modified | Ladder stamp; skip re-resolve on explicit Plan B stock |
| `app/models/portfolio.rb` | modified | `packaging_policy` |
| `app/services/operations/related_instrument_fulfillment.rb` | modified | `standard_call` option-like |
| `app/services/broker_gateway/client.rb` | modified | optional `expiry_max_days` |
| desk views + justification | modified | `standard_call` type + copy |
| `db/migrate/20260919120000_add_fulfillment_packaging_policy_to_portfolios.rb` | added | jsonb policy |
| `db/schema.rb` | modified | policy + leap_fulfillment + session_order_slates (pending migrations applied in test) |
| specs + frozen chain fixture | added/modified | |

**broker_gateway**

| File | Change | Notes |
|------|--------|-------|
| `app/services/adapters/ibkr_adapter.rb` | modified | OPT missing `conid` → refuse |
| `spec/services/adapters/ibkr_adapter_spec.rb` | modified | missing-conid example |

### Commits

- _Pending wrap commit._

### Branch / PR state at sign-off

- Branch: each repo `main` — dirty until wrap commit
- Pushed: no (wrap step)
- PR: not opened

---

## 4. Decisions Made

### Decision 1: `standard_call` is an ADR-018 rung, not a new TS
- **Choice:** Ordered `packaging_preference`; Plan A = first; Plan B = next tradeable; stock is policy / `allow_equity_fallback`, not a side door in the call picker.
- **Why:** Operator ticket + ADR-018 general law (“Plan A is policy-defined”).
- **Alternatives considered:** Fork a new strategy type; silent OMS auto-stock; put stock inside `CallFulfillmentSelector`.
- **Reversibility:** easy (jsonb policy; Mode C derives old ladder when hash empty).
- **Promote to ADR?** Addendum on ADR-018 (done). Do not reopen ADR-017.

### Decision 2: Mode C default unchanged
- **Choice:** Empty policy + `leap_fulfillment=all` → `[leap, stock]`, `allow_equity_fallback: true`.
- **Why:** BITQ / SMH Plan B stock must not suddenly become a 60-DTE call.
- **Reversibility:** easy.

### Decision 3: No Black–Scholes for missing delta
- **Choice:** Standard-call filter requires delta/quote; missing → untradeable candidate.
- **Why:** Mode C lock: no BS synthesize.
- **Reversibility:** easy once Client Portal Gateway (CPGW) greeks exist.

### Decision 4: BG OPT Desk-Send not wired
- **Choice:** Refuse missing `conid` only. Confirm already stamps `conid` when a call resolves.
- **Why:** Ticket first deliverable; prove ticket still parked.
- **Promote to ADR?** no.

---

## 5. Insights Surfaced

- Workspace `graphify-out/graph.json` did not contain `LeapCandidateResolver` / `LeapPackaging` — map stale; files are proof (ADR-014).
- `LeapCandidateResolver` fetched `expiry_min_days: 365`, so standard calls never reached the picker until `chain_for` generalized.
- Confirm form `price` is often **premium**, not underlying last — must not drive ATM spot (parquet last instead).
- Journal `units: 2` in some Mode C specs already means **contracts**; floor(`/100`) would zero them. Sizing law is `signal_share_units`.
- Live IBKR `LeapCandidates` snapshots have bid/ask/last, **not** delta — live `standard_call` will fail the delta band until greeks are on the chain.

---

## 6. Issues & Tickets

### Resolved this session
- First deliverable of `2026-09-19-standard-call-fulfillment-packaging-rung.md` (selector, stamp, tests, design note).

### Deferred
- WUT lab Plan-B / `standard_call` parity (ticket says out of scope).
- BG OPT Desk-Send / `place_order` — already `2026-09-15-bg-ibkr-opt-order-intent-prove.md`.
- CPGW greeks/delta on `option_candidates` so live standard-call is tradeable.
- DA / desk **GET** prefill of packaging (still Confirm POST on `main`; `LeapPackaging` lives on worktree `mode-c-leap-desk-prefill`).
- OP UI to edit `fulfillment_packaging_policy` (console/jsonb only).
- Flatten / roll **jobs** (helper only).
- Mode C paper exit spec: `ExitAtStopService` does not stamp `exit_at_stop` (pre-existing).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Selector ladder / refuse / sizing / OCC / heat / flatten | compose `winston_v2` rspec | ✅ |
| LeapCandidateResolver | same | ✅ |
| Mode C Plan B + standard_call + Justification | `mode_c_leap_untradeable_fallback_spec` | ✅ |
| Mode C paper LEAP enter + Plan B GET/confirm | `mode_c_paper_leap_spec` | ✅ except exit STC |
| BG missing conid | `ibkr_adapter_spec` -e missing conid | ✅ |
| Browser desk | not run | ⚠️ |
| Live CPGW standard-call | not run | ⚠️ |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec \
  spec/services/operations/fulfillment_packaging_selector_spec.rb \
  spec/services/operations/call_fulfillment_selector_spec.rb \
  spec/services/operations/related_instrument_fulfillment_spec.rb \
  spec/services/operations/leap_candidate_resolver_spec.rb \
  spec/integration/mode_c_leap_untradeable_fallback_spec.rb \
  spec/integration/mode_c_paper_leap_spec.rb

cd broker_gateway && bundle exec rspec spec/services/adapters/ibkr_adapter_spec.rb -e "missing conid"
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** existing compose (`winston_v2`, `wv2_postgres`, `broker_gateway`)
- **Migrations:** `20260919120000_add_fulfillment_packaging_policy_to_portfolios`; test DB also applied pending `session_order_slates` + `leap_fulfillment` (schema.rb catch-up)

---

## 9. Risks & Technical Debt

- Empty-policy Mode C is `[leap, stock]`; adding `standard_call` without an explicit hash will not change live books — operators must set jsonb.
- Live standard-call untradeable without delta (honest, but easy to misread as a bug).
- `schema.rb` now includes `session_order_slates` from a prior undumped migration.
- Unused `leap_packaging_details` helper removed from desk controller; worktree `LeapPackaging` still not on `main`.

---

## 10. Open Questions

- **Should Mode C books opt into `[leap, standard_call, stock]`?** — operator; blocks live use of the new rung.
- **Greeks source for listed calls (CPGW vs refuse)?** — operator / BG; blocks live standard-call Plan A.
- **WUT PBR Plan B parity?** — operator; not implied by ADR-018.

---

## 11. Handoff & Resume Notes

- **Where I left off:** First deliverable on working trees; wrap. Operator asked for a single Grok Bot doc: `ecosystem/docs/analysis/2026-09-19-standard-call-packaging-rung.md`.
- **Next concrete step:** Decide whether any Mode C OP gets `packaging_preference: [leap, standard_call, stock]`; else leave derived `[leap, stock]`.
- **Files to read first:**
  1. `ecosystem/docs/analysis/2026-09-19-standard-call-packaging-rung.md`
  2. ADR-018 addendum
  3. `winston_v2/app/services/operations/fulfillment_packaging_selector.rb`

---

## 12. Stakeholder Communications

- Operator: Mode C paper books **do not change** until `fulfillment_packaging_policy` is set. Same TF signals.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, graphify (query stale), wrap, session-report, record (ticket/ADR/analysis)
- **Graphify Graph:** updated `ecosystem/graphify-out` (14781 nodes) and `broker_gateway/graphify-out` (745 nodes, includes `.option_intent?()` at `ibkr_adapter.rb:L555`). **winston_v2 `graphify-out/graph.json` missing** — no silent full rebuild. Workspace merge of 5 existing graphs → `graphify-out/graph.json` (20772 nodes; Wv2 omitted). `graphify-out/` not staged.
- **Ponytail flags:** New Wv2 ladder (`FulfillmentPackagingSelector` / `CallFulfillmentSelector`) is the packaging-pick owner; `LeapCandidateResolver` stays chain fetch + Mode C guards. Do not grow a third ATM picker (`LeapPackaging` still on worktree `mode-c-leap-desk-prefill`, not `main`). BG `.option_intent?` is a fail-closed guard next to `.resolve_conid`, not a second secdef walker. Ops UI ticket `2026-09-01-fulfillment-packaging-policy-ops-ui` already exists on the ecosystem graph — do not fork a second policy UI.
- **What worked well:** frozen-chain unit tests independent of CPGW; deriving Mode C ladder from `leap_fulfillment` avoided a book cutover.
- **Friction points:** Mode C request specs used a non-existent route helper and lacked CSRF/`host!`; Graphify missing Wv2 leap nodes; compose-only Wv2 test DB.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] **P0** Mode C LEAP stop-out option mark — See: [`docs/tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md`](../tickets/2026-09-20-mode-c-leap-exit-at-stop-option-mark.md)
- [ ] CPGW/BG option greeks — See: [`docs/tickets/2026-09-20-bg-option-candidates-greeks.md`](../tickets/2026-09-20-bg-option-candidates-greeks.md)
- [ ] OP UI for packaging policy — See: [`docs/tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md`](../tickets/2026-09-01-fulfillment-packaging-policy-ops-ui.md)
- [ ] Flatten/roll desk tasks — See: [`docs/tickets/2026-09-20-standard-call-flatten-roll-desk.md`](../tickets/2026-09-20-standard-call-flatten-roll-desk.md)
- [ ] WUT lab parity — See: [`docs/tickets/2026-09-20-wut-standard-call-plan-b-parity.md`](../tickets/2026-09-20-wut-standard-call-plan-b-parity.md)
- [ ] BG OPT Desk-Send prove — already [`docs/tickets/2026-09-15-bg-ibkr-opt-order-intent-prove.md`](../tickets/2026-09-15-bg-ibkr-opt-order-intent-prove.md)

---

## 15. Appendix (optional)

Grok Bot handle: `ecosystem/docs/analysis/2026-09-19-standard-call-packaging-rung.md`

Example opt-in:

```ruby
portfolio.update!(fulfillment_packaging_policy: {
  "packaging_preference" => %w[leap standard_call stock],
  "allow_equity_fallback" => true
})
```
