# Plan: Winston MCP Access Layer (Immediate) — Telegram + Core Wv2 Tooling via nanobot + MCP

**Status**: New authoritative plan (2026-06-12). Evaluation complete; immediate slice scoped for build enablement only. Next/LLM plans in sibling docs. Promote all updates here.

**Authoritative location**: This file in `ecosystem/plans/`. Detailed working notes may live in sessions; final decisions and artifacts promoted here + referenced from README/principles.

## Context & Goal
Winston ecosystem (DM + WUT + Wv2 + future Cromwell) is built on majestic monoliths, parquet standard, Sidekiq + webhooks/APIs for coordination, podman compose at root, WUT as reference implementation. Wv2 is the live operational monolith (portfolios with real cash via CashEvents, TradingStrategies for methodology, daily analysis producing journals + action items + Cromwell notifications).

The immediate workstream: provide an **alternative access path** to core Wv2 functionality via **MCP (Model Context Protocol)** so that agentic components (starting with our Cromwell bot on Telegram) can securely invoke the primary Wv2 use cases without relying solely on rakes, internal HTTP, or the governance UI.

**Core Wv2 use cases to expose first (via MCP tools)**:
1. Transfer portfolio from WUT (leverage existing export JSON flow over shared /portfolio_configs volume + import).
2. Create portfolio in Wv2 (new or via import/TS apply).
3. Add market to a Wv2 portfolio (Book + trigger data sync).
4. Sync data in Wv2 (request DM acquisition for symbols + ingest coverage).
5. Perform daily analysis in Wv2 for a given portfolio (or all active).
6. Send / retrieve link (or payload) to daily activity report / Cromwell notification for access to Wv2 state.

Wv2 is "explicitly designed as an MCP component" (per its initial plan). Internal APIs (`/internal/portfolios*`, `/internal/.../evaluate`, `active_markets`, `data_ready`, `trading_strategies`) + rakes (`wv2:portfolios:*`, `wv2:daily_analysis`, `wv2:request_dm_sync`) + services (DmParquetIngester, DailyAnalysisJob, CromwellNotifier) already provide most of the surface. The MCP layer wraps them cleanly for agents.

**The access layer source under evaluation**: `openclawd-stack/` (ollama + open-webui + nanobot gateways wired for Telegram + MCP client support). User previously selected nanobot over openclaw components due to the latter's immaturity and insecurity.

## Evaluation of openclawd-stack (Summary of Findings)
**Strengths for our use case**:
- Ollama container: local, private, downloadable models. Hardened (read_only fs, tmpfs noexec, cap_drop: ALL, no-new-privileges, healthchecks). Perfect for "secure downloaded LLM" roadmap.
- Nanobot: ultra-lightweight (~4k core LOC Python), first-class Telegram support (python-telegram-bot + markdown handling), multi-channel ready, explicit MCP support (stdio + HTTP/SSE transports; config format compatible with Claude Desktop/Cursor; "mcp" dep in pyproject). Heartbeat, skills, workspace, cron. SECURITY.md documents allowFrom, restrictToWorkspace, key hygiene, non-root recs, exec/fs protections.
- Compose.yml already attempts hardening and uses separate instances (g/h) + localhost-bound ports for safety.
- Directly enables the goal: configure one nanobot instance as the "cromwell bot" Telegram endpoint; point its `mcpServers` at a Winston-provided MCP server that exposes the 6 tools. The LLM (local via ollama custom provider or remote) + agent loop in nanobot can then "perform daily analysis", "transfer portfolio", "get report", etc., on natural language instruction from the principals.
- Small, research-friendly, Docker-friendly (its own Dockerfile builds reproducibly from the nanobot/ tree).

