# Plan: Winston lab eval (Strategy 77 × resting stop-touch × heat × risk)

**Status:** Operator-locked 2026-09-13 — **authoritative** for WUT lab experiment-control MCP, Edge (R) scoreboard tools, Grok Bot lab UAT, and Shell-on-sawtooth as the Bot hop.  
**Date:** 2026-09-13  
**Type:** Cross-monolith implementation plan (lab geometry / report-only)  
**Mode:** contractor (GC files the plan; Winston Unit Test is the lab contractor for A/B)  
**UAT owner:** Grok Bot (Builder plane), via MCP first; Shell-on-sawtooth is the inelegant but sufficient bridge  
**Interface (when B ships):** `interfaces/winston-mcp-tools.md` (still v0.4 until Wave 1)  
**Vault sources (historical, not SOT):**
- `typewriter/librarian/koisch-jr/winston_foundations/Winston lab eval — Grok CLI plan.md`
- `typewriter/librarian/koisch-jr/winston_foundations/Winston MCP — Grok Bot access.md`
**Sawtooth SOT to keep:** ADR-015, `interfaces/winston-edge-v1.md`, `docs/business-context/measuring-edge.md`, ticket `2026-09-11-measuring-edge-scoreboard.md`, ticket `2026-08-20-wut-resting-stop-touch-fill-cadence`, `business_analysis/2026-08-12-turtle-systems-and-heat.md`

---

## Related plans (overlap — this file wins)

Where another plan names WUT PBR create/execute, lab scorecards, or Grok Bot vs Cromwell ownership of lab science, **this file is correct**. Sibling plans keep their own remaining scope.

| Plan | Relationship | What remains there |
|------|----------------|-------------------|
| [`winston-mcp-immediate.md`](winston-mcp-immediate.md) | **Shipped.** Architecture invariants inherited (thin MCP, compose-internal, no public ports, no business logic in Python). Not subsumed. | Wv2 core tools + optional `ai` profile. |
| [`winston-mcp-next-steps.md`](winston-mcp-next-steps.md) | **Does not own** lab experiment-control tools. The “list recent good backtest runs / vetted TS” bullet is **split** (below). | Cromwell/Telegram polish; DM sync; transfer-smarter **read** listing; docs for ops MCP. |
| [`cromwell-ai-skills-part2.md`](cromwell-ai-skills-part2.md) | Phase 2C `wut_get_run_summary` is **subsumed** by `wut_get_portfolio_backtest_run`. Do **not** add a second contract file `wut-mcp-tools.md`. | `wut_list_vetted_runs` as a **read filter** for Wv2 transfer; DM coverage tools; Cromwell skills. |
| [`cromwell-staff-roster.md`](cromwell-staff-roster.md) | Lab Scout **must not** start PBRs (CPU or Telegram). Tool name `wut_start_pbr` is **superseded** by `wut_execute_portfolio_backtest_run`. `wut_get_pbr_scorecard` (return/DD) is **superseded** by `wut_get_run_edge_report` (`edge_v1`). GPU gate applies to **Desk autonomous start**, not Builder/Grok Bot UAT. | Ops Steward, process-eval, watchdog/`/status`, WAN-forbidden **for Cromwell**. |
| [`winston-plus-llm.md`](winston-plus-llm.md) | Lab eval is **not** native LLM in WUT. Edge math stays Ruby (`EdgeCalculator`). | Journal notes, RAG, Cromwell planning. |
| [`loop-engineering-and-evolution-mode.md`](loop-engineering-and-evolution-mode.md) | Instrumentation for WUT goal-loops; **not** Evolution Portfolios / paper autofill. | Evolution lane (later). |

**Split (next-steps / Part 2C vs this plan):**

