# Ticket: MCP deactivate + Cromwell confirmation skill

**Status:** Done (2026-07-14 Phase 2B)  
**Date:** 2026-07-14  
**Source:** Paper Telegram roadmap Phase 2; session `2026-07-14-1112-paper-telegram-phase0-1.md`

## Problem

1. Skills/docs reference `wv2_deactivate_portfolio` but MCP server lacks the tool (HTTP + rake exist).  
2. Confirm tools exist (`wv2_confirm_journal`, etc.) but `winston-confirmation-loop` skill is missing (Part 2A).

## Scope

1. Add MCP `wv2_deactivate_portfolio` → `POST /internal/portfolios/deactivate`.  
2. Update `interfaces/winston-mcp-tools.md` if needed.  
3. Seed skill `winston-confirmation-loop` (list pending → confirm → status).  
4. Register in `cromwell-agents.md`; `bin/seed-cromwell-workspace`.  
5. Optional: `winston-position-inquiry` skill (status tool already exists).

## Acceptance

- [x] Deactivate via MCP tool + internal `id_or_name` (smoke on non-focus #5; #12 remains sole Active)  
- [x] Confirmation skill present and seeded (`ecosystem/ai` v1.4.0 → workspace)  
- [x] Telegram or MCP smoke: list pending → confirm path documented in skill + ops shell  

## Delivery notes (2026-07-14)

- MCP: `wv2_deactivate_portfolio`; activate/deactivate map `id_or_name` → `{id}`/`{name}`  
- Internal: `find_portfolio_from_params` accepts `id_or_name`  
- Skill: `ecosystem/ai/skills/winston-confirmation-loop/SKILL.md`  
- Registered in `cromwell-agents.md`; `bin/seed-cromwell-workspace` run

## Related

- `ai/mcp_winston/mcp_winston/server.py`  
- `ecosystem/plans/cromwell-ai-skills-part2.md` Phase 2A  
