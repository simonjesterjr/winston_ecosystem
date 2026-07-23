# Ticket: Smooth MCP transfer + activate flow (errors, timeouts, reply contract)

**Status:** Proposed  
**Priority:** P1  
**Date:** 2026-07-23  
**Domain:** MCP handoff, Cromwell reply contract, Capital Activation / Active  
**Monoliths:** winston_mcp, winston_unit_test, winston_v2, Cromwell  
**See:** [session report](../session-reports/2026-07-23-1038-mint-yellow-exclusive-pbr-dm-transfer.md); related [`2026-07-21-cromwell-activate-id-or-name.md`](2026-07-21-cromwell-activate-id-or-name.md), [`2026-07-18-ops-mcp-recreate-after-demo-tools.md`](2026-07-18-ops-mcp-recreate-after-demo-tools.md)

## Problem

Operator experience for **WUT PBR → Wv2 transfer → activate** is brittle:

1. **Silent/opaque failures** — `wv2_transfer_portfolio_from_wut` failed in **165ms** with `OneWayDynamicRiskValidator::Error` (missing pyramid_risks), but Cromwell/Telegram often surfaces as a **hang** or generic error (WUT returned HTML exception page, not structured MCP error).  
2. **HTTP hangs under load** — `/internal/portfolio_config?run_id=` can time out when WUT puma is busy with large PBR progress writes (see sibling ticket on results_json).  
3. **No single happy-path playbook** — transfer lands **inactive paper** by design; activate is a second step with Active mutex; agents sometimes chain poorly or wait forever.  
4. **Reply contract gaps** — when transfer fails, `reply_text` / structured `code` may be missing so the agent retries blindly.

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
- [ ] Under moderate WUT load, transfer either succeeds or returns timeout code (no infinite agent wait)  
- [ ] Documented two-step flow: transfer (inactive) → activate (explicit)  
- [ ] Optional smoke script under `portfolio_configs/` or `ecosystem/tmp` promoted if useful  

## Non-goals

- Auto-activate on every transfer  
- Changing Active mutex policy  
- Real capital activation (separate ticket)  
