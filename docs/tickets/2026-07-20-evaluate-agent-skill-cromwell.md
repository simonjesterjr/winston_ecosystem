# Ticket: evaluate-agent-skill for Cromwell skill changes

**Status:** Proposed  
**Priority:** P3  
**Source:** Session [`docs/session-reports/2026-07-20-2214-ai-workflow-skills-high-roi-install.md`](../session-reports/2026-07-20-2214-ai-workflow-skills-high-roi-install.md)

## Problem

Cromwell has ~13 `winston-*` skills plus cron allowlists. Skill prose is product surface; `ai-workflow-skills` includes `evaluate-agent-skill` + `validate-skills.py`, not yet installed for Winston AI assets.

## Acceptance criteria

- [ ] Decide install path (ecosystem-only vs Cromwell workspace)
- [ ] Install or adapt `evaluate-agent-skill` for `ecosystem/ai/skills/`
- [ ] Run once on a recent skill change (e.g. allowlist / report delivery)
- [ ] Optional: periodic retro using session reports + nanobot JSONL (`dev-lifecycle-retro` pattern)

## Related

- `ecosystem/ai/skills/`, `ecosystem/ai/schedule/`
- Ops runbook: `docs/operations/cron-tool-allowlist.md`
