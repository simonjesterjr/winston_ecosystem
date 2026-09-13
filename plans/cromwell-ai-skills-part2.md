# Plan: Cromwell AI Skills — Part 2 (Remaining Use Cases)

**Status**: Backlog (2026-06-18). Execute after Part 1 is deployed and validated via Telegram test matrix. Part 1 lives in `ecosystem/ai/`.

**Lab eval (2026-09-13):** WUT experiment-control MCP (create/execute PBR, Edge report) is **not** this file. Authoritative: [`winston-lab-eval-grok-cli.md`](winston-lab-eval-grok-cli.md). This plan keeps Cromwell **skills** and the transfer-oriented **read** tools.

**Prerequisite**: Principals have used the seeded Cromwell bot for several real daily flows.

## Use Case Inventory

| # | Use Case | Part 2 deliverable | MCP dependency |
|---|----------|-------------------|----------------|
| 1 | Confirmation loop | `winston-confirmation-loop` skill | `wv2_confirm_journal`, `wv2_mark_task_done` |
| 2 | Data health / sync diagnostics | `winston-data-sync` skill (extended) | `wv2_sync_data`; future `dm_get_coverage`, `dm_request_full_sync` |
| 3 | Principal todo tracking | MEMORY sections + `winston-pending-actions` skill | `wv2_list_pending_actions`, `wv2_get_portfolio_status` |
| 4 | Cross-portfolio concentration | Section in `winston-daily-ops` | Report payload aggregation |
| 5 | WUT strategy vetting (transfer) | `winston-strategy-vetting` skill | `wut_list_vetted_runs` (read filter). Summary = lab-eval `wut_get_portfolio_backtest_run` when B1 ships — **do not** add a second `wut_get_run_summary`. Lab Sweep/execute is Grok Bot, not this skill. |
| 6 | Passed-signal education | `winston-passed-signals` skill | Future `llm_explain` |
| 7 | Data health dashboard | `winston-data-health` skill + heartbeat | DM coverage APIs |
| 8 | Stale confirmation reminders | HEARTBEAT task + skill | `wv2_list_pending_actions` by age |
| 9 | Contextual explain / RAG | `winston-contextual-explain` skill | `rag_query`, `llm_explain` |
| 10 | Position / journal inquiry | `winston-position-inquiry` skill | `wv2_get_journal`, `wv2_get_position_status` |
| 11 | Prompt/skill versioning | `ecosystem/ai/VERSION` + MEMORY correlation | None |

## Phased Implementation

### Phase 2A — Confirmation + Extended Sync (next-steps plan)

- MCP: `wv2_confirm_journal`, `wv2_mark_task_done` in `ai/mcp_winston/` + `ecosystem/interfaces/winston-mcp-tools.md` — **done**
- MCP: `wv2_deactivate_portfolio` + `id_or_name` mapping for activate/deactivate — **done** (2026-07-14 paper Phase 2)
- Skills: `winston-confirmation-loop` **done** (2026-07-14); still open: `winston-data-sync`, `winston-position-inquiry`
- HEARTBEAT: stale pending reminders, optional pre-close data check

### Phase 2B — Memory Patterns (no new MCP)

- Expand `MEMORY.template.md`: Principal Todos, Promotion Candidates, Recurring Decisions
- Skills: `winston-pending-actions`, `winston-passed-signals`
- Deterministic concentration warnings in `winston-daily-ops`

### Phase 2C — WUT + DM MCP

- Tools still in **this** plan: `wut_list_vetted_runs` (read-only filter for transfer), `dm_get_coverage_status`, `dm_request_full_sync` (latter may already exist).
- **Subsumed by lab-eval:** `wut_get_run_summary` → `wut_get_portfolio_backtest_run`. PBR create/execute/heat/edge → [`winston-lab-eval-grok-cli.md`](winston-lab-eval-grok-cli.md).
- Interfaces: keep a **single** contract file `ecosystem/interfaces/winston-mcp-tools.md`. Do **not** create `wut-mcp-tools.md` / `dm-mcp-tools.md` unless inventory is later split on purpose (staff roster already forbade the extra WUT file).
- Skills: extend `winston-wut-to-wv2`, add `winston-data-health`. Do not teach Cromwell to start PBRs.

### Phase 2D — Native LLM + RAG (winston-plus-llm Phase 1–2)

- Wv2 `OllamaClient` (gated, default off)
- MCP proxy: `wv2_llm_explain`, `wv2_rag_query`
- Skill: `winston-contextual-explain`
- Interface: `llm-rag-corpus.md`

### Phase 2E — Cromwell Monolith Memory (Phase 3)

- Cromwell PG owns todos, orchestration logs, RAG
- Nanobot MEMORY becomes thin cache; skills stay in `ecosystem/ai/skills/`

## Sequencing

1. Phase 2A — unblocks full daily loop with confirmations
2. Phase 2B — immediate principal value, no Ruby MCP work
3. Phase 2C — when transfer/sync pain surfaces in real usage
4. Phase 2D — after 2+ weeks stable MCP bot usage

See `ecosystem/plans/winston-mcp-next-steps.md`, `ecosystem/plans/winston-lab-eval-grok-cli.md` (WUT lab MCP), and `ecosystem/plans/winston-plus-llm.md` for related monolith work.