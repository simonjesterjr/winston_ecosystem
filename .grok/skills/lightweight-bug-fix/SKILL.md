---
name: lightweight-bug-fix
description: >
  Fix an existing defect with a regression-locked, lightweight workflow — issue
  readiness, reproduce, failing test, minimal patch, verify, and durable notes.
  Use when fixing a ready bug/regression without the full agent-harness
  safe-bug-fix stack. Prefer for Winston Rails/MCP/Cromwell defects. Do not use
  for intentional contract or behavior changes (route those to a plan/ADR).
metadata:
  short-description: "Ready issue → reproduce → test → minimal fix → verify"
---

# Lightweight bug-fix (Winston)

A practical subset of the full `safe-bug-fix` kit. **No** `.agent-harness` requirement. Still non-negotiable: evidence, failing test first, and no silent behavior change.

## When to use

- Existing defect with a path in `docs/issues/` (ecosystem or monolith) at status **ready** (or equivalent clear readiness: repro + acceptance criteria).
- Money path, journals, risk ladder, parquet contracts, MCP/Telegram guards, data reconciliation, or any fix that must not regress.

## When not to use

- Features or refactors without a current wrong behavior → normal TDD / ticket work.
- Intentional contract changes → plan + ADR / explicit approval; do not disguise as a bug fix.
- Cannot reproduce after honest attempt → stop; keep issue in triage/blocked with evidence.

## Inputs

1. Exact issue path under `docs/issues/` (create/refine with `manage-issue-ticket` first if missing or not ready).
2. Target monolith `AGENTS.md` + `PROJECT_PROFILE.md` when present.
3. For cross-system symptoms, consider `investigate-system-variance` before patching.

## Procedure

### 1. Issue gate

- Confirm issue has: observable problem, expected behavior, repro or bounded investigation, acceptance criteria, must-preserve list.
- If not ready, invoke `manage-issue-ticket` and stop until status is `ready` (or banner clearly equivalent).
- Prefer the issue committed or at least saved before large code churn so the record survives the session.

### 2. Baseline

- Note branch, HEAD, and dirty files (`git status` in each touched repo).
- Run the smallest relevant green check (or record pre-existing failures — do not absorb them into the fix).

### 3. Reproduce

- Execute the issue’s repro steps against the real stack or a deterministic fixture.
- Capture command output, logs, or UI evidence. If intermittent, document frequency; consider flaky-test triage separately.

### 4. Lock a failing regression

- Add or extend an automated test that fails for the right reason **before** production code changes.
- Prefer unit/request/job specs in the owning monolith; for MCP/agent bugs, prefer a unit test on the guard/allowlist/patch plus a smoke script when available.
- Commit or keep the failing test in the working tree as the lock.

### 5. Map impact (brief)

- List files/contracts likely touched (API, parquet columns, journal fields, Telegram, cron allowlist).
- Name behaviors that **must preserve** (from issue + ADRs).

### 6. Minimal patch

- Smallest change that makes the new test pass without weakening existing checks.
- No drive-by refactors. No deleting or skipping failing unrelated tests.

### 7. Verify

1. New regression test passes.
2. Focused related specs pass.
3. Broader suite or relevant smoke as risk demands:
   - Rails: `bundle exec rspec` (full when money/data path)
   - Parity: `bin/verify-daily-analysis-parity` when entry/exit/lookback/parquet load changes
   - MCP: `bin/test-mcp-audit-smoke` / maturity / task9 as appropriate
   - Compose: restart affected services; recreate MCP after tool schema changes
4. Manual repro path now shows expected behavior.

### 8. Durable memory

- Update the issue: status `resolved` or `Fixed in <sha>` only when verified; else `in-progress` with candidate evidence.
- `/record` tickets for leftover work; promote ADR only if the fix encodes a hard-to-reverse decision.
- Session report via `/wrap` or `/session-report`.

## Output checklist

- [ ] Issue path and readiness
- [ ] Repro evidence
- [ ] Regression test path
- [ ] Production files changed
- [ ] Verification commands + results
- [ ] Residual risks / follow-up tickets

## Failure routing

| Situation | Action |
|-----------|--------|
| Issue not ready | `manage-issue-ticket`; stop |
| Cannot reproduce | Blocked on issue; no speculative patch |
| Baseline already red | Record; do not hide under this fix |
| Fix needs intentional behavior change | Stop; explicit approval + plan/ADR |
| Cross-system unexplained drift | `investigate-system-variance` first |

## Relation to full harness

Full `safe-bug-fix` + `.agent-harness` (worktree isolation, run artifacts, integrity audit skills) lives in `ai-workflow-skills/` and may be installed later. This skill is the **default** Winston lane until then.
