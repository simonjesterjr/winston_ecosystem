# Session Report — Lab eval Phase B (MCP Wave 1–2)

**Date:** 2026-09-13
**Time:** 13:45–14:09 MDT
**Duration:** ~25m wall (agent contractors longer)
**Project:** Sawtooth / Winston ecosystem
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `ecosystem` `main` (dirty); `winston_unit_test` `main` (dirty). Sawtooth root is not a git repo.
**Model:** Grok 4.6
**Operator:** John

**Prior report:** [`2026-09-13-1344-lab-eval-plan-and-phase-a.md`](2026-09-13-1344-lab-eval-plan-and-phase-a.md) (plan lock + Phase A harness). This file is **Phase B only**.

---

## 1. Goal & Outcome

**Stated goal:** Skip session-report follow-up tickets; start Phase B under the general-contractor pattern (WUT internals vs thin MCP).

**Outcome:** Delivered (Wave 1–2). Wave 3–4 and live execute of PBR #596 not in scope.

**One-line summary:** Grok Bot can now create/list/get lab Portfolio Backtest Runs and Edge (R) reports through Winston MCP; the Mint smoke cell #596 is still pending and was not executed.

---

## 2. Work Completed

- Operator: `skip all` on §14 of the 13:44 report.
- GC spawned two contractors (disjoint files): WUT HTTP API; MCP wrappers + interface v0.5.
- WUT: `Internal::LabEvalController` + `LabEval::*` API services; routes under `/internal/...`.
- MCP: 10 new `wut_*` lab-eval tools; mutating tools require `authorization: lab_geometry_report_only`; **not** added to Cromwell cron allowlist.
- Rebuilt `winston_mcp` image; recreated `winston_mcp` + `nanobot_cromwell`.
- Live smoke: HTTP + MCP get #596 pending; create **reused** #596. **Did not** call execute (would enqueue the hours-long Mint book).
- Plan `winston-lab-eval-grok-cli.md` marked Wave 1–2 landed.

---

## 3. Code Delivered

### Files changed

**Phase B (this slice)**

| File | Change | Notes |
|------|--------|-------|
| `winston_unit_test/config/routes.rb` | modified | +12 lab-eval routes |
| `winston_unit_test/app/controllers/internal/lab_eval_controller.rb` | added | Thin; CSRF skipped; 35 lines |
| `winston_unit_test/app/services/lab_eval/api_error.rb` | added | Auth token |
| `winston_unit_test/app/services/lab_eval/run_summary.rb` | added | Locked RunSummary keys |
| `winston_unit_test/app/services/lab_eval/list_strategies.rb` | added | TradingStrategy rows, not signal classes |
| `winston_unit_test/app/services/lab_eval/create_run.rb` | added | Finder reuse + Stamper |
| `winston_unit_test/app/services/lab_eval/stamp_knobs.rb` | added | Pending-only fill/heat/risk |
| `winston_unit_test/app/services/lab_eval/enqueue.rb` | added | `PortfolioBacktestJob.perform_later` only |
| `winston_unit_test/app/services/lab_eval/list_cells.rb` | added | |
| `winston_unit_test/app/services/lab_eval/edge_report.rb` | added | `edge_v1` + heat_skips |
| `winston_unit_test/app/services/lab_eval/compare_runs.rb` | added | Rank by `edge_r`; report-only note |
| `winston_unit_test/spec/requests/internal_lab_eval_spec.rb` | added | |
| `winston_unit_test/spec/services/lab_eval/{create_run,stamp_knobs,enqueue,compare_runs,edge_report}_spec.rb` | added | |
| `ecosystem/ai/mcp/mcp_winston/server.py` | modified | +~487 lab tools/dispatch |
| `ecosystem/ai/mcp/mcp_winston/tools_schema.py` | modified | `LAB_AUTHORIZATION_SCHEMA`, `HEAT_CONFIG_SCHEMA` |
| `ecosystem/ai/mcp/mcp_winston/errors.py` | modified | Retry hints for lab tools |
| `ecosystem/interfaces/winston-mcp-tools.md` | modified | **v0.5** WUT lab eval section |
| `ecosystem/plans/winston-lab-eval-grok-cli.md` | modified | Wave 1–2 landed notes |

