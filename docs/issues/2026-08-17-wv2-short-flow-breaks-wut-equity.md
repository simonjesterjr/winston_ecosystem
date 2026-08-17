---
id: ISSUE-20260817-wv2-short-flow-breaks-wut-equity
title: Wv2 short journal flows debit cash; equity collapses vs WUT PBR identity
status: resolved
type: bug
priority: high
created: 2026-08-17
updated: 2026-08-17
labels: [winston_v2, equity, dar, ops-shell, capital]
related:
  - docs/tickets/2026-08-17-wv2-equity-wut-parity-flow-dar-shell.md
  - docs/tickets/2026-08-13-investigate-negative-risk-equity-active-ops.md
  - docs/tickets/2026-08-12-dar-risk-equity-live-render.md
  - winston_v2/app/services/operations/related_instrument_fulfillment.rb
  - winston_v2/app/services/operations/portfolio_equity_series.rb
---

# Wv2 short journal flows debit cash; equity collapses vs WUT PBR identity

**Status banner (human-readable):** Fixed in `cd37a1f` (winston_v2) — short flows backfilled; DAR + shell dual metrics verified live

Map YAML `status` ↔ banner: `resolved`.

## Summary

Winston v2 (Wv2) reports **risk equity** with the Winston Unit Test (WUT) Portfolio Backtest Run (PBR) identity `free cash + long market value − short market value`. On two-way books the number is still wrong because short enters are booked as cash **debits**. The operator shell and Daily Activity Report (DAR) then present that collapsed figure as account value, and they label free cash as `capital`.

## Problem statement

Three related defects (one capital identity, two presentation):

1. **D1 — direction-blind journal flow (root).** `RelatedInstrumentFulfillment.signed_flow` always does enter = −notional, exit = +notional. WUT credits free cash on a stock/proxy short enter and debits the buyback. Equity therefore falls by about **2 × short notional**. Option-like fulfillment (buy premium) is a separate path and must stay debit-on-enter.
2. **D2 — shell/DAR call free cash “capital.”** Ops shell `list` / `status` / `positions` print `capital=$` from `Portfolio#capital_base` (free cash). DAR summary **Total capital** sums free cash, including large long debits. Operators read that as wealth.
3. **D3 — no WUT-style recon; over-deployed inverted.** There is no cash-equity vs position-PnL delta. Over-deployed only fires when risk equity > 0, so the worst-collapsed books (negative equity) get no attention flag.

## Current behavior

- Live DAR 2026-08-16 (paper Active OPs): Mint · 0478e0ea free cash −$2,440, risk/end equity **−$14,973**, unrealized MTM only −$292, five open shorts, zero longs. SHY enter flow −$6,793.55 on a `direction=short` lot.
- Orange · 7ea76741 risk equity **−$910**; Blue · f4dd31eb **−$3,970**. Every open short journal flow is negative.
- Long-only Turtle OPs (Mint · 85730621, Yellow · 7aa73357) match WUT (~$10k).
- Reconstructing WUT signs (flip short-enter flows) restores those books to ~$9.2k–$9.8k.
- Shell panels already show `free` + `risk eq`; chat `list`/`status`/`positions` still say `capital=$` free cash.

## Expected behavior

WUT PBR cash ledger (`PortfolioPositionManager#update_cash_on_entry/exit`, `cash_snapshot`):

- Stock/proxy **long** enter −notional, exit +notional.
- Stock/proxy **short** enter +notional (sale proceeds), exit −notional (buyback).
- Equity = free cash + long MV − short MV.
- Option/LEAP enter remains −premium (purchase), exit +premium regardless of signal direction.
- Operator surfaces distinguish **free cash** (funding) from **risk equity** (account value). Household totals use risk equity.
- A recon row shows cash-identity equity vs initial + CashEvents + realized position PnL + unrealized MTM; a material gap is an attention flag even when risk equity is negative.

## Reproduction

### Preconditions

