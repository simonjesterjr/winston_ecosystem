# Session Report — ADR-009 #4 Stop-Out Reconciliation + #2 Desk Workflow

**Date:** 2026-07-21  
**Time:** ~through 15:40 MDT  
**Duration:** ~product session (continuation after #1/#3 wrap)  
**Project:** sawtooth Winston multi-monolith workspace  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `main` (`winston_v2`, `ecosystem`)  
**Model:** Grok 4.5  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Implement ADR-009 desk series items (1) Stop-Out Reconciliation and (2) Desk Workflow guided confirm page.

**Outcome:** Delivered

**One-line summary:** Real-world exits now snapshot Working Stop with gap warnings and unique-lot resolution; DAR handoffs deep-link to a guided `/operations/workflow` confirm UI.

---

## 2. Work Completed

### A. #4 Stop-Out Reconciliation
- Added `Operations::StopOutReconciliation` (working stop, fill, gap, warn threshold).
- Hardened `AdHocExitService`: require unique open lot or `position_id`; multi-lot → `ambiguous_position`.
- Confirm-exit path stamps same snapshot; shell exit reply surfaces gap WARN.
- DAR recent journals + `InternalJournalPresenter` expose provenance fields.
- Specs: stop-out unit + ad-hoc exit extensions.

### B. #2 Desk Workflow page
- Routes `GET/POST /operations/workflow` → `DeskWorkflowsController`.
- Guided view: signal spine (dates/prefill), packaging, confirm/edit/exit_adhoc; stop-out preview.
- `DeskActionHandoff.form_path` → workflow when journal/task present; classic desk for free-form.
- Closed OP / non-draft refuse mutate; multi-leg package_order warn stub.
- Request + handoff specs (host `localhost` for Rails allowed_hosts).

### C. Docs
- Archived tickets #2 and #4; INDEX + gap checklist + Cromwell skills updated.

---

## 3. Code Delivered

### Files changed (this session)

#### `winston_v2/`

| File | Change |
|------|--------|
| `app/services/operations/stop_out_reconciliation.rb` | **added** |
| `app/services/operations/ad_hoc_exit_service.rb` | unique lot + snapshot |
| `app/services/operations/journal_confirmation_service.rb` | exit snapshot |
| `app/services/operations/ops_shell_chat.rb` | exit warn line |
| `app/services/operations/desk_action_handoff.rb` | workflow form_path |
| `app/services/daily_report_payload_builder.rb` | journal stop-out fields |
| `app/services/internal_journal_presenter.rb` | stop-out fields |
| `app/controllers/operations/desk_workflows_controller.rb` | **added** |
| `app/views/operations/desk_workflows/show.html.erb` | **added** |
| `config/routes.rb` | workflow routes |
| `spec/services/operations/stop_out_reconciliation_spec.rb` | **added** |
| `spec/services/operations/ad_hoc_exit_service_spec.rb` | stop-out + multi-lot |
| `spec/services/operations/desk_action_handoff_workflow_spec.rb` | **added** |
| `spec/requests/operations_desk_workflow_spec.rb` | **added** |

#### `ecosystem/`

| File | Change |
|------|--------|
| `docs/tickets/archive/2026-07-20-stop-out-reconciliation-snapshot.md` | Done |
| `docs/tickets/archive/2026-07-20-desk-workflow-guided-confirm-page.md` | Done |
| `docs/tickets/INDEX.md` | archive rows |
| `docs/business-context/human-gated-desk-and-fulfillment.md` | gap checklist |
| `ai/skills/winston-ad-hoc-fill/SKILL.md` | stop-out docs |
| `ai/skills/winston-confirmation-loop/SKILL.md` | workflow URL |
| `docs/session-reports/2026-07-21-1540-…` | this report |

### Commits

- `winston_v2` `2673a84` — feat(desk): ADR-009 stop-out reconciliation + Desk Workflow page
- `ecosystem` `ae62132` — docs: ADR-009 #2+#4 wrap

### Branch / PR state at sign-off

- Branch: `main` both repos  
- Pushed: yes (origin main)  
- PR: not opened  

---

## 4. Decisions Made

### Decision 1: Ambiguous multi-lot exit refused without position_id
- **Choice:** `ambiguous_position` error; use `position_id` or `exit_all`.  
- **Why:** ADR-009 requires lot linkage for Working Stop snapshot.  
- **Reversibility:** easy  

### Decision 2: Gap warn not hard-block
- **Choice:** Default 1% / $0.05 threshold; still confirmable.  
- **Why:** Grill rejected hard-block option B.  
- **Reversibility:** easy  

### Decision 3: Workflow vs classic desk split
- **Choice:** Draft/task → `/operations/workflow`; free-form → `/operations/desk`.  
- **Why:** Guided path is product intent; ad-hoc remains for exceptions.  
- **Reversibility:** easy  

---

## 5. Insights Surfaced

- Rails `config.hosts` in this app requires `host! "localhost"` for request specs (not `www.example.com`).
- Multi-lot pyramids make symbol-only exit unsafe for stop-out accounting.
- Package-order warn is enough until series #5 emits real packages.

---

## 6. Issues & Tickets

### Resolved this session
- ADR-009 **#4** Stop-Out Reconciliation — archived Done.  
- ADR-009 **#2** Desk Workflow page — archived Done.  

### Deferred (already ticketed)
- Series **#6** DAR real process-miss attention — `docs/tickets/2026-07-20-dar-real-process-miss-attention.md` (still untracked on disk from prior).  
- Series **#5** Capacity swap packages (P2) — `docs/tickets/2026-07-20-wv2-capacity-swap-desk-packages.md`.  
- ADR-009 file itself still untracked from pre-session hygiene.  

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Stop-out + exit + workflow + regression #1/#3 | container rspec 53 examples | ✅ |
| Live browser smoke on `/operations/workflow` | not run | ⚠️ |
| MCP exit reply_text for warnings | shell path covered; MCP surface not recreated | ⚠️ |

**Test command(s):** container `bundle exec rspec` on stop_out, ad_hoc_exit, handoff workflow, request workflow, plus eod/signaled suite.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None  
- **Services:** winston_v2 + wv2_postgres for tests  
- **Migrations:** none  

---

## 9. Risks & Technical Debt

- Ecosystem still has pre-existing dirty (CONTEXT, ADR-006/007, untracked ADR-009 + remaining tickets).  
- Workflow form enables submit even when non-confirmable edges are thin (read-only panel for executed).  
- Gap threshold constants may need ops tuning.  

---

## 10. Open Questions

- **Should MCP `wv2_exit_trade` surface `warnings[]` in reply_text always?** — shell does; verify MCP adapter.  

---

## 11. Handoff & Resume Notes

- **Where I left off:** #2 and #4 shipped and tested.  
- **Next concrete step:** ADR-009 **#6** DAR Active real process-miss attention; hygiene commit for untracked ADR-009 + remaining tickets.  
- **Files to read first:**  
  1. `winston_v2/app/services/operations/stop_out_reconciliation.rb`  
  2. `winston_v2/app/controllers/operations/desk_workflows_controller.rb`  
  3. `winston_v2/app/views/operations/desk_workflows/show.html.erb`  
  4. `docs/tickets/2026-07-20-dar-real-process-miss-attention.md`  

---

## 12. Stakeholder Communications

- _None._  

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report  
- **What worked well:** ticket acceptance → implementation; request specs with host fix.  
- **Friction:** allowed_hosts 403 in container request specs.  

---

## 14. Follow-up Actions

- [ ] ADR-009 #6 DAR process-miss attention — next session  
- [ ] Commit untracked ADR-009 + remaining series tickets (hygiene)  
- [ ] Optional: browser smoke workflow on paper Blue  
- [ ] Optional: MCP exit warnings in reply_text  

---

## 15. Appendix

_None._  
