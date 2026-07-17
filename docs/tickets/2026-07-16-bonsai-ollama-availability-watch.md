# Ticket: Watch for Bonsai 27B (and 8B) Ollama availability

**Status:** Proposed (watch active via scheduler)  
**Date:** 2026-07-16  
**Priority:** Low (opportunistic)  
**Repos:** `ai/` / Cromwell model ops  
**Source:** Session report `docs/session-reports/2026-07-16-1000-bonsai-core-model-advice.md`

## Problem

PrismML Bonsai 27B (ternary / 1-bit Qwen3.6-27B) is an attractive local quality step for Cromwell, but as of 2026-07-16 it is **not** available as a mainline Ollama tag. Cromwell’s production path is Ollama OpenAI-compat (`http://ollama:11434/v1`). We need a lightweight watch so we notice when community or Prism publishes a runnable Ollama model **without** rediscovering the topic every session.

## Watch criteria (any one is enough to “fire”)

1. Official or widely used Ollama library tag for **Bonsai 27B** / **Ternary-Bonsai-27B** that pulls cleanly on our Ollama version.  
2. Documented **mainline** llama.cpp/Ollama support for the ternary GGUF (no Prism fork required for basic chat + tools).  
3. Fallback: solid **Bonsai 8B** Ollama tag that is clearly maintained and tool-capable — note it for the 8B A/B ticket even if 27B is still blocked.

## Check procedure (agent or human)

```bash
# Local inventory
./bin/compose --profile ai exec ollama ollama list | grep -i bonsai || true

# Library search (host or container if search is available)
./bin/compose --profile ai exec ollama ollama search bonsai 2>/dev/null || true
```

Also check:

- https://ollama.com/search?q=bonsai  
- https://ollama.com/search?q=ternary-bonsai  
- https://huggingface.co/prism-ml (new GGUF / Ollama notes)  
- Optional: HN / r/LocalLLaMA for “Bonsai 27B Ollama”

## When found — do this

1. Update this ticket **Status** → `In progress` or `Done` with the exact tag name, size, and source URL.  
2. Unblock / prioritize:
   - `docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md` (if 8B)  
   - `docs/tickets/2026-07-16-bonsai-27b-lab-eval-when-runnable.md` (if 27B)  
3. **Do not** change `agents.defaults.model` until `docs/tickets/2026-07-16-cromwell-core-model-promotion-policy.md` checklist passes.  
4. Notify operator in session: tag name + recommended next ticket.

## Acceptance

- [ ] Periodic check method exists (scheduler and/or human runbook above)  
- [ ] On first positive hit: ticket updated with tag + links  
- [ ] Downstream eval ticket status bumped or explicitly deferred with reason  
- [ ] Negative results can stay silent; only status changes on positive or “still blocked after N weeks” note  

## Non-goals

- Running Prism fork as production Ollama replacement  
- Automatic model pull into production without eval  
- Signal/trading logic changes  

## Related

- Session: `docs/session-reports/2026-07-16-1000-bonsai-core-model-advice.md`  
- `docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md`  
- `docs/tickets/2026-07-16-bonsai-27b-lab-eval-when-runnable.md`  
- `docs/tickets/2026-07-16-cromwell-core-model-promotion-policy.md`  
- `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md`  
- HF: `https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf`  

## Log

| Date | Result |
|------|--------|
| 2026-07-16 | No Bonsai tags on local Ollama; 27B not mainline Ollama. Watch opened. |
| 2026-07-17 | **Not available (stock).** Local Ollama: no bonsai tags. Community **1-bit** tag `defyma85/bonsai-27b-q1_0` (~3.8 GB, 256K) at https://ollama.com/defyma85/bonsai-27b-q1_0 — Q1_0; stock Ollama still widely reported unable to load Q1_0 (see also eslider/bonsai-1.7b notes). **No Ternary-Bonsai-27B** Ollama tag. 8B still exists: `digitsflow/bonsai-8b` (~1.2 GB), `MichelRosselli/ternary-bonsai:8b-f16` (F16 tools-capable, not packed ternary). Status remains Proposed/watch. |
