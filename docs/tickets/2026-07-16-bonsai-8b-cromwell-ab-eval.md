# Ticket: Bonsai 8B vs cromwell-qwen3:8b A/B for Cromwell

**Status:** Proposed  
**Date:** 2026-07-16  
**Priority:** P2
**Repos:** `ai/` Cromwell  
**Source:** Session report `docs/session-reports/2026-07-16-1000-bonsai-core-model-advice.md`

## Problem

If a tool-capable **Bonsai 8B** (or Ternary Bonsai 8B) becomes easy to run under Ollama, it may improve agentic quality at a similar size to our current core (`cromwell-qwen3:8b`, ~5.2 GB). Public benchmarks are not enough — Cromwell needs **schema-strict MCP**, short Telegram prose, and fail-closed behavior on CPU.

## Preconditions

- Runnable Ollama (or drop-in OpenAI-compat) tag for Bonsai 8B class — see watch ticket.  
- Production remains on `cromwell-qwen3:8b` until this ticket accepts promote.

## Scope

1. **Create side tag** (do not overwrite production tag), e.g. `cromwell-bonsai:8b` via Modelfile mirroring `ai/ollama/Modelfile.cromwell` (num_ctx / num_predict choices for CPU).  
2. **Fixed scenario harness** (scripted prompts + MCP or recorded tool results), minimum:
   - Greeting / identity (Cromwell, not model name)  
   - `wv2_list_portfolios` path: tool called, no invented portfolios  
   - Market snapshot cron-style: real tool, **no** `path/to/file.txt`, no fake “stable markets” without tools  
   - Transfer / activate style: paste `reply_text` / action + id when MCP returns it  
   - “Don’t call tools” chat: no eager tool spam  
3. **Metrics:** tool-call correctness, hallucinated completions, turns-to-done, wall-clock p50/p95 on warm model (CPU), timeout rate under light load.  
4. **Document result** in ticket log + short note in `ai/README.md` model guidance if either wins clearly.

## Acceptance

- [ ] Side tag runs through nanobot OpenAI-compat with tools  
- [ ] Scorecard vs `cromwell-qwen3:8b` on harness (≥5 scenarios)  
- [ ] Explicit recommend: keep base / promote interactive only / reject  
- [ ] If promote: follow `docs/tickets/2026-07-16-cromwell-core-model-promotion-policy.md` (cron stays small)

## Non-goals

- Replacing cron model with 8B Bonsai if interactive wins  
- Training / LoRA (separate tickets)  
- 27B eval (separate ticket)

## Related

- `docs/tickets/2026-07-16-bonsai-ollama-availability-watch.md`  
- `docs/tickets/2026-07-16-bonsai-27b-lab-eval-when-runnable.md`  
- `docs/tickets/2026-07-16-cromwell-core-model-promotion-policy.md`  
- `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md`  
- `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`  
- `ai/README.md` model choice section  
