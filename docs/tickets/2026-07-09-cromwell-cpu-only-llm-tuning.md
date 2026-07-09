# Ticket: CPU-only Cromwell/Ollama tuning (no hardware buy)

**Status:** In progress → largely **Done** (2026-07-09 implement pass)  
**Context:** 2026-07-09 hardware diagnosis on `sawtooth-ai` (System76 Thelio Mira). Confirmed pure-CPU Ollama is **correct** (no discrete GPU; Raphael iGPU 2 GiB cannot hold current models). Telegram cron failures (`Error calling LLM: timed out after 300s`) are a **workload vs CPU** problem, not a mis-mounted GPU.

## Goal

Make the local LLM stack **as good as it gets on this machine without buying a discrete GPU** — reliable cron Telegram posts, usable interactive chat, documented operator knobs.

## Hardware baseline (do not “fix” with GPU passthrough)

| Fact | Implication |
|------|-------------|
| Ryzen 9 9900X, ~92 GiB RAM, AVX-512 | Strong CPU appliance; Ollama already uses icelake backend, 12 threads, all cores |
| No NVIDIA / no discrete AMD GPU | Empty PCIe slots exist; discrete card is **out of scope** here |
| AMD Raphael iGPU only (2 GiB VRAM) | Do **not** mount `/dev/dri`/`/dev/kfd` or chase ROCm for these models |
| Stock `ollama/ollama:latest` | CUDA/Vulkan libs present; discovers `compute=cpu`, `total_vram=0` — expected |
| Concurrent WUT backtests | Steal cycles from Ollama at top-of-hour; ops consideration |

## Checklist (acceptance)

### A. Model & context (highest leverage)

- [x] Pick a **primary cron/tool model** that is not a heavy “thinking” path on CPU → `cromwell-qwen2.5:3b` (from `qwen2.5:3b`, tools, no thinking)
- [x] Set runtime `ai/data/cromwell-bot/config.json` + example `ai/configs/nanobot-cromwell.example.json` to the same intentional model
- [x] Reduce effective context: **`num_ctx` 8192**, `num_predict` 512 (Modelfile + agent options)
- [x] Create Modelfile tag: `ai/ollama/Modelfile.cromwell-cpu`

### B. Ollama service knobs

- [x] `OLLAMA_KEEP_ALIVE=24h`
- [x] `OLLAMA_NUM_PARALLEL=1`
- [x] `OLLAMA_FLASH_ATTENTION=1`
- [ ] Refresh/pin Ollama image (deferred; optional hygiene)
- [x] Do **not** enable Vulkan/ROCm for the iGPU

### C. Cron / agent workload

- [ ] Observe natural `market-snapshot-hourly` with non-error content (next MT session hour)
- [x] Skills already one MCP call + short prose for snapshot
- [x] Ops note: avoid heavy WUT backtests at top-of-hour MT (`ecosystem/ai/schedule/README.md`)

### D. Docs & hygiene

- [x] Document CPU-only defaults in `ai/README.md`, `ecosystem/deployment/README.md`, example config
- [ ] Track AI runtime in git — **deferred** (`docs/tickets/2026-07-09-track-ai-runtime-config-in-git.md`)

## Verification (2026-07-09)

| Check | Result |
|-------|--------|
| `ollama run cromwell-qwen2.5:3b "pong"` | ~2.5 s warm |
| `ollama ps` | model loaded, **UNTIL 24 hours**, ctx 8192, 100% CPU |
| Nanobot `/health` on compose net | `{"status":"ok"}` (`gateway.host` `0.0.0.0`) |
| MCP | 24 tools connected |

## Out of scope

- Buying / installing a discrete GPU  
- Cloud/API LLM for tool turns  
- Replacing nanobot  
- Session-binding / SSRF whitelist (done 2026-07-09)  
- Host `render` group / ROCm desktop tools  

## Related

- `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`  
- `docs/tickets/2026-07-04-sidekiq-ecosystem-health-watchdog.md` (implemented same session)  
- `docs/tickets/2026-07-09-track-ai-runtime-config-in-git.md` (pick up later)  
- Runtime: `ai/data/cromwell-bot/config.json`, `compose.yml` `ollama` service, `ai/ollama/Modelfile.cromwell-cpu`  
