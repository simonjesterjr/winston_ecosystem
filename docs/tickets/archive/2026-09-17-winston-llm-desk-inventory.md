# Ticket: Winston LLM desk inventory (post-CUDA)

**Status:** Done  
**Date:** 2026-09-17  
**Priority:** P2  
**Scheduled:** Thursday 2026-09-17 morning (CoS routine)  
**Origin:** John → CoS 2026-09-16 after RTX 3090 + Ollama CUDA confirmation  
**Closed:** 2026-09-17 afternoon re-verify (inventory + GPU eval outline; no live model swap)

## Problem

CUDA is confirmed on sawtooth-ai for compose `ai` / `ollama`. Before any model tournament, we need a **desk inventory** of every LLM touchpoint so cron/MCP/Telegram expectations match GPU reality.

## Scope (inventory first, short eval second)

1. Map every LLM touchpoint: Cromwell/nanobot, `winston_mcp`, Sidekiq/cron jobs, Open WebUI, any Wv2 helpers.
2. Per touchpoint: model tag, schedule, timeout, CPU vs GPU expectation, failure mode.
3. Short eval outline (not a bakeoff): latency / quality on the 2–3 models actually run (Cromwell primary + fallback) **on GPU**.

## Non-goals

- Full model tournament / QLoRA bakeoff *(ran same day as a separate ticket; results cited below)*
- Changing Cromwell default model size in this ticket (separate decision after inventory — **not taken**; pin stays `cromwell-qwen3:8b`)

## Acceptance

- [x] Ticket filled with inventory table
- [x] INDEX stays accurate (this ticket archived)
- [x] Links to CUDA session + deployment GPU notes
- [x] 1–2 page result (this body) with eval outline

## Related

- Session: [`../../session-reports/2026-09-16-1955-rtx3090-ollama-cuda.md`](../../session-reports/2026-09-16-1955-rtx3090-ollama-cuda.md)
- CDI cleanup: [`../2026-09-16-podman-nvidia-cdi-cleanup.md`](../2026-09-16-podman-nvidia-cdi-cleanup.md)
- Ops: [`../../../deployment/README.md`](../../../deployment/README.md) GPU section
- Compose: host `compose.yml` · mirror [`../../../deployment/workspace-compose.yml`](../../../deployment/workspace-compose.yml)
- Pin: [`../../../ai/MODEL_PIN.md`](../../../ai/MODEL_PIN.md)
- Bakeoff (same day, archived): [`2026-09-17-ollama-model-category-eval.md`](2026-09-17-ollama-model-category-eval.md) · analysis [`../../analysis/2026-09-17-ollama-model-category-eval.md`](../../analysis/2026-09-17-ollama-model-category-eval.md)
- Role / priority: [`../../analysis/2026-09-17-llm-role-reeval-checker-narrator.md`](../../analysis/2026-09-17-llm-role-reeval-checker-narrator.md) · [`../../analysis/2026-09-17-cromwell-cuda-priority-revisit.md`](../../analysis/2026-09-17-cromwell-cuda-priority-revisit.md)

---

## Inventory (re-verified 2026-09-17 ~14:00+ MT)

**Network:** compose `sawtooth_default`. Ollama **not** published on the host (`:11434` compose-internal only). Nanobot `/health` on `127.0.0.1:18790`. Open WebUI `127.0.0.1:8080`.

**Live GPU:** RTX 3090, driver `595.91.07`, ~6.3 / 24.0 GiB used. `ollama ps`: `cromwell-qwen3:8b` **100% GPU**, ctx 8192, keep-alive 24h.

**Pin (live config, not the example file):** `ai/data/cromwell-bot/config.json` → `agents.defaults.model = cromwell-qwen3:8b`, `provider=openai` → `http://ollama:11434/v1`, `num_ctx=8192`, `num_predict=1024`, `think: false`. Example `ai/configs/nanobot-cromwell.example.json` still defaults **3b** (clone-safe; live SoT is `MODEL_PIN.md`).