| Need | Owner |
|------|--------|
| Create / stamp / execute PBR; experiment cells; heat/risk/fill knobs | **This plan** |
| Edge (R) report + compare + trades | **This plan** (`edge_v1`, not equity cosmetics) |
| List TradingStrategy rows (lab) | **This plan** `wut_list_trading_strategies` — **not** `GET /internal/testing_strategies` (those are signal classes) |
| List “vetted / exportable” runs for Wv2 transfer | Part 2C / next-steps `wut_list_vetted_runs` (read-only filter) |
| Wv2 live ops MCP | immediate + next-steps (unchanged) |

---

## Verdict

The librarian vault brief is the right **product intent** (Grok Bot evaluates Winston through MCP / API, not the WUT GUI). It was **not** implementable as-is against sawtooth: Edge (R) already ships (ADR-015), WUT internals for PBR create/execute do not exist on MCP, and `testing_strategies` is the wrong list.

**What this workstream is for:** a second evaluation path. Grok CLI builds harness + WUT internals + thin MCP. **Grok Bot builds the 32-cell matrix as UAT** after Phase B and C. Grok CLI does not run the science panel (smoke exceptions only).

---

## Operator locks (2026-09-13)

| Decision | Lock |
|----------|------|
| **UAT panel (problem surface)** | Turtle 8-book × 2 heat × 2 risk × `resting_stop_touch` only = **32 cells**. Books: Blue, Mango, Mint, Yellow, Orange, Red, Green, Rust. Heat: `legacy` vs `turtle` (`PortfolioHeatConfig::TURTLE_DEFAULTS`). Risk: WUT fractions `0.01` and `0.02`. |
| **Who builds that panel** | **Grok Bot**, via MCP/API, as UAT. Grok CLI may use **testing exceptions** (1–2 smoke cells) to prove stamps. Do not Grok-CLI-stamp or execute the 32. |
| **Phase A execute** | **Setup harness only.** Full execute is UAT after B+C. |
| **Window / parent** | Per-book turtle_systems_v1 **S2** parent PBR (`experiment=turtle_systems_v1`, `cell_key=B1`). Inherit overlapping dates + $10k chassis. Not Mint-432 for every book. Not Mint 537 window forced onto all books. |
| **Phase C** | **Shell-on-sawtooth only** for now and the immediate future. No Tailscale Serve `/mcp`, no Funnel. Inelegant; no access/speed/function gap that Funnel would fix for this work. |
| **Phase D** | **Grok Bot skills + Shell.** Cromwell does **not** start PBRs. Lab Scout stays recommendation-only. |

---

## Goal

Using Trading Strategy (TS) **#77** (`TurtleV1 S2 Breakout55/20`), fills at `resting_stop_touch`, knobs **max-risk** + **variable heat**, against the turtle 8-book panel: **what is the best Edge (R), and why does it work on portfolio X?** Answered by **Grok Bot UAT**, not a Grok CLI bakeoff session.

Then: more strategies; later **build** books that show that edge (Wave 4).

**Doctrine:** Lab geometry / report-only. No Broker Gateway `order_write`. No pack-default promotion without scored walk-forward. Edge = ADR-015 / `winston-edge-v1`, not equity cosmetics.

**Non-goals:** live Cromwell desk fills; Funnel/public MCP; rewriting Measuring Edge prose; a second edge formula; Cromwell cron starting PBRs; native LLM inside the scorecard.

---

## What already exists (vault missed)

