# Plan: Cromwell AI Skills — Part 2 (Remaining Use Cases)

**Status**: Backlog (2026-06-18). Execute after Part 1 is deployed and validated via Telegram test matrix. Part 1 lives in `ecosystem/ai/`.

**Prerequisite**: Principals have used the seeded Cromwell bot for several real daily flows.

## Use Case Inventory

| # | Use Case | Part 2 deliverable | MCP dependency |
|---|----------|-------------------|----------------|
| 1 | Confirmation loop | `winston-confirmation-loop` skill | `wv2_confirm_journal`, `wv2_mark_task_done` |
| 2 | Data health / sync diagnostics | `winston-data-sync` skill (extended) | `wv2_sync_data`; future `dm_get_coverage`, `dm_request_full_sync` |
| 3 | Principal todo tracking | MEMORY sections + `winston-pending-actions` skill | `wv2_list_pending_actions`, `wv2_get_portfolio_status` |
| 4 | Cross-portfolio concentration | Section in `winston-daily-ops` | Report payload aggregation |
| 5 | WUT strategy vetting | `winston-strategy-vetting` skill | Future `wut_list_vetted_runs`, `wut_get_run_summary` |
| 6 | Passed-signal education | `winston-passed-signals` skill | Future `llm_explain` |
| 7 | Data health dashboard | `winston-data-health` skill + heartbeat | DM coverage APIs |
| 8 | Stale confirmation reminders | HEARTBEAT task + skill | `wv2_list_pending_actions` by age |
| 9 | Contextual explain / RAG | `winston-contextual-explain` skill | `rag_query`, `llm_explain` |
| 10 | Position / journal inquiry | `winston-position-inquiry` skill | `wv2_get_journal`, `wv2_get_position_status` |
| 11 | Prompt/skill versioning | `ecosystem/ai/VERSION` + MEMORY correlation | None |

## Phased Implementation

### Phase 2A — Confirmation + Extended Sync (next-steps plan)

- MCP: `wv2_confirm_journal`, `wv2_mark_task_done` in `ai/mcp_winston/` + `ecosystem/interfaces/winston-mcp-tools.md`
- Skills: `winston-confirmation-loop`, `winston-data-sync`, `winston-position-inquiry`
- HEARTBEAT: stale pending reminders, optional pre-close data check

### Phase 2B — Memory Patterns (no new MCP)

- Expand `MEMORY.template.md`: Principal Todos, Promotion Candidates, Recurring Decisions
- Skills: `winston-pending-actions`, `winston-passed-signals`
- Deterministic concentration warnings in `winston-daily-ops`

### Phase 2C — WUT + DM MCP

- Tools: `wut_list_vetted_runs`, `wut_get_run_summary`, `dm_get_coverage_status`, `dm_request_full_sync`
- Interfaces: `wut-mcp-tools.md`, `dm-mcp-tools.md`
- Skills: extend `winston-wut-to-wv2`, add `winston-data-health`

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

See `ecosystem/plans/winston-mcp-next-steps.md` and `ecosystem/plans/winston-plus-llm.md` for related monolith work.