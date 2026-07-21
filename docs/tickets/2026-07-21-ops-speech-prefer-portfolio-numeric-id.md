# Ticket: Prefer numeric portfolio `#id` in ops speech and skill examples

**Status:** Proposed  
**Priority:** P3  
**Date:** 2026-07-21  
**Domain:** Cromwell skills, operator UX  
**Glossary:** Operational Portfolio, fingerprint

## Problem

Short fingerprint speech (“activate 9cf64e64”) is ambiguous when two OPs share a display suffix (e.g. #240 and #241 both “Portfolio Blue · 9cf64e64”). Numeric id is unique and matches internal API digit path.

## Scope

1. Update skill examples (`winston-portfolio-lifecycle`, `winston-wut-to-wv2`, transfer success template) to lead with `#{id}`.  
2. Workspace AGENTS/TOOLS: short-fp optional secondary only.  
3. Optional: MCP `reply_text` for list/status always includes `#id` first (if not already).

## Non-goals

- Removing fingerprint from display names  
- Full fingerprint resolution product work (see sibling ticket)  

## Acceptance

- [ ] Skill playbooks show `activate #157` / `id_or_name: "157"` as primary examples  
- [ ] Transfer success template still requires `#id` on line 1  
- [ ] No skill example uses bare 8-hex as the only identifier  

## Related

- Session: `docs/session-reports/2026-07-21-0927-wut80-transfer-activate-recovery.md`  
- Sibling: `2026-07-21-cromwell-activate-id-or-name.md`  
- Sibling: `2026-07-21-portfolio-id-or-name-fingerprint-resolution.md`  
