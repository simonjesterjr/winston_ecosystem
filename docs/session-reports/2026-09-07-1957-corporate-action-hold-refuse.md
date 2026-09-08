# Session Report — CORPORATE_ACTION_HOLD: Confirm refuses until named override

**Date:** 2026-09-07
**Time:** ~17:55–19:57 MDT
**Duration:** ~2h (inventory + explain; then desk HOLD implement)
**Project:** sawtooth Winston ecosystem — winston_v2 (Wv2), ecosystem docs
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` on `winston_v2`, `ecosystem` (started from each `origin/main`)
**Model:** Grok 4.6
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Start the remaining P0 corporate-action stop safeguards. Explain the issue; ask before coding. Operator then chose: harden desk HOLD so Confirm **refuses** a split-like fill until a named override, with recommendations.

**Outcome:** Delivered for the desk gate. Broker Gateway (BG) `order_write` hold remains L3. Universe parquet hygiene remains scan-only.

**One-line summary:** A reverse-split-sized **adverse** fill vs the working stop now refuses Confirm until `tradable_gap` or `broker_print` plus audit notes; preferred next action is Exit at stop.

---

## 2. Work Completed

- Inventoried leftovers after the End of Day Historical Data (EODHD) lag-retry wrap; operator picked P0 corporate-action safeguards (option A).
- Explained Mint System 2 resting Portfolio Backtest Run (PBR) 533 ruin: unadjusted reverse-split × cover-at-open (USO 1-for-8, XOP 1-for-4), not same-bar stops.
- Live parquet scan: United States Oil Fund (USO) / SPDR S&P Oil & Gas Exploration (XOP) / VanEck Oil Services (OIH) still clean; United States Natural Gas Fund (UNG), Teucrium Wheat (WEAT), Amcor (AMCR), Applied Digital (APLD) now clean; **0 of 81 Active Operational Portfolio (OP) book names** still jump. 271 of 2716 other files still trip the 1.8 detector.
- Operator lock: Confirm refuses until named override; recommendations preferred.
- `StopOutReconciliation.confirm_gate`: HOLD is refuse; overrides `tradable_gap` / `broker_print` require audit notes (generic desk strings do not count). Split-like is **adverse** only (long fill ≪ stop; short fill ≫ stop) so profitable exits are not HOLDs.
- Wired JournalConfirmationService (before close), AdHocExitService, desk workflow, classic desk, ops shell (`override=`), internal confirm API.
- Desk workflow: HOLD banner + recommendation list + override select. Exit-at-stop still books at the working stop (ratio 1 — no HOLD).
- Specs: 64 examples green (reconciliation, confirm, ad-hoc exit, desk workflow, exit-at-stop). Adjacent ops-shell / paper-fill also green.
- Restarted `winston_v2`, `winston_v2_sidekiq`.
- Updated issue + P0 ticket for refuse semantics and live scan.

---

## 3. Code Delivered

### Files changed

#### winston_v2

| File | Change | Notes |
|------|--------|-------|
| `app/services/operations/stop_out_reconciliation.rb` | modified | Adverse split-like; `confirm_gate`; recommendations |
| `app/services/operations/journal_confirmation_service.rb` | modified | Gate before transaction; stamp override |
| `app/services/operations/ad_hoc_exit_service.rb` | modified | `corporate_action_override:` through to confirm |
| `app/controllers/operations/desk_workflows_controller.rb` | modified | Pass override; HOLD flash + preferred next |
| `app/controllers/operations/desk_actions_controller.rb` | modified | Pass override on confirm / ad-hoc exit |
| `app/controllers/internal_controller.rb` | modified | `corporate_action_override` on confirm |
| `app/services/operations/ops_shell_chat.rb` | modified | `override=`; help; recs on confirm error |
| `app/views/operations/desk_workflows/show.html.erb` | modified | HOLD banner + override select |
| `app/views/operations/desk_actions/show.html.erb` | modified | Override select |
| `spec/services/operations/stop_out_reconciliation_spec.rb` | modified | Gate + adverse vs profitable |
| `spec/services/operations/journal_confirmation_service_spec.rb` | modified | Refuse / override / generic notes |
| `spec/services/operations/ad_hoc_exit_service_spec.rb` | modified | Refuse / broker_print |
| `spec/requests/operations_desk_workflow_spec.rb` | modified | GET banner + POST refuse |

**Not this session (do not stage)**

- Wv2: `app/views/operations/home/index.html.erb`, `config/routes.rb`, untracked `ecosystem_controller` / `ecosystem_board` / `ecosystem_pulse` / `views/operations/ecosystem/` / `public/ecosystem/` / `spec/requests/operations_ecosystem_spec.rb`
- ecosystem: `AGENTS.md`, `CONTEXT.md`, `docs/README.md`, `docs/tickets/INDEX.md`, `docs/poster/`, `ecosystem_view/`, Winston Ecosystem View plans/tickets/interface, `plans/cromwell-staff-roster.md`, `vendor/`

#### ecosystem

| File | Change | Notes |
|------|--------|-------|
| `docs/issues/2026-08-22-unadjusted-reverse-split-jumps.md` | modified | Refuse + live scan; checkboxes |
| `docs/tickets/2026-08-22-corporate-action-stop-safeguards.md` | modified | Wv2 row = refuse 2026-09-07 |
| `docs/session-reports/2026-09-07-1957-corporate-action-hold-refuse.md` | added | this report |

### Commits

- `winston_v2` `445815c` — fix(ops): refuse split-like stop-out fills until named override
- `ecosystem` — this wrap (SHA filled after commit)

### Branch / PR state at sign-off

- Branch: `main` on `winston_v2` and `ecosystem`
- Pushed: pending this wrap
- PR: not opened (direct `main`)

---

## 4. Decisions Made

### Decision 1: Confirm refuses, not warn-only
- **Choice:** `confirm_gate` returns error unless a named override + audit notes.
- **Why:** Operator lock. Warning-only still booked an 8× fill.
- **Alternatives considered:** Keep warn-only; `force=true` bypass (rejected — named codes only).
- **Reversibility:** easy
- **Promote to ADR?** no (implements existing P0 expected behavior)

### Decision 2: Two override codes
- **Choice:** `tradable_gap` (verified real gap) and `broker_print` (matched broker fill already happened).
- **Why:** Distinguishes “I looked at the tape” from “cash already moved.” Both require notes that are not generic desk strings.
- **Alternatives considered:** Free-form `force=true`; a third `operator_accept` code (unnecessary).
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: HOLD is adverse fill vs working stop
- **Choice:** Long HOLD only if fill ≪ stop (≤ 1/1.8); short HOLD only if fill ≫ stop (≥ 1.8). No direction → bidirectional (fail closed).
- **Why:** A long profitable exit at 11 vs stop 6 (ratio 1.83) is not a reverse split. Bidirectional 1.8 would have blocked `drop_book` at 11.
- **Alternatives considered:** Keep bidirectional ratio; raise threshold to 3×.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 4: Preferred recommendation is Exit at stop
- **Choice:** Rank `exit_at_stop` preferred; then Pass Signal; overrides last.
- **Why:** Books at the working stop (same survival as next-open on the artifact) without claiming the post-split print.
- **Alternatives considered:** Default to Pass; auto-rewrite fill to working stop on Confirm (silent).
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- P0 parquet stitch for USO/XOP/OIH held. UNG/WEAT/AMCR/APLD (left as suspects on 2026-08-22) are now clean — likely later full acquire + `ParquetStandardizer` auto-stitch / EODHD `adjusted_close` scaling.
- 271 remaining jumps are **not** on Active books. Blind universe-APPLY is still wrong (penny 2×).
- Wv2 HOLD is fill vs **working stop**, not overnight open vs prev close. Direction-aware adverse check is load-bearing.
- Generic confirm notes (`confirmed via ops shell`, `desk workflow confirm`) would have been a silent bypass if treated as audit notes.
- Exit at stop never hits HOLD (fill = working stop).
- Mint re-score 536/537 already ran (537 +242 / 56 vs 536 +94 / 58). Issue file was stale (“pending”). Guard did not fire on 537 because stitch removed the jump.

---

## 6. Issues & Tickets

### Resolved this session
- Wv2 desk HOLD was warning-only — now refuse + named override. Issue [`docs/issues/2026-08-22-unadjusted-reverse-split-jumps.md`](../issues/2026-08-22-unadjusted-reverse-split-jumps.md) still **in-progress** (BG L3 + universe leftovers). Ticket [`docs/tickets/2026-08-22-corporate-action-stop-safeguards.md`](../tickets/2026-08-22-corporate-action-stop-safeguards.md) Wv2 row updated.

### Deferred
- BG `order_write` split-like send hold — already on the P0 ticket as L3. See: [`../tickets/2026-08-22-corporate-action-stop-safeguards.md`](../tickets/2026-08-22-corporate-action-stop-safeguards.md); write path [`../tickets/2026-08-20-resting-session-stop-orders.md`](../tickets/2026-08-20-resting-session-stop-orders.md) (Blocked). Not cloned.
- Classify remaining 271 parquet jumps — See: [`../tickets/2026-09-07-classify-remaining-split-jump-parquet.md`](../tickets/2026-09-07-classify-remaining-split-jump-parquet.md)
- Optional new Mint S2 pair now that UNG/WEAT/AMCR are clean — See: [`../tickets/2026-09-07-mint-s2-rescore-after-ung-weat-amcr.md`](../tickets/2026-09-07-mint-s2-rescore-after-ung-weat-amcr.md)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| StopOutReconciliation + confirm_gate | compose rspec | ✅ 12 examples |
| JournalConfirmationService HOLD | compose rspec | ✅ including refuse / override / generic notes |
| AdHocExitService HOLD | compose rspec | ✅ refuse + broker_print; no leftover draft |
| Desk workflow GET banner + POST refuse | compose request spec | ✅ |
| Exit at stop (working-stop fill) | compose rspec | ✅ 4 examples |
| Adjacent ops-shell exit parse + paper fill | compose rspec | ✅ |
| Live parquet Active books | `SplitAdjustmentService.scan_symbol` × 81 | ✅ 0 jumps |
| Universe scan | `data:scan_split_jumps` | ⚠️ 271/2716 still jump (not Active) |
| Browser click-through | not opened | ⚠️ |
| Live Telegram / DAR copy | not this session | ⚠️ |

**Test command(s):**

```
./bin/compose exec -T -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres winston_v2 bundle exec rspec \
  spec/services/operations/stop_out_reconciliation_spec.rb \
  spec/services/operations/journal_confirmation_service_spec.rb \
  spec/services/operations/ad_hoc_exit_service_spec.rb \
  spec/requests/operations_desk_workflow_spec.rb \
  spec/services/operations/exit_at_stop_service_spec.rb
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new
- **Services:** restarted `winston_v2`, `winston_v2_sidekiq` (bind-mount; no image rebuild)
- **Migrations:** none
- **Secrets:** none

