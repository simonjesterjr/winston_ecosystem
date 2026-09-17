# Ticket: Ollama model category eval (ops vs lab vs light)

**Status:** Done  
**Priority:** P1  
**Date:** 2026-09-17  
**Origin:** John → CoS (parallel to P0 CUDA inventory; after RTX 3090)  
**DoD:** Desk has a scored shortlist: which tag for ops Cromwell, which for lab analyst, which for light/triage — with latency/quality/VRAM notes — and an explicit “do not pull yet” list.

## Problem

We run several local tags (`cromwell-qwen3:8b` primary, 3b/4b variants, `qwen3.5:9b`, `llama3.1:8b`, …) chosen largely in the CPU era. GPU changes the feasible set (size, quant, tool-use, thinking modes). Without a category bakeoff we will either stick with defaults too long or pull models ad hoc.

## Scope

1. **Inventory baseline** (from P0): current tags, VRAM when loaded, ctx, pin in `ai/MODEL_PIN.md`.
2. **Define categories** (jobs, not brand names):
   - **Ops router** — Telegram Cromwell tool-use, short grounded briefs, cron (primary today: `cromwell-qwen3:8b`)
   - **Light / triage** — quiet snapshots, classification, low-latency (candidate: `cromwell-qwen2.5:3b` / 4b)
   - **Lab analyst** — long-form PBR/journal commentary, Open WebUI (not Telegram default)
   - **Optional:** embedder-only; “thinking” variants only if tool-use stays reliable
3. **Candidates to compare** (examples — refine during work): same-family quants (Q4/Q5/Q8), newer Qwen/Llama/Mistral tool-capable mid-size that fit **≤~20GB** headroom on 3090 with ops primary resident, and any Cromwell-tuned successors already on disk.
4. **Eval protocol (short, not a research paper):**
   - Fixed prompts: (a) MCP-grounded EOD triage, (b) pending-confirm checker JSON, (c) quiet-vs-movers one-liner, (d) lab “explain this backtest day” paragraph from a stored Edge snapshot — **no Edge recomputation**
   - Metrics: wall latency p50/p95, VRAM, tool-call validity rate, groundedness (no invented fills), human preference on 5–10 samples
5. **Optimizations to consider:** quant level, `num_ctx` / `num_predict`, `think` on/off, concurrent>1 safety on GPU, keep-alive, speculative dual-load ops+light
6. Write results to `docs/analysis/YYYY-MM-DD-ollama-model-category-eval.md`; update `ai/MODEL_PIN.md` if winners change

## Non-goals

- Fine-tune / QLoRA bakeoff (separate P3+ tickets)
- Replacing deterministic DAR/sizer/Edge with model output
- Pulling every trending GGUF onto the box

## Acceptance

- [x] Category definitions + candidate list locked in ticket or analysis
- [x] Baseline numbers for current primary (+ light) on GPU
- [x] Scored comparison table for ≥1 alternative per category (or explicit “no better fit”)
- [x] Recommendation: keep / swap primary, adopt light router, lab default
- [x] `MODEL_PIN.md` + inventory ticket linked; INDEX updated

## Related

- P0 inventory: [`2026-09-17-winston-llm-desk-inventory.md`](2026-09-17-winston-llm-desk-inventory.md)
- Role re-eval: [`../../analysis/2026-09-17-llm-role-reeval-checker-narrator.md`](../../analysis/2026-09-17-llm-role-reeval-checker-narrator.md)
- CUDA priority: [`../../analysis/2026-09-17-cromwell-cuda-priority-revisit.md`](../../analysis/2026-09-17-cromwell-cuda-priority-revisit.md)
- Model pin: [`../../../ai/MODEL_PIN.md`](../../../ai/MODEL_PIN.md)
- Analyst adapter (future): [`2026-07-15-cromwell-analyst-adapter-future.md`](../2026-07-15-cromwell-analyst-adapter-future.md)
- Plan: [`../../../plans/winston-plus-llm.md`](../../../plans/winston-plus-llm.md)


## Outcome (2026-09-17)

Analysis: [`../../analysis/2026-09-17-ollama-model-category-eval.md`](../../analysis/2026-09-17-ollama-model-category-eval.md)

- **Ops:** keep `cromwell-qwen3:8b`
- **Light:** `cromwell-qwen2.5:3b`
- **Lab:** `qwen3.5:9b` (optional `qwen3:14b`)
- **Kimi:** cloud-only; 401; **skipped** per John
- Live Cromwell config **unchanged**
