# Cromwell / Ollama model pin (desk SoT)

**Date locked:** 2026-09-17 (CoS P0 after RTX 3090 CUDA)  
**Bakeoff:** [`../docs/analysis/2026-09-17-ollama-model-category-eval.md`](../docs/analysis/2026-09-17-ollama-model-category-eval.md) — **no live primary change**

| Role | Tag | Where | Notes |
|------|-----|-------|-------|
| **Primary (ops)** | `cromwell-qwen3:8b` | `ai/data/cromwell-bot/config.json` → `agents.defaults.model` | Live: **100% GPU**, `num_ctx=8192`, `num_predict=1024`. Provider `openai` → `http://ollama:11434/v1`. Bakeoff ~145 tok/s; JSON+quiet OK. |
| **Fallback / light** | `cromwell-qwen2.5:3b` | Documented pin (not dual-routed yet) | Bakeoff ~262 tok/s. Spare: `cromwell-qwen3.5:4b`. |
| **Lab / Open WebUI** | `qwen3.5:9b` | `open-webui` → Ollama | Default lab. Optional challenger: `qwen3:14b` (~81 tok/s, ~10GB) — not Telegram ops. |
| **Not ops** | `llama3.1:8b` | — | Quiet-line discipline fail in bakeoff. |
| **Not local / skipped** | `kimi-k2.6:cloud` | Ollama cloud only | Needs ollama.com sign-in; prompts leave box. Skipped 2026-09-17. |

## Timeouts (compose `nanobot_cromwell`)
- `NANOBOT_MAX_CONCURRENT_REQUESTS=1` — keep until GPU concurrency proven (was CPU stampede mitigation).
- `NANOBOT_OPENAI_COMPAT_TIMEOUT_S=600`
- `NANOBOT_LLM_TIMEOUT_S=900`

## Change procedure
1. Edit `ai/data/cromwell-bot/config.json` model tag (operator path; gitignored secrets).
2. `./bin/compose --profile ai restart nanobot_cromwell`
3. Confirm `podman exec ollama ollama ps` shows GPU.
4. Update this file + archived inventory [`../docs/tickets/archive/2026-09-17-winston-llm-desk-inventory.md`](../docs/tickets/archive/2026-09-17-winston-llm-desk-inventory.md).

## Follow-on
- P0 inventory (Done): [`../docs/tickets/archive/2026-09-17-winston-llm-desk-inventory.md`](../docs/tickets/archive/2026-09-17-winston-llm-desk-inventory.md)
- P1 eval ticket (Done): [`../docs/tickets/archive/2026-09-17-ollama-model-category-eval.md`](../docs/tickets/archive/2026-09-17-ollama-model-category-eval.md)