---

## 9. Risks & Technical Debt

- HOLD is untested against a live broker print (no `order_write`). `broker_print` override is the escape hatch if cash already moved.
- Duplicate `CorporateActionJump` in data_manager (DM) and Winston Unit Test (WUT) still must stay in lockstep (RATIO_HIGH 1.8).
- Desk workflow HOLD banner uses the preview fill; if the operator changes price after load, they must re-GET or POST to see the new gate (POST still gates).
- Unrelated Wv2 ecosystem-view dirty tree must not be staged with this wrap.

---

## 10. Open Questions

- **Should the leftover 271 jumps get a child P2 ticket, or stay a note on the P0 issue?** — operator; blocks: none for Active desk
- **Re-score Mint S2 on current parquet?** — operator; not required to close the desk gate

---

## 11. Handoff & Resume Notes

- **Where I left off:** Confirm refuse live on compose; issue/ticket updated; wrap.
- **Next concrete step:** Optional — classify 271 jumps, or leave the P0 until BG L3. Next non-WQ build remains TF desk (process-miss / Slate Contest) or Yellow PBR 550 import.
- **Files to read first:**
  1. `winston_v2/app/services/operations/stop_out_reconciliation.rb` (`confirm_gate`)
  2. `winston_v2/app/services/operations/journal_confirmation_service.rb`
  3. `ecosystem/docs/issues/2026-08-22-unadjusted-reverse-split-jumps.md`
  4. `ecosystem/docs/tickets/2026-08-22-corporate-action-stop-safeguards.md`

