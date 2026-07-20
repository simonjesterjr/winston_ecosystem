# Ticket: Propagate ecosystem log hygiene patterns to top-level and monoliths

**Status:** Proposed
**Priority:** P3

**Context:** Created as follow-up from session report `docs/session-reports/2026-07-06-1539-ecosystem-logs-gitignore.md`. The ecosystem repo now properly ignores all log contents (blanket `logs/` rule + committed `logs/audit/.gitignore` rules file per ADR-004). No log data or placeholders are tracked, and history was cleaned of the prior placeholder.

## Problem

The broader sawtooth workspace (multi-repo) and other monoliths may not have equivalent protections. Root `.gitignore` and monolith `.gitignore`s/AGENTS.md have some related rules (parquet, logs in Rails apps), but lack the explicit ecosystem-style audit log hygiene and defense-in-depth. Risk of accidental commits of logs in other parts of the workspace.

## Goal

Review and propagate consistent log hygiene patterns (e.g. `logs/` ignores, audit-specific rules, no tracked placeholders under log dirs) to the top-level `.gitignore` and relevant docs/hints in other monoliths where applicable.

## Acceptance criteria

- [ ] Audit root `.gitignore` for log-related patterns
- [ ] Review `.gitignore` and AGENTS.md in data_manager/, winston_v2/, winston_unit_test/, winston/ for gaps vs. new ecosystem approach
- [ ] Add/update rules for consistency (e.g. blanket log ignores where appropriate, notes referencing ADR-004 style)
- [ ] Add hint in ecosystem/hints/ or relevant AGENTS.md if needed
- [ ] Verify no log files are accidentally tracked in other repos

## Related

- `ecosystem/docs/session-reports/2026-07-06-1539-ecosystem-logs-gitignore.md`
- `ecosystem/.gitignore`
- `ecosystem/logs/audit/.gitignore`
- `ecosystem/docs/adr/ADR-004-ecosystem-audit-log.md`
- Root `.gitignore`
- Other monolith `.gitignore` files

## Out of scope

- Implementing full audit log systems in other monoliths (that's per their scope)
- Forcing changes in eta-service-2.0/ or openclawd-stack/ (separate domains)
