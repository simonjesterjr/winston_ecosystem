# Ticket: Cromwell LLM CPU reliability (timeouts, think, cron isolation)

**Status:** In progress (ops fixes applied host-side; remaining work open)  
**Date:** 2026-07-15  
**Priority:** Medium (D — stability)  
**Source:** Session 2026-07-15 — 45 min “no reply”; LLM timed out 4× at 120s; qwen3 thinking burn  

## Problem

On CPU-only sawtooth-ai, `cromwell-qwen3:8b` with default nanobot OpenAI-compat **120s** timeout fails multi-turn agent prompts (SOUL + tools + history). Qwen3 **thinking** burns tokens before content. Concurrent 3b+8b resident and cron jobs stampede the single Ollama parallel slot. Operator sees silence or error; Telegram Flood Control can delay the eventual message.

## Done this session (host / compose — verify committed)

- Model: `cromwell-qwen3:8b` in `ai/data/cromwell-bot/config.json`  
- `providers.openai.extra_body.think: false`  
- `agents.defaults.reasoning_effort: "none"`  
- `num_predict` 1024  
- Root `compose.yml` nanobot env:  
  - `NANOBOT_OPENAI_COMPAT_TIMEOUT_S=600`  
  - `NANOBOT_LLM_TIMEOUT_S=900`  
  - existing `NANOBOT_MAX_CONCURRENT_REQUESTS=1`  
- Unload 3b when possible; warm 8b after restart  

**Note:** Root `compose.yml` and `ai/data/cromwell-bot/config.json` are operator-local (not ecosystem git by default). Capture durable defaults in `ai/configs/nanobot-cromwell.example.json` + docs.

## Remaining scope (D)

1. Update **example** config + `ai/README.md` / deployment README for 8b + think off + timeout env (CPU quality path vs 3b latency path).  
2. **Cron isolation:** prevent hourly snapshot / dream from polluting mid-DM session or starving Ollama during user turns (queue, separate session discipline, or busy-reply skill already in agents — enforce).  
3. Document Telegram **group privacy**: bot `can_read_all_group_messages=false` requires @mention or reply; optional BotFather privacy off.  
4. Avoid `bin/compose up --force-recreate` cascade with podman name conflicts — document safe nanobot-only recreate (`podman stop/rm nanobot` then `up -d --no-deps`).  
5. Optional: eval that transfer-ok replies contain `action` and portfolio id (ties to A).  

## Acceptance

- [ ] Example config documents think:false + timeout envs  
- [ ] User DM transfer completes without 120s timeout under normal load  
- [ ] Cron does not silently fail user turns for 10+ minutes without “busy” ack  
- [ ] Operator runbook snippet for mention + model + timeouts  

## Related

- Ticket A (reply quality)  
- Tier 0 session isolation + busy-ack: `2026-07-15-cromwell-cron-session-isolation-busy-ack.md`  
- Tier 2 thin cron + priority: `2026-07-15-cromwell-thin-cron-and-priority.md`  
- Tier 1 dual runtime: `2026-07-15-cromwell-parallel-capacity-dual-runtime.md`  
- `ecosystem/docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`  
- Compose comment already noted 2m timeout stampede  

## Non-goals

- GPU dependency  
- Replacing nanobot  
