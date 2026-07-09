# Session Report — Cromwell CPU Tuning, Watchdog & Telegram Delivery

**Date:** 2026-07-09  
**Time:** ~13:05–14:10 MDT  
**Duration:** ~1h 5m  
**Project:** Sawtooth ecosystem + data_manager + AI runtime (`ai/`, root `compose.yml`)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main`; `data_manager` `main`  
**Model:** Grok  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Diagnose Telegram `Error calling LLM: timed out after 300s`; verify Ollama/CPU optimality; implement CPU-only tuning, ops note (backtest vs cron), and Sidekiq health watchdog (defer tracking AI runtime in git).

**Outcome:** Partially delivered (infra/tuning/watchdog landed; Telegram client visibility still open for operator confirmation)

**One-line summary:** Confirmed sawtooth-ai is correctly CPU-only (no discrete GPU); switched Cromwell to a snappier 3b model + 8k ctx + 24h keep-alive; shipped DM Sidekiq ecosystem health watchdog with Telegram alerts; serialized nanobot concurrency to stop Ollama stampede.

---

## 2. Work Completed

- Hardware diagnosis: System76 Thelio Mira, Ryzen 9 9900X, ~92 GiB RAM, **no discrete GPU**; only AMD Raphael iGPU (2 GiB) — pure-CPU Ollama is correct, not a misconfiguration
- CPU-only LLM path: model `cromwell-qwen2.5:3b`, `num_ctx` 8192, `num_predict` 512, `OLLAMA_KEEP_ALIVE=24h`, flash attention, parallel=1
- Filed/updated tickets for timeout, CPU tuning, watchdog
- Ops note: avoid heavy WUT backtests at top-of-hour MT during snapshot window
- DM `EcosystemHealthCheckJob` + service + specs + Sidekiq schedule + watchdog env template
- Nanobot `gateway.host: 0.0.0.0` for compose-network `/health`; `NANOBOT_MAX_CONCURRENT_REQUESTS=1`
- Diagnosed Telegram DM “no reply”: inbound + Bot API outbound OK; concurrent agent turns starved Ollama (2m 500s); agent did generate some replies with 70s+ latency

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md` | added | CPU-only checklist ticket |
| `ecosystem/docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md` | modified | points at CPU tuning mitigations |
| `ecosystem/docs/tickets/2026-07-04-sidekiq-ecosystem-health-watchdog.md` | modified | marked largely Done |
| `ecosystem/ai/schedule/README.md` | modified | backtest/cron CPU ops note + health schedule |
| `ecosystem/ai/schedule/sidekiq.yaml` | modified | ecosystem_health hourly/daily |
| `ecosystem/ai/schedule/manifest.yaml` | modified | health tasks catalog |
| `ecosystem/ai/skills/winston-ecosystem-status/SKILL.md` | modified | watchdog owns authoritative infra alerts |
| `ecosystem/deployment/README.md` | modified | watchdog + CPU-only runbook |
| `ecosystem/deployment/watchdog-env-template.txt` | added | Telegram secrets template |
| `data_manager/app/services/ecosystem_health_check_service.rb` | added | HTTP probes + Telegram Bot API |
| `data_manager/app/jobs/ecosystem_health_check_job.rb` | added | Sidekiq entry |
| `data_manager/config/sidekiq_schedule.yml` | modified | hourly :10 + daily 6:05 MT |
| `data_manager/spec/services/ecosystem_health_check_service_spec.rb` | added | 5 examples, pass |
| `compose.yml` (workspace root, **not in git**) | modified | ollama keep-alive/FA; sidekiq env; nanobot concurrency |
| `ai/data/cromwell-bot/config.json` (local secrets runtime) | modified | model 3b, host 0.0.0.0 |
| `ai/configs/nanobot-cromwell.example.json` | modified | CPU defaults |
| `ai/ollama/Modelfile.cromwell-cpu` | added | cromwell-qwen2.5:3b tag |
| `ai/README.md` | modified | CPU model docs |

