# Winston Ecosystem — AI / Cromwell Agent Assets

Versioned source of truth for Cromwell bot personas, skills, memory templates, **MCP server**, and **nanobot image patches**.

The ecosystem is exercised heavily through MCP, so runtime glue lives here alongside skills/schedule — not as a host-only tree under workspace `ai/`.

**Deploy personas/skills/cron to a nanobot workspace:**

```bash
bin/seed-cromwell-workspace
# or specify a workspace:
bin/seed-cromwell-workspace --workspace ai/data/cromwell-bot/workspace
```

**Rebuild MCP / nanobot images (after code changes here):**

```bash
./bin/compose --profile ai build winston_mcp nanobot_cromwell
# Prefer replacing only those containers (full compose recreate can cascade-stop the stack)
```

Then restart the bot if only personas/skills changed:

```bash
./bin/compose --profile ai restart nanobot_cromwell
```

## Contents

| Path | Purpose |
|------|---------|
| `VERSION` | Bump when skills, personas, MCP, or nanobot patches change materially |
| `personas/` | `SOUL.md`, `AGENTS.md`, `TOOLS.md` sources |
| `memory/templates/` | `MEMORY.template.md`, `HEARTBEAT.template.md` |
| `skills/` | Winston workflow playbooks (`*/SKILL.md`) |
| `schedule/` | Recurring task catalog — [`schedule/README.md`](schedule/README.md) |
| `mcp_winston/` | **Winston MCP server** (compose `winston_mcp` build context) |
| `nanobot/` | **Cromwell nanobot** Containerfile + Sawtooth patches (compose `nanobot_cromwell`) |

## What lives where

| Concern | Location |
|---------|----------|
| Architecture, parquet, monolith vision | `ecosystem/principles/` |
| MCP tool **contracts** (docs) | `ecosystem/interfaces/winston-mcp-tools.md` |
| MCP tool **implementation** | `mcp_winston/` → image `winston_mcp` |
| Nanobot image + cron allowlist patch | `nanobot/` → image `nanobot_cromwell` |
| Agent identity + workspace rules | `personas/` → workspace root |
| Workflow playbooks | `skills/` → `workspace/skills/` |
| Principal prefs, portfolio facts | `memory/MEMORY.md` (runtime; seeded from template on first run) |
| Session history | `memory/HISTORY.md` (runtime; never overwritten by seed) |
| Runtime bot config / sessions | host `ai/data/cromwell-bot/` (secrets, not this tree) |

## Channels

[`channels.json`](channels.json) — Sawtooth Main (`-1003884714483`) for broadcasts; 1-1 for direct chat.

## Skills

- `winston-heartbeat` — time windows, channel routing, no menus (`always: true`)
- `winston-market-snapshot` — periodic EOD symbol status (DM parquet)
- `winston-daily-ops` — 11-point daily narrative
- `winston-report-delivery` — PDF report delivery (`always: true`)
- `winston-portfolio-lifecycle` — create, add market, activate
- `winston-wut-to-wv2` — promote backtest configs to live
- `winston-ecosystem-status` — 6 AM morning briefing + `/infra` on-demand (infrastructure probes)

**Telegram commands:** `/infra` (fast infrastructure probes), `/infra full` (full briefing). See `ai/README.md` at sawtooth root for Cromwell bot test matrix.

Part 2 backlog (confirmation loop, data health, RAG, etc.) is documented in the Part 2 plan under `ecosystem/plans/`.

## Seed script behavior

Default: **preserve runtime data**.

- Overwrites: `SOUL.md`, `AGENTS.md`, `TOOLS.md`, all `skills/`
- Skips: non-empty `memory/MEMORY.md`, `HISTORY.md`, `sessions/`, `cron/`, `USER.md`
- `--init-memory` — seed MEMORY from template (first-time setup)
- `--force-skills` — alias for default skill overwrite (explicit)

See `bin/seed-cromwell-workspace --help`.