| Fact | Evidence |
|------|----------|
| Edge (R), profit factor, lot 1R persist on PBR complete | `EdgeCalculator`, `persist_edge_snapshot!`, ADR-015, columns `edge_r` / `profit_factor` / `edge_n` / `edge_components` |
| E-ratio E10/E20/E50/E70 + lab random + DD duration + Sortino on the Edge Snapshot | `ERatioCalculator`, `EdgePathMetrics` |
| Costs are `fill_only` until a commission model exists | `interfaces/winston-edge-v1.md` |
| Heat L1–L4 + turtle defaults fingerprintable | `PortfolioHeatConfig::TURTLE_DEFAULTS`; passed-signal reasons `heat_market` / `heat_close_corr` / `heat_loose_corr` / `heat_direction` |
| Resting stop-touch + thin Mint/Yellow scorecard already ran | `resting_stop_touch_v1_{setup,scorecard}.rb`; Mint v1 ruin was reverse-split artifact (PBR 537 vs 536) |
| Matrix / sync-execute patterns | `turtle_systems_v1_*`, `kelly_hybrid_matrix_*`, `close_trigger_experiment_matrix.rb` (`PortfolioBacktestRunner.new(id).execute`) |
| MCP WUT is ops, not experiment control | list portfolios/runs, add_market, sync, daily ops only |
| `GET /internal/testing_strategies` is **signal classes**, not `TradingStrategy` | `InternalController#testing_strategies` |
| WUT compose does **not** mount `ecosystem/` | runner writes to `/ecosystem/...` fall through to `winston_unit_test/tmp` |
| Cromwell: WAN LLM forbidden; Desk must not start PBRs on CPU | `plans/cromwell-staff-roster.md` |

---

## Corrections vs vault

1. **Scoreboard = `edge_v1` snapshot.** No `LabEdgeReport` fork. Vault `expectancy_r` → **`edge_r`**. Rank by `edge_r`; glance rules n&lt;20 hide, 20–99 thin, ≥100 glance. Show thin cells marked. `costs=fill_only`.
2. **`wut_list_trading_strategies` ≠ `/internal/testing_strategies`.** New `GET /internal/trading_strategies`.
3. **Execute wait 120–600s is too short.** MCP default `wait: false`; poll get. Phase A smoke may sync-execute via `PortfolioBacktestRunner`.
4. **Heat schema** accepts `"turtle"` \| object \| null (legacy). Match `PortfolioHeatConfig.normalize`.
5. **WUT `risk_percentage` is a fraction** (`0.01` = 1%). Do not apply the Wv2 importer percent convention on lab stamps.
6. **Resolve TS by name** `TurtleV1 S2 Breakout55/20` (id 77 can drift).
7. **Parent window per book** from turtle_systems_v1 S2 PBR.
8. **UAT panel is the turtle 8**, not “all lab books.”
9. **`lab_geometry_report_only`** is an agent guardrail. Mutating MCP tools stay **off** Cromwell `cron-tool-allowlist.json`.
10. **Artifacts:** `ecosystem/docs/analysis/` for matrix JSON + md. `business_analysis/` only if a capital-relevant winner is ever claimed (not this UAT).
11. **MCP is HTTP-thin.** Logic in WUT. Recreate `winston_mcp` after schema changes (`docs/operations/recreate-winston-mcp.md`).
12. **65-line new Ruby.**
13. **Builder vs Desk:** Grok Bot / Grok CLI drive lab eval. Cromwell does not execute PBRs. Staff-roster GPU gate = Desk autonomous start, **not** Builder UAT.

---

## Phase A — Harness without MCP (Grok CLI)

**Owner:** Grok CLI.  
**Does not:** create or execute the 32-cell UAT panel.  
**Does:** checked-in config + setup/execute/scorecard scripts (and a WUT helper that MCP will reuse).

**Testing exceptions:** 1–2 smoke cells (e.g. Mint × turtle × 1%) — create pending, prove idempotency + stamps; optionally one sync execute to prove Edge Snapshot lands.

### A0. Write path

WUT cannot see `ecosystem/` today.

1. **Preferred:** compose bind `./ecosystem/docs/analysis:/ecosystem/docs/analysis:rw` on `winston_unit_test` (+ sidekiq if jobs write).
2. Else write `winston_unit_test/tmp/` (bind-mounted) and copy to `ecosystem/docs/analysis/` from the host.

### A1. Parameterized runner

`winston_unit_test/lib/scripts/strategy_fill_heat_risk_matrix_setup.rb` (module + thin script; do not clone a fourth 250-line twin).

Checked-in config, e.g. `ecosystem/docs/analysis/strategy77-rst-heat-risk-v1.config.json`:

