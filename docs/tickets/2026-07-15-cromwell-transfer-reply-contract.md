# Ticket: Cromwell transfer reply contract (skill + persona)

**Status:** In progress — docs seeded; **live smoke FAILED quality** (2026-07-15 ~15:13 MT)  
**Date:** 2026-07-15  
**Priority:** High — next session pick-up (**A**)  
**Source:** Session `2026-07-15-1404-telegram-transfer-agent-gap.md`  
**Plan / context:** Paper Telegram ops; ADR-006 handoff via MCP  
**AI version:** `ecosystem/ai/VERSION` → `1.4.2`

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

- [x] Skill documents mandatory success template and forbidden follow-ups  
- [x] Channel rules restate: no menus on handoff confirmation  
- [ ] Live Telegram transfer of an existing OP reports `action` + `#id` in first two lines  
- [ ] No unsolicited activate/sync/report suggestions after transfer  

## Live smoke (2026-07-15 ~15:13–15:25 MT) — FAIL quality

| Step | Result |
|------|--------|
| Transfer run 57 | MCP **ok** `legacy_updated` `#157` (tool JSON had full portfolio block) |
| User-facing reply | **FAIL** — long briefing + activate/sync/daily-analysis **menu** |
| “activate the portfolio” | **FAIL** — asked for id despite `#157` in prior bot message |
| “activate portfolio 157” | MCP activate **ok** in 40ms; agent then chained `get_portfolio_status`; multi-minute silence (CPU 8b + Flood Control risk) |
| Ground truth | `#157` **active=true**; also Active: `#12` Portfolio Blue · PBR62 |

**Root cause refinement:** Skills are **not auto-injected** — 8b must `read_file` them and usually does not. Always-on `AGENTS.md` HARD RULES + MCP `summary`/`reply_hint` are required; skill alone is insufficient.

## Implementation notes (2026-07-15)

| Artifact | Change |
|----------|--------|
| `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md` | Mandatory success template; action map; no auto-chain activate/sync/report |
| `ecosystem/ai/personas/cromwell-tools.md` | Mutating-tool lead-with-result rule |
| `ecosystem/ai/personas/cromwell-channels.md` | Handoff: no menus |
| `ecosystem/ai/personas/cromwell-agents.md` | HARD RULES block (1.4.2); removed transfer→activate chain default |
| `ecosystem/ai/skills/winston-portfolio-lifecycle/SKILL.md` | Activate playbook: resolve “the portfolio”; no re-ask; no post-activate menus |
| `ecosystem/ai/skills/winston-wut-portfolio-lifecycle/SKILL.md` | Transfer stops at reply contract |
| `ecosystem/ai/memory/templates/MEMORY.template.md` | Few-shot handoff line |
| `ecosystem/interfaces/winston-mcp-tools.md` | Transfer notes + `summary` field |
| `ai/mcp_winston/.../server.py` (host) | `_attach_agent_summary` for transfer/activate/deactivate |
| `bin/seed-cromwell-workspace` | Re-run after docs land |

## Related

- Skill: `ecosystem/ai/skills/winston-wut-to-wv2/SKILL.md`  
- Tickets B/C (export fidelity, MCP summary) reduce model confusion  
- Session report: transfer ok, reply bad  

## Non-goals

- New import endpoints  
- Auto-activate on import  
- Model swap alone as the “fix”  
