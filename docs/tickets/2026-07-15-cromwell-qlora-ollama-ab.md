# Ticket: Offline QLoRA recipe + Ollama tag A/B for Cromwell

**Status:** Proposed  
**Date:** 2026-07-15  
**Priority:** Low (after gold SFT set)  
**Source:** Session report `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`

## Problem

Once a gold tool-use SFT set exists, we need a repeatable offline train path and a safe way to serve the adapter on the optional `ai` profile so Telegram Cromwell can A/B base vs specialized model without touching Rails monoliths.

## Preconditions

- Gold SFT dataset process and seed set: `docs/tickets/2026-07-15-cromwell-trace-harvest-gold-sft.md`
- Model specialization plan: `docs/tickets/2026-07-15-winston-model-specialization-plan.md`

## Scope

1. **Train (offline / GPU host, not trading compose daily path):** QLoRA on chosen base (candidate: Qwen2.5 3B for CPU serve, or 7B/8B if quality wins and host can load it).
2. Export adapter (or merged weights) in a form Ollama can load; document `ollama create cromwell-winston:…` (or similar tag).
3. **Serve:** document Modelfile / config switch in `ai/configs` example; keep base tag available for rollback.
4. **A/B metrics (Telegram or scripted MCP):** tool selection accuracy, hallucinated paths rate, turns-to-done on fixed scenarios (transfer, daily report, confirm loop).
5. Optional later: imatrix-aware quant after merge (orthogonal; document only if needed for disk/RAM).

## Non-goals

- Signal generation or risk sizing in the model
- Training as a Sidekiq job on sawtooth-ai
- Replacing skills/MCP schemas (adapters reduce babysitting; contract stays)

## Acceptance

- [ ] Train recipe documented (commands, hardware assumption, data path)
- [ ] Ollama tag create/serve steps in `ai/README.md` or deployment README
- [ ] A/B checklist with pass/fail vs base model on fixed prompts
- [ ] Rollback = switch model name in nanobot config only

## See also

- `docs/session-reports/2026-07-15-1615-lora-qlora-ecosystem-fit.md`
- `ai/ollama/Modelfile.cromwell-cpu`
- `plans/winston-plus-llm.md` Phase 4
