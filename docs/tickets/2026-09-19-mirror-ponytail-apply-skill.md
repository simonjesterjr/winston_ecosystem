# Ticket: Mirror `/ponytail-apply` skill into Rails monoliths

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-09-19  
**Mode:** contractor  
**Monolith:** ecosystem (mirrors: winston_unit_test, winston_v2, broker_gateway, data_manager)  
**Area:** `.grok/skills/ponytail-apply/`  
**DoD:** each Rails monolith that lists the skill in `AGENTS.md` has the skill file; clones of a single repo still work

See: [`../session-reports/`](../session-reports/) wrap of WUT apply (`winston_unit_test/docs/session-reports/2026-09-19-1233-wut-ponytail-apply.md`). Authored in session `01a0ba69`, not the apply session.

## Problem

Workspace and `ecosystem/.grok/skills/ponytail-apply/SKILL.md` exist. `data_manager/AGENTS.md` and root `AGENTS.md` already name `/ponytail-apply`.

Untracked copies (2026-09-19 wrap):

- `winston_unit_test/.grok/skills/ponytail-apply/` (in stash `cos-dirty-pre-wut49`, not restored into the apply commit)
- `winston_v2/.grok/skills/ponytail-apply/`
- `broker_gateway/.grok/skills/ponytail-apply/`

Without the mirror, a clone of WUT / Winston v2 (Wv2) / Broker Gateway (BG) alone does not have the skill.

## Do

Copy `ecosystem/.grok/skills/ponytail-apply/SKILL.md` (or workspace `.grok/skills/`) into each Rails monolith `.grok/skills/ponytail-apply/`. Confirm `AGENTS.md` tables mention it. Separate commit from WUT ponytail cuts.

## Acceptance

- [ ] Skill present under WUT, Wv2, BG, data_manager (if missing)
- [ ] `AGENTS.md` rows agree
- [ ] Not mixed into the WUT ponytail-apply code commit