**Weaknesses / Risks (and why not adopt openclaw as primary)**:
- openclaw (the big TS monorepo in the stack): powerful full gateway + canvas + skills + many in-process plugins + browser sandboxes. Large surface (3600+ src files), Node 22.12+ strict reqs, complex auth (OAuth for models), higher potential for immaturity/insecurity in the combined "openclawd" packaging (matches user's prior assessment that led to nanobot choice). Its docker-compose is less opinionated on hardening than the nanobot entries. Not needed for our narrow "Cromwell bot on Telegram driving Wv2 tools" + local LLM.
- Nanobot stack compose issues for winston inclusion: absolute host paths in build context (non-portable), mounts `~/.nanobot-*` (config holds plaintext keys — follow its own 0600 advice), two gateways by default, no winston network integration or volume sharing yet, no pre-baked Cromwell persona (we supply the system prompt / skills later). open-webui exposed only on 127.0.0.1:8080 (good). Hermes Dockerfile appears experimental/alternative (Nous hermes-agent) — not core.
- General agent risks: tool-using agents (exec, fs, MCP) are powerful; must be strictly allow-listed and run with least privilege. MCP tools we provide must be idempotent, auditable, and never grant broad shell/DB access.
- Telegram bot setup is manual (user supplies token + user IDs for allowFrom from @userinfobot or @BotFather). "Cromwell bot instance" is our specific bot; config lives outside repo.

**Verdict and direction (no full restart)**:
- Adopt **nanobot + ollama** (from openclawd-stack) as the optional "AI/telegram access layer".
- **Do not** pull in the full openclaw gateway or hermes as primary.
- **Integrate without coupling**: Core Winston (DM + WUT + Wv2 + their PGs + redis + dm_data volume) **must** remain fully runnable and dev-friendly with `./bin/compose up -d` (or the bin/compose wrapper) with zero AI dependencies, no model downloads, no agent processes. Use Docker Compose `profiles` (e.g. `ai`) or a companion `compose.ai.yml` for the layer.
- Build a **thin, dedicated Winston MCP server** (new small component, Python to match nanobot's mcp lib and keep it simple/light; or minimal if we extend later). It registers the exact tools, delegates to Wv2 internal HTTP (and WUT for transfer steps), lives in the podman network, can be stdio-launched by nanobot or exposed via HTTP. Harden it (own Containerfile, read-only where possible, no broad creds).
- Keep the "Cromwell" concept as our agentic coordinator (will consume webhooks from monoliths, drive via MCP tools + its own logic, produce the 11-point narrative over Telegram). nanobot is the channel + LLM runtime + tool client; Cromwell logic/persona lives in prompts/skills/config or a future dedicated Cromwell monolith/service.
- Update root compose + bin/compose + ecosystem/deployment + docs for optional inclusion.
- Immediate scope is **scaffolding + the 6 tools + wiring docs** (full strategy eval in daily analysis can remain stub for now; real port of WUT ops services is already on the Wv2 roadmap).
- Update `ecosystem/` on decisions (this plan + any new principles around "MCP as first-class agent surface", "AI layer is always optional").

This keeps us on common frameworks (all monoliths already aligned on 3.3.6 / Rails 7.0.6 / PG 16 / duckdb / Sidekiq patterns) and respects the 65-line new-Ruby rule (MCP server will be Python; any Ruby deltas in Wv2/WUT for better tool surface must be tiny or split).

## High-Level Technical Decisions (Immediate)
- **MCP server component**: New minimal tree (proposed `mcp_winston/` or `winston_mcp/` at root alongside the monoliths). Use the `mcp` Python package (already a dep of nanobot). Tools implemented as clean functions that do HTTP calls to `http://winston_v2:3000/internal/...` (and WUT equivalents). Stdio transport primary for nanobot (secure, local). Provide a tiny HTTP/SSE mode too. Own tiny Containerfile (python slim + uv or pip). Expose only the scoped tools; no generic exec/fs.
- **Tool surface (exact mapping to the 6 use cases)**:
  1. `transfer_portfolio_from_wut(run_id or config_name)` — triggers WUT export (via WUT internal if exposed, or documented rake path + shared volume), returns import path or triggers Wv2 import. Returns created/updated portfolio id + summary.
  2. `create_portfolio(name, initial_capital, markets: [...], trading_strategy_name?, risk_params...)` — creates Portfolio + CashEvent + Books + optional link to existing TS. (Extend Wv2 internal if current import-only surface is insufficient; keep change tiny.)
  3. `add_market_to_portfolio(portfolio_id_or_name, symbol)` — ensure Market/Book, call request_dm_sync for it.
  4. `sync_data_for_portfolio(portfolio_id_or_name, symbols?)` or `sync_data(symbols)` — calls Wv2 request_dm_data + waits/returns status (or fire-and-notify pattern).
  5. `perform_daily_analysis(portfolio_id_or_name?, date?)` — POST to /internal/portfolios/evaluate or equivalent; returns created tasks + summary. (Later will drive full signal eval.)
  6. `get_daily_activity_report(date?, portfolio?)` or `send_daily_report_link(...)` — reads latest CromwellNotifier JSON (or enhances Wv2 to produce a stable report artifact + "link" stub, e.g. file path or future UI route). Agent (nanobot/Cromwell) can then forward the payload or a human-friendly link/summary over Telegram.
- Additional convenience tools: list_portfolios, list_pending_actions, get_portfolio_status (capital, positions, journals), get_trading_strategies.
- **Integration in compose**: Add optional services (ollama, open-webui optional, nanobot-cromwell or similar, winston_mcp) behind `profiles: ["ai"]`. Volumes: share `sawtooth_dm_data:ro`, `portfolio_configs:rw`, and a new small volume or bind for MCP workspace/config if needed. Network allows winston_mcp <-> winston_v2. nanobot config mounted from a non-committed location (e.g. ecosystem/ai/nanobot-config/ or ~/. controlled). Update bin/compose to support profile flags cleanly (or document `podman compose --profile ai ...`).
- **nanobot wiring (for our cromwell bot)**: Provide `ecosystem/ai/nanobot-cromwell.example.json` (or snippet in deployment). User pastes their Telegram bot token + allowFrom IDs, sets providers (ollama for local or openrouter etc.), adds mcpServers entry pointing at the winston_mcp (stdio command or url). System prompt / initial skills instruct it on the Winston narrative, use of tools, when to call daily_analysis, how to format reports for the 11-point flow, escalation to humans (Alex todos).
- **Security & isolation (non-negotiable)**:
  - Core monoliths never depend on AI containers.
  - Strict allowFrom on channels.
  - MCP tools are narrowly scoped (no rm, no arbitrary SQL, no broad fs outside portfolio_configs and report dirs).
  - Recommend running the whole ai profile under a dedicated user / rootless podman with limited caps.
  - All cross calls over compose network; no public exposure.
  - Document credential placement (separate from eodhd.env; e.g. ecosystem/deployment/ai.env or per-user).
- **No changes to core data model or heavy logic** in immediate. Any Wv2/WUT deltas (e.g. better create/add endpoints, richer report payload) must be small, follow 65-line rule where Ruby, and justified.
- **Reporting / Cromwell stub evolution**: Keep file-based notifier for now; MCP get_report consumes it. Future slice turns notifier into real webhook + uses MCP for confirmation flows.
- **Knowledge**: All decisions, new interfaces (MCP tool schemas), example configs, updated commands go into `ecosystem/`. Update principles if a new invariant emerges (e.g. "Agent surfaces (MCP + webhooks) are first-class alongside APIs/Sidekiq").

## Files / Changes (Immediate Slice)
**New**:
- `mcp_winston/` (or `winston_mcp/`): pyproject.toml or requirements, mcp server script (tools.py or server.py implementing the 6+ tools via httpx + fastmcp or the std mcp sdk), simple Containerfile (python:3.12-slim + uv/pip, no broad system tools), README with exact nanobot config snippet, example tool schemas.
- `ecosystem/ai/` (or under deployment/): nanobot-cromwell.example.json, cromwell-bot-prompt.md (initial system instructions for the 11-point narrative, tool usage, Winston principles), notes on Telegram bot creation for "cromwell".
- Updates to root `compose.yml`: add services (ollama, open-webui?, winston_mcp, nanobot_cromwell) under profile "ai", with correct depends/ volumes/ env/ security opts modeled on the openclawd-stack compose. Comments explaining optional nature.
- `ecosystem/deployment/ai-*.env.template` or extension to existing deployment notes.
- `ecosystem/interfaces/winston-mcp-tools.md` (or section): exact tool names, input schemas, output shapes, error semantics, examples. This becomes the contract.
- Possibly a tiny Wv2 controller addition or route tweak if a clean "create_portfolio" or "add_market" JSON endpoint is missing (prefer adding one small internal action over expanding rakes).

**Modify (minimal)**:
- `ecosystem/plans/winston-v2-initial.md` (add note that MCP exposure is the immediate follow-on).
- `ecosystem/deployment/README.md` (new commands section for the AI profile + nanobot setup + "how to talk to Cromwell bot to run daily analysis").
- `bin/compose` (light support for `--profile ai` passthrough or docs).
- Wv2 internal APIs / rakes only if gaps block the 6 tools (e.g. ensure POST create or a simple portfolios#create internal works; make evaluate return richer actionable payload).
- `winston_v2/storage/` or report generation if we want stable "links" (stub a report builder that writes HTML/JSON artifact + path in the notif).
- Root `compose.yml` comments + health for new optional services.
- `ecosystem/README.md` and principles (if "MCP layer" or "optional AI access" becomes a named concept).

**Reuse**:
- All existing Wv2 internal + DmParquetIngester + CromwellNotifier + portfolio/TS import logic.
- WUT export rakes + internal (for transfer tool).
- DM notify / request paths (already symmetric for Wv2).
- Nanobot patterns + hardening from openclawd-stack (copy/adapt compose blocks, Dockerfile inspiration, security checklist).
- Shared volumes already declared (dm_data, portfolio_configs).

## Verification (End of Immediate)
1. Core standalone still works: `./bin/compose up -d` (no ai profile) brings up redis + 3 PGs + DM + WUT + Wv2 exactly as before. No ollama pull, no new images required for basic dev. Wv2 rakes + internal HTTP + daily jobs function.
2. With profile: `./bin/compose --profile ai up -d` (or equivalent) brings ollama + winston_mcp + nanobot (configured). Containers healthy, winston_mcp can reach winston_v2:3000 over network, nanobot can load the MCP server.
3. MCP tools callable (from nanobot CLI or logs, or direct test): exercise the 6:
   - Export a run in WUT → transfer tool → portfolio appears in Wv2 with correct capital/TS/markets.
   - Create new via tool.
   - Add a market → sync_data tool triggers DM request → data_ready → ingest → coverage present.
   - perform_daily_analysis on a portfolio → journals/tasks created, Cromwell stub JSON written with the right shape.
   - get_daily_activity_report returns usable payload (can be forwarded as "report link" or summary).
4. Telegram path (manual but documented): user configures real cromwell bot token + their user ID in allowFrom, points mcpServers at winston_mcp, sends natural language ("Run daily analysis for Trading Portfolio A and tell me the actions"), bot uses tool, replies with summary + any report payload. No credentials leaked.
5. No breakage: DM/WUT unaffected; Wv2 daily cron (sidekiq) still works; parquet volume and reconciliation flows identical.
6. Docs: `cat ecosystem/plans/*.md ecosystem/interfaces/*` includes the new MCP contract. Deployment README has copy-paste commands for "start the Cromwell bot layer".
7. Security spot-check: no new public ports on core services; ai services bound where possible; example config has strict allowFrom.

Success = the six use cases are reachable both the old way (rake/internal) and the new MCP/agent way, core stack is cleanly separable, the openclawd nanobot/ollama bits are safely integrated as optional, and everything is documented in ecosystem/ so future sessions (or humans) start from truth.

## Open Items / Explicitly Deferred (to next or Winston+LLM)
- Full port of WUT's SignalEvaluation / DailyTasksService / ReportBuilder into Wv2 (daily analysis will become real, not demo stubs).
- Real Cromwell webhook (beyond stub file) + bidirectional confirmation (mark journal executed via tool or chat reply).
- Rich report artifacts (graphs, equity curves, PDF "link").
- Auth / tokens for internal + MCP in prod-like deploys.
- Multiple nanobot instances or dedicated Cromwell monolith.
- RAG, native ollama calls inside Wv2/WUT services, vector stores.
- Production deployment notes for the AI layer (Fly/Render sidecars, secrets).
- Any new principles (e.g. "MCP tools are the contract; monoliths expose narrow, auditable surfaces").

This immediate plan unblocks the "alternative access" exploration while preserving all majestic monolith invariants, the parquet/Sidekiq/webhook model, and dev velocity (core without AI).

(End of immediate plan)