| Touchpoint | Model | Schedule | Timeout | CPU/GPU | Failure mode | Status 2026-09-17 |
|------------|-------|----------|---------|---------|--------------|-------------------|
| `ollama` | Tags on disk: `cromwell-qwen3:8b` (loaded), `qwen3:8b`, `cromwell-qwen2.5:3b`, `cromwell-qwen3.5:4b`, `qwen3.5:9b`, `qwen3.5:4b`, `qwen2.5:3b`, `llama3.1:8b`, `qwen3:14b` (bakeoff leftover), `kimi-k2.6:cloud` (manifest only) | always-on `--profile ai` | n/a | **GPU** (classic `/dev/nvidia*` + driver `.so` binds; CDI still broken) | container down → all LLM fail closed | **healthy**; host `:11434` unpublished (expected) |
| `nanobot_cromwell` **interactive Telegram** | primary `cromwell-qwen3:8b` | on demand (John 1-1 / allowFrom) | OpenAI-compat **600s** / LLM **900s**; `NANOBOT_MAX_CONCURRENT_REQUESTS=1` | expects GPU Ollama | timeout / queue behind cron or `dream` → Telegram silence; busy-ack still a documented gap | `/health` **200**; podman may show “starting” while HTTP is ok |
| `nanobot_cromwell` **catalog cron** (5 jobs) | same 8b (no sessionKey dual-route yet) | see table below | same 600/900; MCP client `toolTimeout` **180s** | GPU | allowlist miss / MCP down / queued lock | all five `lastStatus=ok` today (EOD last ok **yesterday** 16:35 MT — next is 16:35 today) |
| `nanobot_cromwell` **`dream`** | same 8b | **every 2h** (`everyMs: 7200000`), `kind: system_event` | last run **~59s** | GPU | unlisted in `cron-tool-allowlist.json` (no MCP); still holds the global lock; known MEMORY path hygiene ticket | **live, not in** `ecosystem/ai/schedule/cromwell-cron.json` |
| Heartbeat | — | `gateway.heartbeat.enabled=false` | — | — | — | **off** (cron owns broadcasts) |
| `winston_mcp` | **no LLM** (HTTP → Wv2/WUT/DM `/internal/*`) | always-on ai | toolTimeout 180s | N/A | DNS/getaddrinfo if ai profile down | `/health` **200** from sidekiq (0.001s); SSE `http://winston_mcp:8088/sse` |
| `open-webui` | operator pick (lab default pin `qwen3.5:9b`) | on-demand | UI | via Ollama GPU | UI only; can dual-load a large tag and steal VRAM from ops keep-alive | host `127.0.0.1:8080` → **200** |
| DM `EcosystemHealthCheckJob` | **no LLM** | hourly `:10` (Telegram only if degraded) + daily **06:05** MT (always) | HTTP 5s | N/A | false DEGRADED if compose DNS fails | mcp/ollama/nanobot **200** from `data_manager_sidekiq` |
| Wv2 `DailyAnalysisJob` | **no LLM** | 16:30 MT weekdays | Rails | CPU | journals still SoT | Cromwell EOD uses `fetch_only` — **does not** re-run analysis |
| Wv2 `TelegramReportDelivery` | **no LLM** | after DAR | Bot API | N/A | PDF post can race Cromwell EOD narrative | Bot API `sendDocument` to Sawtooth Main |
| Wv2/WUT `LlmClient` / `OllamaClient` | — | — | — | — | — | **absent** (Phase 1 still nanobot-edge) |
| Bakeoff harness | one-off tags | 2026-09-17 only | — | GPU | leftover `qwen3:14b` / cloud Kimi on disk | not a production caller |
| Builder Grok TUI (this session) | cloud Grok | operator | — | WAN | **not** a Winston desk LLM | out of inventory (Builder plane) |

### Cromwell catalog cron (LLM)

Source of truth: `ecosystem/ai/schedule/cromwell-cron.json` + `manifest.yaml`. Runtime: `ai/data/cromwell-bot/workspace/cron/jobs.json`. Allowlist: `ecosystem/ai/schedule/cron-tool-allowlist.json`. Channel: Sawtooth Main `-1003884714483`.

| Job id | Cron (America/Denver) | MCP allowed | Last run (UTC) |
|--------|----------------------|-------------|----------------|
| `ecosystem-status-daily` | `0 6 * * *` | list portfolios / pending / fetch_only DAR / WUT portfolios / DM events | 2026-09-17 12:00 ok |
| `market-snapshot-open` | `30 7 * * 1-5` | `wv2_market_snapshot` only | 2026-09-17 13:30 ok |
| `market-snapshot-hourly` | `0 8-14 * * 1-5` | `wv2_market_snapshot` only | 2026-09-17 20:00 ok (14:00 MT) |
| `dm-sync-events` | `35,45 15 * * 1-5` | `dm_get_cromwell_events` only | 2026-09-17 21:45 ok |
| `eod-daily-report` | `35 16 * * 1-5` | `wv2_get_daily_activity_report` **fetch_only** | 2026-09-16 22:35 ok |

