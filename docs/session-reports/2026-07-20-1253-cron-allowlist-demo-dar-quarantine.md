# Session Report — Cron MCP allowlist + demo DAR quarantine

**Date:** 2026-07-20  
**Time:** ~10:31–12:53 MDT (continuation after morning DAR leak wrap)  
**Duration:** ~2h 20m (this segment)  
**Project:** sawtooth Winston ecosystem (cross-monolith)  
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`  
**Branch:** `ecosystem` `main`; `winston_v2` `main` (guards already on main)  
**Model:** Grok 4.5 (xAI)  
**Operator:** johnkoisch  

---

## 1. Goal & Outcome

**Stated goal:** After filing tickets from the historical DAR morning leak wrap, implement **#1 cron MCP tool allowlist** and **#2 quarantine demo DAR artifacts**. Defer **#3 MCP git home**.

**Outcome:** Delivered

**One-line summary:** Hard-blocked off-duty MCP tools on Cromwell cron sessions via nanobot ToolRegistry patch + schedule allowlist; moved demo/historical DAR packages off the live report path.

---

## 2. Work Completed

- Added `ecosystem/ai/schedule/cron-tool-allowlist.json` (per-job MCP allow + EOD `fetch_only` force)
- Documented allowlist in `ecosystem/ai/schedule/README.md`; bumped `ecosystem/ai/VERSION` → 1.4.8
- Seed path: `bin/seed-cromwell-workspace` copies allowlist → `workspace/schedule/`
- Runtime: `ai/nanobot/patches/cron_tool_allowlist.py` + Containerfile install hook on `ToolRegistry`
- Unit tests: 5 passed (`ai/nanobot/patches/test_cron_tool_allowlist.py`)
- Rebuilt and recreated **only** `nanobot_cromwell` (avoided full compose recreate)
- Live smoke: deny `perform_daily_analysis` under `cron:market-snapshot-open`; health OK
- Quarantined demo DARs: 2021-03-17, 2023-10-15, 2025-06-14 → `winston_v2/storage/archive/demo_dars/`
- Marked both tickets **Done**; updated parent issue status

---

## 3. Code Delivered

### Files changed

| File | Change | Repo / home |
|------|--------|-------------|
| `ecosystem/ai/schedule/cron-tool-allowlist.json` | **added** | ecosystem |
| `ecosystem/ai/schedule/README.md` | allowlist section | ecosystem |
| `ecosystem/ai/VERSION` | 1.4.7 → 1.4.8 | ecosystem |
| `ecosystem/docs/tickets/2026-07-20-cromwell-cron-tool-allowlist.md` | Status Done | ecosystem |
| `ecosystem/docs/tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md` | Status Done | ecosystem |
| `ecosystem/docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md` | status banner | ecosystem |
| `ecosystem/docs/session-reports/2026-07-20-1253-cron-allowlist-demo-dar-quarantine.md` | **added** | ecosystem |
| `ai/nanobot/Containerfile` | allowlist patch hook | host (no git) |
| `ai/nanobot/patches/cron_tool_allowlist.py` | **added** | host (no git) |
| `ai/nanobot/patches/test_cron_tool_allowlist.py` | **added** | host (no git) |
| `bin/seed-cromwell-workspace` | seed allowlist | host (no git) |
| `winston_v2/storage/archive/demo_dars/**` | quarantine + README | gitignored storage |

### Commits (prior this wrap)

- `ecosystem` `f426ff9` — feat(cromwell): cron MCP tool allowlist and demo DAR quarantine  
- `ecosystem` `fee781d` — docs: historical DAR morning leak issue, guards contracts, follow-up tickets  
- `winston_v2` `8327e8a` — fix(daily): block historical evaluate and non-production Telegram DARs  

### Branch / PR state at sign-off

- `ecosystem` `main` @ `f426ff9` (+ session report commit pending wrap)
- `winston_v2` `main` @ `8327e8a` (clean for session work)
- Host-only nanobot/seed/MCP still outside git
- PR: not opened (direct main)

---

## 4. Decisions Made

### Decision 1: Enforce allowlist in nanobot, not only MCP
- **Choice:** Patch `ToolRegistry.prepare_call` + `get_definitions` using `current_request_session_key()` when key is `cron:<job-id>`
- **Why:** MCP has no session context; prompt FORBIDDEN already failed; filter definitions so the model does not see off-duty tools
- **Alternatives considered:** Time-of-day deny in MCP; full nanobot fork
- **Reversibility:** easy (image rebuild without patch)
- **Promote to ADR?** no

### Decision 2: Non-MCP builtins stay allowed on cron
- **Choice:** Allowlist only restricts `mcp_*` tools
- **Why:** Skills may use message/read_file; delivery is response content
- **Alternatives considered:** Full tool lockdown per job
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 3: Quarantine only clear demo/historical dates
- **Choice:** Move 2021-03-17, 2023-10-15, 2025-06-14 only; keep all 2026-06+ EODs live
- **Why:** Those three are proven demo/leak dates; early June 2026 are real EOD path
- **Alternatives considered:** Archive everything before 2026-07-09
- **Reversibility:** easy (files still on disk under archive/)
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- nanobot-ai 0.2.2 already exposes `current_request_session_key()` — ideal hook for cron isolation
- `podman-compose up` recreate can cascade-stop the whole stack; prefer `podman build` + replace **one** container for image bumps
- Demo PDFs on the `wv2_reports` bind-mount are agent-visible; quarantine under `storage/archive/` removes them from that mount

---

## 6. Issues & Tickets

### Resolved this session
- [`docs/tickets/2026-07-20-cromwell-cron-tool-allowlist.md`](../tickets/2026-07-20-cromwell-cron-tool-allowlist.md) — **Done**
- [`docs/tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md`](../tickets/2026-07-20-quarantine-historical-demo-dar-artifacts.md) — **Done**
- Parent issue status updated: [`docs/issues/2026-07-20-historical-dar-morning-telegram-leak.md`](../issues/2026-07-20-historical-dar-morning-telegram-leak.md)

### Deferred
- MCP (and ideally nanobot patches + seed script) **git home** — See: [`docs/tickets/2026-07-13-mcp-winston-source-git-home.md`](../tickets/2026-07-13-mcp-winston-source-git-home.md) (operator planned next: ticket #3)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Allowlist unit tests | `pytest ai/nanobot/patches/test_cron_tool_allowlist.py` | ✅ 5 passed |
| Runtime deny | `prepare_call(perform_daily_analysis)` under `cron:market-snapshot-open` | ✅ “not allowed” |
| Nanobot health | `curl http://127.0.0.1:18790/health` | ✅ ok |
| Config seeded | workspace `schedule/cron-tool-allowlist.json` | ✅ present |
| Demo PDF off hot path | container `wv2_reports/wv2_20231015.pdf` | ✅ absent |
| Production PDF remains | `wv2_20260719.pdf` | ✅ present |

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new (still `nanobot-ai==0.2.2`)
- **Services:** `nanobot_cromwell` image rebuilt + container recreated on `sawtooth_default`
- **Migrations:** None
- **Data:** Demo DAR files relocated under gitignored `winston_v2/storage/archive/demo_dars/`

---

## 9. Risks & Technical Debt

- **Host-only** nanobot patch + seed script: not in git (same class as `ai/mcp_winston`) — rebuild from another machine will lose allowlist unless documented/copied
- Unknown `cron:<id>` jobs get **empty** MCP allowlist (fail closed) — must update JSON when adding jobs
- Async historical evaluate still cannot carry Telegram force via thread-local (pre-existing; not this ticket)

---

## 10. Open Questions

- **Should nanobot patches live in ecosystem git or a new ai repo with MCP?** — needs answer from: #3 ticket decision; blocks: portable rebuilds

---

## 11. Handoff & Resume Notes

- **Where I left off:** Tickets 1–2 done and live; wrap of this segment; #3 MCP git home next per operator
- **Next concrete step:** Tackle [`docs/tickets/2026-07-13-mcp-winston-source-git-home.md`](../tickets/2026-07-13-mcp-winston-source-git-home.md) — include nanobot patches + seed if folding into ecosystem
- **Files to read first:**
  1. `ecosystem/ai/schedule/cron-tool-allowlist.json`
  2. `ai/nanobot/patches/cron_tool_allowlist.py`
  3. `ecosystem/ai/schedule/README.md` (allowlist section)
  4. `winston_v2/storage/archive/demo_dars/README.md`

---

## 12. Stakeholder Communications

- Principals: morning historical DARs should no longer appear from market-snapshot cron (tool blocked before evaluate). Real EOD still 4:30–4:35 MT.

---

## 13. Tools & Workflow Notes

- **Skills used:** wrap, session-report
- **What worked well:** Unit-test pure allowlist logic before image rebuild; single-container recreate
- **Friction points:** Full compose recreate earlier in the day; host paths outside git
- **Subagent usage:** None

---

## 14. Follow-up Actions

- [ ] Land MCP + nanobot host sources in a git home — See: [`../tickets/2026-07-13-mcp-winston-source-git-home.md`](../tickets/2026-07-13-mcp-winston-source-git-home.md) — owner: next session — due: planned

---

## 15. Appendix

### Operator contract (cron MCP)

| Session key | Allowed MCP |
|-------------|-------------|
| `cron:market-snapshot-open` / `hourly` | `wv2_market_snapshot` |
| `cron:eod-daily-report` | `wv2_get_daily_activity_report` (`fetch_only` forced) |
| `cron:dm-sync-events` | `dm_get_cromwell_events` |
| `cron:ecosystem-status-daily` | list portfolios, pending, fetch_only report, DM events |

### Rebuild nanobot (allowlist patch changes)

```bash
podman build -f ai/nanobot/Containerfile -t localhost/sawtooth_nanobot_cromwell:latest ai/nanobot
# replace nanobot_cromwell only (do not full compose recreate unless needed)
bin/seed-cromwell-workspace
```
