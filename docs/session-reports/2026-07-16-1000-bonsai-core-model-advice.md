# Session Report — Bonsai 27B / Cromwell Core Model Advice

**Date:** 2026-07-16  
**Time:** ~09:45–10:00 MDT  
**Duration:** ~15m  
**Project:** sawtooth / Winston ecosystem (Cromwell + local Ollama)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` repo `main` (docs-only)  
**Model:** Grok (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** Assess PrismML Bonsai 27B (and optionally 8B) as an upgrade to Cromwell’s core local model for trend-following / managing AI; advise on whether to adopt it; wrap with follow-on tickets and a watch for Ollama availability.

**Outcome:** Delivered (decision + backlog; no production model swap)

**One-line summary:** Keep `cromwell-qwen3:8b` as core on CPU-only sawtooth-ai; treat Bonsai as lab/eval first (8B A/B, 27B only after Ollama/runtime fit); dual-runtime and CPU reliability still outrank a bigger base model.

---

## 2. Work Completed

- Reviewed live Cromwell config and host constraints: `ai/data/cromwell-bot/config.json` → `cromwell-qwen3:8b`; Ollama lists 3b/4b/8b/9b tags; **no discrete GPU** (9900X, ~91 GiB RAM).
- Grounded advice in existing CPU/timeout debt: cron vs interactive contention, think-token burn, hallucination tickets, dual-runtime / thin-cron backlog.
- Prior chat context: Bonsai 27B (ternary ~5.9 GB / 1-bit ~3.9 GB) is exciting for agentic quality but **not Ollama-mainline ready** (Prism llama.cpp fork / custom ternary).
- Recommendation locked:
  - **Do not** promote Bonsai 27B to production core yet.
  - **Prefer** Bonsai 8B (if Ollama-runnable) for A/B vs current 8B.
  - **Architecture over single bigger model:** small cron + reliable interactive + optional GPU/API for heavy reasoning.
- Filed follow-on tickets (see §6) and scheduled a periodic Ollama availability check for Bonsai 27B.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/docs/session-reports/2026-07-16-1000-bonsai-core-model-advice.md` | added | This report |
| `ecosystem/docs/tickets/2026-07-16-bonsai-ollama-availability-watch.md` | added | Watch + promote when Ollama-ready |
| `ecosystem/docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md` | added | Side-by-side 8B eval harness |
| `ecosystem/docs/tickets/2026-07-16-bonsai-27b-lab-eval-when-runnable.md` | added | 27B lab path after runtime exists |
| `ecosystem/docs/tickets/2026-07-16-cromwell-core-model-promotion-policy.md` | added | Guardrails before swapping default model |

### Commits

- _Pending wrap commit on this session’s docs only._

### Branch / PR state at sign-off

- Branch: `ecosystem` `main`
- Pushed: pending wrap
- PR: not opened (direct main docs push per prior ecosystem habit)

**Note:** Pre-existing dirty tree on `ecosystem/` (skills, journal-ledger tickets, interfaces, etc.) is **out of scope** for this session and must not be included in the wrap commit.

---

## 4. Decisions Made

### Decision 1: Do not swap Cromwell core to Bonsai 27B yet
- **Choice:** Keep production default `cromwell-qwen3:8b` (Ollama OpenAI-compat).
- **Why:** Host is CPU-only; failures are latency/timeouts/contention more than “need 27B class”; ternary path is not mainline Ollama; MCP tool reliability is the real gate.
- **Alternatives considered:** Immediate 27B core; API-only interactive; wait forever.
- **Reversibility:** easy (never swapped)
- **Promote to ADR?** no — ticket policy is enough until first successful promote

### Decision 2: Bonsai 8B first for local A/B; 27B is lab-only until Ollama/runtime + latency pass
- **Choice:** Eval order: (1) Ollama availability watch, (2) 8B A/B vs current 8B, (3) 27B lab when runnable.
- **Why:** Matches size class of current core; lower ops risk; reuses existing Modelfile/config patterns.
- **Alternatives considered:** Jump straight to ternary 27B via Prism fork as interactive primary.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Core upgrade = dual-model architecture, not one bigger tag
- **Choice:** Cron stays small/fast (3B or thin template); interactive may grow quality when measured; heavy reasoning may be remote/GPU later.
- **Why:** Aligns with tickets already open (thin cron, dual runtime, CPU reliability, GPU).
- **Alternatives considered:** Single 27B owns all cron + chat.
- **Reversibility:** easy while still design
- **Promote to ADR?** optional later with dual-runtime decision

---

## 5. Insights Surfaced

