# Ticket: Cromwell must always pass `id_or_name` on portfolio activate

**Status:** Proposed  
**Priority:** P2  
**Date:** 2026-07-21  
**Domain:** Cromwell MCP, portfolio lifecycle  
**Glossary:** Active, Operational Portfolio, reply_text

## Problem

Operator: “activate 9cf64e64” after a successful handoff. Cromwell did **not** call `wv2_activate_portfolio` with required `id_or_name` (no MCP audit row). User-facing error claimed missing `id_or_name` and then mixed **activate** vs **deactivate** copy. Transfer/successor had already landed; only attention flag failed.

## Scope

1. **Skills / workspace persona:** reinforce resolve-from-last-transfer `#id` and never call activate without `id_or_name`.  
2. **Examples:** prefer `activate #240` over bare short fingerprint.  
3. Optional MCP guard: if activate args empty, return structured `invalid_input` with example JSON (already schema-required — ensure agent surfaces schema error cleanly).  
4. Optional: regression prompt fixture / smoke that tool call includes `id_or_name` after transfer→activate turn.

## Non-goals

- Auto-activate after transfer (still forbidden unless user asks)  
- Capital Activation (real series) — separate ticket  

## Acceptance

- [ ] “activate &lt;id|name|fp&gt;” after transfer always produces MCP call with non-empty `id_or_name`  
- [ ] Error replies never confuse activate with deactivate  
- [ ] Skill text + AGENTS/TOOLS examples show numeric `#id` first  

## Related

- Session: `docs/session-reports/2026-07-21-0927-wut80-transfer-activate-recovery.md`  
- Skills: `ai/skills/winston-portfolio-lifecycle/SKILL.md`, `ai/skills/winston-wut-to-wv2/SKILL.md`  
- MCP: `ai/mcp/mcp_winston/server.py` (`wv2_activate_portfolio`, `_portfolio_id_payload`)  
- Related reliability: `2026-07-15-cromwell-llm-cpu-reliability.md`, `2026-07-09-cromwell-cron-llm-timeout.md`  
