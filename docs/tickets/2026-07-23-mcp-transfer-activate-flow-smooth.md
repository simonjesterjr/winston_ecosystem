# Ticket: Smooth MCP transfer + activate flow (errors, timeouts, reply contract)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-23  
**Domain:** MCP handoff, Cromwell reply contract, Capital Activation / Active  
**Monoliths:** winston_mcp, winston_unit_test, winston_v2, Cromwell  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md); related [`2026-07-21-cromwell-activate-id-or-name.md`](2026-07-21-cromwell-activate-id-or-name.md), [`2026-07-18-ops-mcp-recreate-after-demo-tools.md`](2026-07-18-ops-mcp-recreate-after-demo-tools.md), [`2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md`](2026-07-23-cromwell-telegram-ops-fastpath-empty-response.md)

## Problem

Operator experience for **WUT PBR → Wv2 transfer → activate** is brittle:

1. **Silent/opaque failures** — `wv2_transfer_portfolio_from_wut` failed in **165ms** with `OneWayDynamicRiskValidator::Error` (missing pyramid_risks), but Cromwell/Telegram often surfaces as a **hang** or generic error (WUT returned HTML exception page, not structured MCP error).  
2. **HTTP hangs under load** — `/internal/portfolio_config?run_id=` can time out when WUT puma is busy with large PBR progress writes (see sibling ticket on results_json).  
3. **No single happy-path playbook** — transfer lands **inactive paper** by design; activate is a second step with Active mutex; agents sometimes chain poorly or wait forever.  
4. **Reply contract gaps** — when transfer fails, `reply_text` / structured `code` may be missing so the agent retries blindly.  
5. **False failure after successful import (2026-07-23 PM)** — see evidence below: Telegram said HTTP 500 while OP was created.

### Evidence — false 500 on run 121 (2026-07-23 ~16:18–16:27 UTC)

| Time (UTC) | Event |
|------------|--------|
| 16:18 | Telegram: `transfer WUT run 121 to Wv2` |
| 16:22 | Tool: `wv2_transfer_portfolio_from_wut` `{run_id: 121}` |
| 16:26 | MCP → session: **`http_error` HTTP 500**, `body_preview` = Rails **HTML** exception page (`Action Controller: Exception caught`), corr=`8142d673-…` |
| 16:26 | Cromwell replied with generic “server-side issue / retry” narrative (not `reply_text` contract) |
| 16:27 | **OP#311** `Portfolio Mint · 3749c990` **created** (`export_kind=trade_ready`, fingerprint `3749c990…`, `wut_backtest_run_id` lineage = 121, cash_events=1) |

Later same day: WUT `GET /internal/portfolio_config?run_id=121` returns full valid JSON (ladder + markets present). So either:

- Import **committed** then a post-commit step raised (response still 500), or  
- A concurrent/retry path created the OP while the tool call that Telegram saw failed on HTML error parsing, or  
- Exception path after successful create without structured JSON.

**Operator impact:** human believes transfer failed; portfolio exists inactive; next message is `activate 311` which then hits empty-LLM hang (sibling fastpath ticket). **P1:** never report failure when OP id was allocated; never return HTML to MCP.

**Debug anchors:** session `telegram_-1003884714483.jsonl`; MCP log `wv2_transfer_portfolio_from_wut error in 165ms corr=8142d673`; Wv2 `create_portfolio` → `PortfolioConfigImporter`.

## Desired outcome

### A. Structured errors end-to-end

- WUT `InternalController#portfolio_config` rescues `OneWayDynamicRiskValidator::Error` (and export failures) → **JSON** `{ status: "error", code: "missing_pyramid_risks", message: "..." }` not HTML 500.  
- MCP maps known codes to operator-readable `reply_text` (and never hangs waiting for HTML).  
- Timeout budget: transfer tool returns error before Cromwell LLM idle-timeout.

### B. Transfer reliability

- Ensure factory/runner always seed/preserve ladder for one_way_dynamic (partially fixed 2026-07-23; verify + regression test).  
- Optional: MCP preflight “can_export?” that only checks ladder + markets without full capture.  
- Document max wall time; if WUT slow, fail with `code: timeout` + retry guidance.

### C. Activate path

- After successful transfer, MCP `reply_text` includes **numeric OP id** and one line: “inactive paper — activate with id N when ready”.  
- Cromwell skill / AGENTS: **do not auto-activate** unless user asked; but **do not hang** waiting for activate.  
- Align with existing activate `id_or_name` tickets.

### D. Smoke script

- Host script: export run_id → import → list → optional activate (compose).  
- Used by humans when MCP path is flaky (already informal via rails rake).

## Acceptance

- [ ] Transfer of one_way_dynamic PBR without ladder returns **structured JSON error** via MCP in &lt;5s with clear message  
- [ ] Transfer of PBR 121-class (ladder present) succeeds via MCP; `reply_text` has `action` + `#id`  
- [ ] **No HTML exception pages** on WUT `portfolio_config` or Wv2 `create_portfolio` for known importer/validator failures — always JSON `{status,code,message}`  
- [ ] If an OP row is committed, MCP returns **success** (or `action: forked/created` + id) — never a bare 500 that implies “nothing happened”  
- [ ] Under moderate WUT load, transfer either succeeds or returns timeout code (no infinite agent wait)  
- [ ] Documented two-step flow: transfer (inactive) → activate (explicit)  
- [ ] Optional smoke script under `portfolio_configs/` or `ecosystem/tmp` promoted if useful  
- [ ] Reproduce or classify the 2026-07-23 run-121 false-500 (logs + importer path) and lock with a regression if root cause is code

## Non-goals

- Auto-activate on every transfer  
- Changing Active mutex policy  
- Real capital activation (separate ticket)  