Staff-roster Saturday process-eval / adversary file-only crons are **not seeded**. Dual-role 3b-for-cron is **documented, not implemented** (single `agents.defaults.model`).

### Findings (inventory, not new defects)

1. **`dream` is a real LLM consumer** (~59s / 2h) missing from the schedule catalog and allowlist. Path hygiene already ticketed: [`../2026-07-13-cromwell-dream-memory-path-hygiene.md`](../2026-07-13-cromwell-dream-memory-path-hygiene.md).
2. **Docs lagged GPU:** `ecosystem/ai/schedule/README.md` still said CPU-only; compose comments still justified `MAX_CONCURRENT=1` as “CPU Ollama.” Concurrent=1 stays (one Ollama slot); rationale is now serial **agent lock**, not missing VRAM. Comments refreshed with this close-out.
3. **Example config ≠ live pin.** First-time clone still copies 3b. Live Cromwell is 8b on GPU.
4. **`kimi-k2.6:cloud` is on disk** from the bakeoff; 401 without ollama.com sign-in; **do not pin** (WAN).
5. **Open WebUI can dual-load** a 14b (~10 GB) beside ops 8b (~6.6 GB) → ~17 GB / 24 GB. Unload challengers after lab use.

---

## Eval outline (GPU) — 2–3 models actually run

This ticket asked for a **short** latency/quality outline on the models the desk actually runs, not a research bakeoff. Same-day category eval (`n=26`, temp 0.2, `think=false`, `num_ctx=4096`) already produced the numbers; outline below is the desk cut.

**Models in play**

| Role | Tag | Why it is “actually run” |
|------|-----|--------------------------|
| Ops primary | `cromwell-qwen3:8b` | Live Telegram + every catalog cron |
| Light / fallback | `cromwell-qwen2.5:3b` | On disk; pin documented; **not dual-routed** |
| Lab | `qwen3.5:9b` | Open WebUI; optional `qwen3:14b` challenger |

**Protocol (enough to trust the pin)**

- **a** MCP-grounded EOD triage (Mode C paper books)  
- **b** checker JSON `TAKE|SIZE_DOWN|SKIP|HOLD`  
- **c** exact quiet line `All markets quiet.`  
- **d** lab explain from a stored Edge snapshot — **no Edge recompute**

**GPU results (warm ≈ sub-second; first EOD ~24–34s is load/context)**

| Tag | Med tok/s | Warm checker | Quiet exact | JSON | Call |
|-----|-----------|--------------|-------------|------|------|
| `cromwell-qwen3:8b` | ~145 | 0.52s | yes | yes | **keep ops primary** |
| `cromwell-qwen2.5:3b` | ~262 | 0.20s | yes | yes | **light pin** (faster; weaker long triage) |
| `qwen3.5:9b` | ~105 | 1.18s | yes | yes | **lab default** |
| `qwen3:14b` | ~81 | 1.58s | yes | yes | optional lab; ~10 GB; do not displace 8b |
| `llama3.1:8b` | ~148 | 0.43s | **no** | yes | **not ops** |

**Timeouts vs GPU reality:** 600s / 900s / concurrent=1 were CPU-era. Warm 8b turns are **&lt;1s**; keep the long timeouts for cold load + 180s MCP. Do **not** raise `OLLAMA_NUM_PARALLEL` in the same breath as CUDA — still one nanobot lock, and `dream` already occupies it for ~1 min / 2h.

**Eval conclusion:** no live model change. Next product work is STATE / triage / checker skills on the **current** 8b, not a bigger tag.

---

## Close-out checklist

- [x] Inventory table filled (including `dream`, watchdog, DAR, Open WebUI, absent Rails `LlmClient`)
- [x] Primary + fallback documented in `ai/MODEL_PIN.md`
- [x] Health/DNS verified from `data_manager_sidekiq` → mcp / ollama / nanobot
- [x] GPU latency/quality outline (bakeoff numbers)
- [x] Compose comments no longer say “CPU Ollama” as the concurrent=1 rationale
- [x] Schedule README GPU-aware
- [ ] Dual-route 3b for cron (staff roster) — **not this ticket**
- [ ] Dream catalog + allowlist — existing hygiene ticket
- [ ] CDI cleanup — P3 `2026-09-16-podman-nvidia-cdi-cleanup.md`
