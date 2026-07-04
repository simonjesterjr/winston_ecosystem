# Plan: Winston MCP Access Layer — Next Steps (Post-Immediate)

**Status**: Companion to winston-mcp-immediate.md (2026-06-12). Do not execute until immediate slice complete and reviewed. Immediate only is enabled for the next build turn.

**Task tracking**: [`winston-mcp-next-steps.md.tasks.json`](winston-mcp-next-steps.md.tasks.json) — 13 tasks across 6 phases with dependencies.

**Scope**: Hardening, completion, Cromwell persona, real flows, production-readiness for the MCP/telegram layer. Builds directly on the 6 core tools and optional ai profile from immediate.

## Context
With the immediate MCP server (winston_mcp) + optional ollama/nanobot integration live and the 6 use cases callable over Telegram via our cromwell bot, the agentic surface is proven.

Next focuses on:
- Making the daily analysis real (full strategy evaluation, not stubs).
- Closing the Cromwell loop (real notifications, confirmations, todos, the full 11-point narrative).
- Tool surface expansion + reliability (idempotency, progress, error handling, human-in-loop).
- Polish on the access layer itself (config management, multiple bots, monitoring).
- Better reports and "send link" experience.
- Preparation for deeper LLM integration (see Winston + LLM plan).

All work continues to respect: core monoliths runnable standalone; AI layer strictly optional via profiles; WUT as reference; parquet as data standard; Sidekiq + webhooks + narrow APIs/MCP as coordination; updates to ecosystem/ as source of truth; 65-line rule for new Ruby.

## Recommended Phasing (Next Slice)
1. **Full Daily Analysis in Wv2 (port/adapt from WUT)**:
   - **Design decisions:** [`docs/business-context/daily-analysis-phase1-design.md`](../docs/business-context/daily-analysis-phase1-design.md) (grill session 2026-06-30).
   - Bring over (copy + adapt + split to stay small) the real services: SignalEvaluation, DailyTasksService (or equivalent), TaskGenerator, ReportBuilder, PositionManager, PyramidService, the risk/entry/exit strategy instances.
   - Register the same strategy names.
   - DailyAnalysisJob (and the evaluate tool) now produces real entrance/exit/pyramid signals, passed_signals with reasons (portfolio/symbol/risk limits), draft journals with proper flow/mtm/risk sizing (using capital_base from CashEvents + realized), operations_tasks.
   - Update the MCP perform_daily_analysis tool + get_report to return rich, structured output (signals taken/passed, proposed position sizes, stop levels, cash impact).
   - Idempotency: per (portfolio, date) or use existing journal guards.
   - Verification: backtest a known config in WUT, promote/transfer to Wv2, run daily, assert signals match expectations on the same parquet data.

2. **Cromwell Narratives + Real Webhook + Bidirectional**:
   - Evolve CromwellNotifier (in Wv2, and symmetrically DM) to support real POST (configurable endpoint or discovered via registry) in addition to the file stub.
   - Define the full payload shape in ecosystem/interfaces/ (portfolios, outstanding trades/confirmations, new entrances, passed reasons, last-N journals + equity series data for graphs, action items, links).
   - MCP tools for confirmation: `confirm_journal(journal_id, notes, fulfillment_type="leap"|"stock"|..., details)`, `mark_task_done(task_id, notes)`. These update status, adjust capital, feed back into future analysis.
   - The nanobot/Cromwell bot receives the daily_complete notification (via webhook it exposes, or polling the notifier dir for now, or direct tool), renders the 11-point story, posts to the Telegram channel, and offers follow-up actions via tools.
   - "Send link to daily activity report": produce a stable artifact (HTML/Markdown/JSON under storage/reports/ or served by a lightweight Wv2 controller) and include a usable reference (path or future /reports/UUID) in the payload + MCP response. Agent can "send" it (the Telegram message itself becomes the delivery).

3. **MCP Server Maturity**:
   - Richer tool schemas + descriptions (for good LLM tool selection).
   - Progress / streaming where MCP supports (long DM syncs or analysis).
   - Better error payloads + retry guidance.
   - Observability: structured logs, correlation IDs that appear in Cromwell notifs and Telegram.
   - Add tools surfaced by immediate feedback: list_pending_actions, get_journal, get_position_status, list_trading_strategies (already partially there), request_full_dm_sync_for_all, etc.
   - Config-driven: which portfolios are "managed" by the bot, escalation rules, quiet hours.
   - Security: signed/authorized calls if we move beyond compose-net trust; rate limiting on expensive tools (analysis, DM sync); audit log of every tool invocation (written to a volume mountable by Cromwell).
   - Packaging: make the mcp_winston a proper installable (uv tool or pip) or always run via its Containerfile in compose. Support both stdio (nanobot) and SSE (other clients or direct curl tests).

