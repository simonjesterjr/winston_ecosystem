# Session Report — Cromwell Cron Telegram Fix

**Date:** 2026-07-09
**Time:** ~07:15–07:36 MDT
**Duration:** ~20m
**Project:** Sawtooth ecosystem + Cromwell nanobot runtime
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` (ecosystem)
**Model:** Grok
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Investigate why nothing was sent from Telegram yesterday; determine why scheduled tasks appear not to be running.

**Outcome:** Delivered (root cause fixed; residual LLM timeout risk remains)

**One-line summary:** Cromwell Telegram silence was nanobot 0.2.x rejecting unbound legacy cron payloads (and SSRF-blocking MCP); schedules converted to session-bound `agent_turn` + private-net whitelist; backend Sidekiq was fine.

---

## 2. Work Completed

- Confirmed core stack and AI profile containers were up (including `nanobot_cromwell`)
- Differentiated **Sidekiq backend** (worked) vs **Cromwell Telegram delivery** (skipped)
- Traced all five broadcast jobs to `lastStatus: skipped` with  
  `unbound agent cron job must be recreated from a chat session`
- Read nanobot 0.2.2 cron path (`on_cron_job` → `is_bound_cron_job` / special `dream`|`heartbeat` only)
- Fixed second failure: MCP `winston` blocked as private URL without `tools.ssrf_whitelist`
- Converted `ecosystem/ai/schedule/cromwell-cron.json` to session-bound format for Sawtooth Main
- Updated runtime `ai/data/cromwell-bot/config.json` + example config with SSRF CIDRs
- Documented binding + SSRF requirements in `ecosystem/ai/schedule/README.md`
- Reseeded workspace cron (`bin/seed-cromwell-workspace`), restarted `nanobot_cromwell`
- Smoke: bound job entered agent loop (no longer skipped); LLM later timed out on 4b CPU
- Restored normal cron schedules after temporary every-15s smoke experiment
- Pinned `nanobot-ai==0.2.2` in `ai/nanobot/Containerfile` (workspace, not git-tracked)

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/ai/schedule/cromwell-cron.json` | modified | `system_event`+`deliver` → bound `agent_turn` + session/origin fields |
| `ecosystem/ai/schedule/README.md` | modified | Nanobot 0.2.x binding + SSRF whitelist runbook |
| `ai/data/cromwell-bot/config.json` | modified | `tools.ssrf_whitelist` (runtime; **has secrets; not in git**) |
| `ai/configs/nanobot-cromwell.example.json` | modified | SSRF whitelist + note (workspace path; **not in ecosystem git**) |
| `ai/nanobot/Containerfile` | modified | Pin `nanobot-ai==0.2.2` (workspace path; **not in ecosystem git**) |
| `ecosystem/docs/session-reports/2026-07-09-0736-cromwell-cron-telegram-fix.md` | added | This report |

### Commits

- _Pending `/wrap` commit in `ecosystem/`_

### Branch / PR state at sign-off

- Branch: `ecosystem` `main` — dirty (this session’s schedule/docs only for commit)
- Pushed: no (at report time)
- PR: not opened (direct main workflow)

---

## 4. Decisions Made

### Decision 1: Convert Cromwell broadcast jobs to session-bound `agent_turn`
- **Choice:** All five Telegram jobs use `sessionKey: telegram:-1003884714483`, `originChannel: telegram`, `originChatId: -1003884714483`, with `deliver/channel/to` cleared
- **Why:** nanobot 0.2.x only runs bound agent jobs (plus named system jobs `dream`/`heartbeat`); legacy `system_event`+`deliver` is skipped
- **Alternatives considered:** Patch nanobot to re-accept legacy deliver; create jobs from a live Telegram chat session only
- **Reversibility:** easy (template + seed)
- **Promote to ADR?** no — operational constraint of current nanobot version; documented in schedule README

