# Ticket: Harden Cromwell cron against post-truncation hallucination

**Status:** Done (offline guards 2026-07-20; live hourly observe deferred)  
**Priority:** P1
**Context:** Issue `docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`. Session `docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`. Related open quality work: `docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`.

## Problem

On 2026-07-13, `market-snapshot-hourly` called `wv2_market_snapshot` successfully, hit output truncation, then looped **8×** on `read_file({"path": "path/to/file.txt"})` and posted a human-facing ask for the path to Sawtooth Main. Job still marked completed.

Same day, later hourlies posted “stable market” with **no** MCP tool call.

Cron duty is not enforced: completion does not require the mandated tool, and identical failed tool calls are not circuit-broken.

## Acceptance criteria

- [x] Circuit-break (or hard-stop) after N identical failed tool calls (same name + args) within one turn/job — **runtime** `identical_fail_limit` (default 2) on `ToolRegistry.execute` / `prepare_call`
- [x] Cron turns that require MCP (e.g. market snapshot) either invoke the tool with a fresh call or **hard-fail** with a short ops error — never invent “stable / no movers” — **`mcp_require` + `finalize_content` rewrite + message-tool gate**
- [x] Cron/system turns must **not** ask the human for file paths or other free-form recovery — **path-ask detector + `builtin_deny` read_file + placeholder path block**
- [ ] Natural or forced `market-snapshot-hourly` posts non-placeholder content after a real `wv2_market_snapshot` call — **deferred to live observe** ([`2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md)); offline unit tests cover guards only
- [x] Cross-link result from parent issue when Done

## Implementation (2026-07-20)

### Layers

1. **Runtime (nanobot image patch)** — `ecosystem/ai/nanobot/patches/cron_tool_allowlist.py`
   - MCP allowlist (existing) + `mcp_require` duty hard-fail
   - `builtin_deny` (snapshot/EOD/DM/ecosystem deny `read_file`/`write_file`/`edit_file`)
   - Placeholder path reject (`path/to/file.txt`)
   - Identical-fail circuit-break (N=2)
   - Message tool blocked until required MCP succeeds; path-asks blocked
   - `AgentProgressHook.finalize_content` rewrites missing-MCP / path-ask finals to OPS ERROR
2. **Config** — `ecosystem/ai/schedule/cron-tool-allowlist.json` (`mcp_require`, `builtin_deny`, `identical_fail_limit`)
3. **Prompts/skills** — market-snapshot + heartbeat + open/hourly cron messages + `cromwell-tools.md`

### Verify offline

```bash
pytest ecosystem/ai/nanobot/patches/test_cron_tool_allowlist.py -v
# 18 passed
```

### Deploy (ops)

```bash
bin/seed-cromwell-workspace --force-cron
./bin/compose --profile ai build nanobot_cromwell
./bin/compose --profile ai up -d --no-deps nanobot_cromwell
```

### Residual risk

- Live Telegram hourlies not observed in this session — track on observe ticket.
- Small model may still produce low-quality (but non-hallucinated-duty) prose after a real tool call; quality is separate from duty enforcement.
- `AgentProgressHook` patch depends on nanobot-ai 0.2.2 layout; re-check on pin bump.

## Related

- Issue: [`docs/issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md`](../issues/2026-07-13-cromwell-cron-placeholder-path-hallucination.md)
- Observe (live AC): [`docs/tickets/2026-07-13-observe-cromwell-market-snapshot-hourlies.md`](2026-07-13-observe-cromwell-market-snapshot-hourlies.md)
- Ticket: [`docs/tickets/2026-07-09-cromwell-cron-llm-timeout.md`](2026-07-09-cromwell-cron-llm-timeout.md)
- Ticket: [`docs/tickets/2026-07-09-cromwell-cpu-only-llm-tuning.md`](2026-07-09-cromwell-cpu-only-llm-tuning.md)
- Prior allowlist: [`docs/tickets/archive/2026-07-20-cromwell-cron-tool-allowlist.md`](archive/2026-07-20-cromwell-cron-tool-allowlist.md)
- Session: [`docs/session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md`](../session-reports/2026-07-13-1216-cromwell-telegram-placeholder-path.md)
- Ops: [`docs/operations/cron-tool-allowlist.md`](../operations/cron-tool-allowlist.md)
