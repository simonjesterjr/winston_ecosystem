# Ticket: Ops daily demo epic — Ops UI + Telegram essential loop

**Status:** In progress (smoke Done 2026-07-17)  
**Date:** 2026-07-17  
**Source:** Session planning + wrap after Close/successor  
**Priority:** High (operator demo confidence)

## Goal

Prove essential **daily** Operational Portfolio functions work via **Wv2 Ops UI** (confirmatory layer) and **Telegram** (close but not identical surface), without Rails console.

Parent epic for thin tickets below. Close + successor are **Done** (`2026-07-14-wv2-close-and-successor-rebalance-services.md`) and unlock engaged shape change.

## Capability matrix (as of 2026-07-17)

| Capability | Ops UI / shell | Telegram / MCP | Gap ticket |
|------------|----------------|----------------|------------|
| List Active OPs by band | `list` | list portfolios | smoke |
| List all open positions | `positions` | portfolio status | smoke |
| DAR desk handoff + confirm | desk form | confirm phrase | smoke |
| Ad-hoc enter / exit / stop | shell + desk | book/exit tools | smoke |
| Capital add/remove | `cash` shell + API | `wv2_add_cash_event` | Done (`shell-cash-parity`) |
| Close OP series | `close_portfolio` | `wv2_close_portfolio` | smoke |
| Successor / add market (engaged) | `successor` | `wv2_successor_portfolio` | smoke |
| All positions last DAR page + move/signal | Open book page | same payload | Done (`dar-positions-blotter`) |
| Edit draft journal | view/confirm only | get/confirm | draft edit |
| Signal → related instrument (LEAP) | schema only | fulfillment_type thin | related fill |
| External stop (no Winston signal) | reason=external_stop | reason on exit | Done (`external-stop-exit`) |
| Pyramid / close-all / move-all stops | exit_all / stops | exit_all / update_stops | Done (`bulk-risk-actions`) |
| Equity graphs Telegram compare | PDF series | no ad-hoc chart | telegram charts |
| Capital Activation (paper→real series) | — | — | existing ticket |

## Child tickets (demo order)

0. `2026-07-17-ops-daily-demo-smoke-checklist.md`  
1. `2026-07-17-ops-daily-shell-cash-parity.md`  
2. `2026-07-17-ops-daily-dar-positions-blotter.md`  
3. `2026-07-17-ops-daily-external-stop-exit.md`  
4. `2026-07-17-ops-daily-bulk-risk-actions.md`  
5. `2026-07-17-ops-daily-related-instrument-fill.md`  
6. `2026-07-17-ops-daily-journal-draft-edit.md`  
7. `2026-07-17-ops-daily-telegram-equity-compare.md`  

Already tracked (not re-filed): Capital Activation, MCP git-home, compose versioning.

## Acceptance (epic)

- [x] Smoke checklist run once with pass/fail recorded — `2026-07-17-ops-daily-demo-smoke-checklist.md` **Done**  
- [x] No console required for paper day loop on Active OPs — shell cash Done; confirm still needs a live draft when DA produces one  
- [ ] Gaps either Done or consciously deferred with ticket links  

## Smoke takeaway (2026-07-17)

Core desk loop works via Ops shell + MCP without Rails console: list/positions/status, enter/stop/exit, close series, successor shape rebalance, **cash via shell + MCP/API**.  
**Smoke takeaway continued (2026-07-17 blotter):** DAR PDF/MD last section is full Active open blotter (real→paper).  
**External stop packaging Done (2026-07-17):** `reason=external_stop` on exit (shell/desk/MCP).  
**Bulk risk Done (2026-07-17):** `exit_all` + `stops`/`move_stops` (shell/API/MCP) for multi-lot flatten and trail-all.  
**Next build in demo order:** related-instrument fill → journal draft edit → …

## Related

- Session: `docs/session-reports/2026-07-17-1214-close-successor-rebalance.md`  
- ADR-006 / lifecycle business-context  
