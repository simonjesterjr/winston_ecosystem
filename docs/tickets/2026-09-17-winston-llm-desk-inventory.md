# Ticket: Winston LLM desk inventory (post-CUDA)

**Status:** Proposed  
**Date:** 2026-09-17 (work window)  
**Priority:** P2  
**Scheduled:** Thursday 2026-09-17 morning (CoS routine)  
**Origin:** John → CoS 2026-09-16 after RTX 3090 + Ollama CUDA confirmation

## Problem

CUDA is confirmed on sawtooth-ai for compose `ai` / `ollama`. Before any model tournament, we need a **desk inventory** of every LLM touchpoint so cron/MCP/Telegram expectations match GPU reality.

## Scope (inventory first, short eval second)

1. Map every LLM touchpoint: Cromwell/nanobot, `winston_mcp`, Sidekiq/cron jobs, Open WebUI, any Wv2 helpers.
2. Per touchpoint: model tag, schedule, timeout, CPU vs GPU expectation, failure mode.
3. Short eval outline (not a bakeoff): latency / quality on the 2–3 models actually run (Cromwell primary + fallback) **on GPU**.

## Non-goals

- Full model tournament / QLoRA bakeoff
- Changing Cromwell default model size in this ticket (separate decision after inventory)

## Acceptance

- [ ] Ticket filled with inventory table
- [ ] INDEX stays accurate
- [ ] Links to CUDA session + deployment GPU notes
- [ ] 1–2 page result (ticket body or short analysis) with eval outline

## Related

- Session: [`../session-reports/2026-09-16-1955-rtx3090-ollama-cuda.md`](../session-reports/2026-09-16-1955-rtx3090-ollama-cuda.md)
- CDI cleanup: [`2026-09-16-podman-nvidia-cdi-cleanup.md`](2026-09-16-podman-nvidia-cdi-cleanup.md)
- Ops: [`../../deployment/README.md`](../../deployment/README.md) GPU section
- Compose mirror: [`../../deployment/workspace-compose.yml`](../../deployment/workspace-compose.yml)
