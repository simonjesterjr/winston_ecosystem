# Winston ecosystem — variance investigation project notes

Use with `investigate-system-variance`. Compare **one scoped case** with a written contract. Domain terms: `CONTEXT.md` (ecosystem root).

## Primary comparison axes

| Axis | Baseline | Candidate | Identity keys |
|------|----------|-----------|---------------|
| Lab vs ops handoff | WUT export / PBR / TradingStrategy | Wv2 Operational Portfolio import | portfolio name, TS fingerprint, market set, capital/risk config |
| Signal / daily analysis parity | WUT strategy evaluation on pinned parquet | Wv2 daily analysis / lookback | symbol, as-of date, strategy class, ATR column presence |
| Data coverage | DM parquet + DataCoverage | WUT/Wv2 consumer coverage / skip reasons | symbol, date range, `atr_17` and required MAs |
| Paper journal economics | Lab backtest journals / expected sizes | Wv2 paper journals / sizer | portfolio id, market, entry date, risk % ladder level |
| Agent channel behavior | Intended cron allowlist + skill text | Live Telegram / MCP audit JSONL | session_key, tool name, date arg, chat_id |

## Authoritative requirements

- `CONTEXT.md` — canonical terms
- `docs/adr/ADR-002` parquet, `ADR-003` DM owns derivatives, `ADR-004` audit, `ADR-006` lineage, `ADR-007` PCS, `ADR-008` confirm entry + dynamic risk
- `interfaces/winston-eod-parquet-standard.md`, `interfaces/winston-mcp-tools.md`
- `docs/business-context/wut-to-wv2-handoff.md` and related business-context files
- Known deliberate differences: document in ADRs, tickets, or this notes file — do not rediscover as regressions

## Artifact locations

| Kind | Location |
|------|----------|
| Parquet | DM volume / `data_manager/data/markets/` (compose) |
| Portfolio exports | `portfolio_configs/` at sawtooth root |
| MCP/webhook audit | `ecosystem/logs/audit/{mcp,webhook}/` |
| Cromwell sessions | `ai/data/cromwell-bot/` session JSONL (runtime) |
| Parity script | `bin/verify-daily-analysis-parity` |
| Pipeline smoke | `bin/test-daily-pipeline` |
| Issues / tickets | `ecosystem/docs/issues/`, `ecosystem/docs/tickets/` |

## Shared-state / contention scopes

- **Symbol demand:** multiple portfolios → one DM fetch; coverage must not be double-counted as independent feeds
- **Pyramid / risk ladder:** concurrent open levels change risk % — compare level index, not only base `risk_percentage`
- **Confirmational entry:** initial entry only; pyramid adds are ATR path (ADR-008)
- **Cash / positions:** journal order vs fill vs cash events — conserve cash and position qty when classifying drift
- **Telegram / cron:** session isolation; allowlist vs prompt FORBIDDEN (runtime allowlist is SOT when present)

## Executable path hints

| System | Entry areas (verify live wiring; do not cite dead code) |
|--------|--------------------------------------------------------|
| DM | download services, ReconciliationService, trigger API, Sidekiq jobs |
| WUT | strategy registry, backtest/PBR runners, export builders, data_sets controllers |
| Wv2 | daily analysis job/services, position sizer, journal confirm, Telegram delivery, internal MCP APIs |
| MCP | `ecosystem/ai/mcp/mcp_winston/`, cron allowlist patch under `ecosystem/ai/nanobot/patches/` |

## Environment and data safety

- Default: local compose stack; treat live Telegram and real capital as **production-impacting**
- External market data / broker: read-only unless operator explicitly authorizes
- Prefer immutable parquet snapshots and committed fixtures over live re-download for parity
- Redact tokens, chat secrets, and account credentials from issue artifacts

## Filing

Write investigations under `ecosystem/docs/issues/` (or monolith `docs/issues/` if single-app). Use `manage-issue-ticket` for defect readiness. Spawn `docs/tickets/` only for remaining work.