| Knob | UAT value |
|------|-----------|
| TS | name `TurtleV1 S2 Breakout55/20` |
| `fill_cadence` | `resting_stop_touch` |
| Portfolios | Blue, Mango, Mint, Yellow, Orange, Red, Green, Rust |
| `heat_grid` | `legacy`, `turtle` |
| `max_risk_grid` | `0.01`, `0.02` |
| `experiment` | `strategy77_rst_heat_risk_v1` |
| Capital | `$10_000` |
| Window | per-book turtle S2 parent (`turtle_systems_v1` / `B1`) |

Chassis freeze: static, `move_to_last_entry`, ATR×2, pyramid 0.5N, max 4/12, no VolatilityExit, `ignore_first_signal`.

Behavior:

- Create **pending** PBRs; idempotent `experiment` + `cell_key`.
- Stamp fill/heat/risk/experiment meta + report-only note.
- Explicit `legacy` must stamp heat null/omit so factory seed from TS cannot silently re-apply turtle defaults.
- Default: **do not execute**. `EXECUTE=1` / `EXECUTE_IDS=` for smoke only.

Grok CLI runs this on **smoke allowlist**, not the full 8×2×2.

### A2. Execute harness (exists; not used for the 32 in Phase A)

Serial `PortfolioBacktestRunner.new(id).execute`; skip completed; print progress. Bot UAT may use this via Shell until MCP Wave 1 execute exists; **preferred UAT path is MCP execute**.

### A3. Scorecard script (Bot runs it after UAT executes)

`WRITE=1` → `ecosystem/docs/analysis/YYYY-MM-DD-strategy77-rst-heat-risk-matrix.json` + sibling `.md`.

Read `edge_components` (recompute only if blank). Include heat-skip aggregates from `passed_signals`. Rank by `edge_r`. Banner: **report only — no pack promotion**. Walk-forward stays on TF P1.

### A4. Acceptance (Phase A)