### Decision 2: Whitelist compose private CIDRs for MCP SSRF
- **Choice:** `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` in `tools.ssrf_whitelist`
- **Why:** `winston_mcp` is only reachable on the podman network; without whitelist MCP never connects
- **Alternatives considered:** Public reverse proxy for MCP (overkill for local stack)
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Pin nanobot-ai image install
- **Choice:** `pip install nanobot-ai==0.2.2` in Containerfile
- **Why:** Unpinned install is what pulled breaking 0.2.x behavior; pin makes rebuilds deliberate
- **Alternatives considered:** Leave unpinned and only document payload shape
- **Reversibility:** easy
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- **Backend vs delivery split:** Wv2 Sidekiq and DM cron can succeed while Telegram is completely silent — always check `workspace/cron/jobs.json` `lastStatus` / `lastError` and `podman logs nanobot_cromwell`.
- **`dream` is a red herring:** It runs `ok` every 2h with empty work; healthy dream does **not** imply broadcast crons work.
- **nanobot 0.2.x binding rule:** `is_bound_cron_job` requires `agent_turn` + sessionKey + originChannel + originChatId and **no** legacy deliver fields.
- **Workspace `ai/` is not git-tracked** at sawtooth root (`Containerfile`, example config, live `config.json`). Versioned SoT for cron remains `ecosystem/ai/schedule/`; runtime secrets stay local.
- **LLM path still fragile:** After binding fix, smoke run hit `LLM request timed out` (2m) on `cromwell-qwen3.5:4b` CPU with full tool surface — can still delay/drop Telegram content.

---

## 6. Issues & Tickets

### Resolved this session
- Cromwell Telegram cron silent due to unbound legacy payloads — fixed via session-bound template + seed + restart
- MCP SSRF block for `winston_mcp` — fixed via `ssrf_whitelist`

### Deferred
- **LLM timeout risk on cron turns** — 4b CPU model timed out during smoke; may still affect 8:00/15:35/16:35 posts  
  See: `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`
- **Workspace `ai/` versioning gap** — Containerfile pin + example SSRF change live only on host; not in ecosystem git  
  See: `docs/tickets/2026-07-09-track-ai-runtime-config-in-git.md`
- **WUT Sidekiq noise (observed, out of scope):** `DailyOperationsJob` / `ActiveAccountsBackupJob` failing on missing `active_account_id` columns — unrelated to Telegram silence  
  See: `docs/tickets/2026-07-09-wut-active-account-id-sidekiq-failures.md`
- **Unpinned-to-pinned rebuild not run** — pin is in Containerfile; current running image already is 0.2.2; rebuild optional until next image change
- **Confirm live Telegram at next natural cron** — operational check (left in §14 only; no ticket)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Wv2 Sidekiq yesterday | logs: `DailyAnalysisJob` completed + JSON/PDF written | ✅ |
| DM/Wv2 artifacts | `wv2_20260708.json`, webhook audit `20260708T223017_*` | ✅ |
| Cron skip root cause | `jobs.json` lastError + nanobot logs | ✅ |
| Session-bound template | `is_bound_cron_job` True for all five jobs in container | ✅ |
| MCP after SSRF fix | `MCP server 'winston': connected, 24 capabilities` | ✅ |
| Bound cron executes | `Processing message from telegram:cron` (no unbound skip) | ✅ |
| Live Telegram delivery | Full EOD/snapshot post to group | ⚠️ not confirmed (LLM timeout on smoke) |
| Next schedule times | hourly 08:00, DM 15:35/45, EOD 16:35 MT today | ✅ armed |

**Test command(s):**

