# Analysis: High-ROI AI workflow skills install (2026-07-20)

## Summary

Installed the next engineering spine from `ai-workflow-skills` into the Winston multi-monolith workspace without the full `.agent-harness` safe-bug-fix stack.

## What landed

| Item | Location |
|------|----------|
| `rails-code-review` + project notes | `data_manager`, `winston_unit_test`, `winston_v2` `.grok/skills/` |
| `PROJECT_PROFILE.md` | each of the three Rails monoliths |
| `manage-issue-ticket` | root + ecosystem + all three monoliths |
| `lightweight-bug-fix` | same (Winston-specific; no harness) |
| `investigate-system-variance` + Winston overlay | same; notes in `references/project-notes.md` |
| `baseline-replay`, `ship-to-test` | same |
| Issue template | `docs/issues/_template.md` |
| Ticket archive + INDEX + Priority | `docs/tickets/archive/`, `docs/tickets/INDEX.md` |
| Operations runbooks | `docs/operations/` (README + MCP recreate + cron allowlist) |
| AGENTS / docs README / record skill | updated skill menus and filing rules |

## Explicitly deferred

- Full `safe-bug-fix` + `.agent-harness` worktree isolation (multi-repo workspace needs a deliberate policy)
- Django / React / Next / .NET / Kerberos skills
- Bulk human re-prioritization of every `unset` ticket

## How to use (defaults)

1. Defect → `manage-issue-ticket` → `ready` → `lightweight-bug-fix`
2. “Why do these systems disagree?” → `baseline-replay` / `investigate-system-variance`
3. Ready to validate on compose → `ship-to-test`
4. Rails health audit → `rails-code-review` in the target monolith
5. Done tickets → `docs/tickets/archive/`; backlog → `INDEX.md`
