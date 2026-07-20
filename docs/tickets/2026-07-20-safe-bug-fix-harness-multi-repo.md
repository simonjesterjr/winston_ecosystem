# Ticket: Multi-repo isolation policy + optional full safe-bug-fix harness

**Status:** Proposed  
**Priority:** P2  
**Source:** Session [`docs/session-reports/2026-07-20-2214-ai-workflow-skills-high-roi-install.md`](../session-reports/2026-07-20-2214-ai-workflow-skills-high-roi-install.md)

## Problem

Winston uses a lightweight bug-fix lane without `.agent-harness`. The full `safe-bug-fix` kit from `ai-workflow-skills` assumes isolated candidate worktrees and a single-repo policy file. Sawtooth has independent git repos (DM, WUT, Wv2, ecosystem).

## Acceptance criteria

- [ ] Written multi-repo isolation policy (when to use worktrees, which repo is primary, how cross-repo patches are identified)
- [ ] Decision: install full harness in one or more repos, or keep lightweight lane as permanent default
- [ ] If install: `.agent-harness/policy.yaml` aligned with each `PROJECT_PROFILE.md`
- [ ] Documented handoff: `manage-issue-ticket` → harness vs lightweight

## Notes

Do not block day-to-day fixes on this ticket — `lightweight-bug-fix` is the current default.
