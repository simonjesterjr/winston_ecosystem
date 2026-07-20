# Winston Journal vs Trading Ledger

**Date:** 2026-07-15  
**Status:** Reference (technical evaluation)  
**Monoliths:** Wv2 (ops SoT), WUT (lab journal / CSV export), Cromwell/Telegram (confirm path)  
**Glossary:** `CONTEXT.md` — Journal, Operational Portfolio, Engaged, CashEvent, Daily Analysis, Position  
**Related ADR:** ADR-006 (engagement lock on first Journal)

## Purpose

Evaluate Winston’s **Journal** (schema, behavior, WUT/Wv2/Telegram access) against:

1. Industry-standard **Trading Ledger** / trade blotter expectations  
2. Core live/Active portfolio desk use cases (esp. free-form fills and stops)  
3. Export as PDF / Word / ledger dump  

This document is the discovery entry for the **journal → ledger** ticket series. Implementers should read this before picking tickets; tickets cite this path rather than restating the full evaluation.

## Product framing

Treat Journal as what it already is:

> A proposed or confirmed trade action record in Wv2 daily analysis — entry, exit, pyramid, with flow/MTM/risk sizing. Any journal engages the Operational Portfolio and freezes its tradeable shape until Closed.

**Not** a full broker OMS ledger or double-entry general ledger. Closest analogues:

| Analogue | Fit |
|----------|-----|
| Ops blotter with approval (`draft` → `executed`) | Strong |
| Cash-flow spine for portfolio equity | Strong (esp. WUT backtests) |
| Broker fill ledger / OMS order book | Weak / absent |
| Human free-form trade diary | Weak today |

**Target evolution:** keep confirmation hygiene; extend toward a desk-usable **trading ledger** for Active OPs without pretending to be a broker.

---

## Schema snapshot

### Wv2 journals (operational)

