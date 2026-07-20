# Ticket: Ad-hoc paper fill (journal without DAR draft)

**Status:** **Done** (2026-07-16) — service + internal API + MCP + skill + live smoke  
**Date:** 2026-07-14 (updated 2026-07-15 for journal→ledger series; closed 2026-07-16)  
**Series:** `journal-to-ledger` **#2**  
**Analysis:** [`docs/analysis/2026-07-15-winston-journal-vs-trading-ledger.md`](../analysis/2026-07-15-winston-journal-vs-trading-ledger.md)  
**Source:** Paper Telegram roadmap Phase 4; session `2026-07-14-1112-paper-telegram-phase0-1.md`; journal evaluation 2026-07-15

## Problem

Desk utterances like:

- “I bought 54 shares of TSMC at 323.44 for portfolio Magenta”  
- “I just bought 45 shares of GGG for Portfolio YGF at $58.87 …”  

are **not** supported. Confirm path only executes **existing draft** journals from Daily Analysis (`TaskGenerator` → draft + task). Free-form fills never create a journal, so Telegram/MCP cannot book them.

See analysis § litmus use case and § Functionality.

## Scope

1. Internal create path: draft-then-confirm **or** single-shot executed journal with explicit portfolio, market, date, direction, units, price.  
2. Reuse `JournalPositionExecutor` / capital flow rules (same signed `flow` as DAR confirm).  
3. Market must be on portfolio Books (or explicit force with audit note — prefer hard require Book).  
4. MCP tool (e.g. `wv2_book_trade` or `wv2_create_journal`) + Cromwell skill (confirm-before-write; never invent fills).  
5. Ops shell: e.g. `book <portfolio> <symbol> units=N price=P [direction=long]`.  
6. Engages OP (first journal locks shape per ADR-006).  
7. Prefer writing first-class fill columns if series **#1** is done; otherwise store in Position + `fulfillment_details` and migrate later.

## Non-goals

- LEAP/options real mechanics (separate, deferred)  
- Broker automation  
- Custom stop (series **#3** — accept optional `stop_price` stub if #3 lands same PR, else ATR default)  
- Ledger export (series **#4**)  

## Acceptance

- [x] Ad-hoc long stock fill updates position + capital_base without prior DAR draft  
- [x] Same accounting as DAR confirm path (`JournalConfirmationService` + `JournalPositionExecutor`)  
- [x] MCP `wv2_book_trade` + audit correlation_id (via MCP hop)  
- [x] Telegram skill `winston-ad-hoc-fill` + ops shell `book`  
- [x] Analysis series table #2 remains the canonical ticket for free-form book  

## Implementation (2026-07-16)

| Surface | Artifact |
|---------|----------|
| Service | `winston_v2` `Operations::AdHocPaperFillService` |
| Confirm reuse | Draft journal + enter/pyramid task → `JournalConfirmationService` |
| Stop override | Optional `stop_price` on open (else ATR default) |
| API | `POST /internal/journals/book` |
| Ops shell | `book <portfolio> <symbol> units=N price=P [direction=long] [stop=S]` |
| MCP | `wv2_book_trade` + `reply_text` |
| Skill | `ecosystem/ai/skills/winston-ad-hoc-fill/SKILL.md` (AI 1.4.6) |
| Specs | `spec/services/operations/ad_hoc_paper_fill_service_spec.rb` (7 examples) |
| Live smoke | OP `#157` MSFT 3 @ 450.25 stop 440 → journal `#39`, capital 8649.25 |

**Gotcha fixed:** do not merge Rails `params[:action]` into fill payload (controller action name polluted `action`).

## Depends on / unblocks

| Relation | Ticket |
|----------|--------|
| Prefer after | [#1 promote fill fields](2026-07-15-journal-ledger-promote-fill-fields.md) |
| Unblocks | [#3 stop on confirm](2026-07-15-journal-ledger-stop-on-confirm-and-update.md) (full litmus), [#4 export](2026-07-15-journal-ledger-export-csv-pdf.md) |

## Related

- Phase 1 proved draft-confirm path on Blue PBR62 (`2026-07-13-confirm-first-paper-journal-focus-cohort.md`)  
- `JournalConfirmationService`, `JournalPositionExecutor`  
- Confirmation skill: `ecosystem/ai/skills/winston-confirmation-loop/SKILL.md`  

## Discovery

Search: `journal-to-ledger`, `ad-hoc`, analysis ticket series #2.  