### Commits

- _Pending this wrap_

### Branch / PR state at sign-off

- `ecosystem` `main` — dirty → commit in wrap  
- `data_manager` `main` — dirty → commit in wrap  
- Workspace `compose.yml` / `ai/*` — **not in any monolith git** (see deferred track-ai-runtime ticket)  
- Pushed: pending wrap  
- PR: not opened (direct main workflow)

---

## 4. Decisions Made

### Decision 1: CPU-only is correct on sawtooth-ai
- **Choice:** Do not mount GPU devices / ROCm for current models  
- **Why:** No discrete GPU; iGPU 2 GiB cannot hold 3–4B Q4 + KV  
- **Alternatives considered:** Vulkan/ROCm iGPU (rejected)  
- **Reversibility:** easy when discrete GPU installed  
- **Promote to ADR?** no — operational fact; document in deployment README  

### Decision 2: Primary model = `cromwell-qwen2.5:3b` @ 8k ctx
- **Choice:** Prefer non-thinking tool-capable 3b over qwen3.5:4b thinking / 16k  
- **Why:** Tool-call smoke ~1.5s; prior path hit 300s timeouts  
- **Alternatives considered:** 8b quality model (slower on CPU); raise timeouts only  
- **Reversibility:** easy (config + Modelfile)  
- **Promote to ADR?** no  

### Decision 3: Independent DM Sidekiq watchdog
- **Choice:** `EcosystemHealthCheckJob` posts Telegram without Cromwell/LLM  
- **Why:** Silent AI-layer death was the original ops failure mode  
- **Alternatives considered:** External SaaS monitoring  
- **Reversibility:** easy  
- **Promote to ADR?** no  

### Decision 4: Serialize nanobot agent turns on CPU
- **Choice:** `NANOBOT_MAX_CONCURRENT_REQUESTS=1`  
- **Why:** Concurrent cron+DM → Ollama 2m 500s → no Telegram reply  
- **Alternatives considered:** Raise OLLAMA_NUM_PARALLEL (hurts latency further on CPU)  
- **Reversibility:** easy  
- **Promote to ADR?** no  

---

## 5. Insights Surfaced

- **“No NVIDIA” is incomplete:** there *is* an AMD iGPU + host ROCm install, but neither helps LLM size/latency here.
- **Ollama 500 after exactly 2m0s** is the hard wall for agent turns; nanobot’s 300s is outer retry budget.
- **`Response to telegram:…` does not prove the human saw the message** — still need client confirmation; Bot API `ok: true` confirms Telegram accepted delivery to chat_id.
- **Workspace `compose.yml` + `ai/` are not git-tracked** at sawtooth root; durable AI config still depends on `2026-07-09-track-ai-runtime-config-in-git`.
- **podman-compose** does not support Compose `env_file: { path, required: false }` dict form — use plain string paths.

---

## 6. Issues & Tickets

### Resolved this session
- Pure-CPU optimality verified (not a GPU passthrough bug)
- Watchdog ticket largely implemented and smoke-tested (daily Telegram 200)
- Cron LLM path mitigated (model/ctx/keep-alive/concurrency)

