# Ticket: Ops daily demo smoke checklist (Ops UI + Telegram)

**Status:** Done (2026-07-17)  
**Date:** 2026-07-17  
**Epic:** `2026-07-17-ops-daily-demo-epic.md`  
**Priority:** High  

## Problem

Several “missing” daily functions may already work and just need operator verification. Without a written smoke, we keep re-implementing.

## Scope

Run once on live paper Active OPs; record pass/fail (no greenfield features unless smoke fails hard).

### Checklist

- [x] Ops shell `list` — bands real → paper  
- [x] Ops shell `positions` — all Active open lots  
- [x] Ops shell `status <fp>` — capital, markets, journals  
- [x] Desk form / `confirm` draft journal — **SKIP** (no draft journals at smoke time)  
- [x] `enter` / `exit` / `stop` on paper OP  
- [x] Cash: MCP or API inflow + adjustment (note if shell missing) — **API + MCP PASS; shell GAP**  
- [x] `close_portfolio` on disposable OP (not cohort)  
- [x] `successor` add-market on disposable engaged OP  
- [x] Telegram/MCP: tools live after rebuild; MCP mutations exercised (live Telegram phrase left to operator)

## Smoke results (2026-07-17 ~12:23–12:25 MDT)

**Environment:** `winston_v2` + rebuilt `winston_mcp` (host image hash matched `server.py`; nanobot recreated).  
**Script:** `ecosystem/tmp/ops-daily-demo-smoke.rb` (shell path) + in-container MCP `CallToolRequest` handlers.

| Check | Result | Notes |
|-------|--------|-------|
| Ops shell `list` | **PASS** | 4 paper Active / 0 real; bands real→paper |
| Ops shell `positions` | **PASS** | Mango #157 has MSFT lots #7–#8; Orange/Rust/Blue flat |
| Ops shell `status` | **PASS** | Blue #12 capital/markets/journals |
| Ops shell `pending` | **PASS** | none as_of 2026-07-17 |
| Ops shell `confirm` | **SKIP** | no draft/pending journals (only executed/passed) |
| Ops shell `enter` | **PASS** | disposable #196 AAPL j#58 |
| Ops shell `stop` | **PASS** | position #17 95→96 |
| Ops shell `exit` | **PASS** | #196 AAPL j#59 |
| CashEventService inflow | **PASS** | Blue #12 +$25 → capital $10029.85 (pre MCP) |
| Ops shell cash verb | **GAP→Done** | closed same day via `2026-07-17-ops-daily-shell-cash-parity.md` |
| Ops shell `close_portfolio` | **PASS** | #196 closed (paper soft-close, open_residue=1) |
| Ops shell `successor` | **PASS** | #197→#198 markets AAPL,BITQ,TSLA; journals on A |
| MCP rebuild tools present | **PASS** | 30 tools; includes close/successor/cash/exit |
| MCP `wv2_list_portfolios` | **PASS** | |
| MCP `wv2_add_cash_event` | **PASS** | Blue #12 +$10 (cash_event #109) |
| MCP `wv2_close_portfolio` | **PASS** | closed #198 |
| MCP `wv2_successor_portfolio` | **PASS** | #199→#200 Smoke-MCP-A |
| Live Telegram confirm phrase | **SKIP** | operator manual; MCP is Telegram mutation path |

**Summary:** pass=14 · fail=0 · skip=2 · gap=1 (shell cash) — gap closed same day (`shell-cash-parity` Done)

### Active paper cohort at smoke (unchanged attention)

| OP | Mode | Notes |
|----|------|-------|
| #6 Orange · 6622b2eb | paper | 15 markets (over paper cap narrative) |
| #11 Rust · dd7e7c7a | paper | |
| #12 Blue · PBR62 | paper | +$35 smoke cash residue ($25 shell path + $10 MCP) |
| #157 Mango | paper | open MSFT paper lots #7–#8 |

### Disposable residue (closed / archive)

- #196 Smoke-Demo closed; #197→#198 shell successor (198 MCP-closed); #199→#200 MCP successor

## Acceptance

- [x] Results table (pass/fail/notes) in ticket  
- [x] Failures spawn or update gap tickets — only gap is existing shell cash parity  

## MCP rebuild notes

- Image already contained close/successor (host/image md5 match).  
- Podman compose `up --force-recreate` cascades name conflicts; working pattern:
  1. `podman rm -f nanobot_cromwell`
  2. `podman rm -f winston_mcp`
  3. `bin/compose --profile ai up -d --no-deps winston_mcp`
  4. `bin/compose --profile ai up -d --no-deps nanobot_cromwell`

## Related

- Epic: `2026-07-17-ops-daily-demo-epic.md`  
- Shell cash gap: `2026-07-17-ops-daily-shell-cash-parity.md`  
- Session: Close/successor wrap `2026-07-17-1214-close-successor-rebalance.md`  
