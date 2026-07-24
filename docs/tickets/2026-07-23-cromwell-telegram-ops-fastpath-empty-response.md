# Ticket: Cromwell Telegram ops fast-path (sidestep empty-response hangs)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-23  
**Domain:** Cromwell, Telegram desk, nanobot, Ollama CPU path  
**Monoliths / runtime:** `ai/` (nanobot_cromwell), `winston_mcp`, Ollama host  
**See:** Session investigation 2026-07-23 ~16:18–16:47 UTC;  
[`2026-07-24-1705-dar-telegram-redeploy.md`](../session-reports/2026-07-24-1705-dar-telegram-redeploy.md) (publish-DAR hang + sidestep); related  
[`2026-07-15-cromwell-llm-cpu-reliability.md`](2026-07-15-cromwell-llm-cpu-reliability.md),  
[`2026-07-15-cromwell-thin-cron-and-priority.md`](2026-07-15-cromwell-thin-cron-and-priority.md),  
[`2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md),  
[`2026-07-23-mcp-transfer-activate-flow-smooth.md`](2026-07-23-mcp-transfer-activate-flow-smooth.md),  
[`2026-07-21-cromwell-activate-id-or-name.md`](2026-07-21-cromwell-activate-id-or-name.md),  
[`2026-07-24-dar-telegram-force-republish-runbook.md`](2026-07-24-dar-telegram-force-republish-runbook.md)

## Problem

Operators keep hitting **Telegram silence** on trivial desk commands (e.g. `@sawtooth_nanobot activate 311`) while the **monolith path is fine**.

### Incident (2026-07-23)

| Time (UTC) | Event |
|------------|--------|
| 16:35:25 | User: `activate 311` (Sawtooth Main / mention path) |
| 16:40:31 | nanobot: **Empty response on turn 0** — retry |
| 16:45:41 | **Empty response on turn 1** — attempting finalization |
| — | **No** `wv2_activate_portfolio` tool call ever issued |
| 16:46 | Direct `POST /internal/portfolios/activate` `{id_or_name:"311"}` → **ok / activated** in milliseconds |

Concurrent state:

- `cromwell-qwen3:8b` Ollama runner **100% CPU**, resident multi-day, context 8192  
- Dream job earlier same day also hit empty-response retries (15:40–15:59)  
- `NANOBOT_LLM_TIMEOUT_S=900` — empty retries can burn **tens of minutes** of user-visible hang  
- Cron hourlies and user turns share one agent/Ollama slot; long timeouts amplify starvation  

**Root class:** interactive path depends on a flaky full agent turn (SOUL + tools + history + 8b CPU) **before** any MCP hop. When the model returns empty content, nanobot retries instead of failing fast or taking a deterministic action. Operator experience = “Telegram hung”; actual activate API never ran.

This is **not** fixed by raising LLM timeouts further (that made hangs longer). It needs a **design sidestep**.

## Desired outcome (design)

### A. Deterministic short-circuit for high-frequency desk phrases

For a small grammar of **safe, fully specified** Telegram commands, skip multi-turn LLM tool selection:

| Phrase pattern | Action |
|----------------|--------|
| `activate <id>` / `activate portfolio <id>` | `wv2_activate_portfolio` with `id_or_name` |
| `deactivate <id>` | `wv2_deactivate_portfolio` |
| `list portfolios` / `list actives` | `wv2_list_portfolios` (or active-only filter if exists) |
| `publish the DAR` / `send the DAR` / `daily activity report` (+ optional date) | `wv2_get_daily_activity_report` once (`fetch_only` when date is production EOD already generated); attach PDF / ensure Sawtooth Main delivery |

Rules:

- Only when **id is numeric or unambiguous name** is present in the user message (no resolution theater).  
- Paste tool **`reply_text`** only (existing AGENTS contract).  
- Mutex / 422 → return structured error text; **do not** invent `force` unless user said force.  
- Anything ambiguous falls through to full agent turn.

Implementation candidates (pick one, document):

1. **nanobot pre-router** (regex/skill match before `agent_turn`)  
2. **MCP “desk shell” tool** that parses phrase + dispatches (still one hop, no multi-tool loop)  
3. **Skill-enforced single-tool** with hard max_turns=1 and fail-closed on empty LLM  

Prefer (1) or (2) so empty LLM cannot block activate.

### B. Fail-fast on empty LLM responses (interactive)

- Empty model content on turn 0 of a **user** Telegram session → **one** short retry (≤30s) then operator-visible error:  
  `LLM empty response — try again or use internal activate API / rails task`  
- Do **not** sit in 5+ minute empty retries under 900s timeout for interactive turns.  
- Cron/dream may keep longer budgets if needed, but **must not block** user turns (busy-ack / queue priority).

### C. User priority over dream/cron

- While a user Telegram turn is queued or running, dream and low-value cron must not hold Ollama for multi-minute empty loops.  
- Align with thin-cron ticket: hourlies should be template/tool-light, not full 8b narratives.  
- Optional ops: unload/restart stuck Ollama runner runbook when CPU pegged multi-hour with empty responses.

### D. Operator escape hatch (documented)

When Telegram is silent:

```bash
# Activate without Cromwell
curl -sS -X POST http://localhost:3002/internal/portfolios/activate \
  -H 'Content-Type: application/json' -d '{"id_or_name":"311"}'

# or
bin/compose exec -T winston_v2 bin/rails wv2:portfolios:activate[311]
```

# Re-publish existing DAR PDF without Cromwell / without re-analysis
# (full runbook: docs/tickets/2026-07-24-dar-telegram-force-republish-runbook.md)
bin/compose exec -T winston_v2 bundle exec rails runner '
date = Date.parse("2026-07-24")  # target report date
path = Rails.root.join("storage/cromwell_notifications/wv2_#{date.strftime("%Y%m%d")}.json")
payload = JSON.parse(File.read(path))
puts TelegramReportDelivery.deliver!(payload, date: date).inspect
'

Document in `ecosystem/docs/operations/` once A/B land (or as interim runbook for DAR re-push).

## Acceptance

- [ ] `activate <numeric_id>` from Telegram completes with MCP tool call **or** deterministic router **without** requiring multi-minute LLM success  
- [ ] Empty LLM on interactive turn surfaces an error to Telegram within **≤60s** (not 10+ min silent)  
- [ ] Concurrent dream/empty-response job does not starve a subsequent user activate for >2 min without busy-ack  
- [ ] Design note in ticket or short ADR-ish comment: “desk phrase fast-path vs full agent”  
- [ ] Cross-link ops runbook for manual activate when bot is wedged  
- [ ] Regression: mutex 422 still reported cleanly (no force invention)

## Non-goals

- Replacing nanobot wholesale  
- GPU requirement  
- Auto-activate on transfer  
- Changing Active mutex policy  
- Full natural-language capital activation wizard (separate capital-activation ticket)

## Evidence pointers

- Session JSONL: `ai/data/cromwell-bot/workspace/sessions/telegram_-1003884714483.jsonl` (user activate 311; no tool call after)  
- `podman logs nanobot_cromwell`: Empty response turn 0/1 for `telegram:-1003884714483`  
- `podman exec ollama ollama ps`: `cromwell-qwen3:8b` 100% CPU  
- Manual activate 2026-07-23: OP#311 `Portfolio Mint · 3749c990` → `active=true`, paper, no conflicts  

### Incident (2026-07-24) — publish DAR hang

Same root class; different desk phrase. EOD artifacts + Telegram delivery already OK; interactive “publish” never finished.

| Time (UTC) | Event |
|------------|--------|
| 22:30 | Wv2 EOD DAR PDF delivered to Sawtooth Main (msg **493**) |
| 22:35–22:44 | Cron `eod-daily-report` → `wv2_get_daily_activity_report` fetch_only + claimed success |
| 22:54:32 | User: `@sawtooth_nanobot please publish the DAR for 7/24/2026` |
| 22:59:47 | nanobot: **Empty response on turn 0** for `telegram:-1003884714483` (1/2); retrying — hang |
| ~23:03 | Sidestep: `TelegramReportDelivery.deliver!` in `winston_v2` → msg **496** |

**See:** [`2026-07-24-1705-dar-telegram-redeploy.md`](../session-reports/2026-07-24-1705-dar-telegram-redeploy.md); interim escape hatch ticket [`2026-07-24-dar-telegram-force-republish-runbook.md`](2026-07-24-dar-telegram-force-republish-runbook.md).

**Acceptance add-on:**

- [ ] `publish the DAR [for YYYY-MM-DD]` completes via fast-path or single MCP hop without multi-minute empty-response silence  
