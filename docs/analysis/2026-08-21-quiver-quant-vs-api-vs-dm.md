# Analysis: Quiver Quant site vs Quiver API vs data_manager

**Date:** 2026-08-21  
**Status:** Standing technical reference  
**Monoliths:** data_manager (DM), Winston v2 (Wv2), Winston Unit Test (WUT)  
**See:** ADR-011; CONTEXT **Alt Filing**, **Quiver Skim**, **Quiver Tracking Portfolio**; plan `ecosystem/plans/quiver-tracking-desk.md`

## Question

Can the operator’s Congress Long-Short **tracking** book come from Quiver Quantitative’s website, from the Quiver HTTP API, or from data_manager (DM) that we already own? **Priority: DM first; Quiver API only if DM cannot do the job.**

## Short answer

| Need | Source of truth | Why |
|---|---|---|
| End of Day Historical Data (EODHD) bars / Average True Range (ATR) / prices | **DM parquet** (Winston EOD Standard) | Already the bar pipeline. Tracking names must go through Symbol Demand → EODHD, never Quiver. |
| Congress / insider **events** (who filed what, file date) | **DM Alt Filings** (`quiver_filings`, `GET /internal/alt/quiver`) | ADR-011. DM holds `QUIVER_API_KEY`. Wv2 must not grow a second key. |
| Winston **reconstruction** of a 130/30 book from filings | **DM catalog** `GET /internal/alt/quiver/books/:recipe` + WUT Quiver Skim | Lab / footnote only. Not the vendor’s live holdings page. Fingerprint `qcls13030-top12x8-l30-filedate-v1`. |
| **Published** strategy holdings + `% of NAV` (what Quiver actually runs) | **Not in the API we use.** Premium **Quiver Strategies** page (login-walled tables). Operator **PDF download (HITL)** is the v1 ingest. | API datasets are trades/holdings-by-politician, not the strategy book. Unpublished lookback/score will never match published Compound Annual Growth Rate (CAGR). |

**Do not** call the Quiver API from Wv2. **Do not** scrape `quiverquant.com` in v1. **Do** store the HITL PDF like a Daily Activity Report (DAR) and parse it into a target book; **do** ask DM for parquet on those tickers.

## Evidence

| Claim | Evidence |
|---|---|
| Live strategy holdings are Premium / login-walled | `https://www.quiverquant.com/strategies/s/Congress%20Long-Short/` — Holdings / Upcoming Trades / Recently Opened / Liquidated / Rebalances. Public copy: “Sign up for Quiver Premium to see live holdings.” |
| Holdings table shape (when logged in) | Columns: Ticker, Amount, % of NAV, Return (1d), Return (Since Open). That is the tracking target, not a filing stream. |
| API is **filings**, not strategy books | DM `QuiverClient` paths: `/beta/bulk/congresstrading`, `/beta/live/congresstrading`, `/beta/live/insiders`. Hobbyist Insider **403** (2026-08-21 wrap). Docs: Congress Trades + Congress Stock Holdings (per-politician estimates), not “Congress Long-Short current book.” |
| DM already reconstructs a stand-in book | `QuiverBooks::Catalog` / `Builder`; `GET /internal/alt/quiver/books`. File-date lookback, top 12 long / 8 short, 130/30. Empty on sawtooth until `quiver.env` is mounted. |
| Wv2 copy-book is a **different** reconstruction | `Operations::QuiverCongressLongShort::FINGERPRINT` = `qcls13030-l30-filedate-v1`, caps 15/10. Must not silently mix with DM catalog `qcls13030-top12x8-l30-filedate-v1`. |
| WUT Quiver Skim is lab, not the tracking OP | CONTEXT: *Avoid treating a skim book as an Operational Portfolio.* Isolated `/quiver_skim` + `quiver_lab_*` tables. |
| Bars stay EODHD | ADR-002/003; ADR-011 “not EOD parquet.” Tracking tickers → DM `request_consumer_sync` / consumer Symbol Demand. |

## Overlap map

```text
Quiver Quant website (Premium)
  published holdings / % NAV / upcoming / opened / liquidated
  → v1: human downloads PDF → Wv2 ingest
  → later: optional login bot (separate plan; not required for tracking desk)

Quiver API (Hobbyist/Trader)
  congress bulk/live filings, insider (plan-gated)
  → DM only (ADR-011)
  → reconstruct Skim books (WUT lab, DM catalog)
  → NOT published strategy weights

DM
  Alt Filings + book catalog     (events / reconstruction)
  EODHD parquet + DataCoverage   (prices for tracking + TF)
  Symbol Demand from consumers   (pull X markets)

Wv2 Quiver Tracking Desk
  target book = parsed PDF (HITL)
  current book = paper Tracking Portfolio (starts empty)
  gap tasks = add/drop/reweight names + “DM pull parquet for X”
  journals / pending / positions / equity = tracking OP only
  Daily Analysis = skip (not TF)
```

## What the API cannot replace

- Official `% of NAV` on the Congress Long-Short strategy page.
- Upcoming trades / recently opened / liquidated / rebalance tape as Quiver publishes them.
- Insider Purchases **proprietary score** (WUT already documents the size-weighted top-20 as a stand-in).
- Matching published CAGR. ADR-011 consequence still holds.

A PDF print of the Holdings table **can** replace those for v1 if parse quality is good enough to emit tickers, sides, and weights.

## Policy (for plans/tickets)

1. **DM owns** vendor HTTP and Alt Filings. Mount `quiver.env` remains the live-sync ticket (`2026-08-20-mount-quiver-env-live-alt-filing-sync.md`). Optional: after a tracking ingest, DM reconstructs the **same as-of** Skim book so the desk can show “PDF vs filing-reconstruction” as a footnote, not as the task generator.
2. **DM owns** parquet for every ticker on the tracking book. Gap task `dm_pull` is automatic: Wv2 lists symbols → DM `request_consumer_sync` (same pattern as WUT `QuiverLab::Snapshot#enqueue_symbol_pull`).
3. **Wv2 owns** the paper Tracking Portfolio, PDF archive, gap tasks, journals, positions, equity curve. No Quiver key in Wv2.
4. **Quiver API** is not an alternate ingest for tracking holdings.
5. **Website scrape / login bot** is a later automation of the HITL PDF step (`ecosystem/plans/quiver-pdf-bot-and-scrape.md`). Not on the critical path.
6. Broker Gateway (BG) automation of fills is **not now** (`ecosystem/plans/quiver-tracking-bg-fulfillment.md`).

## Open facts to re-check on first PDF

- Exact PDF layout (print-to-PDF vs vendor export). Parser is fixture-driven.
- Whether “Amount” is shares, notional, or a display of `% of NAV`.
- Ticker noise (`GOOGN` vs `GOOG`) — reuse DM `TickerRemap` if the symbol is already in the remap table; otherwise HITL task.
- Short fractions vs broker (paper tracking can keep decimal units; real later is BG).
