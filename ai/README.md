# Winston Ecosystem — AI / Cromwell Agent Assets

Versioned source of truth for Cromwell bot personas, skills, and memory templates.

**Deploy to a nanobot workspace:**

```bash
bin/seed-cromwell-workspace
# or specify a workspace:
bin/seed-cromwell-workspace --workspace ai/data/cromwell-bot/workspace
```

Then restart the bot:

```bash
./bin/compose --profile ai restart nanobot_cromwell
```

## Contents

| Path | Purpose |
|------|---------|
| `VERSION` | Bump when skills or personas change materially |
| `personas/` | `SOUL.md`, `AGENTS.md`, `TOOLS.md` sources |
| `memory/templates/` | `MEMORY.template.md`, `HEARTBEAT.template.md` |
| `skills/` | Winston workflow playbooks (`*/SKILL.md`) |
| `schedule/` | Recurring task catalog — [`schedule/README.md`](schedule/README.md) |

## What lives where

| Concern | Location |
|---------|----------|
| Architecture, parquet, monolith vision | `ecosystem/principles/` |
| MCP tool schemas | `ecosystem/interfaces/winston-mcp-tools.md` |
| Agent identity + workspace rules | `personas/` → workspace root |
| Workflow playbooks | `skills/` → `workspace/skills/` |
| Principal prefs, portfolio facts | `memory/MEMORY.md` (runtime; seeded from template on first run) |
| Session history | `memory/HISTORY.md` (runtime; never overwritten by seed) |

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