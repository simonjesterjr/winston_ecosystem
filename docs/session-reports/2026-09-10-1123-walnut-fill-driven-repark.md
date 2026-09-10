# Session Report — Walnut fill-driven repark (intra-day STP prints)

**Date:** 2026-09-10
**Time:** ~09:00–11:23 MDT
**Duration:** ~2h 20m
**Project:** sawtooth Winston ecosystem (winston_v2 + ecosystem)
**Working directory:** `/home/johnkoisch/Documents/com/sawtooth`
**Branch:** `winston_v2` main; `ecosystem` main (both dirty vs origin with other grains)
**Model:** Grok 4.6 (xAI)
**Operator:** johnkoisch

---

## 1. Goal & Outcome

**Stated goal:** Continue Walnut paper Session Order Slate Direction 1. Confirm Winston is picking up intra-day Interactive Brokers (IBKR) paper DUT fills of parked stop-markets (STP); write Good-Til-Cancelled (GTC) protectives for naked lots as soon as possible; wire fill → Telegram → delta slate → Approve → auto-send → book.

**Outcome:** Delivered (live-stressed). Three DUT prints Accept-Filled; fill-driven delta slates minted; operator Approved; GTC protectives and DAY pyramids parked. A nested DBC pyramid print forced a second delta (slate #46). Poll cadence locked at 15 minutes. Broker push/websocket parked as a P1 evaluation.

**One-line summary:** Walnut park → print → book → repark ran on live paper DUT this morning; 15-minute poll is the fill path (no IBKR webhook); GTC stops use the Operational Portfolio’s Trading Strategy (TS) Average True Range (ATR) knobs, not the entry trigger.

---

## 2. Work Completed

- Confirmed live: Portfolio Walnut Operational Portfolio (OP) **#1428**, slate **#40** executing. **Three** Accept-Fills ~13:30 UTC (not two): DD short 36 @ 127.10 (j#1577 / pos#784), DBC pyramid 281 @ 33.21 (j#1571 / pos#785), SCHZ short 914 @ 22.49 (j#1589 / pos#786).
- Documented the fill path: Broker Gateway (BG) poll of Client Portal Gateway (CPGW) `GET /iserver/account/trades` + `GET /iserver/account/orders` → Winston v2 (Wv2) Confirmation Intake → `WqFillBind`. No HTTP webhook. CPGW websocket not used.
- Operator review applied: poll **15 minutes** (not 1/5); TS knobs for protective N and pyramid step; EOD parquet ATR lag accepted; websocket **evaluate later**.
- Filed P1 ticket `docs/tickets/2026-09-10-bg-broker-push-websocket-eval.md` (IBKR/Schwab push vs poll; possible BG listener sidecar; do not implement).
- Fill-Driven Repark: intra-day **delta** slate (not `Builder`/`DayTeardown`, which would yank remaining DAY parks). GTC at last fill ± `effective_atr_multiplier` × ATR; DAY pyramid at last fill ± `effective_pyramid_atr_multiplier` × ATR; opposite DAY entry cancelled (first-to-touch). DBC two-phase: park combined GTC, then cancel old with `allow_protective`.
- Accept-Fill Working Stop: do not copy the entry/pyramid **trigger** onto `Position.original_stop`; compute TS N from the print.
- OpsTelegram text `sendMessage` to Sawtooth Main (fail open). Ops shell NAKED / slate-update tags; position timeline GTC chips; signal-inspect GTC overlay.
- Live loop: slate **#41** Approved → GTC on DD/SCHZ/DBC; DBC DAY pyramid **filled again** (278 @ 33.45, pos#787); stale 563-unit GTC; slate **#46** draft then executing with DBC GTC **841 @ 32.56** (DUT `443701711`) and DAY pyramid 276 @ 33.67 (`443701712`).
- Glossary: **Fill-Driven Repark** in `CONTEXT.md`. Accept-Fill ticket marked Done with ids.

---

## 3. Code Delivered

### Files changed (this session — not other dirty-tree work)

Winston v2:

| File | Change | Notes |
|------|--------|-------|
| `app/services/operations/session_order_slate/fill_driven_repark.rb` | added | delta slate; opposite DAY cancel; DBC replace stamp |
| `app/services/operations/session_order_slate/levels.rb` | added | TS N / pyramid trigger |
| `app/services/operations/session_order_slate/protective_status.rb` | added | NAKED / STALE vs DUT GTC |
| `app/services/operations/session_order_slate/auto_send.rb` | added/modified | two-phase cancel-old GTC after new oid |
| `app/services/ops_telegram.rb` | added | text sendMessage, fail open |
| `app/jobs/quiver_tracking/working_fill_job.rb` | modified | 15-min hook: bind + repark + telegram; run if naked lots |
| `app/models/portfolio.rb` | modified | `effective_pyramid_atr_multiplier` |
| `app/services/operations/session_order_slate/builder.rb` | modified | pyramid step from TS (not hardcoded 0.5) |
| `app/services/operations/journal_confirmation_service.rb` | modified | `lot_working_stop_price` (unstaged hunk; file also has parallel GTC-guard grain — see wrap notes) |
| `app/services/operations/journal_position_executor.rb` | modified | round Working Stop 0.01 |
| `app/services/confirmation_intake/match_notification.rb` | modified | `protective_stop` is exitish |
| `app/controllers/operations/slates_controller.rb` | modified | all `open_desk` slates |
| `app/views/operations/slates/show.html.erb` | modified | fill-driven + NAKED banner |
| `app/services/operations/ops_shell_panels.rb` | modified | naked_lot_count, slate_update, gtc_status |
| `app/views/operations/home/*` | modified | NAKED / GTC chips |
| `app/services/operations/signal_inspect_payload.rb` | modified | `gtc` overlay |
| `config/sidekiq_schedule.yml` | modified | confirmation_intake + wq_working_fill `*/15` |
| matching specs | added/modified | repark, auto-send replace, 2N stop, telegram skip, slate dual list |

Ecosystem:

| File | Change | Notes |
|------|--------|-------|
| `CONTEXT.md` | modified | Fill-Driven Repark; 15-min poll; Accept-Fill proof |
| `docs/tickets/2026-09-10-bg-broker-push-websocket-eval.md` | added | P1 eval, not implement |
| `docs/tickets/2026-09-09-walnut-stp-accept-fill-day-entry.md` | modified | Done + ids |
| `docs/tickets/2026-09-09-walnut-paper-session-order-slate.md` | modified | 2026-09-10 fills + repark |
| `docs/tickets/INDEX.md` | modified | new P1 + Accept-Fill Done |
| `docs/session-reports/2026-09-10-1123-walnut-fill-driven-repark.md` | added | this report |

Broker Gateway: **none** this session (cancel/allow_protective already on the desk from 2026-09-09 evening).

### Commits

Pending this wrap (see §3 wrap notes). Do **not** `git add .`.

### Branch / PR state at sign-off

- Branch: `main` on wv2 and ecosystem
- Pushed: this wrap
- PR: not opened (commits on `main`)

**Do not** `git add .`. Other dirty files (MACD inspect, ProtectiveGtcGuard, Pulse/WEV leftovers, quiver, `vendor/`) are **not** this session.

---

## 4. Decisions Made

### Decision 1: 15-minute poll, not a live tape
- **Choice:** `WorkingFillJob` and `ConfirmationIntakeJob` cron `*/15 * * * *`. BG `ibkr_tickle` stays every minute (session keepalive only).
- **Why:** Operator: “as soon as possible” is not a live-data system. ~32 evals in regular hours is enough for End of Day (EOD) Trend Following (TF).
- **Alternatives considered:** keep 1-minute WorkingFill; CPGW websocket now.
- **Reversibility:** easy (cron)
- **Promote to ADR?** no — operational cadence; note in CONTEXT

### Decision 2: No webhook / websocket in this grain
- **Choice:** stay on REST poll. File P1 eval for IBKR/Schwab push and a possible BG listener sidecar.
- **Why:** CPGW has no HTTP webhook we can register; websocket is unproven against tickle/`compete`/reauth.
- **Reversibility:** easy
- **Promote to ADR?** no until the eval returns go/no-go

### Decision 3: Fill-driven **delta** slate, not Rebuild
- **Choice:** `FillDrivenRepark` mints a new draft; does not call `DayTeardown`. Overnight slate #40 stays executing.
- **Why:** Rebuild cancels all Walnut DAY tickets (POET, ONDS, …).
- **Reversibility:** easy
- **Promote to ADR?** no — glossary Fill-Driven Repark is enough

### Decision 4: Slate Approve still gates the delta (including GTC)
- **Choice:** operator Approves fill-driven GTC + DAY pyramid. Protective auto-send without Approve is a later Direction-1 slice after this loop is proven.
- **Why:** operator sketch; not Slate Automation.
- **Reversibility:** easy
- **Promote to ADR?** no

### Decision 5: Working Stop from TS knobs, not the STP trigger
- **Choice:** `lot_working_stop_price` / `Levels.working_stop` = fill ± `effective_atr_multiplier` × parquet ATR. Pyramid = `effective_pyramid_atr_multiplier`.
- **Why:** DD/SCHZ lots had original_stop = 55-day trigger (127.75 / 22.56). Walnut 2N vs another book 1.25N must come from the TS.
- **Reversibility:** easy
- **Promote to ADR?** no — already in turtle-s2 business-context

### Decision 6: DBC replace = new GTC then cancel old
- **Choice:** `replaces_broker_order_id` on the new protective; AutoSend cancels old with `allow_protective` only after a new DUT oid. Native `replace_order` still refused.
- **Why:** never naked between cancel-ack and new-ack.
- **Reversibility:** easy once native replace ships
- **Promote to ADR?** no

---

## 5. Insights Surfaced

- Accept-Fill at DUT print **works** on Walnut STP, including split executions (SCHZ 4-way, DBC 2-way) summed by `broker_order_id`.
- Nested fills are the real stressor: a fill-driven DAY pyramid can print **immediately**, leaving the just-parked GTC stale (DBC 563 → 841). Idempotency must key **units + stop**, not only role/symbol/side, and must not treat an **executing** prior delta as covering a new size.
- `@portfolio.positions` association cache hid a third lot until `positions.reset` / `reload`.
- 1-minute cron still running until Sidekiq restart minted/cancelled slates #42–#45. Restart after cadence change is required.
- Confirmation Intake fixture specs still orphan when `occurred_at` is outside the 7-day window (pre-existing; ticket `2026-09-06-intake-match-fixture-window.md`). New protective_stop side match passed.
- DD/SCHZ `Position.original_stop` still shows the **old trigger** (booked before the Working Stop fix). DUT GTC is the correct 2N. Next Accept-Fill will stamp TS N.

---

## 6. Issues & Tickets

### Resolved this session
- Accept-Fill at DUT print unproven — **Done** with three ids (`2026-09-09-walnut-stp-accept-fill-day-entry.md`)
- Naked DD/SCHZ after morning prints — GTC parked (slate #41)
- Stale DBC GTC after 3rd lot — slate #46 GTC 841 @ 32.56 parked (`443701711`)

### Deferred
- **BG native replace** — still refused; two-phase is the workaround (parent slate ticket)
- **Protective auto-send without Approve** — later Direction-1 after this loop is proven (operator lock)
- **Broker push/websocket eval** — [`2026-09-10-bg-broker-push-websocket-eval.md`](../tickets/2026-09-10-bg-broker-push-websocket-eval.md)
- **Close-of-day DAY honesty** — [`2026-09-09-walnut-day-stp-close-reconcile.md`](../tickets/2026-09-09-walnut-day-stp-close-reconcile.md) after 16:00 ET
- **LEAPs** — still parked (`2026-09-09-extra-modal-leap-unit-evaluation.md`)
- **Per-conid tick** — [`2026-09-09-ibkr-stp-tick-size.md`](../tickets/2026-09-09-ibkr-stp-tick-size.md)
- **CPGW unattended session** — [`2026-09-06-ibkr-cpgw-unattended-session.md`](../tickets/2026-09-06-ibkr-cpgw-unattended-session.md)
- **DA 20-day exit while lots < max** — slate rule wins at broker; dirty-tree issue exists, not this commit
- Backfill DD/SCHZ `original_stop` to TS N (desk display vs DUT GTC)

---

## 7. Verification Status

| Component | Verification | Result |
|-----------|--------------|--------|
| FillDrivenRepark (TS N, opposite DAY, DBC combine, idempotency, new delta on size change) | `podman exec -e RAILS_ENV=test -e TEST_DB_HOST=wv2_postgres -e DATABASE_HOST=wv2_postgres winston_v2 bundle exec rspec spec/services/operations/session_order_slate_fill_driven_repark_spec.rb` | ✅ 6 examples |
| AutoSend replace-cancel, Confirm-Send 2N stop, WorkingFillJob hook, OpsTelegram skip, slate dual list, protective match | same env: auto_send, journal_confirmation_ibkr_paper, working_fill_job, ops_telegram, operations_slate, match_and_prefill (new example) | ✅ this grain; ⚠️ 5 pre-existing fixture-window orphans in match_and_prefill |
| Live DUT | DD/SCHZ/DBC GTC oids; DBC 3rd lot repark 841 @ 32.56; opposite DAY cancelled | ✅ operator + DB |
| Telegram | fail-open specs; live send depends on `WV2_TELEGRAM_BOT_TOKEN` in compose | ⚠️ not independently confirmed on Sawtooth Main |
| Browser UI | operator used Tailscale slate Approve; agent did not click | ⚠️ operator-verified |

**Test command(s):** see table.

---

## 8. Environment, Dependencies, Data

- **Dependencies:** None new
- **Services:** compose `winston_v2`, `winston_v2_sidekiq` (restarted for 15-min cron), `broker_gateway`, CPGW `https://localhost:5000`, Tailscale Serve `/wv2`
- **Migrations:** None
- **Live objects:** Walnut #1428; slates #40 (overnight DAY) + #41/#46 fill-driven executing; lots DBC 282+281+278 long, DD 36 short, SCHZ 914 short; DUT account DUT070450

---

## 9. Risks & Technical Debt

- Naked window until Approve (mitigated by Telegram + NAKED tag). Next slice: auto-send fill-driven GTC only.
- 15-minute poll after a nested pyramid print leaves GTC stale until the next tick (or a manual `FillDrivenRepark.call`).
- Native replace still off; two GTC overlap briefly on DBC.
- `compete: true` still kicks Trader Workstation (TWS) on the same paper user.
- Wv2 `main` dirty with MACD inspect, ProtectiveGtcGuard, quiver, Pulse leftovers — wrap must not `git add .`.
- `journal_confirmation_service.rb` is mixed with a parallel GTC-guard/flatten grain already in the index.

---

## 10. Open Questions

- **Did Sawtooth Main receive the fill/repark Telegram lines?** — check the channel; token may be unset in Wv2 compose.
- **Should fill-driven GTC auto-send without Approve now that #41 and #46 proved the loop?** — operator later.
- **Backfill DD/SCHZ original_stop?** — DUT GTC is already 2N; desk lots still show the trigger.

---

## 11. Handoff & Resume Notes

- **Where I left off:** Live book protected: DD GTC 133.88, SCHZ GTC 22.76, DBC GTC 841 @ 32.56 + DAY pyramid 33.67. Slate #46 executing. 15-min Sidekiq cron loaded after restart.
- **Next concrete step:** After cash close, reconcile unfilled DAY vs DUT (`2026-09-09-walnut-day-stp-close-reconcile.md`). If DBC 33.67 prints, next fill-driven delta should mint GTC ~1117 at last-fill 2N.
- **Files to read first:**
  1. `ecosystem/docs/tickets/2026-09-09-walnut-paper-session-order-slate.md`
  2. `winston_v2/app/services/operations/session_order_slate/fill_driven_repark.rb`
  3. `winston_v2/app/jobs/quiver_tracking/working_fill_job.rb`
  4. `ecosystem/docs/tickets/2026-09-10-bg-broker-push-websocket-eval.md`

Slate URL: `https://sawtooth-ai.tail944ffb.ts.net/wv2/operations/slate?portfolio_id=1428`

---

## 12. Stakeholder Communications

- Operator (John) is the audience. No outward email.

---

## 13. Tools & Workflow Notes

- **Skills used:** operator-prose, wrap, session-report, record (ticket)
- **What worked well:** live DUT prints as the test harness; fail-closed place + Accept-Fill already in place so this session could be “after the print”
- **Friction points:** mixed dirty trees (MACD + GTC-guard + this grain); Sidekiq-cron not picking up yml until restart; association cache on `positions`
- **Subagent usage:** none

---

## 14. Follow-up Actions

- [ ] After 16:00 ET: DAY vs DUT close reconcile — [`../tickets/2026-09-09-walnut-day-stp-close-reconcile.md`](../tickets/2026-09-09-walnut-day-stp-close-reconcile.md)
- [ ] Evaluate CPGW/Schwab push — [`../tickets/2026-09-10-bg-broker-push-websocket-eval.md`](../tickets/2026-09-10-bg-broker-push-websocket-eval.md)
- [ ] Later Direction 1: auto-send fill-driven GTC without a second Approve
- [ ] Native BG `replace_order`
- [ ] Confirm Telegram delivery on Sawtooth Main
- [x] Wrap: session report + commit/push this grain only

---

## 15. Appendix

### Morning Accept-Fills (13:30 UTC)

| Journal | Symbol | Role | DUT oid | Fill | Position |
|---------|--------|------|---------|------|----------|
| 1577 | DD | entry_stop DAY | 576658786 | 127.10 | 784 |
| 1571 | DBC | pyramid_stop DAY | 576658780 | 33.21 | 785 |
| 1589 | SCHZ | entry_stop DAY | 576658798 | 22.49 | 786 |

### Protective / pyramid working at wrap (11:23 MDT)

| Journal | Symbol | Role | Stop | DUT oid |
|---------|--------|------|------|---------|
| 1637 | DD | GTC protective | 133.88 | 443701250 |
| 1638 | DD | DAY pyramid | 125.40 | 443701278 |
| 1639 | SCHZ | GTC protective | 22.76 | 443701251 |
| 1640 | SCHZ | DAY pyramid | 22.42 | 443701279 |
| 1651 | DBC | GTC protective | 32.56 (841 u) | 443701711 |
| 1652 | DBC | DAY pyramid | 33.67 (276 u) | 443701712 |

DBC lots: 282 @ 32.84 + 281 @ 33.21 + 278 @ 33.45 (3 of 4). Shared `updated_stop` 32.56.
