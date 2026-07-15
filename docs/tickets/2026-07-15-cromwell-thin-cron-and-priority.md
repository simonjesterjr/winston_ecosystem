# Ticket: Thin / LLM-light Cromwell cron + user priority (Tier 2)

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** Medium — after Tier 0 session isolation  
**Repos:** cross-monolith (`ecosystem/ai`, DM/Wv2 notify paths, optional MCP)  
**Source:** Session 2026-07-15 concurrency design  

## Problem

Cron jobs are full `agent_turn` prompts (skills + multi-tool + narrative). On CPU 8b each job can hold the global agent lock for many minutes. User commands wait; Ollama stays at 100% CPU.

Ecosystem doctrine already prefers: **Sidekiq owns truth; Cromwell narrates.** EOD does this (4:30 analysis → 4:35 fetch_only). Market snapshot and DM event relay still re-run agent loops.

## Scope

1. **DM event relay:** prefer push or deterministic post of `event.message` (thin path) — zero or minimal LLM.  
2. **Market snapshot cron:** tool → fixed short template (or Rails/MCP preformatted string); forbid extra tools in prompt (already partly stated — enforce with shorter max tokens / dedicated small model).  
3. **Priority policy:** user Telegram = P0; scheduled narrative = P1; dream = P2. Document and implement where nanobot allows; else ops runbook.  
4. Optional: cron model `cromwell-qwen2.5:3b` vs interactive `cromwell-qwen3:8b` on same Ollama (serial, shorter cron hold).  
5. Align skills (`winston-dm-sync-events`, `winston-market-snapshot`) with thin-path contracts.

## Acceptance

- [ ] At least one high-frequency cron (DM relay or hourly snapshot) does not require multi-minute 8b agent turns  
- [ ] Written priority policy in schedule README + AGENTS  
- [ ] EOD path remains fetch_only (no regression)  

## Related

- Tier 0: `2026-07-15-cromwell-cron-session-isolation-busy-ack.md`  
- Ticket D: `2026-07-15-cromwell-llm-cpu-reliability.md`  
- `ecosystem/ai/schedule/README.md` (CPU contention note)  
- Interfaces: Cromwell notification / DM events  

## Non-goals

- Dual-container capacity (Tier 1)  
- Changing Daily Analysis ownership away from Wv2 Sidekiq  
