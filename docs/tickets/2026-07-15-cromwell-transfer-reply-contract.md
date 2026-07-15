# Ticket: Cromwell transfer reply contract (skill + persona)

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** High — next session pick-up (**A**)  
**Source:** Session `2026-07-15-1404-telegram-transfer-agent-gap.md`  
**Plan / context:** Paper Telegram ops; ADR-006 handoff via MCP

## Problem

Telegram transfer of WUT run 57 **succeeded** (`wv2_transfer_portfolio_from_wut` → `legacy_updated` OP `#157`), but Cromwell’s user-facing reply ignored the transfer result and wrote a generic portfolio briefing with activate/sync/report **menus**. Operator concluded “it failed.”

Root cause: agent report-writing after tools return, not missing import machinery.

## Scope (A)

1. Harden `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md` (and seeded workspace copy via `bin/seed-cromwell-workspace` when ready):
   - After transfer, **lead** with: `status`, `action`, `portfolio.id`, `name`, `active`, `execution_mode`, top `warnings`.
   - Map actions to plain English: `created` / `legacy_updated` / `forked` / `adopted` / `engaged_refuse` / `closed_refuse`.
   - One line: sole Active OP if unchanged.
   - **Forbidden** unless user asked: activate, sync, daily report, menus, “would you like to proceed.”
2. Persona / tools guidance (`cromwell-tools.md`, `cromwell-channels.md`, workspace `TOOLS.md` / `AGENTS.md` as needed):
   - After any **mutating** MCP tool, lead with that tool’s result; never only summarize a subsequent list dump.
3. Optional MEMORY / few-shot line: “transfer run N → report #id action=…”.
4. Re-seed Cromwell workspace and smoke one Telegram transfer reply quality check.

## Acceptance

- [ ] Skill documents mandatory success template and forbidden follow-ups  
- [ ] Channel rules restate: no menus on handoff confirmation  
- [ ] Live Telegram transfer of an existing OP reports `action` + `#id` in first two lines  
- [ ] No unsolicited activate/sync/report suggestions after transfer  

## Related

- Skill: `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md`  
- Tickets B/C (export fidelity, MCP summary) reduce model confusion  
- Session report: transfer ok, reply bad  

## Non-goals

- New import endpoints  
- Auto-activate on import  
- Model swap alone as the “fix”  
