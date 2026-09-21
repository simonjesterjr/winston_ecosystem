# Session Report — Ops shell Pending vs Mode C Plan A/B/C

**Date:** 2026-09-21
**Time:** ~17:24–17:44 MDT
**Duration:** ~20m (after wrap `2026-09-21-1724-mode-c-stop-label-wrap.md`)
**Project:** Sawtooth / Winston ecosystem (cross-monolith)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` `main`; `ecosystem` `main`
**Model:** Grok 4.6
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Make sure every ops shell **Pending** draft follows Mode C Plan A / Plan B / Plan C (LEAP → standard long call → stock).

**Outcome:** Delivered. 12 Pending rows audited; 10 Mode C drafts re-overlaid with Client Portal Gateway (CPGW) up; extra-modal pyramids pinned to the **open listed contract**. Agent did not Confirm or Desk-Send.

**One-line summary:** Pending Mode C pyramids now add the same LEAP/call as the open lot (BITQ stayed Apr 28C, not a fresh 27C); sub-100-share signals are Plan C stock with Justification.

---

## 2. Work Completed

- Listed ops shell Pending (TF source, fill-date window): 12 drafts, 0 copy-book, 0 tracking.
- Classified Mint #384 and Yellow #798 as **not** Mode C (`leap_fulfillment=none` — Plan A **is** stock).
- Re-GET desk workflow for all 12 (HTTP 200) so `overlay_packaging_on_draft!` restamped Plan A/B/C.
- Bug: pyramid overlay re-walked ATM. Indigo BITQ task 1838 was 27C / conid `912464502` vs open lot 889 **28C** / `912464575`. Pin to open lot.
- Stamped **Instrument Label** on option pyramids; dropped ticker-as-OCC; Working Stop suggestion on underlying.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `winston_v2/app/controllers/operations/desk_workflows_controller.rb` | modified | `stamp_pyramid_from_open_lot!` |
| `winston_v2/spec/requests/desk_workflow_plan_c_overlay_spec.rb` | modified | BITQ pyramid keeps 28C when chain offers 27C |
| `ecosystem/docs/session-reports/2026-09-21-1744-mode-c-pending-plan-abc.md` | added | this report |

### Commits

- `winston_v2` `17bbbf3` — fix(desk): Mode C pyramid overlay pins the open listed contract (already on origin/main)
- `ecosystem` — this report (pending wrap commit)

### Branch / PR state at sign-off

- Branch: `main` — wv2 clean except untracked `.grok/skills/ponytail-apply/`
- Pushed: wv2 yes; ecosystem pending this report
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Extra-modal pyramid uses the open contract
- **Choice:** Overlay pins strike / expiry / conid from the open option lot; contract count still `floor(signal_share_units/100)`.
- **Why:** Pyramid adds to the existing extra-modal lot. Re-ATM after spot move would split the book (BITQ 27 vs 28).
- **Alternatives considered:** Live ATM walk on every pyramid GET.
- **Reversibility:** easy
- **Promote to ADR?** no — follows Signal Spine / one-name add

### Decision 2: Sub-100-share Mode C enters stay Plan C stock
- **Choice:** TSM 26/29, AAPL 40, IBM 40 short, SMH 19 pyramid → Plan C with `zero_contracts`.
- **Why:** ADR-018 Plan C is stock at `signal_share_units` when both call rungs floor to 0.
- **Alternatives considered:** Pass (WUT skip parity / journal 1915). Operator asked for A/B/C methodology, not Pass.
- **Reversibility:** easy (Pass those drafts)
- **Promote to ADR?** no — ADR-018 already

---

## 5. Insights Surfaced

- Desk GET overlay on pyramid without an open-lot pin will happily pick a new ATM strike after CPGW last moves.
- Ops shell Pending does **not** include Walnut IBKR-bound DA drafts (fill-date / TF-source window). Those slates are a different Pending surface.

---

## 6. Issues & Tickets

### Resolved this session
- Live BITQ pyramid strike mismatch (not a prior ticket) — fixed in `17bbbf3`.

### Deferred
- Short IBM: v1 call ladder has no put rung (ADR-018: no covered puts until the operator says). Plan C short stock is the current law.
- WUT skip-vs-Plan-C for `zero_contracts` remains a lab-parity question (`2026-09-20-wut-standard-call-plan-b-parity` P3 only if asked).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Pyramid pin spec | `desk_workflow_plan_c_overlay_spec` 8 examples | ✅ |
| Live overlay | curl GET 12 workflows HTTP 200; rails dump after | ✅ BITQ 28C; SEF 30C; RXT Jan 4C; Plan C stamps |
| Confirm / Desk-Send | not run | ⚠️ operator HITL |
| Mint/Yellow stock-only | leap_fulfillment=none | ✅ not Mode C |

**Test command(s):**

```bash
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 \
  bundle exec rspec spec/requests/desk_workflow_plan_c_overlay_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None
