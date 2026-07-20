---
name: ship-to-test
description: >
  Ship current work to the local compose test stack: account for changes, run
  required checks, commit/push when authorized, restart or rebuild services, and
  run Winston smoke scripts. Use when asked to "/ship", "ship to test", "deploy
  and smoke", or after a feature/fix is ready for live compose validation.
  Does not authorize production capital actions or Telegram broadcasts.
metadata:
  short-description: "Checks → commit → compose → smoke"
---

# Ship to test (Winston compose)

Local Podman compose is the test environment. There is no separate staging cluster. **Stop before real-capital or unsolicited Telegram posts.**

## Inputs

- What changed (monoliths: `data_manager`, `winston_unit_test`, `winston_v2`, `ecosystem`, `ai` runtime)
- Optional: skip commit (`checks-only`), skip push, or smoke profile (`rails` | `mcp` | `parity` | `full`)

## Procedure

### 1. Account for work

In **each** git repo with changes (`data_manager`, `winston_unit_test`, `winston_v2`, `ecosystem`, …):

```bash
git status
git diff
```

Stage only intentional files (never blind `git add .`). Confirm no secrets/env dumps.

### 2. Automated checks (risk-proportionate)

| Change surface | Minimum checks |
|----------------|----------------|
| Single Rails app | `bundle exec rspec` in that app (focused then broader) |
| Parquet / lookback / daily analysis | + `bin/verify-daily-analysis-parity` from sawtooth root |
| MCP tools / audit / schema | + `bin/test-mcp-audit-smoke` (and maturity/task9 if tools touched) |
| Cromwell workspace / cron / skills | `bin/seed-cromwell-workspace` after asset change; note image rebuild if nanobot patches changed |
| Multi-app | checks in each touched app |

Record command results. Stop on red unless the failure is pre-existing and documented.

### 3. Commit and push (when authorized)

- Prefer `/wrap` if ending the session; otherwise commit with a clear message per repo.
- Push existing tracking branches. **Do not** open PRs or force-push unless the user asked.
- Multi-repo: commit each repo that changed.

### 4. Compose deploy (test)

From sawtooth root:

```bash
bin/compose up -d                    # core stack
bin/compose --profile ai up -d       # only if AI/Cromwell path changed
```

Service-specific:

| Service | Typical action |
|---------|----------------|
| Code-only Rails (bind-mounted DM) | `bin/compose restart data_manager data_manager_sidekiq` |
| DM Gemfile/Containerfile | `bin/rebuild-dm` |
| WUT / Wv2 image-baked code | rebuild/restart the service per compose setup |
| MCP tool changes | recreate `winston_mcp` / related containers so schema reloads |
| Cromwell skill/schedule | `bin/seed-cromwell-workspace` + restart nanobot if needed |

Prove non-production: local compose project names/ports (3000/3001/3002), not a remote prod host.

### 5. Smoke

Pick profile:

**rails (default):** hit health or a cheap page/API on changed ports; run focused request specs if not already.

**mcp:**

```bash
bin/test-mcp-audit-smoke
# optional:
bin/test-mcp-maturity
bin/test-mcp-task9-smoke
```

**parity:**

```bash
bin/verify-daily-analysis-parity
# optional live stack:
bin/verify-daily-analysis-parity --compose
bin/test-daily-pipeline   # when daily path changed; prefer --offline if documented
```

**full:** rails + parity + mcp as applicable.

### 6. Report

Return: repos/commits, services restarted, smoke commands + pass/fail, residual risks, and any follow-up tickets (`/record`).

## Guardrails

- No production deploy, secret edits, or DB drops without explicit approval.
- No Telegram to real channels as part of smoke unless the user requests it.
- Historical DAR / off-duty MCP tools must remain fail-closed.
- If checks cannot run (stack down), say so; do not claim green.