4. **nanobot / AI Layer Polish**:
   - Single canonical "cromwell" nanobot instance in compose.ai (rename services, one is enough for the bot).
   - Winston skills + MEMORY/HEARTBEAT templates now live in `ecosystem/ai/`; deploy via `bin/seed-cromwell-workspace`. Part 2 backlog: `plans/cromwell-ai-skills-part2.md`.
   - Document + example for using local ollama models (pull a capable one e.g. qwen2.5 or llama-3.1 via the ollama container; configure nanobot provider as custom or vllm-style pointing at http://ollama:11434).
   - open-webui remains optional (useful for humans to inspect the same local models or chat directly).
   - Heartbeat integration: the gateway can wake and run a "daily briefing" tool sequence even without user message.
   - Multi-user / multi-portfolio separation if the same bot serves more than one principal.
   - Update the openclawd-stack pieces we copied (sync improvements, security checklist application).

5. **Cross-Monolith & Ops**:
   - DM already has good Wv2 symmetry; ensure the generalized `dm:sync_from_consumers` (or equivalent) is solid and exposed as an MCP tool too if useful ("make sure all my portfolios have fresh data").
   - WUT side: expose a minimal internal endpoint or MCP-facilitated path for "list recent good backtest runs / vetted TS" so transfer tool can be smarter ("transfer the best vetted trend portfolio from last month").
   - Sidekiq visibility for MCP-triggered jobs (the evaluate tool already enqueues; surface job ids/status in tool responses).
   - **Ecosystem health watchdog (Sidekiq, not Cromwell):** independent Telegram alerts when core services or the Cromwell gateway are down. Cromwell's 6 AM briefing (`cromwell_ecosystem_status_daily`) covers narrative infrastructure probes + business status; authoritative container/DB checks belong in a DM Sidekiq job. Ticket: [`docs/tickets/2026-07-04-sidekiq-ecosystem-health-watchdog.md`](../docs/tickets/2026-07-04-sidekiq-ecosystem-health-watchdog.md). Related: `dm_get_cromwell_events` needs optional `date` for prior-day EODHD market-count line.
   - Governance UI in Wv2 gets light updates only as side-effect (e.g. show "last MCP invocation" or link to the Cromwell notification JSONs). UIs remain secondary.

6. **Documentation & Ecosystem**:
   - Expand ecosystem/interfaces/ with full MCP tool contract (OpenAPI-like or JSON schema + examples) + Cromwell notification v1 schema + "report link" contract.
   - Update principles/ with any new invariants (e.g. "tool-using agents interact only through narrow, auditable, idempotent surfaces (MCP + internal APIs + webhooks)").
   - Deployment README grows the AI section with "first day with Cromwell bot", troubleshooting Telegram/MCP, "how to run only the bot layer", model pull recipes for ollama.
   - Add a small `ecosystem/ai/` tree with prompts, example configs, a "cromwell persona" markdown that can be fed to nanobot or future Cromwell service.
   - Test matrix in the plan: end-to-end from Telegram message → tool calls → real signal journals → confirmation → updated capital base → next day analysis sees the change.

## Key Artifacts to Produce
- Real operations services ported/adapted into winston_v2/app/services/ and strategies/ (split files to obey size rule).
- Enhanced DailyAnalysisJob + ReportBuilder that matches the WUT narrative quality.
- MCP server v2 (more tools, better payloads, audit).
- CromwellNotifier real webhook support + a small Cromwell stub receiver (for dev, e.g. a sinatra or just another nanobot skill) that prints the 11-point story.
- Confirmation tools + journal state machine updates.
- Stable report artifacts + "link" references in notifs/MCP responses.
- Updated compose profile, nanobot example configs, prompts in ecosystem/ai/.
- New/updated ecosystem/interfaces/ docs.
- Verification script or rake that simulates the full Telegram-driven day (or a test that exercises the MCP server directly).

## Verification Targets (Beyond Immediate)
- A full "Cromwell day" simulation: WUT has a vetted run → Telegram "transfer the latest good one to live and run analysis" → tool sequence succeeds → journals + tasks + passed signals created with correct risk sizing and capital from cash events → Cromwell notif payload contains everything in the target narrative → confirmation tool marks things executed → capital_base updates → next analysis run respects the new positions/stops.
- Local ollama model is used end-to-end for at least the "reasoning / report phrasing" step (even if signals are still rule-based).
- Standalone core: `podman compose down ; ./bin/compose up -d ; wv2 rake still works` with zero AI containers or images pulled.
- Security: attempt to call a tool from a non-allowFrom Telegram user → denied at nanobot; MCP server never accepts broad commands.
- Idempotency and error recovery: re-run same daily_analysis → no duplicate journals; bad symbol in add_market → clear error in tool response and Telegram.
- Ecosystem docs are the single source: anyone can cat the plans + interfaces and reproduce the flows.

## Trade-offs & Scope Boundaries
- Real signal logic lands here (necessary to make the MCP tools valuable); heavy UI or option chain valuation stays out.
- Webhook receiver for dev can be minimal (file tail or a one-off HTTP collector); full Cromwell monolith is later.
- Keep the MCP server small and delegating; do not duplicate business logic inside it.
- If nanobot evolves or we want a pure-Python Cromwell runtime, the MCP contract + narrow monolith surfaces make swapping the "agent host" low-risk.
- Continue preferring stdio MCP for the local trusted layer (lower network exposure).

## Open / Later (See Winston + LLM Plan)
- Native LLM calls inside the monoliths (for journal drafting, passed-signal explanations, dynamic strategy parameterization, anomaly detection on parquet).
- RAG over journals, past reports, strategy definitions, market regimes (local embeddings + ollama or dedicated vector sidecar).
- Explicit orchestration (Cromwell service using the MCP tools + Sidekiq jobs + webhooks as the "graph").
- Multi-LLM (cheap model for classification, strong local for reasoning), tool-use fine-tuning on our traces.
- Production secrets, auth, rate limits, cost tracking for any non-local providers.
- Alternative stores or indexes if the simple PG + parquet + file reports become bottlenecks for agent memory.

This next slice turns the "alternative access" experiment into a robust, narrative-complete daily driver for the principals while keeping the majestic monolith architecture and optionality intact.

(End of next-steps plan)
