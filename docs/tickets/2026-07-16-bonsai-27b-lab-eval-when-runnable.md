# Ticket: Lab-eval Bonsai 27B (ternary) when runtime is viable

**Status:** Proposed / blocked on runtime  
**Date:** 2026-07-16  
**Priority:** Low until Ollama (or supported runner) available; then Medium  
**Repos:** `ai/` lab only — not production default  
**Source:** Session report `docs/session-reports/2026-07-16-1000-bonsai-core-model-advice.md`

## Problem

Ternary Bonsai 27B (~5.9 GB, ~95% of FP16 quality claims) could be a strong **interactive** managing model for Cromwell once it can run without a fragile custom stack. On **CPU-only sawtooth-ai**, even a small-on-disk 27B may still be too slow for multi-turn MCP if prompt eval dominates. We need a **lab evaluation**, not an optimistic core swap.

## Blockers

- [ ] Runnable path: mainline Ollama tag **or** explicitly accepted lab runner (document which)  
- [ ] Watch ticket fired: `docs/tickets/2026-07-16-bonsai-ollama-availability-watch.md`  
- Prefer completing 8B A/B first if both exist: `docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md`

## Scope (lab)

1. **Load + smoke:** chat only, then one tool call via nanobot OpenAI-compat if wired.  
2. **Latency budget:** warm-model multi-tool turn must stay under configured timeouts (`NANOBOT_OPENAI_COMPAT_TIMEOUT_S` / LLM timeout) on sawtooth-ai **or** document that 27B requires GPU host / dual runtime.  
3. **Quality harness:** same scenarios as 8B A/B ticket (identity, list, snapshot discipline, transfer reply contract, no eager tools).  
4. **Role decision:**  
   - interactive only (cron stays 3B / thin)  
   - reject for this host  
   - defer to GPU ticket (`docs/tickets/2026-07-09-thelio-discrete-gpu-for-ollama.md`)  
5. Optional: note vision usefulness for chart screenshots (not required for pass).

## Acceptance

- [ ] Lab runner documented (commands, container, model path)  
- [ ] Scorecard vs current `cromwell-qwen3:8b` (quality + latency)  
- [ ] Written recommendation: reject / GPU-only / dual-runtime interactive / promote after policy  
- [ ] No change to production default without promotion policy checklist  

## Non-goals

- Making 27B own hourly cron on CPU  
- Replacing nanobot  
- Production Prism fork as permanent Ollama substitute without an ADR  

## Related

- `docs/tickets/2026-07-16-bonsai-ollama-availability-watch.md`  
- `docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md`  
- `docs/tickets/2026-07-16-cromwell-core-model-promotion-policy.md`  
- `docs/tickets/2026-07-15-cromwell-parallel-capacity-dual-runtime.md`  
- `docs/tickets/2026-07-15-cromwell-thin-cron-and-priority.md`  
- HF ternary GGUF: `https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf`  
- Prism announce: `https://prismml.com/news/bonsai-27b`  