### Deferred
- **Natural hourly non-error Telegram confirmation** after model change (operator)
- **Telegram client “invisible bot replies”** — if DIAG/🔔 messages not visible, client/account/folder issue; if visible but agent silent, dig nanobot send path further
- **`2026-07-09-track-ai-runtime-config-in-git`** — pick up next (user deferred #2)
- Optional: morning briefing skill polish (watchdog one-liner done); simulated nanobot-down alert
- Discrete GPU purchase (structural ceiling)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Ollama CPU discovery | logs `compute=cpu`, 0 layers GPU | ✅ |
| Model warm `pong` | ~2.5s | ✅ |
| Tool-call completion | ~1.5s `wv2_market_snapshot` | ✅ |
| Watchdog specs | `rspec …ecosystem_health_check_service_spec` | ✅ 5/5 |
| Watchdog daily smoke | `perform_now("daily")` → Telegram 200 | ✅ |
| Nanobot health on compose net | `0.0.0.0:18790/health` | ✅ |
| Bot API DM delivery | `sendMessage` / `sendRichMessage` ok | ✅ |
| Natural agent DM visible to operator | manual Telegram | ⚠️ unconfirmed |
| Natural market-snapshot-hourly non-error | next session hour | ⚠️ pending |

**Test command(s):**

```bash
podman exec -e RAILS_ENV=test data_manager_sidekiq bundle exec rspec \
  spec/services/ecosystem_health_check_service_spec.rb
podman exec -e RAILS_ENV=development data_manager_sidekiq bin/rails runner \
  'pp EcosystemHealthCheckJob.perform_now("daily")'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** none new (HTTParty already in DM)  
- **Services:** recreated `ollama`, `nanobot_cromwell`, `data_manager_sidekiq`; model tag `cromwell-qwen2.5:3b`  
- **Secrets:** `ecosystem/deployment/watchdog.env` (gitignored) created locally  
- **Migrations:** None  

---

## 9. Risks & Technical Debt

- Full agent turns still ~70s on CPU with large tool schemas — interactive feel remains mediocre  
- Concurrent cron+DM without concurrency=1 reintroduces timeouts  
- Untracked `compose.yml` / `ai/` can lose NANOBOT_MAX_CONCURRENT_REQUESTS and model defaults on rebuild  
- Telegram “no visible reply” if operator cannot see DIAG messages → not server-side  

---

## 10. Open Questions

- **Does operator see Bot API DIAG/🔔 messages in `@sawtooth_nanobot` DM?** — needs John; blocks “delivery broken” vs “client UX”  
- **Is next natural hourly snapshot non-error on Sawtooth Main?** — needs clock  

---

## 11. Handoff & Resume Notes

- **Where I left off:** Nanobot recreated with `NANOBOT_MAX_CONCURRENT_REQUESTS=1`; Bot API confirmed delivery; operator still reported not seeing agent replies  
- **Next concrete step:** Confirm visibility of 🔔 DIAG DM; if yes, send short `ping` and wait ≤90s; if no, Telegram client/account triage  
- **Files to read first:**  
  1. This report  
  2. `ecosystem/docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`  
  3. `ecosystem/docs/tickets/2026-07-09-track-ai-runtime-config-in-git.md`  
  4. `data_manager/app/services/ecosystem_health_check_service.rb`  

---

## 12. Stakeholder Communications

- _None required._ Optional: note to self that Sawtooth Main may get hourly health at :10 if degraded, and green daily at 6:05 AM MT.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, record (tickets)  
- **What worked well:** hardware inventory + Ollama logs closed the “is GPU misconfigured?” question fast  
- **Friction points:** podman-compose recreate churn; root `compose.yml` not in git  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Confirm natural `market-snapshot-hourly` non-error content on Sawtooth Main — See: `docs/tickets/2026-07-09-confirm-cromwell-hourly-telegram.md`  
- [ ] Confirm Telegram client sees Bot API DIAG messages + agent `ping` reply — See: `docs/tickets/2026-07-09-telegram-agent-reply-visibility.md`  
- [ ] Execute `docs/tickets/2026-07-09-track-ai-runtime-config-in-git.md` (compose + example + Containerfile into versioned tree)  
- [ ] Optional: discrete GPU for Thelio empty PCIe slots — See: `docs/tickets/2026-07-09-thelio-discrete-gpu-for-ollama.md`  

---

## 15. Appendix (optional)

- Ollama: `POST /v1/chat/completions` → 500 after **2m0s** under concurrent load  
- Tool smoke (single tool schema): `elapsed_s=1.5`, tool_calls `wv2_market_snapshot`  
- Model after change: `cromwell-qwen2.5:3b` 100% CPU, ctx 8192, keep-alive 24h  
- PCI: only VGA `1002:13c0` Raphael; slots `0` / `0-1` empty (`adapter: 0`)  