Compose `winston_v2` with Active paper OPs that have executed short stock lots (e.g. Mint #384, Orange #308, Blue #381). DAR artifact `winston_v2/storage/reports/wv2_20260816.md`.

### Steps

1. Open an Operational Portfolio with `direction=short` stock lots (or read DAR 2026-08-16 Mint · 0478e0ea).
2. Sum executed journal `flow` and compare to `Operations::RiskEquity.snapshot`.
3. Compare to WUT identity: credit short enters, then `cash + long_mv − short_mv`.

### Observed result

Short enter flows are negative. Risk equity ≈ free cash − short MV (double count). DAR End equity equals that number. Return % / max DD % show −100% to −250% on ~$10k books that are still ~flat on marks.

### Reproducibility

Always, whenever a stock/proxy short is confirmed through current `signed_flow`.

## Environment

- Monolith: winston_v2 compose service, host :3002, DB `winston_v2_dev` on :5434
- Report date: 2026-08-16
- Branch: `main` (session 2026-08-17)
- Paper Active OPs; no real-capital mutation required to observe

## Evidence

| Evidence | Source | What it establishes |
|---|---|---|
| `signed_flow` ignore direction | `winston_v2/app/services/operations/related_instrument_fulfillment.rb:62-66` | Enter always −notional |
| WUT short credits cash | `winston_unit_test/app/services/portfolio_position_manager.rb:215-247` | Gold-standard cash identity |
| Live lots + flows | `bin/compose exec winston_v2 bin/rails runner` 2026-08-17 | Every open short journal is a debit |
| DAR table | `winston_v2/storage/reports/wv2_20260816.md` | Risk equity = end equity; Mint −$14,973 |
| Shell `capital=$` | `ops_shell_chat.rb` `format_portfolio_list_line` / `portfolio_status` / `show_positions` | Free cash labeled capital |
| DAR total capital | `daily_report_payload_builder.rb` `summary` | Sums `capital_base` (free cash) |

## Impact and priority

Paper desk sizing (`PositionSizer` uses `RiskEquity.for`) under-sizes or zeros units on collapsed books. DAR/Telegram/shell tell the operator the book is ruined when marks say otherwise. **Priority: high** — capital identity on Active OPs; paper today, same code path for real.

Workaround: ignore risk equity / return % on any OP with short lots until flows are rewritten.

## Scope and preservation requirements

### In scope

- D1: direction-aware `signed_flow` for stock/proxy; pass direction from confirm/amend/ad-hoc/draft-edit
- D1: backfill executed (and provisional draft) stock/proxy short journal flows
- D2: shell + DAR labels and household totals
- D3: cash-vs-PnL recon + disagree / over-deployed attention when equity collapsed

### Must preserve

- Long-only identity (Turtle Mint/Yellow already correct)
- LEAP/option enter = −premium (do not flip option-like shorts as if they were stock sales)
- Formula `equity = cash + long_mv − short_mv`
- Human-gated fills; no Telegram broadcast unless operator asks
- Existing over-deployed 0.25 ratio as funding attention when equity is still positive

### Out of scope

- Changing WUT PBR sizing (`capital_base = initial + realized`)
- Exit Capital Reconcile / extra-modal mid-life LEAP mark-to-market
- Regenerating historical DAR PDFs for every past date (optional smoke of one current date)

## Acceptance criteria

- [x] Given a stock short enter, when confirmed, then journal `flow` is **+** units × price (and buyback is negative)
- [x] Given option/LEAP enter, when confirmed, then flow remains **−** premium even if signal direction is short
- [x] Given existing executed short stock journals, when backfill runs, then Active OP risk equity ≈ initial + CashEvents + position PnL (Mint #384 $9,507.78, not −$15k)
- [x] Given shell `list` / `status` / `positions`, when rendered, then lines show **free cash** and **risk equity**, not `capital=$` free cash
- [x] Given DAR summary, when rendered, then household total is summed **risk equity**; free cash is not titled Total capital
- [x] Given a book whose cash-identity equity disagrees with position-PnL equity by more than a small epsilon, when DAR/shell snapshot, then a disagree flag is visible even if risk equity is negative
- [x] Existing long-only RiskEquity / PositionSizer / DAR renderer specs still pass

## Investigation notes

Confirmed 2026-08-17 from live journals:

| OP | Shown risk equity | Short-enter notionals | WUT-parity equity |
|----|------------------:|----------------------:|------------------:|
| Rust · dd7e7c7a | 3,399 | 3,198 | ~9,795 |
| Orange · 7ea76741 | −910 | 5,197 | ~9,484 |
| Blue · f4dd31eb | −3,970 | 6,569 | ~9,168 |
| Mint · 0478e0ea | −14,973 | 12,240 | ~9,508 |
| Mango · 45c09e30 | 2,414 | 3,718 | ~9,850 |
| Mint Turtle · 85730621 | 10,001 | 0 | 10,001 |
| Yellow Turtle · 7aa73357 | 9,997 | 0 | 9,997 |

Unrealized MTM on Mint #384 is −$292; the −$15k hole is cash sign, not marks.

`Portfolio#capital_base` comment still says “realized P&L”; it is free cash (CashEvents + signed notionals).

## Unknowns and clarifying questions

- [x] Operator authorized fix + backfill + presentation (2026-08-17 chat).
- [ ] Whether to rewrite historical DAR markdown/PDF archives or only going-forward / one smoke date.

## Dependencies and risks

- Backfill mutates `journals.flow` (paper series). Must be idempotent and skip option-like rows.
- Draft journals with unsigned positive flow do not enter `capital_base` (executed only) but should be rewritten so confirm/presenters match.
- `debit_credit` on draft-edit currently assumes enter=debit; short stock enter is a credit.

## Verification plan

- Specs: `related_instrument_fulfillment`, confirmation/amend/ad-hoc callers, `risk_equity`, `portfolio_equity_series`, DAR markdown/PDF, ops shell chat
- Compose: `bin/compose exec -T winston_v2 bundle exec rspec <paths>`
- Live: backfill dry-run then apply; re-snapshot Active OPs; confirm Mint #384 risk equity ~$9.5k
- Optional: rebuild DAR markdown for current report date **without Telegram**

## History

- 2026-08-17 — Created from WUT-vs-Wv2 equity evaluation (live DAR 2026-08-16 + rails runner lot dump). Three defects: D1 flow sign, D2 capital label/totals, D3 recon/flag.
- 2026-08-17 — Implemented in winston_v2 `cd37a1f`. `signed_flow` takes direction; 30 paper journals backfilled; DAR 2026-08-16 regenerated (no Telegram send). Live: Mint #384 risk equity $9,507.78, all Active cash_vs_pnl_delta = 0. Specs: 73 examples, 0 failures on the combined suite.
