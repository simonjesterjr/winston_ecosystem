# Ticket: Human-gated desk actions (DAR form + Telegram phrases + journals)

**Status:** Done (foundation 2026-07-16)  
**Date:** 2026-07-16  
**Series:** paper Telegram Phase 4 / journal→ledger  
**Related:** ad-hoc fill, stop-on-confirm #3, ops shell

## Policy

**Daily Analysis never opens or closes positions.** It only creates draft journals + operations tasks (recommendations). Positions change only via human:

- Ops desk form (`/operations/desk`)
- Ops shell (`enter` / `exit` / `confirm` / `stop`)
- MCP / Telegram (`wv2_book_trade`, confirm, future exit)

Clarification: Blue PBR62 AMZN `#1` was **Phase 1 paper confirm** (journal #16, 2026-07-14), not auto-DAR. Bad stop (−239) was ATR default corruption — executor now guards absurd ATR.

## Delivered

| Item | Detail |
|------|--------|
| Desk form | `GET/POST /operations/desk` prefill task_id / portfolio / symbol / units / price / stop / direction |
| Telegram phrase | `@sawtooth_nanobot confirm …` or `enter …` / `exit …` (copy-paste; no reliable Telegram inject URL for group bots) |
| Pending panel | form link + phrase per task |
| Journals panel | recent journals on focus OP; fix-stop chat fill; open form |
| Exit | `AdHocExitService` + shell `exit` + desk form task_type=exit |
| Stop update | `PositionStopUpdateService` + shell `stop <id> price=S` |
| Pyramid stops | `PyramidStopAdjuster` applies MoveToLastEntry (etc.) when pyramiding |
| DAR payload | `form_path`, `telegram_phrase`, `shell_phrase`, `human_gated` on actions/pending |

## Telegram deep link note

Telegram does **not** support pre-filling arbitrary bot messages in group chats. Options:

1. **Copy-paste phrase** (implemented)  
2. `t.me/BOT?start=PAYLOAD` only for private /start deep links (64-byte payload) — not used for multi-arg enter  
3. Future: bot inline keyboard buttons with callback_data confirming a task_id  

## Follow-ons

- [x] PDF DAR chapter print phrases / form URLs visibly (2026-07-16)  
- [ ] MCP `wv2_exit_trade` + Cromwell skill  
- [ ] Journal edit UI (units/price re-write) beyond stop update  
- [ ] Fix historical bad stops on #12 AMZN (operator: `stop 1 price=…`)  

### PDF / MD handoffs

- Payload `next_steps` carry `form_path`, `form_url`, `telegram_phrase`, `shell_phrase`
- `DailyActivityReportPdfRenderer` section **DESK HANDOFFS (human-gated)** on summary + per-portfolio pages
- Markdown mirror section
- Public base URL: `WV2_PUBLIC_BASE_URL` or `WV2_OPS_BASE_URL` (default `http://localhost:3002`)