- **Services:** winston_v2 :3002; CPGW auth HTTP 200, tickle 200
- **Migrations:** None
- **Paper drafts:** journals 1976–1985 restamped; no cash change

---

## 9. Risks & Technical Debt

- Pyramid pin copies `option_premium` from the **open lot**, not a fresh CPGW mid. Confirm form Price may still be overlay-refreshed on enter path only.
- `stamp_pyramid_from_open_lot!` lives on `DeskWorkflowsController` (same as enter overlay). Fine until a second caller needs it.

---

## 10. Open Questions

- **None blocking.** Puts for short Mode C names wait on an explicit operator ask.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Pending drafts restamped; pyramid pin on `main`.
- **Next concrete step:** Operator Confirm/Pass the 12 Pending rows (or Pass sub-100 if WUT skip is wanted after all).
- **Files to read first:** this report; `desk_workflows_controller.rb` `stamp_pyramid_from_open_lot!`; ADR-018.

---

## 12. Stakeholder Communications

- Ops shell Pending Mode C rows now show Plan C stock or the same listed call as the open lot. No fills booked this pass.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report, graphify-ponytail
- **Graphify Graph:** ecosystem `graphify update` (14979 nodes); workspace merge 5 graphs (`winston_v2/graphify-out/graph.json` **missing**, not full-rebuilt). `graphify-out/` not staged.
- **Ponytail flags:** pyramid pin is new controller private methods next to `overlay_packaging_on_draft!` — not a duplicate of `RelatedInstrumentFulfillment.from_position` (that helper is reused).
- **What worked well:** live GET overlay is the same path as the operator desk.
- **Friction points:** CPGW dual-fetch made 12 sequential GETs ~97s.
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Operator Confirm or Pass the 12 Pending drafts — owner: John — due: next desk pass
- [ ] Put rung for short Mode C names — owner: operator ask — due: unset (ADR-018 holds)
- [ ] WUT Plan C vs skip for `zero_contracts` — already P3 optional ticket — skip unless asked

---

## 15. Appendix

Pending after overlay (2026-09-21):

| Task | Book | Adopted |
|------|------|---------|
| 1829 Blue TSM enter 26 | Plan C stock | zero_contracts |
| 1830 Blue RXT pyramid | Plan A `RXT 2029-01-19 C 4` ×9 | open 868/870 |
| 1831 Orange SMH pyramid 19 | Plan C stock | open stock 886 |
| 1832 Orange AAPL enter 40 | Plan C stock | zero_contracts |
| 1833 Mango SEF pyramid | Plan B `SEF 2027-02-19 C 30` ×4 | open 887 |
| 1834 Mango RXT pyramid | Plan A `RXT 2029-01-19 C 4` ×4 | open 869/871 |
| 1835 Copper TSM enter 29 | Plan C stock | zero_contracts |
| 1836 Slate TSM enter 29 | Plan C stock | zero_contracts |
| 1837 Indigo IBM short 40 | Plan C stock | zero_contracts; no puts |
| 1838 Indigo BITQ pyramid | Plan B `BITQ 2027-04-16 C 28` ×2 | open 889 (was 27C) |
| 1806 Mint OIH short | stock | not Mode C |
| 1808 Yellow AKAM long | stock | not Mode C |
