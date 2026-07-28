# Session Report — winston_mcp MCP SDK pin (health DEGRADED)

**Date:** 2026-07-28
**Time:** ~14:05–15:44 MDT
**Duration:** ~1h 40m
**Project:** sawtooth / winston_ecosystem
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `main` (ecosystem repo)
**Model:** Grok 4.5
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Investigate Telegram alert: Ecosystem health DEGRADED — `winston_mcp` connection refused on port 8088.

**Outcome:** Delivered

**One-line summary:** `winston_mcp` was crash-looping after pip installed MCP Python SDK 2.0 (breaking `list_tools`/`call_tool`); pinned `mcp>=1.26,<2`, rebuilt, and restored healthy `/health`.

---

## 2. Work Completed

- Diagnosed Telegram watchdog message as `EcosystemHealthCheckService` probe failure on `http://winston_mcp:8088/health`.
- Confirmed `winston_mcp` container crash-looping (sub-second restarts, exit 0).
- Captured import-time failure under uvicorn:
  - `AttributeError: 'Server' object has no attribute 'list_tools'`
- Root-caused to MCP Python SDK **2.0.0** installed under unbounded `mcp>=1.26.0`.
- Pinned dependency to v1 line and rebuilt image to **mcp 1.29.0**.
- Redeployed AI MCP service; verified health from container and from `data_manager_sidekiq` network.

---

## 3. Code Delivered

### Files changed

| File | Change | Notes |
|------|--------|-------|
| `ecosystem/ai/mcp/pyproject.toml` | modified | `mcp>=1.26.0,<2` + comment |
| `ecosystem/ai/mcp/Containerfile` | modified | fallback pip pin `mcp>=1.26,<2` |
| `ecosystem/docs/session-reports/2026-07-28-1544-winston-mcp-mcp-sdk-pin.md` | added | this report |

### Commits

- `e343ec7` — fix(ops): pin mcp SDK to 1.x for winston_mcp health 

### Branch / PR state at sign-off

- Branch: `main` (ecosystem)
- Pushed: yes (this wrap)
- PR: not opened (direct main)

---

## 4. Decisions Made

### Decision 1: Pin mcp 1.x rather than migrate to SDK 2.0
- **Choice:** Upper-bound `mcp<2` and keep low-level `Server` + SSE transport as-is.
- **Why:** Immediate ops recovery; SDK 2.0 rewrote Server API (no `list_tools`/`call_tool` decorators). Official guidance still documents v1 for production until intentional migration.
- **Alternatives considered:** Migrate to MCPServer / FastMCP-style API in 2.x (larger rewrite, not needed for outage recovery).
- **Reversibility:** easy (drop upper bound after migration).
- **Promote to ADR?** no — operational pin; migration can be a ticket later.

---

## 5. Insights Surfaced

- Unbounded `mcp>=1.26` is unsafe: MCP SDK 2.0 stable can land and break import on next rebuild.
- Containerfile fallback `pip install "mcp>=1.26"` had the same footgun when editable install fails.
- `./bin/compose ... up --force-recreate winston_mcp` cascaded stops across dependent monoliths under podman-compose; safer path is remove AI pair then `up -d --no-deps` or targeted `podman` recreate.
- `podman logs` can hang/appear empty during hard crash loops; one-shot `podman run --rm` surfaces the traceback cleanly.
- Watchdog recovery hints mention nanobot/ollama more than `winston_mcp` logs — still useful but incomplete for this failure mode.

---

## 6. Issues & Tickets

### Resolved this session
- Live DEGRADED alert for `winston_mcp` connection refused (crash loop from mcp 2.0 API break).

### Deferred
- Optional: migrate `mcp_winston` to MCP SDK 2.x / new server surface (no ticket filed this session).
- Optional: tighten ecosystem health recovery hints to include `winston_mcp` logs/rebuild.
- Unrelated dirty tree left uncommitted (pre-existing tickets / session report) — not this session’s work.

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| Image rebuild | `./bin/compose --profile ai build winston_mcp` | ✅ mcp-1.29.0 installed |
| Process stability | container up ~minutes, not sub-second restart | ✅ |
| Local health | `curl http://127.0.0.1:8088/health` inside container | ✅ 200 ok |
| Cross-network health | probe from `data_manager_sidekiq` → `winston_mcp:8088/health` | ✅ 200 ok |
| Nanobot MCP client | logs show GET `/sse` 200 + POST `/messages` 202 | ✅ |
| Stack peers | DM/WUT/Wv2/ollama + nanobot `/health` | ✅ |

**Test command(s):**

```bash
podman exec winston_mcp python -c "import importlib.metadata as m; print(m.version('mcp'))"
podman exec winston_mcp curl -sS http://127.0.0.1:8088/health
podman exec data_manager_sidekiq bash -c 'ruby -rnet/http -e "u=URI(\"http://winston_mcp:8088/health\"); r=Net::HTTP.get_response(u); puts \"#{r.code} #{r.body}\""'
```

---

## 8. Environment, Dependencies, Data

- **Dependencies:** `mcp` pinned to `>=1.26.0,<2` (resolved **1.29.0** in image)
- **Services:** rebuilt/recreated `winston_mcp`; stack briefly bounced during compose recreate recovery; all core + AI services running at sign-off
- **Migrations:** None

---

## 9. Risks & Technical Debt

- Still on MCP SDK v1; will need a deliberate migration when 2.x becomes required.
- Compose recreate dependency cascade under podman is operationally sharp — prefer `--no-deps` for single-service image swaps.
- Pre-existing uncommitted ticket/docs noise in ecosystem repo remains on disk (not staged).

---

## 10. Open Questions

- **When to migrate to mcp 2.x?** — needs product/engineering slot; blocks long-term dependency currency only.
- **Should health recovery Telegram text mention `winston_mcp` rebuild/logs?** — minor UX; not blocking.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Health restored; pin committed/pushed via `/wrap`.
- **Next concrete step:** Optional ticket to migrate `mcp_winston` off low-level v1 Server API; or leave pin until forced.
- **Files to read first:**
  1. `ecosystem/ai/mcp/pyproject.toml`
  2. `ecosystem/ai/mcp/mcp_winston/server.py` (`@server.list_tools` / `@server.call_tool`)
  3. `data_manager/app/services/ecosystem_health_check_service.rb`

---

## 12. Stakeholder Communications

- Operator already saw the Telegram DEGRADED alert; next successful hourly probe should not re-alert for this check (hourly OK messages are suppressed by design).

---

## 13. Tools & Workflow Notes

- **Skills used:** `operator-prose`, `session-report`, `wrap`
- **What worked well:** one-shot container run to capture crash traceback; network probe from Sidekiq container matching the watchdog path
- **Friction points:** `podman logs` hang during crash loop; compose `--force-recreate` stopped/recreated more of the stack than intended
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] Consider ticket: migrate `mcp_winston` to MCP Python SDK 2.x — owner: engineering — due: backlog
- [ ] Optional: improve DEGRADED recovery hints for `winston_mcp` — owner: ops — due: whenever convenient

---

## 15. Appendix (optional)

### Crash signature (pre-fix)

```text
File "/app/mcp_winston/server.py", line 103, in <module>
    @server.list_tools()
AttributeError: 'Server' object has no attribute 'list_tools'
```

### Working image dependency

```text
Successfully installed ... mcp-1.29.0 mcp-winston-0.3.0 ...
```