- [x] Config checked in for the **32-cell UAT panel** (`ecosystem/docs/analysis/strategy77-rst-heat-risk-v1.config.json`)
- [x] Setup/execute/scorecard scripts exist; idempotent re-run does not duplicate (`LabEval::*`, smoke skip PBR #596)
- [x] Scorecard schema in md header uses `edge_v1` keys
- [x] Optional: 1 smoke cell created **pending** (`mint_rst_turtle_r01` PBR #596, parent #432). Not executed (full-window Turtle book).
- [x] **32 pending/completed UAT cells are not a Phase A deliverable**
- [x] No MCP tools, no Funnel, no pack promotion, no BG

---

## Phase B — MCP / internal API (the UAT surface)

**Owner:** Grok CLI. WUT `/internal/...` + thin `mcp_winston`.  
**Contract when implementing:** bump `ecosystem/interfaces/winston-mcp-tools.md` past v0.4 using the appendix below.

### B0

A3 helpers → small WUT service (serialize Edge Snapshot + heat skips). MCP does not reimplement math.

### B1. Wave 1 — Experiment control (P0) — **required before Bot UAT execute**

| Tool | WUT surface |
|------|-------------|
| `wut_list_trading_strategies` | **New** `GET /internal/trading_strategies` |
| `wut_get_portfolio_backtest_run` | `GET /internal/portfolio_backtest_runs/:id` |
| `wut_create_portfolio_backtest_run` | `POST /internal/portfolio_backtest_runs` |
| `wut_set_fill_cadence` / `wut_set_heat` / `wut_set_risk` | pending PBR only |
| `wut_execute_portfolio_backtest_run` | enqueue `PortfolioBacktestJob`; default async |
| `wut_list_experiment_cells` | filter `results_json.experiment` |

Mutating tools: `authorization: "lab_geometry_report_only"`. Off Cromwell cron allowlist.

**Verify (CLI smoke, not the 32):** MCP creates one TS#77 × Mint × resting × turtle × 1% cell, execute accepted, get returns status (and `edge_r` if completed).

**Landed 2026-09-13:** WUT `Internal::LabEvalController` + MCP v0.5 tools. Live: `wut_get_portfolio_backtest_run` #596 pending; create **reused** #596. **Execute not called** (would enqueue the hours-long Mint book). Cron allowlist unchanged.

### B2. Wave 2 — Measuring Edge (P0)

`wut_get_run_edge_report`, `wut_compare_runs`; `wut_get_trades` P1.

**Verify:** compare on smoke cells matches A3 script (± float).

**Landed 2026-09-13:** `wut_get_run_edge_report` / `wut_compare_runs` HTTP + MCP. Compare on experiment `strategy77_rst_heat_risk_v1` returns report-only note; winner nil while #596 is pending. `wut_get_trades` still P1 / not shipped.

### B3. Wave 3 — Attribution (P1)

`wut_get_portfolio_structure` (reuse `GET /internal/correlation_scores` where possible), `wut_get_heat_skips`, `wut_explain_run_vs_run`.

### B4. Wave 4 — Book builder (P2, later)

`wut_create_portfolio`, `wut_clone_portfolio_markets`. Existing `wut_add_market` remains.

### B5–B6

Update interface doc; recreate `winston_mcp`; specs; no business logic in Python; Cromwell/live tools unchanged.

---

## Phase C — Shell-on-sawtooth (locked)

No host port, no Serve `/mcp`, no Funnel.

1. Runbook `ecosystem/docs/operations/grok-bot-shell-lab-eval.md` — `bin/compose exec -T winston_unit_test bin/rails runner ...` and how to invoke MCP **from inside compose** (curl SSE to `http://winston_mcp:8088` via `compose exec`).
2. Artifact paths under `ecosystem/docs/analysis/`
3. Optional `bin/lab-eval` (setup / execute / score / list-cells) for one Shell call
4. **Honest constraint:** Grok Bot cloud cannot call `winston_mcp` directly. Shell-on-sawtooth **is** the hop. MCP is still the structured API the hop should invoke once B1 exists. UAT proves the API; Shell is transport.

Cromwell Telegram continues to use compose-network MCP for **ops** tools only.

### C4. Acceptance

Runbook exists; Chief of Staff can list-cells + read artifacts from chat without WUT GUI; decision recorded: **Shell-only**.

**Landed 2026-09-13:** [`docs/operations/grok-bot-shell-lab-eval.md`](../docs/operations/grok-bot-shell-lab-eval.md) + `bin/lab-eval` (`list` / `get 596` live; `execute` refuses without `--i-mean-it`). No Serve `/mcp`. No Funnel.

---

## Phase D — Grok Bot skills (locked host)

After A harness + C runbook exist, write briefs. After B1–B2, UAT is MCP-shaped.

| Role | Host | When |
|------|------|------|
| **Lab Sweep** | Grok Bot skill; Shell → MCP Wave 1 (or harness until B1) | Brief after A+C; **UAT after B1** |
| **Edge Scorecard** | Grok Bot skill; MCP Wave 2 / A3 script | **UAT after B2** (script fallback ok) |
| **Attribution** | After B3 | Optional |
| **Book Builder** | After B4 | Not before |
| **Cromwell Lab Scout** | Desk, recommendation-only, no PBR start | Do not dual-own execute |

### UAT (the actual 32-cell science)

Chief of Staff / Lab Sweep, after B+C:

1. Create 32 pending cells from the checked-in config (idempotent).
2. Execute serially (or Sidekiq-capped); poll to completed/failed.
3. Score with `edge_v1`; write analysis artifacts.
4. Reply: best Edge (R) + why portfolio X (per-market + heat skips), **report only**.

John gates pack promotion only.

### D6. Acceptance

Briefs point at **this** plan + MCP contract. E2E UAT: ask Chief of Staff → 32-cell matrix via API → scoreboard → “best Edge on portfolio X because …” without clicking WUT UI. No BG. No Cromwell PBR start. No pack promotion.

**Landed 2026-09-13 (briefs only — UAT not run):** [`docs/operations/grok-bot-lab-sweep.md`](../docs/operations/grok-bot-lab-sweep.md), [`docs/operations/grok-bot-edge-scorecard.md`](../docs/operations/grok-bot-edge-scorecard.md), Grok CLI skills `/lab-sweep` and `/edge-scorecard`. Attribution / Book Builder still later. 32-cell execute still operator-gated.

---

## Sequencing

```text
File this plan + sibling pointers (done in the file-plan session)
  → A: harness + 32-cell config + scorecard (+ optional 1–2 smoke cells)
  → C1: Shell runbook + optional bin/lab-eval
  → D briefs (Sweep / Scorecard) pointing at this plan
  → B1–B2: MCP Wave 1–2  ← UAT surface
  → UAT: Grok Bot builds/executes/scores the 32-cell turtle panel
  → B3 + attribution
  → B4 + book builder
  → C2/C3 never unless a later trust-boundary decision
```

---

## Appendix A — MCP schemas (lab eval, not yet in `winston-mcp-tools.md`)

Intent draft for Phase B. Style matches existing Tool `inputSchema`. All tools return `{ "status": "ok"|"error", ... }` with `code` / `message` on error. **Lab only** — no BG `order_write`, no pack promotion.

Mutating tools require `authorization: "lab_geometry_report_only"` (agent guardrail). Keep those names **off** `ecosystem/ai/schedule/cron-tool-allowlist.json`.

Do **not** treat this appendix as live contract until Wave 1 lands in `winston-mcp-tools.md`.

### Shared types

```json
{
  "HeatConfig": {
    "description": "Canonical heat. String turtle → TURTLE_DEFAULTS. null / omit / legacy → lot caps only. Object is an explicit L1–L4 hash.",
    "oneOf": [
      { "type": "null" },
      { "type": "string", "enum": ["turtle", "legacy"] },
      {
        "type": "object",
        "properties": {
          "mode": { "type": "string", "enum": ["turtle", "legacy", "off"] },
          "unit_risk_fraction": { "type": "number", "exclusiveMinimum": 0 },
          "max_units_per_market": { "type": "integer", "minimum": 1 },
          "max_units_closely_correlated_same_direction": { "type": "integer", "minimum": 1 },
          "max_units_loosely_correlated_same_direction": { "type": "integer", "minimum": 1 },
          "max_units_single_direction": { "type": "integer", "minimum": 1 },
          "correlation": {
            "type": "object",
            "properties": {
              "source": { "type": "string", "default": "pcs_pairwise" },
              "close_threshold": { "type": "number" },
              "loose_threshold": { "type": "number" },
              "window": { "type": "string", "default": "methodology" }
            }
          }
        }
      }
    ]
  },
  "ExperimentMeta": {
    "type": "object",
    "properties": {
      "experiment": { "type": "string" },
      "cell_key": { "type": "string" },
      "session_ticket": { "type": "string" },
      "fill_arm": { "type": "string", "enum": ["resting", "next_open", "other"] },
      "knobs": {
        "type": "object",
        "properties": {
          "max_risk_fraction": { "type": "number" },
          "heat_label": { "type": "string" }
        }
      }
    },
    "required": ["experiment", "cell_key"]
  },
  "RunSummary": {
    "type": "object",
    "properties": {
      "pbr_id": { "type": "integer" },
      "portfolio_id": { "type": "integer" },
      "portfolio_name": { "type": "string" },
      "trading_strategy_id": { "type": "integer" },
      "trading_strategy_name": { "type": "string" },
      "status": { "type": "string" },
      "fill_cadence": { "type": "string" },
      "entry_fill_cadence": { "type": "string" },
      "pyramid_fill_cadence": { "type": "string" },
      "heat": { "$ref": "#/HeatConfig" },
      "risk_percentage": { "type": "number", "description": "WUT fraction (0.01 = 1%)" },
      "start_date": { "type": "string", "format": "date" },
      "end_date": { "type": "string", "format": "date" },
      "initial_capital": { "type": "number" },
      "total_return": { "type": "number" },
      "max_drawdown": { "type": "number" },
      "cagr": { "type": ["number", "null"] },
      "practical_sharpe_ratio": { "type": ["number", "null"] },
      "edge_r": { "type": ["number", "null"] },
      "profit_factor": { "type": ["number", "null"] },
      "edge_n": { "type": ["integer", "null"] },
      "total_trades": { "type": "integer" },
      "pyramid_fills": { "type": "integer" },
      "experiment": { "type": "string" },
      "cell_key": { "type": "string" }
    }
  }
}
```

### Wave 1

**`wut_list_trading_strategies`** — List WUT `TradingStrategy` rows (id, name, active, fingerprint, chassis_summary, heat). Filter `id`, `name_contains`, `active_only`, `limit`. **New** `GET /internal/trading_strategies`. Do not wrap `GET /internal/testing_strategies`.

**`wut_get_portfolio_backtest_run`** — `{ pbr_id, include_equity_history?: false, include_results_json_keys?: [] }` → `{ status, run: RunSummary, results_subset }`. Subsumes Part 2C `wut_get_run_summary`.

**`wut_create_portfolio_backtest_run`** — required `authorization` + `portfolio_id_or_name`; anyOf TS id / TS name / `parent_pbr_id`. Optional window, capital, `fill_cadence` (default `resting_stop_touch`), `heat_mode` / `heat`, `risk_percentage` (fraction), `experiment`, `idempotency_key`. Returns `{ action: created|reused, run }`.

**`wut_set_fill_cadence` / `wut_set_heat` / `wut_set_risk`** — pending PBR only; same authorization constant.

**`wut_execute_portfolio_backtest_run`** — `{ authorization, pbr_id, wait?: false, timeout_seconds?: 120 }`. Default **async** (`wait: false`) → enqueue `PortfolioBacktestJob`. `wait: true` is smoke-only; full-window Turtle books exceed 600s. Returns `{ action: started|completed|already_running, run }`. **Supersedes** staff-roster name `wut_start_pbr`. Forbidden on Cromwell cron / Sawtooth Main / Telegram.

**`wut_list_experiment_cells`** — required `experiment`; optional `cell_key`, `status`, `portfolio_id_or_name`, `trading_strategy_id`, `limit`. Returns `{ cells: [RunSummary], counts_by_status }`.

### Wave 2

**`wut_get_run_edge_report`** — `{ pbr_id, include_per_market?: true, after_costs?: true }` → stored `edge_components` (`edge_v1`) plus `e_ratio` / path extras when present. Recompute via `EdgeCalculator.from_timeline` only if `edge_n` blank. **Supersedes** `wut_get_pbr_scorecard` as the ranking payload. Do not return a parallel `expectancy_r` dialect.

**`wut_compare_runs`** — `{ pbr_ids }` or `{ experiment }`; `primary_metric` default `edge_r`; `min_trades` default 100 (glance bar — thin cells listed with `disqualified_reason`). `authorization_note`: report only — no pack promotion.

**`wut_get_trades`** (P1) — closed lots with 1R / MFE/MAE when computed; cursor pagination.

### Wave 3 (P1)

**`wut_get_portfolio_structure`**, **`wut_get_heat_skips`** (`group_by` reason \| symbol \| reason_symbol), **`wut_explain_run_vs_run`**.

### Wave 4 (P2)

**`wut_create_portfolio`**, **`wut_clone_portfolio_markets`** — lab only; same authorization constant.

### Implementation notes

1. Prefer new WUT `/internal/...` endpoints that MCP thin-wraps.
2. `fill_cadence` / entry / pyramid and heat belong in methodology identity (resting-stop-touch ticket).
3. Edge metrics: persist on PBR (`edge_components`); do not fork in Python.
4. Update `winston-mcp-tools.md` when implementing; this appendix is product intent until then.

---

## Out of scope until asked

Phase A script implementation, compose volume, MCP routes, Grok Bot account creation, Funnel, pack promotion, walk-forward.