```bash
python3 -c 'import json; j=json.load(open("ai/data/cromwell-bot/workspace/cron/jobs.json")); ...'
podman logs nanobot_cromwell --tail 50
podman exec nanobot_cromwell python3 -c 'from nanobot.cron.session_turns import is_bound_cron_job; ...'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** Running image `nanobot-ai` 0.2.2; Containerfile pin added for rebuilds
- **Services:** Core stack + `--profile ai` already up; multiple `nanobot_cromwell` restarts this session
- **Migrations:** None
- **Secrets:** Live Telegram bot token present in `ai/data/cromwell-bot/config.json` — **do not commit**

---

## 9. Risks & Technical Debt

- Cron success still depends on LLM latency/timeouts; binding fix alone does not guarantee a Telegram message lands
- Runtime `ai/` (Containerfile, example config) unversioned — easy to lose host-only fixes
- Agent can theoretically delete bound `agent_turn` jobs (no longer protected `system_event`); seed template is recovery path
- `bin/seed-cromwell-workspace --force-cron` flag exists but merge path always takes template definitions (flag is misleading)

---

## 10. Open Questions

- **Should Cromwell cron use a larger/faster model for scheduled posts?** — needs answer from: operator preference + latency budget; blocks: reliable Telegram under CPU load
- **Should workspace `ai/nanobot` + `ai/configs` move into a tracked repo?** — needs answer from: workspace layout preference; blocks: durable Containerfile/example changes

---

## 11. Handoff & Resume Notes

- **Where I left off:** Fixes live; nanobot restarted with bound jobs + MCP connected; normal schedules restored; awaiting natural 08:00 MT hourly for live Telegram proof
- **Next concrete step:** Watch `podman logs -f nanobot_cromwell` around 08:00 MT; confirm Sawtooth Main gets market-snapshot-hourly; if LLM timeout, bump model or timeout
- **Files to read first:**
  1. `ecosystem/ai/schedule/README.md` (§ Nanobot 0.2.x session binding, § MCP SSRF)
  2. `ecosystem/ai/schedule/cromwell-cron.json`
  3. `ai/data/cromwell-bot/workspace/cron/jobs.json` (runtime state)
  4. `ai/data/cromwell-bot/config.json` (SSRF whitelist; secrets)

---

## 12. Stakeholder Communications

- Optional: one-line to team — “Telegram daily posts were blocked by a bot scheduler upgrade; fixed; backend analysis still ran.”

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report (this)
- **What worked well:** Differentiating Sidekiq artifacts vs nanobot cron state immediately narrowed the problem; container source inspection of nanobot package was definitive
- **Friction points:** Workspace `ai/` not in git; smoke schedule recompute on restart overwrites forced `nextRunAtMs`; default shell tool timeouts during long waits
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] Confirm live Telegram at next natural cron (08:00 hourly, then 15:35 DM, 16:35 EOD) — owner: operator — due: today
- [ ] If LLM timeouts continue: raise model / timeout — See: `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`
- [ ] Track AI Containerfile + example config in git — See: `docs/tickets/2026-07-09-track-ai-runtime-config-in-git.md`
- [ ] Fix WUT `active_account_id` Sidekiq failures — See: `docs/tickets/2026-07-09-wut-active-account-id-sidekiq-failures.md`

---

## 15. Appendix (optional)

### Representative nanobot errors (before fix)

```text
Cron: skipped unbound agent job 'eod-daily-report' (eod-daily-report):
  unbound agent cron job must be recreated from a chat session
MCP server 'winston': blocked unsafe URL http://winston_mcp:8088/sse
  (Blocked: winston_mcp resolves to private/internal address 10.89.0.75)
```

### After fix (startup)

```text
MCP server 'winston': connected, 24 capabilities registered
Cron service started with 6 jobs
```

### Bound payload shape (Sawtooth Main)

```json
{
  "kind": "agent_turn",
  "sessionKey": "telegram:-1003884714483",
  "originChannel": "telegram",
  "originChatId": "-1003884714483",
  "deliver": false,
  "channel": null,
  "to": null
}
```

### Smoke residual

```text
LLM transient error (attempt 1/3), retrying in 1s: error calling llm: request timed out.
POST /v1/chat/completions → 500 after 2m0s (ollama)
```