---

## 12. Stakeholder Communications

- _None._ Operator-facing; no outward email.

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `lightweight-bug-fix` (failing spec first), `session-report`, `wrap`
- **What worked well:** Live 81-symbol Active scan made “UNG still pending” obsolete before coding; direction-aware HOLD avoided a `drop_book` false positive.
- **Friction points:** Operator named this chat’s session id (`01a07e4c`) when meaning the lag-retry session (`01a079fd`). Wv2 tree mixed with an in-flight ecosystem-view session.
- **Subagent usage:** _None._

---

## 14. Follow-up Actions

- [ ] BG L3 split-like stop-market send hold — already on [`2026-08-22-corporate-action-stop-safeguards.md`](../tickets/2026-08-22-corporate-action-stop-safeguards.md) — owner: later, after `order_write`
- [ ] Classify remaining 271 parquet jumps; do not universe-APPLY — [`2026-09-07-classify-remaining-split-jump-parquet.md`](../tickets/2026-09-07-classify-remaining-split-jump-parquet.md) — owner: next data hygiene pass
- [ ] Optional: new Mint S2 pair on current parquet (do not overwrite 536/537) — [`2026-09-07-mint-s2-rescore-after-ung-weat-amcr.md`](../tickets/2026-09-07-mint-s2-rescore-after-ung-weat-amcr.md) — owner: operator

---

## 15. Appendix

Active book scan 2026-09-07: `active_book_jumps=0 of 81 symbols`.

Universe: `scanned=2716 symbols_with_jumps=271`.

Override codes: `tradable_gap`, `broker_print`. Generic notes that do **not** count: `confirmed via ops shell`, `desk workflow confirm`, `desk form confirm`, `desk confirm`, `desk workflow`, `exit via ops shell`, `desk exit`, `desk workflow exit`.
