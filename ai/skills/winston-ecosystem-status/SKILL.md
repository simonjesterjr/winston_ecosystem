---
name: winston-ecosystem-status
description: "Infrastructure probes and ecosystem morning briefing. Triggers: /infra (Section 1 only), /infra full, infrastructure status, ecosystem status, system status, morning briefing, are services up, check infrastructure."
---

# Winston Morning Briefing (ecosystem status)

Schedule: `ecosystem/ai/schedule/manifest.yaml` — `cromwell_ecosystem_status_daily` (6:00 AM MT daily).

## When to use (trigger phrases)

Use this skill immediately when the user sends any of:

| Trigger | Scope |
|---------|--------|
| `/infra` | **Section 1 only** — infrastructure probes (deterministic fast-path in nanobot; no LLM wait) |
| `/infra full`, `/infra briefing`, `/infra all` | All three sections (same as 6 AM cron) |
| "infrastructure status", "check infrastructure", "are services up" | **Section 1 only** unless they ask for full briefing |
| "ecosystem status", "system status", "morning briefing" | All three sections |
| "post ecosystem status to Sawtooth Main" | All sections; broadcast to group |

**1-1 (John):** reply in direct chat unless asked to post to the group. **Sawtooth Main:** address as team.

## Message shape

**Scheduled cron (6 AM):** all three sections in order.

**On-demand `/infra`:** Section 1 only — do not include business ops or upstream data unless user used `/infra full` or asked for full/ecosystem/morning briefing.

Post with **three sections in order** when running the full briefing (infrastructure → business ops → business data). No menus, no Runtime Context echo.

## Section 1 — Infrastructure

**Authoritative infra alerts** (including nanobot/ollama/MCP down) are owned by DM Sidekiq `EcosystemHealthCheckJob` — not this skill. It posts Telegram at **:10 hourly** (degraded only) and **6:05 AM MT daily** (always). See `ecosystem/docs/tickets/2026-07-04-sidekiq-ecosystem-health-watchdog.md`. This briefing remains the **narrative** layer via MCP reachability probes.

### MCP probes (fresh call each run)

| Probe | Tool | If OK implies |
|-------|------|----------------|
| Wv2 | `wv2_list_portfolios` | winston_v2 app + wv2_postgres reachable |
| WUT | `wut_list_portfolios` | winston_unit_test app + wut_postgres reachable |
| DM | `dm_get_cromwell_events` with `limit: 1` | data_manager app reachable |

**Cannot probe from Cromwell:** container run state, Sidekiq workers, `redis`/`postgres` health. Do not invent container statuses. If this message posted, Telegram gateway was up for this turn; independent AI-layer liveness is the Sidekiq watchdog.

### Infrastructure lines to include

- **Services:** one line each for DM / Wv2 / WUT — `ok` or `unreachable` from probe result (include error snippet if failed).
- **Databases:** infer from monolith probes (e.g. "Wv2 DB: ok (list_portfolios succeeded)") — not a direct PG health check.
- **Backups:** `not implemented` — ecosystem-wide backup/DR is planned (`ecosystem/plans/operational-data-backup-dr.md`); WUT `ActiveAccountsBackupJob` is partial only. One short line; do not claim backup success.
- **Cromwell layer:** this message proves the gateway ran; note that Sidekiq watchdog owns independent AI-stack alerts.

Lead with failures: if any probe fails, put **Infrastructure: degraded** at the top and name what is down before business sections.

## Section 2 — Business (operations)

- `wv2_list_portfolios` — active vs inactive count, total capital, one line per active portfolio (name, capital, markets).
- `wv2_list_pending_actions` — count; top items (portfolio, market, task type) or "none".
- **Mon–Fri only:** `wv2_get_daily_activity_report` with `fetch_only: true` and `date` = yesterday (America/Denver). If `report_not_ready`, omit EOD recap. One-line prior-session summary when available (actions, skipped portfolios, notable signals).
- **Today:** trading day → DM sync 3:30 PM MT, EOD ~4:35 PM MT; weekend → Saturday DM parquet refresh if Saturday, else light weekend ops.

Do **not** call `wv2_perform_daily_analysis` or `wv2_market_snapshot` on this schedule.

## Section 3 — Business (upstream data)

Report prior **trading day's** EODHD refresh via DM Cromwell events:

1. Call `dm_get_cromwell_events` with `limit: 200` (and `since` if helpful within today's log).
2. Find the latest `sync_complete` event; count distinct `symbol_updated` events for that `run_id`.
3. Format: **"Winston updated N markets from upstream sources (EODHD) on {date}"** — use the date from `sync_complete` / `symbol_updated` details, or "prior trading day" if unclear.

**Known gap:** `dm_get_cromwell_events` reads **today's** event log only. At 6 AM the prior day's 3:30 PM sync is usually in **yesterday's** log file (not yet exposed). When today's log has no relevant events, write: **"Prior day EODHD sync count: unavailable (historical DM event log not yet exposed to MCP)"** — do not guess N.

On weekends / holidays with no prior sync, say so briefly.

## Never Do

- Full portfolio tables or journal dumps
- "Runtime Context", "Active Tasks", or "Next Steps" menus
- Claim live market prices
- Invent container, DB, backup, or market-count figures not in tool responses
- Run analysis or sync tools on this schedule