- Live Ollama inventory (2026-07-16): `cromwell-qwen2.5:3b`, `cromwell-qwen3.5:4b`, `cromwell-qwen3:8b`, plus base `qwen3:8b`, `qwen3.5:9b`, `qwen3.5:4b`, `qwen2.5:3b`, `llama3.1:8b` — **no Bonsai tags**.
- `ai/README.md` already documents 7–8B as the practical sweet spot for tool reliability on this agent; 3B is latency path.
- Community Ollama has smaller Ternary Bonsai (e.g. unofficial 8B/4B/1.7B); 27B still tied to custom low-bit runners as of this session.
- Existing model roadmap (LoRA/QLoRA, specialization plan) is complementary: Bonsai is a **base model** candidate; LoRA remains **operator-fit adapter** after gold traces.

---

## 6. Issues & Tickets

### Resolved this session
- _None (advisory session)._

### Deferred / filed
- Ollama availability watch for Bonsai 27B → `docs/tickets/2026-07-16-bonsai-ollama-availability-watch.md`
- Bonsai 8B Cromwell A/B eval → `docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md`
- Bonsai 27B lab eval when runnable → `docs/tickets/2026-07-16-bonsai-27b-lab-eval-when-runnable.md`
- Core model promotion policy → `docs/tickets/2026-07-16-cromwell-core-model-promotion-policy.md`
- Related open (not re-filed): dual runtime, thin cron, CPU reliability, discrete GPU, QLoRA A/B

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Current nanobot model | Read `ai/data/cromwell-bot/config.json` | ✅ `cromwell-qwen3:8b` |
| Ollama inventory | `compose --profile ai exec ollama ollama list` | ✅ no Bonsai |
| Host GPU | `nvidia-smi` / PCI | ✅ none (AMD iGPU only) |
| Bonsai 27B Ollama tag | Prior search + web context | ⚠️ not available mainline as of session |

**Test command(s):** `./bin/compose --profile ai exec ollama ollama list`

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None added  
- **Services:** Ollama queried (already up under `ai` profile)  
- **Migrations:** None  

---

## 9. Risks & Technical Debt

- Promoting any heavier model without dual runtime risks worse Telegram timeouts during hourly snapshots.
- Extreme quant quality on public benches may not transfer to **schema-strict Winston MCP** (nulls, `reply_text`, fail-closed).
- Scheduled Ollama watch is session/durable tooling with finite recurrence horizon — re-arm if watch expires before availability.

---

## 10. Open Questions

- **Will mainline Ollama/llama.cpp gain ternary Bonsai 27B without a fork?** — needs market/community answer; watch ticket.
- **Can Bonsai 8B beat `qwen3:8b` on tool-call accuracy on CPU at similar latency?** — A/B ticket.
- **GPU timeline for Thelio / Ollama host?** — existing GPU ticket.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Advice delivered; tickets + session report + scheduled watch.
- **Next concrete step:** When watch fires “Ollama ready,” run 8B A/B first if available, else 27B lab path; do not flip default model without promotion policy checklist.
- **Files to read first:**
  1. This session report  
  2. `docs/tickets/2026-07-16-bonsai-ollama-availability-watch.md`  
  3. `docs/tickets/2026-07-16-bonsai-8b-cromwell-ab-eval.md`  
  4. `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md`  
  5. `ai/README.md` (model choice section)  

---

## 12. Stakeholder Communications

- _None required beyond operator (this wrap)._

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report, record (tickets), scheduler  
- **What worked well:** Verifying live model list + config before recommending upgrade.  
- **Friction points:** Prior dirty `ecosystem/` tree from other sessions — wrap must stage only this session’s files.  
- **Subagent usage:** none  

---

## 14. Follow-up Actions

- [ ] Commit + push this report and four tickets (wrap)  
- [ ] Confirm scheduled Bonsai 27B Ollama check is registered  
- [ ] When available: execute 8B A/B ticket before any core swap  
- [ ] Do not `git add` unrelated dirty files on `ecosystem/`  

---

## 15. Appendix (optional)

### Relevant live config (redacted)

- Model: `cromwell-qwen3:8b`  
- Provider: OpenAI-compat → `http://ollama:11434/v1`  
- `think: false`, `reasoning_effort: none`, `num_ctx: 8192`, `num_predict: 1024`  

### HF / product references (external)

- Ternary Bonsai 27B GGUF: `https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf`  
- Prism announce: `https://prismml.com/news/bonsai-27b`  
- Unofficial smaller ternary Ollama: community tags (e.g. Ternary Bonsai 8B class) — not 27B core  

### Cross-links

- `docs/tickets/2026-07-15-cromwell-llm-cpu-reliability.md`  
- `docs/tickets/2026-07-15-cromwell-parallel-capacity-dual-runtime.md`  
- `docs/tickets/2026-07-15-cromwell-thin-cron-and-priority.md`  
- `docs/tickets/2026-07-15-winston-model-specialization-plan.md`  
- `docs/tickets/2026-07-09-thelio-discrete-gpu-for-ollama.md`  
