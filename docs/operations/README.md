# Operations runbooks

Repeatable procedures for the Winston stack (compose, DM, WUT, Wv2, Cromwell/MCP).

## When to add a runbook

Create or update a file here when **the same operational failure or procedure is diagnosed twice** (or once if blast radius is high: Telegram, capital, data loss).

Do **not** put one-off incident narrative here — that belongs in `docs/issues/` or a session report. Link from the runbook to the issue that motivated it.

## Naming

`short-kebab-topic.md` or `YYYY-MM-DD-short-kebab.md` if the procedure is versioned by date.

## Suggested starter topics (add when real)

| Topic | Trigger examples |
|-------|------------------|
| Compose up / AI profile | stack down, port conflicts |
| DM bind-mount + rebuild | permission denied on `bin/rails`, gem native build |
| Reconcile + coverage | consumer `missing_data`, zero-delta smoke |
| Seed Cromwell workspace | skill/schedule change not visible to bot |
| MCP recreate after tool schema | tool missing / stale schema |
| Cron tool allowlist | off-duty tool calls, historical DAR |
| Telegram channel policy | wrong chat, leak of paper noise |

## Related

- Smoke scripts: `../../bin/` at sawtooth root (`test-mcp-*`, `verify-daily-analysis-parity`, `test-daily-pipeline`)
- Skills: `ship-to-test`, `baseline-replay`, Cromwell skills under `../ai/skills/`
- Filing guide: `../README.md`