Phase A harness files (`LabEval::{Config,Stamper,Setup,...}`, rails-runner scripts, analysis JSON, `compose.yml` bind) remain uncommitted from the 13:44 report — do not mix with unrelated dirty files in either repo.

### Commits

- _None._

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — dirty; `winston_unit_test` `main` — dirty
- Pushed: no
- PR: not opened

---

## 4. Decisions Made

### Decision 1: New controller, do not grow `InternalController`
- **Choice:** `Internal::LabEvalController`
- **Why:** Existing internals file is already large; 65-line rule.
- **Alternatives considered:** Add actions to `InternalController`.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 2: Live execute smoke skipped
- **Choice:** Specs cover enqueue; do not `perform_later` PBR #596 on Sidekiq.
- **Why:** Full-window Mint Turtle replay is hours of CPU.
- **Alternatives considered:** Enqueue and let it run overnight.
- **Reversibility:** easy (call `wut_execute_portfolio_backtest_run` later)
- **Promote to ADR?** no

### Decision 3: `wut_get_trades` stays P1
- **Choice:** Wave 2 ships edge report + compare only.
- **Why:** Plan listed trades as P1; UAT surface does not need lot dumps yet.
- **Alternatives considered:** Thin trades endpoint now.
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Host curl to `http://127.0.0.1:3000/internal/...` works (Tailscale `/wut` prefix is stripped on inbound). MCP uses the same unprefixed `/internal` paths via compose DNS.
- Create idempotency is `experiment` + `cell_key` via `LabEval::Finder` — MCP UAT can retry safely.
- `podman-compose up --no-deps winston_mcp` still tried to recreate WUT/Wv2/DM/redis; required `podman start` afterward. Recreating MCP still needs `nanobot_cromwell` removed first (`--requires`).
- Compare on experiment `strategy77_rst_heat_risk_v1` has **no winner** while the only cell (#596) is pending — expected.

---

## 6. Issues & Tickets

### Resolved this session
- _None filed._ Operator skipped all tickets from the 13:44 report.

### Deferred
- Phase C: Shell runbook `ecosystem/docs/operations/grok-bot-shell-lab-eval.md` (+ optional `bin/lab-eval`).
- Phase D: Grok Bot Lab Sweep / Edge Scorecard briefs.
- UAT 32-cell `FULL=1` panel (Grok Bot after C).
- Optional execute of PBR #596.
- `wut_get_trades`, Wave 3 attribution, Wave 4 book builder.
- `/wrap` Graphify + commit of lab-eval files only.
- `compose.yml` still not in a git repo (sawtooth root).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| WUT LabEval + request specs | `bin/compose exec -T winston_unit_test bundle exec rspec spec/services/lab_eval spec/requests/internal_lab_eval_spec.rb` | ✅ 23 examples, 0 failures (contractor; pre-existing `db:test:load` noise) |
| HTTP GET `/internal/trading_strategies` | curl name_contains=TurtleV1 | ✅ TS rows (not signal classes) |
| HTTP GET PBR 596 | curl | ✅ pending `mint_rst_turtle_r01` |
| HTTP POST create same cell | curl + auth | ✅ `action: reused` #596 |
| HTTP POST without auth | curl | ✅ 422 `unauthorized` |
| HTTP edge_report #432 | curl | ✅ `status ok`, `edge_r` present (`edge_n` may be blank on old rows) |
| HTTP compare experiment | curl | ✅ report-only note; winner nil (pending-only cell) |
| MCP tool list | `list_tools` in `winston_mcp` | ✅ 16 `wut_*` including 10 lab-eval names |
| MCP get + create | `call_tool` | ✅ GET596 pending; CREATE reused 596 |
| MCP execute live | — | ⚠️ **not called** |
| Cron allowlist | grep | ✅ `wut_execute` absent |
| Graphify Graph | — | ⚠️ pending wrap (stamps still 12:45 MDT) |

**Test command(s):**

```bash
./bin/compose exec -T winston_unit_test bundle exec rspec spec/services/lab_eval spec/requests/internal_lab_eval_spec.rb --format documentation
curl -sS "http://127.0.0.1:3000/internal/portfolio_backtest_runs/596"
podman exec winston_mcp python3 -c '...'  # list_tools + call_tool get/create
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (MCP image rebuilt from existing `mcp` 1.x pins).
- **Services:** Rebuilt `sawtooth_winston_mcp`; recreated `winston_mcp` + `nanobot_cromwell`. Compose `up --no-deps` also bounced WUT/Wv2/DM/redis; those were started again. Analysis bind on WUT still present. Lab DB: **no new PBR**; #596 still pending.
- **Migrations:** None.

---

## 9. Risks & Technical Debt

- Dirty trees still mix lab-eval with unrelated Edge (R) / ticket work — commit with a path allowlist.
- Live execute of #596 would occupy WUT Sidekiq for hours if someone calls the MCP tool.
- Historical PBRs may have `edge_r` without `edge_n` (edge_report showed n None on #432).
- podman-compose recreate remains operationally sharp.

---

## 10. Open Questions

- **Start Phase C (Shell runbook) now?** — operator; next product slice.
- **Enqueue #596 overnight?** — operator; not a C/D gate.
- **Commit/wrap before C?** — operator; Graphify still stale.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Phase B Wave 1–2 live. MCP get/reuse #596 works. Execute not called. Phase C/D not started. This `/session-report` only (not `/wrap`).
- **Next concrete step:** Phase C — `ecosystem/docs/operations/grok-bot-shell-lab-eval.md` documenting Shell hop: `compose exec` rails runners **or** `podman exec winston_mcp` / MCP SSE from inside compose. Then Grok Bot briefs (Phase D). Do **not** `FULL=1` 32 cells until UAT.
- **Files to read first:**
  1. `ecosystem/plans/winston-lab-eval-grok-cli.md` (Wave 1–2 landed)
  2. `ecosystem/interfaces/winston-mcp-tools.md` (v0.5, section **WUT lab eval**)
  3. `winston_unit_test/app/controllers/internal/lab_eval_controller.rb`
  4. Prior report `2026-09-13-1344-lab-eval-plan-and-phase-a.md`

---

## 12. Stakeholder Communications

- _None._ Lab geometry / report-only; no pack promotion; no capital path.

---

## 13. Tools & Workflow Notes

- **Skills used:** session-report. GC + two general-purpose contractors. Ponytail in prompts (65-line Ruby).
- **Graphify Graph:** **pending wrap.** Graphs exist but stamps are 12:45 MDT (before Phase A and B files).
- **Ponytail flags:** none (`# ponytail:` not added).
- **What worked well:** Locked HTTP contract in both contractor prompts so they could run in parallel. MCP create reuse proved the API without a second PBR.
- **Friction points:** MCP image is not bind-mounted — must rebuild. `podman-compose --no-deps` still recreates dependents’ requirements.
- **Subagent usage:** `WUT lab-eval internal API`; `MCP lab-eval thin tools`. GC reviewed, smoked HTTP, rebuilt MCP, smoked `call_tool`.

---

## 14. Follow-up Actions

- [ ] Phase C Shell runbook — owner: Grok CLI — due: when operator starts C
- [ ] Phase D Grok Bot briefs — owner: operator + Grok CLI — due: after C (or after A+C per plan)
- [ ] Optional execute PBR #596 — owner: operator — due: not a gate
- [ ] `/wrap` Graphify + commit lab-eval paths only — owner: operator + agent — due: unset
- [ ] `wut_get_trades` / Wave 3–4 — owner: Grok CLI — due: later per plan

---

## 15. Appendix

**MCP WUT tools after rebuild (16):**  
`wut_add_market`, `wut_compare_runs`, `wut_create_portfolio_backtest_run`, `wut_execute_portfolio_backtest_run`, `wut_get_daily_operations_report`, `wut_get_portfolio_backtest_run`, `wut_get_run_edge_report`, `wut_list_experiment_cells`, `wut_list_portfolio_runs`, `wut_list_portfolios`, `wut_list_trading_strategies`, `wut_run_daily_operations`, `wut_set_fill_cadence`, `wut_set_heat`, `wut_set_risk`, `wut_sync_portfolio_data`

**Auth constant:** `lab_geometry_report_only`

**Do not:** `FULL=1` 32-cell panel; Cromwell cron execute; Funnel; pack promotion.
