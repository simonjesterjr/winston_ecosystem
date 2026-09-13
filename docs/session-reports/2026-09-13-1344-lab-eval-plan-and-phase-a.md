# Session Report — Lab eval plan lock + Phase A harness

**Date:** 2026-09-13
**Time:** ended 13:44 MDT (start not recorded)
**Duration:** multi-hour (plan grill + Phase A); wall clock not measured
**Project:** Sawtooth / Winston ecosystem
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `ecosystem` `main` (dirty); `winston_unit_test` `main` (dirty). Sawtooth **root is not a git repo** (`compose.yml` lives there).
**Model:** Grok 4.6
**Operator:** John

---

## 1. Goal & Outcome

**Stated goal:** Judge whether the librarian vault “Winston lab eval — Grok CLI plan” was implementable as-is; file an ecosystem-sourced plan; ask Phase A–D questions; then (after locks) implement **Phase A** under the general-contractor pattern.

**Outcome:** Delivered (Phase A). Phases B–D not started.

**One-line summary:** Lab eval is now sourced in `ecosystem/plans/winston-lab-eval-grok-cli.md`; Phase A harness can create an idempotent smoke Portfolio Backtest Run (PBR) without running the hours-long backtest; Grok Bot still owns the 32-cell user-acceptance test (UAT) after MCP exists.

---

## 2. Work Completed

- Read vault notes (`Winston lab eval — Grok CLI plan`, `Winston MCP — Grok Bot access`, Measuring Edge) against sawtooth (ADR-015, `EdgeCalculator`, existing MCP, WUT internals).
- **Verdict:** not implementable as-is (vault would fork Edge (R); `testing_strategies` is the wrong list).
- Operator locks: 32-cell turtle panel as UAT surface; Grok Bot builds that panel; Phase A = harness + smoke only; Shell-on-sawtooth; Cromwell does not start PBRs.
- Filed authoritative plan + overlap table; patched sibling MCP/staff/LLM plans so this file wins on experiment-control MCP.
- Phase A: config JSON, compose analysis bind, `LabEval::*` services + rails-runner scripts + specs.
- Smoke: created **pending PBR #596** (`mint_rst_turtle_r01`, parent #432). Re-run skipped it. **Did not execute** the backtest.
- Clarified that smoke vs execute distinction in chat (operator did not need to re-run the setup command).

---

## 3. Code Delivered

### Files changed