| Field | Role |
|-------|------|
| `portfolio_id`, `market_id`, `position_id` | Account / symbol / lot |
| `trade_date` | Business date (no first-class fill timestamp) |
| `flow`, `debit_credit` | Signed cash impact |
| `run_capital` | Capital base snapshot |
| `mark_to_market` | MTM column present; ops path underused |
| `position_sizing_risk`, `position_action_initiation` | Risk / initiation metadata |
| `expected_return_data` | JSON analytics (WUT parity; live optional) |
| `fulfillment_type`, `fulfillment_details` | stock/LEAP…; JSON still mirrors fill for one-release back-compat |
| `execution_price`, `units`, `executed_at` | **First-class fill columns** (journal-to-ledger #1, 2026-07-20) |
| `status` | `draft` \| `executed` \| `cancelled` \| `passed` |
| `notes` | Signal reason + human confirm notes |

**Positions (adjacent):** `direction`, `units`, `execution_price`, `original_stop`, `updated_stop`, `action_description` (`OPEN…` / `CLOSED @ …`).

### WUT journals (lab)

Same cash spine + `run_id` for backtest runs; rich expected-return / MTM trajectory.  
**Gap:** Operations code writes `status`, `execution_price`, `execution_volume`, `executed_at`, `active_account_id`, `bar_date` — columns **not** present on `journals` in `schema.rb` (schema/code drift). Lab **CSV `export_journal`** is mature; live ops SoT is Wv2.

### Industry trading ledger (reference checklist)

| Concern | Winston today | Gap? |
|---------|---------------|------|
| Account / book | Portfolio (+ seed, execution_mode) | — |
| Instrument | Market | Options mostly on Position |
| Side / action | Split: debit_credit + task_type + Position.direction | Partial |
| Qty & fill price | Position + `fulfillment_details` after confirm | Promote to columns |
| Trade datetime | `trade_date` only | Yes |
| Commission / fees / net | Absent | Yes |
| Broker / venue / order id | Absent | By design for now |
| Realized P&L per ticket | Implied via exit flow | Partial |
| Working orders (resting stop) | Stops on Position only | Yes |
| Partial fills | Single units/price | Yes |
| Draft before book | First-class | Strength |
| Pass / skip reasons | PassedSignal | Strength |
| Strategy linkage | TradingStrategy / fingerprint | Strength |
| Engagement lock | First journal freezes Books/TS | Domain strength |

---

## Functionality (current)

| Path | Behavior |
|------|----------|
| Daily Analysis → `TaskGenerator` | Creates **draft** journals + `OperationsTask` (enter/exit; pyramid type exists) |
| `JournalConfirmationService` | `draft` → `executed`; opens/closes Position; signed `flow`; completes task |
| Stop on open | ATR × portfolio multiplier via `JournalPositionExecutor` — **not** human override |
| MCP | `wv2_get_journal`, `wv2_confirm_journal`, `wv2_mark_task_done`, `wv2_list_pending_actions`, `wv2_get_portfolio_status` |
| Ops shell | Same services: `pending` / `confirm` / `journal` / `status` |
| Telegram | Cromwell `winston-confirmation-loop` — confirm existing drafts only |
| Manual “I bought X” without DAR draft | **Supported** via `wv2_book_trade` / `POST /internal/journals/book` (2026-07-16) |
| Custom stop at confirm / later | **Not supported** |

### Litmus use case

> “I just bought 45 shares of GGG for Portfolio YGF at $58.87 and put a stop in at $55.”

| Sub-step | Today |
|----------|--------|
| Portfolio + symbol (if Book exists) | OK |
| Units + fill price on **confirm of existing draft** | OK (MCP / shell) |
| Free-form book without draft | **No** |
| Stop = $55 | **No** (ATR default only) |
| Telegram natural language → book | **No** (confirm only) |

**Works:** “Winston signaled GGG — confirm 45 @ 58.87.”  
**Fails:** free-form buy + human stop as a single desk utterance.

---

## Accessibility

| Surface | Capability |
|---------|------------|
| **WUT** | Backtest journal UI + CSV export; Operations Accept & Complete (lab; schema drift) |
| **Wv2 ops shell** | Read + confirm; same as MCP |
| **Wv2 MCP / Telegram** | Confirm loop strong; no book/stop/export tools |
| **Wv2 `resources :journals`** | Route without controller — dead |
| **Daily Activity PDF/MD** | Ops narrative + open positions (includes stop column); not a ledger dump |

---

## Export

| Artifact | Journal coverage |
|----------|------------------|
| Wv2 Daily Activity PDF/MD | Today’s actions, open positions, thin `recent_journals` in JSON |
| Cromwell notification JSON | ~20 recent journals (10-day window) |
| WUT `export_journal` CSV | Full run history (lab) |
| Wv2 portfolio ledger CSV/PDF/DOCX | **Missing** |
| Word (.docx) | **Missing** |

---

## Scorecard

| Dimension | 1–5 | Notes |
|-----------|-----|--------|
| Schema for ops confirmation | 4 | Status + fulfillment + position link |
| Schema as industry trading ledger | 2.5 | Fees, timestamps, free-form entry missing |
| Confirm signal-driven trade | 4.5 | Telegram-ready for paper hygiene |
| Free-form buy @ price + stop | 1.5 | Needs book + stop APIs |
| WUT accessibility | 4 lab / 2 live | Live = Wv2 |
| Wv2 + Telegram | 4 confirm / 2 invent | — |
| Export PDF/Word/ledger | 3 daily / 1 ledger | — |

---

## Recommended architecture (journal → ledger)

| Layer | Keep | Add |
|-------|------|-----|
| **Journal** | draft/executed, flow, engagement | Manual book, cancel, first-class fill fields, optional fees later |
| **Position** | units, stops, CLOSED | Stop override on open; stop-update path (or journal type `stop_adjust`) |
| **Export** | Daily PDF | Portfolio-scoped ledger CSV → PDF; Word optional |
| **MCP / Telegram** | Confirmation loop | `book_trade` / `set_stop` with human confirm-before-write |
| **WUT** | Lab CSV + backtest journals | Align or retire ops columns; do not re-home live ledger |

**Order of work (dependency):** promote fill fields → ad-hoc book → stop override/update → ledger export → UI/route cleanup → WUT schema hygiene → (deferred) order-vs-fill.

---

## Ticket series: `journal-to-ledger`

Discoverable label for this program. All tickets below **must** link back here.

| # | Ticket | Status | Depends on | Intent |
|---|--------|--------|------------|--------|
| 0 | **This analysis** | Reference | — | Product + schema evaluation |
| 1 | [`2026-07-15-journal-ledger-promote-fill-fields.md`](../tickets/2026-07-15-journal-ledger-promote-fill-fields.md) | **Done** (2026-07-20) | — | First-class fill columns (foundation) |
| 2 | [`2026-07-14-wv2-ad-hoc-paper-fill-mcp.md`](../tickets/2026-07-14-wv2-ad-hoc-paper-fill-mcp.md) | **Done** (2026-07-16) | #1 preferred (uses fulfillment_details until #1) | Book trade without DAR draft |
| 3 | [`2026-07-15-journal-ledger-stop-on-confirm-and-update.md`](../tickets/2026-07-15-journal-ledger-stop-on-confirm-and-update.md) | Proposed | #1–2 | Human stop at book/confirm + update |
| 4 | [`2026-07-15-journal-ledger-export-csv-pdf.md`](../tickets/2026-07-15-journal-ledger-export-csv-pdf.md) | Proposed | #1–2 (stronger after #3) | Portfolio ledger export |
| 5 | [`2026-07-15-journal-ledger-wv2-journals-ui-or-route-cleanup.md`](../tickets/2026-07-15-journal-ledger-wv2-journals-ui-or-route-cleanup.md) | Proposed | #1 optional | Fix dead route / thin browse UI |
| 6 | [`2026-07-15-journal-ledger-wut-ops-schema-alignment.md`](../tickets/2026-07-15-journal-ledger-wut-ops-schema-alignment.md) | Proposed | — (parallel) | WUT ops vs schema drift |
| 7 | [`2026-07-15-journal-ledger-order-vs-fill-deferred.md`](../tickets/2026-07-15-journal-ledger-order-vs-fill-deferred.md) | Deferred | #3 | Resting orders vs position stops |

**Already done (prerequisite hygiene, not part of ledger expansion):**

- `2026-07-13-confirm-first-paper-journal-focus-cohort.md` — first paper confirm  
- `2026-07-14-mcp-deactivate-and-confirmation-skill.md` — confirmation loop skill  

**Suggested pick-up order for a near-future session:** #1 → #2 → #3 → #4; then #5/#6 as polish; #7 only if desk needs working-order semantics.

---

## Non-goals (this series)

- End-to-end broker automation / OMS  
- Full double-entry accounting GL  
- Tax lot engine  
- LEAP/options real mechanics (separate track)  
- Replacing Daily Activity PDF with ledger PDF (complement, don’t collapse)

## See also

- `CONTEXT.md` — Journal, Engaged Operational Portfolio  
- `docs/business-context/wv2-operational-portfolio-lifecycle.md`  
- `docs/adr/ADR-006-operational-portfolio-lineage-and-lifecycle.md`  
- `interfaces/winston-mcp-tools.md` — confirm / get journal tools  
- `ecosystem/ai/skills/winston-confirmation-loop/SKILL.md`  
- WUT `export_journal` (backtest CSV pattern to reuse for Wv2)  
