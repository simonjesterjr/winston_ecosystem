# Ticket: Draft Winston model specialization plan (or ADR)

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** Low (roadmap capture)  
**Source:** Session report `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`

## Problem

LoRA/QLoRA adapters for Cromwell are a natural extension of the MCP + local Ollama layer, but the ecosystem has no short canonical note that states placement, non-goals, and sequencing. Without it, future sessions may re-debate whether fine-tuning belongs inside monoliths or on the trading host.

## Scope

Draft a half-page plan under `ecosystem/plans/` (preferred first) or promote to ADR when decisions lock:

1. **Problem** — tool reliability, Winston dialect, Telegram voice; optional future analysis adapter.
2. **Non-goals** — LLM does not generate signals or mutate capital without confirmation; no training Sidekiq on the trading host.
3. **Placement** — adapters are optional `ai/` profile artifacts (Ollama tags / Modelfiles); core DM/WUT/Wv2 unchanged.
4. **Data sources** — MCP audit JSONL, successful nanobot sessions, skills/SOUL as target behavior.
5. **Lifecycle** — offline train (GPU) → versioned adapter → serve on Ollama (CPU OK for small models) → optional imatrix quant.
6. **Sequencing** — after MCP reliability + gold traces; RAG/few-shot before first LoRA train.
7. Cross-link `plans/winston-plus-llm.md` Phase 4 and `plans/winston-mcp-next-steps.md`.

## Acceptance

- [ ] Plan (or ADR) filed and linked from `winston-plus-llm.md`
- [ ] Explicit non-goals and “core runs without AI” invariant stated
- [ ] Related tickets (trace harvest, QLoRA recipe) linked

## See also

- `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`
- `plans/winston-plus-llm.md`
- `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md` (stabilize before train)
