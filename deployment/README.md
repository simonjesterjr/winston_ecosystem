# Deployment & Podman for the Sawtooth Ecosystem

## Local Development (Current Target)
- Use podman (or podman-compose / podman compose).
- Root `sawtooth/compose.yml` (committed) defines the services: data_manager, winston_unit_test, redis (for Sidekiq), (later cromwell, winston_v2).
- Each monolith has a minimal Containerfile (or Dockerfile) in its directory or referenced from root.
- Volumes:
  - One (or more) for DM's `data/` parquet tree. WUT can mount it read-only for direct high-performance parquet access during dev.
  - Separate named volumes for each monolith's Postgres (metadata DBs are independent).
- Networking: containers can reach each other by service name for the internal APIs (e.g. WUT calls DM at http://data_manager:3000/... or the other way for discovery).
- Redis is shared (WUT already notes this in its docker-compose).

## Running
```bash
# From sawtooth/ root
./bin/compose up -d

# Sidekiq workers (scheduled backend — see ecosystem/ai/schedule/README.md)
./bin/compose up -d data_manager_sidekiq winston_v2_sidekiq winston_unit_test_sidekiq

# Cromwell cron (Telegram delivery)
bin/seed-cromwell-workspace
./bin/compose --profile ai up -d nanobot_cromwell
```

### AI / MCP build sources (git)

| Image | Compose context (SOT in `winston_ecosystem`) |
|-------|-----------------------------------------------|
| `winston_mcp` | `ecosystem/ai/mcp_winston/` |
| `nanobot_cromwell` | `ecosystem/ai/nanobot/` |

Personas/skills/schedule still seed into host `ai/data/cromwell-bot/workspace` via `bin/seed-cromwell-workspace`. Runtime secrets stay in `ai/data/cromwell-bot/config.json` (not git).

### DM source bind-mount (dev)

Root `compose.yml` bind-mounts `./data_manager` into `data_manager` and `data_manager_sidekiq` (same as WUT/Wv2). Keep `data_manager/bin/*` executable (`git` mode `100755`) or rootless Podman will hit permission denied on `bin/rails`.

- Code-only edits: live (restart Sidekiq if needed).
- Image layers (Gemfile/Containerfile): `./bin/rebuild-dm` or  
  `./bin/compose build data_manager && ./bin/compose up -d data_manager data_manager_sidekiq`

See `data_manager/README.md` and ticket `docs/tickets/2026-07-08-dm-bind-mount-decision.md`.

### M-F schedule (Mountain Time)

| Time | Service | Task |
|------|---------|------|
| 3:30 PM | `data_manager_sidekiq` | EODHD sync (WUT+Wv2 symbols) |
| 4:30 PM | `winston_v2_sidekiq` | `DailyAnalysisJob` → JSON + PDF |
| 4:35 PM | Cromwell cron | EOD Telegram (`fetch_only` report) |
| 7:30 AM–2:00 PM | Cromwell cron | Market snapshots (NYSE session) |

Redis isolation: DM `redis://redis:6379/0`, WUT `/1`, Wv2 `/2`.

## Credentials & Config (EODHD Key etc.)
- User will supply the EODHD API key once this location exists.
- Place it according to the template below (or in per-app `config/credentials.yml.enc` / env files that the compose mounts).
- Never commit real keys. Use the templates in this directory.
- Inter-monolith tokens (for /api/internal/*) live in the same place or as compose secrets / env.

Example template file (create `eodhd.env.template` or similar and copy to a non-committed `eodhd.env`):

```
EODHD_API_KEY=your_key_here
# Also common ones:
# WUT_INTERNAL_API_TOKEN=...
# DM_INTERNAL_API_TOKEN=...
# REDIS_URL=redis://redis:6379/0
```

Compose can load these with `env_file:`.

## Data Volumes & Portability
- The parquet `data/` tree is the valuable artifact.
- In compose you can define a volume that maps to a host path if you want your real data to live outside containers.
- Reconciliation (in DM) + the fact that parquet is the source of truth means you can:
  - Stop everything
  - Drop or rsync parquet files into the volume
  - Bring DM back up (or run its reconcile rake)
  - PG metadata is now in sync; no unnecessary re-downloads.

## Production / Later
- Each monolith can be deployed independently (Fly, Render, k8s, etc.).
- The same principles apply: DM owns the parquet (object storage or persistent volume), exposes it, notifies Cromwell.
- Shared Redis or per-monolith Sidekiq + Redis is fine as long as the monoliths can reach each other for the internal APIs/webhooks.

## Relation to Existing Files
- `winston_unit_test/docker-compose.yml` is minimal and references a shared redis. It will be superseded / composed into the root `compose.yml`.
- DM will get its own Containerfile modeled on WUT's patterns.

See the approved data-manager plan and principles/ for more.

## Portfolio Configurations (WUT -> Wv2)
WUT is the source of "configured portfolios" (via PortfolioBacktestRun + market configs + chosen strategies, risk params, capital, limits).

To move a configuration into live Wv2:

1. In WUT container (after you have a backtest run you like):
   `bin/rails wut:portfolios:export_config[RUN_ID, /portfolio_configs/my-portfolio.json]`

2. Edit the JSON with your favorite raw editor (nano is explicitly supported and sufficient):
   `nano portfolio_configs/my-portfolio.json` (from host)
   or inside Wv2: `bin/rails wv2:portfolios:edit_config[my-portfolio.json]`

3. Import in Wv2:
   `bin/rails wv2:portfolios:import[my-portfolio.json]`

4. Activate and evaluate (the portfolio now participates in daily jobs and Cromwell notifications):
   `bin/rails wv2:portfolios:activate["My Portfolio"]`
   `bin/rails wv2:portfolios:evaluate`
   `cat storage/cromwell_notifications/wv2_YYYYMMDD.json`

The `./portfolio_configs` dir at the sawtooth root is mounted (rw) into both WUT and Wv2 containers by root `compose.yml`. This is the canonical exchange location.

Corresponding rake tasks and a small internal API (`/internal/portfolios*`) exist in Wv2. No heavy UI is provided or required.

See also: root compose.yml comments, `portfolio_configs/README.md`, `ecosystem/plans/winston-v2-initial.md`, `ecosystem/plans/winston-mcp-immediate.md`, and Wv2's `lib/tasks/wv2.rake`.

## Optional AI / MCP / Telegram Layer (ollama + nanobot + winston_mcp) — podman native
The AI access layer (local secure LLM via ollama, one nanobot gateway for the "Cromwell bot" on Telegram, and the Winston MCP server) is **strictly optional**.

Core Winston (DM + WUT + Wv2 + redis + the three dedicated Postgres containers) runs and develops with **zero AI dependencies**:

```bash
./bin/compose up -d
./bin/compose exec -T winston_v2 bin/rails wv2:portfolios:evaluate
```

### Bring up the Cromwell bot / MCP layer
```bash
# 1. Start only the AI profile (ollama + mcp server + nanobot gateway)
./bin/compose --profile ai up -d

# 2. (First time) prepare the bot config from the clean example
mkdir -p ai/data/cromwell-bot
cp ai/configs/nanobot-cromwell.example.json ai/data/cromwell-bot/config.json
# Edit the file:
#   - telegram.token  = token from @BotFather for your cromwell bot
#   - telegram.allowFrom = your Telegram numeric user ID(s) (get from @userinfobot)
#   - providers.ollama.apiBase = http://ollama:11434 (already correct for compose)
#   - tools.mcpServers.winston.url = http://winston_mcp:8088/sse  (already correct)
nano ai/data/cromwell-bot/config.json

# 3. Pull a local model (model choice is the main lever for "snappy conversational" vs "reliable at actual MCP workflows")
# Recommended for Cromwell bot (best balance of tool-calling stability + reasoning for reports/workflows + usable chat speed):
./bin/compose --profile ai exec ollama ollama pull qwen3:8b

# For maximum snappiness on casual messages (still capable of the tools):
# ./bin/compose --profile ai exec ollama ollama pull qwen2.5:3b
# ./bin/compose --profile ai exec ollama ollama pull phi4:3.8b

# See ai/README.md for full evaluation (Qwen3/2.5 family leads for reliable function calling per 2026 data; 8B-class is the sweet spot for not looping and handling "tell me the MCP functions" + "give daily report" + real actions like transfer/add/perform). 

# After pull + any model change in config, restart the bot:
# ./bin/compose --profile ai restart nanobot_cromwell

# 4. Seed the Cromwell workspace from ecosystem/ai/ (personas + skills + templates)
bin/seed-cromwell-workspace
# First-time only (empty MEMORY): bin/seed-cromwell-workspace --init-memory

# Deploys: SOUL.md, AGENTS.md, TOOLS.md, skills/, HEARTBEAT.md (if empty)
# Preserves: memory/MEMORY.md (learned facts), HISTORY.md, sessions/, cron/, USER.md
# Source of truth: ecosystem/ai/ (see ecosystem/ai/README.md)

# Restart after changes (rebuild nanobot if openclawd-stack/nanobot was patched):
# ./bin/compose --profile ai build nanobot_cromwell
./bin/compose --profile ai restart nanobot_cromwell

# Scheduled broadcasts (market snapshot 10 AM / 2 PM MT, EOD report 4:35 PM MT) target
# Sawtooth Main via workspace/cron/jobs.json. gateway.heartbeat.enabled should be false.

# 4. (Optional) watch the gateway logs
./bin/compose --profile ai logs -f nanobot_cromwell
```

### Talk to the bot
Message your Telegram cromwell bot with natural language that maps to the 6 core Wv2 use cases (and the convenience tools). The bot uses the MCP tools defined in `ecosystem/interfaces/winston-mcp-tools.md`.

Examples:
- "list portfolios"
- "transfer portfolio from WUT run 42" or "transfer the latest good one from ts 7"
- "create portfolio MyTest with initial 12000 on AAPL,MSFT"
- "add NVDA to Trading Portfolio A"
- "sync data for Trading Portfolio A"
- "perform daily analysis for Trading Portfolio A" or just "run the daily for A"
- "get today's daily activity report" or "send the report"

The MCP server (`ai/mcp_winston/`) is the thin component that translates those tool calls into real calls against Wv2's (and WUT's) internal HTTP surfaces.

### Shutdown the AI layer only
```bash
./bin/compose --profile ai down
```

The core monoliths are untouched.

### Hardening & security
The AI services in root `compose.yml` use the hardening attributes evaluated from the reference stack (read_only, tmpfs noexec, cap_drop: ALL, no-new-privileges, limited DNS, localhost-only ports for any UI). The MCP tools only call the narrow audited `/internal/*` endpoints.

Never commit real Telegram tokens. Follow the advice in `ai/nanobot/Containerfile` comments and nanobot's own SECURITY.md (0600 on config.json, strict allowFrom, etc.).

### Ecosystem health watchdog (DM Sidekiq — independent of Cromwell)

When `nanobot_cromwell` or Ollama is down, Cromwell cron cannot alert. A **Sidekiq job on Data Manager** probes HTTP health and posts Telegram directly via the Bot API.

| Item | Detail |
|------|--------|
| Job | `EcosystemHealthCheckJob` |
| Schedule | `:10` every hour (degraded-only Telegram); **6:05 AM MT** daily (always post) |
| Probes | DM, WUT, Wv2, `winston_mcp` `/health`, Ollama `/`, nanobot `/health` |
| Secrets | `ecosystem/deployment/watchdog.env` (gitignored) |

```bash
# One-time
cp ecosystem/deployment/watchdog-env-template.txt ecosystem/deployment/watchdog.env
# set ECOSYSTEM_WATCHDOG_TELEGRAM_TOKEN + ECOSYSTEM_WATCHDOG_TELEGRAM_CHAT_ID
./bin/compose up -d data_manager_sidekiq

# Manual smoke
./bin/compose exec -T data_manager_sidekiq bin/rails runner \
  'pp EcosystemHealthCheckJob.perform_now("daily")'
```

Nanobot must listen on `0.0.0.0` (`gateway.host` in `ai/data/cromwell-bot/config.json`) so other containers can reach `/health`. Host publish stays `127.0.0.1:18790`.

### CPU-only LLM notes (sawtooth-ai)

This host has **no discrete GPU** (Raphael iGPU only). Ollama runs 100% CPU. Preferred Cromwell model: `cromwell-qwen2.5:3b` (`ai/ollama/Modelfile.cromwell-cpu`, `num_ctx` 8192). Keep-alive is `OLLAMA_KEEP_ALIVE=24h` in compose. See `ecosystem/docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md` and ops note in `ecosystem/ai/schedule/README.md` (avoid backtests at top-of-hour MT).

### Files that implement the layer (all outside the deprecated openclawd-stack)
- `ai/mcp_winston/` — the MCP component (Containerfile + pyproject + server.py)
- `ai/nanobot/Containerfile` — tiny pip-install based image (no source tree copy)
- `ai/configs/nanobot-cromwell.example.json`
- `ai/README.md`
- Root `compose.yml` (the big "OPTIONAL AI" block at the bottom + profiles on the services)
- `bin/compose` (passes --profile through)
- `ecosystem/interfaces/winston-mcp-tools.md` (the contract)
- `ecosystem/plans/winston-mcp-immediate.md`

See the root compose.yml comments (search for "ai" or "Cromwell") and `ai/README.md` for the authoritative runtime details.

Update this section + the plans + the interface doc when the tool surface or the profile evolves.