**This session only** (other dirty files in both repos predate this work — Edge (R) scoreboard, ADR-015, tickets, etc. — do not mix into a lab-eval commit).

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/plans/winston-lab-eval-grok-cli.md` | added | Authoritative plan + schema appendix |
| `ecosystem/plans/winston-mcp-immediate.md` | modified | Marked shipped; pointer to lab-eval |
| `ecosystem/plans/winston-mcp-next-steps.md` | modified | Lab PBR execute not this slice |
| `ecosystem/plans/winston-mcp-next-steps.md.tasks.json` | modified | Task 11 note + task 18 pointer |
| `ecosystem/plans/cromwell-ai-skills-part2.md` | modified | `wut_get_run_summary` subsumed |
| `ecosystem/plans/cromwell-staff-roster.md` | modified (still **untracked**) | Lab Scout never starts PBRs; tool names superseded |
| `ecosystem/plans/winston-plus-llm.md` | modified | Edge math stays Ruby |
| `ecosystem/plans/loop-engineering-and-evolution-mode.md` | modified | Goal-loop gates = Edge (R) |
| `ecosystem/README.md` | modified | Lab-eval plan in “read first” |
| `ecosystem/interfaces/winston-mcp-tools.md` | modified | Forthcoming Wave 1 pointer (still v0.4) |
| `ecosystem/docs/analysis/strategy77-rst-heat-risk-v1.config.json` | added | 8×2×2 UAT config; smoke subset |
| `ecosystem/docs/analysis/strategy77-rst-heat-risk-v1.md` | added | Operator companion |
| `ecosystem/docs/analysis/2026-09-13-strategy77-rst-heat-risk-setup.json` | added | Smoke setup artifact |
| `compose.yml` | modified | Analysis bind on WUT + Sidekiq (**not in git** — sawtooth root) |
| `winston_unit_test/app/services/lab_eval/*.rb` | added | 8 files, each ≤65 lines |
| `winston_unit_test/lib/scripts/strategy_fill_heat_risk_matrix_{setup,execute,scorecard}.rb` | added | Thin runners |
| `winston_unit_test/spec/services/lab_eval/*` | added | 7 examples + config fixture copy |

### Commits

- _None this session._

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — dirty; `winston_unit_test` `main` — dirty
- Pushed: no
- PR: not opened

---

## 4. Decisions Made

### Decision 1: Ecosystem plan is SOT; vault is historical
- **Choice:** File `winston-lab-eval-grok-cli.md`; do not treat librarian notes as contract.
- **Why:** Vault missed ADR-015 / `edge_v1` and wrapped the wrong WUT list endpoint.
- **Alternatives considered:** Implement vault as-is; keep vault as dual SOT.
- **Reversibility:** easy (docs)
- **Promote to ADR?** no

### Decision 2: 32-cell turtle panel is UAT, not Phase A science
- **Choice:** 8 books × 2 heat × 2 risk × `resting_stop_touch`. Grok Bot builds it via MCP after B+C. Grok CLI smoke = 1 pending cell.
- **Why:** The workstream is a second **evaluation path**, not a CLI bakeoff.
- **Alternatives considered:** Thin 12-cell CLI matrix; execute 32 now.
- **Reversibility:** easy until UAT cells exist
- **Promote to ADR?** no

### Decision 3: Shell-on-sawtooth only (no Funnel / Serve `/mcp`)
- **Choice:** Grok Bot hop = Shell. MCP stays compose-internal.
- **Why:** No access/speed gap Funnel would fix; trust boundary already deferred 2026-09-13.
- **Alternatives considered:** Tailscale Serve; Funnel.
- **Reversibility:** easy
- **Promote to ADR?** only if Funnel is later chosen

### Decision 4: Builder vs Desk for PBR execute
- **Choice:** `wut_execute_portfolio_backtest_run` (Builder / Grok Bot). Cromwell Lab Scout does **not** start PBRs. Name `wut_start_pbr` superseded. GPU gate = Desk autonomous start, not Builder UAT.
- **Why:** Staff roster WAN/CPU constraints vs operator-initiated lab UAT.
- **Alternatives considered:** Cromwell Lab Scout execute; wait for GPU.
- **Reversibility:** medium (tool names / cron allowlist)
- **Promote to ADR?** no — record in staff roster + lab-eval plan is enough

### Decision 5: Phase A smoke = create pending, not execute
- **Choice:** Stamp PBR #596; do not run `PortfolioBacktestRunner`.
- **Why:** Full-window Mint Turtle replay is hours of CPU; not a harness check.
- **Alternatives considered:** Sync-execute one cell before Phase B.
- **Reversibility:** easy (execute #596 later)
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- `GET /internal/testing_strategies` lists **TradingSignalStrategy** (signal classes), not `TradingStrategy` rows. Lab list tool needs a **new** endpoint.
- WUT `risk_percentage` is a **fraction** (`0.01` = 1%). Wv2 importer percent convention is a different store.
- `EdgeCalculator` / `edge_components` already persist on PBR complete — scorecard must not invent `expectancy_r`.
- Factory `seed_heat_from_trading_strategy!` will re-apply turtle heat unless setup **overwrites** `heat` (legacy must stamp JSON `null` with the key present).
- Compose analysis bind works, but **recreating `winston_unit_test` requires removing `winston_mcp` then `nanobot_cromwell` first** (`--requires`). `bin/compose up` also stopped redis/Wv2/DM as a side effect of podman-compose recreate; stack was started again.
- Sawtooth root (`compose.yml`) is not a git repository — compose volume change is only on disk until some other home is chosen.

---

## 6. Issues & Tickets

### Resolved this session
- _None as filed issues._ Plan implementability gaps were absorbed into `winston-lab-eval-grok-cli.md`.

### Deferred
- Phase B: WUT `/internal/...` + MCP Wave 1–2 (`wut_create_portfolio_backtest_run`, execute, edge report, …).
- Phase C runbook `ecosystem/docs/operations/grok-bot-shell-lab-eval.md` + optional `bin/lab-eval`.
- Phase D Grok Bot briefs (Lab Sweep / Edge Scorecard).
- Optional overnight execute of PBR #596 (not a Phase B gate).
- `cromwell-staff-roster.md` still untracked in `ecosystem` git.
- `compose.yml` not versioned at sawtooth root.
- Walk-forward / cost stress remain TF P1 (`2026-09-04-tf-p1-residual-signal-and-oos.md`).

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| `LabEval` unit specs | `bin/compose exec -T winston_unit_test bundle exec rspec spec/services/lab_eval --format documentation` | ✅ 7 examples, 0 failures (pre-existing `db:test:load` noise to `::1:5432`; examples do not need test DB) |
| Smoke setup | rails runner setup script | ✅ created PBR **#596** pending `mint_rst_turtle_r01` parent **#432** |
| Idempotent re-run | same setup script again | ✅ skipped #596 |
| Artifact on host bind | `ecosystem/docs/analysis/2026-09-13-strategy77-rst-heat-risk-setup.json` | ✅ after WUT recreate with analysis mount |
| Config resolve in container | `LabEval::Config.resolve` | ✅ `/ecosystem/docs/analysis/strategy77-rst-heat-risk-v1.config.json` |
| Backtest execute | `PortfolioBacktestRunner` on #596 | ⚠️ **not run** (hours; deferred) |
| MCP tools | — | ❌ not this session |
| Graphify Graph refresh | `/wrap` step 2 | ⚠️ pending wrap |

**Test command(s):**

```bash
./bin/compose exec -T winston_unit_test bundle exec rspec spec/services/lab_eval --format documentation
./bin/compose exec -T winston_unit_test bin/rails runner lib/scripts/strategy_fill_heat_risk_matrix_setup.rb
```

PBR #596 confirmed still `pending` at 13:45 MDT.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new.
- **Services:** Recreated `winston_unit_test` + `winston_unit_test_sidekiq` with analysis bind. Required rm of `winston_mcp` then `nanobot_cromwell`. podman-compose also bounced redis/postgres/WUT PG/Wv2/DM/ollama; those were started again. Live lab DB: new pending PBR **#596** (no migration).
- **Migrations:** None this session.

---

## 9. Risks & Technical Debt

- Dirty trees in `ecosystem` and `winston_unit_test` mix **this session** with unrelated Edge (R) / ticket work — easy to commit the wrong files.
- Spec fixture copies the experiment JSON (`spec/services/lab_eval/strategy77-rst-heat-risk-v1.config.json`); can drift from `ecosystem/docs/analysis/`.
- `LabEval::Finder` scans PBRs with `find_each` (same pattern as turtle_systems_v1). Fine at current N; not indexed JSON query.
- Recreating WUT is operationally sharp (MCP `--requires`). Documented in the companion md; easy to knock Telegram/Cromwell if done carelessly.
- `compose.yml` change has no git home at sawtooth root.

---

## 10. Open Questions

- **Execute PBR #596 overnight before Phase B?** — operator; does not block B.
- **Commit strategy:** separate lab-eval commits vs leave dirty — operator; blocks durable handoff.
- **When to start Phase B** — operator; next implementation slice.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Phase A accepted. Smoke cell #596 pending. Operator asked what “not executed” meant; clarified; `/session-report` (this file). **Not** `/wrap` (no Graphify refresh, no commit/push).
- **Next concrete step:** Phase B Wave 1 — new WUT internals + thin MCP wrappers per plan appendix (`wut_list_trading_strategies` ≠ `testing_strategies`; execute default async). Do not `FULL=1` setup of 32 cells.
- **Files to read first:**
  1. `ecosystem/plans/winston-lab-eval-grok-cli.md`
  2. `ecosystem/docs/analysis/strategy77-rst-heat-risk-v1.md`
  3. `winston_unit_test/app/services/lab_eval/setup.rb` + `stamper.rb`
  4. `ecosystem/interfaces/winston-mcp-tools.md` (v0.4 + forthcoming note)

---

## 12. Stakeholder Communications

- _None._ Internal lab/MCP path; report-only; no pack promotion; no capital action.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, graphify query (session start), session-report. Ponytail applied in contractor prompt (not `/ponytail`). GC pattern: two subagents, disjoint files.
- **Graphify Graph:** **pending wrap.** Graphs exist: `graphify-out/graph.json`, `ecosystem/graphify-out/graph.json`, `winston_unit_test/graphify-out/graph.json` (stamps ~12:45 MDT, before Phase A files).
- **Ponytail flags:** none in new Ruby (`# ponytail:` not used). Finder O(n) scan is inherited pattern.
- **What worked well:** GC wrote the config JSON first as the contract; WUT vs ecosystem contractors did not collide. Operator locks (32-cell UAT, Shell-only, no Cromwell execute) kept Phase A small.
- **Friction points:** Vault vs ADR-015 mismatch. podman-compose recreate of WUT is not `--no-deps` in practice and took down dependents. First setup write landed in container overlay because the bind was not mounted yet.
- **Subagent usage:** `Compose analysis volume` (ecosystem); `WUT LabEval harness` (WUT). GC integrated, fixed `WRITE=1` env passing, `EXECUTE=1` on setup, `edge_components` on scorecard, config resolve fallback, then smoke.

---

## 14. Follow-up Actions

- [ ] Phase B Wave 1–2 (WUT internal API + MCP) — owner: Grok CLI / GC — due: when operator starts B
- [ ] Phase C Shell runbook — owner: Grok CLI — due: after A (can overlap B)
- [ ] `/wrap` Graphify refresh + commit of **this session’s** files only — owner: operator + agent — due: before or with Phase B
- [ ] Optional: execute PBR #596 overnight — owner: operator — due: not a B gate
- [ ] Grok Bot UAT 32-cell panel (`FULL=1`) — owner: Grok Bot — due: after B+C
- [ ] Track `cromwell-staff-roster.md` and `compose.yml` in some git home — owner: operator — due: unset

---

## 15. Appendix

**Cell key scheme:** `{book}_{rst}_{heat}_{r01|r02}` e.g. `mint_rst_turtle_r01`. Smoke = Mint × turtle × 0.01. `FULL=1` = 32 cells.

**Smoke PBR:** `#596` pending, `experiment=strategy77_rst_heat_risk_v1`, parent `#432`.

**Do not:** `FULL=1` on live DB in Phase A; Cromwell cron mutating lab tools; Funnel; pack promotion.

**Vault sources (historical):**  
`typewriter/librarian/koisch-jr/winston_foundations/Winston lab eval — Grok CLI plan.md`  
`typewriter/librarian/koisch-jr/winston_foundations/Winston MCP — Grok Bot access.md`
