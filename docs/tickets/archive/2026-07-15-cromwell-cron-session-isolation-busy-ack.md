# Ticket: Cromwell cron session isolation + busy-ack (Tier 0 / Phase 1)

**Status:** Done (session isolation + docs); busy-ack remains product gap  
**Date:** 2026-07-15  
**Priority:** High — next ops reliability after handoff reply contract  
**Repos:** `ecosystem/ai` (schedule + personas), runtime `ai/data/cromwell-bot`  
**Source:** Session 2026-07-15; single-threaded LLM + shared group session  
**AI version:** `1.4.3`  

## Problem

All Cromwell cron jobs bind `sessionKey: telegram:-1003884714483` (Sawtooth Main). Cron turns therefore:

1. Compete for `NANOBOT_MAX_CONCURRENT_REQUESTS=1` with user DMs  
2. **Auto-compact / archive the group chat session** mid-handoff  
3. Queue user messages silently (`Routed follow-up message to pending queue`) with **no busy ack**  

Observed (UTC):

```text
21:35 Cron dm-sync-events → Auto-compact session telegram:-1003884714483
21:36 Routed follow-up … pending queue
21:37 Idle-session compact (archived=16)
```

Persona rule says busy → immediate “try again…”; runtime does not enforce it.

## Scope

1. **Session split:** each cron job uses isolated `sessionKey` (e.g. `cron:dm-sync-events`, `cron:market-snapshot-hourly`) while keeping `originChannel` / `originChatId` for Telegram delivery to Sawtooth Main.  
2. **Seed path:** update `ecosystem/ai/schedule/cromwell-cron.json` + `bin/seed-cromwell-workspace --force-cron` notes; document in `ecosystem/ai/schedule/README.md`.  
3. **Busy ack:** when a user-facing message arrives while lock held, send short Telegram ack (nanobot config/behavior or lightweight pre-agent path if available). If product cannot ack without LLM, document gap + ops workaround.  
4. **Ops window:** optional temporary disable of hourly snapshot + dream during interactive smoke (flag or seed overlay).  
5. Cross-link ticket D (CPU reliability).

## Acceptance

- [x] Cron jobs no longer share `sessionKey` with live group chat (`cron:<job-id>`)  
- [x] User handoff history not wiped by cron compact during a transfer turn (isolated session keys; verify on next A smoke)  
- [x] User messages during cron either get busy-ack within ~15s or **documented impossibility** + ops runbook  
- [x] Seed + README document the sessionKey convention  

## Implementation (2026-07-15)

| Artifact | Change |
|----------|--------|
| `ecosystem/ai/schedule/cromwell-cron.json` | All jobs `sessionKey: cron:<id>`; origin still Sawtooth Main |
| `ecosystem/ai/schedule/README.md` | Tier 0 convention + busy-ack gap + still-serial note |
| `ecosystem/ai/personas/cromwell-agents.md` | Concurrency section matches runtime truth |
| `bin/seed-cromwell-workspace` | Help text documents sessionKey merge |
| Runtime | `bin/seed-cromwell-workspace` + `podman restart nanobot_cromwell` |

**Busy-ack:** nanobot 0.2.x has no pre-LLM busy Telegram; not fixed in this ticket.  

## Related

- Ticket D: `2026-07-15-cromwell-llm-cpu-reliability.md`  
- Ticket A: `2026-07-15-cromwell-transfer-reply-contract.md`  
- Schedule: `ecosystem/ai/schedule/cromwell-cron.json`  
- Compose: `NANOBOT_MAX_CONCURRENT_REQUESTS=1`, `OLLAMA_NUM_PARALLEL=1`  

## Non-goals

- Dual nanobot / dual Ollama (Tier 1 ticket)  
- LLM-free cron paths (separate ticket)  
- Raising concurrent requests without capacity plan  
