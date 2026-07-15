# Ticket: Cromwell parallel capacity — dual runtime (Tier 1)

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** Low–medium — only after Tier 0 (and preferably Tier 2 thin-cron)  
**Repos:** compose / `ai/` runtime  
**Source:** Session 2026-07-15 concurrency design  

## Problem

`NANOBOT_MAX_CONCURRENT_REQUESTS=1` and `OLLAMA_NUM_PARALLEL=1` serialize all agent work. Raising either naively on one CPU Ollama often increases timeouts. Real parallelism needs **isolated runtimes** and RAM budget, not just config knobs.

## Scope (options — pick via short design note before build)

1. **Dual Ollama (same host):** `ollama_interactive` (8b) + `ollama_cron` (3b); cgroup/nice cron lower priority.  
2. **Dual nanobot:** ops bot (user) + broadcast bot (cron) — Telegram token/session exclusivity must be designed first.  
3. **Remote interactive LLM** (GPU host or API) for tool-heavy user turns; local 3b for cron.  
4. Measure: do **not** set `OLLAMA_NUM_PARALLEL>1` or `NANOBOT_MAX_CONCURRENT>1` without a load test plan on sawtooth-ai.

## Acceptance

- [ ] Written decision: which option (or “defer to GPU”)  
- [ ] If dual Ollama: compose profile + resource notes; interactive user turn does not wait on cron generate  
- [ ] If dual nanobot: no double-poll on one bot token; sessions documented  
- [ ] Mutation tools remain safe under concurrency (no dual concurrent transfer/activate without idempotency review)  

## Related

- Tier 0: `2026-07-15-cromwell-cron-session-isolation-busy-ack.md`  
- Tier 2: `2026-07-15-cromwell-thin-cron-and-priority.md`  
- Ticket D: `2026-07-15-cromwell-llm-cpu-reliability.md`  
- Ticket: `2026-07-09-thelio-discrete-gpu-for-ollama.md` (if present)  

## Non-goals

- Replacing nanobot  
- Parallel conflicting portfolio mutations  
