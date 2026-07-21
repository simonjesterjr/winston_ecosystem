# Session Report — ADR-009 Desk Series (#1 EOD Cadence + #3 Signaled Entry)

**Date:** 2026-07-21  
**Time:** ~session through 15:27 MDT  
**Duration:** ~substantive product session  
**Project:** sawtooth Winston multi-monolith workspace  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` (`winston_v2`, `ecosystem`)  
**Model:** Grok 4.5  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Tackle ADR-009 desk series — main product path (human-gated desk fulfillment).

**Outcome:** Partially delivered (series #1 and #3 shipped; #2/#4/#5/#6 remain)

**One-line summary:** Implemented EOD Signal Date / Fill Date + next-open prefill and enforced Signaled Entry Rule on book-enter paths, with specs green and Cromwell skills updated.

---

## 2. Work Completed

### A. Series orientation
- Mapped ADR-009 tickets, business context, and live Wv2 desk/journal/confirm path.
- Chose order: **#1 EOD cadence** then **#3 Signaled Entry** (before full Desk Workflow UI).

### B. ADR-009 #1 — EOD Signal / Fill / next-open
- Added `Operations::EodCadence` (signal_date, fill_date, next_open_*, price_source).
- Extended `ParquetLookbackLoader` with `next_bar_after`.
- `TaskGenerator` stamps dual dates on DA drafts; never invents next open from close.
- `JournalConfirmationService` prefers next-open prefill; books `trade_date` to fill (or today if early confirm); preserves signal_date in details.
- `ActionItemWindow` + `ExpireStaleActionItemsService` fill-date-aware process-miss expiry.
- Desk handoff, DAR next_steps, journal presenter, desk UI show cadence.
- Specs for cadence, task generator, expire, confirm, parquet, presenter.

### C. ADR-009 #3 — Signaled Entry Rule
- `AdHocPaperFillService`: require `signal_journal_id` / `signal_task_id` or `force=true` + notes.
- Wired `force` through internal book API, desk form, ops shell.
- Updated related-instrument / ad-hoc / bulk specs for force audit path.
- Cromwell skills: `winston-ad-hoc-fill`, `winston-confirmation-loop`.

### D. Docs / tickets
- Archived done tickets #1 and #3; regenerated INDEX P1 rows for remaining series.
- Updated human-gated desk gap checklist (next-open + signaled entry → Built).

---

## 3. Code Delivered

### Files changed (this session)

#### `winston_v2/`

| File | Change |
|------|--------|
| `app/services/operations/eod_cadence.rb` | **added** |
| `app/services/parquet_lookback_loader.rb` | `next_bar_after` |
| `app/services/operations/task_generator.rb` | cadence stamp on drafts |
| `app/services/operations/journal_confirmation_service.rb` | next-open + fill trade_date |
| `app/services/action_item_window.rb` | fill_date stale |
| `app/services/expire_stale_action_items_service.rb` | process_miss expire |
| `app/services/operations/desk_action_handoff.rb` | cadence fields |
| `app/services/daily_report_payload_builder.rb` | DAR cadence notes |
| `app/services/internal_journal_presenter.rb` | signal/fill/prefill |
| `app/services/operations/ad_hoc_paper_fill_service.rb` | Signaled Entry Rule |
| `app/services/operations/ops_shell_chat.rb` | force + help |
| `app/controllers/internal_controller.rb` | book `force` |
| `app/controllers/operations/desk_actions_controller.rb` | force / signal_task |
| `app/views/operations/desk_actions/show.html.erb` | signal/fill UI |
| `spec/services/**` | EOD + signaled entry + related updates |

#### `ecosystem/`

| File | Change |
|------|--------|
| `ai/skills/winston-ad-hoc-fill/SKILL.md` | Signaled Entry + force |
| `ai/skills/winston-confirmation-loop/SKILL.md` | T/T+1 cadence |
| `docs/business-context/human-gated-desk-and-fulfillment.md` | gap checklist |
| `docs/tickets/INDEX.md` | archive #1/#3 |
| `docs/tickets/archive/2026-07-20-eod-signal-fill-dates-next-open.md` | Done |
| `docs/tickets/archive/2026-07-20-enforce-signaled-entry-rule.md` | Done |
| `docs/session-reports/2026-07-21-1527-adr009-desk-series-eod-signaled-entry.md` | this report |

### Commits

- _Filled at wrap commit time._

### Branch / PR state at sign-off

- Branch: `main` on both monoliths  
- Pushed: wrap step  
- PR: not opened  

---

## 4. Decisions Made

### Decision 1: Store dual dates in fulfillment_details (interim)
- **Choice:** No new journal columns for signal_date/fill_date; stamp JSON details + task metadata.  
- **Why:** Ticket allowed interim; avoids migration risk while dual spine is young.  
- **Alternatives considered:** First-class date columns.  
- **Reversibility:** easy  
- **Promote to ADR?** no (already ADR-009)

### Decision 2: Early confirm books capital as of today
- **Choice:** If fill_date is in the future, `trade_date` = today so open position + capital_base match. Intended fill_date stays in details.  
- **Why:** Confirm opens Position immediately; future trade_date would hide cash impact.  
- **Reversibility:** easy  

### Decision 3: Signaled Entry force requires notes
- **Choice:** `force=true` without notes → `force_requires_notes`.  
- **Why:** Audit trail for policy override.  
- **Reversibility:** easy  

---

## 5. Insights Surfaced

- DA drafts already engage OPs; dual dates make process-miss and next-open prefill first-class without inventing prices.
- AR bind placeholders collide with Postgres `jsonb ?` — use `jsonb_exists`.
- Many legacy specs used naked ad-hoc enter; force+notes is the transitional test path until all paths confirm drafts.

---

## 6. Issues & Tickets

### Resolved this session
- ADR-009 series **#1** EOD Signal/Fill/next-open — archived Done.  
- ADR-009 series **#3** Signaled Entry Rule — archived Done.  

### Deferred (already ticketed unless noted)
- Series **#2** Full Desk Workflow page — `docs/tickets/2026-07-20-desk-workflow-guided-confirm-page.md`  
- Series **#4** Stop-Out Reconciliation — `docs/tickets/2026-07-20-stop-out-reconciliation-snapshot.md`  
- Series **#6** DAR real process-miss attention — `docs/tickets/2026-07-20-dar-real-process-miss-attention.md`  
- Series **#5** Capacity swap packages (P2) — `docs/tickets/2026-07-20-wv2-capacity-swap-desk-packages.md`  
- Journal stop on confirm (partially present via stop_price) — `docs/tickets/2026-07-15-journal-ledger-stop-on-confirm-and-update.md`  
- Blue OP #241 successor cleanup — `docs/tickets/2026-07-21-blue-241-successor-cleanup.md`  
- Optional MCP strategy inspect tool — prior session deferral, not filed this session  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| EOD cadence + expire + confirm + signaled entry | container `bundle exec rspec` (71 examples) | ✅ |
| Live paper smoke on OP #240 | not run this session | ⚠️ |
| winston_mcp recreate after book force param | not run | ⚠️ |

**Test command(s):**

```bash
podman exec -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres \
  -e TEST_DB_USER=sawtooth -e TEST_DB_PASSWORD=sawtooth \
  -e TEST_DB_NAME=winston_v2_test winston_v2 bash -lc \
  'bundle exec rspec spec/services/operations/eod_cadence_spec.rb \
    spec/services/operations/task_generator_eod_cadence_spec.rb \
    spec/services/action_item_window_spec.rb \
    spec/services/expire_stale_action_items_eod_spec.rb \
    spec/services/operations/journal_confirmation_service_spec.rb \
    spec/services/operations/ad_hoc_paper_fill_service_spec.rb \
    spec/services/operations/related_instrument_fill_spec.rb \
    spec/services/parquet_lookback_loader_spec.rb \
    spec/services/internal_journal_presenter_spec.rb \
    # (+ bulk exit/stop, ad_hoc exit, ops_shell exit parse)
  '
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new  
- **Services:** existing `winston_v2` + `wv2_postgres` for tests  
- **Migrations:** none  

---

## 9. Risks & Technical Debt

- Dual dates live in JSON until first-class columns if query load grows.  
- `force=true` + default notes in shell (`force enter via ops shell`) still satisfies notes gate — operators should write real audit text.  
- Ecosystem tree had **pre-existing dirty** files unrelated to this session (left unstaged).  

---

## 10. Open Questions

- **Ship MCP `force` on `wv2_book_trade` schema?** — if MCP layer needs explicit force arg pass-through; verify after recreate.  
- **Paper smoke on Blue #240 after DA** — confirm next-open path end-to-end.  

---

## 11. Handoff & Resume Notes

- **Where I left off:** #1 and #3 implemented, specs green, tickets archived; wrap in progress.  
- **Next concrete step:** ADR-009 **#4 Stop-Out Reconciliation** or **#2 Desk Workflow page**.  
- **Files to read first:**  
  1. `ecosystem/docs/adr/ADR-009-human-gated-desk-and-fulfillment.md`  
  2. `winston_v2/app/services/operations/eod_cadence.rb`  
  3. `winston_v2/app/services/operations/ad_hoc_paper_fill_service.rb`  
  4. Remaining tickets #2/#4/#6 under `ecosystem/docs/tickets/`  

---

## 12. Stakeholder Communications

- _None required._ Desk path now closer to “signal T → fill T+1 open → human confirm; no naked enter without force.”

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report  
- **What worked well:** series ticket acceptance criteria as implementation checklist; container rspec with TEST_DB_HOST.  
- **Friction points:** host `bundle`/DB vs container; AR `?` vs jsonb operator.  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] ADR-009 #4 Stop-Out Reconciliation — owner: next session  
- [ ] ADR-009 #2 Full Desk Workflow page — owner: next session  
- [ ] Paper smoke Blue #240 after next DA — owner: ops  
- [ ] Recreate/smoke winston_mcp if book tool schema needs `force` — owner: ops  
- [ ] Optional: first-class signal_date/fill_date columns if JSON friction — deferred  

---

## 15. Appendix

Remaining active ADR-009 P1 tickets after archive:

- `2026-07-20-desk-workflow-guided-confirm-page.md`  
- `2026-07-20-stop-out-reconciliation-snapshot.md`  
- `2026-07-20-dar-real-process-miss-attention.md`  
- `2026-07-20-wv2-capacity-swap-desk-packages.md` (P2)  
